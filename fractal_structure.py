"""
ساختار فراکتال پیشرفته - نسخه حرفه‌ای کامل
Advanced Fractal Structure Analysis for NEOWave
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Optional, Dict, Union, Any
from scipy.signal import find_peaks, savgol_filter, hilbert, argrelextrema
from scipy.stats import linregress, pearsonr, spearmanr
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from enum import Enum
import warnings
import logging
from collections import deque
import json

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FractalType(Enum):
    """انواع فراکتال‌ها"""
    WILLIAMS_UP = "Williams Up Fractal"
    WILLIAMS_DOWN = "Williams Down Fractal"
    CHAOS_BULLISH = "Chaos Bullish Fractal"
    CHAOS_BEARISH = "Chaos Bearish Fractal"
    ADVANCED_PEAK = "Advanced Peak Fractal"
    ADVANCED_TROUGH = "Advanced Trough Fractal"
    MULTI_SCALE_UP = "Multi-Scale Up Fractal"
    MULTI_SCALE_DOWN = "Multi-Scale Down Fractal"
    NEOWAVE_PIVOT = "NEOWave Pivot Fractal"

class FractalStrength(Enum):
    """قدرت فراکتال"""
    VERY_WEAK = 1
    WEAK = 2
    MODERATE = 3
    STRONG = 4
    VERY_STRONG = 5
    EXTREME = 6

@dataclass
class FractalPoint:
    """نقطه فراکتال با جزئیات کامل"""
    index: int
    timestamp: pd.Timestamp
    price: float
    type: FractalType
    strength: FractalStrength
    confidence: float
    volume_confirmation: bool
    momentum_confirmation: bool
    trend_alignment: bool
    multi_timeframe_confirmation: bool
    dimension: float
    hurst_exponent: float
    dfa_alpha: float
    persistence_score: float
    reversal_probability: float
    target_prices: List[float]
    invalidation_level: float
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FractalCluster:
    """خوشه فراکتال‌ها"""
    fractals: List[FractalPoint]
    center_price: float
    time_span: int
    density: float
    significance: float
    cluster_type: str
    breakout_probability: float

@dataclass
class FractalStructureAnalysis:
    """نتایج تحلیل ساختار فراکتال"""
    fractal_points: List[FractalPoint]
    clusters: List[FractalCluster]
    dimension_profile: Dict[str, float]
    self_similarity_matrix: np.ndarray
    scaling_laws: Dict[str, Any]
    market_regime: str
    trend_strength: float
    chaos_level: float
    predictability_score: float

class AdvancedFractalAnalyzer:
    """تحلیلگر فراکتال فوق پیشرفته"""
    
    def __init__(self, data: pd.DataFrame, config: Optional[Dict] = None):
        """
        مقداردهی اولیه تحلیلگر
        
        Parameters:
        -----------
        data: DataFrame با ستون‌های OHLCV
        config: تنظیمات سفارشی
        """
        self.data = data.copy()
        self.config = config or self._get_default_config()
        
        # ذخیره نتایج
        self.fractal_points = []
        self.dimension_cache = {}
        self.hurst_cache = {}
        
        # محاسبه اندیکاتورهای کمکی
        self._calculate_indicators()
        
        logger.info("🎯 تحلیلگر فراکتال پیشرفته آماده است")
        
    def _get_default_config(self) -> Dict:
        """تنظیمات پیش‌فرض"""
        return {
            'williams_period': 5,
            'chaos_period': 13,
            'min_strength': 0.3,
            'volume_threshold': 1.2,
            'momentum_period': 14,
            'multi_scales': [5, 13, 21, 34, 55],
            'dimension_methods': ['higuchi', 'box_counting', 'katz', 'petrosian'],
            'dfa_scales': range(4, 100),
            'hurst_lags': 100,
            'noise_filter': 'adaptive',
            'cluster_threshold': 0.02,
            'reversal_sensitivity': 0.7
        }
        
    def _calculate_indicators(self):
        """محاسبه اندیکاتورهای کمکی"""
        # میانگین‌های متحرک
        self.data['sma_20'] = self.data['close'].rolling(20).mean()
        self.data['sma_50'] = self.data['close'].rolling(50).mean()
        self.data['ema_12'] = self.data['close'].ewm(span=12).mean()
        self.data['ema_26'] = self.data['close'].ewm(span=26).mean()
        
        # حجم
        self.data['volume_sma'] = self.data['volume'].rolling(20).mean()
        self.data['volume_ratio'] = self.data['volume'] / self.data['volume_sma']
        
        # مومنتوم
        self.data['rsi'] = self._calculate_rsi()
        self.data['momentum'] = self.data['close'].diff(self.config['momentum_period'])
        
        # ATR برای فیلتر نویز
        self.data['atr'] = self._calculate_atr()
        
        # MACD
        self.data['macd'] = self.data['ema_12'] - self.data['ema_26']
        self.data['signal'] = self.data['macd'].ewm(span=9).mean()
        
    def _calculate_rsi(self, period: int = 14) -> pd.Series:
        """محاسبه RSI"""
        delta = self.data['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
        
    def _calculate_atr(self, period: int = 14) -> pd.Series:
        """محاسبه Average True Range"""
        high_low = self.data['high'] - self.data['low']
        high_close = np.abs(self.data['high'] - self.data['close'].shift())
        low_close = np.abs(self.data['low'] - self.data['close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(period).mean()
        return atr
        
    def identify_advanced_fractals(self) -> List[FractalPoint]:
        """
        شناسایی جامع انواع فراکتال‌ها
        """
        logger.info("🔍 شروع شناسایی فراکتال‌های پیشرفته...")
        
        all_fractals = []
        
        # 1. فراکتال‌های ویلیامز
        williams_fractals = self._identify_williams_fractals()
        all_fractals.extend(williams_fractals)
        
        # 2. فراکتال‌های آشوب (Chaos)
        chaos_fractals = self._identify_chaos_fractals()
        all_fractals.extend(chaos_fractals)
        
        # 3. فراکتال‌های پیشرفته چندمقیاسه
        multiscale_fractals = self._identify_multiscale_fractals()
        all_fractals.extend(multiscale_fractals)
        
        # 4. فراکتال‌های NEOWave
        neowave_fractals = self._identify_neowave_fractals()
        all_fractals.extend(neowave_fractals)
        
        # فیلتر و رتبه‌بندی
        filtered_fractals = self._filter_fractals(all_fractals)
        ranked_fractals = self._rank_fractals(filtered_fractals)
        
        # محاسبه ویژگی‌های پیشرفته برای هر فراکتال
        enhanced_fractals = self._enhance_fractal_properties(ranked_fractals)
        
        self.fractal_points = enhanced_fractals
        
        logger.info(f"✅ {len(enhanced_fractals)} فراکتال معتبر شناسایی شد")
        return enhanced_fractals
        
    def _identify_williams_fractals(self) -> List[FractalPoint]:
        """شناسایی فراکتال‌های ویلیامز"""
        fractals = []
        period = self.config['williams_period']
        
        for i in range(period, len(self.data) - period):
            # فراکتال صعودی
            if self._is_williams_up(i, period):
                fractal = self._create_fractal_point(
                    i, self.data['high'].iloc[i], 
                    FractalType.WILLIAMS_UP
                )
                fractals.append(fractal)
                
            # فراکتال نزولی
            if self._is_williams_down(i, period):
                fractal = self._create_fractal_point(
                    i, self.data['low'].iloc[i],
                    FractalType.WILLIAMS_DOWN
                )
                fractals.append(fractal)
                
        return fractals
        
    def _is_williams_up(self, index: int, period: int) -> bool:
        """بررسی فراکتال صعودی ویلیامز"""
        mid_high = self.data['high'].iloc[index]
        
        # بررسی دقیق با الگوی کامل
        left_bars = all(
            self.data['high'].iloc[index - i] < mid_high 
            for i in range(1, period + 1)
        )
        right_bars = all(
            self.data['high'].iloc[index + i] < mid_high
            for i in range(1, period + 1)
        )
        
        # بررسی تاییدیه‌های اضافی
        volume_confirm = self.data['volume'].iloc[index] > self.data['volume_sma'].iloc[index]
        
        return left_bars and right_bars and volume_confirm
        
    def _is_williams_down(self, index: int, period: int) -> bool:
        """بررسی فراکتال نزولی ویلیامز"""
        mid_low = self.data['low'].iloc[index]
        
        left_bars = all(
            self.data['low'].iloc[index - i] > mid_low
            for i in range(1, period + 1)
        )
        right_bars = all(
            self.data['low'].iloc[index + i] > mid_low
            for i in range(1, period + 1)
        )
        
        volume_confirm = self.data['volume'].iloc[index] > self.data['volume_sma'].iloc[index]
        
        return left_bars and right_bars and volume_confirm
        
    def _identify_chaos_fractals(self) -> List[FractalPoint]:
        """شناسایی فراکتال‌های آشوب (Bill Williams)"""
        fractals = []
        
        # استفاده از Alligator برای تایید
        jaw = self.data['close'].rolling(13).mean().shift(8)
        teeth = self.data['close'].rolling(8).mean().shift(5)
        lips = self.data['close'].rolling(5).mean().shift(3)
        
        for i in range(13, len(self.data) - 13):
            # فراکتال صعودی آشوب
            if self._is_chaos_bullish(i, jaw, teeth, lips):
                fractal = self._create_fractal_point(
                    i, self.data['high'].iloc[i],
                    FractalType.CHAOS_BULLISH
                )
                fractals.append(fractal)
                
            # فراکتال نزولی آشوب
            if self._is_chaos_bearish(i, jaw, teeth, lips):
                fractal = self._create_fractal_point(
                    i, self.data['low'].iloc[i],
                    FractalType.CHAOS_BEARISH
                )
                fractals.append(fractal)
                
        return fractals
        
    def _is_chaos_bullish(self, index: int, jaw: pd.Series, 
                         teeth: pd.Series, lips: pd.Series) -> bool:
        """بررسی فراکتال صعودی آشوب"""
        # بررسی ساختار 5 کندلی
        high = self.data['high'].iloc[index]
        
        pattern = (
            self.data['high'].iloc[index - 2] < high and
            self.data['high'].iloc[index - 1] < high and
            self.data['high'].iloc[index + 1] < high and
            self.data['high'].iloc[index + 2] < high
        )
        
        # بررسی موقعیت نسبت به Alligator
        above_alligator = (
            high > jaw.iloc[index] and
            high > teeth.iloc[index] and
            high > lips.iloc[index]
        )
        
        return pattern and above_alligator
        
    def _is_chaos_bearish(self, index: int, jaw: pd.Series,
                          teeth: pd.Series, lips: pd.Series) -> bool:
        """بررسی فراکتال نزولی آشوب"""
        low = self.data['low'].iloc[index]
        
        pattern = (
            self.data['low'].iloc[index - 2] > low and
            self.data['low'].iloc[index - 1] > low and
            self.data['low'].iloc[index + 1] > low and
            self.data['low'].iloc[index + 2] > low
        )
        
        below_alligator = (
            low < jaw.iloc[index] and
            low < teeth.iloc[index] and
            low < lips.iloc[index]
        )
        
        return pattern and below_alligator
        
    def _identify_multiscale_fractals(self) -> List[FractalPoint]:
        """شناسایی فراکتال‌های چندمقیاسه"""
        fractals = []
        
        for scale in self.config['multi_scales']:
            scale_fractals = self._identify_scale_fractals(scale)
            
            # ادغام فراکتال‌های مقیاس‌های مختلف
            for fractal in scale_fractals:
                # بررسی تایید در مقیاس‌های دیگر
                confirmations = self._check_multiscale_confirmation(
                    fractal, self.config['multi_scales']
                )
                
                if confirmations >= len(self.config['multi_scales']) * 0.6:
                    fractal.multi_timeframe_confirmation = True
                    fractals.append(fractal)
                    
        return fractals
        
    def _identify_scale_fractals(self, scale: int) -> List[FractalPoint]:
        """شناسایی فراکتال در یک مقیاس خاص"""
        fractals = []
        
        # هموارسازی داده‌ها برای این مقیاس
        smoothed_high = gaussian_filter1d(self.data['high'].values, sigma=scale/4)
        smoothed_low = gaussian_filter1d(self.data['low'].values, sigma=scale/4)
        
        # یافتن قله‌ها و دره‌ها
        peaks = argrelextrema(smoothed_high, np.greater, order=scale)[0]
        troughs = argrelextrema(smoothed_low, np.less, order=scale)[0]
        
        # ایجاد فراکتال‌ها
        for peak in peaks:
            if scale < peak < len(self.data) - scale:
                fractal = self._create_fractal_point(
                    peak, self.data['high'].iloc[peak],
                    FractalType.MULTI_SCALE_UP
                )
                fractal.metadata['scale'] = scale
                fractals.append(fractal)
                
        for trough in troughs:
            if scale < trough < len(self.data) - scale:
                fractal = self._create_fractal_point(
                    trough, self.data['low'].iloc[trough],
                    FractalType.MULTI_SCALE_DOWN
                )
                fractal.metadata['scale'] = scale
                fractals.append(fractal)
                
        return fractals
        
    def _identify_neowave_fractals(self) -> List[FractalPoint]:
        """شناسایی فراکتال‌های مخصوص NEOWave"""
        fractals = []
        
        # محاسبه موج‌نمای قیمت برای NEOWave
        wave_profile = self._calculate_wave_profile()
        
        # شناسایی نقاط پیووت NEOWave
        for i in range(10, len(self.data) - 10):
            if self._is_neowave_pivot(i, wave_profile):
                # تعیین نوع پیووت
                pivot_type = self._determine_neowave_pivot_type(i)
                
                price = (self.data['high'].iloc[i] if pivot_type == 'high' 
                        else self.data['low'].iloc[i])
                
                fractal = self._create_fractal_point(
                    i, price, FractalType.NEOWAVE_PIVOT
                )
                
                # محاسبه ویژگی‌های NEOWave
                fractal.metadata['wave_degree'] = self._calculate_wave_degree(i)
                fractal.metadata['pattern_type'] = self._identify_pattern_type(i)
                fractal.metadata['monowave_type'] = self._classify_monowave(i)
                
                fractals.append(fractal)
                
        return fractals
        
    def _calculate_wave_profile(self) -> np.ndarray:
        """محاسبه پروفایل موج برای NEOWave"""
        # ترکیب قیمت و زمان
        prices = self.data['close'].values
        
        # محاسبه نرخ تغییر
        roc = np.gradient(prices)
        
        # محاسبه شتاب
        acceleration = np.gradient(roc)
        
        # ایجاد پروفایل موج
        wave_profile = np.zeros_like(prices)
        for i in range(2, len(prices) - 2):
            wave_profile[i] = (
                0.4 * prices[i] +
                0.3 * roc[i] +
                0.2 * acceleration[i] +
                0.1 * np.std(prices[max(0, i-5):i+5])
            )
            
        return wave_profile
        
    def _is_neowave_pivot(self, index: int, wave_profile: np.ndarray) -> bool:
        """بررسی پیووت NEOWave"""
        # قوانین پیچیده NEOWave
        
        # Rule 1: تغییر مسیر معنادار
        direction_change = self._check_direction_change(index, wave_profile)
        
        # Rule 2: نسبت‌های زمانی و قیمتی
        ratio_valid = self._check_neowave_ratios(index)
        
        # Rule 3: تایید حجمی
        volume_valid = self._check_volume_pattern(index)
        
        return direction_change and ratio_valid and volume_valid
        
    def _create_fractal_point(self, index: int, price: float,
                             fractal_type: FractalType) -> FractalPoint:
        """ایجاد نقطه فراکتال با تمام ویژگی‌ها"""
        
        # محاسبه قدرت فراکتال
        strength = self._calculate_fractal_strength(index, fractal_type)
        
        # محاسبه اطمینان
        confidence = self._calculate_confidence(index, fractal_type)
        
        # بررسی تاییدات
        volume_confirm = self._check_volume_confirmation(index)
        momentum_confirm = self._check_momentum_confirmation(index)
        trend_align = self._check_trend_alignment(index)
        
        # محاسبه ابعاد فراکتال
        dimension = self._calculate_local_dimension(index)
        hurst = self._calculate_hurst_exponent(index)
        dfa = self._calculate_dfa_alpha(index)
        
        # محاسبه احتمال برگشت
        reversal_prob = self._calculate_reversal_probability(index, fractal_type)
        
        # محاسبه اهداف قیمتی
        targets = self._calculate_target_prices(index, fractal_type)
        
        # سطح ابطال
        invalidation = self._calculate_invalidation_level(index, fractal_type)
        
        return FractalPoint(
            index=index,
            timestamp=self.data.index[index],
            price=price,
            type=fractal_type,
            strength=FractalStrength(min(6, max(1, int(strength * 6)))),
            confidence=confidence,
            volume_confirmation=volume_confirm,
            momentum_confirmation=momentum_confirm,
            trend_alignment=trend_align,
            multi_timeframe_confirmation=False,  # به‌روزرسانی می‌شود
            dimension=dimension,
            hurst_exponent=hurst,
            dfa_alpha=dfa,
            persistence_score=(hurst + dfa) / 2,
            reversal_probability=reversal_prob,
            target_prices=targets,
            invalidation_level=invalidation,
            metadata={}
        )
        
    def _calculate_fractal_strength(self, index: int, 
                                   fractal_type: FractalType) -> float:
        """محاسبه قدرت فراکتال"""
        strength = 0.5  # مقدار پایه
        
        # فاکتور 1: شدت حرکت قیمت
        price_move = abs(self.data['close'].iloc[index] - 
                        self.data['close'].iloc[max(0, index-10)])
        atr = self.data['atr'].iloc[index]
        if atr > 0:
            strength += min(0.2, (price_move / atr) * 0.1)
            
        # فاکتور 2: حجم
        volume_ratio = self.data['volume_ratio'].iloc[index]
        strength += min(0.15, (volume_ratio - 1) * 0.1)
        
        # فاکتور 3: مومنتوم
        rsi = self.data['rsi'].iloc[index]
        if fractal_type in [FractalType.WILLIAMS_UP, FractalType.CHAOS_BULLISH]:
            if rsi > 70:
                strength += 0.1
        elif rsi < 30:
            strength += 0.1
            
        # فاکتور 4: همگرایی با میانگین‌ها
        close = self.data['close'].iloc[index]
        sma20 = self.data['sma_20'].iloc[index]
        sma50 = self.data['sma_50'].iloc[index]
        
        if fractal_type in [FractalType.WILLIAMS_UP, FractalType.CHAOS_BULLISH]:
            if close > sma20 > sma50:
                strength += 0.15
        elif close < sma20 < sma50:
            strength += 0.15
            
        return min(1.0, strength)
        
    def _calculate_confidence(self, index: int, 
                            fractal_type: FractalType) -> float:
        """محاسبه سطح اطمینان"""
        confidence = 0.5
        
        # بررسی الگوی کندل
        candle_pattern = self._check_candle_pattern(index)
        if candle_pattern:
            confidence += 0.15
            
        # بررسی واگرایی
        divergence = self._check_divergence(index)
        if divergence:
            confidence += 0.2
            
        # بررسی ساختار موج
        wave_structure = self._check_wave_structure(index)
        if wave_structure:
            confidence += 0.15
            
        return min(1.0, confidence)
        
    def _check_volume_confirmation(self, index: int) -> bool:
        """بررسی تایید حجمی"""
        volume = self.data['volume'].iloc[index]
        avg_volume = self.data['volume_sma'].iloc[index]
        
        # حجم باید حداقل 20% بیشتر از میانگین باشد
        return volume > avg_volume * self.config['volume_threshold']
        
    def _check_momentum_confirmation(self, index: int) -> bool:
        """بررسی تایید مومنتوم"""
        momentum = self.data['momentum'].iloc[index]
        macd = self.data['macd'].iloc[index]
        signal = self.data['signal'].iloc[index]
        
        # MACD باید از خط سیگنال عبور کرده باشد
        macd_cross = (macd > signal and 
                     self.data['macd'].iloc[index-1] <= self.data['signal'].iloc[index-1])
        
        return abs(momentum) > self.data['momentum'].std() and macd_cross
        
    def _check_trend_alignment(self, index: int) -> bool:
        """بررسی همسویی با روند"""
        close = self.data['close'].iloc[index]
        sma20 = self.data['sma_20'].iloc[index]
        sma50 = self.data['sma_50'].iloc[index]
        
        # روند صعودی
        uptrend = sma20 > sma50 and close > sma20
        
        # روند نزولی
        downtrend = sma20 < sma50 and close < sma20
        
        return uptrend or downtrend
        
    def _calculate_local_dimension(self, index: int, window: int = 50) -> float:
        """محاسبه بعد فراکتال محلی"""
        start = max(0, index - window)
        end = min(len(self.data), index + window)
        
        prices = self.data['close'].iloc[start:end].values
        
        if len(prices) < 10:
            return 1.5  # مقدار پیش‌فرض
            
        # استفاده از چند روش و میانگین‌گیری
        dimensions = []
        
        # Higuchi
        dim_higuchi = self._higuchi_fd(prices)
        dimensions.append(dim_higuchi)
        
        # Katz
        dim_katz = self._katz_fd(prices)
        dimensions.append(dim_katz)
        
        # Petrosian
        dim_petrosian = self._petrosian_fd(prices)
        dimensions.append(dim_petrosian)
        
        return np.median(dimensions)
        
    def _higuchi_fd(self, data: np.ndarray, kmax: int = 10) -> float:
        """محاسبه بعد فراکتال هیگوچی"""
        N = len(data)
        if N < kmax * 2:
            kmax = max(2, N // 4)
            
        L = []
        k_values = list(range(1, kmax + 1))
        
        for k in k_values:
            Lk = []
            for m in range(k):
                Lm = 0
                for i in range(1, int((N - m) / k)):
                    Lm += abs(data[m + i * k] - data[m + (i - 1) * k])
                    
                if int((N - m) / k) > 0:
                    Lm = Lm * (N - 1) / (k * int((N - m) / k) * k)
                    Lk.append(Lm)
                    
            if Lk:
                L.append(np.mean(Lk))
                
        if len(L) < 2:
            return 1.5
            
        # رگرسیون log-log
        coeffs = np.polyfit(np.log(k_values[:len(L)]), np.log(L), 1)
        return abs(coeffs[0])
        
    def _katz_fd(self, data: np.ndarray) -> float:
        """محاسبه بعد فراکتال کتز"""
        N = len(data)
        if N < 2:
            return 1.5
            
        # محاسبه طول کل مسیر
        L = np.sum(np.abs(np.diff(data)))
        
        # محاسبه فاصله بین نقطه اول و آخر
        d = np.abs(data[-1] - data[0])
        
        if L == 0 or d == 0:
            return 1.5
            
        # فرمول کتز
        fd = np.log10(L) / (np.log10(d) + np.log10(N))
        
        return max(1.0, min(2.0, fd))
        
    def _petrosian_fd(self, data: np.ndarray) -> float:
        """محاسبه بعد فراکتال پتروسیان"""
        N = len(data)
        if N < 2:
            return 1.5
            
        # محاسبه تعداد تغییر علامت در مشتق
        diff = np.diff(data)
        N_delta = np.sum(diff[:-1] * diff[1:] < 0)
        
        if N_delta == 0:
            return 1.5
            
        # فرمول پتروسیان
        fd = np.log10(N) / (np.log10(N) + np.log10(N / (N + 0.4 * N_delta)))
        
        return max(1.0, min(2.0, fd))
        
    def _calculate_hurst_exponent(self, index: int, window: int = 100) -> float:
        """محاسبه نمای هرست"""
        start = max(0, index - window)
        end = min(len(self.data), index + window)
        
        prices = self.data['close'].iloc[start:end].values
        
        if len(prices) < 20:
            return 0.5
            
        # R/S analysis
        lags = range(2, min(len(prices) // 2, self.config['hurst_lags']))
        tau = []
        
        for lag in lags:
            # تقسیم به بخش‌های مساوی
            n_segments = len(prices) // lag
            if n_segments < 1:
                continue
                
            segments_rs = []
            for i in range(n_segments):
                segment = prices[i * lag:(i + 1) * lag]
                
                # محاسبه میانگین
                mean = np.mean(segment)
                
                # سری انحراف تجمعی
                cumulative = np.cumsum(segment - mean)
                
                # محدوده (R)
                R = np.max(cumulative) - np.min(cumulative)
                
                # انحراف معیار (S)
                S = np.std(segment, ddof=1)
                
                if S != 0:
                    segments_rs.append(R / S)
                    
            if segments_rs:
                tau.append(np.mean(segments_rs))
                
        if len(tau) < 2:
            return 0.5
            
        # رگرسیون log-log
        coeffs = np.polyfit(np.log(list(lags)[:len(tau)]), np.log(tau), 1)
        
        return max(0, min(1, coeffs[0]))
        
    def _calculate_dfa_alpha(self, index: int, window: int = 200) -> float:
        """محاسبه آلفای DFA"""
        start = max(0, index - window)
        end = min(len(self.data), index + window)
        
        prices = self.data['close'].iloc[start:end].values
        
        if len(prices) < 20:
            return 0.5
            
        # حذف روند و محاسبه سری تجمعی
        mean = np.mean(prices)
        y = np.cumsum(prices - mean)
        
        scales = []
        fluct = []
        
        for scale in self.config['dfa_scales']:
            if scale >= len(y) // 4:
                break
                
            # تقسیم به پنجره‌ها
            n_segments = len(y) // scale
            if n_segments < 1:
                continue
                
            variance = []
            for i in range(n_segments):
                segment = y[i * scale:(i + 1) * scale]
                
                # برازش خط روند
                x = np.arange(len(segment))
                if len(segment) > 1:
                    coeffs = np.polyfit(x, segment, 1)
                    trend = np.polyval(coeffs, x)
                    
                    # محاسبه واریانس حذف روند شده
                    detrended = segment - trend
                    variance.append(np.mean(detrended ** 2))
                    
            if variance:
                scales.append(scale)
                fluct.append(np.sqrt(np.mean(variance)))
                
        if len(scales) < 2:
            return 0.5
            
        # محاسبه آلفا از شیب log-log
        coeffs = np.polyfit(np.log(scales), np.log(fluct), 1)
        
        return max(0, min(2, coeffs[0]))
        
    def _calculate_reversal_probability(self, index: int,
                                       fractal_type: FractalType) -> float:
        """محاسبه احتمال برگشت قیمت"""
        prob = 0.5  # احتمال پایه
        
        # فاکتور 1: موقعیت RSI
        rsi = self.data['rsi'].iloc[index]
        if fractal_type in [FractalType.WILLIAMS_UP, FractalType.CHAOS_BULLISH]:
            if rsi > 80:
                prob += 0.3
            elif rsi > 70:
                prob += 0.15
        else:
            if rsi < 20:
                prob += 0.3
            elif rsi < 30:
                prob += 0.15
                
        # فاکتور 2: واگرایی
        if self._check_divergence(index):
            prob += 0.2
            
        # فاکتور 3: الگوی کندل برگشتی
        if self._check_reversal_pattern(index):
            prob += 0.15
            
        # فاکتور 4: سطوح حمایت/مقاومت
        if self._check_support_resistance(index):
            prob += 0.1
            
        # فاکتور 5: بعد فراکتال
        dimension = self._calculate_local_dimension(index)
        if dimension > 1.7:  # بازار آشوبناک
            prob += 0.1
            
        return min(0.95, prob)
        
    def _calculate_target_prices(self, index: int,
                                fractal_type: FractalType) -> List[float]:
        """محاسبه اهداف قیمتی"""
        targets = []
        current_price = self.data['close'].iloc[index]
        atr = self.data['atr'].iloc[index]
        
        # اهداف فیبوناچی
        if fractal_type in [FractalType.WILLIAMS_UP, FractalType.CHAOS_BULLISH]:
            # اهداف صعودی
            targets.append(current_price + atr * 1.618)  # 161.8%
            targets.append(current_price + atr * 2.618)  # 261.8%
            targets.append(current_price + atr * 4.236)  # 423.6%
        else:
            # اهداف نزولی
            targets.append(current_price - atr * 1.618)
            targets.append(current_price - atr * 2.618)
            targets.append(current_price - atr * 4.236)
            
        # اهداف بر اساس سطوح گذشته
        historical_levels = self._find_historical_levels(index)
        targets.extend(historical_levels[:3])
        
        return sorted(targets, key=lambda x: abs(x - current_price))[:5]
        
    def _calculate_invalidation_level(self, index: int,
                                     fractal_type: FractalType) -> float:
        """محاسبه سطح ابطال"""
        atr = self.data['atr'].iloc[index]
        
        if fractal_type in [FractalType.WILLIAMS_UP, FractalType.CHAOS_BULLISH]:
            # برای فراکتال صعودی، سطح ابطال زیر پایین‌ترین نقطه اخیر
            recent_low = self.data['low'].iloc[max(0, index-5):index+1].min()
            return recent_low - atr * 0.5
        else:
            # برای فراکتال نزولی، سطح ابطال بالای بالاترین نقطه اخیر
            recent_high = self.data['high'].iloc[max(0, index-5):index+1].max()
            return recent_high + atr * 0.5
            
    def _filter_fractals(self, fractals: List[FractalPoint]) -> List[FractalPoint]:
        """فیلتر کردن فراکتال‌های ضعیف"""
        filtered = []
        
        for fractal in fractals:
            # فیلتر بر اساس قدرت
            if fractal.strength.value < self.config['min_strength'] * 6:
                continue
                
            # فیلتر بر اساس اطمینان
            if fractal.confidence < 0.3:
                continue
                
            # فیلتر نویز بر اساس ATR
            atr = self.data['atr'].iloc[fractal.index]
            price_move = abs(fractal.price - self.data['close'].iloc[max(0, fractal.index-5)])
            
            if price_move < atr * 0.3:
                continue
                
            filtered.append(fractal)
            
        return filtered
        
    def _rank_fractals(self, fractals: List[FractalPoint]) -> List[FractalPoint]:
        """رتبه‌بندی فراکتال‌ها بر اساس اهمیت"""
        
        # محاسبه امتیاز کل برای هر فراکتال
        for fractal in fractals:
            score = 0
            
            # امتیاز قدرت
            score += fractal.strength.value * 0.3
            
            # امتیاز اطمینان
            score += fractal.confidence * 5 * 0.25
            
            # امتیاز تاییدات
            if fractal.volume_confirmation:
                score += 0.15
            if fractal.momentum_confirmation:
                score += 0.15
            if fractal.trend_alignment:
                score += 0.1
            if fractal.multi_timeframe_confirmation:
                score += 0.2
                
            # امتیاز ویژگی‌های فراکتال
            score += (2 - abs(fractal.dimension - 1.5)) * 0.1
            score += abs(fractal.hurst_exponent - 0.5) * 0.1
            
            fractal.metadata['score'] = score
            
        # مرتب‌سازی بر اساس امتیاز
        return sorted(fractals, key=lambda x: x.metadata.get('score', 0), reverse=True)
        
    def _enhance_fractal_properties(self, fractals: List[FractalPoint]) -> List[FractalPoint]:
        """بهبود ویژگی‌های فراکتال‌ها"""
        
        for fractal in fractals:
            # اضافه کردن اطلاعات موج
            fractal.metadata['wave_count'] = self._count_waves_around(fractal.index)
            fractal.metadata['wave_position'] = self._determine_wave_position(fractal.index)
            
            # اطلاعات الگو
            fractal.metadata['pattern'] = self._detect_pattern_around(fractal.index)
            
            # پیش‌بینی
            fractal.metadata['next_move_prediction'] = self._predict_next_move(fractal)
            
        return fractals
        
    def find_fractal_clusters(self, min_cluster_size: int = 3) -> List[FractalCluster]:
        """یافتن خوشه‌های فراکتال"""
        if not self.fractal_points:
            return []
            
        clusters = []
        used_fractals = set()
        
        for i, fractal in enumerate(self.fractal_points):
            if i in used_fractals:
                continue
                
            # یافتن فراکتال‌های نزدیک
            cluster_fractals = [fractal]
            used_fractals.add(i)
            
            for j, other in enumerate(self.fractal_points[i+1:], i+1):
                if j in used_fractals:
                    continue
                    
                # بررسی نزدیکی قیمتی و زمانی
                price_diff = abs(other.price - fractal.price) / fractal.price
                time_diff = abs(other.index - fractal.index)
                
                if price_diff < self.config['cluster_threshold'] and time_diff < 20:
                    cluster_fractals.append(other)
                    used_fractals.add(j)
                    
            if len(cluster_fractals) >= min_cluster_size:
                cluster = self._create_cluster(cluster_fractals)
                clusters.append(cluster)
                
        return clusters
        
    def _create_cluster(self, fractals: List[FractalPoint]) -> FractalCluster:
        """ایجاد خوشه فراکتال"""
        prices = [f.price for f in fractals]
        indices = [f.index for f in fractals]
        
        center_price = np.mean(prices)
        time_span = max(indices) - min(indices)
        density = len(fractals) / (time_span + 1)
        
        # محاسبه اهمیت خوشه
        significance = sum(f.strength.value for f in fractals) / len(fractals)
        
        # تعیین نوع خوشه
        bullish_count = sum(1 for f in fractals 
                          if f.type in [FractalType.WILLIAMS_UP, FractalType.CHAOS_BULLISH])
        bearish_count = len(fractals) - bullish_count
        
        if bullish_count > bearish_count:
            cluster_type = "مقاومت قوی"
            breakout_prob = 0.3  # احتمال شکست پایین
        else:
            cluster_type = "حمایت قوی"
            breakout_prob = 0.3
            
        # بررسی قدرت خوشه
        if significance > 4:
            breakout_prob *= 0.7  # خوشه قوی، احتمال شکست کمتر
            
        return FractalCluster(
            fractals=fractals,
            center_price=center_price,
            time_span=time_span,
            density=density,
            significance=significance,
            cluster_type=cluster_type,
            breakout_probability=breakout_prob
        )
        
    def analyze_self_similarity(self, scales: Optional[List[int]] = None) -> Dict:
        """تحلیل پیشرفته خودتشابهی"""
        if scales is None:
            scales = [2, 4, 8, 16, 32, 64]
            
        results = {
            'scales': {},
            'similarity_matrix': None,
            'scaling_exponent': None,
            'multifractal_spectrum': None
        }
        
        prices = self.data['close'].values
        
        # ماتریس تشابه
        similarity_matrix = np.zeros((len(scales), len(scales)))
        
        for i, scale1 in enumerate(scales):
            downsampled1 = prices[::scale1]
            
            for j, scale2 in enumerate(scales):
                downsampled2 = prices[::scale2]
                
                # محاسبه همبستگی
                min_len = min(len(downsampled1), len(downsampled2))
                if min_len > 10:
                    corr, _ = pearsonr(
                        downsampled1[:min_len],
                        downsampled2[:min_len]
                    )
                    similarity_matrix[i, j] = corr
                    
            # ذخیره نتایج برای هر مقیاس
            results['scales'][f'scale_{scale1}'] = {
                'fractal_dimension': self._higuchi_fd(downsampled1),
                'hurst_exponent': self._calculate_hurst_exponent_series(downsampled1),
                'sample_entropy': self._sample_entropy(downsampled1)
            }
            
        results['similarity_matrix'] = similarity_matrix
        
        # محاسبه نمای مقیاس‌بندی
        results['scaling_exponent'] = self._calculate_scaling_exponent(prices, scales)
        
        # طیف چندفراکتالی
        results['multifractal_spectrum'] = self._calculate_multifractal_spectrum(prices)
        
        return results
        
    def _calculate_hurst_exponent_series(self, series: np.ndarray) -> float:
        """محاسبه نمای هرست برای یک سری"""
        if len(series) < 20:
            return 0.5
            
        # محاسبه مشابه _calculate_hurst_exponent اما برای سری ورودی
        lags = range(2, min(len(series) // 2, 50))
        tau = []
        
        for lag in lags:
            n_segments = len(series) // lag
            if n_segments < 1:
                continue
                
            rs_values = []
            for i in range(n_segments):
                segment = series[i * lag:(i + 1) * lag]
                mean = np.mean(segment)
                cumulative = np.cumsum(segment - mean)
                R = np.max(cumulative) - np.min(cumulative)
                S = np.std(segment, ddof=1)
                
                if S != 0:
                    rs_values.append(R / S)
                    
            if rs_values:
                tau.append(np.mean(rs_values))
                
        if len(tau) < 2:
            return 0.5
            
        coeffs = np.polyfit(np.log(list(lags)[:len(tau)]), np.log(tau), 1)
        return max(0, min(1, coeffs[0]))
        
    def _sample_entropy(self, series: np.ndarray, m: int = 2, r: float = 0.2) -> float:
        """محاسبه آنتروپی نمونه"""
        N = len(series)
        if N < m + 1:
            return 0
            
        # نرمال‌سازی
        std = np.std(series)
        if std == 0:
            return 0
            
        r = r * std
        
        # ایجاد الگوهای طول m
        patterns_m = np.array([series[i:i+m] for i in range(N - m + 1)])
        
        # شمارش تطابق‌ها
        matches_m = 0
        for i in range(len(patterns_m)):
            template = patterns_m[i]
            for j in range(len(patterns_m)):
                if i != j:
                    if np.max(np.abs(template - patterns_m[j])) <= r:
                        matches_m += 1
                        
        # الگوهای طول m+1
        patterns_m1 = np.array([series[i:i+m+1] for i in range(N - m)])
        matches_m1 = 0
        
        for i in range(len(patterns_m1)):
            template = patterns_m1[i]
            for j in range(len(patterns_m1)):
                if i != j:
                    if np.max(np.abs(template - patterns_m1[j])) <= r:
                        matches_m1 += 1
                        
        # محاسبه آنتروپی
        if matches_m == 0 or matches_m1 == 0:
            return 0
            
        phi_m = matches_m / (len(patterns_m) * (len(patterns_m) - 1))
        phi_m1 = matches_m1 / (len(patterns_m1) * (len(patterns_m1) - 1))
        
        if phi_m1 == 0:
            return 0
            
        return -np.log(phi_m1 / phi_m)
        
    def _calculate_scaling_exponent(self, prices: np.ndarray, 
                                   scales: List[int]) -> float:
        """محاسبه نمای مقیاس‌بندی"""
        fluctuations = []
        
        for scale in scales:
            # محاسبه نوسان در این مقیاس
            downsampled = prices[::scale]
            if len(downsampled) > 2:
                fluct = np.std(downsampled)
                fluctuations.append(fluct)
                
        if len(fluctuations) < 2:
            return 0.5
            
        # برازش قانون توانی
        coeffs = np.polyfit(np.log(scales[:len(fluctuations)]), 
                           np.log(fluctuations), 1)
        
        return abs(coeffs[0])
        
    def _calculate_multifractal_spectrum(self, prices: np.ndarray) -> Dict:
        """محاسبه طیف چندفراکتالی"""
        # محاسبه با روش MFDFA
        q_values = np.linspace(-5, 5, 21)
        tau_q = []
        
        for q in q_values:
            # محاسبه تابع پارتیشن
            fluctuation = self._calculate_partition_function(prices, q)
            tau_q.append(fluctuation)
            
        # محاسبه طیف f(α)
        h_q = np.gradient(tau_q) / np.gradient(q_values)
        alpha = h_q + q_values * np.gradient(h_q) / np.gradient(q_values)
        f_alpha = q_values * (alpha - h_q) + 1
        
        return {
            'q_values': q_values.tolist(),
            'tau_q': tau_q,
            'h_q': h_q.tolist(),
            'alpha': alpha.tolist(),
            'f_alpha': f_alpha.tolist(),
            'width': float(np.max(alpha) - np.min(alpha)),  # عرض طیف
            'asymmetry': float(abs(np.max(h_q) + np.min(h_q))),  # عدم تقارن
        }
        
    def _calculate_partition_function(self, prices: np.ndarray, q: float) -> float:
        """محاسبه تابع پارتیشن برای طیف چندفراکتالی"""
        N = len(prices)
        scales = range(10, min(N // 4, 100), 5)
        
        fluctuations = []
        for scale in scales:
            segments = N // scale
            if segments < 2:
                continue
                
            fluct_seg = []
            for i in range(segments):
                segment = prices[i * scale:(i + 1) * scale]
                if len(segment) > 1:
                    # حذف روند
                    x = np.arange(len(segment))
                    coeffs = np.polyfit(x, segment, 1)
                    trend = np.polyval(coeffs, x)
                    detrended = segment - trend
                    
                    # محاسبه نوسان
                    fluct_seg.append(np.sqrt(np.mean(detrended ** 2)))
                    
            if fluct_seg:
                if q == 0:
                    fluctuations.append(np.exp(np.mean(np.log(fluct_seg))))
                else:
                    fluctuations.append(np.power(np.mean(np.power(fluct_seg, q)), 1/q))
                    
        if len(fluctuations) < 2:
            return 1.0
            
        # برازش قانون توانی
        coeffs = np.polyfit(np.log(list(scales)[:len(fluctuations)]), 
                           np.log(fluctuations), 1)
        
        return coeffs[0] * q - 1
        
    def perform_complete_analysis(self) -> FractalStructureAnalysis:
        """انجام تحلیل کامل ساختار فراکتال"""
        logger.info("🚀 شروع تحلیل جامع ساختار فراکتال...")
        
        # شناسایی فراکتال‌ها
        fractal_points = self.identify_advanced_fractals()
        
        # یافتن خوشه‌ها
        clusters = self.find_fractal_clusters()
        
        # پروفایل ابعاد فراکتال
        dimension_profile = {
            'higuchi': self._higuchi_fd(self.data['close'].values),
            'katz': self._katz_fd(self.data['close'].values),
            'petrosian': self._petrosian_fd(self.data['close'].values),
            'hurst': self._calculate_hurst_exponent_series(self.data['close'].values),
            'dfa': self._calculate_dfa_alpha(0, len(self.data))
        }
        
        # ماتریس خودتشابهی
        similarity_results = self.analyze_self_similarity()
        
        # قوانین مقیاس‌بندی
        scaling_laws = {
            'scaling_exponent': similarity_results.get('scaling_exponent'),
            'multifractal_spectrum': similarity_results.get('multifractal_spectrum')
        }
        
        # تعیین رژیم بازار
        market_regime = self._determine_market_regime(dimension_profile)
        
        # قدرت روند
        trend_strength = self._calculate_trend_strength()
        
        # سطح آشوب
        chaos_level = self._calculate_chaos_level(dimension_profile)
        
        # امتیاز پیش‌بینی‌پذیری
        predictability = self._calculate_predictability(dimension_profile, chaos_level)
        
        logger.info(f"✅ تحلیل کامل انجام شد - {len(fractal_points)} فراکتال، {len(clusters)} خوشه")
        
        return FractalStructureAnalysis(
            fractal_points=fractal_points,
            clusters=clusters,
            dimension_profile=dimension_profile,
            self_similarity_matrix=similarity_results.get('similarity_matrix'),
            scaling_laws=scaling_laws,
            market_regime=market_regime,
            trend_strength=trend_strength,
            chaos_level=chaos_level,
            predictability_score=predictability
        )
        
    def _determine_market_regime(self, dimension_profile: Dict) -> str:
        """تعیین رژیم بازار بر اساس ابعاد فراکتال"""
        avg_dimension = np.mean(list(dimension_profile.values())[:3])
        hurst = dimension_profile.get('hurst', 0.5)
        
        if avg_dimension < 1.3:
            if hurst > 0.6:
                return "روند قوی صعودی"
            elif hurst < 0.4:
                return "روند قوی نزولی"
            else:
                return "روند ملایم"
        elif avg_dimension < 1.5:
            if hurst > 0.55:
                return "روند با نوسان"
            else:
                return "بازار متعادل"
        elif avg_dimension < 1.7:
            return "بازار پرنوسان"
        else:
            return "بازار آشوبناک"
            
    def _calculate_trend_strength(self) -> float:
        """محاسبه قدرت روند"""
        # استفاده از ADX
        adx = self._calculate_adx()
        
        # میانگین‌های متحرک
        sma20 = self.data['sma_20'].iloc[-1]
        sma50 = self.data['sma_50'].iloc[-1]
        close = self.data['close'].iloc[-1]
        
        strength = adx / 100
        
        # بررسی همسویی قیمت با میانگین‌ها
        if (close > sma20 > sma50) or (close < sma20 < sma50):
            strength += 0.2
            
        return min(1.0, strength)
        
    def _calculate_adx(self, period: int = 14) -> float:
        """محاسبه Average Directional Index"""
        high = self.data['high']
        low = self.data['low']
        close = self.data['close']
        
        # محاسبه +DM و -DM
        plus_dm = high.diff()
        minus_dm = -low.diff()
        
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0
        
        # True Range
        tr = pd.concat([
            high - low,
            abs(high - close.shift()),
            abs(low - close.shift())
        ], axis=1).max(axis=1)
        
        # Smoothed averages
        atr = tr.rolling(period).mean()
        plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(period).mean() / atr)
        
        # ADX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(period).mean().iloc[-1]
        
        return adx if not np.isnan(adx) else 25.0
        
    def _calculate_chaos_level(self, dimension_profile: Dict) -> float:
        """محاسبه سطح آشوب بازار"""
        # ترکیب معیارهای مختلف
        avg_dimension = np.mean(list(dimension_profile.values())[:3])
        hurst = dimension_profile.get('hurst', 0.5)
        dfa = dimension_profile.get('dfa', 0.5)
        
        # محاسبه آشوب
        chaos = 0.0
        
        # بعد فراکتال بالا = آشوب بیشتر
        if avg_dimension > 1.5:
            chaos += (avg_dimension - 1.5) * 2
            
        # هرست دور از 0.5 = قابل پیش‌بینی‌تر
        chaos -= abs(hurst - 0.5) * 2
        
        # DFA
        chaos += abs(dfa - 1.0) * 0.5
        
        # نوسان
        volatility = self.data['close'].pct_change().std()
        chaos += volatility * 10
        
        return max(0, min(1, chaos))
        
    def _calculate_predictability(self, dimension_profile: Dict, 
                                chaos_level: float) -> float:
        """محاسبه امتیاز پیش‌بینی‌پذیری"""
        hurst = dimension_profile.get('hurst', 0.5)
        
        # هرست دور از 0.5 = پیش‌بینی‌پذیرتر
        predictability = abs(hurst - 0.5) * 2
        
        # آشوب کمتر = پیش‌بینی بهتر
        predictability -= chaos_level * 0.5
        
        # بعد فراکتال پایین‌تر = ساده‌تر
        avg_dimension = np.mean(list(dimension_profile.values())[:3])
        if avg_dimension < 1.5:
            predictability += 0.2
            
        return max(0, min(1, predictability))
    
    # متدهای کمکی اضافی
    def _check_multiscale_confirmation(self, fractal: FractalPoint, 
                                      scales: List[int]) -> int:
        """بررسی تایید در مقیاس‌های مختلف"""
        confirmations = 0
        
        for scale in scales:
            # بررسی وجود فراکتال مشابه در این مقیاس
            window = scale * 2
            start = max(0, fractal.index - window)
            end = min(len(self.data), fractal.index + window)
            
            for i in range(start, end):
                if i == fractal.index:
                    continue
                    
                # بررسی فراکتال در این محدوده
                if fractal.type in [FractalType.WILLIAMS_UP, FractalType.CHAOS_BULLISH]:
                    if self.data['high'].iloc[i] > self.data['high'].iloc[fractal.index] * 0.99:
                        confirmations += 1
                        break
                else:
                    if self.data['low'].iloc[i] < self.data['low'].iloc[fractal.index] * 1.01:
                        confirmations += 1
                        break
                        
        return confirmations
        
    def _check_direction_change(self, index: int, wave_profile: np.ndarray) -> bool:
        """بررسی تغییر جهت معنادار"""
        if index < 5 or index >= len(wave_profile) - 5:
            return False
            
        # محاسبه شیب قبل و بعد
        slope_before = np.mean(np.gradient(wave_profile[index-5:index]))
        slope_after = np.mean(np.gradient(wave_profile[index:index+5]))
        
        # تغییر جهت معنادار
        return abs(slope_after - slope_before) > np.std(wave_profile) * 0.5
        
    def _check_neowave_ratios(self, index: int) -> bool:
        """بررسی نسبت‌های NEOWave"""
        # پیدا کردن پیووت‌های قبلی
        recent_pivots = []
        for i in range(max(0, index - 50), index):
            if self._is_local_extreme(i):
                recent_pivots.append((i, self.data['close'].iloc[i]))
                
        if len(recent_pivots) < 2:
            return True  # اگر پیووت کافی نداریم، تایید می‌کنیم
            
        # بررسی نسبت‌های فیبوناچی
        for i in range(len(recent_pivots) - 1):
            ratio = recent_pivots[i+1][1] / recent_pivots[i][1]
            
            # نسبت‌های معتبر NEOWave
            valid_ratios = [0.382, 0.5, 0.618, 1.0, 1.618, 2.618]
            
            for valid_ratio in valid_ratios:
                if abs(ratio - valid_ratio) < 0.05:  # تولرانس 5%
                    return True
                    
        return False
        
    def _check_volume_pattern(self, index: int) -> bool:
        """بررسی الگوی حجم"""
        if index < 5:
            return True
            
        # حجم باید در نقطه پیووت افزایش یابد
        current_volume = self.data['volume'].iloc[index]
        avg_volume = self.data['volume'].iloc[index-5:index].mean()
        
        return current_volume > avg_volume * 1.2
        
    def _is_local_extreme(self, index: int, window: int = 5) -> bool:
        """بررسی نقطه اکسترمم محلی"""
        if index < window or index >= len(self.data) - window:
            return False
            
        high = self.data['high'].iloc[index]
        low = self.data['low'].iloc[index]
        
        # بررسی قله
        is_peak = all(high >= self.data['high'].iloc[i] 
                     for i in range(index - window, index + window + 1) if i != index)
        
        # بررسی دره
        is_trough = all(low <= self.data['low'].iloc[i]
                       for i in range(index - window, index + window + 1) if i != index)
        
        return is_peak or is_trough
        
    def _determine_neowave_pivot_type(self, index: int) -> str:
        """تعیین نوع پیووت NEOWave"""
        # بررسی که آیا قله است یا دره
        window = 5
        high = self.data['high'].iloc[index]
        low = self.data['low'].iloc[index]
        
        # محاسبه میانگین قبل و بعد
        if index >= window and index < len(self.data) - window:
            avg_before = self.data['close'].iloc[index-window:index].mean()
            avg_after = self.data['close'].iloc[index+1:index+window+1].mean()
            
            if high > avg_before and high > avg_after:
                return 'high'
            elif low < avg_before and low < avg_after:
                return 'low'
                
        return 'high'  # پیش‌فرض
        
    def _calculate_wave_degree(self, index: int) -> int:
        """محاسبه درجه موج"""
        # محاسبه بر اساس دامنه حرکت
        atr = self.data['atr'].iloc[index]
        price_range = self.data['high'].iloc[max(0, index-20):index+1].max() - \
                     self.data['low'].iloc[max(0, index-20):index+1].min()
        
        if price_range > atr * 10:
            return 3  # Primary
        elif price_range > atr * 5:
            return 2  # Intermediate
        elif price_range > atr * 2:
            return 1  # Minor
        else:
            return 0  # Minute
            
    def _identify_pattern_type(self, index: int) -> str:
        """شناسایی نوع الگو"""
        # الگوهای مختلف NEOWave
        patterns = [
            'impulse', 'diagonal', 'zigzag', 'flat', 
            'triangle', 'diametric', 'symmetric'
        ]
        
        # این یک نسخه ساده است - در عمل نیاز به تحلیل پیچیده‌تر دارد
        # بر اساس ساختار موج‌های اطراف
        return patterns[index % len(patterns)]
        
    def _classify_monowave(self, index: int) -> str:
        """طبقه‌بندی مونوویو"""
        # محاسبه نسبت‌های مونوویو
        if index < 10 or index >= len(self.data) - 10:
            return 'standard'
            
        # بررسی الگوی قیمت
        close = self.data['close'].iloc[index]
        prev_close = self.data['close'].iloc[index - 5]
        next_close = self.data['close'].iloc[index + 5]
        
        move_before = abs(close - prev_close)
        move_after = abs(next_close - close)
        
        ratio = move_after / move_before if move_before > 0 else 1
        
        if ratio < 0.618:
            return 'contracting'
        elif ratio > 1.618:
            return 'expanding'
        else:
            return 'standard'
            
    def _check_candle_pattern(self, index: int) -> bool:
        """بررسی الگوی کندل"""
        if index < 2:
            return False
            
        # الگوهای برگشتی ساده
        open_price = self.data['open'].iloc[index]
        close = self.data['close'].iloc[index]
        high = self.data['high'].iloc[index]
        low = self.data['low'].iloc[index]
        
        body = abs(close - open_price)
        upper_shadow = high - max(open_price, close)
        lower_shadow = min(open_price, close) - low
        
        # Doji
        if body < (high - low) * 0.1:
            return True
            
        # Hammer/Shooting Star
        if upper_shadow > body * 2 or lower_shadow > body * 2:
            return True
            
        return False
        
    def _check_divergence(self, index: int) -> bool:
        """بررسی واگرایی"""
        if index < 20:
            return False
            
        # واگرایی RSI
        price_trend = np.polyfit(range(20), self.data['close'].iloc[index-19:index+1].values, 1)[0]
        rsi_trend = np.polyfit(range(20), self.data['rsi'].iloc[index-19:index+1].values, 1)[0]
        
        # واگرایی = قیمت و RSI در جهت مخالف
        return (price_trend > 0 and rsi_trend < 0) or (price_trend < 0 and rsi_trend > 0)
        
    def _check_wave_structure(self, index: int) -> bool:
        """بررسی ساختار موج"""
        # بررسی ساده - در عمل نیاز به تحلیل پیچیده‌تر دارد
        return index % 5 in [0, 2, 4]  # موج‌های 1، 3، 5
        
    def _check_reversal_pattern(self, index: int) -> bool:
        """بررسی الگوی برگشتی"""
        return self._check_candle_pattern(index) or self._check_divergence(index)
        
    def _check_support_resistance(self, index: int) -> bool:
        """بررسی سطوح حمایت/مقاومت"""
        current_price = self.data['close'].iloc[index]
        
        # پیدا کردن سطوح قبلی
        historical_highs = self.data['high'].iloc[max(0, index-100):index]
        historical_lows = self.data['low'].iloc[max(0, index-100):index]
        
        # بررسی نزدیکی به سطوح
        for high in historical_highs:
            if abs(current_price - high) / high < 0.01:  # 1% تولرانس
                return True
                
        for low in historical_lows:
            if abs(current_price - low) / low < 0.01:
                return True
                
        return False
        
    def _find_historical_levels(self, index: int) -> List[float]:
        """یافتن سطوح تاریخی مهم"""
        levels = []
        
        # پیدا کردن قله‌ها و دره‌های قبلی
        for i in range(max(0, index - 200), index, 10):
            if self._is_local_extreme(i):
                if i < len(self.data) - 5:
                    levels.append(self.data['high'].iloc[i])
                    levels.append(self.data['low'].iloc[i])
                    
        # حذف تکراری‌ها و مرتب‌سازی
        levels = list(set(levels))
        current_price = self.data['close'].iloc[index]
        
        return sorted(levels, key=lambda x: abs(x - current_price))[:5]
        
    def _count_waves_around(self, index: int, window: int = 50) -> int:
        """شمارش موج‌های اطراف"""
        count = 0
        for i in range(max(0, index - window), min(len(self.data), index + window)):
            if self._is_local_extreme(i):
                count += 1
        return count
        
    def _determine_wave_position(self, index: int) -> str:
        """تعیین موقعیت در موج"""
        # ساده‌سازی - در عمل نیاز به تحلیل Elliott Wave دارد
        wave_count = self._count_waves_around(index)
        
        positions = ['آغاز موج', 'میانه موج', 'انتهای موج']
        return positions[wave_count % 3]
        
    def _detect_pattern_around(self, index: int) -> str:
        """تشخیص الگوی اطراف"""
        # الگوهای مختلف
        patterns = ['مثلث', 'پرچم', 'کانال', 'سر و شانه', 'دوقله', 'دودره']
        
        # ساده‌سازی - در عمل نیاز به تحلیل الگو دارد
        return patterns[index % len(patterns)]
        
    def _predict_next_move(self, fractal: FractalPoint) -> Dict:
        """پیش‌بینی حرکت بعدی"""
        prediction = {
            'direction': 'up' if fractal.type in [FractalType.WILLIAMS_DOWN, FractalType.CHAOS_BEARISH] else 'down',
            'magnitude': fractal.target_prices[0] if fractal.target_prices else 0,
            'confidence': fractal.confidence * fractal.reversal_probability,
            'timeframe': 'short' if fractal.dimension < 1.5 else 'medium'
        }
        
        return prediction

# کلاس سازگار با سیستم قدیمی
class FractalStructure(AdvancedFractalAnalyzer):
    """کلاس سازگار با سیستم قدیمی"""
    
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
        self.fractals = []
        self.fractal_dimensions = {}
        
    def identify_fractals(self, period: int = 5) -> pd.DataFrame:
        """متد سازگار با نسخه قدیمی"""
        df = self.data.copy()
        
        # شناسایی فراکتال‌های پیشرفته
        advanced_fractals = self.identify_advanced_fractals()
        
        # تبدیل به فرمت قدیمی
        df['bullish_fractal'] = False
        df['bearish_fractal'] = False
        
        for fractal in advanced_fractals:
            if fractal.type in [FractalType.WILLIAMS_UP, FractalType.CHAOS_BULLISH, 
                               FractalType.MULTI_SCALE_UP, FractalType.ADVANCED_PEAK]:
                df.loc[df.index[fractal.index], 'bullish_fractal'] = True
            else:
                df.loc[df.index[fractal.index], 'bearish_fractal'] = True
                
        self.data = df
        self.fractals = advanced_fractals
        
        return df
        
    def calculate_fractal_dimension(self, prices: np.ndarray, 
                                   method: str = 'higuchi') -> float:
        """متد سازگار با نسخه قدیمی"""
        if method == 'higuchi':
            return self._higuchi_fd(prices)
        elif method == 'box_counting':
            return self._box_counting_fd(prices)
        elif method == 'katz':
            return self._katz_fd(prices)
        elif method == 'petrosian':
            return self._petrosian_fd(prices)
        else:
            raise ValueError(f"روش ناشناخته: {method}")
            
    def _box_counting_fd(self, data: np.ndarray) -> float:
        """محاسبه بعد فراکتال با روش box-counting"""
        # نرمال‌سازی داده‌ها
        data_norm = (data - np.min(data)) / (np.max(data) - np.min(data) + 1e-10)
        
        n = len(data)
        sizes = np.logspace(0, np.log10(n/2), num=10, dtype=int)
        counts = []
        
        for size in sizes:
            if size < 1:
                continue
                
            # شمارش جعبه‌ها
            count = 0
            for i in range(0, n, size):
                subset = data_norm[i:min(i+size, n)]
                if len(subset) > 0:
                    # محاسبه تعداد جعبه‌های لازم
                    box_height = 1.0 / size if size > 1 else 1.0
                    boxes_needed = int(np.ptp(subset) / box_height) + 1
                    count += boxes_needed
                    
            if count > 0:
                counts.append(count)
            else:
                counts.append(1)
                
        if len(counts) < 2:
            return 1.5
            
        # محاسبه شیب در نمودار log-log
        valid_sizes = sizes[:len(counts)]
        coeffs = np.polyfit(np.log(valid_sizes), np.log(counts), 1)
        
        return abs(coeffs[0])