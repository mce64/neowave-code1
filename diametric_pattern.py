# ================= diametric_pattern.py =================
"""
💎 سیستم پیشرفته تحلیل الگوهای دیامتریک NEOWave
نسخه کامل و حرفه‌ای مبتنی بر تئوری Glenn Neely

الگو دیامتریک یکی از پیچیده‌ترین و دقیق‌ترین الگوهای NEOWave است که شامل:
- ساختار 7-موجی دقیق (A-B-C-D-E-F-G)
- قوانین هندسی پیچیده
- روابط زمانی و قیمتی خاص
- تحلیل مرکز هندسی
- پیش‌بینی حرکات پسا-الگو

ویژگی‌های کلیدی:
- تشخیص دقیق 6+ نوع دیامتریک
- اعتبارسنجی چندلایه براساس قوانین NEOWave
- تحلیل هندسی پیشرفته
- محاسبه مرکز جرم الگو
- ارزیابی تقارن و توازن
- پیش‌بینی targets پسا-الگو
"""

import numpy as np
import pandas as pd
import logging
from typing import List, Tuple, Dict, Optional, Union
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from scipy import stats, optimize
from scipy.spatial.distance import euclidean
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import warnings

logger = logging.getLogger(__name__)

class DiametricType(Enum):
    """انواع کامل الگوی دیامتریک NEOWave"""
    STANDARD = "standard_diametric"           # دیامتریک استاندارد
    BOW_TIE = "bow_tie_diametric"            # پروانه‌ای (امواج A,G بزرگ)
    DIAMOND = "diamond_diametric"             # الماسی (امواج میانی بزرگ)
    DIAMOND_SHAPED = "diamond_shaped"         # الماس تغییر شکل
    NEUTRAL_TRIANGLE = "neutral_triangle"     # مثلث خنثی
    SKEWED_TRIANGLE = "skewed_triangle"       # مثلث کج
    IRREGULAR_DIAMOND = "irregular_diamond"   # الماس نامنظم

class DiametricSubtype(Enum):
    """زیرانواع دیامتریک"""
    CONTRACTING = "contracting"    # انقباضی
    EXPANDING = "expanding"        # انبساطی
    NEUTRAL = "neutral"           # خنثی
    RUNNING = "running"           # در حال اجرا
    BARRIER = "barrier"           # سدی
    COMPLEX = "complex"           # پیچیده

class WaveLabel(Enum):
    """برچسب امواج دیامتریک"""
    A = "A"
    B = "B"
    C = "C"
    D = "D"  # مرکز الگو
    E = "E"
    F = "F"
    G = "G"

@dataclass
class DiametricWave:
    """جزئیات یک موج در الگوی دیامتریک"""
    label: WaveLabel
    start_index: int
    end_index: int
    start_price: float
    end_price: float
    amplitude: float
    duration: int
    slope: float
    direction: str  # 'up' or 'down'
    velocity: float  # amplitude/duration
    
    # روابط هندسی
    angle_to_center: float = 0.0
    distance_to_center: float = 0.0
    symmetry_score: float = 0.0
    
    # نسبت‌های فیبوناچی
    fibonacci_relations: Dict[str, float] = field(default_factory=dict)
    validation_score: float = 0.0

@dataclass
class GeometricProperties:
    """خصوصیات هندسی الگوی دیامتریک"""
    center_point: Tuple[float, float]          # مرکز هندسی
    center_of_mass: Tuple[float, float]        # مرکز جرم
    symmetry_axis: Dict[str, float]            # محور تقارن
    geometric_balance: float                    # توازن هندسی
    
    # اندازه‌گیری‌های هندسی
    maximum_radius: float = 0.0                # حداکثر شعاع
    minimum_radius: float = 0.0                # حداقل شعاع  
    aspect_ratio: float = 0.0                  # نسبت ابعاد
    area: float = 0.0                         # مساحت الگو
    perimeter: float = 0.0                    # محیط الگو
    
    # تحلیل تقارن
    radial_symmetry: float = 0.0              # تقارن شعاعی
    bilateral_symmetry: float = 0.0           # تقارن دوطرفه
    rotational_symmetry: float = 0.0          # تقارن چرخشی

@dataclass
class DiametricPattern:
    """الگوی کامل دیامتریک"""
    pattern_id: str
    pattern_type: DiametricType
    subtype: DiametricSubtype
    waves: List[DiametricWave]
    
    # خصوصیات کلی
    start_index: int
    end_index: int
    start_price: float
    end_price: float
    duration: int
    
    # تحلیل هندسی
    geometry: GeometricProperties
    
    # اعتبارسنجی
    is_valid: bool = False
    confidence_score: float = 0.0
    validation_errors: List[str] = field(default_factory=list)
    validation_details: Dict = field(default_factory=dict)
    
    # پیش‌بینی‌ها
    post_pattern_target: Optional[float] = None
    invalidation_level: Optional[float] = None
    reversal_probability: float = 0.0
    continuation_probability: float = 0.0
    
    # متادیتا
    identified_at: Optional[str] = None
    degree: int = 0

