"""
امواج شتابدار و انواع آن - نسخه پیشرفته
Advanced Impulse Wave Analysis with Enhanced Accuracy
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ImpulseType(Enum):
    """انواع الگوی شتابدار"""
    SIMPLE_TRENDING = "روند دار ساده"
    EXTENDED_1 = "موج 1 ممتد"
    EXTENDED_3 = "موج 3 ممتد"
    EXTENDED_5 = "موج 5 ممتد"
    DOUBLE_EXTENDED = "امتداد دوگانه"
    TRUNCATED_5 = "موج 5 کوتاه شده"
    LEADING_DIAGONAL = "قطری پیشرو"
    ENDING_DIAGONAL = "قطری پایانی"
    COMPLEX_IMPULSE = "شتابدار پیچیده"

class ValidationLevel(Enum):
    """سطح دقت اعتبارسنجی"""
    HIGH = "دقیق"
    MEDIUM = "متوسط"
    LOW = "آزاد"

@dataclass
class WaveMetrics:
    """متریک های پیشرفته موج"""
    fibonacci_accuracy: float = 0.0
    fibonacci_extensions: Dict[str, float] = field(default_factory=dict)
    fibonacci_retracements: Dict[str, float] = field(default_factory=dict)
    channeling_quality: float = 0.0
    momentum_confirmation: float = 0.0
    volume_confirmation: float = 0.0
    time_proportions: Dict[str, float] = field(default_factory=dict)
    fractal_dimension: float = 1.5
    hurst_exponent: float = 0.5
    predictive_power: float = 0.0
    structural_integrity: float = 0.0
    wave_personality: Dict[str, float] = field(default_factory=dict)
    alternation_score: float = 0.0
    complexity_index: float = 0.0
    market_context_score: float = 0.0
    
    def calculate_overall_score(self) -> float:
        """محاسبه امتیاز کلی موج"""
        weights = {
            'fibonacci_accuracy': 0.25,
            'channeling_quality': 0.15,
            'momentum_confirmation': 0.15,
            'volume_confirmation': 0.10,
            'structural_integrity': 0.20,
            'predictive_power': 0.15
        }
        
        score = 0.0
        for metric, weight in weights.items():
            score += getattr(self, metric, 0.0) * weight
            
        return min(max(score, 0.0), 1.0)

@dataclass
class ImpulseWave:
    """کلاس موج شتابدار پیشرفته"""
    wave_type: ImpulseType
    waves: List[Dict]  # لیست 5 موج
    start_price: float
    end_price: float
    start_index: int
    end_index: int
    is_valid: bool = False
    validation_errors: List[str] = field(default_factory=list)
    validation_warnings: List[str] = field(default_factory=list)
    
    # ویژگی های پیشرفته جدید
    wave_id: str = ""
    confidence_score: float = 0.0
    confidence_level: str = "LOW"
    degree: int = 0
    direction: str = "UP"
    validation_level: ValidationLevel = ValidationLevel.MEDIUM
    metrics: Optional[WaveMetrics] = None
    projections: Dict[str, any] = field(default_factory=dict)
    fibonacci_targets: Dict[str, float] = field(default_factory=dict)
    next_wave_prediction: Dict[str, any] = field(default_factory=dict)
    invalidation_level: float = 0.0
    market_context: Dict[str, any] = field(default_factory=dict)
    timeframe: str = "1h"
    
    def __post_init__(self):
        if self.validation_errors is None:
            self.validation_errors = []
        if self.metrics is None:
            self.metrics = WaveMetrics()
        if not self.wave_id:
            self.wave_id = f"IMP_{self.start_index}_{datetime.now().strftime('%H%M%S')}"
        self._update_confidence_level()
    
    def _update_confidence_level(self):
        """به روزرسانی سطح اطمینان"""
        if self.confidence_score >= 0.9:
            self.confidence_level = "VERY_HIGH"
        elif self.confidence_score >= 0.75:
            self.confidence_level = "HIGH"
        elif self.confidence_score >= 0.6:
            self.confidence_level = "MEDIUM"
        elif self.confidence_score >= 0.4:
            self.confidence_level = "LOW"
        else:
            self.confidence_level = "VERY_LOW"

class AdvancedFibonacciAnalyzer:
    """تحلیلگر پیشرفته فیبوناچی"""
    
    # نسبت های فیبوناچی کلاسیک و نئوویو
    FIBONACCI_RATIOS = {
        'retracements': [0.236, 0.382, 0.500, 0.618, 0.786],
        'extensions': [1.000, 1.272, 1.382, 1.618, 2.000, 2.618, 3.618, 4.236],
        'time_ratios': [0.382, 0.618, 1.000, 1.618, 2.618],
        'neowave_special': [0.146, 0.854, 1.146, 1.854, 2.146]  # نسبت های ویژه نئوویو
    }
    
    @staticmethod
    def calculate_fibonacci_accuracy(wave_data: Dict, reference_wave: Dict = None) -> float:
        """محاسبه دقت فیبوناچی با الگوریتم بهبود یافته"""
        try:
            if not reference_wave:
                return 0.5
                
            wave_length = abs(wave_data['end'][1] - wave_data['start'][1])
            ref_length = abs(reference_wave['end'][1] - reference_wave['start'][1])
            
            if ref_length == 0:
                return 0.0
                
            ratio = wave_length / ref_length
            
            # بررسی نزدیکی به نسبت های فیبوناچی
            best_accuracy = 0.0
            tolerance = 0.05  # 5% تلرانس
            
            for ratio_set in AdvancedFibonacciAnalyzer.FIBONACCI_RATIOS.values():
                for fib_ratio in ratio_set:
                    deviation = abs(ratio - fib_ratio) / fib_ratio
                    if deviation <= tolerance:
                        accuracy = 1.0 - (deviation / tolerance)
                        best_accuracy = max(best_accuracy, accuracy)
                        
            return min(best_accuracy, 1.0)
            
        except Exception:
            return 0.0
    
    @staticmethod
    def find_fibonacci_relationships(waves: List[Dict]) -> Dict[str, float]:
        """یافتن روابط فیبوناچی پیشرفته بین امواج"""
        relationships = {}
        
        try:
            if len(waves) < 3:
                return relationships
                
            # بررسی روابط بین امواج محرک (1, 3, 5)
            impulse_indices = [0, 2, 4]
            impulse_waves = [waves[i] for i in impulse_indices if i < len(waves)]
            
            for i, wave1 in enumerate(impulse_waves):
                for j, wave2 in enumerate(impulse_waves):
                    if i != j:
                        length1 = abs(wave1['end'][1] - wave1['start'][1])
                        length2 = abs(wave2['end'][1] - wave2['start'][1])
                        
                        if length2 != 0:
                            ratio = length1 / length2
                            wave1_num = wave1.get('number', i+1)
                            wave2_num = wave2.get('number', j+1)
                            key = f"wave_{wave1_num}_to_{wave2_num}"
                            relationships[key] = ratio
            
            # تحلیل روابط زمانی
            for i in range(len(waves)-1):
                duration1 = waves[i].get('duration', 1)
                duration2 = waves[i+1].get('duration', 1)
                if duration2 != 0:
                    time_ratio = duration1 / duration2
                    relationships[f"time_{i+1}_to_{i+2}"] = time_ratio
                            
            return relationships
            
        except Exception:
            return {}

class AdvancedVolumeAnalyzer:
    """تحلیلگر پیشرفته حجم معاملات"""
    
    @staticmethod
    def analyze_volume_confirmation(price_data: pd.DataFrame, wave_start: int, 
                                  wave_end: int, wave_direction: str) -> float:
        """تحلیل پیشرفته تأیید حجم برای موج"""
        try:
            if 'volume' not in price_data.columns or wave_start >= len(price_data) or wave_end >= len(price_data):
                return 0.5  # حالت خنثی
                
            wave_data = price_data.iloc[wave_start:wave_end+1]
            
            if len(wave_data) < 3:
                return 0.5
                
            # محاسبه متغیرهای حجم
            volumes = wave_data['volume'].values
            prices = wave_data['close'].values
            
            avg_volume = np.mean(volumes)
            volume_trend = np.corrcoef(range(len(volumes)), volumes)[0,1] if len(volumes) > 1 else 0
            
            # تحلیل توزیع حجم
            high_volume_periods = len([v for v in volumes if v > avg_volume * 1.5])
            total_periods = len(volumes)
            
            confirmation_score = 0.0
            
            # بررسی افزایش حجم در جهت موج
            price_change = prices[-1] - prices[0]
            
            if (wave_direction == "UP" and price_change > 0) or (wave_direction == "DOWN" and price_change < 0):
                # جهت قیمت و موج همسو است
                if volume_trend > 0.1:  # حجم در حال افزایش
                    confirmation_score += 0.4
                    
                # بررسی حجم در نقاط کلیدی
                if high_volume_periods / total_periods > 0.3:  # بیش از 30% دوره ها حجم بالا
                    confirmation_score += 0.3
                    
                # بررسی حجم در ابتدا و انتها
                start_volume = volumes[0]
                end_volume = volumes[-1]
                
                if end_volume > start_volume:
                    confirmation_score += 0.2
                    
                # بونوس برای حجم فوق العاده
                max_volume = np.max(volumes)
                if max_volume > avg_volume * 2:
                    confirmation_score += 0.1
                    
            return min(confirmation_score, 1.0)
            
        except Exception:
            return 0.5

class AdvancedMomentumAnalyzer:
    """تحلیلگر پیشرفته مومنتوم"""
    
    @staticmethod
    def calculate_momentum_confirmation(price_data: pd.DataFrame, wave_start: int, 
                                      wave_end: int, wave_direction: str) -> float:
        """محاسبه پیشرفته تأیید مومنتوم"""
        try:
            if wave_start >= len(price_data) or wave_end >= len(price_data):
                return 0.5
                
            wave_data = price_data.iloc[wave_start:wave_end+1]
            
            if len(wave_data) < 5:
                return 0.5
                
            prices = wave_data['close'].values
            highs = wave_data['high'].values
            lows = wave_data['low'].values
            
            # محاسبه اندیکاتورهای مومنتوم
            rsi = AdvancedMomentumAnalyzer._calculate_rsi(prices)
            stoch = AdvancedMomentumAnalyzer._calculate_stochastic(prices, highs, lows)
            roc = AdvancedMomentumAnalyzer._calculate_roc(prices)
            
            momentum_score = 0.0
            
            # بررسی RSI
            rsi_start = rsi[0] if len(rsi) > 0 else 50
            rsi_end = rsi[-1] if len(rsi) > 0 else 50
            
            if wave_direction == "UP":
                if rsi_end > 50 and rsi_end > rsi_start:
                    momentum_score += 0.3
                if rsi_end > 70:  # overbought که تأیید میکند
                    momentum_score += 0.1
            else:
                if rsi_end < 50 and rsi_end < rsi_start:
                    momentum_score += 0.3
                if rsi_end < 30:  # oversold که تأیید میکند
                    momentum_score += 0.1
                    
            # بررسی Stochastic
            if len(stoch) > 1:
                stoch_start = stoch[0]
                stoch_end = stoch[-1]
                
                if wave_direction == "UP":
                    if stoch_end > 50 and stoch_end > stoch_start:
                        momentum_score += 0.2
                else:
                    if stoch_end < 50 and stoch_end < stoch_start:
                        momentum_score += 0.2
                        
            # بررسی Rate of Change
            if len(roc) > 1:
                avg_roc = np.mean(roc)
                if wave_direction == "UP" and avg_roc > 0:
                    momentum_score += 0.2
                elif wave_direction == "DOWN" and avg_roc < 0:
                    momentum_score += 0.2
                    
            return min(momentum_score, 1.0)
            
        except Exception:
            return 0.5
    
    @staticmethod
    def _calculate_rsi(prices: np.ndarray, period: int = 14) -> np.ndarray:
        """محاسبه RSI بهبود یافته"""
        try:
            if len(prices) < period + 1:
                return np.full(len(prices), 50.0)
                
            deltas = np.diff(prices)
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            # محاسبه میانگین متحرک نمایی
            alpha = 1.0 / period
            avg_gains = np.zeros_like(gains)
            avg_losses = np.zeros_like(losses)
            
            # مقدار اولیه
            avg_gains[0] = np.mean(gains[:period]) if len(gains) >= period else np.mean(gains)
            avg_losses[0] = np.mean(losses[:period]) if len(losses) >= period else np.mean(losses)
            
            for i in range(1, len(gains)):
                avg_gains[i] = alpha * gains[i] + (1 - alpha) * avg_gains[i-1]
                avg_losses[i] = alpha * losses[i] + (1 - alpha) * avg_losses[i-1]
            
            rs = avg_gains / (avg_losses + 1e-10)
            rsi = 100 - (100 / (1 + rs))
            
            # پر کردن مقادیر اولیه
            rsi_full = np.full(len(prices), 50.0)
            rsi_full[1:] = rsi
            
            return rsi_full
            
        except Exception:
            return np.full(len(prices), 50.0)
    
    @staticmethod
    def _calculate_stochastic(close: np.ndarray, high: np.ndarray, low: np.ndarray, period: int = 14) -> np.ndarray:
        """محاسبه Stochastic بهبود یافته"""
        try:
            if len(close) < period:
                return np.full(len(close), 50.0)
                
            stoch_k = np.zeros_like(close)
            
            for i in range(period-1, len(close)):
                highest = np.max(high[max(0, i-period+1):i+1])
                lowest = np.min(low[max(0, i-period+1):i+1])
                
                if highest != lowest:
                    stoch_k[i] = 100 * (close[i] - lowest) / (highest - lowest)
                else:
                    stoch_k[i] = 50.0
                    
            # پر کردن مقادیر اولیه
            stoch_k[:period-1] = 50.0
            
            return stoch_k
            
        except Exception:
            return np.full(len(close), 50.0)
    
    @staticmethod
    def _calculate_roc(prices: np.ndarray, period: int = 10) -> np.ndarray:
        """محاسبه Rate of Change"""
        try:
            if len(prices) < period + 1:
                return np.zeros(len(prices))
                
            roc = np.zeros_like(prices)
            
            for i in range(period, len(prices)):
                if prices[i-period] != 0:
                    roc[i] = ((prices[i] - prices[i-period]) / prices[i-period]) * 100
                    
            return roc
            
        except Exception:
            return np.zeros(len(prices))

class ImpulseWaveAnalyzer:
    """تحلیلگر پیشرفته امواج شتابدار"""
    
    # قوانین نقض ناپذیر امواج شتابدار با دقت بالا
    IMPULSE_RULES = {
        'cardinal_rule_1': {
            'description': 'موج 2 نمی تواند بیش از 100% موج 1 را اصلاح کند',
            'critical': True,
            'tolerance': 0.02
        },
        'cardinal_rule_2': {
            'description': 'موج 3 نمی تواند کوتاه ترین موج محرک باشد',
            'critical': True,
            'tolerance': 0.0
        },
        'cardinal_rule_3': {
            'description': 'موج 4 نمی تواند وارد قلمرو قیمتی موج 1 شود',
            'critical': True,
            'tolerance': 0.03
        },
        'neowave_rule_1': {
            'description': 'موج 2 باید حداقل 38.2% موج 1 را اصلاح کند',
            'critical': False,
            'tolerance': 0.1
        },
        'neowave_rule_2': {
            'description': 'موج 3 باید حداقل 161.8% موج 1 باشد',
            'critical': False,
            'tolerance': 0.15
        },
        'time_rule_1': {
            'description': 'موج 2 باید حداقل 1/3 زمان موج 1 را اشغال کند',
            'critical': False,
            'tolerance': 0.2
        },
        'proportion_rule': {
            'description': 'تناسب های فیبوناچی باید رعایت شود',
            'critical': False,
            'tolerance': 0.25
        }
    }
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.identified_impulses = []
        self.fibonacci_analyzer = AdvancedFibonacciAnalyzer()
        self.volume_analyzer = AdvancedVolumeAnalyzer()
        self.momentum_analyzer = AdvancedMomentumAnalyzer()
        
        # آماده سازی داده های تکمیلی
        self._prepare_enhanced_data()
        
    def _prepare_enhanced_data(self):
        """آماده سازی داده های تکمیلی برای تحلیل پیشرفته"""
        try:
            # محاسبه بازدهی
            self.data['returns'] = self.data['close'].pct_change()
            
            # محاسبه نوسان پذیری
            self.data['volatility'] = self.data['returns'].rolling(window=20).std()
            
            # محاسبه میانگین های متحرک
            self.data['sma_20'] = self.data['close'].rolling(window=20).mean()
            self.data['sma_50'] = self.data['close'].rolling(window=50).mean()
            
            # محاسبه ATR (Average True Range)
            high_low = self.data['high'] - self.data['low']
            high_close = np.abs(self.data['high'] - self.data['close'].shift())
            low_close = np.abs(self.data['low'] - self.data['close'].shift())
            
            true_range = np.maximum(high_low, np.maximum(high_close, low_close))
            self.data['atr'] = true_range.rolling(window=14).mean()
            
            # محاسبه Bollinger Bands
            bb_period = 20
            bb_std = 2
            bb_ma = self.data['close'].rolling(window=bb_period).mean()
            bb_stddev = self.data['close'].rolling(window=bb_period).std()
            self.data['bb_upper'] = bb_ma + (bb_stddev * bb_std)
            self.data['bb_lower'] = bb_ma - (bb_stddev * bb_std)
            
            # پر کردن مقادیر NaN
            self.data.fillna(method='forward', inplace=True)
            self.data.fillna(method='backward', inplace=True)
            
        except Exception:
            pass  # در صورت خطا، ادامه با داده های اصلی
        
    def identify_impulse_patterns(self, pivots: List[Tuple]) -> List[ImpulseWave]:
        """شناسایی الگوهای شتابدار با دقت فوق العاده بالا"""
        impulses = []
        
        try:
            if len(pivots) < 9:
                return impulses
                
            # تحلیل با پنجره های مختلف برای دقت بیشتر
            for window_size in [9, 11, 13, 15]:
                new_impulses = self._analyze_with_enhanced_window(pivots, window_size)
                impulses.extend(new_impulses)
            
            # حذف موج های تکراری
            impulses = self._remove_duplicate_impulses(impulses)
            
            # فیلتر کردن براساس کیفیت
            high_quality_impulses = [imp for imp in impulses if imp.confidence_score >= 0.6]
            
            # مرتب سازی براساس اطمینان
            high_quality_impulses.sort(key=lambda x: x.confidence_score, reverse=True)
            
            self.identified_impulses.extend(high_quality_impulses)
            return high_quality_impulses
            
        except Exception:
            return []
    
    def identify_impulse_patterns_advanced(self, pivots: List[Tuple], degree: int = 0, 
                                         min_confidence: float = 0.6) -> List[ImpulseWave]:
        """شناسایی پیشرفته الگوهای شتابدار"""
        return self.identify_impulse_patterns(pivots)
    
    def _analyze_with_enhanced_window(self, pivots: List[Tuple], window_size: int) -> List[ImpulseWave]:
        """تحلیل پیشرفته با پنجره مشخص"""
        impulses = []
        
        for i in range(len(pivots) - window_size + 1):
            try:
                wave_pivots = pivots[i:i + window_size]
                
                # بررسی پیشرفته الترناسیون
                if not self._check_enhanced_alternation(wave_pivots):
                    continue
                
                # ساخت موج های فرعی پیشرفته
                sub_waves = self._build_enhanced_sub_waves(wave_pivots)
                if not sub_waves or len(sub_waves) != 5:
                    continue
                
                # تعیین نوع الگو
                impulse_type = self._determine_enhanced_impulse_type(sub_waves)
                
                # تعیین جهت
                direction = self._determine_wave_direction(sub_waves)
                
                # ایجاد موج شتابدار
                impulse = ImpulseWave(
                    wave_type=impulse_type,
                    waves=sub_waves,
                    start_price=wave_pivots[0][1],
                    end_price=wave_pivots[-1][1],
                    start_index=wave_pivots[0][0],
                    end_index=wave_pivots[-1][0],
                    direction=direction,
                    validation_level=ValidationLevel.HIGH
                )
                
                # اعتبارسنجی جامع
                self._validate_impulse_comprehensive(impulse)
                
                # محاسبه متریک های پیشرفته
                self._calculate_enhanced_metrics(impulse)
                
                # محاسبه امتیاز اطمینان
                self._calculate_enhanced_confidence_score(impulse)
                
                # پروژکشن ها
                self._calculate_enhanced_projections(impulse)
                
                # پیش بینی موج بعدی
                self._predict_next_wave(impulse)
                
                impulses.append(impulse)
                
            except Exception:
                continue
        
        return impulses
    
    def _check_enhanced_alternation(self, pivots: List[Tuple]) -> bool:
        """بررسی پیشرفته الترناسیون"""
        try:
            if len(pivots) < 3:
                return False
                
            # بررسی الترناسیون ساده
            for i in range(len(pivots) - 1):
                current_type = pivots[i][2] if len(pivots[i]) > 2 else None
                next_type = pivots[i + 1][2] if len(pivots[i + 1]) > 2 else None
                
                if current_type and next_type and current_type == next_type:
                    return False
            
            # بررسی کیفیت روند
            prices = [p[1] for p in pivots]
            overall_trend = prices[-1] - prices[0]
            price_std = np.std(prices)
            
            # روند باید معنی دار باشد
            if abs(overall_trend) < price_std * 0.3:
                return False
            
            # بررسی نوسانات معقول
            price_ranges = []
            for i in range(len(pivots) - 1):
                price_range = abs(pivots[i+1][1] - pivots[i][1])
                price_ranges.append(price_range)
                
            if len(price_ranges) > 1:
                range_ratio = max(price_ranges) / (min(price_ranges) + 1e-10)
                if range_ratio > 8:  # نوسانات غیرمعقول
                    return False
            
            # بررسی تناسب زمانی
            time_intervals = []
            for i in range(len(pivots) - 1):
                time_interval = pivots[i+1][0] - pivots[i][0]
                time_intervals.append(time_interval)
            
            if len(time_intervals) > 1:
                time_ratio = max(time_intervals) / (min(time_intervals) + 1e-10)
                if time_ratio > 10:  # اختلاف زمانی غیرمعقول
                    return False
            
            return True
            
        except Exception:
            return False
    
    def _build_enhanced_sub_waves(self, pivots: List[Tuple]) -> List[Dict]:
        """ساخت پیشرفته موج های فرعی"""
        try:
            if len(pivots) < 9:
                return []
            
            waves = []
            
            # تعریف نقاط موج ها
            wave_points = [
                (0, 2),  # موج 1
                (2, 3),  # موج 2  
                (3, 5),  # موج 3
                (5, 6),  # موج 4
                (6, 8)   # موج 5
            ]
            
            for i, (start_idx, end_idx) in enumerate(wave_points):
                if start_idx >= len(pivots) or end_idx >= len(pivots):
                    continue
                    
                start_point = pivots[start_idx]
                end_point = pivots[end_idx]
                
                # محاسبه خصوصیات موج
                wave_length = abs(end_point[1] - start_point[1])
                wave_duration = max(1, end_point[0] - start_point[0])
                is_bullish = end_point[1] > start_point[1]
                
                # تحلیل زیر ساختار
                sub_structure = self._analyze_sub_structure(start_point[0], end_point[0])
                
                # محاسبه شخصیت موج
                personality = self._calculate_wave_personality(i + 1, start_point, end_point)
                
                # محاسبه سرعت و شتاب
                velocity = self._calculate_wave_velocity(start_point[0], end_point[0])
                acceleration = self._calculate_wave_acceleration(start_point[0], end_point[0])
                
                wave = {
                    'number': i + 1,
                    'start': start_point,
                    'end': end_point,
                    'start_index': start_point[0],
                    'end_index': end_point[0],
                    'start_price': start_point[1],
                    'end_price': end_point[1],
                    'length': wave_length,
                    'duration': wave_duration,
                    'is_bullish': is_bullish,
                    'sub_structure': sub_structure,
                    'personality': personality,
                    'slope': wave_length / wave_duration,
                    'velocity': velocity,
                    'acceleration': acceleration,
                    'intensity': self._calculate_wave_intensity(start_point[0], end_point[0])
                }
                
                waves.append(wave)
            
            return waves
            
        except Exception:
            return []
    
    def _analyze_sub_structure(self, start_idx: int, end_idx: int) -> Dict:
        """تحلیل زیر ساختار موج"""
        try:
            start_idx = max(0, min(start_idx, len(self.data) - 1))
            end_idx = max(start_idx, min(end_idx, len(self.data) - 1))
            
            wave_data = self.data.iloc[start_idx:end_idx+1]
            
            if len(wave_data) < 3:
                return {'complexity': 'simple', 'sub_waves': 0, 'internal_retracements': []}
            
            # شناسایی زیر پیوت ها
            sub_pivots = self._find_minor_pivots(wave_data, start_idx)
            
            complexity = 'simple'
            if len(sub_pivots) >= 5:
                complexity = 'complex'
            elif len(sub_pivots) >= 3:
                complexity = 'moderate'
            
            # محاسبه اصلاحات داخلی
            internal_retracements = self._calculate_internal_retracements(wave_data)
            
            return {
                'complexity': complexity,
                'sub_waves': len(sub_pivots),
                'internal_retracements': internal_retracements,
                'volatility': float(wave_data['close'].std() / wave_data['close'].mean()) if len(wave_data) > 1 else 0.0
            }
            
        except Exception:
            return {'complexity': 'simple', 'sub_waves': 0, 'internal_retracements': []}
    
    def _find_minor_pivots(self, wave_data: pd.DataFrame, offset: int = 0) -> List[Tuple]:
        """یافتن پیوت های کوچک درون موج"""
        try:
            pivots = []
            window = max(2, len(wave_data) // 6)
            
            closes = wave_data['close'].values
            
            for i in range(window, len(wave_data) - window):
                price = closes[i]
                
                # بررسی قله
                is_peak = all(price >= closes[i-j] for j in range(1, window+1)) and \
                         all(price >= closes[i+j] for j in range(1, window+1))
                
                # بررسی دره
                is_valley = all(price <= closes[i-j] for j in range(1, window+1)) and \
                           all(price <= closes[i+j] for j in range(1, window+1))
                
                if is_peak:
                    pivots.append((offset + i, price, 'HIGH'))
                elif is_valley:
                    pivots.append((offset + i, price, 'LOW'))
            
            return pivots
            
        except Exception:
            return []
    
    def _calculate_internal_retracements(self, wave_data: pd.DataFrame) -> List[float]:
        """محاسبه اصلاحات داخلی موج"""
        try:
            retracements = []
            prices = wave_data['close'].values
            
            if len(prices) < 3:
                return retracements
            
            start_price = prices[0]
            end_price = prices[-1]
            wave_range = abs(end_price - start_price)
            
            if wave_range == 0:
                return retracements
            
            # یافتن نقاط برگشت داخلی
            for i in range(1, len(prices) - 1):
                price = prices[i]
                
                if start_price < end_price:  # موج صعودی
                    if price < start_price:
                        retracement = (start_price - price) / wave_range
                        retracements.append(retracement)
                else:  # موج نزولی
                    if price > start_price:
                        retracement = (price - start_price) / wave_range
                        retracements.append(retracement)
            
            return retracements[:5]  # حداکثر 5 اصلاح
            
        except Exception:
            return []
    
    def _calculate_wave_personality(self, wave_number: int, start_point: Tuple, end_point: Tuple) -> Dict:
        """محاسبه شخصیت موج براساس نظریه نئوویو"""
        try:
            personality = {
                'energy': 0.5,
                'momentum_character': 'neutral',
                'fibonacci_harmony': 0.0
            }
            
            # شخصیت براساس شماره موج
            wave_personalities = {
                1: {'energy': 0.7, 'momentum_character': 'initiating'},
                2: {'energy': 0.3, 'momentum_character': 'corrective'},
                3: {'energy': 1.0, 'momentum_character': 'dynamic'},
                4: {'energy': 0.4, 'momentum_character': 'corrective'},
                5: {'energy': 0.6, 'momentum_character': 'exhaustive'}
            }
            
            if wave_number in wave_personalities:
                personality.update(wave_personalities[wave_number])
            
            # تحلیل شدت حرکت
            try:
                start_idx = max(0, min(start_point[0], len(self.data) - 1))
                end_idx = max(start_idx, min(end_point[0], len(self.data) - 1))
                
                wave_data = self.data.iloc[start_idx:end_idx+1]
                if len(wave_data) > 1:
                    volatility = wave_data['close'].std()
                    personality['volatility'] = float(volatility) if not np.isnan(volatility) else 0.0
                    
                    if 'volume' in wave_data.columns:
                        volume_intensity = wave_data['volume'].mean()
                        personality['volume_intensity'] = float(volume_intensity) if not np.isnan(volume_intensity) else 1.0
            except Exception:
                pass
            
            return personality
            
        except Exception:
            return {'energy': 0.5, 'momentum_character': 'neutral'}
    
    def _calculate_wave_velocity(self, start_idx: int, end_idx: int) -> float:
        """محاسبه سرعت موج"""
        try:
            start_idx = max(0, min(start_idx, len(self.data) - 1))
            end_idx = max(start_idx, min(end_idx, len(self.data) - 1))
            
            wave_data = self.data.iloc[start_idx:end_idx+1]
            
            if len(wave_data) < 2:
                return 0.0
            
            total_distance = 0.0
            for i in range(1, len(wave_data)):
                price_change = abs(wave_data['close'].iloc[i] - wave_data['close'].iloc[i-1])
                total_distance += price_change
            
            time_duration = max(1, len(wave_data) - 1)
            velocity = total_distance / time_duration
            
            return velocity
            
        except Exception:
            return 0.0
    
    def _calculate_wave_acceleration(self, start_idx: int, end_idx: int) -> float:
        """محاسبه شتاب موج"""
        try:
            start_idx = max(0, min(start_idx, len(self.data) - 1))
            end_idx = max(start_idx, min(end_idx, len(self.data) - 1))
            
            wave_data = self.data.iloc[start_idx:end_idx+1]
            
            if len(wave_data) < 3:
                return 0.0
            
            # محاسبه تغییرات سرعت
            velocities = []
            for i in range(1, len(wave_data)):
                price_change = wave_data['close'].iloc[i] - wave_data['close'].iloc[i-1]
                velocities.append(abs(price_change))
            
            if len(velocities) < 2:
                return 0.0
            
            # محاسبه تغییرات در سرعت (شتاب)
            accelerations = []
            for i in range(1, len(velocities)):
                acc = velocities[i] - velocities[i-1]
                accelerations.append(acc)
            
            return np.mean(accelerations) if accelerations else 0.0
            
        except Exception:
            return 0.0
    
    def _calculate_wave_intensity(self, start_idx: int, end_idx: int) -> float:
        """محاسبه شدت موج"""
        try:
            start_idx = max(0, min(start_idx, len(self.data) - 1))
            end_idx = max(start_idx, min(end_idx, len(self.data) - 1))
            
            wave_data = self.data.iloc[start_idx:end_idx+1]
            
            if len(wave_data) < 2:
                return 0.0
            
            # ترکیب عوامل مختلف برای شدت
            price_intensity = wave_data['close'].std() / wave_data['close'].mean()
            
            volume_intensity = 1.0
            if 'volume' in wave_data.columns and len(wave_data) > 1:
                volume_intensity = wave_data['volume'].std() / (wave_data['volume'].mean() + 1e-10)
            
            # اگر ATR موجود باشد
            atr_intensity = 1.0
            if 'atr' in wave_data.columns and len(wave_data) > 1:
                atr_intensity = wave_data['atr'].mean() / (wave_data['close'].mean() + 1e-10)
            
            # ترکیب وزن دار
            intensity = (price_intensity * 0.5 + volume_intensity * 0.3 + atr_intensity * 0.2)
            
            return float(intensity) if not np.isnan(intensity) else 0.5
            
        except Exception:
            return 0.5
    
    def _determine_enhanced_impulse_type(self, waves: List[Dict]) -> ImpulseType:
        """تعیین پیشرفته نوع الگوی شتابدار"""
        try:
            if len(waves) != 5:
                return ImpulseType.SIMPLE_TRENDING
                
            # محاسبه طول های امواج محرک
            impulse_lengths = {
                1: waves[0]['length'],
                3: waves[2]['length'], 
                5: waves[4]['length']
            }
            
            # محاسبه میانگین و انحراف معیار
            lengths = list(impulse_lengths.values())
            avg_length = np.mean(lengths)
            std_length = np.std(lengths)
            
            # تشخیص امتدادها با آستانه دقیق تر
            extended_waves = []
            extension_threshold = avg_length + std_length * 0.5
            
            for wave_num, length in impulse_lengths.items():
                if length > extension_threshold and length > avg_length * 1.5:
                    extended_waves.append(wave_num)
            
            # تعیین نوع براساس امتدادها
            if len(extended_waves) == 0:
                return ImpulseType.SIMPLE_TRENDING
            elif len(extended_waves) == 1:
                if 1 in extended_waves:
                    return ImpulseType.EXTENDED_1
                elif 3 in extended_waves:
                    return ImpulseType.EXTENDED_3
                elif 5 in extended_waves:
                    return ImpulseType.EXTENDED_5
            elif len(extended_waves) >= 2:
                return ImpulseType.DOUBLE_EXTENDED
            
            # بررسی Truncation با دقت بیشتر
            wave3_end = waves[2]['end_price']
            wave5_end = waves[4]['end_price']
            
            if waves[0]['is_bullish']:  # موج صعودی
                if wave5_end < wave3_end * 0.98:  # 2% تلرانس
                    return ImpulseType.TRUNCATED_5
            else:  # موج نزولی
                if wave5_end > wave3_end * 1.02:  # 2% تلرانس
                    return ImpulseType.TRUNCATED_5
            
            # بررسی الگوهای قطری
            if self._check_diagonal_pattern(waves):
                if self._is_leading_diagonal(waves):
                    return ImpulseType.LEADING_DIAGONAL
                else:
                    return ImpulseType.ENDING_DIAGONAL
            
            # بررسی پیچیدگی
            complexity_scores = [w.get('sub_structure', {}).get('complexity', 'simple') for w in waves]
            if complexity_scores.count('complex') >= 2:
                return ImpulseType.COMPLEX_IMPULSE
            
            return ImpulseType.SIMPLE_TRENDING
            
        except Exception:
            return ImpulseType.SIMPLE_TRENDING
    
    def _check_diagonal_pattern(self, waves: List[Dict]) -> bool:
        """بررسی الگوی قطری"""
        try:
            # بررسی همپوشانی موج 4 با موج 1
            wave1_start = waves[0]['start_price']
            wave1_end = waves[0]['end_price']
            wave4_end = waves[3]['end_price']
            
            overlap_detected = False
            if waves[0]['is_bullish']:
                overlap_detected = wave4_end <= wave1_end
            else:
                overlap_detected = wave4_end >= wave1_end
            
            if not overlap_detected:
                return False
            
            # بررسی کاهش تدریجی یا افزایش حجم امواج
            impulse_lengths = [waves[0]['length'], waves[2]['length'], waves[4]['length']]
            
            # الگوی کاهشی (Ending Diagonal)
            decreasing_trend = (impulse_lengths[0] >= impulse_lengths[1] >= impulse_lengths[2])
            
            # الگوی افزایشی (Leading Diagonal)
            increasing_trend = (impulse_lengths[0] <= impulse_lengths[1] <= impulse_lengths[2])
            
            return decreasing_trend or increasing_trend
            
        except Exception:
            return False
    
    def _is_leading_diagonal(self, waves: List[Dict]) -> bool:
        """تشخیص قطری پیشرو"""
        try:
            # قطری پیشرو معمولاً الگوی افزایشی دارد
            impulse_lengths = [waves[0]['length'], waves[2]['length'], waves[4]['length']]
            increasing_trend = (impulse_lengths[0] <= impulse_lengths[1] <= impulse_lengths[2])
            
            # بررسی ساختار امواج اصلاحی (معمولاً ساده تر)
            corrective_complexities = [
                waves[1].get('sub_structure', {}).get('complexity', 'simple'),
                waves[3].get('sub_structure', {}).get('complexity', 'simple')
            ]
            
            simple_corrections = corrective_complexities.count('simple')
            
            return increasing_trend and simple_corrections >= 1
            
        except Exception:
            return False
    
    def _determine_wave_direction(self, waves: List[Dict]) -> str:
        """تعیین جهت کلی موج"""
        try:
            start_price = waves[0]['start_price']
            end_price = waves[-1]['end_price']
            
            price_change = end_price - start_price
            price_change_percent = abs(price_change) / start_price
            
            if price_change_percent < 0.015:  # کمتر از 1.5% تغییر
                return "SIDEWAYS"
            elif price_change > 0:
                return "UP"
            else:
                return "DOWN"
                
        except Exception:
            return "UP"
    
    def _validate_impulse_comprehensive(self, impulse: ImpulseWave):
        """اعتبارسنجی جامع موج شتابدار"""
        try:
            waves = impulse.waves
            errors = []
            warnings = []
            
            # قوانین کاردینال (حیاتی)
            self._validate_cardinal_rules(waves, errors, warnings, impulse)
            
            # قوانین نئوویو
            self._validate_neowave_rules(waves, errors, warnings)
            
            # قوانین زمانی
            self._validate_time_rules(waves, errors, warnings)
            
            # قوانین حجمی
            self._validate_volume_rules(waves, errors, warnings)
            
            # قوانین فیبوناچی
            self._validate_fibonacci_rules(waves, errors, warnings)
            
            # قوانین تناسب
            self._validate_proportion_rules(waves, errors, warnings)
            
            impulse.validation_errors = errors
            impulse.validation_warnings = warnings
            impulse.is_valid = len(errors) == 0
            
        except Exception:
            impulse.is_valid = False
            impulse.validation_errors = ["خطا در اعتبارسنجی"]
    
    def _validate_cardinal_rules(self, waves: List[Dict], errors: List[str], warnings: List[str], impulse: ImpulseWave):
        """اعتبارسنجی قوانین کاردینال"""
        try:
            # قانون 1: موج 2 نباید بیش از 100% موج 1 را اصلاح کند
            if len(waves) >= 2:
                wave2_retracement = waves[1]['length'] / waves[0]['length']
                tolerance = self.IMPULSE_RULES['cardinal_rule_1']['tolerance']
                
                if wave2_retracement >= (1.0 + tolerance):
                    errors.append("موج 2 بیش از 100% موج 1 را اصلاح کرده")
                elif wave2_retracement > 0.95:
                    warnings.append("موج 2 تقریباً 100% موج 1 را اصلاح کرده")
            
            # قانون 2: موج 3 نباید کوتاه ترین موج محرک باشد
            if len(waves) >= 5:
                impulse_lengths = [waves[0]['length'], waves[2]['length'], waves[4]['length']]
                if waves[2]['length'] <= min(impulse_lengths):
                    errors.append("موج 3 کوتاه ترین یا برابر کوتاه ترین موج محرک است")
            
            # قانون 3: موج 4 نباید وارد قلمرو موج 1 شود
            if len(waves) >= 4:
                overlap_detected = self._check_wave4_overlap(waves)
                if overlap_detected:
                    if impulse.wave_type not in [ImpulseType.LEADING_DIAGONAL, ImpulseType.ENDING_DIAGONAL]:
                        errors.append("موج 4 وارد قلمرو موج 1 شده")
                    else:
                        warnings.append("همپوشانی موج 4 با موج 1 در الگوی قطری مجاز است")
                        
        except Exception:
            pass
    
    def _check_wave4_overlap(self, waves: List[Dict]) -> bool:
        """بررسی همپوشانی موج 4 با موج 1"""
        try:
            wave1_end = waves[0]['end_price']
            wave4_end = waves[3]['end_price']
            
            if waves[0]['is_bullish']:
                # در موج صعودی، موج 4 نباید زیر انتهای موج 1 برود
                return wave4_end <= wave1_end
            else:
                # در موج نزولی، موج 4 نباید بالای انتهای موج 1 برود
                return wave4_end >= wave1_end
                
        except Exception:
            return False
    
    def _validate_neowave_rules(self, waves: List[Dict], errors: List[str], warnings: List[str]):
        """اعتبارسنجی قوانین نئوویو"""
        try:
            if len(waves) < 3:
                return
                
            # قانون اصلاح حداقل موج 2
            wave2_retracement = waves[1]['length'] / waves[0]['length']
            if wave2_retracement < 0.382:
                warnings.append("موج 2 کمتر از 38.2% موج 1 را اصلاح کرده (نئوویو)")
            
            # قانون حداقل موج 3
            if len(waves) >= 3:
                wave3_extension = waves[2]['length'] / waves[0]['length']
                if wave3_extension < 1.0:
                    errors.append("موج 3 کوتاهتر از موج 1 است")
                elif wave3_extension < 1.618:
                    warnings.append("موج 3 کمتر از 161.8% موج 1 است (نئوویو)")
            
            # بررسی تناسب های فیبوناچی
            self._check_fibonacci_proportions(waves, warnings)
            
        except Exception:
            pass
    
    def _validate_time_rules(self, waves: List[Dict], errors: List[str], warnings: List[str]):
        """اعتبارسنجی قوانین زمانی"""
        try:
            if len(waves) < 2:
                return
                
            # قانون زمان موج 2
            if waves[1]['duration'] > 0 and waves[0]['duration'] > 0:
                time_ratio = waves[1]['duration'] / waves[0]['duration']
                if time_ratio < 0.33:
                    warnings.append("موج 2 زمان کافی ندارد (کمتر از 1/3 موج 1)")
                elif time_ratio > 5.0:
                    warnings.append("موج 2 زمان زیادی گرفته است")
            
            # بررسی تعادل زمانی کلی
            if len(waves) >= 5:
                impulse_durations = [waves[0]['duration'], waves[2]['duration'], waves[4]['duration']]
                corrective_durations = [waves[1]['duration'], waves[3]['duration']]
                
                total_impulse_time = sum(impulse_durations)
                total_corrective_time = sum(corrective_durations)
                
                if total_corrective_time > 0:
                    time_balance = total_impulse_time / total_corrective_time
                    if time_balance < 0.4:
                        warnings.append("امواج اصلاحی زمان نسبتاً زیادی گرفته اند")
                    elif time_balance > 8.0:
                        warnings.append("امواج محرک خیلی سریع هستند")
                        
        except Exception:
            pass
    
    def _validate_volume_rules(self, waves: List[Dict], errors: List[str], warnings: List[str]):
        """اعتبارسنجی قوانین حجمی"""
        try:
            if 'volume' not in self.data.columns or len(waves) < 3:
                return
            
            # بررسی حجم موج 3 (باید معمولاً بالاترین باشد)
            wave_volumes = []
            for wave in waves:
                start_idx = max(0, min(wave['start_index'], len(self.data) - 1))
                end_idx = max(start_idx, min(wave['end_index'], len(self.data) - 1))
                
                if start_idx < len(self.data) and end_idx < len(self.data):
                    avg_volume = self.data['volume'].iloc[start_idx:end_idx+1].mean()
                    wave_volumes.append(avg_volume)
                else:
                    wave_volumes.append(0.0)
            
            if len(wave_volumes) >= 3:
                wave3_volume = wave_volumes[2]
                max_volume = max(wave_volumes)
                avg_volume = np.mean(wave_volumes)
                
                if wave3_volume < max_volume * 0.7:
                    warnings.append("حجم موج 3 نسبتاً پایین است")
                    
                if wave3_volume < avg_volume:
                    warnings.append("حجم موج 3 زیر میانگین است")
                    
        except Exception:
            pass
    
    def _validate_fibonacci_rules(self, waves: List[Dict], errors: List[str], warnings: List[str]):
        """اعتبارسنجی قوانین فیبوناچی"""
        try:
            if len(waves) < 3:
                return
                
            wave_lengths = [w['length'] for w in waves[:5]]
            
            # نسبت موج 3 به موج 1
            if len(wave_lengths) >= 3:
                ratio_3_to_1 = wave_lengths[2] / (wave_lengths[0] + 1e-10)
                expected_ratios = [1.0, 1.618, 2.618]
                
                min_deviation = min(abs(ratio_3_to_1 - ratio) / ratio for ratio in expected_ratios)
                if min_deviation > 0.4:
                    warnings.append(f"نسبت موج 3 به 1 ({ratio_3_to_1:.2f}) از نسبت های فیبوناچی فاصله دارد")
            
            # نسبت موج 5 به موج 1
            if len(wave_lengths) >= 5:
                ratio_5_to_1 = wave_lengths[4] / (wave_lengths[0] + 1e-10)
                common_ratios = [0.618, 1.0, 1.618]
                
                min_deviation = min(abs(ratio_5_to_1 - ratio) / ratio for ratio in common_ratios)
                if min_deviation > 0.4:
                    warnings.append(f"نسبت موج 5 به 1 ({ratio_5_to_1:.2f}) غیر متعارف است")
                    
        except Exception:
            pass
    
    def _validate_proportion_rules(self, waves: List[Dict], errors: List[str], warnings: List[str]):
        """اعتبارسنجی قوانین تناسب"""
        try:
            if len(waves) < 5:
                return
                
            # بررسی الترناسیون بین امواج 2 و 4
            wave2_complexity = waves[1].get('sub_structure', {}).get('complexity', 'simple')
            wave4_complexity = waves[3].get('sub_structure', {}).get('complexity', 'simple')
            
            if wave2_complexity == wave4_complexity and wave2_complexity != 'simple':
                warnings.append("موج های 2 و 4 پیچیدگی مشابه دارند (کمبود الترناسیون)")
            
            # بررسی تناسب طولی امواج اصلاحی
            wave2_length = waves[1]['length']
            wave4_length = waves[3]['length']
            
            if wave2_length > 0 and wave4_length > 0:
                length_ratio = max(wave2_length, wave4_length) / min(wave2_length, wave4_length)
                if length_ratio > 5.0:
                    warnings.append("اختلاف زیاد در طول امواج اصلاحی 2 و 4")
            
            # بررسی تناسب زمانی
            wave2_duration = waves[1]['duration']
            wave4_duration = waves[3]['duration']
            
            if wave2_duration > 0 and wave4_duration > 0:
                time_ratio = max(wave2_duration, wave4_duration) / min(wave2_duration, wave4_duration)
                if time_ratio > 4.0:
                    warnings.append("اختلاف زیاد در مدت زمان امواج اصلاحی 2 و 4")
                    
        except Exception:
            pass
    
    def _check_fibonacci_proportions(self, waves: List[Dict], warnings: List[str]):
        """بررسی تناسب های فیبوناچی"""
        try:
            relationships = self.fibonacci_analyzer.find_fibonacci_relationships(waves)
            
            for relationship, ratio in relationships.items():
                if 'time_' in relationship:
                    continue  # روابط زمانی را جداگانه بررسی می کنیم
                    
                # یافتن نزدیک ترین نسبت فیبوناچی
                all_ratios = []
                for ratio_set in self.fibonacci_analyzer.FIBONACCI_RATIOS.values():
                    all_ratios.extend(ratio_set)
                
                deviations = [abs(ratio - fib_ratio) / fib_ratio for fib_ratio in all_ratios]
                min_deviation = min(deviations)
                
                if min_deviation > 0.3:  # انحراف بیش از 30%
                    closest_ratio = all_ratios[deviations.index(min_deviation)]
                    warnings.append(f"نسبت {relationship} ({ratio:.2f}) از فیبوناچی ({closest_ratio:.2f}) فاصله دارد")
                    
        except Exception:
            pass
    
    def _calculate_enhanced_metrics(self, impulse: ImpulseWave):
        """محاسبه متریک های پیشرفته"""
        try:
            metrics = impulse.metrics
            waves = impulse.waves
            
            # دقت فیبوناچی
            fib_accuracies = []
            for i, wave in enumerate(waves):
                if i > 0:
                    accuracy = self.fibonacci_analyzer.calculate_fibonacci_accuracy(wave, waves[i-1])
                    fib_accuracies.append(accuracy)
            
            metrics.fibonacci_accuracy = np.mean(fib_accuracies) if fib_accuracies else 0.0
            
            # روابط فیبوناچی
            metrics.fibonacci_extensions = self.fibonacci_analyzer.find_fibonacci_relationships(waves)
            
            # تأیید حجم
            metrics.volume_confirmation = self.volume_analyzer.analyze_volume_confirmation(
                self.data, impulse.start_index, impulse.end_index, impulse.direction
            )
            
            # تأیید مومنتوم
            metrics.momentum_confirmation = self.momentum_analyzer.calculate_momentum_confirmation(
                self.data, impulse.start_index, impulse.end_index, impulse.direction
            )
            
            # کیفیت کانال بندی
            metrics.channeling_quality = self._calculate_enhanced_channeling_quality(waves)
            
            # بعد فرکتال
            metrics.fractal_dimension = self._calculate_fractal_dimension(impulse)
            
            # نمای هرست
            metrics.hurst_exponent = self._calculate_hurst_exponent(impulse)
            
            # قدرت پیش بینی
            metrics.predictive_power = self._calculate_predictive_power(waves)
            
            # یکپارچگی ساختاری
            metrics.structural_integrity = self._calculate_structural_integrity(waves)
            
            # شخصیت موج
            for i, wave in enumerate(waves):
                personality = wave.get('personality', {})
                metrics.wave_personality[f'wave_{i+1}'] = personality.get('energy', 0.5)
            
            # امتیاز الترناسیون
            metrics.alternation_score = self._calculate_alternation_score(waves)
            
            # شاخص پیچیدگی
            metrics.complexity_index = self._calculate_complexity_index(waves)
            
            # امتیاز بافت بازار
            metrics.market_context_score = self._calculate_market_context(impulse)
            
        except Exception:
            pass
    
    def _calculate_enhanced_channeling_quality(self, waves: List[Dict]) -> float:
        """محاسبه کیفیت کانال بندی پیشرفته"""
        try:
            if len(waves) < 5:
                return 0.0
            
            # نقاط برای رسم کانال (0-2)
            wave_0_start = waves[0]['start']
            wave_2_end = waves[2]['end']
            
            # محاسبه شیب خط پایه
            time_diff = wave_2_end[0] - wave_0_start[0]
            if time_diff == 0:
                return 0.0
                
            base_slope = (wave_2_end[1] - wave_0_start[1]) / time_diff
            
            # بررسی قرارگیری موج های 1، 3، 5 روی خطوط موازی
            deviations = []
            
            for wave_idx in [0, 2, 4]:  # موج های 1، 3، 5
                if wave_idx >= len(waves):
                    continue
                    
                wave_end = waves[wave_idx]['end']
                expected_price = wave_0_start[1] + base_slope * (wave_end[0] - wave_0_start[0])
                actual_price = wave_end[1]
                
                deviation = abs(actual_price - expected_price)
                deviations.append(deviation)
            
            if not deviations:
                return 0.0
            
            # نرمال سازی انحرافات
            price_range = max(w['end'][1] for w in waves) - min(w['start'][1] for w in waves)
            if price_range == 0:
                return 0.0
            
            normalized_deviations = [dev / price_range for dev in deviations]
            avg_deviation = np.mean(normalized_deviations)
            
            # محاسبه کیفیت (کمتر انحراف = بهتر کیفیت)
            quality = max(0.0, 1.0 - avg_deviation * 2)  # ضریب 2 برای حساسیت بیشتر
            
            return min(quality, 1.0)
            
        except Exception:
            return 0.0
    
    def _calculate_fractal_dimension(self, impulse: ImpulseWave) -> float:
        """محاسبه بعد فرکتال"""
        try:
            start_idx = max(0, min(impulse.start_index, len(self.data) - 1))
            end_idx = max(start_idx, min(impulse.end_index, len(self.data) - 1))
            
            price_data = self.data['close'].iloc[start_idx:end_idx+1].values
            
            if len(price_data) < 10:
                return 1.5
            
            # روش Higuchi برای محاسبه بعد فرکتال
            k_max = min(10, len(price_data) // 3)
            lk_values = []
            k_values = []
            
            for k in range(1, k_max + 1):
                lk = 0
                normalization_factor = (len(price_data) - 1) / (k * k)
                
                for m in range(k):
                    lm = 0
                    max_i = int((len(price_data) - m - 1) / k)
                    
                    for i in range(1, max_i + 1):
                        if m + i * k < len(price_data):
                            lm += abs(price_data[m + i * k] - price_data[m + (i - 1) * k])
                    
                    if max_i > 0:
                        lm = lm * normalization_factor / max_i
                        lk += lm
                
                if k > 0:
                    lk = lk / k
                    if lk > 0:
                        lk_values.append(np.log(lk))
                        k_values.append(np.log(k))
            
            if len(lk_values) > 3:
                # محاسبه شیب برای بعد فرکتال
                slope = np.polyfit(k_values, lk_values, 1)[0]
                fractal_dimension = -slope
                return max(1.0, min(2.0, fractal_dimension))
            
            return 1.5
            
        except Exception:
            return 1.5
    
    def _calculate_hurst_exponent(self, impulse: ImpulseWave) -> float:
        """محاسبه نمای هرست"""
        try:
            start_idx = max(0, min(impulse.start_index, len(self.data) - 1))
            end_idx = max(start_idx, min(impulse.end_index, len(self.data) - 1))
            
            price_data = self.data['close'].iloc[start_idx:end_idx+1].values
            
            if len(price_data) < 20:
                return 0.5
            
            # محاسبه بازدهی ها
            log_returns = np.diff(np.log(price_data + 1e-10))
            
            # روش R/S Analysis
            lags = range(2, min(len(log_returns) // 4, 20))
            rs_values = []
            lag_values = []
            
            for lag in lags:
                # تقسیم به زیر دوره ها
                n_periods = len(log_returns) // lag
                rs_period = []
                
                for i in range(n_periods):
                    period_returns = log_returns[i*lag:(i+1)*lag]
                    
                    if len(period_returns) > 1:
                        mean_return = np.mean(period_returns)
                        deviations = period_returns - mean_return
                        cumulative_deviations = np.cumsum(deviations)
                        
                        R = np.max(cumulative_deviations) - np.min(cumulative_deviations)
                        S = np.std(period_returns)
                        
                        if S > 1e-10:
                            rs_period.append(R / S)
                
                if rs_period:
                    avg_rs = np.mean(rs_period)
                    if avg_rs > 0:
                        rs_values.append(np.log(avg_rs))
                        lag_values.append(np.log(lag))
            
            # محاسبه نمای هرست
            if len(rs_values) > 3:
                hurst = np.polyfit(lag_values, rs_values, 1)[0]
                return max(0.0, min(1.0, hurst))
            
            return 0.5
            
        except Exception:
            return 0.5
    
    def _calculate_predictive_power(self, waves: List[Dict]) -> float:
        """محاسبه قدرت پیش بینی"""
        try:
            # عوامل مختلف برای قدرت پیش بینی
            factors = []
            
            # 1. کیفیت تناسب های فیبوناچی
            if len(waves) >= 3:
                fib_quality = 0.0
                relationships = self.fibonacci_analyzer.find_fibonacci_relationships(waves)
                
                for relationship, ratio in relationships.items():
                    if 'time_' not in relationship:
                        # یافتن نزدیک ترین نسبت فیبوناچی
                        all_ratios = [0.618, 1.0, 1.618, 2.618]
                        min_deviation = min(abs(ratio - fib_ratio) / fib_ratio for fib_ratio in all_ratios)
                        accuracy = max(0.0, 1.0 - min_deviation)
                        fib_quality += accuracy
                
                if len(relationships) > 0:
                    factors.append(fib_quality / len(relationships))
            
            # 2. کیفیت ساختاری
            structural_quality = 0.0
            if len(waves) == 5:
                # بررسی قانون موج 3
                impulse_lengths = [waves[0]['length'], waves[2]['length'], waves[4]['length']]
                if waves[2]['length'] > min(impulse_lengths):
                    structural_quality += 0.5
                
                # بررسی الترناسیون
                wave2_complexity = waves[1].get('sub_structure', {}).get('complexity', 'simple')
                wave4_complexity = waves[3].get('sub_structure', {}).get('complexity', 'simple')
                if wave2_complexity != wave4_complexity:
                    structural_quality += 0.5
                    
                factors.append(structural_quality)
            
            # 3. کیفیت جهت گیری
            direction_quality = 0.0
            if len(waves) >= 5:
                impulse_directions = [w['is_bullish'] for w in [waves[0], waves[2], waves[4]]]
                if all(impulse_directions) or not any(impulse_directions):
                    direction_quality = 1.0
                else:
                    direction_quality = 0.3
                    
                factors.append(direction_quality)
            
            return np.mean(factors) if factors else 0.5
            
        except Exception:
            return 0.5
    
    def _calculate_structural_integrity(self, waves: List[Dict]) -> float:
        """محاسبه یکپارچگی ساختاری"""
        try:
            if len(waves) != 5:
                return 0.0
                
            integrity_score = 0.0
            
            # 1. همسویی امواج محرک
            impulse_waves = [waves[0], waves[2], waves[4]]
            impulse_directions = [w['is_bullish'] for w in impulse_waves]
            
            if all(impulse_directions) or not any(impulse_directions):
                integrity_score += 0.3
            
            # 2. تناسب امواج اصلاحی
            corrective_waves = [waves[1], waves[3]]
            corrective_lengths = [w['length'] for w in corrective_waves]
            impulse_lengths = [w['length'] for w in impulse_waves]
            
            avg_impulse = np.mean(impulse_lengths)
            avg_corrective = np.mean(corrective_lengths)
            
            if avg_impulse > 0:
                corrective_ratio = avg_corrective / avg_impulse
                if 0.2 <= corrective_ratio <= 0.9:
                    integrity_score += 0.3
            
            # 3. یکنواختی طولی
            impulse_std = np.std(impulse_lengths)
            impulse_mean = np.mean(impulse_lengths)
            
            if impulse_mean > 0:
                cv = impulse_std / impulse_mean  # ضریب تغییرات
                if cv < 0.5:  # تغییرات کم
                    integrity_score += 0.2
            
            # 4. تناسب زمانی
            total_time = sum(w['duration'] for w in waves)
            if total_time > 0:
                corrective_time = sum(w['duration'] for w in corrective_waves)
                time_balance = corrective_time / total_time
                
                if 0.15 <= time_balance <= 0.5:  # تعادل زمانی معقول
                    integrity_score += 0.2
            
            return min(integrity_score, 1.0)
            
        except Exception:
            return 0.5
    
    def _calculate_alternation_score(self, waves: List[Dict]) -> float:
        """محاسبه امتیاز الترناسیون"""
        try:
            if len(waves) < 4:
                return 0.0
                
            wave2 = waves[1]
            wave4 = waves[3]
            
            score = 0.0
            
            # 1. الترناسیون پیچیدگی
            complexity2 = wave2.get('sub_structure', {}).get('complexity', 'simple')
            complexity4 = wave4.get('sub_structure', {}).get('complexity', 'simple')
            
            if complexity2 != complexity4:
                score += 0.4
            
            # 2. الترناسیون طولی
            length_ratio = wave4['length'] / (wave2['length'] + 1e-10)
            if 0.4 <= length_ratio <= 2.5:
                score += 0.3
            
            # 3. الترناسیون زمانی
            time_ratio = wave4['duration'] / (wave2['duration'] + 1e-10)
            if 0.4 <= time_ratio <= 2.5:
                score += 0.3
            
            return min(score, 1.0)
            
        except Exception:
            return 0.5
    
    def _calculate_complexity_index(self, waves: List[Dict]) -> float:
        """محاسبه شاخص پیچیدگی"""
        try:
            complexity_factors = []
            
            # 1. پیچیدگی زیر ساختار
            for wave in waves:
                sub_structure = wave.get('sub_structure', {})
                complexity = sub_structure.get('complexity', 'simple')
                
                complexity_map = {'simple': 0.0, 'moderate': 0.5, 'complex': 1.0}
                complexity_factors.append(complexity_map.get(complexity, 0.0))
            
            # 2. پیچیدگی نسبت ها
            wave_lengths = [w['length'] for w in waves]
            if len(wave_lengths) > 1:
                length_cv = np.std(wave_lengths) / (np.mean(wave_lengths) + 1e-10)
                complexity_factors.append(min(length_cv, 1.0))
            
            # 3. پیچیدگی زمانی
            wave_durations = [w['duration'] for w in waves]
            if len(wave_durations) > 1:
                duration_cv = np.std(wave_durations) / (np.mean(wave_durations) + 1e-10)
                complexity_factors.append(min(duration_cv, 1.0))
            
            return np.mean(complexity_factors) if complexity_factors else 0.0
            
        except Exception:
            return 0.5
    
    def _calculate_market_context(self, impulse: ImpulseWave) -> float:
        """محاسبه امتیاز بافت بازار"""
        try:
            score = 0.0
            
            # بررسی موقعیت در روند کلی
            lookback = min(100, impulse.start_index)
            if lookback > 10:
                start_idx = max(0, impulse.start_index - lookback)
                end_idx = min(len(self.data), impulse.end_index + 1)
                
                extended_data = self.data.iloc[start_idx:end_idx]
                
                if len(extended_data) > 20:
                    # روند بلندمدت
                    long_trend = (extended_data['close'].iloc[-1] - extended_data['close'].iloc[0]) / extended_data['close'].iloc[0]
                    
                    # جهت موج
                    impulse_direction = (impulse.end_price - impulse.start_price) / impulse.start_price
                    
                    # همسویی با روند
                    if (long_trend > 0 and impulse_direction > 0) or (long_trend < 0 and impulse_direction < 0):
                        score += 0.4
                    
                    # نوسان پذیری متعادل
                    volatility = extended_data['close'].std() / extended_data['close'].mean()
                    if 0.05 <= volatility <= 0.4:
                        score += 0.3
                    
                    # حجم متعادل
                    if 'volume' in extended_data.columns:
                        volume_trend = np.corrcoef(range(len(extended_data)), extended_data['volume'])[0, 1]
                        if not np.isnan(volume_trend) and abs(volume_trend) < 0.7:
                            score += 0.3
            
            return score
            
        except Exception:
            return 0.5
    
    def _calculate_enhanced_confidence_score(self, impulse: ImpulseWave):
        """محاسبه امتیاز اطمینان کلی پیشرفته"""
        try:
            # وزن های بهینه شده
            weights = {
                'validation': 0.30,      # اهمیت بالا به اعتبارسنجی
                'fibonacci_accuracy': 0.20,
                'structural_integrity': 0.15,
                'channeling_quality': 0.10,
                'momentum_confirmation': 0.08,
                'volume_confirmation': 0.07,
                'predictive_power': 0.05,
                'market_context': 0.05
            }
            
            score = 0.0
            
            # امتیاز اعتبارسنجی
            validation_score = 1.0 if impulse.is_valid else 0.0
            if not impulse.is_valid:
                # جریمه براساس تعداد خطاها
                critical_errors = len([e for e in impulse.validation_errors if any(rule['critical'] for rule in self.IMPULSE_RULES.values())])
                warning_count = len(impulse.validation_warnings)
                
                error_penalty = critical_errors * 0.3 + warning_count * 0.1
                validation_score = max(0.0, 0.8 - error_penalty)
            
            score += validation_score * weights['validation']
            
            # متریک های کیفیت
            metrics = impulse.metrics
            score += metrics.fibonacci_accuracy * weights['fibonacci_accuracy']
            score += metrics.structural_integrity * weights['structural_integrity']
            score += metrics.channeling_quality * weights['channeling_quality']
            score += metrics.momentum_confirmation * weights['momentum_confirmation']
            score += metrics.volume_confirmation * weights['volume_confirmation']
            score += metrics.predictive_power * weights['predictive_power']
            score += metrics.market_context_score * weights['market_context']
            
            # بونوس برای الگوهای خاص
            if impulse.wave_type in [ImpulseType.EXTENDED_3, ImpulseType.SIMPLE_TRENDING]:
                score += 0.05  # الگوهای رایج
            elif impulse.wave_type in [ImpulseType.LEADING_DIAGONAL, ImpulseType.ENDING_DIAGONAL]:
                score += 0.03  # الگوهای پیچیده
            
            # تنظیم نهایی
            impulse.confidence_score = min(max(score, 0.0), 1.0)
            
        except Exception:
            impulse.confidence_score = 0.5
    
    def _calculate_enhanced_projections(self, impulse: ImpulseWave):
        """محاسبه پروژکشن های قیمتی و زمانی پیشرفته"""
        try:
            waves = impulse.waves
            projections = {}
            
            if len(waves) < 5:
                return
            
            # پروژکشن های قیمتی براساس فیبوناچی
            wave1_length = waves[0]['length']
            wave3_length = waves[2]['length']
            
            # تعیین الگوی امتدادی
            is_wave3_extended = wave3_length > wave1_length * 1.5
            
            # اهداف موج 5
            wave5_start = waves[4]['start_price']
            
            if impulse.direction == "UP":
                if is_wave3_extended:
                    # موج 3 ممتد - موج 5 معمولاً کوتاهتر
                    projections['wave5_targets'] = {
                        '38.2%': wave5_start + (wave1_length * 0.382),
                        '61.8%': wave5_start + (wave1_length * 0.618),
                        '100%': wave5_start + wave1_length,
                        '123.6%': wave5_start + (wave1_length * 1.236)
                    }
                else:
                    # موج 5 احتمالاً ممتد
                    projections['wave5_targets'] = {
                        '100%': wave5_start + wave1_length,
                        '161.8%': wave5_start + (wave1_length * 1.618),
                        '200%': wave5_start + (wave1_length * 2.0),
                        '261.8%': wave5_start + (wave1_length * 2.618)
                    }
            else:  # جهت نزولی
                if is_wave3_extended:
                    projections['wave5_targets'] = {
                        '38.2%': wave5_start - (wave1_length * 0.382),
                        '61.8%': wave5_start - (wave1_length * 0.618),
                        '100%': wave5_start - wave1_length,
                        '123.6%': wave5_start - (wave1_length * 1.236)
                    }
                else:
                    projections['wave5_targets'] = {
                        '100%': wave5_start - wave1_length,
                        '161.8%': wave5_start - (wave1_length * 1.618),
                        '200%': wave5_start - (wave1_length * 2.0),
                        '261.8%': wave5_start - (wave1_length * 2.618)
                    }
            
            # پروژکشن های زمانی
            wave1_duration = waves[0]['duration']
            current_time = impulse.end_index
            
            projections['time_targets'] = {
                '61.8%': current_time + int(wave1_duration * 0.618),
                '100%': current_time + wave1_duration,
                '161.8%': current_time + int(wave1_duration * 1.618),
                '261.8%': current_time + int(wave1_duration * 2.618)
            }
            
            # سطح باطل سازی
            if impulse.direction == "UP":
                invalidation = min(w['start'][1] for w in waves if w.get('start'))
            else:
                invalidation = max(w['start'][1] for w in waves if w.get('start'))
            
            projections['invalidation_level'] = invalidation
            
            # اهداف موج اصلاحی بعدی
            impulse_range = abs(impulse.end_price - impulse.start_price)
            
            if impulse.direction == "UP":
                projections['correction_targets'] = {
                    '23.6%': impulse.end_price - (impulse_range * 0.236),
                    '38.2%': impulse.end_price - (impulse_range * 0.382),
                    '50%': impulse.end_price - (impulse_range * 0.5),
                    '61.8%': impulse.end_price - (impulse_range * 0.618),
                    '78.6%': impulse.end_price - (impulse_range * 0.786)
                }
            else:
                projections['correction_targets'] = {
                    '23.6%': impulse.end_price + (impulse_range * 0.236),
                    '38.2%': impulse.end_price + (impulse_range * 0.382),
                    '50%': impulse.end_price + (impulse_range * 0.5),
                    '61.8%': impulse.end_price + (impulse_range * 0.618),
                    '78.6%': impulse.end_price + (impulse_range * 0.786)
                }
            
            impulse.projections = projections
            impulse.invalidation_level = invalidation
            
        except Exception:
            impulse.projections = {}
    
    def _predict_next_wave(self, impulse: ImpulseWave):
        """پیش بینی موج بعدی"""
        try:
            # تحلیل موقعیت در چرخه بزرگ تر
            prediction_confidence = 0.6
            
            if impulse.wave_type in [ImpulseType.EXTENDED_5, ImpulseType.TRUNCATED_5]:
                next_prediction = {
                    'type': 'corrective_complex',
                    'direction': 'opposite',
                    'confidence': 0.8,
                    'expected_retracement': '61.8% - 78.6%',
                    'description': 'موج اصلاحی پیچیده مورد انتظار است'
                }
            elif impulse.wave_type == ImpulseType.EXTENDED_3:
                next_prediction = {
                    'type': 'corrective_simple',
                    'direction': 'opposite', 
                    'confidence': 0.75,
                    'expected_retracement': '38.2% - 50%',
                    'description': 'موج اصلاحی ساده تا متوسط'
                }
            elif impulse.wave_type in [ImpulseType.LEADING_DIAGONAL]:
                next_prediction = {
                    'type': 'impulsive_continuation',
                    'direction': 'same',
                    'confidence': 0.7,
                    'expected_retracement': '23.6% - 38.2%',
                    'description': 'ادامه حرکت محرک پس از اصلاح کوتاه'
                }
            else:
                next_prediction = {
                    'type': 'corrective_moderate',
                    'direction': 'opposite',
                    'confidence': prediction_confidence,
                    'expected_retracement': '50% - 61.8%',
                    'description': 'موج اصلاحی متوسط'
                }
            
            # محاسبه اهداف احتمالی
            if impulse.projections and 'correction_targets' in impulse.projections:
                correction_targets = impulse.projections['correction_targets']
                retracement_level = next_prediction['expected_retracement']
                
                if '38.2%' in retracement_level:
                    next_prediction['target_range'] = [
                        correction_targets.get('23.6%', impulse.end_price),
                        correction_targets.get('50%', impulse.end_price)
                    ]
                elif '61.8%' in retracement_level:
                    next_prediction['target_range'] = [
                        correction_targets.get('50%', impulse.end_price),
                        correction_targets.get('78.6%', impulse.end_price)
                    ]
                else:
                    next_prediction['target_range'] = [
                        correction_targets.get('38.2%', impulse.end_price),
                        correction_targets.get('61.8%', impulse.end_price)
                    ]
            
            impulse.next_wave_prediction = next_prediction
            
        except Exception:
            impulse.next_wave_prediction = {}
    
    def _remove_duplicate_impulses(self, impulses: List[ImpulseWave]) -> List[ImpulseWave]:
        """حذف امواج تکراری با الگوریتم بهبود یافته"""
        try:
            if len(impulses) <= 1:
                return impulses
            
            unique_impulses = []
            overlap_threshold = 0.6  # آستانه همپوشانی 60%
            
            # مرتب سازی براساس اطمینان (بالاترین اول)
            sorted_impulses = sorted(impulses, key=lambda x: x.confidence_score, reverse=True)
            
            for impulse in sorted_impulses:
                is_duplicate = False
                
                for existing in unique_impulses:
                    # محاسبه همپوشانی
                    overlap_start = max(impulse.start_index, existing.start_index)
                    overlap_end = min(impulse.end_index, existing.end_index)
                    
                    if overlap_start < overlap_end:
                        overlap_length = overlap_end - overlap_start
                        impulse_length = impulse.end_index - impulse.start_index
                        existing_length = existing.end_index - existing.start_index
                        
                        min_length = min(impulse_length, existing_length)
                        max_length = max(impulse_length, existing_length)
                        
                        overlap_ratio = overlap_length / min_length
                        size_ratio = min_length / max_length
                        
                        # بررسی همپوشانی قابل توجه
                        if overlap_ratio > overlap_threshold and size_ratio > 0.5:
                            is_duplicate = True
                            break
                
                if not is_duplicate:
                    unique_impulses.append(impulse)
            
            return unique_impulses
            
        except Exception:
            return impulses
    
    def calculate_wave_projections(self, impulse: ImpulseWave) -> Dict[str, float]:
        """محاسبه پروژکشن های قیمتی موج ها - سازگاری با کد قدیمی"""
        return impulse.projections.get('wave5_targets', {})
    
    def get_impulse_summary(self) -> Dict:
        """خلاصه امواج شتابدار شناسایی شده"""
        try:
            if not self.identified_impulses:
                return {
                    'total_count': 0,
                    'valid_count': 0,
                    'high_confidence_count': 0,
                    'wave_types': {},
                    'average_confidence': 0.0,
                    'best_impulse': None
                }
            
            valid_impulses = [imp for imp in self.identified_impulses if imp.is_valid]
            high_conf_impulses = [imp for imp in self.identified_impulses if imp.confidence_score > 0.8]
            
            wave_types = {}
            for impulse in self.identified_impulses:
                wave_type = impulse.wave_type.value
                wave_types[wave_type] = wave_types.get(wave_type, 0) + 1
            
            avg_confidence = np.mean([imp.confidence_score for imp in self.identified_impulses])
            best_impulse = max(self.identified_impulses, key=lambda x: x.confidence_score)
            
            return {
                'total_count': len(self.identified_impulses),
                'valid_count': len(valid_impulses),
                'high_confidence_count': len(high_conf_impulses),
                'wave_types': wave_types,
                'average_confidence': float(avg_confidence),
                'best_impulse': best_impulse
            }
            
        except Exception:
            return {
                'total_count': 0,
                'valid_count': 0,
                'high_confidence_count': 0,
                'wave_types': {},
                'average_confidence': 0.0,
                'best_impulse': None
            }