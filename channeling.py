"""
🔗 تحلیل و ایجاد کانال‌های قیمتی NEOWave
نسخه کامل و حرفه‌ای با تمام قابلیت‌ها

- کانال‌های موازی
- کانال‌های همگرا  
- کانال‌های الیوت
- پروژکشن قیمتی دقیق
"""

import numpy as np
import pandas as pd
import logging
from typing import List, Tuple, Dict, Optional, Union
from scipy import stats
from dataclasses import dataclass
from enum import Enum
import matplotlib.pyplot as plt
from datetime import datetime

logger = logging.getLogger(__name__)

class ChannelType(Enum):
    """انواع کانال‌ها"""
    PARALLEL = "parallel"
    CONVERGING = "converging" 
    DIVERGING = "diverging"
    ELLIOTT = "elliott"
    ACCELERATION = "acceleration"
    BASE = "base"

@dataclass
class TrendLine:
    """خط روند"""
    slope: float
    intercept: float
    r_squared: float
    start_point: Tuple[float, float]
    end_point: Tuple[float, float]
    points_used: List[Tuple[float, float]]
    confidence: float = 0.0
    
    def calculate_y(self, x: float) -> float:
        """محاسبه Y برای X داده شده"""
        return self.slope * x + self.intercept
        
    def calculate_x(self, y: float) -> float:
        """محاسبه X برای Y داده شده"""
        if abs(self.slope) < 1e-10:
            return float('inf')
        return (y - self.intercept) / self.slope
        
    def distance_to_point(self, point: Tuple[float, float]) -> float:
        """فاصله نقطه تا خط"""
        x, y = point
        return abs(self.slope * x - y + self.intercept) / np.sqrt(self.slope**2 + 1)

@dataclass  
class Channel:
    """کانال قیمتی"""
    channel_id: str
    channel_type: ChannelType
    upper_line: TrendLine
    lower_line: TrendLine
    midline: Optional[TrendLine] = None
    width: float = 0.0
    angle: float = 0.0
    strength: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0
    breakout_target: Optional[float] = None
    confluence_points: List[Tuple[float, float]] = None
    
    def __post_init__(self):
        if self.confluence_points is None:
            self.confluence_points = []

