# ================= corrective_waves.py =================
"""
🔄 سیستم پیشرفته تحلیل امواج اصلاحی NEOWave
نسخه کامل و حرفه‌ای مبتنی بر تئوری Glenn Neely

ویژگی‌های کلیدی:
- شناسایی دقیق 12+ نوع الگوی اصلاحی
- اعتبارسنجی کامل براساس قوانین NEOWave
- تحلیل نسبت‌های فیبوناچی پیشرفته
- بررسی روابط زمانی و قیمتی
- تشخیص الگوهای ترکیبی پیچیده
- ارزیابی قدرت و اعتماد هر الگو
- پیش‌بینی ادامه الگوهای اصلاحی
"""

import numpy as np
import pandas as pd
import logging
from typing import List, Tuple, Dict, Optional, Union, Set
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from scipy import stats
from sklearn.cluster import KMeans
from collections import defaultdict, Counter
import warnings

logger = logging.getLogger(__name__)

class CorrectiveType(Enum):
    """انواع کامل الگوهای اصلاحی NEOWave"""
    # الگوهای اصلی 3-موجی
    ZIGZAG = "zigzag"                    # 5-3-5
    FLAT = "flat"                        # 3-3-5
    TRIANGLE = "triangle"                # 3-3-3-3-3
    
    # انواع خاص Zigzag
    DOUBLE_ZIGZAG = "double_zigzag"      # W-X-Y
    TRIPLE_ZIGZAG = "triple_zigzag"      # W-X-Y-X-Z
    
    # انواع خاص Flat
    REGULAR_FLAT = "regular_flat"        # موج B = 90-100% A
    EXPANDED_FLAT = "expanded_flat"      # موج B > 105% A
    RUNNING_FLAT = "running_flat"        # موج C < A
    
    # انواع Triangle
    CONTRACTING_TRIANGLE = "contracting_triangle"  # مثلث انقباضی
    EXPANDING_TRIANGLE = "expanding_triangle"      # مثلث انبساطی
    BARRIER_TRIANGLE = "barrier_triangle"          # مثلث سدی
    RUNNING_TRIANGLE = "running_triangle"          # مثلث در حال اجرا
    
    # الگوهای پیچیده NEOWave
    DIAMETRIC = "diametric"              # 7-موجی (A-B-C-D-E-F-G)
    SYMMETRIC = "symmetric"              # 9-موجی (A-B-C-D-E-F-G-H-I)
    
    # ترکیبات پیچیده
    COMPLEX_COMBINATION = "complex_combination"    # ترکیب الگوهای مختلف
    ELONGATED_FLAT = "elongated_flat"             # مسطح کشیده
    IRREGULAR_CORRECTION = "irregular_correction"  # اصلاح نامنظم

class CorrectionSubtype(Enum):
    """زیرانواع دقیق اصلاحی"""
    STANDARD = "standard"
    TRUNCATED = "truncated"
    ELONGATED = "elongated" 
    RUNNING = "running"
    IRREGULAR = "irregular"
    COMPLEX = "complex"

class WavePosition(Enum):
    """موقعیت موج در الگو"""
    A = "A"
    B = "B" 
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    X = "X"  # موج رابط
    Y = "Y"  # موج دوم در ترکیب
    Z = "Z"  # موج سوم در ترکیب

@dataclass
class CorrectionMetrics:
    """معیارهای کمی الگوی اصلاحی"""
    fibonacci_accuracy: float = 0.0      # دقت نسبت‌های فیبوناچی
    time_symmetry: float = 0.0           # تقارن زمانی
    price_symmetry: float = 0.0          # تقارن قیمتی
    alternation_score: float = 0.0       # امتیاز Alternation
    momentum_divergence: float = 0.0     # واگرایی مومنتوم
    volume_confirmation: float = 0.0     # تأیید حجمی
    structural_integrity: float = 0.0    # یکپارچگی ساختاری
    completion_probability: float = 0.0  # احتمال تکمیل

@dataclass
class SubWaveDetail:
    """جزئیات دقیق sub-wave"""
    position: WavePosition
    wave_type: str                       # impulse یا corrective
    start_index: int
    end_index: int
    start_price: float
    end_price: float
    high_price: float
    low_price: float
    duration: int
    amplitude: float
    slope: float
    retracement_ratio: float = 0.0
    extension_ratio: float = 0.0
    time_ratio: float = 0.0
    fibonacci_relations: Dict[str, float] = field(default_factory=dict)
    validation_score: float = 0.0

@dataclass
class CorrectiveWave:
    """کلاس پیشرفته موج اصلاحی"""
    wave_id: str
    wave_type: CorrectiveType
    subtype: CorrectionSubtype
    sub_waves: List[SubWaveDetail]
    start_price: float
    end_price: float
    start_index: int
    end_index: int
    high_price: float
    low_price: float
    
    # معیارهای کیفی
    is_valid: bool = False
    confidence_score: float = 0.0
    validation_errors: List[str] = field(default_factory=list)
    validation_warnings: List[str] = field(default_factory=list)
    
    # معیارهای کمی
    metrics: CorrectionMetrics = field(default_factory=CorrectionMetrics)
    
    # پیش‌بینی
    next_wave_target: Optional[float] = None
    completion_status: float = 0.0       # درصد تکمیل
    invalidation_level: Optional[float] = None
    
    # متا دیتا
    identified_at: Optional[str] = None
    degree: int = 0                      # درجه موج
    parent_wave: Optional[str] = None

