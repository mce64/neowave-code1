# ================= elliott_basics.py =================
"""
🌊 سیستم پیشرفته تحلیل امواج Elliott و NEOWave
نسخه کامل و حرفه‌ای مبتنی بر تئوری Ralph Elliott و Glenn Neely

ویژگی‌های کلیدی:
- شناسایی دقیق pivot points با الگوریتم‌های پیشرفته
- اعتبارسنجی کامل قوانین Elliott و NEOWave
- تحلیل چندمقیاسه (Multi-timeframe)
- محاسبه دقیق نسبت‌های فیبوناچی
- درجه‌بندی هوشمند امواج
- ارزیابی اعتماد و قدرت الگوها
- تشخیص الگوهای پیچیده و ترکیبی
- تحلیل momentum و divergence
"""

import numpy as np
import pandas as pd
import logging
from typing import List, Tuple, Dict, Optional, Union, Set
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from scipy import stats, signal
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import warnings

logger = logging.getLogger(__name__)

class WaveType(Enum):
    """انواع کامل امواج Elliott و NEOWave"""
    # امواج اصلی Elliott
    IMPULSE = "impulse"
    CORRECTIVE = "corrective"
    
    # امواج خاص
    DIAGONAL = "diagonal"
    LEADING_DIAGONAL = "leading_diagonal"
    ENDING_DIAGONAL = "ending_diagonal"
    
    # امواج اصلاحی
    ZIGZAG = "zigzag"
    FLAT = "flat"
    TRIANGLE = "triangle"
    COMPLEX_CORRECTION = "complex_correction"
    
    # امواج NEOWave خاص
    DIAMETRIC = "diametric"
    SYMMETRIC = "symmetric"
    NEUTRAL_TRIANGLE = "neutral_triangle"
    
    # امواج ترکیبی
    DOUBLE_ZIGZAG = "double_zigzag"
    TRIPLE_ZIGZAG = "triple_zigzag"
    DOUBLE_THREE = "double_three"
    TRIPLE_THREE = "triple_three"

class WaveDegree(IntEnum):
    """درجه‌بندی دقیق امواج براساس تئوری Elliott"""
    GRAND_SUPERCYCLE = 9    # [(I)] - صدها سال
    SUPERCYCLE = 8          # (I) - دهه‌ها سال
    CYCLE = 7               # I - چندین سال
    PRIMARY = 6             # 1 - ماه‌ها تا سال
    INTERMEDIATE = 5        # A - هفته‌ها تا ماه‌ها
    MINOR = 4               # 1 - روزها تا هفته‌ها
    MINUTE = 3              # i - ساعت‌ها تا روز
    MINUETTE = 2            # (i) - دقایق تا ساعت
    SUBMINUETTE = 1         # ((i)) - ثانیه‌ها تا دقایق

class PivotType(Enum):
    """انواع pivot points"""
    HIGH = "high"
    LOW = "low"
    FRACTAL_HIGH = "fractal_high"
    FRACTAL_LOW = "fractal_low"
    SWING_HIGH = "swing_high"
    SWING_LOW = "swing_low"

class ValidationRule(Enum):
    """قوانین اعتبارسنجی"""
    ELLIOTT_RULE_1 = "elliott_rule_1"    # موج 2 < 100% موج 1
    ELLIOTT_RULE_2 = "elliott_rule_2"    # موج 3 != کوتاه‌ترین
    ELLIOTT_RULE_3 = "elliott_rule_3"    # موج 4 خارج از موج 1
    NEOWAVE_TIME = "neowave_time"        # قوانین زمانی NEOWave
    NEOWAVE_COMPLEXITY = "neowave_complexity"  # قوانین پیچیدگی
    FIBONACCI_RELATIONSHIP = "fibonacci_relationship"  # روابط فیبوناچی

@dataclass
class PivotPoint:
    """نقطه pivot پیشرفته"""
    index: int
    price: float
    pivot_type: PivotType
    strength: float = 0.0           # قدرت pivot (0-1)
    volume: float = 0.0            # حجم در pivot
    confirmation: bool = False      # تایید pivot
    timeframe: str = "1h"          # تایم‌فریم
    
    # معیارهای تکنیکال
    rsi_value: float = 50.0
    macd_signal: float = 0.0
    volume_profile: float = 0.0
    
    # روابط فیبوناچی
    fibonacci_cluster: List[float] = field(default_factory=list)
    support_resistance_level: bool = False