class DiametricAnalyzer:
    """تحلیلگر پیشرفته الگوهای دیامتریک NEOWave"""
    
    def __init__(self, data: pd.DataFrame, precision: float = 0.001):
        """
        راه‌اندازی تحلیلگر دیامتریک
        
        Args:
            data: داده‌های قیمتی OHLCV
            precision: دقت محاسبات هندسی
        """
        if data is None or data.empty:
            raise ValueError("داده‌های قیمتی نمی‌تواند خالی باشد")
            
        self.data = data.copy()
        self.precision = precision
        self.identified_diametrics = []
        
        # تنظیمات پیشرفته
        self.fibonacci_levels = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618, 2.618]
        self.geometric_tolerance = 0.05  # 5% تلرانس هندسی
        
        # آستانه‌های اعتبارسنجی
        self.validation_thresholds = {
            'min_confidence': 0.75,
            'min_symmetry': 0.65,
            'min_geometric_balance': 0.70,
            'time_equality_threshold': 0.3,  # 30% tolerance برای برابری زمان
            'price_relationship_threshold': 0.25
        }
        
        # Cache برای بهینه‌سازی
        self.geometry_cache = {}
        
        logger.info(f"DiametricAnalyzer راه‌اندازی شد با {len(data)} کندل")
        
    def identify_diametric(self, pivots: List[Tuple[int, float, str]], 
                         wave_degree: int = 0,
                         strict_validation: bool = True) -> Optional[DiametricPattern]:
        """
        شناسایی دقیق الگوی دیامتریک
        
        Args:
            pivots: لیست pivot points (index, price, type)
            wave_degree: درجه موج
            strict_validation: اعتبارسنجی سخت‌گیرانه
            
        Returns:
            DiametricPattern یا None
        """
        try:
            logger.info(f"شروع شناسایی الگوی دیامتریک در درجه {wave_degree}")
            
            # دیامتریک دقیقاً 7 موج دارد = 8 pivot point
            if len(pivots) < 8:
                logger.warning(f"تعداد pivot points کافی نیست: {len(pivots)} < 8")
                return None
                
            # انتخاب 8 pivot اول برای تحلیل
            pattern_pivots = pivots[:8]
            
            # ایجاد امواج از pivots
            waves = self._create_diametric_waves(pattern_pivots)
            if not waves or len(waves) != 7:
                logger.warning("نتوانست 7 موج معتبر ایجاد کند")
                return None
                
            # تحلیل هندسی
            geometry = self._analyze_geometry(waves)
            
            # تشخیص نوع دیامتریک
            pattern_type, subtype = self._classify_diametric(waves, geometry)
            
            # ایجاد الگوی اولیه
            pattern = DiametricPattern(
                pattern_id=f"DIAM_{wave_degree}_{pattern_pivots[0][0]}",
                pattern_type=pattern_type,
                subtype=subtype,
                waves=waves,
                start_index=pattern_pivots[0][0],
                end_index=pattern_pivots[-1][0],
                start_price=pattern_pivots[0][1],
                end_price=pattern_pivots[-1][1],
                duration=pattern_pivots[-1][0] - pattern_pivots[0][0],
                geometry=geometry,
                degree=wave_degree,
                identified_at=pd.Timestamp.now().isoformat()
            )
            
            # اعتبارسنجی کامل
            pattern.is_valid, pattern.confidence_score = self._validate_diametric_complete(
                pattern, strict_validation
            )
            
            if pattern.is_valid:
                # محاسبه پیش‌بینی‌ها
                self._calculate_post_pattern_implications(pattern)
                
                self.identified_diametrics.append(pattern)
                logger.info(f"✅ الگوی دیامتریک {pattern_type.value} شناسایی شد - اعتماد: {pattern.confidence_score:.2f}")
                return pattern
            else:
                logger.info(f"❌ الگوی دیامتریک رد شد - اعتماد: {pattern.confidence_score:.2f}")
                return None
                
        except Exception as e:
            logger.error(f"خطا در شناسایی دیامتریک: {e}")
            return None
    
    def _create_diametric_waves(self, pivots: List[Tuple]) -> List[DiametricWave]:
        """ایجاد 7 موج دیامتریک از pivot points"""
        try:
            waves = []
            wave_labels = [WaveLabel.A, WaveLabel.B, WaveLabel.C, WaveLabel.D,
                          WaveLabel.E, WaveLabel.F, WaveLabel.G]
            
            for i, label in enumerate(wave_labels):
                if i >= len(pivots) - 1:
                    break
                    
                start_pivot = pivots[i]
                end_pivot = pivots[i + 1]
                
                # محاسبه خصوصیات موج
                amplitude = abs(end_pivot[1] - start_pivot[1])
                duration = max(1, end_pivot[0] - start_pivot[0])
                slope = (end_pivot[1] - start_pivot[1]) / duration
                direction = 'up' if end_pivot[1] > start_pivot[1] else 'down'
                velocity = amplitude / duration
                
                wave = DiametricWave(
                    label=label,
                    start_index=start_pivot[0],
                    end_index=end_pivot[0],
                    start_price=start_pivot[1],
                    end_price=end_pivot[1],
                    amplitude=amplitude,
                    duration=duration,
                    slope=slope,
                    direction=direction,
                    velocity=velocity
                )
                
                # محاسبه نسبت‌های فیبوناچی
                self._calculate_wave_fibonacci_relations(wave, waves)
                
                waves.append(wave)
                
            logger.debug(f"ایجاد {len(waves)} موج دیامتریک")
            return waves
            
        except Exception as e:
            logger.error(f"خطا در ایجاد امواج دیامتریک: {e}")
            return []
    
    def _analyze_geometry(self, waves: List[DiametricWave]) -> GeometricProperties:
        """تحلیل جامع هندسی الگوی دیامتریک"""
        try:
            if len(waves) != 7:
                raise ValueError("برای تحلیل هندسی دقیقاً 7 موج نیاز است")
                
            # تبدیل امواج به نقاط هندسی
            points = []
            for wave in waves:
                points.append((wave.start_index, wave.start_price))
            points.append((waves[-1].end_index, waves[-1].end_price))  # نقطه پایانی
            
            # محاسبه مرکز هندسی
            center_point = self._calculate_geometric_center(points)
            
            # محاسبه مرکز جرم (با وزن‌دهی براساس amplitude)
            center_of_mass = self._calculate_center_of_mass(waves)
            
            # محاسبه محور تقارن
            symmetry_axis = self._calculate_symmetry_axis(points, center_point)
            
            # اندازه‌گیری‌های هندسی
            radii = [euclidean(point, center_point) for point in points]
            max_radius = max(radii)
            min_radius = min(radii)
            
            # محاسبه مساحت با الگوریتم Shoelace
            area = self._calculate_polygon_area(points)
            
            # محاسبه محیط
            perimeter = sum(euclidean(points[i], points[i+1]) 
                          for i in range(len(points)-1))
            perimeter += euclidean(points[-1], points[0])  # بستن چندضلعی
            
            # تحلیل انواع تقارن
            radial_symmetry = self._calculate_radial_symmetry(points, center_point)
            bilateral_symmetry = self._calculate_bilateral_symmetry(points, symmetry_axis)
            rotational_symmetry = self._calculate_rotational_symmetry(points, center_point)
            
            # محاسبه توازن هندسی کلی
            geometric_balance = self._calculate_geometric_balance(
                radial_symmetry, bilateral_symmetry, rotational_symmetry
            )
            
            geometry = GeometricProperties(
                center_point=center_point,
                center_of_mass=center_of_mass,
                symmetry_axis=symmetry_axis,
                geometric_balance=geometric_balance,
                maximum_radius=max_radius,
                minimum_radius=min_radius,
                aspect_ratio=max_radius / (min_radius + 1e-10),
                area=area,
                perimeter=perimeter,
                radial_symmetry=radial_symmetry,
                bilateral_symmetry=bilateral_symmetry,
                rotational_symmetry=rotational_symmetry
            )
            
            logger.debug(f"تحلیل هندسی کامل - توازن: {geometric_balance:.3f}")
            return geometry
            
        except Exception as e:
            logger.error(f"خطا در تحلیل هندسی: {e}")
            return GeometricProperties(
                center_point=(0, 0),
                center_of_mass=(0, 0),
                symmetry_axis={'slope': 0, 'intercept': 0},
                geometric_balance=0.0
            )
    
    def _calculate_geometric_center(self, points: List[Tuple]) -> Tuple[float, float]:
        """محاسبه مرکز هندسی (centroid)"""
        try:
            n = len(points)
            if n == 0:
                return (0, 0)
                
            x_sum = sum(p[0] for p in points)
            y_sum = sum(p[1] for p in points)
            
            return (x_sum / n, y_sum / n)
            
        except:
            return (0, 0)
    
    def _calculate_center_of_mass(self, waves: List[DiametricWave]) -> Tuple[float, float]:
        """محاسبه مرکز جرم با وزن‌دهی amplitude"""
        try:
            total_weight = sum(wave.amplitude for wave in waves)
            if total_weight == 0:
                return (0, 0)
                
            weighted_x = sum(wave.start_index * wave.amplitude for wave in waves)
            weighted_y = sum(wave.start_price * wave.amplitude for wave in waves)
            
            return (weighted_x / total_weight, weighted_y / total_weight)
            
        except:
            return (0, 0)
    
    def _calculate_symmetry_axis(self, points: List[Tuple], 
                               center: Tuple[float, float]) -> Dict[str, float]:
        """محاسبه محور تقارن اصلی"""
        try:
            if len(points) < 3:
                return {'slope': 0, 'intercept': 0, 'r_squared': 0}
                
            # انتقال نقاط نسبت به مرکز
            translated_points = [(p[0] - center[0], p[1] - center[1]) for p in points]
            
            # یافتن بهترین خط با PCA
            points_array = np.array(translated_points)
            
            # محاسبه مؤلفه‌های اصلی
            cov_matrix = np.cov(points_array.T)
            eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
            
            # انتخاب eigenvector با بزرگ‌ترین eigenvalue
            main_direction = eigenvectors[:, np.argmax(eigenvalues)]
            
            # محاسبه شیب
            if abs(main_direction[0]) > 1e-10:
                slope = main_direction[1] / main_direction[0]
            else:
                slope = float('inf')  # خط عمودی
                
            # محاسبه y-intercept
            intercept = center[1] - slope * center[0] if slope != float('inf') else center[0]
            
            # محاسبه R-squared برای کیفیت fit
            r_squared = max(eigenvalues) / sum(eigenvalues) if sum(eigenvalues) > 0 else 0
            
            return {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_squared
            }
            
        except Exception as e:
            logger.warning(f"خطا در محاسبه محور تقارن: {e}")
            return {'slope': 0, 'intercept': 0, 'r_squared': 0}
    
    def _calculate_polygon_area(self, points: List[Tuple]) -> float:
        """محاسبه مساحت چندضلعی با فرمول Shoelace"""
        try:
            if len(points) < 3:
                return 0.0
                
            n = len(points)
            area = 0.0
            
            for i in range(n):
                j = (i + 1) % n
                area += points[i][0] * points[j][1]
                area -= points[j][0] * points[i][1]
                
            return abs(area) / 2.0
            
        except:
            return 0.0
    
    def _calculate_radial_symmetry(self, points: List[Tuple], 
                                 center: Tuple[float, float]) -> float:
        """محاسبه تقارن شعاعی"""
        try:
            # محاسبه فواصل از مرکز
            distances = [euclidean(point, center) for point in points]
            
            if len(distances) < 2:
                return 0.0
                
            # محاسبه ضریب تغییرات (کمتر = تقارن بیشتر)
            mean_dist = np.mean(distances)
            std_dist = np.std(distances)
            
            if mean_dist == 0:
                return 1.0 if std_dist == 0 else 0.0
                
            cv = std_dist / mean_dist
            
            # تبدیل به امتیاز تقارن (0 تا 1)
            symmetry = 1 / (1 + cv)
            
            return min(1.0, symmetry)
            
        except:
            return 0.0
    
    def _calculate_bilateral_symmetry(self, points: List[Tuple], 
                                    axis: Dict[str, float]) -> float:
        """محاسبه تقارن دوطرفه نسبت به محور"""
        try:
            if len(points) < 4:
                return 0.0
                
            slope = axis.get('slope', 0)
            intercept = axis.get('intercept', 0)
            
            # محاسبه فاصله نقاط از محور تقارن
            distances = []
            
            for point in points:
                x, y = point
                
                if slope == float('inf'):  # خط عمودی
                    distance = abs(x - intercept)
                else:
                    # فاصله نقطه از خط: |ax + by + c| / sqrt(a² + b²)
                    # خط: y = mx + b → mx - y + b = 0
                    distance = abs(slope * x - y + intercept) / np.sqrt(slope**2 + 1)
                    
                distances.append(distance)
                
            # تقارن بر اساس توزیع فواصل
            mean_dist = np.mean(distances)
            std_dist = np.std(distances)
            
            if mean_dist == 0:
                return 1.0 if std_dist == 0 else 0.0
                
            cv = std_dist / mean_dist
            symmetry = 1 / (1 + cv)
            
            return min(1.0, symmetry)
            
        except:
            return 0.0
    
    def _calculate_rotational_symmetry(self, points: List[Tuple], 
                                     center: Tuple[float, float]) -> float:
        """محاسبه تقارن چرخشی"""
        try:
            if len(points) < 3:
                return 0.0
                
            # محاسبه زوایای نقاط نسبت به مرکز
            angles = []
            for point in points:
                dx = point[0] - center[0]
                dy = point[1] - center[1]
                angle = np.arctan2(dy, dx)
                angles.append(angle)
                
            # مرتب‌سازی زوایا
            angles.sort()
            
            # محاسبه اختلاف زوایای متوالی
            angle_diffs = []
            n = len(angles)
            
            for i in range(n):
                diff = angles[(i + 1) % n] - angles[i]
                if diff < 0:
                    diff += 2 * np.pi  # تصحیح برای زاویه منفی
                angle_diffs.append(diff)
                
            # زاویه ایده‌آل برای تقسیم مساوی
            ideal_angle = 2 * np.pi / n
            
            # محاسبه انحراف از توزیع مساوی
            deviations = [abs(diff - ideal_angle) for diff in angle_diffs]
            mean_deviation = np.mean(deviations)
            
            # تبدیل به امتیاز تقارن
            max_possible_deviation = np.pi  # حداکثر انحراف ممکن
            symmetry = 1 - (mean_deviation / max_possible_deviation)
            
            return max(0.0, min(1.0, symmetry))
            
        except:
            return 0.0
    
    def _calculate_geometric_balance(self, radial: float, bilateral: float, 
                                   rotational: float) -> float:
        """محاسبه توازن هندسی کلی"""
        try:
            # وزن‌دهی انواع تقارن
            weights = [0.4, 0.35, 0.25]  # radial, bilateral, rotational
            symmetries = [radial, bilateral, rotational]
            
            # میانگین وزن‌دار
            balance = sum(w * s for w, s in zip(weights, symmetries))
            
            return min(1.0, balance)
            
        except:
            return 0.0
    
    def _classify_diametric(self, waves: List[DiametricWave], 
                          geometry: GeometricProperties) -> Tuple[DiametricType, DiametricSubtype]:
        """تشخیص دقیق نوع و زیرنوع دیامتریک"""
        try:
            if len(waves) != 7:
                return DiametricType.STANDARD, DiametricSubtype.NEUTRAL
                
            # آنالیز الگوی اندازه موج‌ها
            amplitudes = [wave.amplitude for wave in waves]
            
            # تشخیص الگوی اصلی
            pattern_type = self._determine_main_pattern(amplitudes, geometry)
            
            # تشخیص زیرنوع براساس رفتار کلی
            subtype = self._determine_subtype(waves, geometry)
            
            return pattern_type, subtype
            
        except Exception as e:
            logger.warning(f"خطا در طبقه‌بندی دیامتریک: {e}")
            return DiametricType.STANDARD, DiametricSubtype.NEUTRAL
    
    def _determine_main_pattern(self, amplitudes: List[float], 
                              geometry: GeometricProperties) -> DiametricType:
        """تعیین الگوی اصلی براساس توزیع amplitudes"""
        try:
            if len(amplitudes) != 7:
                return DiametricType.STANDARD
                
            # نرمال‌سازی amplitudes
            max_amp = max(amplitudes)
            normalized_amps = [amp / max_amp for amp in amplitudes]
            
            # BOW-TIE: امواج A و G بزرگ
            if (normalized_amps[0] > 0.8 and normalized_amps[6] > 0.8 and
                max(normalized_amps[1:6]) < 0.7):
                return DiametricType.BOW_TIE
                
            # DIAMOND: امواج میانی (C, D, E) بزرگ
            middle_amps = normalized_amps[2:5]
            if (np.mean(middle_amps) > 0.8 and
                normalized_amps[0] < 0.6 and normalized_amps[6] < 0.6):
                return DiametricType.DIAMOND
                
            # DIAMOND_SHAPED: الگوی تدریجی افزایش و کاهش
            if self._is_diamond_shaped_pattern(normalized_amps):
                return DiametricType.DIAMOND_SHAPED
                
            # NEUTRAL_TRIANGLE: amplitudes تقریباً برابر
            cv = np.std(normalized_amps) / np.mean(normalized_amps)
            if cv < 0.3:
                return DiametricType.NEUTRAL_TRIANGLE
                
            # SKEWED_TRIANGLE: عدم تعادل در amplitudes
            if cv > 0.6:
                return DiametricType.SKEWED_TRIANGLE
                
            # IRREGULAR_DIAMOND: ترکیب خصوصیات مختلف
            if (geometry.radial_symmetry < 0.6 and 
                geometry.bilateral_symmetry > 0.7):
                return DiametricType.IRREGULAR_DIAMOND
                
            return DiametricType.STANDARD
            
        except:
            return DiametricType.STANDARD
    
    def _is_diamond_shaped_pattern(self, amplitudes: List[float]) -> bool:
        """بررسی الگوی الماسی تدریجی"""
        try:
            # الگو باید از کوچک شروع شود، به اوج برسد، و دوباره کوچک شود
            n = len(amplitudes)
            mid_point = n // 2
            
            # نیمه اول: افزایشی
            first_half = amplitudes[:mid_point + 1]
            increasing = all(first_half[i] <= first_half[i + 1] 
                           for i in range(len(first_half) - 1))
            
            # نیمه دوم: کاهشی  
            second_half = amplitudes[mid_point:]
            decreasing = all(second_half[i] >= second_half[i + 1] 
                           for i in range(len(second_half) - 1))
            
            return increasing and decreasing
            
        except:
            return False
    
    def _determine_subtype(self, waves: List[DiametricWave], 
                         geometry: GeometricProperties) -> DiametricSubtype:
        """تعیین زیرنوع براساس رفتار کلی"""
        try:
            amplitudes = [wave.amplitude for wave in waves]
            durations = [wave.duration for wave in waves]
            
            # CONTRACTING: امواج کوچک‌تر می‌شوند
            amp_trend = np.polyfit(range(len(amplitudes)), amplitudes, 1)[0]
            if amp_trend < -0.1 * np.mean(amplitudes):
                return DiametricSubtype.CONTRACTING
                
            # EXPANDING: امواج بزرگ‌تر می‌شوند
            if amp_trend > 0.1 * np.mean(amplitudes):
                return DiametricSubtype.EXPANDING
                
            # RUNNING: الگو به سمت یک جهت متمایل
            if abs(waves[0].start_price - waves[-1].end_price) > np.mean(amplitudes):
                return DiametricSubtype.RUNNING
                
            # BARRIER: یک طرف الگو تقریباً مسطح
            if geometry.bilateral_symmetry < 0.5:
                return DiametricSubtype.BARRIER
                
            # COMPLEX: ترکیب پیچیده خصوصیات
            if (geometry.geometric_balance < 0.6 and 
                len(set(wave.direction for wave in waves)) > 1):
                return DiametricSubtype.COMPLEX
                
            return DiametricSubtype.NEUTRAL
            
        except:
            return DiametricSubtype.NEUTRAL
    
    def _validate_diametric_complete(self, pattern: DiametricPattern, 
                                   strict: bool = True) -> Tuple[bool, float]:
        """اعتبارسنجی کامل الگوی دیامتریک"""
        try:
            confidence_factors = []
            errors = []
            warnings = []
            
            # بررسی تعداد امواج
            if len(pattern.waves) == 7:
                confidence_factors.append(0.15)
            else:
                errors.append(f"تعداد امواج نادرست: {len(pattern.waves)} != 7")
                
            # بررسی برابری نسبی زمان امواج (قانون اصلی دیامتریک)
            time_equality_score = self._validate_time_equality(pattern.waves)
            if time_equality_score >= self.validation_thresholds['time_equality_threshold']:
                confidence_factors.append(0.25)
            else:
                errors.append(f"عدم رعایت برابری زمان: {time_equality_score:.2f}")
                
            # بررسی توازن هندسی
            if pattern.geometry.geometric_balance >= self.validation_thresholds['min_geometric_balance']:
                confidence_factors.append(0.20)
            else:
                warnings.append(f"توازن هندسی ضعیف: {pattern.geometry.geometric_balance:.2f}")
                
            # بررسی تقارن
            symmetry_score = (pattern.geometry.radial_symmetry + 
                            pattern.geometry.bilateral_symmetry + 
                            pattern.geometry.rotational_symmetry) / 3
            
            if symmetry_score >= self.validation_thresholds['min_symmetry']:
                confidence_factors.append(0.15)
            else:
                warnings.append(f"تقارن ناکافی: {symmetry_score:.2f}")
                
            # بررسی نسبت‌های قیمتی
            price_relationship_score = self._validate_price_relationships(pattern.waves)
            if price_relationship_score >= self.validation_thresholds['price_relationship_threshold']:
                confidence_factors.append(0.15)
            else:
                warnings.append(f"روابط قیمتی ضعیف: {price_relationship_score:.2f}")
                
            # بررسی continuity (پیوستگی امواج)
            continuity_score = self._validate_wave_continuity(pattern.waves)
            confidence_factors.append(0.10 * continuity_score)
            
            # اعتبارسنجی خاص نوع الگو
            type_specific_score = self._validate_pattern_type_specific(pattern)
            confidence_factors.append(0.10 * type_specific_score)
            
            # محاسبه اعتماد کلی
            total_confidence = sum(confidence_factors)
            
            # تعیین اعتبار
            min_confidence = self.validation_thresholds['min_confidence'] if strict else 0.6
            is_valid = (total_confidence >= min_confidence and 
                       len(errors) == 0 and 
                       (len(warnings) <= 2 or not strict))
            
            # ذخیره جزئیات اعتبارسنجی
            pattern.validation_errors = errors
            pattern.validation_warnings = warnings
            pattern.validation_details = {
                'time_equality_score': time_equality_score,
                'geometric_balance': pattern.geometry.geometric_balance,
                'symmetry_score': symmetry_score,
                'price_relationship_score': price_relationship_score,
                'continuity_score': continuity_score,
                'type_specific_score': type_specific_score,
                'confidence_breakdown': {
                    'wave_count': 0.15 if len(pattern.waves) == 7 else 0,
                    'time_equality': 0.25 if time_equality_score >= self.validation_thresholds['time_equality_threshold'] else 0,
                    'geometric_balance': 0.20 if pattern.geometry.geometric_balance >= self.validation_thresholds['min_geometric_balance'] else 0,
                    'symmetry': 0.15 if symmetry_score >= self.validation_thresholds['min_symmetry'] else 0,
                    'price_relationships': 0.15 if price_relationship_score >= self.validation_thresholds['price_relationship_threshold'] else 0,
                    'continuity': 0.10 * continuity_score,
                    'type_specific': 0.10 * type_specific_score
                }
            }
            
            logger.debug(f"اعتبارسنجی دیامتریک - معتبر: {is_valid}, اعتماد: {total_confidence:.3f}")
            return is_valid, total_confidence
            
        except Exception as e:
            logger.error(f"خطا در اعتبارسنجی دیامتریک: {e}")
            return False, 0.0
    
    def _validate_time_equality(self, waves: List[DiametricWave]) -> float:
        """اعتبارسنجی برابری نسبی زمان امواج"""
        try:
            durations = [wave.duration for wave in waves]
            
            # محاسبه ضریب تغییرات
            mean_duration = np.mean(durations)
            std_duration = np.std(durations)
            
            if mean_duration == 0:
                return 0.0
                
            cv = std_duration / mean_duration
            
            # تبدیل به امتیاز (کمتر بودن CV = برابری بیشتر)
            equality_score = 1 / (1 + cv)
            
            return min(1.0, equality_score)
            
        except:
            return 0.0
    
    def _validate_price_relationships(self, waves: List[DiametricWave]) -> float:
        """اعتبارسنجی روابط قیمتی امواج"""
        try:
            amplitudes = [wave.amplitude for wave in waves]
            
            # بررسی نسبت‌های فیبوناچی بین امواج
            fibonacci_matches = 0
            total_comparisons = 0
            
            for i in range(len(amplitudes)):
                for j in range(i + 1, len(amplitudes)):
                    ratio = amplitudes[i] / amplitudes[j] if amplitudes[j] > 0 else 0
                    
                    # یافتن نزدیک‌ترین سطح فیبوناچی
                    best_match = min(self.fibonacci_levels, 
                                   key=lambda x: abs(x - ratio))
                    
                    # اگر نزدیک به سطح فیبوناچی باشد
                    if abs(ratio - best_match) / best_match < 0.1:  # 10% tolerance
                        fibonacci_matches += 1
                        
                    total_comparisons += 1
                    
            if total_comparisons == 0:
                return 0.0
                
            return fibonacci_matches / total_comparisons
            
        except:
            return 0.0
    
    def _validate_wave_continuity(self, waves: List[DiametricWave]) -> float:
        """اعتبارسنجی پیوستگی امواج"""
        try:
            continuity_score = 0.0
            
            for i in range(len(waves) - 1):
                current_wave = waves[i]
                next_wave = waves[i + 1]
                
                # بررسی اتصال امواج
                if (current_wave.end_index == next_wave.start_index and
                    abs(current_wave.end_price - next_wave.start_price) < self.precision):
                    continuity_score += 1
                    
            return continuity_score / (len(waves) - 1) if len(waves) > 1 else 0
            
        except:
            return 0.0
    
    def _validate_pattern_type_specific(self, pattern: DiametricPattern) -> float:
        """اعتبارسنجی خاص نوع الگو"""
        try:
            if pattern.pattern_type == DiametricType.BOW_TIE:
                return self._validate_bow_tie_specific(pattern)
            elif pattern.pattern_type == DiametricType.DIAMOND:
                return self._validate_diamond_specific(pattern)
            elif pattern.pattern_type == DiametricType.NEUTRAL_TRIANGLE:
                return self._validate_neutral_triangle_specific(pattern)
            else:
                return 0.7  # امتیاز پیش‌فرض برای انواع استاندارد
                
        except:
            return 0.0
    
    def _validate_bow_tie_specific(self, pattern: DiametricPattern) -> float:
        """اعتبارسنجی خاص Bow-Tie"""
        amplitudes = [wave.amplitude for wave in pattern.waves]
        
        # امواج A و G باید بزرگ‌ترین باشند
        if (amplitudes[0] >= max(amplitudes[1:6]) * 0.8 and
            amplitudes[6] >= max(amplitudes[1:6]) * 0.8):
            return 1.0
        return 0.3
    
    def _validate_diamond_specific(self, pattern: DiametricPattern) -> float:
        """اعتبارسنجی خاص Diamond"""
        amplitudes = [wave.amplitude for wave in pattern.waves]
        
        # امواج میانی باید بزرگ‌ترین باشند
        middle_max = max(amplitudes[2:5])
        outer_max = max([amplitudes[0], amplitudes[1], amplitudes[5], amplitudes[6]])
        
        if middle_max > outer_max * 1.2:
            return 1.0
        return 0.4
    
    def _validate_neutral_triangle_specific(self, pattern: DiametricPattern) -> float:
        """اعتبارسنجی خاص Neutral Triangle"""
        amplitudes = [wave.amplitude for wave in pattern.waves]
        
        # امواج باید تقریباً برابر باشند
        cv = np.std(amplitudes) / np.mean(amplitudes)
        if cv < 0.3:
            return 1.0
        return max(0.0, 1.0 - cv)
    
    def _calculate_post_pattern_implications(self, pattern: DiametricPattern):
        """محاسبه پیامدهای پسا-الگو"""
        try:
            waves = pattern.waves
            amplitudes = [wave.amplitude for wave in waves]
            avg_amplitude = np.mean(amplitudes)
            
            # محاسبه اهداف احتمالی
            # دیامتریک معمولاً نشان‌دهنده پایان یک حرکت و شروع حرکت معکوس است
            
            # هدف حداقل: 61.8% متوسط amplitudes
            min_target = avg_amplitude * 0.618
            
            # هدف عادی: برابر متوسط amplitudes
            normal_target = avg_amplitude
            
            # هدف حداکثر: 161.8% متوسط amplitudes
            max_target = avg_amplitude * 1.618
            
            # تعیین جهت حرکت بعدی
            last_wave = waves[-1]
            start_price = pattern.start_price
            end_price = pattern.end_price
            
            # اگر الگو نزولی است، حرکت بعدی احتمالاً صعودی
            if end_price < start_price:
                pattern.post_pattern_target = end_price + normal_target
                pattern.reversal_probability = 0.75
            else:
                pattern.post_pattern_target = end_price - normal_target
                pattern.reversal_probability = 0.75
                
            pattern.continuation_probability = 1.0 - pattern.reversal_probability
            
            # سطح باطل‌سازی
            # معمولاً شکست مرکز الگو (موج D) الگو را باطل می‌کند
            if len(waves) >= 4:
                d_wave = waves[3]  # موج D
                pattern.invalidation_level = d_wave.end_price
                
            logger.debug(f"پیامدهای پسا-الگو محاسبه شد - هدف: {pattern.post_pattern_target}")
            
        except Exception as e:
            logger.error(f"خطا در محاسبه پیامدهای پسا-الگو: {e}")
    
    def _calculate_wave_fibonacci_relations(self, wave: DiametricWave, 
                                          previous_waves: List[DiametricWave]):
        """محاسبه روابط فیبوناچی موج با امواج قبلی"""
        try:
            relations = {}
            
            for i, prev_wave in enumerate(previous_waves):
                if prev_wave.amplitude > 0:
                    ratio = wave.amplitude / prev_wave.amplitude
                    
                    # یافتن نزدیک‌ترین سطح فیبوناچی
                    closest_fib = min(self.fibonacci_levels,
                                    key=lambda x: abs(x - ratio))
                    
                    relations[f'vs_wave_{prev_wave.label.value}'] = {
                        'ratio': ratio,
                        'closest_fibonacci': closest_fib,
                        'accuracy': 1 - abs(ratio - closest_fib) / closest_fib
                    }
                    
            wave.fibonacci_relations = relations
            
        except Exception as e:
            logger.warning(f"خطا در محاسبه روابط فیبوناچی: {e}")
    
    def get_diametric_by_id(self, pattern_id: str) -> Optional[DiametricPattern]:
        """دریافت الگوی دیامتریک بر اساس ID"""
        for pattern in self.identified_diametrics:
            if pattern.pattern_id == pattern_id:
                return pattern
        return None
    
    def get_active_diametrics(self, current_index: int) -> List[DiametricPattern]:
        """دریافت الگوهای دیامتریک فعال"""
        return [
            pattern for pattern in self.identified_diametrics
            if (pattern.start_index <= current_index <= pattern.end_index and 
                pattern.is_valid)
        ]
    
    def generate_diametric_report(self, patterns: List[DiametricPattern] = None) -> Dict:
        """تولید گزارش جامع الگوهای دیامتریک"""
        if patterns is None:
            patterns = [p for p in self.identified_diametrics if p.is_valid]
            
        try:
            from collections import Counter
            
            report = {
                'summary': {
                    'total_patterns': len(patterns),
                    'pattern_types': dict(Counter(p.pattern_type.value for p in patterns)),
                    'subtypes': dict(Counter(p.subtype.value for p in patterns)),
                    'average_confidence': np.mean([p.confidence_score for p in patterns]) if patterns else 0,
                    'generated_at': pd.Timestamp.now().isoformat()
                },
                'detailed_analysis': [],
                'geometric_statistics': {},
                'recommendations': []
            }
            
            # تحلیل تفصیلی هر الگو
            for pattern in patterns:
                detail = {
                    'id': pattern.pattern_id,
                    'type': pattern.pattern_type.value,
                    'subtype': pattern.subtype.value,
                    'confidence': pattern.confidence_score,
                    'duration': pattern.duration,
                    'geometry': {
                        'geometric_balance': pattern.geometry.geometric_balance,
                        'radial_symmetry': pattern.geometry.radial_symmetry,
                        'bilateral_symmetry': pattern.geometry.bilateral_symmetry,
                        'rotational_symmetry': pattern.geometry.rotational_symmetry,
                        'aspect_ratio': pattern.geometry.aspect_ratio
                    },
                    'predictions': {
                        'target': pattern.post_pattern_target,
                        'invalidation': pattern.invalidation_level,
                        'reversal_probability': pattern.reversal_probability
                    }
                }
                report['detailed_analysis'].append(detail)
                
            # آمار هندسی کلی
            if patterns:
                geometric_balances = [p.geometry.geometric_balance for p in patterns]
                symmetries = [p.geometry.radial_symmetry for p in patterns]
                
                report['geometric_statistics'] = {
                    'average_geometric_balance': np.mean(geometric_balances),
                    'balance_std': np.std(geometric_balances),
                    'average_symmetry': np.mean(symmetries),
                    'symmetry_std': np.std(symmetries),
                    'quality_distribution': {
                        'high_quality': len([p for p in patterns if p.confidence_score >= 0.8]),
                        'medium_quality': len([p for p in patterns if 0.6 <= p.confidence_score < 0.8]),
                        'low_quality': len([p for p in patterns if p.confidence_score < 0.6])
                    }
                }
                
            # توصیه‌ها
            report['recommendations'] = self._generate_diametric_recommendations(patterns)
            
            return report
            
        except Exception as e:
            logger.error(f"خطا در تولید گزارش دیامتریک: {e}")
            return {'error': str(e)}
    
    def _generate_diametric_recommendations(self, patterns: List[DiametricPattern]) -> List[str]:
        """تولید توصیه‌های عملی برای الگوهای دیامتریک"""
        recommendations = []
        
        try:
            if not patterns:
                recommendations.append("هیچ الگوی دیامتریک معتبر شناسایی نشد")
                return recommendations
                
            # بهترین الگو
            best_pattern = max(patterns, key=lambda p: p.confidence_score)
            recommendations.append(f"قوی‌ترین الگو: {best_pattern.pattern_type.value} با اعتماد {best_pattern.confidence_score:.1%}")
            
            # توصیه بر اساس نوع الگو
            if best_pattern.pattern_type == DiametricType.BOW_TIE:
                recommendations.append("الگوی Bow-Tie نشان‌دهنده تغییر روند قوی است")
            elif best_pattern.pattern_type == DiametricType.DIAMOND:
                recommendations.append("الگوی Diamond احتمال برگشت قیمت را افزایش می‌دهد")
                
            # توصیه target
            if best_pattern.post_pattern_target:
                recommendations.append(f"هدف احتمالی: {best_pattern.post_pattern_target:.2f}")
                
            # توصیه invalidation
            if best_pattern.invalidation_level:
                recommendations.append(f"سطح باطل‌سازی: {best_pattern.invalidation_level:.2f}")
                
            # توصیه بر اساس احتمال برگشت
            if best_pattern.reversal_probability > 0.7:
                recommendations.append("احتمال بالای برگشت روند - آماده باش برای تغییر جهت")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"خطا در تولید توصیه‌ها: {e}")
            return ["خطا در تولید توصیه‌های دیامتریک"]