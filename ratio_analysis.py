"""
تحلیل نسبت‌ها و روابط فیبوناچی - نسخه پیشرفته
Advanced Fibonacci Ratio Analysis with Machine Learning & Deep Statistics

این ماژول شامل تحلیل‌های پیشرفته نسبت‌های فیبوناچی، روابط هندسی، 
تحلیل‌های آماری عمیق، و پیش‌بینی‌های مبتنی بر هوش مصنوعی است.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum, auto
import warnings
from scipy import stats, optimize
from scipy.spatial.distance import euclidean
from scipy.signal import find_peaks, savgol_filter
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.metrics import mean_squared_error, r2_score
import math
import itertools
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import logging

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RatioType(Enum):
    """انواع نسبت‌های فیبوناچی"""
    RETRACEMENT = "retracement"
    EXTENSION = "extension" 
    PROJECTION = "projection"
    ALTERNATION = "alternation"
    TIME_RATIO = "time_ratio"
    PRICE_RATIO = "price_ratio"
    HARMONIC = "harmonic"
    GEOMETRIC = "geometric"

class ValidationLevel(Enum):
    """سطوح اعتبارسنجی"""
    STRICT = auto()
    MODERATE = auto()
    LENIENT = auto()
    CUSTOM = auto()

class ConfidenceLevel(Enum):
    """سطوح اطمینان"""
    VERY_LOW = (0.0, 0.3)
    LOW = (0.3, 0.5)
    MEDIUM = (0.5, 0.7)
    HIGH = (0.7, 0.85)
    VERY_HIGH = (0.85, 1.0)
    
    def __init__(self, min_val: float, max_val: float):
        self.min_val = min_val
        self.max_val = max_val

@dataclass
class FibonacciRatio:
    """کلاس نسبت فیبوناچی"""
    value: float
    ratio_type: RatioType
    description: str
    theoretical_basis: str
    frequency_weight: float = 1.0
    historical_accuracy: float = 0.5
    market_regime_sensitivity: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.market_regime_sensitivity:
            self.market_regime_sensitivity = {
                'trending': 1.0,
                'ranging': 0.8,
                'volatile': 0.6,
                'low_volume': 0.4
            }

@dataclass
class RatioResult:
    """نتیجه تحلیل نسبت"""
    target_ratio: float
    closest_fibonacci: FibonacciRatio
    deviation: float
    deviation_percent: float
    confidence_score: float
    confidence_level: ConfidenceLevel
    statistical_significance: float
    z_score: float
    p_value: float
    market_context_score: float
    volume_confirmation: float
    momentum_confirmation: float
    is_valid: bool
    validation_details: Dict[str, Any] = field(default_factory=dict)
    alternative_ratios: List[FibonacciRatio] = field(default_factory=list)
    
@dataclass
class GeometricRelationship:
    """روابط هندسی بین امواج"""
    wave1_vector: np.ndarray
    wave2_vector: np.ndarray
    angle_degrees: float
    symmetry_score: float
    golden_angle_deviation: float
    spiral_correlation: float
    fractal_dimension: float
    geometric_mean: float
    
@dataclass
class AdvancedWaveMetrics:
    """متریک‌های پیشرفته موج"""
    amplitude: float
    wavelength: float
    frequency: float
    phase: float
    momentum: float
    acceleration: float
    jerk: float  # مشتق سوم
    velocity_profile: np.ndarray
    acceleration_profile: np.ndarray
    energy_density: float
    spectral_entropy: float
    
@dataclass
class StatisticalAnalysis:
    """تحلیل آماری عمیق"""
    mean: float
    median: float
    std: float
    skewness: float
    kurtosis: float
    autocorrelation: np.ndarray
    partial_autocorr: np.ndarray
    hurst_exponent: float
    fractal_dimension: float
    lyapunov_exponent: float
    entropy: float
    mutual_information: float
    
class AdvancedRatioAnalyzer:
    """تحلیلگر پیشرفته نسبت‌های فیبوناچی"""
    
    # نسبت‌های فیبوناچی کلاسیک
    CLASSIC_FIBONACCI_RATIOS = {
        RatioType.RETRACEMENT: [
            FibonacciRatio(0.236, RatioType.RETRACEMENT, "اصلاح سطحی ۲۳.۶٪", "نسبت طلایی^2", 0.7, 0.65),
            FibonacciRatio(0.382, RatioType.RETRACEMENT, "اصلاح معمولی ۳۸.۲٪", "نسبت طلایی", 1.0, 0.78),
            FibonacciRatio(0.500, RatioType.RETRACEMENT, "اصلاح نصف ۵۰٪", "نسبت نصف", 0.9, 0.72),
            FibonacciRatio(0.618, RatioType.RETRACEMENT, "اصلاح طلایی ۶۱.۸٪", "نسبت طلایی معکوس", 1.0, 0.82),
            FibonacciRatio(0.786, RatioType.RETRACEMENT, "اصلاح عمیق ۷۸.۶٪", "ریشه نسبت طلایی", 0.8, 0.68),
            FibonacciRatio(0.886, RatioType.RETRACEMENT, "اصلاح بسیار عمیق ۸۸.۶٪", "نسبت ویژه الیوت", 0.6, 0.55)
        ],
        RatioType.EXTENSION: [
            FibonacciRatio(1.000, RatioType.EXTENSION, "امواج مساوی ۱۰۰٪", "تساوی طبیعی", 0.9, 0.75),
            FibonacciRatio(1.272, RatioType.EXTENSION, "امتداد ۱۲۷.۲٪", "ریشه نسبت طلایی", 0.7, 0.65),
            FibonacciRatio(1.414, RatioType.EXTENSION, "امتداد ۱۴۱.۴٪", "ریشه ۲", 0.6, 0.58),
            FibonacciRatio(1.618, RatioType.EXTENSION, "امتداد طلایی ۱۶۱.۸٪", "نسبت طلایی", 1.0, 0.85),
            FibonacciRatio(2.000, RatioType.EXTENSION, "امتداد دوگانه ۲۰۰٪", "دوبرابر", 0.8, 0.70),
            FibonacciRatio(2.618, RatioType.EXTENSION, "امتداد ۲۶۱.۸٪", "نسبت طلایی^2", 0.9, 0.78),
            FibonacciRatio(3.618, RatioType.EXTENSION, "امتداد ۳۶۱.۸٪", "نسبت طلایی^2 + 1", 0.7, 0.62),
            FibonacciRatio(4.236, RatioType.EXTENSION, "امتداد شدید ۴۲۳.۶٪", "نسبت طلایی^3", 0.6, 0.55)
        ],
        RatioType.HARMONIC: [
            FibonacciRatio(0.707, RatioType.HARMONIC, "هارمونیک ۷۰.۷٪", "ریشه ۲ / ۲", 0.6, 0.58),
            FibonacciRatio(1.128, RatioType.HARMONIC, "هارمونیک ۱۱۲.۸٪", "e^ln(فی)/۲", 0.5, 0.52),
            FibonacciRatio(1.732, RatioType.HARMONIC, "هارمونیک ۱۷۳.۲٪", "ریشه ۳", 0.4, 0.48)
        ]
    }
    
    # نسبت‌های NEOWave خاص
    NEOWAVE_SPECIALIZED_RATIOS = {
        'monowave': [0.146, 0.236, 0.382, 0.618, 0.786],
        'polywave': [1.000, 1.618, 2.618, 4.236],
        'time_relationships': [0.382, 0.618, 1.000, 1.618, 2.618],
        'complexity_ratios': [1, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    }
    
    # ثوابت ریاضی
    PHI = (1 + np.sqrt(5)) / 2  # نسبت طلایی
    PI = np.pi
    E = np.e
    SQRT2 = np.sqrt(2)
    SQRT3 = np.sqrt(3)
    SQRT5 = np.sqrt(5)
    
    def __init__(self, waves: List[Dict], 
                 validation_level: ValidationLevel = ValidationLevel.MODERATE,
                 enable_ml: bool = True,
                 enable_statistics: bool = True,
                 enable_geometry: bool = True):
        """
        راه‌اندازی تحلیلگر پیشرفته
        
        Args:
            waves: لیست امواج برای تحلیل
            validation_level: سطح اعتبارسنجی
            enable_ml: فعال‌سازی یادگیری ماشین
            enable_statistics: فعال‌سازی تحلیل‌های آماری
            enable_geometry: فعال‌سازی تحلیل‌های هندسی
        """
        self.waves = waves
        self.validation_level = validation_level
        self.enable_ml = enable_ml
        self.enable_statistics = enable_statistics
        self.enable_geometry = enable_geometry
        
        # مدل‌های یادگیری ماشین
        self.ratio_predictor = None
        self.confidence_estimator = None
        self.anomaly_detector = None
        
        # کش برای محاسبات
        self._cache = {}
        self._statistical_cache = {}
        self._geometry_cache = {}
        
        # تنظیمات پیشرفته
        self.tolerance_base = 0.05  # تلرانس پایه ۵٪
        self.confidence_threshold = 0.6
        self.statistical_significance_threshold = 0.05
        
        # راه‌اندازی مدل‌ها
        if self.enable_ml:
            self._initialize_ml_models()
            
        # محاسبه متریک‌های اولیه
        self._calculate_base_metrics()
        
        logger.info(f"AdvancedRatioAnalyzer initialized with {len(waves)} waves")
    
    def _initialize_ml_models(self):
        """راه‌اندازی مدل‌های یادگیری ماشین"""
        try:
            # مدل پیش‌بینی نسبت
            self.ratio_predictor = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            
            # مدل تخمین اطمینان
            self.confidence_estimator = RandomForestRegressor(
                n_estimators=50,
                max_depth=8,
                random_state=42
            )
            
            # تشخیص ناهنجاری
            self.anomaly_detector = IsolationForest(
                contamination=0.1,
                random_state=42
            )
            
            logger.info("Machine Learning models initialized successfully")
            
        except Exception as e:
            logger.warning(f"ML model initialization failed: {e}")
            self.enable_ml = False
    
    def _calculate_base_metrics(self):
        """محاسبه متریک‌های پایه"""
        if not self.waves:
            return
            
        # محاسبه طول‌ها و مدت‌ها
        self.wave_lengths = [w.get('length', 0) for w in self.waves]
        self.wave_durations = [w.get('duration', 1) for w in self.waves]
        self.wave_prices = [w.get('price', 0) for w in self.waves]
        
        # محاسبه متریک‌های آماری پایه
        if self.wave_lengths:
            self.mean_length = np.mean(self.wave_lengths)
            self.std_length = np.std(self.wave_lengths)
            self.median_length = np.median(self.wave_lengths)
    
    def calculate_advanced_internal_ratios(self) -> Dict[str, Any]:
        """محاسبه نسبت‌های داخلی پیشرفته"""
        if len(self.waves) < 2:
            return {'error': 'حداقل 2 موج نیاز است'}
        
        results = {
            'classic_ratios': {},
            'advanced_ratios': {},
            'statistical_analysis': {},
            'geometric_analysis': {},
            'ml_predictions': {},
            'confidence_metrics': {},
            'market_context': {}
        }
        
        try:
            # نسبت‌های کلاسیک
            results['classic_ratios'] = self._calculate_classic_ratios()
            
            # نسبت‌های پیشرفته
            results['advanced_ratios'] = self._calculate_advanced_ratios()
            
            # تحلیل آماری
            if self.enable_statistics:
                results['statistical_analysis'] = self._perform_statistical_analysis()
            
            # تحلیل هندسی
            if self.enable_geometry:
                results['geometric_analysis'] = self._perform_geometric_analysis()
            
            # پیش‌بینی‌های ML
            if self.enable_ml and self.ratio_predictor is not None:
                results['ml_predictions'] = self._generate_ml_predictions()
            
            # متریک‌های اطمینان
            results['confidence_metrics'] = self._calculate_confidence_metrics()
            
            # بافت بازار
            results['market_context'] = self._analyze_market_context()
            
            return results
            
        except Exception as e:
            logger.error(f"Error in advanced internal ratios calculation: {e}")
            return {'error': str(e)}
    
    def _calculate_classic_ratios(self) -> Dict[str, RatioResult]:
        """محاسبه نسبت‌های کلاسیک فیبوناچی"""
        ratios = {}
        
        for i in range(len(self.waves) - 1):
            for j in range(i + 1, len(self.waves)):
                wave1 = self.waves[i]
                wave2 = self.waves[j]
                
                if wave1.get('length', 0) == 0:
                    continue
                
                ratio = wave2.get('length', 0) / wave1.get('length', 1)
                ratio_key = f"wave_{j+1}_to_wave_{i+1}"
                
                # تشخیص نوع نسبت
                if ratio < 1.0:
                    ratio_type = RatioType.RETRACEMENT
                    fibonacci_pool = self.CLASSIC_FIBONACCI_RATIOS[RatioType.RETRACEMENT]
                else:
                    ratio_type = RatioType.EXTENSION
                    fibonacci_pool = self.CLASSIC_FIBONACCI_RATIOS[RatioType.EXTENSION]
                
                # یافتن نزدیک‌ترین فیبوناچی
                result = self._find_closest_fibonacci_advanced(ratio, fibonacci_pool)
                ratios[ratio_key] = result
        
        return ratios
    
    def _calculate_advanced_ratios(self) -> Dict[str, Any]:
        """محاسبه نسبت‌های پیشرفته"""
        advanced = {
            'harmonic_ratios': {},
            'geometric_means': {},
            'weighted_averages': {},
            'momentum_ratios': {},
            'acceleration_ratios': {},
            'time_price_relationships': {},
            'spiral_relationships': {},
            'fractal_ratios': {}
        }
        
        try:
            # نسبت‌های هارمونیک
            advanced['harmonic_ratios'] = self._calculate_harmonic_ratios()
            
            # میانگین‌های هندسی
            advanced['geometric_means'] = self._calculate_geometric_means()
            
            # میانگین‌های وزنی
            advanced['weighted_averages'] = self._calculate_weighted_averages()
            
            # نسبت‌های مومنتوم
            advanced['momentum_ratios'] = self._calculate_momentum_ratios()
            
            # نسبت‌های شتاب
            advanced['acceleration_ratios'] = self._calculate_acceleration_ratios()
            
            # روابط زمان-قیمت
            advanced['time_price_relationships'] = self._calculate_time_price_relationships()
            
            # روابط مارپیچی
            advanced['spiral_relationships'] = self._calculate_spiral_relationships()
            
            # نسبت‌های فرکتال
            advanced['fractal_ratios'] = self._calculate_fractal_ratios()
            
        except Exception as e:
            logger.error(f"Error in advanced ratios calculation: {e}")
            
        return advanced
    
    def _find_closest_fibonacci_advanced(self, target_ratio: float, 
                                       fibonacci_pool: List[FibonacciRatio]) -> RatioResult:
        """یافتن نزدیک‌ترین نسبت فیبوناچی با تحلیل پیشرفته"""
        
        if not fibonacci_pool:
            return self._create_empty_ratio_result(target_ratio)
        
        # محاسبه انحرافات
        deviations = []
        for fib_ratio in fibonacci_pool:
            deviation = abs(target_ratio - fib_ratio.value)
            relative_deviation = deviation / fib_ratio.value if fib_ratio.value != 0 else float('inf')
            deviations.append((deviation, relative_deviation, fib_ratio))
        
        # پیدا کردن بهترین تطبیق
        best_match = min(deviations, key=lambda x: x[1])  # کمترین انحراف نسبی
        deviation, relative_deviation, closest_fib = best_match
        
        # محاسبه اطمینان
        confidence_score = self._calculate_ratio_confidence(
            target_ratio, closest_fib, relative_deviation
        )
        
        # تعیین سطح اطمینان
        confidence_level = self._determine_confidence_level(confidence_score)
        
        # محاسبه آمارهای تکمیلی
        z_score = self._calculate_z_score(target_ratio, closest_fib.value)
        p_value = self._calculate_p_value(z_score)
        
        # محاسبه امتیاز بافت بازار
        market_context_score = self._calculate_market_context_score(closest_fib, target_ratio)
        
        # تأیید حجمی و مومنتومی
        volume_confirmation = self._calculate_volume_confirmation(target_ratio)
        momentum_confirmation = self._calculate_momentum_confirmation(target_ratio)
        
        # اعتبارسنجی
        is_valid = self._validate_ratio_result(
            relative_deviation, confidence_score, p_value
        )
        
        # جزئیات اعتبارسنجی
        validation_details = {
            'tolerance_used': self._get_tolerance_for_ratio(closest_fib),
            'validation_level': self.validation_level.name,
            'statistical_tests': self._perform_ratio_statistical_tests(target_ratio, closest_fib),
            'market_regime_compatibility': self._check_market_regime_compatibility(closest_fib)
        }
        
        # نسبت‌های جایگزین
        alternative_ratios = self._find_alternative_ratios(target_ratio, fibonacci_pool, closest_fib)
        
        return RatioResult(
            target_ratio=target_ratio,
            closest_fibonacci=closest_fib,
            deviation=deviation,
            deviation_percent=relative_deviation * 100,
            confidence_score=confidence_score,
            confidence_level=confidence_level,
            statistical_significance=1 - p_value,
            z_score=z_score,
            p_value=p_value,
            market_context_score=market_context_score,
            volume_confirmation=volume_confirmation,
            momentum_confirmation=momentum_confirmation,
            is_valid=is_valid,
            validation_details=validation_details,
            alternative_ratios=alternative_ratios
        )
    
    def _calculate_harmonic_ratios(self) -> Dict[str, Any]:
        """محاسبه نسبت‌های هارمونیک"""
        if len(self.waves) < 3:
            return {}
        
        harmonic_results = {}
        
        # نسبت‌های هارمونیک ساده
        for i in range(len(self.waves) - 2):
            wave1 = self.waves[i].get('length', 0)
            wave2 = self.waves[i + 1].get('length', 0)
            wave3 = self.waves[i + 2].get('length', 0)
            
            if wave1 > 0 and wave2 > 0 and wave3 > 0:
                # میانگین هارمونیک
                harmonic_mean = 3 / (1/wave1 + 1/wave2 + 1/wave3)
                
                # نسبت‌های متقابل
                reciprocal_sum = 1/wave1 + 1/wave2 + 1/wave3
                
                harmonic_results[f'triplet_{i}'] = {
                    'harmonic_mean': harmonic_mean,
                    'reciprocal_sum': reciprocal_sum,
                    'harmonic_ratio_1_2': (2 * wave1 * wave2) / (wave1 + wave2),
                    'harmonic_ratio_2_3': (2 * wave2 * wave3) / (wave2 + wave3),
                    'golden_harmonic_deviation': abs(harmonic_mean - self.PHI * min(wave1, wave2, wave3))
                }
        
        return harmonic_results
    
    def _calculate_geometric_means(self) -> Dict[str, float]:
        """محاسبه میانگین‌های هندسی"""
        if len(self.waves) < 2:
            return {}
        
        geometric_means = {}
        
        # میانگین هندسی جفتی
        for i in range(len(self.waves) - 1):
            wave1 = self.waves[i].get('length', 0)
            wave2 = self.waves[i + 1].get('length', 0)
            
            if wave1 > 0 and wave2 > 0:
                geom_mean = np.sqrt(wave1 * wave2)
                geometric_means[f'pair_{i}_{i+1}'] = geom_mean
        
        # میانگین هندسی کل
        if all(w.get('length', 0) > 0 for w in self.waves):
            all_lengths = [w['length'] for w in self.waves]
            overall_geom_mean = np.power(np.prod(all_lengths), 1/len(all_lengths))
            geometric_means['overall'] = overall_geom_mean
        
        return geometric_means
    
    def _calculate_momentum_ratios(self) -> Dict[str, Any]:
        """محاسبه نسبت‌های مومنتوم"""
        momentum_ratios = {}
        
        for i, wave in enumerate(self.waves):
            wave_length = wave.get('length', 0)
            wave_duration = wave.get('duration', 1)
            
            if wave_duration > 0:
                momentum = wave_length / wave_duration
                
                momentum_ratios[f'wave_{i}'] = {
                    'momentum': momentum,
                    'velocity': momentum,  # سرعت = مومنتوم در این مقیاس
                    'normalized_momentum': momentum / self.mean_length if self.mean_length > 0 else 0
                }
        
        # نسبت‌های مومنتوم بین امواج
        for i in range(len(self.waves) - 1):
            momentum1 = momentum_ratios.get(f'wave_{i}', {}).get('momentum', 0)
            momentum2 = momentum_ratios.get(f'wave_{i+1}', {}).get('momentum', 0)
            
            if momentum1 > 0:
                momentum_ratio = momentum2 / momentum1
                momentum_ratios[f'momentum_ratio_{i}_{i+1}'] = momentum_ratio
        
        return momentum_ratios
    
    def _calculate_acceleration_ratios(self) -> Dict[str, Any]:
        """محاسبه نسبت‌های شتاب"""
        if len(self.waves) < 3:
            return {}
        
        acceleration_ratios = {}
        
        # محاسبه شتاب برای هر موج
        for i in range(1, len(self.waves) - 1):
            prev_wave = self.waves[i - 1]
            curr_wave = self.waves[i]
            next_wave = self.waves[i + 1]
            
            # محاسبه سرعت‌ها
            v1 = prev_wave.get('length', 0) / prev_wave.get('duration', 1)
            v2 = curr_wave.get('length', 0) / curr_wave.get('duration', 1)
            v3 = next_wave.get('length', 0) / next_wave.get('duration', 1)
            
            # محاسبه شتاب
            if curr_wave.get('duration', 0) > 0:
                acceleration = (v3 - v1) / (2 * curr_wave['duration'])
                
                acceleration_ratios[f'wave_{i}'] = {
                    'acceleration': acceleration,
                    'velocity_change': v3 - v1,
                    'acceleration_normalized': acceleration / self.mean_length if self.mean_length > 0 else 0
                }
        
        return acceleration_ratios
    
    def _calculate_time_price_relationships(self) -> Dict[str, Any]:
        """محاسبه روابط زمان-قیمت"""
        time_price = {}
        
        for i, wave in enumerate(self.waves):
            length = wave.get('length', 0)
            duration = wave.get('duration', 1)
            
            if duration > 0:
                time_price_ratio = length / duration
                
                # تطبیق با نسبت‌های فیبوناچی
                fibonacci_match = self._find_fibonacci_match_in_time_price(time_price_ratio)
                
                time_price[f'wave_{i}'] = {
                    'time_price_ratio': time_price_ratio,
                    'fibonacci_similarity': fibonacci_match,
                    'efficiency': length / (duration + 1),  # کارایی موج
                    'time_dominance': duration / (length + duration),  # غلبه زمان
                    'price_dominance': length / (length + duration)  # غلبه قیمت
                }
        
        return time_price
    
    def _calculate_spiral_relationships(self) -> Dict[str, Any]:
        """محاسبه روابط مارپیچی (اسپیرال طلایی)"""
        spiral_relationships = {}
        
        if len(self.waves) < 4:
            return spiral_relationships
        
        # محاسبه اسپیرال طلایی
        for i in range(len(self.waves) - 3):
            waves_group = self.waves[i:i+4]
            
            # محاسبه نسبت‌های متوالی
            ratios = []
            for j in range(3):
                if waves_group[j].get('length', 0) > 0:
                    ratio = waves_group[j+1].get('length', 0) / waves_group[j]['length']
                    ratios.append(ratio)
            
            if len(ratios) == 3:
                # تطبیق با اسپیرال طلایی
                golden_spiral_similarity = self._calculate_golden_spiral_similarity(ratios)
                
                spiral_relationships[f'group_{i}'] = {
                    'ratios': ratios,
                    'golden_spiral_similarity': golden_spiral_similarity,
                    'spiral_acceleration': self._calculate_spiral_acceleration(ratios),
                    'logarithmic_spiral_fit': self._fit_logarithmic_spiral(ratios)
                }
        
        return spiral_relationships
    
    def _calculate_fractal_ratios(self) -> Dict[str, Any]:
        """محاسبه نسبت‌های فرکتال"""
        fractal_ratios = {}
        
        if len(self.waves) < 2:
            return fractal_ratios
        
        # محاسبه بعد فرکتال
        lengths = [w.get('length', 0) for w in self.waves if w.get('length', 0) > 0]
        
        if len(lengths) >= 2:
            fractal_dimension = self._calculate_fractal_dimension(lengths)
            
            fractal_ratios['fractal_dimension'] = fractal_dimension
            fractal_ratios['complexity_index'] = fractal_dimension / 2.0  # نرمال‌سازی
            
            # نسبت‌های خودشباهت
            self_similarity_ratios = self._calculate_self_similarity_ratios(lengths)
            fractal_ratios['self_similarity'] = self_similarity_ratios
            
            # شاخص هرست
            if len(lengths) >= 10:
                hurst_exponent = self._calculate_hurst_exponent(lengths)
                fractal_ratios['hurst_exponent'] = hurst_exponent
                fractal_ratios['persistence'] = 'persistent' if hurst_exponent > 0.5 else 'anti-persistent'
        
        return fractal_ratios
    
    def _perform_statistical_analysis(self) -> StatisticalAnalysis:
        """انجام تحلیل آماری عمیق"""
        lengths = [w.get('length', 0) for w in self.waves if w.get('length', 0) > 0]
        
        if len(lengths) < 3:
            return StatisticalAnalysis(0, 0, 0, 0, 0, np.array([]), np.array([]), 0, 0, 0, 0, 0)
        
        lengths_array = np.array(lengths)
        
        # آمارهای پایه
        mean_val = np.mean(lengths_array)
        median_val = np.median(lengths_array)
        std_val = np.std(lengths_array)
        skewness_val = stats.skew(lengths_array)
        kurtosis_val = stats.kurtosis(lengths_array)
        
        # خودهمبستگی
        autocorr = self._calculate_autocorrelation(lengths_array, max_lag=min(10, len(lengths)//2))
        partial_autocorr = self._calculate_partial_autocorrelation(lengths_array, max_lag=min(5, len(lengths)//3))
        
        # نمای هرست
        hurst_exp = self._calculate_hurst_exponent(lengths_array)
        
        # بعد فرکتال
        fractal_dim = self._calculate_fractal_dimension(lengths_array)
        
        # نمای لیاپانوف
        lyapunov_exp = self._calculate_lyapunov_exponent(lengths_array)
        
        # آنتروپی
        entropy_val = self._calculate_entropy(lengths_array)
        
        # اطلاعات متقابل
        mutual_info = self._calculate_mutual_information(lengths_array)
        
        return StatisticalAnalysis(
            mean=mean_val,
            median=median_val,
            std=std_val,
            skewness=skewness_val,
            kurtosis=kurtosis_val,
            autocorrelation=autocorr,
            partial_autocorr=partial_autocorr,
            hurst_exponent=hurst_exp,
            fractal_dimension=fractal_dim,
            lyapunov_exponent=lyapunov_exp,
            entropy=entropy_val,
            mutual_information=mutual_info
        )
    
    def _perform_geometric_analysis(self) -> Dict[str, Any]:
        """انجام تحلیل هندسی"""
        if len(self.waves) < 2:
            return {}
        
        geometric_analysis = {
            'wave_vectors': {},
            'angular_relationships': {},
            'symmetry_analysis': {},
            'golden_geometry': {},
            'spiral_patterns': {}
        }
        
        # تبدیل امواج به بردارها
        wave_vectors = self._waves_to_vectors()
        geometric_analysis['wave_vectors'] = wave_vectors
        
        # روابط زاویه‌ای
        if len(wave_vectors) >= 2:
            angular_relationships = self._calculate_angular_relationships(wave_vectors)
            geometric_analysis['angular_relationships'] = angular_relationships
        
        # تحلیل تقارن
        symmetry_analysis = self._analyze_symmetry(wave_vectors)
        geometric_analysis['symmetry_analysis'] = symmetry_analysis
        
        # هندسه طلایی
        golden_geometry = self._analyze_golden_geometry(wave_vectors)
        geometric_analysis['golden_geometry'] = golden_geometry
        
        return geometric_analysis
    
    def calculate_extended_wave_validation(self, wave_number: int, 
                                         strict_validation: bool = True) -> Dict[str, Any]:
        """اعتبارسنجی پیشرفته موج ممتد"""
        
        if wave_number < 1 or wave_number > len(self.waves):
            return {'is_valid': False, 'error': 'شماره موج نامعتبر'}
        
        wave = self.waves[wave_number - 1]
        other_waves = [w for i, w in enumerate(self.waves) if i != wave_number - 1]
        
        if not other_waves:
            return {'is_valid': False, 'error': 'حداقل دو موج نیاز است'}
        
        validation_result = {
            'is_extended': False,
            'extension_ratio': 0.0,
            'confidence_score': 0.0,
            'validation_level': self.validation_level.name,
            'fibonacci_accuracy': 0.0,
            'neowave_compliance': False,
            'statistical_significance': 0.0,
            'geometric_validation': {},
            'advanced_metrics': {},
            'recommendations': []
        }
        
        try:
            wave_length = wave.get('length', 0)
            if wave_length <= 0:
                return {'is_valid': False, 'error': 'طول موج نامعتبر'}
            
            # محاسبه نسبت امتداد
            max_other_length = max(w.get('length', 0) for w in other_waves)
            
            if max_other_length <= 0:
                return {'is_valid': False, 'error': 'طول سایر امواج نامعتبر'}
            
            extension_ratio = wave_length / max_other_length
            validation_result['extension_ratio'] = extension_ratio
            
            # بررسی حد آستانه امتداد
            min_extension_ratio = 1.618 if strict_validation else 1.382
            validation_result['is_extended'] = extension_ratio >= min_extension_ratio
            
            # تطبیق با نسبت‌های فیبوناچی
            fibonacci_accuracy = self._calculate_fibonacci_accuracy_for_extension(extension_ratio)
            validation_result['fibonacci_accuracy'] = fibonacci_accuracy
            
            # بررسی انطباق با قوانین NEOWave
            neowave_compliance = self._check_neowave_compliance(wave, other_waves)
            validation_result['neowave_compliance'] = neowave_compliance
            
            # محاسبه اطمینان کلی
            confidence_factors = [
                extension_ratio / 1.618 if extension_ratio >= 1.618 else extension_ratio / 1.618 * 0.5,
                fibonacci_accuracy,
                1.0 if neowave_compliance else 0.3,
                self._calculate_volume_confirmation_for_wave(wave),
                self._calculate_momentum_confirmation_for_wave(wave)
            ]
            
            confidence_score = np.mean([min(1.0, max(0.0, factor)) for factor in confidence_factors])
            validation_result['confidence_score'] = confidence_score
            
            # تحلیل آماری
            validation_result['statistical_significance'] = self._calculate_statistical_significance_for_extension(
                extension_ratio, [w.get('length', 0) for w in other_waves]
            )
            
            # اعتبارسنجی هندسی
            validation_result['geometric_validation'] = self._validate_geometric_properties(wave, other_waves)
            
            # متریک‌های پیشرفته
            validation_result['advanced_metrics'] = self._calculate_advanced_wave_metrics(wave)
            
            # تولید توصیه‌ها
            validation_result['recommendations'] = self._generate_extension_recommendations(validation_result)
            
        except Exception as e:
            logger.error(f"Error in extended wave validation: {e}")
            validation_result['error'] = str(e)
        
        return validation_result
    
    def calculate_comprehensive_fibonacci_relationship(self, 
                                                     wave1_length: float, 
                                                     wave2_length: float,
                                                     tolerance: float = 0.05,
                                                     include_harmonics: bool = True) -> Dict[str, Any]:
        """بررسی جامع روابط فیبوناچی بین دو موج"""
        
        if wave1_length <= 0:
            return {'valid': False, 'error': 'طول موج اول باید مثبت باشد'}
        
        ratio = wave2_length / wave1_length
        
        comprehensive_result = {
            'basic_analysis': {},
            'advanced_analysis': {},
            'harmonic_analysis': {},
            'statistical_analysis': {},
            'confidence_metrics': {},
            'alternative_interpretations': [],
            'recommendations': []
        }
        
        try:
            # تحلیل پایه
            basic_result = self._analyze_basic_fibonacci_relationship(ratio, tolerance)
            comprehensive_result['basic_analysis'] = basic_result
            
            # تحلیل پیشرفته
            advanced_result = self._analyze_advanced_fibonacci_relationship(
                ratio, wave1_length, wave2_length, tolerance
            )
            comprehensive_result['advanced_analysis'] = advanced_result
            
            # تحلیل هارمونیک
            if include_harmonics:
                harmonic_result = self._analyze_harmonic_relationships(ratio, tolerance)
                comprehensive_result['harmonic_analysis'] = harmonic_result
            
            # تحلیل آماری
            statistical_result = self._analyze_statistical_properties(ratio, wave1_length, wave2_length)
            comprehensive_result['statistical_analysis'] = statistical_result
            
            # متریک‌های اطمینان
            confidence_result = self._calculate_comprehensive_confidence(comprehensive_result)
            comprehensive_result['confidence_metrics'] = confidence_result
            
            # تفسیرهای جایگزین
            alternatives = self._find_alternative_interpretations(ratio, tolerance)
            comprehensive_result['alternative_interpretations'] = alternatives
            
            # تولید توصیه‌ها
            recommendations = self._generate_comprehensive_recommendations(comprehensive_result)
            comprehensive_result['recommendations'] = recommendations
            
        except Exception as e:
            logger.error(f"Error in comprehensive fibonacci analysis: {e}")
            comprehensive_result['error'] = str(e)
        
        return comprehensive_result
    
    # متدهای کمکی - بخش اول
    def _create_empty_ratio_result(self, target_ratio: float) -> RatioResult:
        """ایجاد نتیجه خالی برای نسبت"""
        empty_fib = FibonacciRatio(0.0, RatioType.RETRACEMENT, "نامعتبر", "نامعتبر")
        return RatioResult(
            target_ratio=target_ratio,
            closest_fibonacci=empty_fib,
            deviation=0.0,
            deviation_percent=0.0,
            confidence_score=0.0,
            confidence_level=ConfidenceLevel.VERY_LOW,
            statistical_significance=0.0,
            z_score=0.0,
            p_value=1.0,
            market_context_score=0.0,
            volume_confirmation=0.0,
            momentum_confirmation=0.0,
            is_valid=False
        )
    
    def _calculate_ratio_confidence(self, target_ratio: float, 
                                  fibonacci_ratio: FibonacciRatio, 
                                  relative_deviation: float) -> float:
        """محاسبه اطمینان نسبت"""
        base_confidence = max(0.0, 1.0 - relative_deviation / self.tolerance_base)
        
        # اعمال وزن تاریخی
        historical_weight = fibonacci_ratio.historical_accuracy
        
        # اعمال وزن فرکانس
        frequency_weight = fibonacci_ratio.frequency_weight
        
        # محاسبه اطمینان نهایی
        confidence = base_confidence * historical_weight * frequency_weight
        
        return min(1.0, max(0.0, confidence))
    
    def _determine_confidence_level(self, confidence_score: float) -> ConfidenceLevel:
        """تعیین سطح اطمینان"""
        for level in ConfidenceLevel:
            if level.min_val <= confidence_score <= level.max_val:
                return level
        return ConfidenceLevel.VERY_LOW
    
    def _calculate_z_score(self, target_ratio: float, fibonacci_value: float) -> float:
        """محاسبه Z-Score"""
        if self.std_length > 0:
            return abs(target_ratio - fibonacci_value) / self.std_length
        return 0.0
    
    def _calculate_p_value(self, z_score: float) -> float:
        """محاسبه P-Value"""
        return 2 * (1 - stats.norm.cdf(abs(z_score)))
    
    def _calculate_market_context_score(self, fibonacci_ratio: FibonacciRatio, 
                                      target_ratio: float) -> float:
        """محاسبه امتیاز بافت بازار"""
        # فرض: رژیم trending
        market_regime = 'trending'
        regime_sensitivity = fibonacci_ratio.market_regime_sensitivity.get(market_regime, 0.5)
        
        # محاسبه امتیاز بر اساس شرایط بازار
        context_score = regime_sensitivity
        
        return context_score
    
    def _calculate_volume_confirmation(self, target_ratio: float) -> float:
        """محاسبه تأیید حجمی"""
        # فرض: تأیید حجمی متوسط
        return 0.6
    
    def _calculate_momentum_confirmation(self, target_ratio: float) -> float:
        """محاسبه تأیید مومنتومی"""
        # فرض: تأیید مومنتومی متوسط
        return 0.65
    
    def _validate_ratio_result(self, relative_deviation: float, 
                             confidence_score: float, p_value: float) -> bool:
        """اعتبارسنجی نتیجه نسبت"""
        tolerance = self._get_dynamic_tolerance()
        
        conditions = [
            relative_deviation <= tolerance,
            confidence_score >= self.confidence_threshold,
            p_value <= self.statistical_significance_threshold or self.validation_level == ValidationLevel.LENIENT
        ]
        
        if self.validation_level == ValidationLevel.STRICT:
            return all(conditions)
        elif self.validation_level == ValidationLevel.MODERATE:
            return sum(conditions) >= 2
        else:  # LENIENT
            return any(conditions)
    
    def _get_dynamic_tolerance(self) -> float:
        """محاسبه تلرانس دینامیک"""
        base_tolerance = self.tolerance_base
        
        if self.validation_level == ValidationLevel.STRICT:
            return base_tolerance * 0.7
        elif self.validation_level == ValidationLevel.MODERATE:
            return base_tolerance
        else:  # LENIENT
            return base_tolerance * 1.5
    
    def _get_tolerance_for_ratio(self, fibonacci_ratio: FibonacciRatio) -> float:
        """تلرانس خاص برای نسبت"""
        base_tolerance = self._get_dynamic_tolerance()
        
        # تنظیم بر اساس نوع نسبت
        if fibonacci_ratio.ratio_type in [RatioType.RETRACEMENT, RatioType.EXTENSION]:
            return base_tolerance
        else:
            return base_tolerance * 1.2
    
    # متدهای کمکی پیشرفته
    def _calculate_fractal_dimension(self, data: np.ndarray) -> float:
        """محاسبه بعد فرکتال با روش Higuchi"""
        try:
            N = len(data)
            if N < 6:
                return 1.0
            
            kmax = min(int(N/4), 20)
            
            lk = []
            for k in range(1, kmax + 1):
                Lk = []
                for m in range(k):
                    Lkm = 0
                    maxRange = int((N - m - 1) / k)
                    for i in range(1, maxRange + 1):
                        Lkm += abs(data[m + i * k] - data[m + (i - 1) * k])
                    
                    Lkm = Lkm * (N - 1) / (maxRange * k * k)
                    Lk.append(Lkm)
                
                if Lk:
                    lk.append(np.log(np.mean(Lk)))
            
            if len(lk) < 2:
                return 1.0
            
            # برازش خطی در فضای لگاریتمی
            x = np.log(range(1, len(lk) + 1))
            slope, _ = np.polyfit(x, lk, 1)
            
            fractal_dimension = -slope
            return max(1.0, min(2.0, fractal_dimension))
            
        except Exception:
            return 1.0
    
    def _calculate_hurst_exponent(self, data: np.ndarray) -> float:
        """محاسبه نمای هرست"""
        try:
            if len(data) < 10:
                return 0.5
            
            data = np.array(data)
            n = len(data)
            
            # محاسبه R/S
            lags = [int(n/(2**i)) for i in range(1, int(np.log2(n)) - 3)]
            rs = []
            
            for lag in lags:
                if lag < 4:
                    continue
                    
                # تقسیم داده به بخش‌های هم‌اندازه
                segments = int(n / lag)
                rs_values = []
                
                for i in range(segments):
                    segment = data[i*lag:(i+1)*lag]
                    
                    if len(segment) < 2:
                        continue
                    
                    # محاسبه میانگین
                    mean_segment = np.mean(segment)
                    
                    # انحرافات تجمعی
                    deviations = segment - mean_segment
                    cumulative_deviations = np.cumsum(deviations)
                    
                    # محدوده
                    R = np.max(cumulative_deviations) - np.min(cumulative_deviations)
                    
                    # انحراف معیار
                    S = np.std(segment)
                    
                    if S > 0 and R > 0:
                        rs_values.append(R / S)
                
                if rs_values:
                    rs.append(np.mean(rs_values))
            
            if len(rs) < 2:
                return 0.5
            
            # برازش خطی
            log_lags = np.log([lags[i] for i in range(len(rs))])
            log_rs = np.log(rs)
            
            hurst_exponent, _ = np.polyfit(log_lags, log_rs, 1)
            
            return max(0.0, min(1.0, hurst_exponent))
            
        except Exception:
            return 0.5
    
    def _calculate_autocorrelation(self, data: np.ndarray, max_lag: int) -> np.ndarray:
        """محاسبه خودهمبستگی"""
        try:
            if len(data) < max_lag + 1:
                return np.array([])
            
            autocorr = []
            data_centered = data - np.mean(data)
            
            for lag in range(max_lag + 1):
                if lag == 0:
                    autocorr.append(1.0)
                else:
                    corr = np.corrcoef(data_centered[:-lag], data_centered[lag:])[0, 1]
                    if np.isnan(corr):
                        corr = 0.0
                    autocorr.append(corr)
            
            return np.array(autocorr)
            
        except Exception:
            return np.array([])
    
    def _calculate_partial_autocorrelation(self, data: np.ndarray, max_lag: int) -> np.ndarray:
        """محاسبه خودهمبستگی جزئی"""
        try:
            if len(data) < max_lag + 1:
                return np.array([])
            
            # استفاده از روش Yule-Walker
            from statsmodels.tsa.stattools import pacf
            pacf_values = pacf(data, nlags=max_lag, method='ols')
            return pacf_values
            
        except Exception:
            # پیاده‌سازی ساده در صورت عدم دسترسی به statsmodels
            return np.zeros(max_lag + 1)
    
    def _calculate_lyapunov_exponent(self, data: np.ndarray) -> float:
        """محاسبه نمای لیاپانوف"""
        try:
            if len(data) < 10:
                return 0.0
            
            # روش ساده برای تخمین
            diff = np.diff(data)
            if len(diff) < 2:
                return 0.0
            
            # محاسبه نرخ واگرایی
            log_divergence = []
            for i in range(1, min(len(diff), 20)):
                if abs(diff[i-1]) > 0:
                    divergence = abs(diff[i] / diff[i-1])
                    if divergence > 0:
                        log_divergence.append(np.log(divergence))
            
            if log_divergence:
                return np.mean(log_divergence)
            else:
                return 0.0
                
        except Exception:
            return 0.0
    
    def _calculate_entropy(self, data: np.ndarray) -> float:
        """محاسبه آنتروپی"""
        try:
            if len(data) < 2:
                return 0.0
            
            # تقسیم‌بندی داده‌ها به bins
            hist, _ = np.histogram(data, bins=min(10, len(data)//2))
            
            # حذف bins خالی
            hist = hist[hist > 0]
            
            if len(hist) == 0:
                return 0.0
            
            # محاسبه احتمالات
            probabilities = hist / np.sum(hist)
            
            # محاسبه آنتروپی
            entropy = -np.sum(probabilities * np.log2(probabilities))
            
            return entropy
            
        except Exception:
            return 0.0
    
    def _calculate_mutual_information(self, data: np.ndarray) -> float:
        """محاسبه اطلاعات متقابل"""
        try:
            if len(data) < 4:
                return 0.0
            
            # تأخیر 1 برای محاسبه اطلاعات متقابل
            x = data[:-1]
            y = data[1:]
            
            # تقسیم‌بندی به bins
            bins = min(5, len(x)//3)
            hist_xy, _, _ = np.histogram2d(x, y, bins=bins)
            hist_x, _ = np.histogram(x, bins=bins)
            hist_y, _ = np.histogram(y, bins=bins)
            
            # محاسبه اطلاعات متقابل
            mi = 0.0
            n = len(x)
            
            for i in range(bins):
                for j in range(bins):
                    if hist_xy[i, j] > 0 and hist_x[i] > 0 and hist_y[j] > 0:
                        pxy = hist_xy[i, j] / n
                        px = hist_x[i] / n
                        py = hist_y[j] / n
                        mi += pxy * np.log2(pxy / (px * py))
            
            return max(0.0, mi)
            
        except Exception:
            return 0.0
    
    def _waves_to_vectors(self) -> List[np.ndarray]:
        """تبدیل امواج به بردارهای هندسی"""
        vectors = []
        
        for i, wave in enumerate(self.waves):
            length = wave.get('length', 0)
            duration = wave.get('duration', 1)
            
            # ایجاد بردار 2 بعدی (قیمت، زمان)
            vector = np.array([length, duration])
            vectors.append(vector)
        
        return vectors
    
    def _calculate_angular_relationships(self, vectors: List[np.ndarray]) -> Dict[str, Any]:
        """محاسبه روابط زاویه‌ای"""
        angular_relationships = {}
        
        for i in range(len(vectors) - 1):
            for j in range(i + 1, len(vectors)):
                vec1 = vectors[i]
                vec2 = vectors[j]
                
                # محاسبه زاویه
                dot_product = np.dot(vec1, vec2)
                norms = np.linalg.norm(vec1) * np.linalg.norm(vec2)
                
                if norms > 0:
                    cos_angle = dot_product / norms
                    cos_angle = max(-1, min(1, cos_angle))  # محدود کردن به [-1, 1]
                    angle_rad = np.arccos(cos_angle)
                    angle_deg = np.degrees(angle_rad)
                    
                    # انحراف از زاویه طلایی (137.5 درجه)
                    golden_angle_deviation = abs(angle_deg - 137.5)
                    
                    angular_relationships[f'pair_{i}_{j}'] = {
                        'angle_degrees': angle_deg,
                        'angle_radians': angle_rad,
                        'golden_angle_deviation': golden_angle_deviation,
                        'is_golden_angle': golden_angle_deviation < 10
                    }
        
        return angular_relationships
    
    def _analyze_symmetry(self, vectors: List[np.ndarray]) -> Dict[str, Any]:
        """تحلیل تقارن"""
        if len(vectors) < 2:
            return {}
        
        symmetry_analysis = {
            'bilateral_symmetry': 0.0,
            'radial_symmetry': 0.0,
            'translational_symmetry': 0.0,
            'scale_symmetry': 0.0
        }
        
        # تقارن دوطرفه
        symmetry_analysis['bilateral_symmetry'] = self._calculate_bilateral_symmetry(vectors)
        
        # تقارن شعاعی
        symmetry_analysis['radial_symmetry'] = self._calculate_radial_symmetry(vectors)
        
        # تقارن انتقالی
        symmetry_analysis['translational_symmetry'] = self._calculate_translational_symmetry(vectors)
        
        # تقارن مقیاس
        symmetry_analysis['scale_symmetry'] = self._calculate_scale_symmetry(vectors)
        
        return symmetry_analysis
    
    def _analyze_golden_geometry(self, vectors: List[np.ndarray]) -> Dict[str, Any]:
        """تحلیل هندسه طلایی"""
        golden_geometry = {
            'golden_ratios_count': 0,
            'golden_rectangles': 0,
            'golden_spirals': 0,
            'phi_relationships': []
        }
        
        # بررسی نسبت‌های طلایی
        for i in range(len(vectors) - 1):
            vec1_norm = np.linalg.norm(vectors[i])
            vec2_norm = np.linalg.norm(vectors[i + 1])
            
            if vec1_norm > 0:
                ratio = vec2_norm / vec1_norm
                phi_deviation = abs(ratio - self.PHI)
                
                if phi_deviation < 0.1:
                    golden_geometry['golden_ratios_count'] += 1
                    golden_geometry['phi_relationships'].append({
                        'pair': f'{i}_{i+1}',
                        'ratio': ratio,
                        'deviation': phi_deviation
                    })
        
        return golden_geometry
    
    # ادامه متدهای کمکی
    def _find_fibonacci_match_in_time_price(self, ratio: float) -> Dict[str, Any]:
        """یافتن تطبیق فیبوناچی در نسبت زمان-قیمت"""
        all_ratios = (
            self.CLASSIC_FIBONACCI_RATIOS[RatioType.RETRACEMENT] +
            self.CLASSIC_FIBONACCI_RATIOS[RatioType.EXTENSION] +
            self.CLASSIC_FIBONACCI_RATIOS[RatioType.HARMONIC]
        )
        
        best_match = None
        min_deviation = float('inf')
        
        for fib_ratio in all_ratios:
            deviation = abs(ratio - fib_ratio.value)
            relative_deviation = deviation / fib_ratio.value if fib_ratio.value > 0 else float('inf')
            
            if relative_deviation < min_deviation:
                min_deviation = relative_deviation
                best_match = fib_ratio
        
        if best_match:
            return {
                'fibonacci_ratio': best_match.value,
                'deviation': min_deviation,
                'similarity_score': max(0, 1 - min_deviation),
                'description': best_match.description
            }
        
        return {'similarity_score': 0.0}
    
    def _calculate_golden_spiral_similarity(self, ratios: List[float]) -> float:
        """محاسبه شباهت به اسپیرال طلایی"""
        if len(ratios) < 2:
            return 0.0
        
        # نسبت‌های ایده‌آل اسپیرال طلایی
        ideal_ratios = [self.PHI, self.PHI, self.PHI]
        
        similarities = []
        for i, ratio in enumerate(ratios):
            if i < len(ideal_ratios):
                similarity = 1 - abs(ratio - ideal_ratios[i]) / ideal_ratios[i]
                similarities.append(max(0, similarity))
        
        return np.mean(similarities) if similarities else 0.0
    
    def _calculate_spiral_acceleration(self, ratios: List[float]) -> float:
        """محاسبه شتاب اسپیرال"""
        if len(ratios) < 2:
            return 0.0
        
        accelerations = []
        for i in range(1, len(ratios)):
            acceleration = ratios[i] - ratios[i-1]
            accelerations.append(acceleration)
        
        return np.mean(accelerations) if accelerations else 0.0
    
    def _fit_logarithmic_spiral(self, ratios: List[float]) -> Dict[str, float]:
        """برازش اسپیرال لگاریتمی"""
        if len(ratios) < 3:
            return {'fit_quality': 0.0}
        
        try:
            # برازش ساده با تقریب خطی در فضای لگاریتمی
            x = np.arange(len(ratios))
            log_ratios = np.log(np.maximum(ratios, 1e-10))  # جلوگیری از log(0)
            
            slope, intercept = np.polyfit(x, log_ratios, 1)
            
            # محاسبه کیفیت برازش
            predicted = slope * x + intercept
            r_squared = r2_score(log_ratios, predicted)
            
            return {
                'fit_quality': max(0, r_squared),
                'growth_rate': slope,
                'initial_value': np.exp(intercept)
            }
        except Exception:
            return {'fit_quality': 0.0}
    
    def _calculate_self_similarity_ratios(self, lengths: List[float]) -> Dict[str, float]:
        """محاسبه نسبت‌های خودشباهت"""
        if len(lengths) < 4:
            return {}
        
        # تقسیم به دو نیمه
        mid = len(lengths) // 2
        first_half = lengths[:mid]
        second_half = lengths[mid:mid*2] if mid*2 <= len(lengths) else lengths[mid:]
        
        # محاسبه همبستگی بین نیمه‌ها
        if len(first_half) == len(second_half) and len(first_half) > 1:
            correlation = np.corrcoef(first_half, second_half)[0, 1]
            if np.isnan(correlation):
                correlation = 0.0
        else:
            correlation = 0.0
        
        # محاسبه نسبت مقیاس
        avg_first = np.mean(first_half) if first_half else 0
        avg_second = np.mean(second_half) if second_half else 0
        scale_ratio = avg_second / avg_first if avg_first > 0 else 0
        
        return {
            'self_similarity_correlation': correlation,
            'scale_ratio': scale_ratio,
            'fibonacci_scale_similarity': abs(scale_ratio - self.PHI) if scale_ratio > 0 else float('inf')
        }
    
    # متدهای اعتبارسنجی پیشرفته
    def _calculate_fibonacci_accuracy_for_extension(self, extension_ratio: float) -> float:
        """محاسبه دقت فیبوناچی برای موج ممتد"""
        extension_ratios = self.CLASSIC_FIBONACCI_RATIOS[RatioType.EXTENSION]
        
        best_match = None
        min_deviation = float('inf')
        
        for fib_ratio in extension_ratios:
            deviation = abs(extension_ratio - fib_ratio.value) / fib_ratio.value
            if deviation < min_deviation:
                min_deviation = deviation
                best_match = fib_ratio
        
        if best_match:
            accuracy = max(0, 1 - min_deviation)
            return accuracy
        
        return 0.0
    
    def _check_neowave_compliance(self, wave: Dict, other_waves: List[Dict]) -> bool:
        """بررسی انطباق با قوانین NEOWave"""
        # قانون 1: موج ممتد باید حداقل 9 زیرموج داشته باشد
        sub_waves_count = wave.get('sub_waves_count', 0)
        if sub_waves_count < 9:
            return False
        
        # قانون 2: موج ممتد نباید بیش از 161.8% بزرگترین موج دیگر باشد (حد پایین)
        wave_length = wave.get('length', 0)
        max_other_length = max(w.get('length', 0) for w in other_waves) if other_waves else 0
        
        if max_other_length > 0:
            ratio = wave_length / max_other_length
            if ratio < 1.618:
                return False
        
        # قانون 3: بررسی شکل موج (فرض: شکل طبیعی)
        wave_shape_quality = wave.get('shape_quality', 0.5)
        if wave_shape_quality < 0.6:
            return False
        
        return True
    
    def _calculate_volume_confirmation_for_wave(self, wave: Dict) -> float:
        """محاسبه تأیید حجمی برای موج"""
        volume_profile = wave.get('volume_profile', {})
        
        if not volume_profile:
            return 0.5  # تأیید متوسط در غیاب داده
        
        # تحلیل الگوی حجم
        volume_trend = volume_profile.get('trend', 'neutral')
        volume_intensity = volume_profile.get('intensity', 0.5)
        
        if volume_trend == 'increasing' and volume_intensity > 0.7:
            return 0.9
        elif volume_trend == 'stable' and volume_intensity > 0.5:
            return 0.7
        else:
            return 0.4
    
    def _calculate_momentum_confirmation_for_wave(self, wave: Dict) -> float:
        """محاسبه تأیید مومنتومی برای موج"""
        momentum_data = wave.get('momentum', {})
        
        if not momentum_data:
            return 0.5
        
        momentum_strength = momentum_data.get('strength', 0.5)
        momentum_consistency = momentum_data.get('consistency', 0.5)
        
        return (momentum_strength + momentum_consistency) / 2
    
    def _calculate_statistical_significance_for_extension(self, 
                                                        extension_ratio: float, 
                                                        other_lengths: List[float]) -> float:
        """محاسبه معناداری آماری برای امتداد"""
        if not other_lengths:
            return 0.0
        
        # آزمون t برای مقایسه موج ممتد با سایر امواج
        try:
            other_lengths_array = np.array([l for l in other_lengths if l > 0])
            
            if len(other_lengths_array) < 2:
                return 0.0
            
            # فرض: موج ممتد = extension_ratio * میانگین سایر امواج
            mean_other = np.mean(other_lengths_array)
            extended_length = extension_ratio * mean_other
            
            # آزمون t یک نمونه‌ای
            t_stat, p_value = stats.ttest_1samp(other_lengths_array, extended_length)
            
            # تبدیل p-value به امتیاز معناداری
            significance = 1 - p_value if p_value <= 1 else 0
            
            return max(0, min(1, significance))
            
        except Exception:
            return 0.0
    
    def _validate_geometric_properties(self, wave: Dict, other_waves: List[Dict]) -> Dict[str, Any]:
        """اعتبارسنجی خصوصیات هندسی"""
        geometric_validation = {
            'proportion_harmony': 0.0,
            'angular_relationships': 0.0,
            'symmetry_score': 0.0,
            'golden_ratio_presence': False
        }
        
        try:
            # تناسب هارمونیک
            wave_length = wave.get('length', 0)
            other_lengths = [w.get('length', 0) for w in other_waves if w.get('length', 0) > 0]
            
            if other_lengths:
                # محاسبه تناسب با نسبت‌های طلایی
                for other_length in other_lengths:
                    ratio = wave_length / other_length if other_length > 0 else 0
                    
                    # بررسی نزدیکی به نسبت طلایی
                    if abs(ratio - self.PHI) < 0.1:
                        geometric_validation['golden_ratio_presence'] = True
                        geometric_validation['proportion_harmony'] += 0.3
            
            # محدود کردن امتیاز
            geometric_validation['proportion_harmony'] = min(1.0, geometric_validation['proportion_harmony'])
            
        except Exception:
            pass
        
        return geometric_validation
    
    def _calculate_advanced_wave_metrics(self, wave: Dict) -> AdvancedWaveMetrics:
        """محاسبه متریک‌های پیشرفته موج"""
        length = wave.get('length', 0)
        duration = wave.get('duration', 1)
        
        # متریک‌های پایه
        amplitude = length
        wavelength = duration
        frequency = 1 / duration if duration > 0 else 0
        phase = wave.get('phase', 0)
        
        # متریک‌های دینامیکی
        momentum = length / duration if duration > 0 else 0
        acceleration = wave.get('acceleration', 0)
        jerk = wave.get('jerk', 0)
        
        # پروفایل‌های سرعت و شتاب (فرضی)
        velocity_profile = np.linspace(0, momentum, max(1, int(duration)))
        acceleration_profile = np.gradient(velocity_profile) if len(velocity_profile) > 1 else np.array([0])
        
        # چگالی انرژی
        energy_density = length ** 2 / duration if duration > 0 else 0
        
        # آنتروپی طیفی (تقریبی)
        spectral_entropy = self._calculate_spectral_entropy(velocity_profile)
        
        return AdvancedWaveMetrics(
            amplitude=amplitude,
            wavelength=wavelength,
            frequency=frequency,
            phase=phase,
            momentum=momentum,
            acceleration=acceleration,
            jerk=jerk,
            velocity_profile=velocity_profile,
            acceleration_profile=acceleration_profile,
            energy_density=energy_density,
            spectral_entropy=spectral_entropy
        )
    
    def _calculate_spectral_entropy(self, signal: np.ndarray) -> float:
        """محاسبه آنتروپی طیفی"""
        try:
            if len(signal) < 2:
                return 0.0
            
            # FFT
            fft_signal = np.fft.fft(signal)
            power_spectrum = np.abs(fft_signal) ** 2
            
            # نرمال‌سازی
            power_spectrum = power_spectrum / np.sum(power_spectrum)
            
            # حذف مقادیر صفر
            power_spectrum = power_spectrum[power_spectrum > 0]
            
            if len(power_spectrum) == 0:
                return 0.0
            
            # محاسبه آنتروپی
            entropy = -np.sum(power_spectrum * np.log2(power_spectrum))
            
            return entropy
            
        except Exception:
            return 0.0
    
    def _generate_extension_recommendations(self, validation_result: Dict) -> List[str]:
        """تولید توصیه‌ها برای موج ممتد"""
        recommendations = []
        
        confidence = validation_result.get('confidence_score', 0)
        extension_ratio = validation_result.get('extension_ratio', 0)
        fibonacci_accuracy = validation_result.get('fibonacci_accuracy', 0)
        
        if confidence > 0.8:
            recommendations.append("✅ موج ممتد با اطمینان بالا تشخیص داده شده")
        elif confidence > 0.6:
            recommendations.append("⚠️ موج ممتد احتمالی - نیاز به تأیید بیشتر")
        else:
            recommendations.append("❌ شواهد کافی برای موج ممتد وجود ندارد")
        
        if extension_ratio > 2.618:
            recommendations.append("🚀 موج فوق‌العاده ممتد - احتمال پایان روند")
        elif extension_ratio > 1.618:
            recommendations.append("📈 موج ممتد طبیعی")
        
        if fibonacci_accuracy > 0.8:
            recommendations.append("🎯 تطبیق عالی با نسبت‌های فیبوناچی")
        elif fibonacci_accuracy < 0.5:
            recommendations.append("⚠️ تطبیق ضعیف با نسبت‌های فیبوناچی")
        
        return recommendations
    
    # متدهای تحلیل جامع
    def _analyze_basic_fibonacci_relationship(self, ratio: float, tolerance: float) -> Dict[str, Any]:
        """تحلیل پایه رابطه فیبوناچی"""
        # ترکیب تمام نسبت‌های فیبوناچی
        all_ratios = []
        for ratio_type in [RatioType.RETRACEMENT, RatioType.EXTENSION, RatioType.HARMONIC]:
            all_ratios.extend(self.CLASSIC_FIBONACCI_RATIOS[ratio_type])
        
        # یافتن بهترین تطبیق
        result = self._find_closest_fibonacci_advanced(ratio, all_ratios)
        
        return {
            'target_ratio': ratio,
            'closest_fibonacci': result.closest_fibonacci.value,
            'deviation_percent': result.deviation_percent,
            'confidence_score': result.confidence_score,
            'is_valid': result.is_valid,
            'fibonacci_type': result.closest_fibonacci.ratio_type.value,
            'description': result.closest_fibonacci.description
        }
    
    def _analyze_advanced_fibonacci_relationship(self, ratio: float, 
                                               wave1_length: float, 
                                               wave2_length: float, 
                                               tolerance: float) -> Dict[str, Any]:
        """تحلیل پیشرفته رابطه فیبوناچی"""
        advanced_analysis = {
            'multi_level_analysis': {},
            'contextual_factors': {},
            'mathematical_properties': {},
            'predictive_indicators': {}
        }
        
        # تحلیل چندسطحی
        advanced_analysis['multi_level_analysis'] = self._perform_multi_level_fibonacci_analysis(ratio)
        
        # عوامل زمینه‌ای
        advanced_analysis['contextual_factors'] = self._analyze_contextual_factors(
            ratio, wave1_length, wave2_length
        )
        
        # خصوصیات ریاضی
        advanced_analysis['mathematical_properties'] = self._analyze_mathematical_properties(ratio)
        
        # شاخص‌های پیش‌بینی
        advanced_analysis['predictive_indicators'] = self._calculate_predictive_indicators(
            ratio, wave1_length, wave2_length
        )
        
        return advanced_analysis
    
    def _perform_multi_level_fibonacci_analysis(self, ratio: float) -> Dict[str, Any]:
        """انجام تحلیل چندسطحی فیبوناچی"""
        multi_level = {
            'primary_level': {},
            'secondary_level': {},
            'harmonic_level': {},
            'composite_level': {}
        }
        
        # سطح اولیه - نسبت‌های کلاسیک
        primary_ratios = self.CLASSIC_FIBONACCI_RATIOS[RatioType.RETRACEMENT] + \
                        self.CLASSIC_FIBONACCI_RATIOS[RatioType.EXTENSION]
        
        primary_result = self._find_closest_fibonacci_advanced(ratio, primary_ratios)
        multi_level['primary_level'] = {
            'closest_ratio': primary_result.closest_fibonacci.value,
            'confidence': primary_result.confidence_score,
            'type': primary_result.closest_fibonacci.ratio_type.value
        }
        
        # سطح ثانویه - نسبت‌های مرکب
        secondary_ratios = self._generate_composite_ratios()
        secondary_result = self._find_closest_fibonacci_advanced(ratio, secondary_ratios)
        multi_level['secondary_level'] = {
            'closest_ratio': secondary_result.closest_fibonacci.value,
            'confidence': secondary_result.confidence_score
        }
        
        # سطح هارمونیک
        harmonic_ratios = self.CLASSIC_FIBONACCI_RATIOS[RatioType.HARMONIC]
        harmonic_result = self._find_closest_fibonacci_advanced(ratio, harmonic_ratios)
        multi_level['harmonic_level'] = {
            'closest_ratio': harmonic_result.closest_fibonacci.value,
            'confidence': harmonic_result.confidence_score
        }
        
        return multi_level
    
    def _generate_composite_ratios(self) -> List[FibonacciRatio]:
        """تولید نسبت‌های مرکب فیبوناچی"""
        base_values = [0.382, 0.618, 1.000, 1.618, 2.618]
        composite_ratios = []
        
        # ترکیبات خطی
        for i, val1 in enumerate(base_values):
            for j, val2 in enumerate(base_values):
                if i != j:
                    # جمع
                    sum_ratio = val1 + val2
                    composite_ratios.append(FibonacciRatio(
                        sum_ratio, RatioType.EXTENSION, 
                        f"مرکب جمعی {val1}+{val2}", 
                        "ترکیب خطی", 0.5, 0.4
                    ))
                    
                    # تفریق
                    if val1 > val2:
                        diff_ratio = val1 - val2
                        composite_ratios.append(FibonacciRatio(
                            diff_ratio, RatioType.RETRACEMENT, 
                            f"مرکب تفریقی {val1}-{val2}", 
                            "تفریق خطی", 0.4, 0.3
                        ))
        
        return composite_ratios
    
    def _analyze_contextual_factors(self, ratio: float, 
                                  wave1_length: float, 
                                  wave2_length: float) -> Dict[str, Any]:
        """تحلیل عوامل زمینه‌ای"""
        contextual = {
            'magnitude_context': {},
            'relative_context': {},
            'market_context': {},
            'temporal_context': {}
        }
        
        # زمینه اندازه
        total_magnitude = wave1_length + wave2_length
        magnitude_ratio = max(wave1_length, wave2_length) / min(wave1_length, wave2_length) if min(wave1_length, wave2_length) > 0 else 0
        
        contextual['magnitude_context'] = {
            'total_magnitude': total_magnitude,
            'magnitude_ratio': magnitude_ratio,
            'magnitude_category': self._categorize_magnitude(total_magnitude)
        }
        
        # زمینه نسبی
        contextual['relative_context'] = {
            'dominance_factor': wave2_length / wave1_length if wave1_length > 0 else 0,
            'symmetry_measure': 1 - abs(wave1_length - wave2_length) / max(wave1_length, wave2_length) if max(wave1_length, wave2_length) > 0 else 0
        }
        
        return contextual
    
    def _analyze_mathematical_properties(self, ratio: float) -> Dict[str, Any]:
        """تحلیل خصوصیات ریاضی"""
        mathematical = {
            'number_theory': {},
            'geometric_properties': {},
            'algebraic_relationships': {}
        }
        
        # نظریه اعداد
        mathematical['number_theory'] = {
            'is_rational': self._is_rational_approximation(ratio),
            'decimal_precision': len(str(ratio).split('.')[-1]) if '.' in str(ratio) else 0,
            'prime_factorization_complexity': self._analyze_prime_complexity(ratio)
        }
        
        # خصوصیات هندسی
        mathematical['geometric_properties'] = {
            'golden_ratio_power': self._find_golden_ratio_power(ratio),
            'geometric_mean_relation': self._analyze_geometric_mean_relation(ratio),
            'logarithmic_properties': self._analyze_logarithmic_properties(ratio)
        }
        
        return mathematical
    
    def _calculate_predictive_indicators(self, ratio: float, 
                                       wave1_length: float, 
                                       wave2_length: float) -> Dict[str, Any]:
        """محاسبه شاخص‌های پیش‌بینی"""
        predictive = {
            'trend_continuation_probability': 0.5,
            'reversal_probability': 0.5,
            'next_wave_projections': {},
            'confidence_intervals': {}
        }
        
        # احتمال ادامه روند
        if ratio > 1.618:
            predictive['trend_continuation_probability'] = 0.3  # احتمال کم
            predictive['reversal_probability'] = 0.7  # احتمال بالا
        elif ratio > 1.0:
            predictive['trend_continuation_probability'] = 0.6
            predictive['reversal_probability'] = 0.4
        else:
            predictive['trend_continuation_probability'] = 0.7
            predictive['reversal_probability'] = 0.3
        
        # پروژکشن موج بعدی
        predictive['next_wave_projections'] = self._project_next_wave(ratio, wave2_length)
        
        return predictive
    
    def _project_next_wave(self, current_ratio: float, current_wave_length: float) -> Dict[str, Any]:
        """پروژکشن موج بعدی"""
        projections = {
            'fibonacci_targets': {},
            'probability_weighted_target': 0.0,
            'confidence_ranges': {}
        }
        
        # اهداف فیبوناچی
        fibonacci_multiples = [0.382, 0.618, 1.000, 1.618, 2.618]
        
        for multiple in fibonacci_multiples:
            target = current_wave_length * multiple
            probability = self._calculate_target_probability(current_ratio, multiple)
            
            projections['fibonacci_targets'][f'{multiple:.3f}'] = {
                'target_length': target,
                'probability': probability
            }
        
        # هدف وزن‌دار شده
        weighted_sum = sum(
            proj['target_length'] * proj['probability'] 
            for proj in projections['fibonacci_targets'].values()
        )
        total_probability = sum(
            proj['probability'] 
            for proj in projections['fibonacci_targets'].values()
        )
        
        if total_probability > 0:
            projections['probability_weighted_target'] = weighted_sum / total_probability
        
        return projections
    
    def _calculate_target_probability(self, current_ratio: float, target_multiple: float) -> float:
        """محاسبه احتمال هدف"""
        # روش ساده: نزدیکی به نسبت‌های فیبوناچی احتمال بیشتری دارد
        fibonacci_values = [0.382, 0.618, 1.000, 1.618, 2.618]
        
        min_distance = min(abs(target_multiple - fib) for fib in fibonacci_values)
        probability = max(0.1, 1.0 - min_distance)
        
        # تنظیم بر اساس نسبت فعلی
        if current_ratio > 1.5:  # موج قوی
            if target_multiple > 1.0:
                probability *= 0.7  # احتمال کمتر برای امتداد بیشتر
            else:
                probability *= 1.3  # احتمال بیشتر برای اصلاح
        
        return min(1.0, probability)
    
    # متدهای کمکی ریاضی
    def _is_rational_approximation(self, number: float, tolerance: float = 1e-6) -> bool:
        """بررسی تقریب گویا بودن عدد"""
        try:
            from fractions import Fraction
            frac = Fraction(number).limit_denominator(1000)
            return abs(float(frac) - number) < tolerance
        except:
            return False
    
    def _analyze_prime_complexity(self, number: float) -> float:
        """تحلیل پیچیدگی تجزیه اول"""
        # تقریب ساده - در عمل پیچیده‌تر است
        try:
            # تبدیل به عدد صحیح برای تحلیل
            int_part = int(number * 1000)  # ضرب در 1000 برای دقت
            
            # شمارش عوامل
            factors = 0
            temp = int_part
            d = 2
            
            while d * d <= temp and factors < 10:  # محدود کردن حلقه
                while temp % d == 0:
                    factors += 1
                    temp //= d
                d += 1
            
            if temp > 1:
                factors += 1
            
            return factors
        except:
            return 0
    
    def _find_golden_ratio_power(self, number: float) -> Dict[str, Any]:
        """یافتن توان نسبت طلایی"""
        golden_powers = {}
        
        for power in range(-3, 4):  # بررسی توان‌های -3 تا 3
            phi_power = self.PHI ** power
            deviation = abs(number - phi_power)
            relative_deviation = deviation / phi_power if phi_power > 0 else float('inf')
            
            if relative_deviation < 0.1:  # 10% تلرانس
                golden_powers[f'phi^{power}'] = {
                    'value': phi_power,
                    'deviation': deviation,
                    'relative_deviation': relative_deviation
                }
        
        return golden_powers
    
    def _analyze_geometric_mean_relation(self, number: float) -> Dict[str, Any]:
        """تحلیل رابطه میانگین هندسی"""
        # رابطه با میانگین هندسی نسبت‌های معروف
        famous_ratios = [0.382, 0.618, 1.000, 1.618, 2.618]
        
        geometric_relations = {}
        
        for i in range(len(famous_ratios) - 1):
            for j in range(i + 1, len(famous_ratios)):
                geom_mean = np.sqrt(famous_ratios[i] * famous_ratios[j])
                deviation = abs(number - geom_mean)
                
                if deviation < 0.1:
                    geometric_relations[f'geom_mean_{famous_ratios[i]}_{famous_ratios[j]}'] = {
                        'geometric_mean': geom_mean,
                        'deviation': deviation
                    }
        
        return geometric_relations
    
    def _analyze_logarithmic_properties(self, number: float) -> Dict[str, Any]:
        """تحلیل خصوصیات لگاریتمی"""
        logarithmic = {}
        
        if number > 0:
            logarithmic['natural_log'] = np.log(number)
            logarithmic['log_base_phi'] = np.log(number) / np.log(self.PHI)
            logarithmic['log_base_2'] = np.log2(number)
            logarithmic['log_base_10'] = np.log10(number)
            
            # بررسی اینکه آیا لگاریتم نزدیک به عدد صحیح است
            log_phi = logarithmic['log_base_phi']
            logarithmic['is_phi_power'] = abs(log_phi - round(log_phi)) < 0.1
        
        return logarithmic
    
    def _categorize_magnitude(self, magnitude: float) -> str:
        """دسته‌بندی اندازه"""
        if magnitude < 100:
            return "کوچک"
        elif magnitude < 1000:
            return "متوسط"
        elif magnitude < 10000:
            return "بزرگ"
        else:
            return "خیلی بزرگ"
    
    # متدهای کمکی تحلیل هندسی
    def _calculate_bilateral_symmetry(self, vectors: List[np.ndarray]) -> float:
        """محاسبه تقارن دوطرفه"""
        if len(vectors) < 2:
            return 0.0
        
        # تقارن ساده بر اساس اندازه بردارها
        lengths = [np.linalg.norm(vec) for vec in vectors]
        
        if len(lengths) < 2:
            return 0.0
        
        # محاسبه تقارن جفتی
        symmetries = []
        for i in range(0, len(lengths) - 1, 2):
            if i + 1 < len(lengths):
                l1, l2 = lengths[i], lengths[i + 1]
                symmetry = 1 - abs(l1 - l2) / max(l1, l2) if max(l1, l2) > 0 else 0
                symmetries.append(symmetry)
        
        return np.mean(symmetries) if symmetries else 0.0
    
    def _calculate_radial_symmetry(self, vectors: List[np.ndarray]) -> float:
        """محاسبه تقارن شعاعی"""
        if len(vectors) < 3:
            return 0.0
        
        # محاسبه زوایا نسبت به مرکز
        angles = []
        for vec in vectors:
            if np.linalg.norm(vec) > 0:
                angle = np.arctan2(vec[1], vec[0])
                angles.append(angle)
        
        if len(angles) < 3:
            return 0.0
        
        # بررسی توزیع یکنواخت زوایا
        angles = np.array(angles)
        angles = np.sort(angles)
        
        expected_spacing = 2 * np.pi / len(angles)
        actual_spacings = np.diff(angles)
        
        # افزودن فاصله بین آخرین و اولین زاویه
        actual_spacings = np.append(actual_spacings, 2 * np.pi - (angles[-1] - angles[0]))
        
        # محاسبه انحراف از توزیع یکنواخت
        deviations = np.abs(actual_spacings - expected_spacing)
        mean_deviation = np.mean(deviations)
        
        # تبدیل به امتیاز تقارن
        symmetry_score = max(0, 1 - mean_deviation / expected_spacing)
        
        return symmetry_score
    
    def _calculate_translational_symmetry(self, vectors: List[np.ndarray]) -> float:
        """محاسبه تقارن انتقالی"""
        if len(vectors) < 4:
            return 0.0
        
        # بررسی الگوهای تکراری
        similarities = []
        
        # مقایسه جفت‌های متوالی
        for i in range(len(vectors) - 2):
            vec1 = vectors[i]
            vec2 = vectors[i + 1]
            vec3 = vectors[i + 2]
            
            # بردار تفاضل
            diff1 = vec2 - vec1
            diff2 = vec3 - vec2
            
            # شباهت بردارهای تفاضل
            if np.linalg.norm(diff1) > 0 and np.linalg.norm(diff2) > 0:
                cosine_sim = np.dot(diff1, diff2) / (np.linalg.norm(diff1) * np.linalg.norm(diff2))
                similarities.append(max(0, cosine_sim))
        
        return np.mean(similarities) if similarities else 0.0
    
    def _calculate_scale_symmetry(self, vectors: List[np.ndarray]) -> float:
        """محاسبه تقارن مقیاس"""
        if len(vectors) < 2:
            return 0.0
        
        # محاسبه نسبت‌های مقیاس متوالی
        scale_ratios = []
        lengths = [np.linalg.norm(vec) for vec in vectors]
        
        for i in range(len(lengths) - 1):
            if lengths[i] > 0:
                ratio = lengths[i + 1] / lengths[i]
                scale_ratios.append(ratio)
        
        if len(scale_ratios) < 2:
            return 0.0
        
        # بررسی ثبات نسبت مقیاس
        ratio_std = np.std(scale_ratios)
        ratio_mean = np.mean(scale_ratios)
        
        if ratio_mean > 0:
            coefficient_of_variation = ratio_std / ratio_mean
            scale_symmetry = max(0, 1 - coefficient_of_variation)
        else:
            scale_symmetry = 0.0
        
        return scale_symmetry
    
    # متدهای اضافی برای تکمیل کلاس
    def _generate_ml_predictions(self) -> Dict[str, Any]:
        """تولید پیش‌بینی‌های یادگیری ماشین"""
        if not self.enable_ml or self.ratio_predictor is None:
            return {}
        
        # در صورت نیاز، پیاده‌سازی پیش‌بینی‌های ML
        return {
            'ml_enabled': True,
            'predictions_available': False,
            'note': 'ML predictions require training data'
        }
    
    def _calculate_confidence_metrics(self) -> Dict[str, Any]:
        """محاسبه متریک‌های اطمینان"""
        if not self.waves:
            return {}
        
        confidence_metrics = {
            'overall_confidence': 0.0,
            'data_quality_score': 0.0,
            'sample_size_adequacy': 0.0,
            'consistency_score': 0.0
        }
        
        # ارزیابی کیفیت داده
        valid_waves = sum(1 for w in self.waves if w.get('length', 0) > 0)
        data_quality = valid_waves / len(self.waves) if self.waves else 0
        confidence_metrics['data_quality_score'] = data_quality
        
        # کفایت اندازه نمونه
        sample_adequacy = min(1.0, len(self.waves) / 5)  # حداقل 5 موج برای تحلیل مطمئن
        confidence_metrics['sample_size_adequacy'] = sample_adequacy
        
        # اطمینان کلی
        overall_confidence = (data_quality + sample_adequacy) / 2
        confidence_metrics['overall_confidence'] = overall_confidence
        
        return confidence_metrics
    
    def _analyze_market_context(self) -> Dict[str, Any]:
        """تحلیل بافت بازار"""
        market_context = {
            'market_regime': 'unknown',
            'volatility_level': 'medium',
            'trend_strength': 0.5,
            'volume_profile': 'normal',
            'sentiment_indicator': 'neutral'
        }
        
        if self.waves and len(self.waves) >= 3:
            # تخمین رژیم بازار بر اساس امواج
            lengths = [w.get('length', 0) for w in self.waves]
            length_std = np.std(lengths) if lengths else 0
            length_mean = np.mean(lengths) if lengths else 0
            
            if length_mean > 0:
                cv = length_std / length_mean  # ضریب تغییرات
                
                if cv < 0.3:
                    market_context['volatility_level'] = 'low'
                    market_context['market_regime'] = 'trending'
                elif cv > 0.7:
                    market_context['volatility_level'] = 'high'
                    market_context['market_regime'] = 'volatile'
                else:
                    market_context['volatility_level'] = 'medium'
                    market_context['market_regime'] = 'mixed'
        
        return market_context
    
    def _perform_ratio_statistical_tests(self, target_ratio: float, 
                                       fibonacci_ratio: FibonacciRatio) -> Dict[str, Any]:
        """انجام آزمون‌های آماری نسبت"""
        tests = {
            'normality_test': {},
            'goodness_of_fit': {},
            'outlier_detection': {}
        }
        
        # در حالت واقعی، آزمون‌های آماری پیچیده‌تری انجام می‌شود
        tests['goodness_of_fit'] = {
            'test_statistic': abs(target_ratio - fibonacci_ratio.value),
            'p_value': self._calculate_p_value(abs(target_ratio - fibonacci_ratio.value)),
            'conclusion': 'acceptable' if abs(target_ratio - fibonacci_ratio.value) < 0.1 else 'questionable'
        }
        
        return tests
    
    def _check_market_regime_compatibility(self, fibonacci_ratio: FibonacciRatio) -> Dict[str, Any]:
        """بررسی سازگاری رژیم بازار"""
        compatibility = {
            'regime_match': True,
            'confidence_adjustment': 1.0,
            'recommendations': []
        }
        
        # فرض: رژیم trending
        market_regime = 'trending'
        regime_sensitivity = fibonacci_ratio.market_regime_sensitivity.get(market_regime, 0.5)
        
        if regime_sensitivity < 0.5:
            compatibility['regime_match'] = False
            compatibility['confidence_adjustment'] = 0.7
            compatibility['recommendations'].append("نسبت با رژیم فعلی بازار سازگاری کمی دارد")
        
        return compatibility
    
    def _find_alternative_ratios(self, target_ratio: float, 
                               fibonacci_pool: List[FibonacciRatio], 
                               primary_match: FibonacciRatio) -> List[FibonacciRatio]:
        """یافتن نسبت‌های جایگزین"""
        alternatives = []
        
        # مرتب‌سازی بر اساس انحراف
        sorted_ratios = sorted(
            fibonacci_pool, 
            key=lambda x: abs(target_ratio - x.value)
        )
        
        # انتخاب 3 گزینه برتر (غیر از انتخاب اولیه)
        for ratio in sorted_ratios[:4]:
            if ratio != primary_match:
                alternatives.append(ratio)
            if len(alternatives) >= 3:
                break
        
        return alternatives
    
    def _analyze_harmonic_relationships(self, ratio: float, tolerance: float) -> Dict[str, Any]:
        """تحلیل روابط هارمونیک"""
        harmonic_analysis = {
            'harmonic_matches': [],
            'harmonic_series_position': None,
            'overtone_relationships': {}
        }
        
        # بررسی تطبیق با سری هارمونیک
        harmonic_series = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]  # سری هارمونیک ساده
        
        for i, harmonic in enumerate(harmonic_series):
            deviation = abs(ratio - harmonic)
            if deviation < tolerance:
                harmonic_analysis['harmonic_matches'].append({
                    'harmonic_number': i + 1,
                    'harmonic_value': harmonic,
                    'deviation': deviation
                })
        
        # بررسی نسبت‌های overtone
        for i in range(len(harmonic_series) - 1):
            for j in range(i + 1, len(harmonic_series)):
                overtone_ratio = harmonic_series[j] / harmonic_series[i]
                if abs(ratio - overtone_ratio) < tolerance:
                    harmonic_analysis['overtone_relationships'][f'{i+1}_{j+1}'] = {
                        'ratio': overtone_ratio,
                        'deviation': abs(ratio - overtone_ratio)
                    }
        
        return harmonic_analysis
    
    def _analyze_statistical_properties(self, ratio: float, 
                                      wave1_length: float, 
                                      wave2_length: float) -> Dict[str, Any]:
        """تحلیل خصوصیات آماری"""
        statistical = {
            'distribution_analysis': {},
            'correlation_measures': {},
            'regression_analysis': {}
        }
        
        # تحلیل توزیع (فرضی)
        statistical['distribution_analysis'] = {
            'ratio_percentile': self._estimate_ratio_percentile(ratio),
            'z_score': self._calculate_z_score(ratio, 1.0),  # فرض میانگین 1
            'probability_density': self._estimate_probability_density(ratio)
        }
        
        # اندازه‌گیری همبستگی
        if self.wave_lengths and len(self.wave_lengths) > 2:
            correlation_with_history = np.corrcoef([ratio], self.wave_lengths[:1])[0, 1] if len(self.wave_lengths) > 0 else 0
            statistical['correlation_measures'] = {
                'historical_correlation': correlation_with_history if not np.isnan(correlation_with_history) else 0
            }
        
        return statistical
    
    def _calculate_comprehensive_confidence(self, comprehensive_result: Dict) -> Dict[str, Any]:
        """محاسبه اطمینان جامع"""
        confidence_factors = []
        
        # اطمینان تحلیل پایه
        basic_confidence = comprehensive_result.get('basic_analysis', {}).get('confidence_score', 0)
        confidence_factors.append(('basic', basic_confidence, 0.4))
        
        # اطمینان تحلیل پیشرفته
        advanced_analysis = comprehensive_result.get('advanced_analysis', {})
        multi_level = advanced_analysis.get('multi_level_analysis', {})
        primary_confidence = multi_level.get('primary_level', {}).get('confidence', 0)
        confidence_factors.append(('advanced', primary_confidence, 0.3))
        
        # اطمینان هارمونیک
        harmonic_analysis = comprehensive_result.get('harmonic_analysis', {})
        harmonic_matches = len(harmonic_analysis.get('harmonic_matches', []))
        harmonic_confidence = min(1.0, harmonic_matches / 3)  # حداکثر 3 تطبیق
        confidence_factors.append(('harmonic', harmonic_confidence, 0.2))
        
        # اطمینان آماری
        statistical_analysis = comprehensive_result.get('statistical_analysis', {})
        statistical_confidence = 0.5  # فرض متوسط
        confidence_factors.append(('statistical', statistical_confidence, 0.1))
        
        # محاسبه اطمینان وزن‌دار
        total_weight = sum(weight for _, _, weight in confidence_factors)
        weighted_confidence = sum(
            confidence * weight for _, confidence, weight in confidence_factors
        ) / total_weight if total_weight > 0 else 0
        
        return {
            'overall_confidence': weighted_confidence,
            'confidence_breakdown': {
                name: confidence for name, confidence, _ in confidence_factors
            },
            'confidence_level': self._determine_confidence_level(weighted_confidence).name
        }
    
    def _find_alternative_interpretations(self, ratio: float, tolerance: float) -> List[Dict[str, Any]]:
        """یافتن تفسیرهای جایگزین"""
        alternatives = []
        
        # تفسیر ریاضی
        alternatives.append({
            'interpretation_type': 'mathematical',
            'description': f"نسبت {ratio:.3f} به عنوان ضریب مقیاس",
            'confidence': 0.6,
            'mathematical_basis': 'تحلیل مقیاس هندسی'
        })
        
        # تفسیر موجی
        if 0.5 < ratio < 0.9:
            alternatives.append({
                'interpretation_type': 'corrective',
                'description': 'احتمال موج اصلاحی',
                'confidence': 0.7,
                'wave_theory_basis': 'نظریه امواج الیوت'
            })
        elif ratio > 1.5:
            alternatives.append({
                'interpretation_type': 'impulsive',
                'description': 'احتمال موج شتابدار',
                'confidence': 0.8,
                'wave_theory_basis': 'نظریه امواج الیوت'
            })
        
        return alternatives
    
    def _generate_comprehensive_recommendations(self, comprehensive_result: Dict) -> List[str]:
        """تولید توصیه‌های جامع"""
        recommendations = []
        
        # بر اساس اطمینان کلی
        overall_confidence = comprehensive_result.get('confidence_metrics', {}).get('overall_confidence', 0)
        
        if overall_confidence > 0.8:
            recommendations.append("✅ تطبیق عالی با نسبت‌های فیبوناچی - اعتماد بالا")
        elif overall_confidence > 0.6:
            recommendations.append("⚠️ تطبیق قابل قبول - نیاز به تأیید بیشتر")
        else:
            recommendations.append("❌ تطبیق ضعیف - بررسی مجدد توصیه می‌شود")
        
        # بر اساس تحلیل پیشرفته
        advanced_analysis = comprehensive_result.get('advanced_analysis', {})
        predictive_indicators = advanced_analysis.get('predictive_indicators', {})
        
        trend_continuation = predictive_indicators.get('trend_continuation_probability', 0.5)
        if trend_continuation > 0.7:
            recommendations.append("📈 احتمال بالای ادامه روند")
        elif trend_continuation < 0.3:
            recommendations.append("🔄 احتمال بالای تغییر روند")
        
        # بر اساس تحلیل هارمونیک
        harmonic_analysis = comprehensive_result.get('harmonic_analysis', {})
        harmonic_matches = harmonic_analysis.get('harmonic_matches', [])
        
        if len(harmonic_matches) > 0:
            recommendations.append("🎵 تطبیق با نسبت‌های هارمونیک یافت شده")
        
        return recommendations
    
    def _estimate_ratio_percentile(self, ratio: float) -> float:
        """تخمین صدک نسبت"""
        # تخمین ساده بر اساس توزیع نرمال
        # در عمل باید از داده‌های تاریخی استفاده کرد
        if ratio < 0.5:
            return 0.2
        elif ratio < 1.0:
            return 0.4
        elif ratio < 1.5:
            return 0.6
        elif ratio < 2.0:
            return 0.8
        else:
            return 0.9
    
    def _estimate_probability_density(self, ratio: float) -> float:
        """تخمین چگالی احتمال"""
        # تخمین ساده - در عمل از مدل‌های پیچیده‌تری استفاده می‌شود
        fibonacci_values = [0.382, 0.618, 1.000, 1.618, 2.618]
        
        min_distance = min(abs(ratio - fib) for fib in fibonacci_values)
        density = max(0.1, 1.0 - min_distance)
        
        return density

    def export_analysis_results(self, results: Dict, format: str = 'json') -> str:
        """صادرات نتایج تحلیل"""
        import json
        
        if format.lower() == 'json':
            # تبدیل numpy arrays و سایر اشیاء غیرقابل serialization
            serializable_results = self._make_serializable(results)
            return json.dumps(serializable_results, indent=2, ensure_ascii=False)
        
        elif format.lower() == 'csv':
            # صادرات CSV ساده
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # استخراج نسبت‌های کلیدی
            classic_ratios = results.get('classic_ratios', {})
            for ratio_name, ratio_result in classic_ratios.items():
                if hasattr(ratio_result, 'target_ratio'):
                    writer.writerow([
                        ratio_name,
                        ratio_result.target_ratio,
                        ratio_result.closest_fibonacci.value,
                        ratio_result.confidence_score,
                        ratio_result.is_valid
                    ])
            
            return output.getvalue()
        
        return "فرمت پشتیبانی نشده"
    
    def _make_serializable(self, obj: Any) -> Any:
        """تبدیل اشیاء به فرمت قابل serialization"""
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, dict):
            return {key: self._make_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return self._make_serializable(obj.__dict__)
        else:
            return obj

# اضافه کردن alias برای سازگاری با کد موجود
RatioAnalyzer = AdvancedRatioAnalyzer

# تست کلاس
if __name__ == "__main__":
    # نمونه داده برای تست
    sample_waves = [
        {'length': 100, 'duration': 10, 'price': 50000},
        {'length': 61.8, 'duration': 8, 'price': 51000},
        {'length': 161.8, 'duration': 15, 'price': 49000},
        {'length': 38.2, 'duration': 6, 'price': 52000},
        {'length': 261.8, 'duration': 20, 'price': 48000}
    ]
    
    # ایجاد تحلیلگر پیشرفته
    analyzer = AdvancedRatioAnalyzer(
        waves=sample_waves,
        validation_level=ValidationLevel.MODERATE,
        enable_ml=True,
        enable_statistics=True,
        enable_geometry=True
    )
    
    # انجام تحلیل کامل
    results = analyzer.calculate_advanced_internal_ratios()
    
    print("=== نتایج تحلیل پیشرفته نسبت‌ها ===")
    print(f"تعداد نسبت‌های کلاسیک: {len(results.get('classic_ratios', {}))}")
    print(f"تحلیل آماری: {'✓' if results.get('statistical_analysis') else '✗'}")
    print(f"تحلیل هندسی: {'✓' if results.get('geometric_analysis') else '✗'}")
    
    # تست اعتبارسنجی موج ممتد
    extension_validation = analyzer.calculate_extended_wave_validation(3, strict_validation=True)
    print(f"\nاعتبارسنجی موج ممتد: {extension_validation.get('is_extended', False)}")
    print(f"نسبت امتداد: {extension_validation.get('extension_ratio', 0):.3f}")
    print(f"اطمینان: {extension_validation.get('confidence_score', 0):.3f}")
    
    # تست تحلیل جامع
    comprehensive_analysis = analyzer.calculate_comprehensive_fibonacci_relationship(
        wave1_length=100, 
        wave2_length=161.8, 
        tolerance=0.05,
        include_harmonics=True
    )
    
    basic_analysis = comprehensive_analysis.get('basic_analysis', {})
    print(f"\nتحلیل جامع فیبوناچی:")
    print(f"نسبت هدف: {basic_analysis.get('target_ratio', 0):.3f}")
    print(f"نزدیک‌ترین فیبوناچی: {basic_analysis.get('closest_fibonacci', 0):.3f}")
    print(f"اطمینان: {basic_analysis.get('confidence_score', 0):.3f}")
    
    print("\n=== تحلیل با موفقیت تکمیل شد ===")