class ChannelAnalyzer:
    """تحلیلگر کانال‌های قیمتی"""
    
    def __init__(self, data: pd.DataFrame):
        """راه‌اندازی تحلیلگر کانال"""
        if data is None or data.empty:
            raise ValueError("داده‌های قیمتی نمی‌تواند خالی باشد")
            
        # اعتبارسنجی ستون‌های مورد نیاز
        required_columns = ['open', 'high', 'low', 'close']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"ستون‌های مورد نیاز وجود ندارد: {missing_columns}")
            
        self.data = data.copy()
        self.channels: List[Channel] = []
        
        # اضافه کردن index زمانی اگر وجود ندارد
        if not isinstance(data.index, pd.DatetimeIndex):
            self.data.index = pd.to_datetime(self.data.index)
            
        logger.info(f"📊 ChannelAnalyzer راه‌اندازی شد با {len(data)} کندل")
        
    def create_parallel_channel(self, 
                              wave_points: List[Tuple[float, float, str]],
                              min_touches: int = 2,
                              tolerance: float = 0.02) -> Optional[Channel]:
        """
        ایجاد کانال موازی از نقاط امواج
        
        Args:
            wave_points: لیست نقاط (time, price, type)
            min_touches: حداقل تعداد تماس با خط
            tolerance: تلرانس قیمتی (درصد)
        """
        try:
            if len(wave_points) < 4:
                logger.warning("⚠️ برای کانال موازی حداقل 4 نقطه نیاز است")
                return None
                
            # جداسازی نقاط بالا و پایین
            highs = [(p[0], p[1]) for p in wave_points if p[2] == 'HIGH']
            lows = [(p[0], p[1]) for p in wave_points if p[2] == 'LOW']
            
            if len(highs) < min_touches or len(lows) < min_touches:
                logger.warning(f"⚠️ تعداد نقاط کافی نیست: بالا={len(highs)}, پایین={len(lows)}")
                return None
                
            # محاسبه خطوط روند
            upper_line = self._fit_trendline(highs, "upper")
            lower_line = self._fit_trendline(lows, "lower")
            
            if not upper_line or not lower_line:
                logger.warning("⚠️ نتوانست خطوط روند محاسبه کند")
                return None
                
            # بررسی موازی بودن
            slope_diff = abs(upper_line.slope - lower_line.slope)
            max_slope = max(abs(upper_line.slope), abs(lower_line.slope), 1e-6)
            
            if slope_diff / max_slope > tolerance:
                logger.info("💡 خطوط کاملاً موازی نیستند، تنظیم می‌کنیم...")
                # میانگین شیب
                avg_slope = (upper_line.slope + lower_line.slope) / 2
                
                # تنظیم خطوط
                upper_line = self._adjust_trendline(highs, avg_slope, "upper")
                lower_line = self._adjust_trendline(lows, avg_slope, "lower")
                
            # محاسبه خط میانی
            midline = self._calculate_midline(upper_line, lower_line)
            
            # محاسبه عرض و زاویه
            width = self._calculate_channel_width(upper_line, lower_line)
            angle = np.degrees(np.arctan(upper_line.slope))
            
            # قدرت کانال
            strength = self._calculate_channel_strength(wave_points, upper_line, lower_line)
            
            channel = Channel(
                channel_id=f"parallel_{datetime.now().strftime('%H%M%S')}",
                channel_type=ChannelType.PARALLEL,
                upper_line=upper_line,
                lower_line=lower_line,
                midline=midline,
                width=width,
                angle=angle,
                strength=strength,
                start_time=min(p[0] for p in wave_points),
                end_time=max(p[0] for p in wave_points),
                breakout_target=self._calculate_breakout_target(upper_line, lower_line, width)
            )
            
            self.channels.append(channel)
            logger.info(f"✅ کانال موازی ایجاد شد - عرض: {width:.2f}, زاویه: {angle:.1f}°")
            
            return channel
            
        except Exception as e:
            logger.error(f"❌ خطا در ایجاد کانال موازی: {e}")
            return None
            
    def create_converging_channel(self, 
                                triangle_points: List[Tuple[float, float, str]],
                                convergence_threshold: float = 0.1) -> Optional[Channel]:
        """
        ایجاد کانال همگرا (مثلث)
        
        Args:
            triangle_points: نقاط مثلث
            convergence_threshold: آستانه همگرایی
        """
        try:
            if len(triangle_points) < 5:
                logger.warning("⚠️ برای کانال همگرا حداقل 5 نقطه نیاز است")
                return None
                
            # جداسازی نقاط
            highs = [(p[0], p[1]) for p in triangle_points if p[2] == 'HIGH']
            lows = [(p[0], p[1]) for p in triangle_points if p[2] == 'LOW']
            
            if len(highs) < 2 or len(lows) < 2:
                return None
                
            # محاسبه خطوط با روند نزولی/صعودی
            upper_line = self._fit_trendline(highs, "upper")
            lower_line = self._fit_trendline(lows, "lower")
            
            if not upper_line or not lower_line:
                return None
                
            # بررسی همگرایی
            if not self._is_converging(upper_line, lower_line, convergence_threshold):
                logger.warning("⚠️ خطوط به اندازه کافی همگرا نیستند")
                return None
                
            # نقطه تلاقی (Apex)
            apex = self._find_intersection(upper_line, lower_line)
            
            if not apex:
                logger.warning("⚠️ نقطه تلاقی یافت نشد")
                return None
                
            # محاسبه نرخ همگرایی
            convergence_rate = abs(upper_line.slope - lower_line.slope)
            
            # پروژکشن زمانی تا Apex
            current_time = max(p[0] for p in triangle_points)
            time_to_apex = max(0, apex[0] - current_time)
            
            channel = Channel(
                channel_id=f"converging_{datetime.now().strftime('%H%M%S')}",
                channel_type=ChannelType.CONVERGING,
                upper_line=upper_line,
                lower_line=lower_line,
                width=convergence_rate,  # نرخ همگرایی به جای عرض
                angle=np.degrees(np.arctan((upper_line.slope + lower_line.slope) / 2)),
                strength=self._calculate_channel_strength(triangle_points, upper_line, lower_line),
                start_time=min(p[0] for p in triangle_points),
                end_time=apex[0],
                confluence_points=[apex],
                breakout_target=self._calculate_triangle_breakout(triangle_points, apex)
            )
            
            self.channels.append(channel)
            logger.info(f"✅ کانال همگرا ایجاد شد - Apex: ({apex[0]:.0f}, {apex[1]:.2f})")
            
            return channel
            
        except Exception as e:
            logger.error(f"❌ خطا در ایجاد کانال همگرا: {e}")
            return None
            
    def create_elliott_channel(self, impulse_waves: List[Dict]) -> Optional[Channel]:
        """
        ایجاد کانال مخصوص امواج الیوت
        
        Args:
            impulse_waves: لیست امواج شتابدار 1-2-3-4-5
        """
        try:
            if len(impulse_waves) < 4:
                logger.warning("⚠️ برای کانال الیوت حداقل 4 موج نیاز است")
                return None
                
            # اعتبارسنجی ساختار موج
            if not self._validate_elliott_structure(impulse_waves):
                logger.warning("⚠️ ساختار امواج الیوت معتبر نیست")
                return None
                
            # کانال پایه 0-2-4
            base_points = [
                (impulse_waves[0]['start_time'], impulse_waves[0]['start_price']),  # شروع موج 1
                (impulse_waves[1]['end_time'], impulse_waves[1]['end_price']),    # انتهای موج 2
                (impulse_waves[3]['end_time'], impulse_waves[3]['end_price'])     # انتهای موج 4
            ]
            
            base_line = self._fit_trendline(base_points, "base")
            if not base_line:
                logger.warning("⚠️ نتوانست خط پایه محاسبه کند")
                return None
                
            # خط موازی از قله موج 1 یا 3
            wave1_peak = (impulse_waves[0]['end_time'], impulse_waves[0]['end_price'])
            wave3_peak = (impulse_waves[2]['end_time'], impulse_waves[2]['end_price'])
            
            # انتخاب قله بالاتر برای خط موازی
            parallel_point = wave3_peak if wave3_peak[1] > wave1_peak[1] else wave1_peak
            
            parallel_line = self._create_parallel_line(base_line, parallel_point)
            
            # پروژکشن موج 5
            wave5_projection = self._project_wave5_elliott(
                impulse_waves, base_line, parallel_line
            )
            
            # محاسبه کانال شتاب 1-3-5
            acceleration_points = [
                wave1_peak,
                wave3_peak
            ]
            
            # اضافه کردن موج 5 اگر وجود دارد
            if len(impulse_waves) >= 5:
                wave5_peak = (impulse_waves[4]['end_time'], impulse_waves[4]['end_price'])
                acceleration_points.append(wave5_peak)
                
            acceleration_line = self._fit_trendline(acceleration_points, "acceleration")
            
            # عرض کانال
            width = self._calculate_channel_width(parallel_line, base_line)
            
            channel = Channel(
                channel_id=f"elliott_{datetime.now().strftime('%H%M%S')}",
                channel_type=ChannelType.ELLIOTT,
                upper_line=parallel_line,
                lower_line=base_line,
                midline=self._calculate_midline(parallel_line, base_line),
                width=width,
                angle=np.degrees(np.arctan(base_line.slope)),
                strength=self._calculate_elliott_strength(impulse_waves),
                start_time=impulse_waves[0]['start_time'],
                end_time=impulse_waves[-1]['end_time'],
                breakout_target=wave5_projection.get('target_price'),
                confluence_points=[(wave5_projection.get('target_time', 0), 
                                  wave5_projection.get('target_price', 0))]
            )
            
            self.channels.append(channel)
            logger.info(f"✅ کانال الیوت ایجاد شد - هدف موج 5: {wave5_projection.get('target_price', 0):.2f}")
            
            return channel
            
        except Exception as e:
            logger.error(f"❌ خطا در ایجاد کانال الیوت: {e}")
            return None
    
    def find_channel_breakouts(self, channel: Channel, 
                             sensitivity: float = 0.01) -> List[Dict]:
        """
        شناسایی شکست کانال
        
        Args:
            channel: کانال مورد بررسی
            sensitivity: حساسیت شکست (درصد)
        """
        breakouts = []
        
        try:
            # فیلتر کردن داده‌ها در بازه زمانی کانال
            start_idx = self.data.index.get_loc(pd.Timestamp(channel.start_time))
            end_idx = min(start_idx + 100, len(self.data) - 1)  # محدود کردن بررسی
            
            channel_data = self.data.iloc[start_idx:end_idx]
            
            for idx, row in channel_data.iterrows():
                timestamp = idx.timestamp()
                
                # محاسبه سطوح کانال در این زمان
                upper_level = channel.upper_line.calculate_y(timestamp)
                lower_level = channel.lower_line.calculate_y(timestamp)
                
                # بررسی شکست سقف
                if row['high'] > upper_level * (1 + sensitivity):
                    breakout = {
                        'time': timestamp,
                        'type': 'upward',
                        'price': row['high'],
                        'channel_level': upper_level,
                        'strength': (row['high'] - upper_level) / upper_level,
                        'volume': row.get('volume', 0)
                    }
                    breakouts.append(breakout)
                    
                # بررسی شکست کف
                elif row['low'] < lower_level * (1 - sensitivity):
                    breakout = {
                        'time': timestamp,
                        'type': 'downward',
                        'price': row['low'],
                        'channel_level': lower_level,
                        'strength': (lower_level - row['low']) / lower_level,
                        'volume': row.get('volume', 0)
                    }
                    breakouts.append(breakout)
                    
            logger.info(f"🔍 {len(breakouts)} شکست کانال شناسایی شد")
            return breakouts
            
        except Exception as e:
            logger.error(f"❌ خطا در شناسایی شکست: {e}")
            return []
    
    def get_channel_support_resistance(self, channel: Channel, 
                                     future_periods: int = 50) -> Dict:
        """
        محاسبه سطوح حمایت و مقاومت آینده کانال
        """
        try:
            current_time = self.data.index[-1].timestamp()
            future_times = [current_time + i * 3600 for i in range(1, future_periods + 1)]  # هر ساعت
            
            support_levels = []
            resistance_levels = []
            
            for time in future_times:
                resistance = channel.upper_line.calculate_y(time)
                support = channel.lower_line.calculate_y(time)
                
                resistance_levels.append({
                    'time': time,
                    'price': resistance,
                    'strength': channel.strength
                })
                
                support_levels.append({
                    'time': time,
                    'price': support,
                    'strength': channel.strength
                })
                
            return {
                'resistance_levels': resistance_levels,
                'support_levels': support_levels,
                'midline_levels': [
                    {
                        'time': time,
                        'price': channel.midline.calculate_y(time) if channel.midline else 
                               (resistance_levels[i]['price'] + support_levels[i]['price']) / 2,
                        'strength': channel.strength * 0.7
                    }
                    for i, time in enumerate(future_times)
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ خطا در محاسبه سطوح: {e}")
            return {}
            
    def _fit_trendline(self, points: List[Tuple[float, float]], 
                       line_type: str = "trend") -> Optional[TrendLine]:
        """محاسبه خط روند با رگرسیون خطی بهبود یافته"""
        if len(points) < 2:
            return None
            
        try:
            x = np.array([p[0] for p in points])
            y = np.array([p[1] for p in points])
            
            # حذف outliers
            if len(points) > 3:
                # Z-score برای شناسایی outliers
                z_scores = np.abs(stats.zscore(y))
                valid_indices = z_scores < 2.5
                x = x[valid_indices]
                y = y[valid_indices]
                points = [points[i] for i, valid in enumerate(valid_indices) if valid]
                
            if len(x) < 2:
                return None
                
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            # محاسبه confidence
            confidence = r_value ** 2 * (1 - p_value) if p_value < 0.05 else r_value ** 2 * 0.5
            
            return TrendLine(
                slope=slope,
                intercept=intercept,
                r_squared=r_value ** 2,
                start_point=(x[0], slope * x[0] + intercept),
                end_point=(x[-1], slope * x[-1] + intercept),
                points_used=points,
                confidence=confidence
            )
            
        except Exception as e:
            logger.error(f"❌ خطا در محاسبه خط روند: {e}")
            return None
    
    def _adjust_trendline(self, points: List[Tuple[float, float]], 
                         target_slope: float, line_type: str) -> Optional[TrendLine]:
        """تنظیم خط روند با شیب مشخص"""
        if len(points) < 2:
            return None
            
        try:
            x = np.array([p[0] for p in points])
            y = np.array([p[1] for p in points])
            
            # محاسبه intercept با شیب ثابت
            # y = mx + b -> b = y - mx
            intercepts = y - target_slope * x
            avg_intercept = np.mean(intercepts)
            
            # محاسبه R-squared با شیب ثابت
            y_pred = target_slope * x + avg_intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            return TrendLine(
                slope=target_slope,
                intercept=avg_intercept,
                r_squared=max(0, r_squared),
                start_point=(x[0], target_slope * x[0] + avg_intercept),
                end_point=(x[-1], target_slope * x[-1] + avg_intercept),
                points_used=points,
                confidence=r_squared
            )
            
        except Exception as e:
            logger.error(f"❌ خطا در تنظیم خط روند: {e}")
            return None
            
    def _calculate_midline(self, upper_line: TrendLine, 
                          lower_line: TrendLine) -> TrendLine:
        """محاسبه خط میانی"""
        return TrendLine(
            slope=(upper_line.slope + lower_line.slope) / 2,
            intercept=(upper_line.intercept + lower_line.intercept) / 2,
            r_squared=(upper_line.r_squared + lower_line.r_squared) / 2,
            start_point=((upper_line.start_point[0] + lower_line.start_point[0]) / 2,
                        (upper_line.start_point[1] + lower_line.start_point[1]) / 2),
            end_point=((upper_line.end_point[0] + lower_line.end_point[0]) / 2,
                      (upper_line.end_point[1] + lower_line.end_point[1]) / 2),
            points_used=[],
            confidence=(upper_line.confidence + lower_line.confidence) / 2
        )
        
    def _calculate_channel_width(self, upper_line: TrendLine, 
                               lower_line: TrendLine) -> float:
        """محاسبه عرض کانال"""
        try:
            # فاصله عمودی متوسط بین دو خط
            mid_time = (upper_line.start_point[0] + upper_line.end_point[0]) / 2
            upper_y = upper_line.calculate_y(mid_time)
            lower_y = lower_line.calculate_y(mid_time)
            
            return abs(upper_y - lower_y)
            
        except Exception as e:
            logger.error(f"❌ خطا در محاسبه عرض کانال: {e}")
            return 0.0
            
    def _calculate_channel_strength(self, points: List[Tuple], 
                                  upper_line: TrendLine, 
                                  lower_line: TrendLine) -> float:
        """محاسبه قدرت کانال"""
        try:
            # قدرت بر اساس:
            # 1. تعداد تماس‌ها
            # 2. دقت خطوط (R-squared)
            # 3. طول زمانی
            
            touch_count = len(points)
            avg_r_squared = (upper_line.r_squared + lower_line.r_squared) / 2
            
            # امتیاز تماس
            touch_score = min(touch_count / 6.0, 1.0)  # حداکثر 6 تماس
            
            # امتیاز دقت  
            accuracy_score = avg_r_squared
            
            # امتیاز confidence
            confidence_score = (upper_line.confidence + lower_line.confidence) / 2
            
            # ترکیب امتیازها
            strength = (touch_score * 0.4 + accuracy_score * 0.3 + confidence_score * 0.3)
            
            return min(strength, 1.0)
            
        except Exception as e:
            logger.error(f"❌ خطا در محاسبه قدرت کانال: {e}")
            return 0.0
            
    def _calculate_breakout_target(self, upper_line: TrendLine, 
                                 lower_line: TrendLine, width: float) -> float:
        """محاسبه هدف شکست کانال"""
        try:
            # هدف معمولاً برابر عرض کانال است
            current_time = max(upper_line.end_point[0], lower_line.end_point[0])
            upper_price = upper_line.calculate_y(current_time)
            
            # هدف صعودی
            return upper_price + width
            
        except Exception as e:
            logger.error(f"❌ خطا در محاسبه هدف شکست: {e}")
            return 0.0
            
    def _find_intersection(self, line1: TrendLine, line2: TrendLine) -> Optional[Tuple[float, float]]:
        """یافتن نقطه تقاطع دو خط"""
        try:
            slope_diff = line1.slope - line2.slope
            if abs(slope_diff) < 1e-10:
                return None  # خطوط موازی
                
            x = (line2.intercept - line1.intercept) / slope_diff
            y = line1.slope * x + line1.intercept
            
            return (x, y)
            
        except Exception as e:
            logger.error(f"❌ خطا در یافتن تقاطع: {e}")
            return None
            
    def _is_converging(self, upper_line: TrendLine, lower_line: TrendLine, 
                      threshold: float) -> bool:
        """بررسی همگرایی خطوط"""
        try:
            # شیب خط بالا باید منفی یا کمتر از خط پایین باشد
            return upper_line.slope < lower_line.slope - threshold
            
        except:
            return False
            
    def _create_parallel_line(self, base_line: TrendLine, 
                            point: Tuple[float, float]) -> TrendLine:
        """ایجاد خط موازی از نقطه مشخص"""
        try:
            x, y = point
            # intercept = y - slope * x
            new_intercept = y - base_line.slope * x
            
            return TrendLine(
                slope=base_line.slope,
                intercept=new_intercept,
                r_squared=base_line.r_squared,
                start_point=(base_line.start_point[0], 
                           base_line.slope * base_line.start_point[0] + new_intercept),
                end_point=(base_line.end_point[0],
                          base_line.slope * base_line.end_point[0] + new_intercept),
                points_used=[point],
                confidence=base_line.confidence * 0.8  # کمی کمتر از خط اصلی
            )
            
        except Exception as e:
            logger.error(f"❌ خطا در ایجاد خط موازی: {e}")
            return base_line
            
    def _validate_elliott_structure(self, waves: List[Dict]) -> bool:
        """اعتبارسنجی ساختار امواج الیوت"""
        try:
            if len(waves) < 4:
                return False
                
            # بررسی کلیدهای مورد نیاز
            required_keys = ['start_time', 'end_time', 'start_price', 'end_price']
            for wave in waves:
                if not all(key in wave for key in required_keys):
                    return False
                    
            # موج 2 نباید زیر شروع موج 1 برود
            if waves[1]['end_price'] <= waves[0]['start_price']:
                return False
                
            # موج 4 نباید با موج 1 همپوشانی داشته باشد
            if len(waves) >= 4:
                wave1_range = (waves[0]['start_price'], waves[0]['end_price'])
                wave4_price = waves[3]['end_price']
                
                if (min(wave1_range) <= wave4_price <= max(wave1_range)):
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"❌ خطا در اعتبارسنجی امواج: {e}")
            return False
            
    def _project_wave5_elliott(self, waves: List[Dict], base_line: TrendLine, 
                             parallel_line: TrendLine) -> Dict:
        """پروژکشن موج 5 الیوت"""
        try:
            if len(waves) < 4:
                return {}
                
            wave4_end = waves[3]['end_price']
            wave4_time = waves[3]['end_time']
            
            # محاسبه نسبت‌های فیبوناچی معمول
            wave1_length = abs(waves[0]['end_price'] - waves[0]['start_price'])
            wave3_length = abs(waves[2]['end_price'] - waves[2]['start_price'])
            
            # هدف اول: 0.618 * موج 1
            target1 = wave4_end + (0.618 * wave1_length)
            
            # هدف دوم: برابر موج 1  
            target2 = wave4_end + wave1_length
            
            # هدف سوم: 1.618 * موج 1
            target3 = wave4_end + (1.618 * wave1_length)
            
            # تقاطع با خط کانال بالایی
            wave3_slope = (waves[2]['end_price'] - waves[2]['start_price']) / \
                         (waves[2]['end_time'] - waves[2]['start_time'])
                         
            # زمان رسیدن به کانال
            time_to_channel = (parallel_line.intercept - wave4_end + 
                             wave3_slope * wave4_time) / wave3_slope
            channel_target = parallel_line.calculate_y(time_to_channel)
            
            # انتخاب بهترین هدف
            targets = [target1, target2, target3, channel_target]
            best_target = min(targets, key=lambda x: abs(x - channel_target))
            
            return {
                'target_price': best_target,
                'target_time': time_to_channel,
                'fibonacci_targets': {
                    '0.618': target1,
                    '1.0': target2, 
                    '1.618': target3
                },
                'channel_target': channel_target,
                'confidence': 0.75 if best_target == channel_target else 0.65
            }
            
        except Exception as e:
            logger.error(f"❌ خطا در پروژکشن موج 5: {e}")
            return {}
            
    def _calculate_elliott_strength(self, waves: List[Dict]) -> float:
        """محاسبه قدرت کانال الیوت"""
        try:
            if len(waves) < 3:
                return 0.0
                
            # قدرت بر اساس:
            # 1. رعایت قوانین الیوت
            # 2. نسبت‌های فیبوناچی
            # 3. طول و قدرت امواج
            
            strength = 0.0
            
            # موج 3 بلندترین باشد
            wave1_len = abs(waves[0]['end_price'] - waves[0]['start_price'])
            wave3_len = abs(waves[2]['end_price'] - waves[2]['start_price']) if len(waves) > 2 else 0
            wave5_len = abs(waves[4]['end_price'] - waves[4]['start_price']) if len(waves) > 4 else 0
            
            if wave3_len > wave1_len and (len(waves) < 5 or wave3_len > wave5_len):
                strength += 0.3
                
            # نسبت‌های فیبوناچی
            if len(waves) >= 2:
                wave2_retracement = abs(waves[1]['end_price'] - waves[0]['end_price']) / wave1_len
                if 0.5 <= wave2_retracement <= 0.618:
                    strength += 0.2
                    
            if len(waves) >= 4:
                wave4_retracement = abs(waves[3]['end_price'] - waves[2]['end_price']) / wave3_len
                if 0.236 <= wave4_retracement <= 0.5:
                    strength += 0.2
                    
            # تعداد امواج کامل
            if len(waves) >= 5:
                strength += 0.3
                
            return min(strength, 1.0)
            
        except Exception as e:
            logger.error(f"❌ خطا در محاسبه قدرت الیوت: {e}")
            return 0.0
            
    def _calculate_triangle_breakout(self, points: List[Tuple], 
                                   apex: Tuple[float, float]) -> float:
        """محاسبه هدف شکست مثلث"""
        try:
            # عرض مثلث در شروع
            price_points = [p[1] for p in points]
            triangle_width = max(price_points) - min(price_points)
            
            # هدف شکست = عرض اولیه مثلث
            return apex[1] + triangle_width
            
        except Exception as e:
            logger.error(f"❌ خطا در محاسبه هدف مثلث: {e}")
            return 0.0
    
    def get_all_channels(self) -> List[Channel]:
        """دریافت تمام کانال‌ها"""
        return self.channels.copy()
        
    def get_active_channels(self, current_time: Optional[float] = None) -> List[Channel]:
        """دریافت کانال‌های فعال"""
        if current_time is None:
            current_time = self.data.index[-1].timestamp()
            
        return [ch for ch in self.channels if ch.start_time <= current_time <= ch.end_time]
        
    def clear_channels(self):
        """پاک کردن تمام کانال‌ها"""
        self.channels.clear()
        logger.info("🗑️ تمام کانال‌ها پاک شدند")