@dataclass
class WaveMetrics:
    """معیارهای کمی موج"""
    length: float = 0.0
    duration: int = 0
    velocity: float = 0.0           # length/duration
    angle: float = 0.0             # زاویه موج
    volume_weighted_price: float = 0.0
    
    # نسبت‌های فیبوناچی
    fibonacci_ratios: Dict[str, float] = field(default_factory=dict)
    
    # معیارهای momentum
    rsi_divergence: float = 0.0
    macd_divergence: float = 0.0
    momentum_score: float = 0.0
    
    # کیفیت موج
    clarity_score: float = 0.0      # وضوح موج
    impulsiveness: float = 0.0      # شتاب‌داری موج

@dataclass
class Wave:
    """کلاس موج پیشرفته"""
    wave_id: str
    start_index: int
    end_index: int
    start_price: float
    end_price: float
    high_price: float
    low_price: float
    wave_type: WaveType
    degree: WaveDegree
    label: str
    
    # ساختار موج
    parent_wave: Optional['Wave'] = None
    sub_waves: List['Wave'] = field(default_factory=list)
    
    # معیارهای کمی
    metrics: WaveMetrics = field(default_factory=WaveMetrics)
    
    # اعتبارسنجی
    is_valid: bool = False
    confidence_score: float = 0.0
    validation_errors: List[str] = field(default_factory=list)
    rule_compliance: Dict[ValidationRule, bool] = field(default_factory=dict)
    
    # پیش‌بینی
    targets: Dict[str, float] = field(default_factory=dict)
    invalidation_level: Optional[float] = None
    
    # متادیتا
    identified_at: Optional[str] = None
    
    @property
    def length(self) -> float:
        """طول موج"""
        return abs(self.end_price - self.start_price)
        
    @property
    def duration(self) -> int:
        """مدت زمان موج"""
        return max(1, self.end_index - self.start_index)
        
    @property
    def is_bullish(self) -> bool:
        """موج صعودی"""
        return self.end_price > self.start_price
        
    @property
    def slope(self) -> float:
        """شیب موج"""
        return (self.end_price - self.start_price) / self.duration
        
    @property
    def retracement_ratio(self) -> float:
        """نسبت اصلاح"""
        if self.parent_wave and len(self.parent_wave.sub_waves) >= 2:
            prev_wave = self.parent_wave.sub_waves[-2] if len(self.parent_wave.sub_waves) > 1 else None
            if prev_wave:
                return self.length / prev_wave.length
        return 0.0

