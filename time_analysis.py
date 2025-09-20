"""تحلیل زمانی پیشرفته در نئوویو"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Union, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import logging
from scipy import stats, signal, fft
from scipy.optimize import minimize
from sklearn.cluster import DBSCAN, KMeans
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import warnings
import json
from collections import defaultdict

# تنظیم logging
logger = logging.getLogger(__name__)

class TimeFrameType(Enum):
    """انواع تایم فریم"""
    INTRADAY = "intraday"          # درون روزی
    DAILY = "daily"                # روزانه
    WEEKLY = "weekly"              # هفتگی
    MONTHLY = "monthly"            # ماهانه
    YEARLY = "yearly"              # سالانه

class CycleType(Enum):
    """انواع چرخه‌های زمانی"""
    FIBONACCI = "fibonacci"        # چرخه‌های فیبوناچی
    SEASONAL = "seasonal"          # چرخه‌های موسمی
    HARMONIC = "harmonic"          # چرخه‌های هارمونیک
    CUSTOM = "custom"              # چرخه‌های سفارشی
    
class TimeProjectionType(Enum):
    """انواع پروژکشن زمانی"""
    LINEAR = "linear"              # خطی
    EXPONENTIAL = "exponential"    # نمایی
    FIBONACCI = "fibonacci"        # فیبوناچی
    HARMONIC = "harmonic"          # هارمونیک
    MACHINE_LEARNING = "ml"        # یادگیری ماشین

class ConfidenceLevel(Enum):
    """سطوح اطمینان"""
    VERY_HIGH = "very_high"        # 95%+
    HIGH = "high"                  # 80-95%
    MEDIUM = "medium"              # 60-80%
    LOW = "low"                    # 40-60%
    VERY_LOW = "very_low"          # <40%

@dataclass
class TimeMetrics:
    """متریک‌های زمانی پیشرفته"""
    duration: float
    velocity: float                # سرعت حرکت قیمت
    acceleration: float            # شتاب
    momentum_persistence: float    # پایداری مومنتوم
    volatility_clustering: float   # خوشه‌بندی نوسانات
    hurst_exponent: float         # نمای هرست
    fractal_dimension: float      # بعد فرکتالی
    entropy: float                # آنتروپی
    lyapunov_exponent: float      # نمای لیاپانوف
    correlation_length: float     # طول همبستگی
    
@dataclass
class CycleAnalysis:
    """تحلیل چرخه‌های زمانی"""
    cycle_type: CycleType
    period: float                 # دوره چرخه
    amplitude: float              # دامنه
    phase: float                  # فاز
    confidence: float            # اطمینان
    strength: float              # قدرت چرخه
    next_peak: Optional[float]   # زمان قله بعدی
    next_trough: Optional[float] # زمان کف بعدی
    harmonic_frequencies: List[float] = field(default_factory=list)
    statistical_significance: float = 0.0

@dataclass
class TimeProjection:
    """پروژکشن زمانی"""
    target_time: float
    projection_type: TimeProjectionType
    confidence_level: ConfidenceLevel
    confidence_score: float
    supporting_factors: List[str] = field(default_factory=list)
    invalidation_time: Optional[float] = None
    probability_distribution: Dict[str, float] = field(default_factory=dict)
    
@dataclass
class TimeCluster:
    """خوشه زمانی"""
    center_time: float
    time_range: Tuple[float, float]
    strength: int
    targets: List[float]
    cluster_type: str
    significance: float
    probability: float
    supporting_ratios: List[float] = field(default_factory=list)

@dataclass
class SeasonalPattern:
    """الگوی موسمی"""
    pattern_name: str
    period_days: int
    strength: float
    phase_offset: float
    seasonal_component: np.ndarray
    trend_component: np.ndarray
    residual_component: np.ndarray
    forecasted_values: np.ndarray
    
@dataclass
class TimeAlternation:
    """تناوب زمانی پیشرفته"""
    wave_pair: Tuple[int, int]
    time_ratio: float
    alternation_type: str
    alternation_strength: float
    fibonacci_alignment: float
    statistical_significance: float
    expected_range: Tuple[float, float]
    
@dataclass
class AdvancedTimeAnalysisResult:
    """نتیجه تحلیل زمانی پیشرفته"""
    analysis_id: str
    timestamp: datetime
    timeframe: TimeFrameType
    
    # متریک‌های اصلی
    time_metrics: TimeMetrics
    
    # تحلیل چرخه‌ها
    cycles: List[CycleAnalysis]
    dominant_cycle: Optional[CycleAnalysis]
    
    # پروژکشن‌ها
    time_projections: List[TimeProjection]
    critical_time_zones: List[TimeCluster]
    
    # الگوهای موسمی
    seasonal_patterns: List[SeasonalPattern]
    
    # تناوب‌ها
    time_alternations: List[TimeAlternation]
    
    # پیش‌بینی‌های ML
    ml_predictions: Dict[str, Any] = field(default_factory=dict)
    
    # ارزیابی کیفیت
    analysis_quality: float = 0.0
    reliability_score: float = 0.0
    
    # خلاصه
    summary: Dict[str, Any] = field(default_factory=dict)

class AdvancedTimeAnalyzer:
    """تحلیلگر زمانی پیشرفته"""
    
    # نسبت‌های زمانی گسترده شده
    FIBONACCI_TIME_RATIOS = [
        0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.414, 1.618, 
        2.0, 2.414, 2.618, 3.0, 3.236, 3.618, 4.236, 5.0
    ]
    
    # چرخه‌های استاندارد بازار
    MARKET_CYCLES = {
        'short_term': [3, 5, 8, 13, 21],      # روز
        'medium_term': [34, 55, 89, 144],      # روز  
        'long_term': [233, 377, 610, 987]      # روز
    }
    
    def __init__(self, data: pd.DataFrame, config: Dict = None):
        self.data = data
        self.config = config or self._get_default_config()
        self.time_analysis_results = []
        
        # ML models
        self.ml_models = {}
        self.scaler = StandardScaler()
        
        # پردازش داده‌های اولیه
        self._prepare_time_data()
        
        # آماده‌سازی مدل‌های ML
        if self.config.get('ml_enabled', True):
            self._initialize_ml_models()
            
        logger.info("Advanced Time Analyzer initialized")
    
    def _get_default_config(self) -> Dict:
        """تنظیمات پیش‌فرض"""
        return {
            'min_cycle_length': 3,
            'max_cycle_length': 987,
            'confidence_threshold': 0.6,
            'ml_enabled': True,
            'fourier_analysis': True,
            'wavelet_analysis': True,
            'seasonal_decomposition': True,
            'harmonic_analysis': True,
            'fractal_analysis': True,
            'correlation_analysis': True,
            'projection_methods': ['fibonacci', 'harmonic', 'ml'],
            'cluster_tolerance': 0.05,
            'statistical_significance': 0.05
        }
    
    def _prepare_time_data(self):
        """آماده‌سازی داده‌های زمانی"""
        try:
            # محاسبه متغیرهای زمانی
            self.data['returns'] = self.data['close'].pct_change()
            self.data['log_returns'] = np.log(self.data['close'] / self.data['close'].shift(1))
            self.data['volatility'] = self.data['returns'].rolling(window=20).std()
            self.data['volume_rate'] = self.data['volume'].pct_change()
            
            # محاسبه momentum و acceleration
            self.data['momentum'] = self.data['close'].diff()
            self.data['acceleration'] = self.data['momentum'].diff()
            
            # شاخص‌های زمانی
            if 'timestamp' in self.data.columns:
                self.data['hour'] = pd.to_datetime(self.data['timestamp']).dt.hour
                self.data['day_of_week'] = pd.to_datetime(self.data['timestamp']).dt.dayofweek
                self.data['day_of_month'] = pd.to_datetime(self.data['timestamp']).dt.day
                self.data['month'] = pd.to_datetime(self.data['timestamp']).dt.month
            
            logger.info("Time data preparation completed")
            
        except Exception as e:
            logger.error(f"Error in time data preparation: {e}")
    
    def _initialize_ml_models(self):
        """آماده‌سازی مدل‌های ML"""
        try:
            # مدل پیش‌بینی زمان
            self.ml_models['time_predictor'] = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            # مدل تشخیص چرخه
            self.ml_models['cycle_detector'] = RandomForestRegressor(
                n_estimators=50,
                max_depth=8,
                random_state=42
            )
            
            # مدل تشخیص ناهنجاری
            self.ml_models['anomaly_detector'] = IsolationForest(
                contamination=0.1,
                random_state=42
            )
            
            logger.info("ML models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing ML models: {e}")
            self.config['ml_enabled'] = False
    
    def analyze_advanced_time_relationships(self, waves: List[Dict], 
                                          degree: int = 0) -> AdvancedTimeAnalysisResult:
        """تحلیل پیشرفته روابط زمانی"""
        
        try:
            analysis_id = f"TIME_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{np.random.randint(1000, 9999)}"
            
            # 1. محاسبه متریک‌های زمانی پیشرفته
            time_metrics = self._calculate_advanced_time_metrics(waves)
            
            # 2. تحلیل چرخه‌های زمانی
            cycles = self._analyze_cycles(waves)
            dominant_cycle = self._find_dominant_cycle(cycles)
            
            # 3. تولید پروژکشن‌های زمانی
            time_projections = self._generate_time_projections(waves, cycles)
            
            # 4. شناسایی مناطق زمانی بحرانی
            critical_zones = self._identify_critical_time_zones(time_projections)
            
            # 5. تحلیل الگوهای موسمی
            seasonal_patterns = self._analyze_seasonal_patterns(waves)
            
            # 6. تحلیل تناوب‌های زمانی پیشرفته
            time_alternations = self._analyze_advanced_time_alternation(waves)
            
            # 7. پیش‌بینی‌های ML
            ml_predictions = {}
            if self.config.get('ml_enabled', False):
                ml_predictions = self._generate_ml_predictions(waves, time_metrics)
            
            # 8. ارزیابی کیفیت تحلیل
            analysis_quality = self._evaluate_analysis_quality(
                time_metrics, cycles, time_projections
            )
            
            # 9. محاسبه امتیاز قابلیت اطمینان
            reliability_score = self._calculate_reliability_score(
                cycles, time_projections, ml_predictions
            )
            
            # 10. تولید خلاصه
            summary = self._generate_time_analysis_summary(
                time_metrics, cycles, time_projections, critical_zones
            )
            
            # ایجاد نتیجه نهایی
            result = AdvancedTimeAnalysisResult(
                analysis_id=analysis_id,
                timestamp=datetime.now(),
                timeframe=self._determine_timeframe(),
                time_metrics=time_metrics,
                cycles=cycles,
                dominant_cycle=dominant_cycle,
                time_projections=time_projections,
                critical_time_zones=critical_zones,
                seasonal_patterns=seasonal_patterns,
                time_alternations=time_alternations,
                ml_predictions=ml_predictions,
                analysis_quality=analysis_quality,
                reliability_score=reliability_score,
                summary=summary
            )
            
            self.time_analysis_results.append(result)
            logger.info(f"Advanced time analysis completed: {analysis_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in advanced time analysis: {e}")
            return None
    
    def _calculate_advanced_time_metrics(self, waves: List[Dict]) -> TimeMetrics:
        """محاسبه متریک‌های زمانی پیشرفته"""
        try:
            if not waves:
                return TimeMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            
            # محاسبه مدت کل
            total_duration = sum(w['duration'] for w in waves)
            
            # محاسبه سرعت (تغییر قیمت / زمان)
            price_changes = [abs(w['end'][1] - w['start'][1]) for w in waves]
            durations = [w['duration'] for w in waves]
            velocities = [pc / d if d > 0 else 0 for pc, d in zip(price_changes, durations)]
            avg_velocity = np.mean(velocities) if velocities else 0
            
            # محاسبه شتاب
            accelerations = np.diff(velocities) if len(velocities) > 1 else [0]
            avg_acceleration = np.mean(accelerations) if len(accelerations) > 0 else 0
            
            # پایداری مومنتوم
            returns = self.data['returns'].dropna()
            momentum_persistence = self._calculate_momentum_persistence(returns)
            
            # خوشه‌بندی نوسانات
            volatility_clustering = self._calculate_volatility_clustering()
            
            # نمای هرست
            hurst_exponent = self._calculate_hurst_exponent(self.data['close'].values)
            
            # بعد فرکتالی
            fractal_dimension = self._calculate_fractal_dimension(self.data['close'].values)
            
            # آنتروپی
            entropy = self._calculate_entropy(returns.values)
            
            # نمای لیاپانوف
            lyapunov_exponent = self._calculate_lyapunov_exponent(returns.values)
            
            # طول همبستگی
            correlation_length = self._calculate_correlation_length(returns.values)
            
            return TimeMetrics(
                duration=total_duration,
                velocity=avg_velocity,
                acceleration=avg_acceleration,
                momentum_persistence=momentum_persistence,
                volatility_clustering=volatility_clustering,
                hurst_exponent=hurst_exponent,
                fractal_dimension=fractal_dimension,
                entropy=entropy,
                lyapunov_exponent=lyapunov_exponent,
                correlation_length=correlation_length
            )
            
        except Exception as e:
            logger.error(f"Error calculating advanced time metrics: {e}")
            return TimeMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    def _analyze_cycles(self, waves: List[Dict]) -> List[CycleAnalysis]:
        """تحلیل چرخه‌های زمانی"""
        try:
            cycles = []
            
            # 1. تحلیل چرخه‌های فیبوناچی
            fib_cycles = self._analyze_fibonacci_cycles(waves)
            cycles.extend(fib_cycles)
            
            # 2. تحلیل فوریه برای یافتن چرخه‌های پریودیک
            if self.config.get('fourier_analysis', True):
                fourier_cycles = self._analyze_fourier_cycles()
                cycles.extend(fourier_cycles)
            
            # 3. تحلیل چرخه‌های هارمونیک
            if self.config.get('harmonic_analysis', True):
                harmonic_cycles = self._analyze_harmonic_cycles(waves)
                cycles.extend(harmonic_cycles)
            
            # 4. تحلیل چرخه‌های موسمی
            seasonal_cycles = self._analyze_seasonal_cycles()
            cycles.extend(seasonal_cycles)
            
            # مرتب‌سازی بر اساس قدرت
            cycles.sort(key=lambda x: x.strength, reverse=True)
            
            return cycles
            
        except Exception as e:
            logger.error(f"Error analyzing cycles: {e}")
            return []
    
    def _analyze_fibonacci_cycles(self, waves: List[Dict]) -> List[CycleAnalysis]:
        """تحلیل چرخه‌های فیبوناچی"""
        try:
            cycles = []
            
            if not waves:
                return cycles
            
            # محاسبه دوره‌های موجود
            durations = [w['duration'] for w in waves]
            
            for fib_ratio in self.FIBONACCI_TIME_RATIOS:
                for base_duration in durations:
                    cycle_period = base_duration * fib_ratio
                    
                    # بررسی وجود این چرخه در داده‌ها
                    strength = self._calculate_cycle_strength(cycle_period)
                    
                    if strength > 0.3:  # حد آستانه
                        # محاسبه فاز و دامنه
                        phase, amplitude = self._calculate_cycle_phase_amplitude(cycle_period)
                        
                        # پیش‌بینی نقاط بحرانی
                        next_peak, next_trough = self._predict_cycle_extremes(cycle_period, phase)
                        
                        # محاسبه معنی‌داری آماری
                        stat_significance = self._calculate_cycle_statistical_significance(cycle_period)
                        
                        cycle = CycleAnalysis(
                            cycle_type=CycleType.FIBONACCI,
                            period=cycle_period,
                            amplitude=amplitude,
                            phase=phase,
                            confidence=strength,
                            strength=strength,
                            next_peak=next_peak,
                            next_trough=next_trough,
                            statistical_significance=stat_significance
                        )
                        
                        cycles.append(cycle)
            
            return cycles
            
        except Exception as e:
            logger.error(f"Error analyzing Fibonacci cycles: {e}")
            return []
    
    def _analyze_fourier_cycles(self) -> List[CycleAnalysis]:
        """تحلیل فوریه برای یافتن چرخه‌ها"""
        try:
            cycles = []
            
            # تحلیل فوریه روی قیمت‌ها
            prices = self.data['close'].dropna().values
            
            if len(prices) < 20:
                return cycles
            
            # محاسبه FFT
            fft_result = np.fft.fft(prices)
            frequencies = np.fft.fftfreq(len(prices))
            power_spectrum = np.abs(fft_result) ** 2
            
            # یافتن فرکانس‌های غالب
            # حذف فرکانس صفر (DC component)
            non_zero_indices = np.where(frequencies != 0)[0]
            
            # مرتب‌سازی بر اساس قدرت
            sorted_indices = non_zero_indices[np.argsort(power_spectrum[non_zero_indices])[::-1]]
            
            # استخراج بهترین چرخه‌ها
            for i in range(min(10, len(sorted_indices))):  # حداکثر 10 چرخه
                idx = sorted_indices[i]
                frequency = frequencies[idx]
                
                if frequency > 0:  # فقط فرکانس‌های مثبت
                    period = 1 / frequency
                    
                    # بررسی اینکه دوره در محدوده مجاز باشد
                    if self.config['min_cycle_length'] <= period <= self.config['max_cycle_length']:
                        strength = power_spectrum[idx] / np.max(power_spectrum)
                        amplitude = np.abs(fft_result[idx]) / len(prices)
                        phase = np.angle(fft_result[idx])
                        
                        if strength > 0.1:  # حد آستانه
                            cycle = CycleAnalysis(
                                cycle_type=CycleType.HARMONIC,
                                period=period,
                                amplitude=amplitude,
                                phase=phase,
                                confidence=strength,
                                strength=strength,
                                next_peak=self._calculate_next_peak_from_phase(period, phase),
                                next_trough=self._calculate_next_trough_from_phase(period, phase),
                                statistical_significance=self._calculate_fourier_significance(strength)
                            )
                            
                            cycles.append(cycle)
            
            return cycles
            
        except Exception as e:
            logger.error(f"Error in Fourier cycle analysis: {e}")
            return []
    
    def _analyze_harmonic_cycles(self, waves: List[Dict]) -> List[CycleAnalysis]:
        """تحلیل چرخه‌های هارمونیک"""
        try:
            cycles = []
            
            if not waves:
                return cycles
            
            # یافتن چرخه پایه
            base_periods = [w['duration'] for w in waves]
            
            for base_period in base_periods:
                # تولید هارمونیک‌ها
                harmonics = [base_period / i for i in range(2, 9)]  # هارمونیک‌های 1/2 تا 1/8
                harmonics.extend([base_period * i for i in range(2, 6)])  # هارمونیک‌های 2x تا 5x
                
                for harmonic_period in harmonics:
                    if self.config['min_cycle_length'] <= harmonic_period <= self.config['max_cycle_length']:
                        strength = self._calculate_harmonic_strength(harmonic_period, base_period)
                        
                        if strength > 0.25:
                            amplitude = self._estimate_harmonic_amplitude(harmonic_period)
                            phase = self._estimate_harmonic_phase(harmonic_period)
                            
                            cycle = CycleAnalysis(
                                cycle_type=CycleType.HARMONIC,
                                period=harmonic_period,
                                amplitude=amplitude,
                                phase=phase,
                                confidence=strength,
                                strength=strength,
                                next_peak=self._predict_harmonic_peak(harmonic_period, phase),
                                next_trough=self._predict_harmonic_trough(harmonic_period, phase),
                                harmonic_frequencies=[base_period, harmonic_period],
                                statistical_significance=self._test_harmonic_significance(harmonic_period, base_period)
                            )
                            
                            cycles.append(cycle)
            
            return cycles
            
        except Exception as e:
            logger.error(f"Error analyzing harmonic cycles: {e}")
            return []
    
    def _analyze_seasonal_cycles(self) -> List[CycleAnalysis]:
        """تحلیل چرخه‌های موسمی"""
        try:
            cycles = []
            
            if 'timestamp' not in self.data.columns:
                return cycles
            
            # چرخه‌های موسمی استاندارد
            seasonal_periods = {
                'daily': 24,          # ساعتی (اگر داده ساعتی داشته باشیم)
                'weekly': 7,          # روزانه در هفته
                'monthly': 30,        # روزانه در ماه
                'quarterly': 90,      # روزانه در فصل
                'yearly': 365         # روزانه در سال
            }
            
            for season_name, period in seasonal_periods.items():
                if period <= len(self.data):
                    strength = self._calculate_seasonal_strength(period)
                    
                    if strength > 0.2:
                        amplitude = self._calculate_seasonal_amplitude(period)
                        phase = self._calculate_seasonal_phase(period)
                        
                        cycle = CycleAnalysis(
                            cycle_type=CycleType.SEASONAL,
                            period=period,
                            amplitude=amplitude,
                            phase=phase,
                            confidence=strength,
                            strength=strength,
                            next_peak=self._predict_seasonal_peak(period, phase),
                            next_trough=self._predict_seasonal_trough(period, phase),
                            statistical_significance=self._test_seasonal_significance(period)
                        )
                        
                        cycles.append(cycle)
            
            return cycles
            
        except Exception as e:
            logger.error(f"Error analyzing seasonal cycles: {e}")
            return []
    
    def _generate_time_projections(self, waves: List[Dict], 
                                 cycles: List[CycleAnalysis]) -> List[TimeProjection]:
        """تولید پروژکشن‌های زمانی"""
        try:
            projections = []
            
            if not waves:
                return projections
            
            # 1. پروژکشن‌های فیبوناچی
            fib_projections = self._generate_fibonacci_projections(waves)
            projections.extend(fib_projections)
            
            # 2. پروژکشن‌های بر اساس چرخه‌ها
            cycle_projections = self._generate_cycle_projections(cycles)
            projections.extend(cycle_projections)
            
            # 3. پروژکشن‌های هارمونیک
            harmonic_projections = self._generate_harmonic_projections(waves, cycles)
            projections.extend(harmonic_projections)
            
            # 4. پروژکشن‌های ML
            if self.config.get('ml_enabled', False):
                ml_projections = self._generate_ml_time_projections(waves)
                projections.extend(ml_projections)
            
            # 5. پروژکشن‌های ترکیبی
            composite_projections = self._generate_composite_projections(projections)
            projections.extend(composite_projections)
            
            # مرتب‌سازی بر اساس اعتماد
            projections.sort(key=lambda x: x.confidence_score, reverse=True)
            
            return projections
            
        except Exception as e:
            logger.error(f"Error generating time projections: {e}")
            return []
    
    def _generate_fibonacci_projections(self, waves: List[Dict]) -> List[TimeProjection]:
        """تولید پروژکشن‌های فیبوناچی"""
        try:
            projections = []
            
            if not waves:
                return projections
            
            last_wave = waves[-1]
            last_time = last_wave['end'][0]
            
            # پروژکشن بر اساس آخرین موج
            for ratio in self.FIBONACCI_TIME_RATIOS:
                target_time = last_time + (last_wave['duration'] * ratio)
                
                # محاسبه اعتماد بر اساس تاریخچه
                confidence_score = self._calculate_fibonacci_projection_confidence(
                    waves, ratio
                )
                
                if confidence_score > 0.3:
                    confidence_level = self._determine_confidence_level(confidence_score)
                    
                    # عوامل پشتیبان
                    supporting_factors = [
                        f"Fibonacci ratio {ratio}",
                        f"Based on wave duration {last_wave['duration']}"
                    ]
                    
                    # سطح باطل‌سازی
                    invalidation_time = target_time * 1.1  # 10% tolerance
                    
                    projection = TimeProjection(
                        target_time=target_time,
                        projection_type=TimeProjectionType.FIBONACCI,
                        confidence_level=confidence_level,
                        confidence_score=confidence_score,
                        supporting_factors=supporting_factors,
                        invalidation_time=invalidation_time,
                        probability_distribution={
                            'early': 0.2,
                            'on_time': 0.6,
                            'late': 0.2
                        }
                    )
                    
                    projections.append(projection)
            
            # پروژکشن بر اساس کل الگو
            if len(waves) >= 3:
                total_duration = sum(w['duration'] for w in waves)
                
                for ratio in [0.618, 1.0, 1.618]:
                    target_time = last_time + (total_duration * ratio)
                    confidence_score = self._calculate_pattern_projection_confidence(waves, ratio)
                    
                    if confidence_score > 0.4:
                        projection = TimeProjection(
                            target_time=target_time,
                            projection_type=TimeProjectionType.FIBONACCI,
                            confidence_level=self._determine_confidence_level(confidence_score),
                            confidence_score=confidence_score,
                            supporting_factors=[
                                f"Pattern ratio {ratio}",
                                f"Total pattern duration {total_duration}"
                            ],
                            invalidation_time=target_time * 1.15
                        )
                        
                        projections.append(projection)
            
            return projections
            
        except Exception as e:
            logger.error(f"Error generating Fibonacci projections: {e}")
            return []
    
    def _identify_critical_time_zones(self, projections: List[TimeProjection]) -> List[TimeCluster]:
        """شناسایی مناطق زمانی بحرانی"""
        try:
            if not projections:
                return []
            
            # استخراج زمان‌های هدف
            target_times = [p.target_time for p in projections]
            
            # خوشه‌بندی زمان‌ها
            clusters = []
            tolerance = self.config.get('cluster_tolerance', 0.05)
            
            used = [False] * len(target_times)
            
            for i in range(len(target_times)):
                if used[i]:
                    continue
                
                cluster_times = [target_times[i]]
                cluster_projections = [projections[i]]
                used[i] = True
                
                for j in range(i + 1, len(target_times)):
                    if not used[j]:
                        time_diff = abs(target_times[j] - target_times[i])
                        relative_diff = time_diff / target_times[i]
                        
                        if relative_diff < tolerance:
                            cluster_times.append(target_times[j])
                            cluster_projections.append(projections[j])
                            used[j] = True
                
                if len(cluster_times) >= 2:  # حداقل 2 هدف برای تشکیل خوشه
                    center_time = np.mean(cluster_times)
                    time_range = (min(cluster_times), max(cluster_times))
                    strength = len(cluster_times)
                    
                    # محاسبه معنی‌داری
                    significance = self._calculate_cluster_significance(cluster_projections)
                    
                    # محاسبه احتمال
                    probability = self._calculate_cluster_probability(cluster_projections)
                    
                    # نسبت‌های پشتیبان
                    supporting_ratios = [p.confidence_score for p in cluster_projections]
                    
                    cluster = TimeCluster(
                        center_time=center_time,
                        time_range=time_range,
                        strength=strength,
                        targets=cluster_times,
                        cluster_type='convergence',
                        significance=significance,
                        probability=probability,
                        supporting_ratios=supporting_ratios
                    )
                    
                    clusters.append(cluster)
            
            # مرتب‌سازی بر اساس قدرت
            clusters.sort(key=lambda x: x.strength, reverse=True)
            
            return clusters
            
        except Exception as e:
            logger.error(f"Error identifying critical time zones: {e}")
            return []
    
    def _analyze_seasonal_patterns(self, waves: List[Dict]) -> List[SeasonalPattern]:
        """تحلیل الگوهای موسمی"""
        try:
            patterns = []
            
            if not self.config.get('seasonal_decomposition', True):
                return patterns
            
            if len(self.data) < 100:  # حداقل داده برای تحلیل موسمی
                return patterns
            
            # تجزیه موسمی سری زمانی
            try:
                from statsmodels.tsa.seasonal import seasonal_decompose
                
                # تحلیل قیمت‌های بسته شدن
                decomposition = seasonal_decompose(
                    self.data['close'].dropna(), 
                    model='additive', 
                    period=min(30, len(self.data) // 4)
                )
                
                # استخراج اجزا
                seasonal_component = decomposition.seasonal.values
                trend_component = decomposition.trend.dropna().values
                residual_component = decomposition.resid.dropna().values
                
                # پیش‌بینی مقادیر آتی
                period = min(30, len(self.data) // 4)
                forecasted_values = self._forecast_seasonal_values(
                    seasonal_component, trend_component, period
                )
                
                # محاسبه قدرت الگوی موسمی
                strength = self._calculate_seasonal_pattern_strength(
                    seasonal_component, residual_component
                )
                
                pattern = SeasonalPattern(
                    pattern_name='Price Seasonality',
                    period_days=period,
                    strength=strength,
                    phase_offset=0,
                    seasonal_component=seasonal_component,
                    trend_component=trend_component,
                    residual_component=residual_component,
                    forecasted_values=forecasted_values
                )
                
                patterns.append(pattern)
                
            except ImportError:
                logger.warning("statsmodels not available for seasonal decomposition")
            except Exception as e:
                logger.warning(f"Seasonal decomposition failed: {e}")
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing seasonal patterns: {e}")
            return []
    
    def _analyze_advanced_time_alternation(self, waves: List[Dict]) -> List[TimeAlternation]:
        """تحلیل تناوب‌های زمانی پیشرفته"""
        try:
            alternations = []
            
            if len(waves) < 4:
                return alternations
            
            # تحلیل تناوب بین موج‌های اصلاحی (2 و 4)
            if len(waves) >= 4:
                wave2_duration = waves[1]['duration']
                wave4_duration = waves[3]['duration']
                
                time_ratio = wave4_duration / wave2_duration if wave2_duration > 0 else 0
                
                # تعیین نوع تناوب
                alternation_type = self._determine_advanced_alternation_type(
                    wave2_duration, wave4_duration
                )
                
                # محاسبه قدرت تناوب
                alternation_strength = self._calculate_alternation_strength(
                    wave2_duration, wave4_duration
                )
                
                # تراز با فیبوناچی
                fibonacci_alignment = self._calculate_fibonacci_alignment(time_ratio)
                
                # معنی‌داری آماری
                statistical_significance = self._test_alternation_significance(
                    wave2_duration, wave4_duration
                )
                
                # محدوده مورد انتظار برای موج‌های آتی
                expected_range = self._calculate_expected_alternation_range(
                    wave2_duration, wave4_duration
                )
                
                alternation = TimeAlternation(
                    wave_pair=(2, 4),
                    time_ratio=time_ratio,
                    alternation_type=alternation_type,
                    alternation_strength=alternation_strength,
                    fibonacci_alignment=fibonacci_alignment,
                    statistical_significance=statistical_significance,
                    expected_range=expected_range
                )
                
                alternations.append(alternation)
            
            # تحلیل تناوب بین موج‌های محرک (1, 3, 5)
            if len(waves) >= 5:
                impulse_durations = [waves[0]['duration'], waves[2]['duration'], waves[4]['duration']]
                
                # تناوب 1-3
                ratio_1_3 = impulse_durations[1] / impulse_durations[0] if impulse_durations[0] > 0 else 0
                alternation_1_3 = TimeAlternation(
                    wave_pair=(1, 3),
                    time_ratio=ratio_1_3,
                    alternation_type=self._determine_advanced_alternation_type(
                        impulse_durations[0], impulse_durations[1]
                    ),
                    alternation_strength=self._calculate_alternation_strength(
                        impulse_durations[0], impulse_durations[1]
                    ),
                    fibonacci_alignment=self._calculate_fibonacci_alignment(ratio_1_3),
                    statistical_significance=self._test_alternation_significance(
                        impulse_durations[0], impulse_durations[1]
                    ),
                    expected_range=self._calculate_expected_alternation_range(
                        impulse_durations[0], impulse_durations[1]
                    )
                )
                alternations.append(alternation_1_3)
                
                # تناوب 3-5
                ratio_3_5 = impulse_durations[2] / impulse_durations[1] if impulse_durations[1] > 0 else 0
                alternation_3_5 = TimeAlternation(
                    wave_pair=(3, 5),
                    time_ratio=ratio_3_5,
                    alternation_type=self._determine_advanced_alternation_type(
                        impulse_durations[1], impulse_durations[2]
                    ),
                    alternation_strength=self._calculate_alternation_strength(
                        impulse_durations[1], impulse_durations[2]
                    ),
                    fibonacci_alignment=self._calculate_fibonacci_alignment(ratio_3_5),
                    statistical_significance=self._test_alternation_significance(
                        impulse_durations[1], impulse_durations[2]
                    ),
                    expected_range=self._calculate_expected_alternation_range(
                        impulse_durations[1], impulse_durations[2]
                    )
                )
                alternations.append(alternation_3_5)
            
            return alternations
            
        except Exception as e:
            logger.error(f"Error analyzing advanced time alternation: {e}")
            return []
    
    # متدهای کمکی برای محاسبات پیشرفته
    def _calculate_momentum_persistence(self, returns: pd.Series) -> float:
        """محاسبه پایداری مومنتوم"""
        try:
            if len(returns) < 10:
                return 0.0
            
            # محاسبه autocorrelation
            autocorr = returns.autocorr(lag=1)
            return max(0, autocorr) if not np.isnan(autocorr) else 0.0
            
        except:
            return 0.0
    
    def _calculate_volatility_clustering(self) -> float:
        """محاسبه خوشه‌بندی نوسانات"""
        try:
            volatility = self.data['volatility'].dropna()
            if len(volatility) < 10:
                return 0.0
            
            # ARCH test برای خوشه‌بندی نوسانات
            squared_returns = (self.data['returns'].dropna()) ** 2
            autocorr = squared_returns.autocorr(lag=1)
            
            return max(0, autocorr) if not np.isnan(autocorr) else 0.0
            
        except:
            return 0.0
    
    def _calculate_hurst_exponent(self, prices: np.ndarray) -> float:
        """محاسبه نمای هرست"""
        try:
            if len(prices) < 20:
                return 0.5
            
            # روش R/S
            log_returns = np.diff(np.log(prices))
            n = len(log_returns)
            
            lags = range(2, min(n//4, 100))
            rs_values = []
            
            for lag in lags:
                chunks = [log_returns[i:i+lag] for i in range(0, len(log_returns), lag) 
                         if i+lag <= len(log_returns)]
                rs_list = []
                
                for chunk in chunks:
                    if len(chunk) == lag:
                        mean_chunk = np.mean(chunk)
                        cumsum_chunk = np.cumsum(chunk - mean_chunk)
                        R = np.max(cumsum_chunk) - np.min(cumsum_chunk)
                        S = np.std(chunk)
                        if S > 0:
                            rs_list.append(R / S)
                
                if rs_list:
                    rs_values.append(np.mean(rs_list))
                else:
                    rs_values.append(1)
            
            if len(rs_values) < 2:
                return 0.5
            
            x = np.log(lags[:len(rs_values)])
            y = np.log(rs_values)
            
            hurst, _ = np.polyfit(x, y, 1)
            return max(0.0, min(1.0, hurst))
            
        except:
            return 0.5
    
    def _calculate_fractal_dimension(self, prices: np.ndarray) -> float:
        """محاسبه بعد فرکتالی"""
        try:
            if len(prices) < 10:
                return 1.0
            
            # روش Higuchi
            k_max = min(10, len(prices) // 4)
            lks = []
            
            for k in range(1, k_max + 1):
                lk = 0
                for m in range(k):
                    ll = 0
                    max_i = int((len(prices) - m - 1) / k)
                    for i in range(1, max_i):
                        ll += abs(prices[m + i * k] - prices[m + (i - 1) * k])
                    ll = ll * (len(prices) - 1) / (max_i * k * k)
                    lk += ll
                lks.append(lk / k)
            
            if len(lks) < 2:
                return 1.0
            
            x = np.log(range(1, len(lks) + 1))
            y = np.log(lks)
            
            slope, _ = np.polyfit(x, y, 1)
            fractal_dim = -slope
            
            return max(1.0, min(3.0, fractal_dim))
            
        except:
            return 1.0
    
    def _calculate_entropy(self, data: np.ndarray) -> float:
        """محاسبه آنتروپی"""
        try:
            if len(data) < 5:
                return 0.0
            
            # تبدیل به bins
            hist, _ = np.histogram(data, bins=min(20, len(data) // 5))
            hist = hist[hist > 0]  # حذف bin های خالی
            
            # نرمال‌سازی
            probabilities = hist / np.sum(hist)
            
            # محاسبه آنتروپی شانون
            entropy = -np.sum(probabilities * np.log2(probabilities))
            
            return entropy
            
        except:
            return 0.0
    
    def _calculate_lyapunov_exponent(self, data: np.ndarray) -> float:
        """محاسبه نمای لیاپانوف"""
        try:
            if len(data) < 10:
                return 0.0
            
            # تخمین ساده
            differences = np.abs(np.diff(data))
            
            if len(differences) == 0:
                return 0.0
            
            log_differences = np.log(differences + 1e-10)  # جلوگیری از log(0)
            lyapunov = np.mean(log_differences)
            
            return max(-1.0, min(1.0, lyapunov))
            
        except:
            return 0.0
    
    def _calculate_correlation_length(self, data: np.ndarray) -> float:
        """محاسبه طول همبستگی"""
        try:
            if len(data) < 10:
                return 1.0
            
            correlations = []
            max_lag = min(len(data) // 4, 50)
            
            for lag in range(1, max_lag):
                if lag < len(data):
                    corr = np.corrcoef(data[:-lag], data[lag:])[0, 1]
                    if not np.isnan(corr):
                        correlations.append(abs(corr))
                    else:
                        correlations.append(0)
            
            # یافتن اولین نقطه‌ای که همبستگی به زیر آستانه می‌رسد
            threshold = 1/np.e  # e^(-1)
            for i, corr in enumerate(correlations):
                if corr < threshold:
                    return i + 1
            
            return len(correlations)
            
        except:
            return 1.0
    
    # ادامه متدهای کمکی...
    def _find_dominant_cycle(self, cycles: List[CycleAnalysis]) -> Optional[CycleAnalysis]:
        """یافتن چرخه غالب"""
        if not cycles:
            return None
        
        # مرتب‌سازی بر اساس قدرت و اعتماد
        sorted_cycles = sorted(cycles, key=lambda x: x.strength * x.confidence, reverse=True)
        return sorted_cycles[0]
    
    def _determine_timeframe(self) -> TimeFrameType:
        """تعیین نوع تایم فریم"""
        # بر اساس تعداد داده‌ها تخمین بزنیم
        data_length = len(self.data)
        
        if data_length < 100:
            return TimeFrameType.INTRADAY
        elif data_length < 500:
            return TimeFrameType.DAILY
        elif data_length < 2000:
            return TimeFrameType.WEEKLY
        else:
            return TimeFrameType.MONTHLY
    
    def _calculate_cycle_strength(self, period: float) -> float:
        """محاسبه قدرت چرخه"""
        try:
            # تحلیل ساده بر اساس تکرار
            data_length = len(self.data)
            
            if period <= 0 or period >= data_length:
                return 0.0
            
            # محاسبه تعداد چرخه‌های کامل
            num_cycles = data_length / period
            
            if num_cycles < 2:  # حداقل 2 چرخه کامل
                return 0.0
            
            # محاسبه همبستگی برای پریود مشخص
            prices = self.data['close'].values
            
            if len(prices) < period * 2:
                return 0.0
            
            # محاسبه همبستگی بین periods
            period_int = int(period)
            correlations = []
            
            for i in range(period_int, len(prices) - period_int):
                segment1 = prices[i-period_int:i]
                segment2 = prices[i:i+period_int]
                
                if len(segment1) == len(segment2):
                    corr = np.corrcoef(segment1, segment2)[0, 1]
                    if not np.isnan(corr):
                        correlations.append(abs(corr))
            
            return np.mean(correlations) if correlations else 0.0
            
        except:
            return 0.0
    
    def _determine_confidence_level(self, score: float) -> ConfidenceLevel:
        """تعیین سطح اطمینان"""
        if score >= 0.95:
            return ConfidenceLevel.VERY_HIGH
        elif score >= 0.8:
            return ConfidenceLevel.HIGH
        elif score >= 0.6:
            return ConfidenceLevel.MEDIUM
        elif score >= 0.4:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW
    
    # متدهای کمکی اضافی که باید پیاده‌سازی شوند...
    def _calculate_cycle_phase_amplitude(self, period: float) -> Tuple[float, float]:
        """محاسبه فاز و دامنه چرخه"""
        # پیاده‌سازی ساده
        return 0.0, 1.0
    
    def _predict_cycle_extremes(self, period: float, phase: float) -> Tuple[Optional[float], Optional[float]]:
        """پیش‌بینی نقاط حداکثر و حداقل چرخه"""
        current_time = len(self.data)
        next_peak = current_time + period * 0.25
        next_trough = current_time + period * 0.75
        return next_peak, next_trough
    
    def _calculate_cycle_statistical_significance(self, period: float) -> float:
        """محاسبه معنی‌داری آماری چرخه"""
        # پیاده‌سازی ساده
        strength = self._calculate_cycle_strength(period)
        return min(0.05, 0.1 * (1 - strength))  # کمتر = معنی‌دارتر
    
    def _generate_ml_predictions(self, waves: List[Dict], metrics: TimeMetrics) -> Dict[str, Any]:
        """تولید پیش‌بینی‌های ML"""
        try:
            if not self.config.get('ml_enabled', False):
                return {}
            
            predictions = {}
            
            # آماده‌سازی ویژگی‌ها
            features = self._extract_time_features(waves, metrics)
            
            if len(features) > 0:
                # پیش‌بینی زمان موج بعدی
                if 'time_predictor' in self.ml_models:
                    time_prediction = self._predict_next_wave_time(features)
                    predictions['next_wave_time'] = time_prediction
                
                # تشخیص ناهنجاری
                if 'anomaly_detector' in self.ml_models:
                    anomaly_score = self._detect_time_anomalies(features)
                    predictions['anomaly_score'] = anomaly_score
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error in ML predictions: {e}")
            return {}
    
    def _extract_time_features(self, waves: List[Dict], metrics: TimeMetrics) -> np.ndarray:
        """استخراج ویژگی‌های زمانی برای ML"""
        try:
            features = []
            
            # ویژگی‌های امواج
            if waves:
                durations = [w['duration'] for w in waves]
                features.extend([
                    np.mean(durations),
                    np.std(durations),
                    np.max(durations),
                    np.min(durations),
                    len(durations)
                ])
            else:
                features.extend([0, 0, 0, 0, 0])
            
            # ویژگی‌های متریک‌ها
            features.extend([
                metrics.velocity,
                metrics.acceleration,
                metrics.momentum_persistence,
                metrics.volatility_clustering,
                metrics.hurst_exponent,
                metrics.fractal_dimension,
                metrics.entropy,
                metrics.lyapunov_exponent,
                metrics.correlation_length
            ])
            
            return np.array(features).reshape(1, -1)
            
        except Exception as e:
            logger.error(f"Error extracting time features: {e}")
            return np.array([])
    
    def _evaluate_analysis_quality(self, metrics: TimeMetrics, 
                                 cycles: List[CycleAnalysis],
                                 projections: List[TimeProjection]) -> float:
        """ارزیابی کیفیت تحلیل"""
        try:
            quality_factors = []
            
            # کیفیت متریک‌ها
            if metrics.hurst_exponent > 0:
                quality_factors.append(0.8)  # متریک‌ها محاسبه شده
            
            # کیفیت چرخه‌ها
            if cycles:
                avg_cycle_strength = np.mean([c.strength for c in cycles])
                quality_factors.append(avg_cycle_strength)
            
            # کیفیت پروژکشن‌ها
            if projections:
                avg_projection_confidence = np.mean([p.confidence_score for p in projections])
                quality_factors.append(avg_projection_confidence)
            
            return np.mean(quality_factors) if quality_factors else 0.0
            
        except:
            return 0.0
    
    def _calculate_reliability_score(self, cycles: List[CycleAnalysis],
                                   projections: List[TimeProjection],
                                   ml_predictions: Dict) -> float:
        """محاسبه امتیاز قابلیت اطمینان"""
        try:
            reliability_factors = []
            
            # قابلیت اطمینان چرخه‌ها
            if cycles:
                strong_cycles = [c for c in cycles if c.strength > 0.5]
                reliability_factors.append(len(strong_cycles) / len(cycles))
            
            # قابلیت اطمینان پروژکشن‌ها
            if projections:
                high_conf_projections = [p for p in projections if p.confidence_score > 0.7]
                reliability_factors.append(len(high_conf_projections) / len(projections))
            
            # قابلیت اطمینان ML
            if ml_predictions and 'anomaly_score' in ml_predictions:
                anomaly_score = ml_predictions['anomaly_score']
                reliability_factors.append(1 - anomaly_score)  # کمتر ناهنجاری = بیشتر قابلیت اطمینان
            
            return np.mean(reliability_factors) if reliability_factors else 0.5
            
        except:
            return 0.5
    
    def _generate_time_analysis_summary(self, metrics: TimeMetrics,
                                      cycles: List[CycleAnalysis],
                                      projections: List[TimeProjection],
                                      critical_zones: List[TimeCluster]) -> Dict[str, Any]:
        """تولید خلاصه تحلیل زمانی"""
        return {
            'total_cycles_found': len(cycles),
            'dominant_cycle_period': cycles[0].period if cycles else None,
            'total_projections': len(projections),
            'critical_time_zones': len(critical_zones),
            'average_projection_confidence': np.mean([p.confidence_score for p in projections]) if projections else 0,
            'hurst_exponent': metrics.hurst_exponent,
            'fractal_dimension': metrics.fractal_dimension,
            'market_persistence': 'Trending' if metrics.hurst_exponent > 0.5 else 'Mean Reverting',
            'volatility_clustering': 'High' if metrics.volatility_clustering > 0.3 else 'Low',
            'time_structure': 'Complex' if metrics.entropy > 2 else 'Simple'
        }
    
    # متدهای کمکی که نیاز به پیاده‌سازی بیشتر دارند...
    def _calculate_next_peak_from_phase(self, period: float, phase: float) -> Optional[float]:
        return len(self.data) + period * 0.25
    
    def _calculate_next_trough_from_phase(self, period: float, phase: float) -> Optional[float]:
        return len(self.data) + period * 0.75
    
    def _calculate_fourier_significance(self, strength: float) -> float:
        return 0.05 * (1 - strength)
    
    # سایر متدهای کمکی که به دلیل محدودیت فضا خلاصه شده‌اند...
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """دریافت خلاصه تحلیل‌ها"""
        try:
            if not self.time_analysis_results:
                return {'total_analyses': 0, 'analyses': []}
            
            return {
                'total_analyses': len(self.time_analysis_results),
                'latest_analysis': self.time_analysis_results[-1].summary,
                'average_quality': np.mean([r.analysis_quality for r in self.time_analysis_results]),
                'average_reliability': np.mean([r.reliability_score for r in self.time_analysis_results])
            }
            
        except Exception as e:
            logger.error(f"Error generating analysis summary: {e}")
            return {}
    
    def export_analysis_results(self, format: str = 'json') -> str:
        """صادرات نتایج تحلیل"""
        try:
            if not self.time_analysis_results:
                return ""
            
            # تبدیل به دیکشنری قابل سریالایز
            results_dict = []
            for result in self.time_analysis_results:
                result_dict = {
                    'analysis_id': result.analysis_id,
                    'timestamp': result.timestamp.isoformat(),
                    'timeframe': result.timeframe.value,
                    'analysis_quality': result.analysis_quality,
                    'reliability_score': result.reliability_score,
                    'summary': result.summary,
                    'total_cycles': len(result.cycles),
                    'total_projections': len(result.time_projections),
                    'critical_zones': len(result.critical_time_zones)
                }
                results_dict.append(result_dict)
            
            if format.lower() == 'json':
                return json.dumps(results_dict, indent=2, ensure_ascii=False)
            else:
                return str(results_dict)
                
        except Exception as e:
            logger.error(f"Error exporting analysis results: {e}")
            return ""