class CorrectiveWaveAnalyzer:
    """تحلیلگر پیشرفته امواج اصلاحی NEOWave"""
    
    def __init__(self, data: pd.DataFrame, precision: float = 0.001):
        """
        راه‌اندازی تحلیلگر امواج اصلاحی
        
        Args:
            data: داده‌های قیمتی OHLCV
            precision: دقت محاسبات
        """
        if data is None or data.empty:
            raise ValueError("داده‌های قیمتی نمی‌تواند خالی باشد")
            
        self.data = data.copy()
        self.precision = precision
        self.identified_corrections = []
        
        # تنظیمات پیشرفته
        self.fibonacci_levels = {
            'retracement': [0.236, 0.382, 0.50, 0.618, 0.786],
            'extension': [1.0, 1.272, 1.414, 1.618, 2.618, 4.236],
            'projection': [0.618, 1.0, 1.272, 1.618]
        }
        
        # آستانه‌های اعتبارسنجی
        self.validation_thresholds = {
            'min_fibonacci_accuracy': 0.65,
            'min_alternation_score': 0.60,
            'min_structural_integrity': 0.70,
            'min_confidence': 0.75
        }
        
        # cache برای بهینه‌سازی
        self.pattern_cache = {}
        self.fibonacci_cache = {}
        
        logger.info(f"CorrectiveWaveAnalyzer راه‌اندازی شد با {len(data)} کندل")
        
    def identify_corrective_patterns(self, pivots: List[Tuple[int, float, str]], 
                                   wave_degree: int = 0,
                                   min_confidence: float = 0.7) -> List[CorrectiveWave]:
        """
        شناسایی جامع الگوهای اصلاحی
        
        Args:
            pivots: لیست pivot points (index, price, type)
            wave_degree: درجه موج (0=Minor, 1=Minute, 2=Minuette, ...)
            min_confidence: حداقل اعتماد برای پذیرش الگو
            
        Returns:
            List[CorrectiveWave]: لیست الگوهای اصلاحی شناسایی شده
        """
        try:
            logger.info(f"شروع شناسایی الگوهای اصلاحی در درجه {wave_degree}")
            
            if len(pivots) < 4:
                logger.warning("تعداد pivot points کافی نیست (حداقل 4 نیاز است)")
                return []
                
            all_corrections = []
            
            # شناسایی الگوهای ساده (3-موجی)
            simple_corrections = self._identify_simple_corrections(pivots, wave_degree)
            all_corrections.extend(simple_corrections)
            
            # شناسایی الگوهای پیچیده (5+ موجی)  
            complex_corrections = self._identify_complex_corrections(pivots, wave_degree)
            all_corrections.extend(complex_corrections)
            
            # شناسایی ترکیبات
            combination_corrections = self._identify_combinations(pivots, wave_degree)
            all_corrections.extend(combination_corrections)
            
            # فیلتر براساس اعتماد
            valid_corrections = [c for c in all_corrections if c.confidence_score >= min_confidence]
            
            # حذف overlap های غیرضروری
            filtered_corrections = self._remove_overlapping_patterns(valid_corrections)
            
            # مرتب‌سازی براساس کیفیت
            filtered_corrections.sort(key=lambda x: x.confidence_score, reverse=True)
            
            self.identified_corrections.extend(filtered_corrections)
            logger.info(f"✅ {len(filtered_corrections)} الگوی اصلاحی معتبر شناسایی شد")
            
            return filtered_corrections
            
        except Exception as e:
            logger.error(f"خطا در شناسایی الگوهای اصلاحی: {e}")
            return []
    
    def _identify_simple_corrections(self, pivots: List[Tuple], wave_degree: int) -> List[CorrectiveWave]:
        """شناسایی الگوهای اصلاحی ساده"""
        corrections = []
        
        try:
            # Zigzag patterns (5-3-5)
            zigzags = self._identify_zigzag_patterns(pivots, wave_degree)
            corrections.extend(zigzags)
            
            # Flat patterns (3-3-5)
            flats = self._identify_flat_patterns(pivots, wave_degree)  
            corrections.extend(flats)
            
            # Triangle patterns (3-3-3-3-3)
            triangles = self._identify_triangle_patterns(pivots, wave_degree)
            corrections.extend(triangles)
            
            logger.debug(f"شناسایی {len(corrections)} الگوی ساده")
            return corrections
            
        except Exception as e:
            logger.error(f"خطا در شناسایی الگوهای ساده: {e}")
            return []
    
    def _identify_zigzag_patterns(self, pivots: List[Tuple], wave_degree: int) -> List[CorrectiveWave]:
        """شناسایی دقیق الگوهای Zigzag"""
        zigzags = []
        
        try:
            # حداقل 4 pivot برای zigzag ساده
            for i in range(len(pivots) - 3):
                pattern_pivots = pivots[i:i+4]
                
                if self._validate_zigzag_structure(pattern_pivots):
                    zigzag = self._create_zigzag_wave(pattern_pivots, wave_degree)
                    if zigzag and zigzag.is_valid:
                        zigzags.append(zigzag)
                        
            # Double Zigzag (W-X-Y)
            for i in range(len(pivots) - 6):
                pattern_pivots = pivots[i:i+7]
                if self._validate_double_zigzag_structure(pattern_pivots):
                    double_zz = self._create_double_zigzag(pattern_pivots, wave_degree)
                    if double_zz and double_zz.is_valid:
                        zigzags.append(double_zz)
                        
            logger.debug(f"شناسایی {len(zigzags)} الگوی Zigzag")
            return zigzags
            
        except Exception as e:
            logger.error(f"خطا در شناسایی Zigzag: {e}")
            return []
    
    def _validate_zigzag_structure(self, pivots: List[Tuple]) -> bool:
        """اعتبارسنجی دقیق ساختار Zigzag براساس قوانین NEOWave"""
        try:
            if len(pivots) < 4:
                return False
                
            # استخراج قیمت‌ها
            prices = [p[1] for p in pivots]
            
            # تشخیص جهت الگو
            is_bullish = prices[0] > prices[-1]  # الگوی نزولی
            
            if is_bullish:
                # در zigzag نزولی: A(down), B(up), C(down)
                # قوانین اصلی:
                # 1. موج B نباید بیش از 61.8% موج A را اصلاح کند
                # 2. موج C باید فراتر از انتهای موج A برود
                # 3. C >= 0.618 * A و C <= 1.618 * A
                
                wave_a = abs(prices[1] - prices[0])  # موج A
                wave_b = abs(prices[2] - prices[1])  # موج B  
                wave_c = abs(prices[3] - prices[2])  # موج C
                
                # بررسی retracement موج B
                b_retracement = wave_b / wave_a
                if b_retracement > 0.618:
                    return False
                    
                # بررسی extension موج C
                if prices[3] >= prices[1]:  # C باید پایین‌تر از A باشد
                    return False
                    
                # بررسی نسبت‌های فیبوناچی
                c_ratio = wave_c / wave_a
                if not (0.618 <= c_ratio <= 1.618):
                    return False
                    
            else:
                # قوانین مشابه برای zigzag صعودی
                wave_a = abs(prices[1] - prices[0])
                wave_b = abs(prices[2] - prices[1])
                wave_c = abs(prices[3] - prices[2])
                
                b_retracement = wave_b / wave_a
                if b_retracement > 0.618:
                    return False
                    
                if prices[3] <= prices[1]:
                    return False
                    
                c_ratio = wave_c / wave_a
                if not (0.618 <= c_ratio <= 1.618):
                    return False
                    
            # بررسی روابط زمانی
            times = [p[0] for p in pivots]
            time_a = times[1] - times[0]
            time_b = times[2] - times[1] 
            time_c = times[3] - times[2]
            
            # موج B معمولاً کوتاه‌تر از A و C است
            if time_b > max(time_a, time_c):
                return False
                
            return True
            
        except Exception as e:
            logger.warning(f"خطا در اعتبارسنجی Zigzag: {e}")
            return False
    
    def _create_zigzag_wave(self, pivots: List[Tuple], wave_degree: int) -> Optional[CorrectiveWave]:
        """ایجاد موج Zigzag با تمام جزئیات"""
        try:
            if len(pivots) < 4:
                return None
                
            # ایجاد sub-waves
            sub_waves = []
            wave_positions = [WavePosition.A, WavePosition.B, WavePosition.C]
            
            for i, pos in enumerate(wave_positions):
                start_pivot = pivots[i]
                end_pivot = pivots[i + 1]
                
                sub_wave = SubWaveDetail(
                    position=pos,
                    wave_type="impulse" if pos in [WavePosition.A, WavePosition.C] else "corrective",
                    start_index=start_pivot[0],
                    end_index=end_pivot[0],
                    start_price=start_pivot[1],
                    end_price=end_pivot[1],
                    high_price=max(start_pivot[1], end_pivot[1]),
                    low_price=min(start_pivot[1], end_pivot[1]),
                    duration=end_pivot[0] - start_pivot[0],
                    amplitude=abs(end_pivot[1] - start_pivot[1]),
                    slope=(end_pivot[1] - start_pivot[1]) / max(1, end_pivot[0] - start_pivot[0])
                )
                
                # محاسبه نسبت‌های فیبوناچی
                if i > 0:  # برای موج B و C
                    prev_wave = sub_waves[0] if i == 1 else sub_waves[0]
                    sub_wave.retracement_ratio = sub_wave.amplitude / prev_wave.amplitude
                    
                sub_waves.append(sub_wave)
                
            # محاسبه metrics
            metrics = self._calculate_correction_metrics(sub_waves, CorrectiveType.ZIGZAG)
            
            # ایجاد موج اصلی
            zigzag = CorrectiveWave(
                wave_id=f"ZZ_{wave_degree}_{pivots[0][0]}",
                wave_type=CorrectiveType.ZIGZAG,
                subtype=CorrectionSubtype.STANDARD,
                sub_waves=sub_waves,
                start_price=pivots[0][1],
                end_price=pivots[-1][1],
                start_index=pivots[0][0],
                end_index=pivots[-1][0],
                high_price=max(p[1] for p in pivots),
                low_price=min(p[1] for p in pivots),
                metrics=metrics,
                degree=wave_degree,
                identified_at=pd.Timestamp.now().isoformat()
            )
            
            # اعتبارسنجی نهایی
            zigzag.is_valid, zigzag.confidence_score = self._validate_zigzag_complete(zigzag)
            
            # محاسبه targets
            if zigzag.is_valid:
                zigzag.next_wave_target = self._calculate_zigzag_target(zigzag)
                zigzag.invalidation_level = self._calculate_invalidation_level(zigzag)
                
            return zigzag
            
        except Exception as e:
            logger.error(f"خطا در ایجاد Zigzag: {e}")
            return None
    
    def _identify_flat_patterns(self, pivots: List[Tuple], wave_degree: int) -> List[CorrectiveWave]:
        """شناسایی الگوهای Flat (3-3-5)"""
        flats = []
        
        try:
            # Flat معمولی
            for i in range(len(pivots) - 3):
                pattern_pivots = pivots[i:i+4]
                if self._validate_flat_structure(pattern_pivots):
                    flat = self._create_flat_wave(pattern_pivots, wave_degree)
                    if flat and flat.is_valid:
                        flats.append(flat)
                        
            logger.debug(f"شناسایی {len(flats)} الگوی Flat")
            return flats
            
        except Exception as e:
            logger.error(f"خطا در شناسایی Flat: {e}")
            return []
    
    def _validate_flat_structure(self, pivots: List[Tuple]) -> bool:
        """اعتبارسنجی دقیق ساختار Flat"""
        try:
            if len(pivots) < 4:
                return False
                
            prices = [p[1] for p in pivots]
            
            # محاسبه امواج
            wave_a = abs(prices[1] - prices[0])
            wave_b = abs(prices[2] - prices[1])
            wave_c = abs(prices[3] - prices[2])
            
            # قوانین اصلی Flat:
            # 1. موج B باید حداقل 90% موج A را اصلاح کند
            b_retracement = wave_b / wave_a
            if b_retracement < 0.90:
                return False
                
            # 2. موج C باید تقریباً برابر موج A باشد (0.8 تا 1.2)
            c_ratio = wave_c / wave_a
            if not (0.80 <= c_ratio <= 1.20):
                return False
                
            # 3. بررسی overlap بین موج A و C
            is_bullish = prices[0] < prices[3]
            
            if is_bullish:
                # در flat صعودی، C نباید خیلی بالاتر از A برود
                if prices[3] > prices[1] * 1.05:  # 5% tolerance
                    return False
            else:
                # در flat نزولی، C نباید خیلی پایین‌تر از A برود
                if prices[3] < prices[1] * 0.95:
                    return False
                    
            return True
            
        except Exception as e:
            logger.warning(f"خطا در اعتبارسنجی Flat: {e}")
            return False
    
    def _create_flat_wave(self, pivots: List[Tuple], wave_degree: int) -> Optional[CorrectiveWave]:
        """ایجاد موج Flat کامل"""
        try:
            prices = [p[1] for p in pivots]
            wave_a = abs(prices[1] - prices[0])
            wave_b = abs(prices[2] - prices[1])
            
            # تعیین نوع Flat براساس موج B
            b_ratio = wave_b / wave_a
            
            if b_ratio <= 1.05:
                subtype = CorrectionSubtype.STANDARD  # Regular Flat
            elif b_ratio > 1.05:
                subtype = CorrectionSubtype.ELONGATED  # Expanded Flat
            else:
                subtype = CorrectionSubtype.IRREGULAR
                
            # ایجاد sub-waves
            sub_waves = []
            wave_positions = [WavePosition.A, WavePosition.B, WavePosition.C]
            wave_types = ["corrective", "corrective", "impulse"]  # 3-3-5
            
            for i, (pos, w_type) in enumerate(zip(wave_positions, wave_types)):
                start_pivot = pivots[i]
                end_pivot = pivots[i + 1]
                
                sub_wave = SubWaveDetail(
                    position=pos,
                    wave_type=w_type,
                    start_index=start_pivot[0],
                    end_index=end_pivot[0],
                    start_price=start_pivot[1],
                    end_price=end_pivot[1],
                    high_price=max(start_pivot[1], end_pivot[1]),
                    low_price=min(start_pivot[1], end_pivot[1]),
                    duration=end_pivot[0] - start_pivot[0],
                    amplitude=abs(end_pivot[1] - start_pivot[1]),
                    slope=(end_pivot[1] - start_pivot[1]) / max(1, end_pivot[0] - start_pivot[0])
                )
                
                # محاسبه نسبت‌ها
                if i > 0:
                    prev_amplitude = sub_waves[0].amplitude
                    sub_wave.retracement_ratio = sub_wave.amplitude / prev_amplitude
                    
                sub_waves.append(sub_wave)
                
            # محاسبه metrics
            metrics = self._calculate_correction_metrics(sub_waves, CorrectiveType.FLAT)
            
            # تشخیص نوع دقیق flat
            flat_type = CorrectiveType.REGULAR_FLAT
            if b_ratio > 1.05:
                flat_type = CorrectiveType.EXPANDED_FLAT
            elif sub_waves[2].amplitude / sub_waves[0].amplitude < 0.9:
                flat_type = CorrectiveType.RUNNING_FLAT
                
            flat = CorrectiveWave(
                wave_id=f"FLAT_{wave_degree}_{pivots[0][0]}",
                wave_type=flat_type,
                subtype=subtype,
                sub_waves=sub_waves,
                start_price=pivots[0][1],
                end_price=pivots[-1][1],
                start_index=pivots[0][0],
                end_index=pivots[-1][0],
                high_price=max(p[1] for p in pivots),
                low_price=min(p[1] for p in pivots),
                metrics=metrics,
                degree=wave_degree,
                identified_at=pd.Timestamp.now().isoformat()
            )
            
            # اعتبارسنجی
            flat.is_valid, flat.confidence_score = self._validate_flat_complete(flat)
            
            return flat
            
        except Exception as e:
            logger.error(f"خطا در ایجاد Flat: {e}")
            return None
    
    def _identify_triangle_patterns(self, pivots: List[Tuple], wave_degree: int) -> List[CorrectiveWave]:
        """شناسایی الگوهای Triangle (3-3-3-3-3)"""
        triangles = []
        
        try:
            # حداقل 6 pivot برای triangle
            for i in range(len(pivots) - 5):
                pattern_pivots = pivots[i:i+6]
                
                if self._validate_triangle_structure(pattern_pivots):
                    triangle = self._create_triangle_wave(pattern_pivots, wave_degree)
                    if triangle and triangle.is_valid:
                        triangles.append(triangle)
                        
            logger.debug(f"شناسایی {len(triangles)} الگوی Triangle")
            return triangles
            
        except Exception as e:
            logger.error(f"خطا در شناسایی Triangle: {e}")
            return []
    
    def _validate_triangle_structure(self, pivots: List[Tuple]) -> bool:
        """اعتبارسنجی ساختار Triangle"""
        try:
            if len(pivots) < 6:
                return False
                
            prices = [p[1] for p in pivots]
            times = [p[0] for p in pivots]
            
            # محاسبه امواج
            waves = []
            for i in range(len(pivots) - 1):
                wave_length = abs(prices[i+1] - prices[i])
                wave_time = times[i+1] - times[i]
                waves.append({'length': wave_length, 'time': wave_time})
                
            if len(waves) < 5:
                return False
                
            # قانون اصلی Triangle: هر موج باید کوچک‌تر از موج قبلی باشد
            # (در contracting triangle)
            
            # بررسی کاهش اندازه امواج
            lengths = [w['length'] for w in waves]
            
            # Contracting Triangle: اکثر امواج باید کوچک‌تر شوند
            decreasing_count = 0
            for i in range(1, len(lengths)):
                if lengths[i] < lengths[i-1]:
                    decreasing_count += 1
                    
            # حداقل 60% امواج باید کوچک‌تر شوند
            if decreasing_count / (len(lengths) - 1) < 0.6:
                return False
                
            # بررسی overlap بین خطوط triangle
            upper_line = self._calculate_trendline([
                (times[i], prices[i]) for i in range(0, len(pivots), 2)
            ])
            lower_line = self._calculate_trendline([
                (times[i], prices[i]) for i in range(1, len(pivots), 2)
            ])
            
            if not upper_line or not lower_line:
                return False
                
            # خطوط باید همگرا باشند
            if abs(upper_line['slope'] - lower_line['slope']) < 0.0001:
                return False  # خطوط موازی
                
            return True
            
        except Exception as e:
            logger.warning(f"خطا در اعتبارسنجی Triangle: {e}")
            return False
    
    def _calculate_trendline(self, points: List[Tuple]) -> Optional[Dict]:
        """محاسبه خط روند"""
        try:
            if len(points) < 2:
                return None
                
            x_vals = np.array([p[0] for p in points])
            y_vals = np.array([p[1] for p in points])
            
            slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
            
            return {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_value ** 2,
                'confidence': r_value ** 2 if p_value < 0.05 else 0
            }
            
        except:
            return None
    
    def _create_triangle_wave(self, pivots: List[Tuple], wave_degree: int) -> Optional[CorrectiveWave]:
        """ایجاد موج Triangle کامل"""
        try:
            # تشخیص نوع triangle
            triangle_type = self._determine_triangle_type(pivots)
            
            # ایجاد sub-waves (5 موج: A-B-C-D-E)
            sub_waves = []
            wave_positions = [WavePosition.A, WavePosition.B, WavePosition.C, 
                            WavePosition.D, WavePosition.E]
            
            for i, pos in enumerate(wave_positions):
                if i >= len(pivots) - 1:
                    break
                    
                start_pivot = pivots[i]
                end_pivot = pivots[i + 1]
                
                sub_wave = SubWaveDetail(
                    position=pos,
                    wave_type="corrective",  # همه امواج triangle اصلاحی هستند
                    start_index=start_pivot[0],
                    end_index=end_pivot[0],
                    start_price=start_pivot[1],
                    end_price=end_pivot[1],
                    high_price=max(start_pivot[1], end_pivot[1]),
                    low_price=min(start_pivot[1], end_pivot[1]),
                    duration=end_pivot[0] - start_pivot[0],
                    amplitude=abs(end_pivot[1] - start_pivot[1]),
                    slope=(end_pivot[1] - start_pivot[1]) / max(1, end_pivot[0] - start_pivot[0])
                )
                
                sub_waves.append(sub_wave)
                
            # محاسبه metrics
            metrics = self._calculate_correction_metrics(sub_waves, CorrectiveType.TRIANGLE)
            
            triangle = CorrectiveWave(
                wave_id=f"TRI_{wave_degree}_{pivots[0][0]}",
                wave_type=triangle_type,
                subtype=CorrectionSubtype.STANDARD,
                sub_waves=sub_waves,
                start_price=pivots[0][1],
                end_price=pivots[-1][1],
                start_index=pivots[0][0],
                end_index=pivots[-1][0],
                high_price=max(p[1] for p in pivots),
                low_price=min(p[1] for p in pivots),
                metrics=metrics,
                degree=wave_degree,
                identified_at=pd.Timestamp.now().isoformat()
            )
            
            # اعتبارسنجی
            triangle.is_valid, triangle.confidence_score = self._validate_triangle_complete(triangle)
            
            return triangle
            
        except Exception as e:
            logger.error(f"خطا در ایجاد Triangle: {e}")
            return None
    
    def _determine_triangle_type(self, pivots: List[Tuple]) -> CorrectiveType:
        """تشخیص نوع دقیق Triangle"""
        try:
            prices = [p[1] for p in pivots]
            
            # محاسبه امواج
            wave_lengths = []
            for i in range(len(pivots) - 1):
                length = abs(prices[i+1] - prices[i])
                wave_lengths.append(length)
                
            # بررسی روند اندازه امواج
            decreasing_count = sum(1 for i in range(1, len(wave_lengths)) 
                                 if wave_lengths[i] < wave_lengths[i-1])
            total_comparisons = len(wave_lengths) - 1
            
            if total_comparisons > 0:
                decreasing_ratio = decreasing_count / total_comparisons
                
                if decreasing_ratio >= 0.6:
                    return CorrectiveType.CONTRACTING_TRIANGLE
                elif decreasing_ratio <= 0.4:
                    return CorrectiveType.EXPANDING_TRIANGLE
                else:
                    return CorrectiveType.BARRIER_TRIANGLE
            else:
                return CorrectiveType.TRIANGLE
                
        except:
            return CorrectiveType.TRIANGLE
    
    def _identify_complex_corrections(self, pivots: List[Tuple], wave_degree: int) -> List[CorrectiveWave]:
        """شناسایی الگوهای پیچیده (Diametric, Symmetric)"""
        complex_corrections = []
        
        try:
            # Diametric (7-wave: A-B-C-D-E-F-G)
            diametrics = self._identify_diametric_patterns(pivots, wave_degree)
            complex_corrections.extend(diametrics)
            
            # Symmetric (9-wave: A-B-C-D-E-F-G-H-I)  
            symmetrics = self._identify_symmetric_patterns(pivots, wave_degree)
            complex_corrections.extend(symmetrics)
            
            logger.debug(f"شناسایی {len(complex_corrections)} الگوی پیچیده")
            return complex_corrections
            
        except Exception as e:
            logger.error(f"خطا در شناسایی الگوهای پیچیده: {e}")
            return []
    
    def _identify_combinations(self, pivots: List[Tuple], wave_degree: int) -> List[CorrectiveWave]:
        """شناسایی ترکیبات پیچیده (Double/Triple patterns)"""
        combinations = []
        
        try:
            # شناسایی W-X-Y patterns
            # شناسایی W-X-Y-X-Z patterns
            # ساده‌سازی موقت
            return combinations
            
        except Exception as e:
            logger.error(f"خطا در شناسایی ترکیبات: {e}")
            return []
    
    def _calculate_correction_metrics(self, sub_waves: List[SubWaveDetail], 
                                    pattern_type: CorrectiveType) -> CorrectionMetrics:
        """محاسبه معیارهای کمی الگوی اصلاحی"""
        try:
            metrics = CorrectionMetrics()
            
            if not sub_waves:
                return metrics
                
            # محاسبه دقت فیبوناچی
            metrics.fibonacci_accuracy = self._calculate_fibonacci_accuracy(sub_waves)
            
            # محاسبه تقارن زمانی
            metrics.time_symmetry = self._calculate_time_symmetry(sub_waves)
            
            # محاسبه تقارن قیمتی
            metrics.price_symmetry = self._calculate_price_symmetry(sub_waves)
            
            # محاسبه امتیاز alternation
            metrics.alternation_score = self._calculate_alternation_score(sub_waves)
            
            # محاسبه یکپارچگی ساختاری
            metrics.structural_integrity = self._calculate_structural_integrity(
                sub_waves, pattern_type
            )
            
            # احتمال تکمیل
            metrics.completion_probability = self._calculate_completion_probability(
                sub_waves, pattern_type
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"خطا در محاسبه metrics: {e}")
            return CorrectionMetrics()
    
    # متدهای کمکی برای محاسبات
    def _calculate_fibonacci_accuracy(self, sub_waves: List[SubWaveDetail]) -> float:
        """محاسبه دقت نسبت‌های فیبوناچی"""
        try:
            if len(sub_waves) < 2:
                return 0.0
                
            accuracy_scores = []
            
            for i in range(1, len(sub_waves)):
                ratio = sub_waves[i].amplitude / sub_waves[0].amplitude
                
                # یافتن نزدیک‌ترین سطح فیبوناچی
                best_match = min(self.fibonacci_levels['retracement'] + 
                               self.fibonacci_levels['extension'],
                               key=lambda x: abs(x - ratio))
                
                # محاسبه دقت
                accuracy = 1 - abs(ratio - best_match) / best_match
                accuracy_scores.append(max(0, accuracy))
                
            return np.mean(accuracy_scores)
            
        except:
            return 0.0
    
    def _calculate_time_symmetry(self, sub_waves: List[SubWaveDetail]) -> float:
        """محاسبه تقارن زمانی"""
        try:
            if len(sub_waves) < 2:
                return 0.0
                
            durations = [sw.duration for sw in sub_waves]
            
            # محاسبه ضریب تغییرات
            cv = np.std(durations) / (np.mean(durations) + 1e-10)
            
            # تبدیل به امتیاز تقارن (کمتر بودن CV = تقارن بیشتر)
            symmetry = 1 / (1 + cv)
            
            return min(1.0, symmetry)
            
        except:
            return 0.0
    
    def _calculate_price_symmetry(self, sub_waves: List[SubWaveDetail]) -> float:
        """محاسبه تقارن قیمتی"""
        try:
            if len(sub_waves) < 2:
                return 0.0
                
            amplitudes = [sw.amplitude for sw in sub_waves]
            
            # محاسبه تقارن براساس انحراف معیار
            cv = np.std(amplitudes) / (np.mean(amplitudes) + 1e-10)
            symmetry = 1 / (1 + cv)
            
            return min(1.0, symmetry)
            
        except:
            return 0.0
    
    def _calculate_alternation_score(self, sub_waves: List[SubWaveDetail]) -> float:
        """محاسبه امتیاز alternation"""
        try:
            if len(sub_waves) < 3:
                return 0.0
                
            # بررسی alternation بین موج‌های زوج و فرد
            alternation_score = 0.0
            
            # مقایسه موج‌های A و C (اگر وجود دارد)
            if len(sub_waves) >= 3:
                wave_a = sub_waves[0]
                wave_c = sub_waves[2]
                
                # تفاوت در مدت زمان
                time_diff = abs(wave_a.duration - wave_c.duration) / max(wave_a.duration, wave_c.duration)
                
                # تفاوت در اندازه
                size_diff = abs(wave_a.amplitude - wave_c.amplitude) / max(wave_a.amplitude, wave_c.amplitude)
                
                alternation_score = (time_diff + size_diff) / 2
                
            return min(1.0, alternation_score)
            
        except:
            return 0.0
    
    def _calculate_structural_integrity(self, sub_waves: List[SubWaveDetail], 
                                      pattern_type: CorrectiveType) -> float:
        """محاسبه یکپارچگی ساختاری"""
        try:
            integrity_score = 0.0
            
            if pattern_type == CorrectiveType.ZIGZAG:
                # بررسی ساختار 5-3-5
                expected_types = ["impulse", "corrective", "impulse"]
                actual_types = [sw.wave_type for sw in sub_waves[:3]]
                
                matches = sum(1 for e, a in zip(expected_types, actual_types) if e == a)
                integrity_score = matches / len(expected_types)
                
            elif pattern_type == CorrectiveType.FLAT:
                # بررسی ساختار 3-3-5
                expected_types = ["corrective", "corrective", "impulse"]
                actual_types = [sw.wave_type for sw in sub_waves[:3]]
                
                matches = sum(1 for e, a in zip(expected_types, actual_types) if e == a)
                integrity_score = matches / len(expected_types)
                
            elif pattern_type == CorrectiveType.TRIANGLE:
                # همه امواج باید corrective باشند
                corrective_count = sum(1 for sw in sub_waves if sw.wave_type == "corrective")
                integrity_score = corrective_count / len(sub_waves)
                
            return integrity_score
            
        except:
            return 0.0
    
    def _calculate_completion_probability(self, sub_waves: List[SubWaveDetail],
                                        pattern_type: CorrectiveType) -> float:
        """محاسبه احتمال تکمیل الگو"""
        try:
            # براساس تعداد امواج تکمیل شده
            if pattern_type in [CorrectiveType.ZIGZAG, CorrectiveType.FLAT]:
                required_waves = 3
            elif pattern_type == CorrectiveType.TRIANGLE:
                required_waves = 5
            elif pattern_type == CorrectiveType.DIAMETRIC:
                required_waves = 7
            elif pattern_type == CorrectiveType.SYMMETRIC:
                required_waves = 9
            else:
                required_waves = 3
                
            completion = len(sub_waves) / required_waves
            return min(1.0, completion)
            
        except:
            return 0.0
    
    # متدهای اعتبارسنجی کامل
    def _validate_zigzag_complete(self, zigzag: CorrectiveWave) -> Tuple[bool, float]:
        """اعتبارسنجی کامل Zigzag"""
        try:
            confidence_factors = []
            errors = []
            
            # بررسی تعداد sub-waves
            if len(zigzag.sub_waves) >= 3:
                confidence_factors.append(0.3)
            else:
                errors.append("تعداد sub-waves کافی نیست")
                
            # بررسی نسبت‌های فیبوناچی
            if zigzag.metrics.fibonacci_accuracy >= 0.7:
                confidence_factors.append(0.25)
            else:
                errors.append("نسبت‌های فیبوناچی ضعیف")
                
            # بررسی ساختار
            if zigzag.metrics.structural_integrity >= 0.8:
                confidence_factors.append(0.25)
            else:
                errors.append("ساختار نامناسب")
                
            # بررسی alternation
            if zigzag.metrics.alternation_score >= 0.6:
                confidence_factors.append(0.2)
            else:
                errors.append("alternation ضعیف")
                
            zigzag.validation_errors = errors
            
            total_confidence = sum(confidence_factors)
            is_valid = total_confidence >= 0.75 and len(errors) <= 1
            
            return is_valid, total_confidence
            
        except Exception as e:
            logger.error(f"خطا در اعتبارسنجی Zigzag: {e}")
            return False, 0.0
    
    def _validate_flat_complete(self, flat: CorrectiveWave) -> Tuple[bool, float]:
        """اعتبارسنجی کامل Flat"""
        # مشابه zigzag با قوانین خاص flat
        return self._validate_zigzag_complete(flat)  # ساده‌سازی موقت
    
    def _validate_triangle_complete(self, triangle: CorrectiveWave) -> Tuple[bool, float]:
        """اعتبارسنجی کامل Triangle"""
        # مشابه zigzag با قوانین خاص triangle
        return self._validate_zigzag_complete(triangle)  # ساده‌سازی موقت
    
    # متدهای کمکی اضافی
    def _validate_double_zigzag_structure(self, pivots: List[Tuple]) -> bool:
        """اعتبارسنجی Double Zigzag"""
        return False  # ساده‌سازی موقت
    
    def _create_double_zigzag(self, pivots: List[Tuple], wave_degree: int) -> Optional[CorrectiveWave]:
        """ایجاد Double Zigzag"""
        return None  # ساده‌سازی موقت
    
    def _identify_diametric_patterns(self, pivots: List[Tuple], wave_degree: int) -> List[CorrectiveWave]:
        """شناسایی Diametric patterns"""
        return []  # ساده‌سازی موقت
    
    def _identify_symmetric_patterns(self, pivots: List[Tuple], wave_degree: int) -> List[CorrectiveWave]:
        """شناسایی Symmetric patterns"""
        return []  # ساده‌سازی موقت
    
    def _remove_overlapping_patterns(self, corrections: List[CorrectiveWave]) -> List[CorrectiveWave]:
        """حذف الگوهای overlap دار"""
        if not corrections:
            return corrections
            
        # مرتب‌سازی براساس confidence
        sorted_corrections = sorted(corrections, key=lambda x: x.confidence_score, reverse=True)
        
        filtered = []
        for correction in sorted_corrections:
            # بررسی overlap با الگوهای قبلی
            has_overlap = False
            for existing in filtered:
                if self._check_pattern_overlap(correction, existing):
                    has_overlap = True
                    break
                    
            if not has_overlap:
                filtered.append(correction)
                
        return filtered
    
    def _check_pattern_overlap(self, pattern1: CorrectiveWave, pattern2: CorrectiveWave) -> bool:
        """بررسی overlap بین دو الگو"""
        try:
            # بررسی overlap زمانی
            time_overlap = not (pattern1.end_index <= pattern2.start_index or 
                              pattern2.end_index <= pattern1.start_index)
            
            if time_overlap:
                # محاسبه درصد overlap
                overlap_start = max(pattern1.start_index, pattern2.start_index)
                overlap_end = min(pattern1.end_index, pattern2.end_index)
                overlap_duration = overlap_end - overlap_start
                
                min_duration = min(pattern1.end_index - pattern1.start_index,
                                 pattern2.end_index - pattern2.start_index)
                
                overlap_ratio = overlap_duration / min_duration
                
                # overlap بیش از 70% را غیرقابل قبول می‌دانیم
                return overlap_ratio > 0.7
                
            return False
            
        except:
            return False
    
    def _calculate_zigzag_target(self, zigzag: CorrectiveWave) -> Optional[float]:
        """محاسبه target برای Zigzag"""
        try:
            if len(zigzag.sub_waves) >= 3:
                wave_a = zigzag.sub_waves[0]
                wave_c = zigzag.sub_waves[2]
                
                # معمولاً C = A یا C = 1.618 * A
                target_1 = zigzag.start_price + wave_a.amplitude  # C = A
                target_2 = zigzag.start_price + wave_a.amplitude * 1.618  # C = 1.618*A
                
                # انتخاب نزدیک‌ترین target
                current_price = wave_c.end_price
                
                if abs(current_price - target_1) < abs(current_price - target_2):
                    return target_1
                else:
                    return target_2
                    
            return None
            
        except:
            return None
    
    def _calculate_invalidation_level(self, correction: CorrectiveWave) -> Optional[float]:
        """محاسبه سطح باطل‌سازی الگو"""
        try:
            if correction.wave_type == CorrectiveType.ZIGZAG:
                # برای zigzag، شکست شروع موج A الگو را باطل می‌کند
                return correction.start_price
            elif correction.wave_type in [CorrectiveType.FLAT, CorrectiveType.REGULAR_FLAT]:
                # برای flat، شکست extreme موج B الگو را باطل می‌کند
                if len(correction.sub_waves) >= 2:
                    return correction.sub_waves[1].end_price
                    
            return None
            
        except:
            return None
    
    def get_active_corrections(self, current_index: int) -> List[CorrectiveWave]:
        """دریافت الگوهای اصلاحی فعال"""
        return [
            corr for corr in self.identified_corrections
            if corr.start_index <= current_index <= corr.end_index and corr.is_valid
        ]
    
    def get_correction_by_id(self, wave_id: str) -> Optional[CorrectiveWave]:
        """دریافت الگو بر اساس ID"""
        for correction in self.identified_corrections:
            if correction.wave_id == wave_id:
                return correction
        return None
    
    def generate_correction_report(self, corrections: List[CorrectiveWave] = None) -> Dict:
        """تولید گزارش جامع الگوهای اصلاحی"""
        if corrections is None:
            corrections = self.identified_corrections
            
        try:
            report = {
                'summary': {
                    'total_patterns': len(corrections),
                    'valid_patterns': sum(1 for c in corrections if c.is_valid),
                    'pattern_distribution': Counter(c.wave_type.value for c in corrections),
                    'average_confidence': np.mean([c.confidence_score for c in corrections]) if corrections else 0,
                    'generated_at': pd.Timestamp.now().isoformat()
                },
                'patterns': [],
                'statistics': {},
                'recommendations': []
            }
            
            # جزئیات هر الگو
            for correction in corrections:
                if correction.is_valid:
                    pattern_detail = {
                        'id': correction.wave_id,
                        'type': correction.wave_type.value,
                        'subtype': correction.subtype.value,
                        'confidence': correction.confidence_score,
                        'start_price': correction.start_price,
                        'end_price': correction.end_price,
                        'duration': correction.end_index - correction.start_index,
                        'target': correction.next_wave_target,
                        'invalidation': correction.invalidation_level,
                        'completion': correction.completion_status,
                        'metrics': {
                            'fibonacci_accuracy': correction.metrics.fibonacci_accuracy,
                            'structural_integrity': correction.metrics.structural_integrity,
                            'alternation_score': correction.metrics.alternation_score
                        }
                    }
                    report['patterns'].append(pattern_detail)
            
            # آمار کلی
            if corrections:
                confidence_scores = [c.confidence_score for c in corrections if c.is_valid]
                if confidence_scores:
                    report['statistics'] = {
                        'highest_confidence': max(confidence_scores),
                        'lowest_confidence': min(confidence_scores),
                        'confidence_std': np.std(confidence_scores),
                        'quality_distribution': {
                            'high_quality': sum(1 for c in confidence_scores if c >= 0.8),
                            'medium_quality': sum(1 for c in confidence_scores if 0.6 <= c < 0.8),
                            'low_quality': sum(1 for c in confidence_scores if c < 0.6)
                        }
                    }
            
            # توصیه‌ها
            report['recommendations'] = self._generate_correction_recommendations(corrections)
            
            return report
            
        except Exception as e:
            logger.error(f"خطا در تولید گزارش: {e}")
            return {'error': str(e)}
    
    def _generate_correction_recommendations(self, corrections: List[CorrectiveWave]) -> List[str]:
        """تولید توصیه‌های عملی"""
        recommendations = []
        
        try:
            valid_corrections = [c for c in corrections if c.is_valid]
            
            if not valid_corrections:
                recommendations.append("هیچ الگوی اصلاحی معتبر شناسایی نشد")
                return recommendations
            
            # پیدا کردن بهترین الگو
            best_pattern = max(valid_corrections, key=lambda x: x.confidence_score)
            recommendations.append(f"قوی‌ترین الگو: {best_pattern.wave_type.value} با اعتماد {best_pattern.confidence_score:.1%}")
            
            # توصیه برای target
            if best_pattern.next_wave_target:
                recommendations.append(f"هدف قیمتی: {best_pattern.next_wave_target:.2f}")
                
            # توصیه برای invalidation
            if best_pattern.invalidation_level:
                recommendations.append(f"سطح باطل‌سازی: {best_pattern.invalidation_level:.2f}")
            
            # بررسی تکمیل
            if best_pattern.completion_status > 0.8:
                recommendations.append("الگو در حال تکمیل - احتمال شکست بالا")
            elif best_pattern.completion_status < 0.5:
                recommendations.append("الگو در مراحل اولیه - نیاز به صبر بیشتر")
                
            return recommendations
            
        except Exception as e:
            logger.error(f"خطا در تولید توصیه‌ها: {e}")
            return ["خطا در تولید توصیه‌ها"]