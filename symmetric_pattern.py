"""الگوهای سیمتریک پیشرفته (9 موجی) - نسخه حرفه‌ای"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum
import logging
from scipy import stats, optimize, signal
from scipy.spatial.distance import euclidean, cosine
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import warnings
from datetime import datetime, timedelta
import json

# تنظیم logging
logger = logging.getLogger(__name__)

class SymmetryType(Enum):
    """انواع تقارن"""
    BILATERAL = "bilateral"          # تقارن دوطرفه
    RADIAL = "radial"               # تقارن شعاعی
    ROTATIONAL = "rotational"       # تقارن چرخشی
    TRANSLATIONAL = "translational" # تقارن انتقالی
    SPIRAL = "spiral"               # تقارن مارپیچی
    FRACTAL = "fractal"             # تقارن فرکتالی

class SymmetryQuality(Enum):
    """کیفیت تقارن"""
    PERFECT = "perfect"         # 95%+
    EXCELLENT = "excellent"     # 85-95%
    GOOD = "good"              # 70-85%
    MODERATE = "moderate"      # 55-70%
    POOR = "poor"              # 40-55%
    INVALID = "invalid"        # <40%

class SymmetricPatternType(Enum):
    """انواع الگوهای سیمتریک"""
    CLASSIC_SYMMETRIC = "classic_symmetric"
    EXPANDED_SYMMETRIC = "expanded_symmetric"
    CONTRACTED_SYMMETRIC = "contracted_symmetric"
    IRREGULAR_SYMMETRIC = "irregular_symmetric"
    RUNNING_SYMMETRIC = "running_symmetric"
    COMPLEX_SYMMETRIC = "complex_symmetric"

@dataclass
class WaveStructure:
    """ساختار موج پیشرفته"""
    label: str
    wave_number: int
    start_index: int
    end_index: int
    start_price: float
    end_price: float
    length: float
    duration: int
    direction: str
    sub_waves: List['WaveStructure'] = field(default_factory=list)
    volume_profile: Dict = field(default_factory=dict)
    momentum_profile: Dict = field(default_factory=dict)
    fibonacci_levels: Dict = field(default_factory=dict)
    fractal_dimension: float = 0.0
    hurst_exponent: float = 0.0
    shape_complexity: float = 0.0
    
@dataclass
class GeometricSymmetry:
    """تحلیل هندسی تقارن"""
    center_point: Tuple[float, float]
    symmetry_axis: float
    reflection_accuracy: float
    rotation_angle: float
    scaling_factor: float
    geometric_balance: float
    aspect_ratio: float
    golden_ratio_alignment: float
    
@dataclass
class SymmetryMetrics:
    """متریک‌های پیشرفته تقارن"""
    spatial_symmetry: float
    temporal_symmetry: float
    amplitude_symmetry: float
    frequency_symmetry: float
    phase_symmetry: float
    harmonic_symmetry: float
    fractal_symmetry: float
    statistical_symmetry: float
    information_entropy: float
    lyapunov_exponent: float
    correlation_dimension: float
    
@dataclass
class PatternProjections:
    """پروژکشن‌های الگو"""
    post_pattern_targets: Dict[str, float]
    time_projections: Dict[str, int]
    support_resistance_levels: List[float]
    invalidation_levels: Dict[str, float]
    confidence_intervals: Dict[str, Tuple[float, float]]
    probability_distribution: Dict[str, float]

@dataclass
class AdvancedSymmetricWave:
    """کلاس موج سیمتریک پیشرفته"""
    pattern_id: str
    waves: List[WaveStructure]
    pivot_points: List[Tuple]
    pattern_type: SymmetricPatternType
    symmetry_type: SymmetryType
    symmetry_quality: SymmetryQuality
    center_wave: int
    
    # متریک‌های پیشرفته
    overall_confidence: float
    pattern_completion: float
    geometric_analysis: GeometricSymmetry
    symmetry_metrics: SymmetryMetrics
    
    # پروژکشن‌ها و اهداف
    projections: PatternProjections
    market_context: Dict
    
    # اعتبارسنجی
    validation_score: float
    validation_details: Dict
    statistical_significance: float
    
    # Machine Learning Features
    ml_features: np.ndarray = field(default=None)
    ml_confidence: float = 0.0
    anomaly_score: float = 0.0
    
    # ویژگی‌های کیفی
    is_valid: bool = False
    strength_rating: str = "UNKNOWN"
    trade_recommendation: str = "NONE"
    risk_assessment: Dict = field(default_factory=dict)

class AdvancedSymmetricAnalyzer:
    """تحلیلگر پیشرفته الگوهای سیمتریک"""
    
    def __init__(self, data: pd.DataFrame, config: Dict = None):
        self.data = data
        self.config = config or self._get_default_config()
        self.symmetric_patterns = []
        self.ml_models = {}
        self.feature_scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        
        # تنظیمات پیشرفته
        self.min_pattern_length = self.config.get('min_pattern_length', 200)
        self.max_pattern_length = self.config.get('max_pattern_length', 800)
        self.symmetry_tolerance = self.config.get('symmetry_tolerance', 0.05)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.7)
        
        # آماده‌سازی ML models
        self._initialize_ml_models()
        
        logger.info("Advanced Symmetric Analyzer initialized")
    
    def _get_default_config(self) -> Dict:
        """تنظیمات پیش‌فرض"""
        return {
            'min_pattern_length': 200,
            'max_pattern_length': 800,
            'symmetry_tolerance': 0.05,
            'confidence_threshold': 0.7,
            'ml_enabled': True,
            'statistical_analysis': True,
            'geometric_analysis': True,
            'multi_timeframe': True,
            'advanced_validation': True,
            'harmonic_analysis': True
        }
    
    def _initialize_ml_models(self):
        """راه‌اندازی مدل‌های ML"""
        try:
            # مدل تشخیص الگو
            self.ml_models['pattern_classifier'] = RandomForestClassifier(
                n_estimators=100, 
                random_state=42,
                max_depth=10
            )
            
            # مدل کیفیت تقارن
            self.ml_models['quality_estimator'] = RandomForestClassifier(
                n_estimators=50,
                random_state=42
            )
            
            logger.info("ML models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing ML models: {e}")
            self.config['ml_enabled'] = False
    
    def identify_advanced_symmetric(self, pivots: List[Tuple], 
                                  degree: int = 0,
                                  strict_validation: bool = True) -> Optional[AdvancedSymmetricWave]:
        """شناسایی پیشرفته الگوی سیمتریک"""
        
        if len(pivots) < 10:  # حداقل 10 نقطه برای 9 موج
            return None
        
        try:
            # مرحله 1: استخراج امواج
            waves = self._extract_advanced_waves(pivots)
            if not waves or len(waves) != 9:
                return None
            
            # مرحله 2: تحلیل هندسی
            geometric_analysis = self._perform_geometric_analysis(waves)
            
            # مرحله 3: محاسبه متریک‌های تقارن
            symmetry_metrics = self._calculate_advanced_symmetry(waves)
            
            # مرحله 4: تعیین نوع تقارن و الگو
            symmetry_type = self._determine_symmetry_type(waves, geometric_analysis)
            pattern_type = self._classify_pattern_type(waves, symmetry_metrics)
            
            # مرحله 5: اعتبارسنجی پیشرفته
            validation_result = self._advanced_validation(waves, symmetry_metrics, strict_validation)
            
            if not validation_result['is_valid']:
                return None
            
            # مرحله 6: محاسبه اعتماد کلی
            overall_confidence = self._calculate_overall_confidence(
                waves, symmetry_metrics, geometric_analysis, validation_result
            )
            
            if overall_confidence < self.confidence_threshold:
                return None
            
            # مرحله 7: پروژکشن و اهداف
            projections = self._calculate_projections(waves, symmetry_metrics)
            
            # مرحله 8: تحلیل ML (اگر فعال باشد)
            ml_features = None
            ml_confidence = 0.0
            anomaly_score = 0.0
            
            if self.config.get('ml_enabled', False):
                ml_features = self._extract_ml_features(waves, symmetry_metrics)
                ml_confidence = self._calculate_ml_confidence(ml_features)
                anomaly_score = self._detect_anomalies(ml_features)
            
            # مرحله 9: ایجاد الگوی نهایی
            pattern = AdvancedSymmetricWave(
                pattern_id=f"SYM_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{np.random.randint(1000, 9999)}",
                waves=waves,
                pivot_points=pivots[:10],
                pattern_type=pattern_type,
                symmetry_type=symmetry_type,
                symmetry_quality=self._determine_quality(symmetry_metrics.spatial_symmetry),
                center_wave=4,  # موج E
                overall_confidence=overall_confidence,
                pattern_completion=self._calculate_completion_percentage(waves),
                geometric_analysis=geometric_analysis,
                symmetry_metrics=symmetry_metrics,
                projections=projections,
                market_context=self._analyze_market_context(waves),
                validation_score=validation_result['score'],
                validation_details=validation_result['details'],
                statistical_significance=validation_result['statistical_significance'],
                ml_features=ml_features,
                ml_confidence=ml_confidence,
                anomaly_score=anomaly_score,
                is_valid=True,
                strength_rating=self._rate_pattern_strength(overall_confidence),
                trade_recommendation=self._generate_trade_recommendation(projections, overall_confidence),
                risk_assessment=self._assess_pattern_risks(waves, symmetry_metrics)
            )
            
            self.symmetric_patterns.append(pattern)
            logger.info(f"Advanced symmetric pattern identified: {pattern.pattern_id}")
            
            return pattern
            
        except Exception as e:
            logger.error(f"Error in advanced symmetric identification: {e}")
            return None
    
    def _extract_advanced_waves(self, pivots: List[Tuple]) -> List[WaveStructure]:
        """استخراج پیشرفته امواج"""
        waves = []
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        
        try:
            for i in range(9):
                if i + 1 >= len(pivots):
                    break
                
                start_point = pivots[i]
                end_point = pivots[i + 1]
                
                # محاسبات پایه
                length = abs(end_point[1] - start_point[1])
                duration = end_point[0] - start_point[0]
                direction = 'up' if end_point[1] > start_point[1] else 'down'
                
                # تحلیل‌های پیشرفته
                wave_data = self.data.iloc[start_point[0]:end_point[0]+1]
                
                # محاسبه volume profile
                volume_profile = self._calculate_volume_profile(wave_data)
                
                # محاسبه momentum profile
                momentum_profile = self._calculate_momentum_profile(wave_data)
                
                # محاسبه سطوح فیبوناچی
                fibonacci_levels = self._calculate_fibonacci_levels(start_point[1], end_point[1])
                
                # محاسبه بعد فرکتالی
                fractal_dimension = self._calculate_fractal_dimension(wave_data['close'].values)
                
                # محاسبه نمای هرست
                hurst_exponent = self._calculate_hurst_exponent(wave_data['close'].values)
                
                # محاسبه پیچیدگی شکل
                shape_complexity = self._calculate_shape_complexity(wave_data)
                
                wave = WaveStructure(
                    label=labels[i],
                    wave_number=i + 1,
                    start_index=start_point[0],
                    end_index=end_point[0],
                    start_price=start_point[1],
                    end_price=end_point[1],
                    length=length,
                    duration=duration,
                    direction=direction,
                    volume_profile=volume_profile,
                    momentum_profile=momentum_profile,
                    fibonacci_levels=fibonacci_levels,
                    fractal_dimension=fractal_dimension,
                    hurst_exponent=hurst_exponent,
                    shape_complexity=shape_complexity
                )
                
                waves.append(wave)
            
            return waves
            
        except Exception as e:
            logger.error(f"Error extracting advanced waves: {e}")
            return []
    
    def _perform_geometric_analysis(self, waves: List[WaveStructure]) -> GeometricSymmetry:
        """تحلیل هندسی پیشرفته"""
        try:
            # محاسبه نقطه مرکز
            all_points = [(w.start_index, w.start_price) for w in waves]
            all_points.append((waves[-1].end_index, waves[-1].end_price))
            
            center_x = np.mean([p[0] for p in all_points])
            center_y = np.mean([p[1] for p in all_points])
            center_point = (center_x, center_y)
            
            # محاسبه محور تقارن
            symmetry_axis = self._calculate_symmetry_axis(all_points)
            
            # محاسبه دقت انعکاس
            reflection_accuracy = self._calculate_reflection_accuracy(waves, symmetry_axis)
            
            # محاسبه زاویه چرخش
            rotation_angle = self._calculate_rotation_angle(waves)
            
            # محاسبه فاکتور مقیاس
            scaling_factor = self._calculate_scaling_factor(waves)
            
            # محاسبه تعادل هندسی
            geometric_balance = self._calculate_geometric_balance(waves)
            
            # محاسبه نسبت ابعاد
            aspect_ratio = self._calculate_aspect_ratio(waves)
            
            # محاسبه تراز با نسبت طلایی
            golden_ratio_alignment = self._calculate_golden_ratio_alignment(waves)
            
            return GeometricSymmetry(
                center_point=center_point,
                symmetry_axis=symmetry_axis,
                reflection_accuracy=reflection_accuracy,
                rotation_angle=rotation_angle,
                scaling_factor=scaling_factor,
                geometric_balance=geometric_balance,
                aspect_ratio=aspect_ratio,
                golden_ratio_alignment=golden_ratio_alignment
            )
            
        except Exception as e:
            logger.error(f"Error in geometric analysis: {e}")
            return GeometricSymmetry(
                center_point=(0, 0), symmetry_axis=0, reflection_accuracy=0,
                rotation_angle=0, scaling_factor=1, geometric_balance=0,
                aspect_ratio=1, golden_ratio_alignment=0
            )
    
    def _calculate_advanced_symmetry(self, waves: List[WaveStructure]) -> SymmetryMetrics:
        """محاسبه متریک‌های پیشرفته تقارن"""
        try:
            # تقارن فضایی
            spatial_symmetry = self._calculate_spatial_symmetry(waves)
            
            # تقارن زمانی
            temporal_symmetry = self._calculate_temporal_symmetry(waves)
            
            # تقارن دامنه
            amplitude_symmetry = self._calculate_amplitude_symmetry(waves)
            
            # تقارن فرکانس
            frequency_symmetry = self._calculate_frequency_symmetry(waves)
            
            # تقارن فاز
            phase_symmetry = self._calculate_phase_symmetry(waves)
            
            # تقارن هارمونیک
            harmonic_symmetry = self._calculate_harmonic_symmetry(waves)
            
            # تقارن فرکتالی
            fractal_symmetry = self._calculate_fractal_symmetry(waves)
            
            # تقارن آماری
            statistical_symmetry = self._calculate_statistical_symmetry(waves)
            
            # آنتروپی اطلاعات
            information_entropy = self._calculate_information_entropy(waves)
            
            # نمای لیاپانوف
            lyapunov_exponent = self._calculate_lyapunov_exponent(waves)
            
            # بعد همبستگی
            correlation_dimension = self._calculate_correlation_dimension(waves)
            
            return SymmetryMetrics(
                spatial_symmetry=spatial_symmetry,
                temporal_symmetry=temporal_symmetry,
                amplitude_symmetry=amplitude_symmetry,
                frequency_symmetry=frequency_symmetry,
                phase_symmetry=phase_symmetry,
                harmonic_symmetry=harmonic_symmetry,
                fractal_symmetry=fractal_symmetry,
                statistical_symmetry=statistical_symmetry,
                information_entropy=information_entropy,
                lyapunov_exponent=lyapunov_exponent,
                correlation_dimension=correlation_dimension
            )
            
        except Exception as e:
            logger.error(f"Error calculating advanced symmetry: {e}")
            return SymmetryMetrics(
                spatial_symmetry=0, temporal_symmetry=0, amplitude_symmetry=0,
                frequency_symmetry=0, phase_symmetry=0, harmonic_symmetry=0,
                fractal_symmetry=0, statistical_symmetry=0, information_entropy=0,
                lyapunov_exponent=0, correlation_dimension=0
            )
    
    def _calculate_spatial_symmetry(self, waves: List[WaveStructure]) -> float:
        """محاسبه تقارن فضایی"""
        try:
            center = 4  # موج E
            symmetry_scores = []
            
            for i in range(center):
                left_idx = center - i - 1
                right_idx = center + i + 1
                
                if right_idx < len(waves):
                    left_wave = waves[left_idx]
                    right_wave = waves[right_idx]
                    
                    # مقایسه طول‌ها
                    length_ratio = min(left_wave.length, right_wave.length) / max(left_wave.length, right_wave.length)
                    
                    # مقایسه جهت‌ها (امواج متقابل باید جهت مخالف داشته باشند)
                    direction_score = 1.0 if left_wave.direction != right_wave.direction else 0.5
                    
                    # مقایسه پیچیدگی شکل
                    complexity_ratio = min(left_wave.shape_complexity, right_wave.shape_complexity) / \
                                     max(left_wave.shape_complexity, right_wave.shape_complexity)
                    
                    # ترکیب امتیازات
                    wave_symmetry = (length_ratio * 0.4 + direction_score * 0.3 + complexity_ratio * 0.3)
                    symmetry_scores.append(wave_symmetry)
            
            return np.mean(symmetry_scores) if symmetry_scores else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating spatial symmetry: {e}")
            return 0.0
    
    def _calculate_temporal_symmetry(self, waves: List[WaveStructure]) -> float:
        """محاسبه تقارن زمانی"""
        try:
            center = 4
            time_ratios = []
            
            for i in range(center):
                left_idx = center - i - 1
                right_idx = center + i + 1
                
                if right_idx < len(waves):
                    left_duration = waves[left_idx].duration
                    right_duration = waves[right_idx].duration
                    
                    if max(left_duration, right_duration) > 0:
                        ratio = min(left_duration, right_duration) / max(left_duration, right_duration)
                        time_ratios.append(ratio)
            
            return np.mean(time_ratios) if time_ratios else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating temporal symmetry: {e}")
            return 0.0
    
    def _calculate_amplitude_symmetry(self, waves: List[WaveStructure]) -> float:
        """محاسبه تقارن دامنه"""
        try:
            # محاسبه تقارن بر اساس دامنه حرکات
            center = 4
            amplitude_ratios = []
            
            for i in range(center):
                left_idx = center - i - 1
                right_idx = center + i + 1
                
                if right_idx < len(waves):
                    left_amplitude = abs(waves[left_idx].length)
                    right_amplitude = abs(waves[right_idx].length)
                    
                    if max(left_amplitude, right_amplitude) > 0:
                        ratio = min(left_amplitude, right_amplitude) / max(left_amplitude, right_amplitude)
                        amplitude_ratios.append(ratio)
            
            return np.mean(amplitude_ratios) if amplitude_ratios else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating amplitude symmetry: {e}")
            return 0.0
    
    def _calculate_frequency_symmetry(self, waves: List[WaveStructure]) -> float:
        """محاسبه تقارن فرکانس"""
        try:
            # تحلیل فرکانس بر اساس FFT
            all_prices = []
            for wave in waves:
                wave_data = self.data.iloc[wave.start_index:wave.end_index+1]['close'].values
                all_prices.extend(wave_data)
            
            if len(all_prices) < 8:
                return 0.0
            
            # محاسبه FFT
            fft_result = np.fft.fft(all_prices)
            frequencies = np.fft.fftfreq(len(all_prices))
            
            # تحلیل تقارن فرکانس
            power_spectrum = np.abs(fft_result) ** 2
            
            # بررسی تقارن در طیف توان
            half_len = len(power_spectrum) // 2
            left_half = power_spectrum[:half_len]
            right_half = power_spectrum[-half_len:][::-1]  # معکوس کردن
            
            if len(left_half) == len(right_half) and len(left_half) > 0:
                correlation = np.corrcoef(left_half, right_half)[0, 1]
                return max(0, correlation)
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating frequency symmetry: {e}")
            return 0.0
    
    def _calculate_phase_symmetry(self, waves: List[WaveStructure]) -> float:
        """محاسبه تقارن فاز"""
        try:
            # محاسبه تغییرات فاز بین امواج
            phase_differences = []
            
            for i in range(len(waves) - 1):
                wave1 = waves[i]
                wave2 = waves[i + 1]
                
                # محاسبه زاویه تغییر
                dx = wave2.end_index - wave1.start_index
                dy = wave2.end_price - wave1.start_price
                
                if dx != 0:
                    angle = np.arctan(dy / dx)
                    phase_differences.append(angle)
            
            if not phase_differences:
                return 0.0
            
            # بررسی تقارن در تغییرات فاز
            center_idx = len(phase_differences) // 2
            left_phases = phase_differences[:center_idx]
            right_phases = phase_differences[center_idx:][::-1]
            
            if len(left_phases) == len(right_phases) and len(left_phases) > 0:
                # محاسبه تشابه فازها
                similarity = 1 - np.mean(np.abs(np.array(left_phases) - np.array(right_phases))) / np.pi
                return max(0, similarity)
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating phase symmetry: {e}")
            return 0.0
    
    def _calculate_harmonic_symmetry(self, waves: List[WaveStructure]) -> float:
        """محاسبه تقارن هارمونیک"""
        try:
            # تحلیل هارمونیک‌های الگو
            harmonic_scores = []
            
            # نسبت‌های هارمونیک کلاسیک
            harmonic_ratios = [0.5, 0.618, 0.786, 1.0, 1.272, 1.618, 2.0, 2.618]
            
            for i in range(len(waves) - 1):
                for j in range(i + 1, len(waves)):
                    ratio = waves[j].length / waves[i].length if waves[i].length > 0 else 0
                    
                    # بررسی تطابق با نسبت‌های هارمونیک
                    for harmonic_ratio in harmonic_ratios:
                        if abs(ratio - harmonic_ratio) / harmonic_ratio < 0.05:  # تحمل 5%
                            harmonic_scores.append(1.0)
                            break
                    else:
                        harmonic_scores.append(0.0)
            
            return np.mean(harmonic_scores) if harmonic_scores else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating harmonic symmetry: {e}")
            return 0.0
    
    def _calculate_fractal_symmetry(self, waves: List[WaveStructure]) -> float:
        """محاسبه تقارن فرکتالی"""
        try:
            # محاسبه تشابه فرکتالی بین امواج
            fractal_scores = []
            
            for i in range(len(waves)):
                for j in range(i + 1, len(waves)):
                    # مقایسه ابعاد فرکتالی
                    fd1 = waves[i].fractal_dimension
                    fd2 = waves[j].fractal_dimension
                    
                    if max(fd1, fd2) > 0:
                        fractal_similarity = min(fd1, fd2) / max(fd1, fd2)
                        fractal_scores.append(fractal_similarity)
            
            return np.mean(fractal_scores) if fractal_scores else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating fractal symmetry: {e}")
            return 0.0
    
    def _calculate_statistical_symmetry(self, waves: List[WaveStructure]) -> float:
        """محاسبه تقارن آماری"""
        try:
            # آماره‌های توصیفی امواج
            wave_lengths = [w.length for w in waves]
            wave_durations = [w.duration for w in waves]
            
            # بررسی تقارن در توزیع
            # محاسبه skewness و kurtosis
            length_skewness = abs(stats.skew(wave_lengths))
            duration_skewness = abs(stats.skew(wave_durations))
            
            # تقارن بهتر = skewness کمتر
            symmetry_score = (2 - length_skewness - duration_skewness) / 2
            
            return max(0, min(1, symmetry_score))
            
        except Exception as e:
            logger.error(f"Error calculating statistical symmetry: {e}")
            return 0.0
    
    def _calculate_information_entropy(self, waves: List[WaveStructure]) -> float:
        """محاسبه آنتروپی اطلاعات"""
        try:
            # محاسبه آنتروپی بر اساس توزیع طول امواج
            lengths = [w.length for w in waves]
            
            # تبدیل به احتمالات
            total_length = sum(lengths)
            if total_length == 0:
                return 0.0
                
            probabilities = [l / total_length for l in lengths]
            
            # محاسبه آنتروپی شانون
            entropy = -sum(p * np.log2(p) for p in probabilities if p > 0)
            
            # نرمال‌سازی (حداکثر آنتروپی برای 9 موج)
            max_entropy = np.log2(9)
            normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
            
            return normalized_entropy
            
        except Exception as e:
            logger.error(f"Error calculating information entropy: {e}")
            return 0.0
    
    def _calculate_lyapunov_exponent(self, waves: List[WaveStructure]) -> float:
        """محاسبه نمای لیاپانوف"""
        try:
            # ساده‌سازی شده برای داده‌های قیمت
            all_prices = []
            for wave in waves:
                all_prices.append(wave.end_price)
            
            if len(all_prices) < 3:
                return 0.0
            
            # محاسبه تغییرات لگاریتمی
            log_changes = np.diff(np.log(all_prices))
            
            # تخمین نمای لیاپانوف
            if len(log_changes) > 1:
                lyapunov = np.mean(np.abs(log_changes))
                return min(1.0, lyapunov)  # محدود کردن به 1
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating Lyapunov exponent: {e}")
            return 0.0
    
    def _calculate_correlation_dimension(self, waves: List[WaveStructure]) -> float:
        """محاسبه بعد همبستگی"""
        try:
            # تهیه داده برای محاسبه بعد همبستگی
            wave_features = []
            for wave in waves:
                features = [
                    wave.length,
                    wave.duration,
                    wave.fractal_dimension,
                    wave.hurst_exponent,
                    wave.shape_complexity
                ]
                wave_features.append(features)
            
            if len(wave_features) < 3:
                return 0.0
            
            wave_features = np.array(wave_features)
            
            # محاسبه ماتریس فاصله
            distances = []
            for i in range(len(wave_features)):
                for j in range(i + 1, len(wave_features)):
                    dist = euclidean(wave_features[i], wave_features[j])
                    distances.append(dist)
            
            if not distances:
                return 0.0
            
            # تخمین ساده بعد همبستگی
            # در عمل نیاز به الگوریتم پیچیده‌تری دارد
            correlation_dim = len(wave_features) / (1 + np.std(distances))
            
            return min(3.0, correlation_dim)  # محدود کردن به 3
            
        except Exception as e:
            logger.error(f"Error calculating correlation dimension: {e}")
            return 0.0
    
    # ادامه متدهای کمکی...
    def _calculate_volume_profile(self, wave_data: pd.DataFrame) -> Dict:
        """محاسبه پروفایل حجم"""
        try:
            if 'volume' not in wave_data.columns:
                return {}
            
            return {
                'total_volume': wave_data['volume'].sum(),
                'average_volume': wave_data['volume'].mean(),
                'volume_trend': 'increasing' if wave_data['volume'].iloc[-1] > wave_data['volume'].iloc[0] else 'decreasing',
                'volume_concentration': wave_data['volume'].std() / wave_data['volume'].mean() if wave_data['volume'].mean() > 0 else 0
            }
        except:
            return {}
    
    def _calculate_momentum_profile(self, wave_data: pd.DataFrame) -> Dict:
        """محاسبه پروفایل مومنتوم"""
        try:
            prices = wave_data['close'].values
            momentum = np.diff(prices) / prices[:-1] * 100  # درصد تغییر
            
            return {
                'average_momentum': np.mean(momentum),
                'momentum_acceleration': np.mean(np.diff(momentum)),
                'momentum_volatility': np.std(momentum),
                'directional_consistency': len([m for m in momentum if m > 0]) / len(momentum) if len(momentum) > 0 else 0
            }
        except:
            return {}
    
    def _calculate_fibonacci_levels(self, start_price: float, end_price: float) -> Dict:
        """محاسبه سطوح فیبوناچی"""
        try:
            diff = end_price - start_price
            
            return {
                '23.6%': start_price + diff * 0.236,
                '38.2%': start_price + diff * 0.382,
                '50.0%': start_price + diff * 0.5,
                '61.8%': start_price + diff * 0.618,
                '78.6%': start_price + diff * 0.786
            }
        except:
            return {}
    
    def _calculate_fractal_dimension(self, prices: np.ndarray) -> float:
        """محاسبه بعد فرکتالی"""
        try:
            if len(prices) < 4:
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
            
            # محاسبه slope
            x = np.log(range(1, len(lks) + 1))
            y = np.log(lks)
            
            slope, _ = np.polyfit(x, y, 1)
            fractal_dim = -slope
            
            return max(1.0, min(3.0, fractal_dim))
            
        except:
            return 1.0
    
    def _calculate_hurst_exponent(self, prices: np.ndarray) -> float:
        """محاسبه نمای هرست"""
        try:
            if len(prices) < 10:
                return 0.5
            
            # روش R/S
            n = len(prices)
            log_returns = np.diff(np.log(prices))
            
            lags = range(2, min(n//4, 100))
            rs_values = []
            
            for lag in lags:
                chunks = [log_returns[i:i+lag] for i in range(0, len(log_returns), lag) if i+lag <= len(log_returns)]
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
    
    def _calculate_shape_complexity(self, wave_data: pd.DataFrame) -> float:
        """محاسبه پیچیدگی شکل"""
        try:
            prices = wave_data['close'].values
            
            if len(prices) < 3:
                return 0.0
            
            # محاسبه تغییرات جهت
            direction_changes = 0
            for i in range(1, len(prices) - 1):
                if (prices[i] > prices[i-1] and prices[i] > prices[i+1]) or \
                   (prices[i] < prices[i-1] and prices[i] < prices[i+1]):
                    direction_changes += 1
            
            # نرمال‌سازی
            complexity = direction_changes / max(1, len(prices) - 2)
            
            return min(1.0, complexity)
            
        except:
            return 0.0
    
    # ادامه در بخش بعدی...
    def _determine_symmetry_type(self, waves: List[WaveStructure], 
                                geometric_analysis: GeometricSymmetry) -> SymmetryType:
        """تعیین نوع تقارن"""
        try:
            # بررسی تقارن دوطرفه
            if geometric_analysis.reflection_accuracy > 0.8:
                return SymmetryType.BILATERAL
            
            # بررسی تقارن چرخشی
            if abs(geometric_analysis.rotation_angle) > 10:
                return SymmetryType.ROTATIONAL
            
            # بررسی تقارن شعاعی
            if geometric_analysis.geometric_balance > 0.9:
                return SymmetryType.RADIAL
            
            # بررسی تقارن مارپیچی
            spiral_score = self._calculate_spiral_score(waves)
            if spiral_score > 0.7:
                return SymmetryType.SPIRAL
            
            return SymmetryType.BILATERAL  # پیش‌فرض
            
        except:
            return SymmetryType.BILATERAL
    
    def _classify_pattern_type(self, waves: List[WaveStructure], 
                              symmetry_metrics: SymmetryMetrics) -> SymmetricPatternType:
        """طبقه‌بندی نوع الگو"""
        try:
            # محاسبه امتیازهای مختلف
            avg_symmetry = np.mean([
                symmetry_metrics.spatial_symmetry,
                symmetry_metrics.temporal_symmetry,
                symmetry_metrics.amplitude_symmetry
            ])
            
            if avg_symmetry > 0.9:
                return SymmetricPatternType.CLASSIC_SYMMETRIC
            elif avg_symmetry > 0.8:
                return SymmetricPatternType.EXPANDED_SYMMETRIC
            elif avg_symmetry > 0.7:
                return SymmetricPatternType.CONTRACTED_SYMMETRIC
            elif avg_symmetry > 0.6:
                return SymmetricPatternType.IRREGULAR_SYMMETRIC
            else:
                return SymmetricPatternType.COMPLEX_SYMMETRIC
                
        except:
            return SymmetricPatternType.CLASSIC_SYMMETRIC
    
    def _advanced_validation(self, waves: List[WaveStructure], 
                           symmetry_metrics: SymmetryMetrics,
                           strict: bool = True) -> Dict:
        """اعتبارسنجی پیشرفته"""
        try:
            validation_score = 0.0
            details = {}
            
            # قانون 1: تعداد امواج
            if len(waves) == 9:
                validation_score += 0.2
                details['wave_count'] = True
            else:
                details['wave_count'] = False
                if strict:
                    return {'is_valid': False, 'score': 0, 'details': details, 'statistical_significance': 0}
            
            # قانون 2: موج مرکزی قوی
            center_wave = waves[4]  # موج E
            avg_length = np.mean([w.length for w in waves])
            if center_wave.length >= avg_length * 0.8:
                validation_score += 0.15
                details['center_wave_strength'] = True
            else:
                details['center_wave_strength'] = False
            
            # قانون 3: تقارن مناسب
            if symmetry_metrics.spatial_symmetry > 0.6:
                validation_score += 0.2
                details['spatial_symmetry'] = True
            else:
                details['spatial_symmetry'] = False
            
            # قانون 4: تقارن زمانی
            if symmetry_metrics.temporal_symmetry > 0.5:
                validation_score += 0.15
                details['temporal_symmetry'] = True
            else:
                details['temporal_symmetry'] = False
            
            # قانون 5: الگوی جهت امواج
            direction_pattern = [w.direction for w in waves]
            alternating = all(direction_pattern[i] != direction_pattern[i+1] for i in range(len(direction_pattern)-1))
            if alternating:
                validation_score += 0.1
                details['alternating_directions'] = True
            else:
                details['alternating_directions'] = False
            
            # قانون 6: نسبت‌های فیبوناچی
            fibonacci_score = self._validate_fibonacci_relationships(waves)
            validation_score += fibonacci_score * 0.2
            details['fibonacci_relationships'] = fibonacci_score
            
            # محاسبه معنی‌داری آماری
            statistical_significance = self._calculate_statistical_significance(waves, symmetry_metrics)
            
            # تعیین اعتبار نهایی
            is_valid = validation_score > (0.7 if strict else 0.5)
            
            return {
                'is_valid': is_valid,
                'score': validation_score,
                'details': details,
                'statistical_significance': statistical_significance
            }
            
        except Exception as e:
            logger.error(f"Error in advanced validation: {e}")
            return {'is_valid': False, 'score': 0, 'details': {}, 'statistical_significance': 0}
    
    def _calculate_overall_confidence(self, waves: List[WaveStructure],
                                    symmetry_metrics: SymmetryMetrics,
                                    geometric_analysis: GeometricSymmetry,
                                    validation_result: Dict) -> float:
        """محاسبه اعتماد کلی"""
        try:
            # وزن‌های مختلف فاکتورها
            weights = {
                'validation': 0.3,
                'symmetry': 0.25,
                'geometry': 0.2,
                'statistical': 0.15,
                'fractal': 0.1
            }
            
            # امتیازات مختلف
            validation_score = validation_result['score']
            
            symmetry_score = np.mean([
                symmetry_metrics.spatial_symmetry,
                symmetry_metrics.temporal_symmetry,
                symmetry_metrics.amplitude_symmetry
            ])
            
            geometry_score = np.mean([
                geometric_analysis.reflection_accuracy,
                geometric_analysis.geometric_balance,
                geometric_analysis.golden_ratio_alignment
            ])
            
            statistical_score = symmetry_metrics.statistical_symmetry
            fractal_score = symmetry_metrics.fractal_symmetry
            
            # محاسبه اعتماد کلی
            overall_confidence = (
                validation_score * weights['validation'] +
                symmetry_score * weights['symmetry'] +
                geometry_score * weights['geometry'] +
                statistical_score * weights['statistical'] +
                fractal_score * weights['fractal']
            )
            
            return max(0.0, min(1.0, overall_confidence))
            
        except Exception as e:
            logger.error(f"Error calculating overall confidence: {e}")
            return 0.0
    
    def _calculate_projections(self, waves: List[WaveStructure],
                             symmetry_metrics: SymmetryMetrics) -> PatternProjections:
        """محاسبه پروژکشن‌ها و اهداف"""
        try:
            center_wave = waves[4]  # موج E
            pattern_range = max([w.end_price for w in waves]) - min([w.start_price for w in waves])
            
            # اهداف قیمتی پس از الگو
            post_pattern_targets = {
                'minimum': center_wave.end_price + pattern_range * 0.382,
                'probable': center_wave.end_price + pattern_range * 0.618,
                'maximum': center_wave.end_price + pattern_range * 1.0,
                'extended': center_wave.end_price + pattern_range * 1.618
            }
            
            # پروژکشن‌های زمانی
            total_time = waves[-1].end_index - waves[0].start_index
            time_projections = {
                'next_move_duration': int(total_time * 0.618),
                'consolidation_time': int(total_time * 0.382),
                'major_move_time': int(total_time * 1.0)
            }
            
            # سطوح حمایت و مقاومت
            all_prices = [w.start_price for w in waves] + [waves[-1].end_price]
            support_resistance_levels = sorted(set(all_prices))
            
            # سطوح باطل‌سازی
            invalidation_levels = {
                'minor': min([w.start_price for w in waves]),
                'major': center_wave.start_price,
                'critical': waves[0].start_price
            }
            
            # فواصل اطمینان
            confidence_intervals = {
                'target_range': (post_pattern_targets['minimum'], post_pattern_targets['maximum']),
                'time_range': (time_projections['consolidation_time'], time_projections['major_move_time'])
            }
            
            # توزیع احتمال
            probability_distribution = {
                'upward_breakout': 0.6 if waves[-1].direction == 'up' else 0.4,
                'downward_breakout': 0.4 if waves[-1].direction == 'up' else 0.6,
                'sideways_continuation': 0.2
            }
            
            return PatternProjections(
                post_pattern_targets=post_pattern_targets,
                time_projections=time_projections,
                support_resistance_levels=support_resistance_levels,
                invalidation_levels=invalidation_levels,
                confidence_intervals=confidence_intervals,
                probability_distribution=probability_distribution
            )
            
        except Exception as e:
            logger.error(f"Error calculating projections: {e}")
            return PatternProjections(
                post_pattern_targets={}, time_projections={},
                support_resistance_levels=[], invalidation_levels={},
                confidence_intervals={}, probability_distribution={}
            )
    
    def _analyze_market_context(self, waves: List[WaveStructure]) -> Dict:
        """تحلیل محیط بازار"""
        try:
            # تحلیل روند کلی
            first_price = waves[0].start_price
            last_price = waves[-1].end_price
            
            trend_direction = 'bullish' if last_price > first_price else 'bearish'
            trend_strength = abs(last_price - first_price) / first_price * 100
            
            # تحلیل نوسانات
            price_range = max([w.end_price for w in waves]) - min([w.start_price for w in waves])
            volatility_level = price_range / first_price * 100
            
            # تحلیل حجم (اگر موجود باشد)
            avg_volume = np.mean([w.volume_profile.get('average_volume', 0) for w in waves])
            
            return {
                'trend_direction': trend_direction,
                'trend_strength': trend_strength,
                'volatility_level': volatility_level,
                'pattern_position': 'end_of_trend' if trend_strength > 20 else 'mid_trend',
                'market_sentiment': 'extreme' if volatility_level > 30 else 'normal',
                'volume_context': 'high' if avg_volume > 0 else 'unknown'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market context: {e}")
            return {}
    
    def _determine_quality(self, symmetry_score: float) -> SymmetryQuality:
        """تعیین کیفیت تقارن"""
        if symmetry_score >= 0.95:
            return SymmetryQuality.PERFECT
        elif symmetry_score >= 0.85:
            return SymmetryQuality.EXCELLENT
        elif symmetry_score >= 0.70:
            return SymmetryQuality.GOOD
        elif symmetry_score >= 0.55:
            return SymmetryQuality.MODERATE
        elif symmetry_score >= 0.40:
            return SymmetryQuality.POOR
        else:
            return SymmetryQuality.INVALID
    
    def _calculate_completion_percentage(self, waves: List[WaveStructure]) -> float:
        """محاسبه درصد تکمیل الگو"""
        try:
            # بررسی اینکه آیا همه 9 موج تشکیل شده
            if len(waves) == 9:
                return 1.0
            else:
                return len(waves) / 9
        except:
            return 0.0
    
    def _extract_ml_features(self, waves: List[WaveStructure],
                           symmetry_metrics: SymmetryMetrics) -> np.ndarray:
        """استخراج ویژگی‌های ML"""
        try:
            features = []
            
            # ویژگی‌های امواج
            for wave in waves:
                features.extend([
                    wave.length,
                    wave.duration,
                    wave.fractal_dimension,
                    wave.hurst_exponent,
                    wave.shape_complexity
                ])
            
            # ویژگی‌های تقارن
            features.extend([
                symmetry_metrics.spatial_symmetry,
                symmetry_metrics.temporal_symmetry,
                symmetry_metrics.amplitude_symmetry,
                symmetry_metrics.frequency_symmetry,
                symmetry_metrics.phase_symmetry,
                symmetry_metrics.harmonic_symmetry,
                symmetry_metrics.fractal_symmetry,
                symmetry_metrics.statistical_symmetry,
                symmetry_metrics.information_entropy,
                symmetry_metrics.lyapunov_exponent,
                symmetry_metrics.correlation_dimension
            ])
            
            return np.array(features)
            
        except Exception as e:
            logger.error(f"Error extracting ML features: {e}")
            return np.array([])
    
    def _calculate_ml_confidence(self, features: np.ndarray) -> float:
        """محاسبه اعتماد ML"""
        try:
            if not self.config.get('ml_enabled', False) or len(features) == 0:
                return 0.0
            
            # در صورت عدم وجود مدل آموزش دیده، بازگشت امتیاز ثابت
            # در پیاده‌سازی واقعی، مدل از روی داده‌های تاریخی آموزش می‌بیند
            
            # تخمین ساده بر اساس ویژگی‌ها
            normalized_features = features / (np.max(features) + 1e-8)
            confidence = np.mean(normalized_features[np.isfinite(normalized_features)])
            
            return max(0.0, min(1.0, confidence))
            
        except Exception as e:
            logger.error(f"Error calculating ML confidence: {e}")
            return 0.0
    
    def _detect_anomalies(self, features: np.ndarray) -> float:
        """تشخیص ناهنجاری‌ها"""
        try:
            if len(features) == 0:
                return 0.0
            
            # تشخیص ناهنجاری ساده
            z_scores = np.abs(stats.zscore(features))
            anomaly_score = np.mean(z_scores > 2)  # نسبت ویژگی‌های غیرعادی
            
            return min(1.0, anomaly_score)
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return 0.0
    
    def _rate_pattern_strength(self, confidence: float) -> str:
        """رتبه‌بندی قدرت الگو"""
        if confidence >= 0.9:
            return "VERY_STRONG"
        elif confidence >= 0.8:
            return "STRONG"
        elif confidence >= 0.7:
            return "MODERATE"
        elif confidence >= 0.6:
            return "WEAK"
        else:
            return "VERY_WEAK"
    
    def _generate_trade_recommendation(self, projections: PatternProjections,
                                     confidence: float) -> str:
        """تولید توصیه معاملاتی"""
        try:
            if confidence < 0.6:
                return "NO_TRADE"
            
            prob_dist = projections.probability_distribution
            
            if prob_dist.get('upward_breakout', 0) > 0.6:
                return "BUY_BREAKOUT" if confidence > 0.8 else "WATCH_FOR_BUY"
            elif prob_dist.get('downward_breakout', 0) > 0.6:
                return "SELL_BREAKOUT" if confidence > 0.8 else "WATCH_FOR_SELL"
            else:
                return "RANGE_TRADE"
                
        except:
            return "NO_TRADE"
    
    def _assess_pattern_risks(self, waves: List[WaveStructure],
                            symmetry_metrics: SymmetryMetrics) -> Dict:
        """ارزیابی ریسک‌های الگو"""
        try:
            # محاسبه ریسک‌های مختلف
            volatility_risk = np.std([w.length for w in waves]) / np.mean([w.length for w in waves])
            
            time_risk = max([w.duration for w in waves]) / min([w.duration for w in waves]) - 1
            
            structural_risk = 1 - symmetry_metrics.spatial_symmetry
            
            return {
                'volatility_risk': min(1.0, volatility_risk),
                'time_risk': min(1.0, time_risk / 10),  # نرمال‌سازی
                'structural_risk': structural_risk,
                'overall_risk': np.mean([volatility_risk, time_risk/10, structural_risk]),
                'risk_level': self._categorize_risk(np.mean([volatility_risk, time_risk/10, structural_risk]))
            }
            
        except Exception as e:
            logger.error(f"Error assessing pattern risks: {e}")
            return {'overall_risk': 0.5, 'risk_level': 'MEDIUM'}
    
    def _categorize_risk(self, risk_score: float) -> str:
        """طبقه‌بندی سطح ریسک"""
        if risk_score < 0.2:
            return "LOW"
        elif risk_score < 0.4:
            return "MEDIUM"
        elif risk_score < 0.6:
            return "HIGH"
        else:
            return "VERY_HIGH"
    
    # متدهای کمکی اضافی
    def _calculate_symmetry_axis(self, points: List[Tuple]) -> float:
        """محاسبه محور تقارن"""
        try:
            x_coords = [p[0] for p in points]
            return np.mean(x_coords)
        except:
            return 0.0
    
    def _calculate_reflection_accuracy(self, waves: List[WaveStructure], axis: float) -> float:
        """محاسبه دقت انعکاس"""
        try:
            center = 4
            reflection_scores = []
            
            for i in range(center):
                left_idx = center - i - 1
                right_idx = center + i + 1
                
                if right_idx < len(waves):
                    left_dist = abs(waves[left_idx].start_index - axis)
                    right_dist = abs(waves[right_idx].start_index - axis)
                    
                    if max(left_dist, right_dist) > 0:
                        reflection_score = min(left_dist, right_dist) / max(left_dist, right_dist)
                        reflection_scores.append(reflection_score)
            
            return np.mean(reflection_scores) if reflection_scores else 0.0
            
        except:
            return 0.0
    
    def _calculate_rotation_angle(self, waves: List[WaveStructure]) -> float:
        """محاسبه زاویه چرخش"""
        try:
            # محاسبه ساده بر اساس شیب کلی
            start_point = (waves[0].start_index, waves[0].start_price)
            end_point = (waves[-1].end_index, waves[-1].end_price)
            
            dx = end_point[0] - start_point[0]
            dy = end_point[1] - start_point[1]
            
            if dx != 0:
                angle = np.arctan(dy / dx) * 180 / np.pi
                return angle
            
            return 0.0
            
        except:
            return 0.0
    
    def _calculate_scaling_factor(self, waves: List[WaveStructure]) -> float:
        """محاسبه فاکتور مقیاس"""
        try:
            lengths = [w.length for w in waves]
            if len(lengths) < 2:
                return 1.0
            
            return max(lengths) / min(lengths) if min(lengths) > 0 else 1.0
            
        except:
            return 1.0
    
    def _calculate_geometric_balance(self, waves: List[WaveStructure]) -> float:
        """محاسبه تعادل هندسی"""
        try:
            # محاسبه مرکز جرم
            total_weight = sum(w.length for w in waves)
            if total_weight == 0:
                return 0.0
            
            center_of_mass_x = sum(w.start_index * w.length for w in waves) / total_weight
            center_of_mass_y = sum(w.start_price * w.length for w in waves) / total_weight
            
            # محاسبه انحراف از مرکز هندسی
            geometric_center_x = np.mean([w.start_index for w in waves])
            geometric_center_y = np.mean([w.start_price for w in waves])
            
            deviation = euclidean((center_of_mass_x, center_of_mass_y), 
                                (geometric_center_x, geometric_center_y))
            
            # نرمال‌سازی
            max_possible_deviation = np.sqrt((geometric_center_x**2 + geometric_center_y**2))
            
            if max_possible_deviation > 0:
                balance = 1 - (deviation / max_possible_deviation)
                return max(0.0, balance)
            
            return 1.0
            
        except:
            return 0.0
    
    def _calculate_aspect_ratio(self, waves: List[WaveStructure]) -> float:
        """محاسبه نسبت ابعاد"""
        try:
            time_span = waves[-1].end_index - waves[0].start_index
            price_span = max([w.end_price for w in waves]) - min([w.start_price for w in waves])
            
            if price_span > 0 and time_span > 0:
                return time_span / price_span
            
            return 1.0
            
        except:
            return 1.0
    
    def _calculate_golden_ratio_alignment(self, waves: List[WaveStructure]) -> float:
        """محاسبه تراز با نسبت طلایی"""
        try:
            golden_ratio = 1.618
            golden_ratios = [0.618, 1.0, 1.618, 2.618]
            
            alignment_scores = []
            
            for i in range(len(waves) - 1):
                for j in range(i + 1, len(waves)):
                    ratio = waves[j].length / waves[i].length if waves[i].length > 0 else 0
                    
                    # یافتن نزدیک‌ترین نسبت طلایی
                    min_deviation = min(abs(ratio - gr) / gr for gr in golden_ratios)
                    
                    if min_deviation < 0.05:  # تحمل 5%
                        alignment_scores.append(1 - min_deviation / 0.05)
                    else:
                        alignment_scores.append(0)
            
            return np.mean(alignment_scores) if alignment_scores else 0.0
            
        except:
            return 0.0
    
    def _calculate_spiral_score(self, waves: List[WaveStructure]) -> float:
        """محاسبه امتیاز مارپیچی"""
        try:
            # بررسی الگوی مارپیچی در طول‌ها
            lengths = [w.length for w in waves]
            
            # محاسبه نسبت‌های متوالی
            ratios = []
            for i in range(len(lengths) - 1):
                if lengths[i] > 0:
                    ratios.append(lengths[i + 1] / lengths[i])
            
            if not ratios:
                return 0.0
            
            # بررسی ثبات نسبت‌ها (ویژگی مارپیچ)
            ratio_std = np.std(ratios)
            ratio_mean = np.mean(ratios)
            
            if ratio_mean > 0:
                consistency = 1 - (ratio_std / ratio_mean)
                return max(0.0, consistency)
            
            return 0.0
            
        except:
            return 0.0
    
    def _validate_fibonacci_relationships(self, waves: List[WaveStructure]) -> float:
        """اعتبارسنجی روابط فیبوناچی"""
        try:
            fibonacci_levels = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618, 2.618]
            
            valid_relationships = 0
            total_relationships = 0
            
            for i in range(len(waves)):
                for j in range(i + 1, len(waves)):
                    if waves[i].length > 0:
                        ratio = waves[j].length / waves[i].length
                        
                        # بررسی تطابق با سطوح فیبوناچی
                        for fib_level in fibonacci_levels:
                            if abs(ratio - fib_level) / fib_level < 0.05:  # تحمل 5%
                                valid_relationships += 1
                                break
                        
                        total_relationships += 1
            
            return valid_relationships / total_relationships if total_relationships > 0 else 0.0
            
        except:
            return 0.0
    
    def _calculate_statistical_significance(self, waves: List[WaveStructure],
                                          symmetry_metrics: SymmetryMetrics) -> float:
        """محاسبه معنی‌داری آماری"""
        try:
            # آزمون t برای تقارن
            center = 4
            left_lengths = [waves[center - i - 1].length for i in range(center) if center - i - 1 >= 0]
            right_lengths = [waves[center + i + 1].length for i in range(center) if center + i + 1 < len(waves)]
            
            if len(left_lengths) >= 2 and len(right_lengths) >= 2:
                t_stat, p_value = stats.ttest_ind(left_lengths, right_lengths)
                significance = 1 - p_value  # هرچه p_value کمتر، معنی‌داری بیشتر
                return max(0.0, min(1.0, significance))
            
            return 0.5  # معنی‌داری متوسط در صورت عدم امکان محاسبه
            
        except:
            return 0.5
    
    def get_pattern_summary(self) -> Dict:
        """دریافت خلاصه الگوهای شناسایی شده"""
        try:
            if not self.symmetric_patterns:
                return {'total_patterns': 0, 'patterns': []}
            
            summary = {
                'total_patterns': len(self.symmetric_patterns),
                'average_confidence': np.mean([p.overall_confidence for p in self.symmetric_patterns]),
                'pattern_types': {},
                'quality_distribution': {},
                'patterns': []
            }
            
            # آمار انواع الگو
            for pattern in self.symmetric_patterns:
                pattern_type = pattern.pattern_type.value
                summary['pattern_types'][pattern_type] = summary['pattern_types'].get(pattern_type, 0) + 1
                
                quality = pattern.symmetry_quality.value
                summary['quality_distribution'][quality] = summary['quality_distribution'].get(quality, 0) + 1
            
            # بهترین الگوها
            sorted_patterns = sorted(self.symmetric_patterns, 
                                   key=lambda x: x.overall_confidence, reverse=True)
            
            for pattern in sorted_patterns[:5]:  # 5 الگوی برتر
                pattern_info = {
                    'id': pattern.pattern_id,
                    'type': pattern.pattern_type.value,
                    'confidence': pattern.overall_confidence,
                    'quality': pattern.symmetry_quality.value,
                    'strength': pattern.strength_rating,
                    'recommendation': pattern.trade_recommendation,
                    'risk_level': pattern.risk_assessment.get('risk_level', 'UNKNOWN'),
                    'targets': pattern.projections.post_pattern_targets
                }
                summary['patterns'].append(pattern_info)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating pattern summary: {e}")
            return {'total_patterns': 0, 'patterns': []}
    
    def export_analysis_results(self, format: str = 'json') -> str:
        """صادرات نتایج تحلیل"""
        try:
            summary = self.get_pattern_summary()
            
            if format.lower() == 'json':
                return json.dumps(summary, indent=2, ensure_ascii=False)
            elif format.lower() == 'csv':
                # پیاده‌سازی صادرات CSV
                import csv
                import io
                
                output = io.StringIO()
                if summary['patterns']:
                    fieldnames = summary['patterns'][0].keys()
                    writer = csv.DictWriter(output, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(summary['patterns'])
                
                return output.getvalue()
            else:
                return str(summary)
                
        except Exception as e:
            logger.error(f"Error exporting analysis results: {e}")
            return ""