class ElliottBasics:
    """کلاس پیشرفته تحلیل امواج Elliott و NEOWave"""
    
    # نسبت‌های فیبوناچی کامل
    FIBONACCI_RATIOS = {
        'retracement': [0.236, 0.382, 0.50, 0.618, 0.786],
        'extension': [1.0, 1.272, 1.414, 1.618, 2.0, 2.618, 3.618, 4.236],
        'projection': [0.618, 1.0, 1.382, 1.618],
        'time': [0.382, 0.618, 1.0, 1.618, 2.618]
    }
    
    # قوانین Elliott و NEOWave
    VALIDATION_RULES = {
        ValidationRule.ELLIOTT_RULE_1: {
            'description': 'موج 2 نباید بیشتر از 100% موج 1 را اصلاح کند',
            'critical': True
        },
        ValidationRule.ELLIOTT_RULE_2: {
            'description': 'موج 3 نباید کوتاه‌ترین موج محرک باشد',
            'critical': True
        },
        ValidationRule.ELLIOTT_RULE_3: {
            'description': 'موج 4 نباید وارد قلمرو موج 1 شود',
            'critical': True
        },
        ValidationRule.NEOWAVE_TIME: {
            'description': 'قوانین زمانی NEOWave - تناسب زمانی امواج',
            'critical': False
        },
        ValidationRule.NEOWAVE_COMPLEXITY: {
            'description': 'قوانین پیچیدگی NEOWave - تفاوت امواج 2 و 4',
            'critical': False
        },
        ValidationRule.FIBONACCI_RELATIONSHIP: {
            'description': 'روابط فیبوناچی بین امواج',
            'critical': False
        }
    }
    
    def __init__(self, data: pd.DataFrame, timeframe: str = "1h"):
        """
        راه‌اندازی تحلیلگر Elliott Wave
        
        Args:
            data: داده‌های قیمتی OHLCV
            timeframe: تایم‌فریم داده‌ها
        """
        if data is None or data.empty:
            raise ValueError("داده‌های قیمتی نمی‌تواند خالی باشد")
            
        self.data = data.copy()
        self.timeframe = timeframe
        self.waves = []
        self.pivot_points = []
        
        # تنظیمات پیشرفته
        self.pivot_strength_threshold = 0.5
        self.wave_confidence_threshold = 0.7
        self.fibonacci_tolerance = 0.05  # 5% تلرانس
        
        # Cache برای بهینه‌سازی
        self.pivot_cache = {}
        self.fibonacci_cache = {}
        
        # محاسبه اندیکاتورهای کمکی
        self._calculate_technical_indicators()
        
        logger.info(f"ElliottBasics راه‌اندازی شد با {len(data)} کندل در تایم‌فریم {timeframe}")
        
    def _calculate_technical_indicators(self):
        """محاسبه اندیکاتورهای تکنیکال کمکی"""
        try:
            # RSI
            delta = self.data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            self.data['rsi'] = 100 - (100 / (1 + rs))
            
            # MACD
            exp1 = self.data['close'].ewm(span=12).mean()
            exp2 = self.data['close'].ewm(span=26).mean()
            macd = exp1 - exp2
            signal_line = macd.ewm(span=9).mean()
            self.data['macd'] = macd
            self.data['macd_signal'] = signal_line
            self.data['macd_histogram'] = macd - signal_line
            
            # Volume Profile (simplified)
            self.data['volume_ma'] = self.data['volume'].rolling(window=20).mean()
            self.data['volume_ratio'] = self.data['volume'] / self.data['volume_ma']
            
            logger.debug("اندیکاتورهای تکنیکال محاسبه شدند")
            
        except Exception as e:
            logger.warning(f"خطا در محاسبه اندیکاتورها: {e}")
            # اضافه کردن مقادیر پیش‌فرض
            self.data['rsi'] = 50.0
            self.data['macd'] = 0.0
            self.data['macd_signal'] = 0.0
            self.data['macd_histogram'] = 0.0
            self.data['volume_ratio'] = 1.0
    
    def identify_pivots(self, window: int = 5, 
                       min_strength: float = 0.3,
                       use_fractal: bool = True,
                       volume_confirmation: bool = True) -> List[PivotPoint]:
        """
        شناسایی پیشرفته نقاط pivot
        
        Args:
            window: اندازه پنجره برای جستجو
            min_strength: حداقل قدرت pivot
            use_fractal: استفاده از fractal pivots
            volume_confirmation: تایید با حجم
        """
        try:
            logger.info(f"شناسایی pivot points با پنجره {window}")
            
            pivots = []
            
            # الگوریتم اصلی pivot detection
            pivots.extend(self._identify_basic_pivots(window, min_strength))
            
            # Fractal pivots (Williams Fractal)
            if use_fractal:
                pivots.extend(self._identify_fractal_pivots())
                
            # Swing pivots (براساس ATR)
            pivots.extend(self._identify_swing_pivots())
            
            # فیلتر و تمیز کردن pivots
            pivots = self._filter_and_clean_pivots(pivots)
            
            # تایید با حجم
            if volume_confirmation:
                pivots = self._confirm_pivots_with_volume(pivots)
                
            # محاسبه قدرت pivots
            pivots = self._calculate_pivot_strength(pivots)
            
            # مرتب‌سازی براساس زمان
            pivots.sort(key=lambda p: p.index)
            
            # فیلتر براساس قدرت
            strong_pivots = [p for p in pivots if p.strength >= min_strength]
            
            self.pivot_points = strong_pivots
            logger.info(f"✅ {len(strong_pivots)} pivot معتبر شناسایی شد")
            
            # تبدیل به فرمت سازگار قدیمی برای compatibility
            legacy_pivots = []
            for pivot in strong_pivots:
                pivot_type_str = 'HIGH' if pivot.pivot_type in [PivotType.HIGH, PivotType.FRACTAL_HIGH, PivotType.SWING_HIGH] else 'LOW'
                legacy_pivots.append((pivot.index, pivot.price, pivot_type_str))
                
            return legacy_pivots
            
        except Exception as e:
            logger.error(f"خطا در شناسایی pivots: {e}")
            return []
    
    def _identify_basic_pivots(self, window: int, min_strength: float) -> List[PivotPoint]:
        """شناسایی pivot های اصلی"""
        pivots = []
        
        try:
            highs = self.data['high'].values
            lows = self.data['low'].values
            volumes = self.data.get('volume', pd.Series([0] * len(self.data))).values
            
            for i in range(window, len(self.data) - window):
                # شناسایی قله‌ها
                if highs[i] == max(highs[i-window:i+window+1]):
                    pivot = PivotPoint(
                        index=i,
                        price=highs[i],
                        pivot_type=PivotType.HIGH,
                        volume=volumes[i],
                        timeframe=self.timeframe
                    )
                    pivots.append(pivot)
                    
                # شناسایی دره‌ها
                if lows[i] == min(lows[i-window:i+window+1]):
                    pivot = PivotPoint(
                        index=i,
                        price=lows[i],
                        pivot_type=PivotType.LOW,
                        volume=volumes[i],
                        timeframe=self.timeframe
                    )
                    pivots.append(pivot)
                    
            return pivots
            
        except Exception as e:
            logger.error(f"خطا در شناسایی basic pivots: {e}")
            return []
    
    def _identify_fractal_pivots(self) -> List[PivotPoint]:
        """شناسایی Williams Fractal pivots"""
        pivots = []
        
        try:
            highs = self.data['high'].values
            lows = self.data['low'].values
            
            # Williams Fractal: 5-period pattern
            for i in range(2, len(self.data) - 2):
                # Fractal Up (قله)
                if (highs[i] > highs[i-1] and highs[i] > highs[i-2] and
                    highs[i] > highs[i+1] and highs[i] > highs[i+2]):
                    
                    pivot = PivotPoint(
                        index=i,
                        price=highs[i],
                        pivot_type=PivotType.FRACTAL_HIGH,
                        timeframe=self.timeframe
                    )
                    pivots.append(pivot)
                    
                # Fractal Down (دره)
                if (lows[i] < lows[i-1] and lows[i] < lows[i-2] and
                    lows[i] < lows[i+1] and lows[i] < lows[i+2]):
                    
                    pivot = PivotPoint(
                        index=i,
                        price=lows[i],
                        pivot_type=PivotType.FRACTAL_LOW,
                        timeframe=self.timeframe
                    )
                    pivots.append(pivot)
                    
            return pivots
            
        except Exception as e:
            logger.error(f"خطا در شناسایی fractal pivots: {e}")
            return []
    
    def _identify_swing_pivots(self) -> List[PivotPoint]:
        """شناسایی Swing pivots براساس ATR"""
        pivots = []
        
        try:
            # محاسبه ATR
            high = self.data['high']
            low = self.data['low']
            close = self.data['close']
            
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            
            true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = true_range.rolling(window=14).mean()
            
            # شناسایی swing points براساس ATR
            for i in range(14, len(self.data) - 1):
                current_atr = atr.iloc[i]
                
                # Swing High
                if (self.data['high'].iloc[i] > self.data['high'].iloc[i-1] + current_atr * 0.5):
                    pivot = PivotPoint(
                        index=i,
                        price=self.data['high'].iloc[i],
                        pivot_type=PivotType.SWING_HIGH,
                        timeframe=self.timeframe
                    )
                    pivots.append(pivot)
                    
                # Swing Low  
                elif (self.data['low'].iloc[i] < self.data['low'].iloc[i-1] - current_atr * 0.5):
                    pivot = PivotPoint(
                        index=i,
                        price=self.data['low'].iloc[i],
                        pivot_type=PivotType.SWING_LOW,
                        timeframe=self.timeframe
                    )
                    pivots.append(pivot)
                    
            return pivots
            
        except Exception as e:
            logger.error(f"خطا در شناسایی swing pivots: {e}")
            return []
    
    def _filter_and_clean_pivots(self, pivots: List[PivotPoint]) -> List[PivotPoint]:
        """فیلتر و تمیز کردن pivot های تکراری"""
        if not pivots:
            return pivots
            
        try:
            # مرتب‌سازی براساس زمان
            pivots.sort(key=lambda p: p.index)
            
            # حذف تکراری‌ها
            cleaned = []
            
            for pivot in pivots:
                # بررسی تداخل با pivots موجود
                overlap = False
                for existing in cleaned:
                    if (abs(pivot.index - existing.index) <= 3 and
                        pivot.pivot_type.value.endswith(existing.pivot_type.value.split('_')[-1])):
                        
                        # نگه‌داشتن قوی‌تر
                        if pivot.price > existing.price and 'HIGH' in pivot.pivot_type.value:
                            cleaned.remove(existing)
                        elif pivot.price < existing.price and 'LOW' in pivot.pivot_type.value:
                            cleaned.remove(existing)
                        else:
                            overlap = True
                        break
                        
                if not overlap:
                    cleaned.append(pivot)
                    
            # اطمینان از alternating pattern (HIGH-LOW-HIGH-...)
            alternating = []
            last_type = None
            
            for pivot in cleaned:
                current_type = 'HIGH' if 'HIGH' in pivot.pivot_type.value else 'LOW'
                if last_type != current_type:
                    alternating.append(pivot)
                    last_type = current_type
                    
            return alternating
            
        except Exception as e:
            logger.error(f"خطا در فیلتر pivots: {e}")
            return pivots
    
    def _confirm_pivots_with_volume(self, pivots: List[PivotPoint]) -> List[PivotPoint]:
        """تایید pivots با حجم"""
        try:
            if 'volume' not in self.data.columns:
                return pivots
                
            confirmed_pivots = []
            volume_ma = self.data['volume'].rolling(window=20).mean()
            
            for pivot in pivots:
                try:
                    pivot_volume = self.data['volume'].iloc[pivot.index]
                    avg_volume = volume_ma.iloc[pivot.index]
                    
                    # اگر حجم بالاتر از میانگین باشد، pivot قوی‌تر است
                    if pivot_volume > avg_volume * 1.2:
                        pivot.volume_profile = 1.0
                    elif pivot_volume > avg_volume:
                        pivot.volume_profile = 0.7
                    else:
                        pivot.volume_profile = 0.3
                        
                    pivot.confirmation = pivot.volume_profile >= 0.5
                    confirmed_pivots.append(pivot)
                    
                except IndexError:
                    # در صورت خطای index، pivot را با تایید پایین اضافه می‌کنیم
                    pivot.volume_profile = 0.3
                    pivot.confirmation = False
                    confirmed_pivots.append(pivot)
                    
            return confirmed_pivots
            
        except Exception as e:
            logger.error(f"خطا در تایید حجمی pivots: {e}")
            return pivots
    
    def _calculate_pivot_strength(self, pivots: List[PivotPoint]) -> List[PivotPoint]:
        """محاسبه قدرت pivots"""
        try:
            for pivot in pivots:
                strength_factors = []
                
                try:
                    # قدرت براساس نوع pivot
                    if pivot.pivot_type == PivotType.FRACTAL_HIGH or pivot.pivot_type == PivotType.FRACTAL_LOW:
                        strength_factors.append(0.8)
                    elif pivot.pivot_type == PivotType.SWING_HIGH or pivot.pivot_type == PivotType.SWING_LOW:
                        strength_factors.append(0.6)
                    else:
                        strength_factors.append(0.4)
                        
                    # قدرت براساس حجم
                    strength_factors.append(pivot.volume_profile * 0.3)
                    
                    # قدرت براساس RSI divergence
                    if pivot.index < len(self.data):
                        rsi_value = self.data['rsi'].iloc[pivot.index] if 'rsi' in self.data.columns else 50
                        
                        if 'HIGH' in pivot.pivot_type.value and rsi_value > 70:
                            strength_factors.append(0.2)
                        elif 'LOW' in pivot.pivot_type.value and rsi_value < 30:
                            strength_factors.append(0.2)
                        else:
                            strength_factors.append(0.1)
                            
                        pivot.rsi_value = rsi_value
                        
                    # محاسبه قدرت کل
                    pivot.strength = min(1.0, sum(strength_factors))
                    
                except (IndexError, KeyError):
                    pivot.strength = 0.5  # مقدار پیش‌فرض
                    
            return pivots
            
        except Exception as e:
            logger.error(f"خطا در محاسبه قدرت pivots: {e}")
            return pivots
    
    def create_wave_from_pivots(self, pivots: List[Tuple], 
                              wave_type: WaveType = WaveType.IMPULSE,
                              degree: WaveDegree = WaveDegree.MINOR) -> Optional[Wave]:
        """ایجاد موج از pivot points"""
        try:
            if len(pivots) < 2:
                return None
                
            start_pivot = pivots[0]
            end_pivot = pivots[-1]
            
            # یافتن highest و lowest در بازه
            start_idx, end_idx = start_pivot[0], end_pivot[0]
            wave_data = self.data.iloc[start_idx:end_idx+1]
            
            if wave_data.empty:
                return None
                
            high_price = wave_data['high'].max()
            low_price = wave_data['low'].min()
            
            # ایجاد wave ID یکتا
            wave_id = f"{wave_type.value}_{degree.value}_{start_idx}_{end_idx}"
            
            wave = Wave(
                wave_id=wave_id,
                start_index=start_idx,
                end_index=end_idx,
                start_price=start_pivot[1],
                end_price=end_pivot[1],
                high_price=high_price,
                low_price=low_price,
                wave_type=wave_type,
                degree=degree,
                label=f"{wave_type.value[0].upper()}-{degree.value}",
                identified_at=pd.Timestamp.now().isoformat()
            )
            
            # محاسبه metrics
            self._calculate_wave_metrics(wave)
            
            return wave
            
        except Exception as e:
            logger.error(f"خطا در ایجاد موج: {e}")
            return None
    
    def _calculate_wave_metrics(self, wave: Wave):
        """محاسبه معیارهای کمی موج"""
        try:
            metrics = WaveMetrics()
            
            # معیارهای اصلی
            metrics.length = wave.length
            metrics.duration = wave.duration
            metrics.velocity = metrics.length / metrics.duration if metrics.duration > 0 else 0
            metrics.angle = np.degrees(np.arctan(wave.slope)) if wave.duration > 0 else 0
            
            # Volume weighted price
            if wave.end_index < len(self.data):
                wave_data = self.data.iloc[wave.start_index:wave.end_index+1]
                if 'volume' in wave_data.columns and not wave_data['volume'].sum() == 0:
                    metrics.volume_weighted_price = (
                        (wave_data['close'] * wave_data['volume']).sum() / 
                        wave_data['volume'].sum()
                    )
                else:
                    metrics.volume_weighted_price = wave_data['close'].mean()
                    
                # Momentum analysis
                if len(wave_data) > 5:
                    metrics.momentum_score = self._calculate_momentum_score(wave_data)
                    metrics.clarity_score = self._calculate_clarity_score(wave_data)
                    metrics.impulsiveness = self._calculate_impulsiveness(wave_data)
                    
            wave.metrics = metrics
            
        except Exception as e:
            logger.error(f"خطا در محاسبه metrics موج: {e}")
            wave.metrics = WaveMetrics()
    
    def _calculate_momentum_score(self, wave_data: pd.DataFrame) -> float:
        """محاسبه امتیاز momentum"""
        try:
            if 'rsi' not in wave_data.columns:
                return 0.5
                
            rsi_values = wave_data['rsi'].dropna()
            if len(rsi_values) < 2:
                return 0.5
                
            # تحلیل تغییرات RSI
            rsi_trend = np.polyfit(range(len(rsi_values)), rsi_values, 1)[0]
            
            # تبدیل به امتیاز 0-1
            momentum = (rsi_trend + 10) / 20  # فرض: RSI trend بین -10 تا +10
            return max(0, min(1, momentum))
            
        except:
            return 0.5
    
    def _calculate_clarity_score(self, wave_data: pd.DataFrame) -> float:
        """محاسبه وضوح موج"""
        try:
            closes = wave_data['close']
            
            # محاسبه correlation با خط مستقیم
            x = np.arange(len(closes))
            correlation = np.corrcoef(x, closes)[0, 1]
            
            # تبدیل به امتیاز مثبت
            clarity = abs(correlation) if not np.isnan(correlation) else 0
            return clarity
            
        except:
            return 0.0
    
    def _calculate_impulsiveness(self, wave_data: pd.DataFrame) -> float:
        """محاسبه شتاب‌داری موج"""
        try:
            # براساس نسبت حجم و تغییرات قیمت
            if 'volume' not in wave_data.columns:
                return 0.5
                
            price_changes = wave_data['close'].pct_change().abs()
            volume_changes = wave_data['volume'].pct_change().abs()
            
            # همبستگی حجم و تغییرات قیمت
            correlation = np.corrcoef(price_changes.dropna(), volume_changes.dropna())[0, 1]
            
            impulsiveness = abs(correlation) if not np.isnan(correlation) else 0.5
            return impulsiveness
            
        except:
            return 0.5
    
    def validate_elliott_rules(self, waves: List[Wave]) -> Dict[ValidationRule, bool]:
        """اعتبارسنجی کامل قوانین Elliott و NEOWave"""
        try:
            results = {}
            
            if len(waves) >= 5:  # برای الگوی 5-موجی
                # Elliott Rule 1: موج 2 < 100% موج 1
                wave1 = waves[0]
                wave2 = waves[1]
                results[ValidationRule.ELLIOTT_RULE_1] = wave2.length < wave1.length
                
                # Elliott Rule 2: موج 3 != کوتاه‌ترین
                wave3 = waves[2]
                wave5 = waves[4] if len(waves) > 4 else None
                impulse_lengths = [wave1.length, wave3.length]
                if wave5:
                    impulse_lengths.append(wave5.length)
                results[ValidationRule.ELLIOTT_RULE_2] = wave3.length != min(impulse_lengths)
                
                # Elliott Rule 3: موج 4 خارج از موج 1
                if len(waves) >= 4:
                    wave4 = waves[3]
                    if wave1.is_bullish:
                        results[ValidationRule.ELLIOTT_RULE_3] = wave4.end_price > wave1.end_price
                    else:
                        results[ValidationRule.ELLIOTT_RULE_3] = wave4.end_price < wave1.end_price
                        
                # NEOWave Time Rule
                results[ValidationRule.NEOWAVE_TIME] = self._validate_neowave_time(waves)
                
                # NEOWave Complexity Rule
                results[ValidationRule.NEOWAVE_COMPLEXITY] = self._validate_neowave_complexity(waves)
                
                # Fibonacci Relationships
                results[ValidationRule.FIBONACCI_RELATIONSHIP] = self._validate_fibonacci_relationships(waves)
                
            else:
                # اگر کمتر از 5 موج داریم، فقط قوانین قابل اجرا را بررسی می‌کنیم
                for rule in ValidationRule:
                    results[rule] = False
                    
            return results
            
        except Exception as e:
            logger.error(f"خطا در اعتبارسنجی قوانین: {e}")
            return {rule: False for rule in ValidationRule}
    
    def _validate_neowave_time(self, waves: List[Wave]) -> bool:
        """اعتبارسنجی قوانین زمانی NEOWave"""
        try:
            if len(waves) < 3:
                return False
                
            # موج 2 باید حداقل 1/3 زمان موج 1 داشته باشد
            wave1_time = waves[0].duration
            wave2_time = waves[1].duration
            
            time_ratio = wave2_time / wave1_time if wave1_time > 0 else 0
            
            # قانون NEOWave: 0.33 <= نسبت زمانی <= 3.0
            return 0.33 <= time_ratio <= 3.0
            
        except:
            return False
    
    def _validate_neowave_complexity(self, waves: List[Wave]) -> bool:
        """اعتبارسنجی قوانین پیچیدگی NEOWave"""
        try:
            if len(waves) < 4:
                return False
                
            # موج‌های 2 و 4 باید در پیچیدگی متفاوت باشند
            wave2 = waves[1]
            wave4 = waves[3]
            
            # مقایسه تعداد sub-waves (اگر موجود)
            wave2_complexity = len(wave2.sub_waves) if wave2.sub_waves else 1
            wave4_complexity = len(wave4.sub_waves) if wave4.sub_waves else 1
            
            # مقایسه مدت زمان
            time_complexity_diff = abs(wave2.duration - wave4.duration) / max(wave2.duration, wave4.duration)
            
            # مقایسه طول
            length_complexity_diff = abs(wave2.length - wave4.length) / max(wave2.length, wave4.length)
            
            # اگر حداقل یکی از معیارها تفاوت معنی‌دار داشته باشد
            return (wave2_complexity != wave4_complexity or 
                   time_complexity_diff > 0.2 or 
                   length_complexity_diff > 0.2)
            
        except:
            return False
    
    def _validate_fibonacci_relationships(self, waves: List[Wave]) -> bool:
        """اعتبارسنجی روابط فیبوناچی"""
        try:
            fibonacci_matches = 0
            total_comparisons = 0
            
            # بررسی نسبت‌های فیبوناچی بین امواج
            for i in range(len(waves)):
                for j in range(i + 1, len(waves)):
                    if waves[j].length > 0:
                        ratio = waves[i].length / waves[j].length
                        
                        # یافتن نزدیک‌ترین نسبت فیبوناچی
                        all_fib_ratios = (self.FIBONACCI_RATIOS['retracement'] + 
                                        self.FIBONACCI_RATIOS['extension'])
                        
                        closest_fib = min(all_fib_ratios, key=lambda x: abs(x - ratio))
                        
                        # اگر نزدیک به نسبت فیبوناچی باشد
                        if abs(ratio - closest_fib) / closest_fib <= self.fibonacci_tolerance:
                            fibonacci_matches += 1
                            
                        total_comparisons += 1
                        
            # حداقل 30% روابط باید فیبوناچی باشند
            if total_comparisons > 0:
                fibonacci_ratio = fibonacci_matches / total_comparisons
                return fibonacci_ratio >= 0.3
            else:
                return False
                
        except:
            return False
    
    def calculate_fibonacci_levels(self, start_price: float, end_price: float,
                                 level_type: str = 'retracement') -> Dict[float, float]:
        """محاسبه سطوح فیبوناچی پیشرفته"""
        try:
            if level_type not in self.FIBONACCI_RATIOS:
                level_type = 'retracement'
                
            levels = {}
            price_diff = end_price - start_price
            
            for ratio in self.FIBONACCI_RATIOS[level_type]:
                if price_diff >= 0:  # حرکت صعودی
                    if level_type == 'retracement':
                        levels[ratio] = end_price - (price_diff * ratio)
                    else:  # extension
                        levels[ratio] = start_price + (price_diff * ratio)
                else:  # حرکت نزولی
                    if level_type == 'retracement':
                        levels[ratio] = end_price - (price_diff * ratio)
                    else:  # extension
                        levels[ratio] = start_price + (price_diff * ratio)
                        
            return levels
            
        except Exception as e:
            logger.error(f"خطا در محاسبه سطوح فیبوناچی: {e}")
            return {}
    
    def calculate_wave_targets(self, waves: List[Wave]) -> Dict[str, float]:
        """محاسبه اهداف احتمالی موج بعدی"""
        try:
            targets = {}
            
            if len(waves) < 2:
                return targets
                
            # موج آخر
            last_wave = waves[-1]
            
            # هدف براساس نسبت‌های فیبوناچی
            if len(waves) >= 2:
                prev_wave = waves[-2]
                
                # اهداف extension
                for ratio in [1.0, 1.272, 1.618, 2.618]:
                    if last_wave.is_bullish:
                        target_price = last_wave.start_price + (prev_wave.length * ratio)
                    else:
                        target_price = last_wave.start_price - (prev_wave.length * ratio)
                        
                    targets[f'fib_{ratio}'] = target_price
                    
            # هدف براساس الگوی کلی
            if len(waves) >= 3:
                # الگوی ABC
                wave_a = waves[0]
                wave_c_target = wave_a.length * 1.0  # C = A
                
                if last_wave.is_bullish:
                    targets['abc_parity'] = last_wave.start_price + wave_c_target
                else:
                    targets['abc_parity'] = last_wave.start_price - wave_c_target
                    
            return targets
            
        except Exception as e:
            logger.error(f"خطا در محاسبه اهداف: {e}")
            return {}
    
    def get_wave_statistics(self) -> Dict:
        """آمار کلی امواج شناسایی شده"""
        try:
            stats = {
                'total_waves': len(self.waves),
                'wave_types': {},
                'wave_degrees': {},
                'average_length': 0.0,
                'average_duration': 0.0,
                'valid_waves': 0,
                'confidence_distribution': {
                    'high': 0,    # > 0.8
                    'medium': 0,  # 0.6-0.8
                    'low': 0      # < 0.6
                }
            }
            
            if not self.waves:
                return stats
                
            # آمار انواع موج
            for wave in self.waves:
                wave_type = wave.wave_type.value
                stats['wave_types'][wave_type] = stats['wave_types'].get(wave_type, 0) + 1
                
                degree = wave.degree.name
                stats['wave_degrees'][degree] = stats['wave_degrees'].get(degree, 0) + 1
                
                if wave.is_valid:
                    stats['valid_waves'] += 1
                    
                # توزیع اعتماد
                if wave.confidence_score > 0.8:
                    stats['confidence_distribution']['high'] += 1
                elif wave.confidence_score > 0.6:
                    stats['confidence_distribution']['medium'] += 1
                else:
                    stats['confidence_distribution']['low'] += 1
                    
            # میانگین‌ها
            lengths = [wave.length for wave in self.waves]
            durations = [wave.duration for wave in self.waves]
            
            stats['average_length'] = np.mean(lengths) if lengths else 0.0
            stats['average_duration'] = np.mean(durations) if durations else 0.0
            
            return stats
            
        except Exception as e:
            logger.error(f"خطا در محاسبه آمار: {e}")
            return {}