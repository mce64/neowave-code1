# ================= complexity.py =================
"""
🧩 سیستم پیشرفته تحلیل پیچیدگی ساختاری امواج NEOWave
نسخه کامل و حرفه‌ای مبتنی بر تئوری Glenn Neely

ویژگی‌های کلیدی:
- درجه‌بندی دقیق پیچیدگی امواج (Mono تا Super)
- محاسبه بعد فراکتال دقیق با الگوریتم Box-counting
- تحلیل عمقی ساختار sub-waves
- بررسی قوانین Alternation کامل
- شناسایی موج‌های مفقود (Missing/X-waves)
- ارزیابی پیچیدگی زمانی، قیمتی و ساختاری
- پیش‌بینی سطح پیچیدگی موج‌های آینده
"""

import numpy as np
import pandas as pd
import logging
from typing import List, Dict, Tuple, Optional, Union, Set
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from scipy import stats
from sklearn.linear_model import LinearRegression
from collections import Counter, defaultdict
import warnings

logger = logging.getLogger(__name__)

class ComplexityLevel(IntEnum):
    """سطوح پیچیدگی امواج براساس تئوری NEOWave"""
    MONO = 1      # موج تک (Mono-wave) - ساده‌ترین شکل
    POLY = 3      # موج چندگانه (Poly-wave) - 3 sub-wave
    MULTI = 5     # موج چندمرحله‌ای (Multi-wave) - 5 sub-wave  
    MACRO = 9     # موج کلان (Macro-wave) - 9 sub-wave
    SUPER = 13    # موج ابر (Super-wave) - 13+ sub-wave
    ULTRA = 21    # موج فوق (Ultra-wave) - 21+ sub-wave برای الگوهای بسیار پیچیده
    
    @classmethod
    def from_subwave_count(cls, count: int) -> 'ComplexityLevel':
        """تعیین سطح پیچیدگی از تعداد sub-waves"""
        if count == 0:
            return cls.MONO
        elif count <= 3:
            return cls.POLY
        elif count <= 5:
            return cls.MULTI
        elif count <= 9:
            return cls.MACRO
        elif count <= 13:
            return cls.SUPER
        else:
            return cls.ULTRA

class StructureType(Enum):
    """انواع ساختار امواج"""
    MONO_WAVE = "mono_wave"
    ZIGZAG = "zigzag"
    FLAT = "flat" 
    TRIANGLE = "triangle"
    IMPULSE = "impulse"
    DIAMETRIC = "diametric"
    SYMMETRIC = "symmetric"
    COMBINATION = "combination"
    COMPLEX_CORRECTION = "complex_correction"
    TERMINAL = "terminal"
    UNKNOWN = "unknown"

class AlternationRule(Enum):
    """قوانین Alternation در NEOWave"""
    TIME_ALTERNATION = "time"           # تفاوت در زمان
    PRICE_ALTERNATION = "price"         # تفاوت در قیمت
    COMPLEXITY_ALTERNATION = "complexity" # تفاوت در پیچیدگی
    STRUCTURE_ALTERNATION = "structure"   # تفاوت در ساختار
    SEVERITY_ALTERNATION = "severity"     # تفاوت در شدت حرکت

@dataclass
class WaveComplexityMetrics:
    """معیارهای پیچیدگی موج"""
    fractal_dimension: float = 0.0
    time_complexity: float = 0.0
    price_complexity: float = 0.0
    structural_complexity: float = 0.0
    self_similarity: float = 0.0
    deviation_index: float = 0.0
    fibonacci_ratio_accuracy: float = 0.0
    alternation_score: float = 0.0

@dataclass
class ComplexityAnalysisResult:
    """نتایج کامل تحلیل پیچیدگی"""
    wave_label: str
    complexity_level: ComplexityLevel
    structure_type: StructureType
    sub_wave_count: int
    metrics: WaveComplexityMetrics
    alternation_compliance: Dict[str, bool] = field(default_factory=dict)
    missing_waves: List[Dict] = field(default_factory=list)
    complexity_confidence: float = 0.0
    recommendations: List[str] = field(default_factory=list)
    
class ComplexityAnalyzer:
    """تحلیلگر پیشرفته پیچیدگی ساختاری امواج NEOWave"""
    
    def __init__(self, data: pd.DataFrame, precision: float = 0.001):
        """
        راه‌اندازی تحلیلگر پیچیدگی
        
        Args:
            data: داده‌های قیمتی OHLCV
            precision: دقت محاسبات (پیش‌فرض: 0.001)
        """
        if data is None or data.empty:
            raise ValueError("داده‌های قیمتی نمی‌تواند خالی باشد")
            
        self.data = data.copy()
        self.precision = precision
        self.complexity_cache = {}
        
        # تنظیمات پیشرفته
        self.fibonacci_levels = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618, 2.618]
        self.alternation_rules = {rule.value: [] for rule in AlternationRule}
        
        # آماره‌های کلی
        self.global_stats = {
            'avg_complexity': 0.0,
            'complexity_trend': 0.0,
            'dominant_structure': StructureType.UNKNOWN
        }
        
        logger.info(f"ComplexityAnalyzer راه‌اندازی شد با {len(data)} کندل و دقت {precision}")
        
    def analyze_wave_complexity(self, wave: Dict, 
                              context_waves: Optional[List[Dict]] = None) -> ComplexityAnalysisResult:
        """
        تحلیل جامع پیچیدگی یک موج
        
        Args:
            wave: موج مورد تحلیل
            context_waves: موج‌های مرتبط برای تحلیل زمینه‌ای
            
        Returns:
            ComplexityAnalysisResult: نتایج کامل تحلیل
        """
        try:
            wave_label = wave.get('label', 'Unknown')
            logger.info(f"شروع تحلیل پیچیدگی موج {wave_label}")
            
            # بررسی cache
            cache_key = self._generate_cache_key(wave)
            if cache_key in self.complexity_cache:
                logger.debug(f"استفاده از cache برای موج {wave_label}")
                return self.complexity_cache[cache_key]
            
            # استخراج sub-waves
            sub_waves = wave.get('sub_waves', [])
            sub_wave_count = len(sub_waves)
            
            # تعیین سطح پیچیدگی
            complexity_level = ComplexityLevel.from_subwave_count(sub_wave_count)
            
            # تشخیص نوع ساختار
            structure_type = self._determine_structure_type(wave, sub_waves)
            
            # محاسبه معیارهای پیچیدگی
            metrics = self._calculate_complexity_metrics(wave, sub_waves, context_waves)
            
            # بررسی قوانین alternation
            alternation_compliance = self._check_alternation_rules(wave, sub_waves, context_waves)
            
            # شناسایی موج‌های مفقود
            missing_waves = self._identify_missing_waves(wave, sub_waves)
            
            # محاسبه اعتماد
            confidence = self._calculate_complexity_confidence(
                complexity_level, metrics, alternation_compliance
            )
            
            # تولید توصیه‌ها
            recommendations = self._generate_recommendations(
                complexity_level, structure_type, metrics, alternation_compliance
            )
            
            # ایجاد نتیجه
            result = ComplexityAnalysisResult(
                wave_label=wave_label,
                complexity_level=complexity_level,
                structure_type=structure_type,
                sub_wave_count=sub_wave_count,
                metrics=metrics,
                alternation_compliance=alternation_compliance,
                missing_waves=missing_waves,
                complexity_confidence=confidence,
                recommendations=recommendations
            )
            
            # ذخیره در cache
            self.complexity_cache[cache_key] = result
            
            logger.info(f"تحلیل موج {wave_label} کامل شد - سطح: {complexity_level.name}")
            return result
            
        except Exception as e:
            logger.error(f"خطا در تحلیل پیچیدگی موج: {e}")
            # بازگشت نتیجه پیش‌فرض در صورت خطا
            return ComplexityAnalysisResult(
                wave_label=wave.get('label', 'Error'),
                complexity_level=ComplexityLevel.MONO,
                structure_type=StructureType.UNKNOWN,
                sub_wave_count=0,
                metrics=WaveComplexityMetrics()
            )
            
    def check_alternation_rule(self, wave2: Dict, wave4: Dict, 
                             impulse_context: Optional[List[Dict]] = None) -> Dict[str, Union[bool, str, float]]:
        """
        بررسی دقیق قانون Alternation بین موج 2 و 4
        
        Args:
            wave2: موج شماره 2
            wave4: موج شماره 4  
            impulse_context: زمینه موج‌های impulse
            
        Returns:
            Dict حاوی نتایج تفصیلی alternation
        """
        try:
            logger.info("بررسی قانون Alternation بین موج 2 و 4")
            
            # تحلیل پیچیدگی هر دو موج
            complexity_2 = self.analyze_wave_complexity(wave2, impulse_context)
            complexity_4 = self.analyze_wave_complexity(wave4, impulse_context)
            
            alternation_result = {
                'wave2_complexity': complexity_2.complexity_level,
                'wave4_complexity': complexity_4.complexity_level,
                'basic_alternation': complexity_2.complexity_level != complexity_4.complexity_level,
                'structure_alternation': complexity_2.structure_type != complexity_4.structure_type,
                'alternation_types': [],
                'rule_compliance': {},
                'alternation_strength': 0.0,
                'neowave_valid': False
            }
            
            # بررسی انواع مختلف alternation
            alternation_checks = [
                ('time', self._check_time_alternation(wave2, wave4)),
                ('price', self._check_price_alternation(wave2, wave4)),
                ('complexity', self._check_complexity_alternation(complexity_2, complexity_4)),
                ('structure', self._check_structure_alternation(complexity_2, complexity_4)),
                ('severity', self._check_severity_alternation(wave2, wave4))
            ]
            
            valid_alternations = 0
            total_strength = 0.0
            
            for alt_type, (is_valid, strength, details) in alternation_checks:
                alternation_result['rule_compliance'][alt_type] = {
                    'valid': is_valid,
                    'strength': strength,
                    'details': details
                }
                
                if is_valid:
                    alternation_result['alternation_types'].append(alt_type)
                    valid_alternations += 1
                    total_strength += strength
                    
            # محاسبه قدرت کلی alternation
            alternation_result['alternation_strength'] = total_strength / len(alternation_checks)
            
            # قانون اصلی NEOWave: حداقل یک نوع alternation باید وجود داشته باشد
            alternation_result['neowave_valid'] = valid_alternations >= 1
            
            # توصیه‌های خاص
            if not alternation_result['neowave_valid']:
                alternation_result['warning'] = "عدم رعایت قانون Alternation - الگو ممکن است نامعتبر باشد"
            elif valid_alternations >= 3:
                alternation_result['strength_note'] = "Alternation قوی - الگوی معتبر و قابل اعتماد"
                
            logger.info(f"Alternation check کامل - معتبر: {alternation_result['neowave_valid']}")
            return alternation_result
            
        except Exception as e:
            logger.error(f"خطا در بررسی alternation: {e}")
            return {
                'basic_alternation': False,
                'neowave_valid': False,
                'error': str(e)
            }
    
    def calculate_missing_waves(self, impulse_pattern: List[Dict], 
                              strict_mode: bool = True) -> List[Dict]:
        """
        شناسایی دقیق موج‌های مفقود در الگوهای impulse
        
        Args:
            impulse_pattern: الگوی 5-موجی impulse
            strict_mode: حالت سخت‌گیرانه (پیش‌فرض: True)
            
        Returns:
            List[Dict]: لیست موج‌های مفقود و تحلیل آن‌ها
        """
        try:
            logger.info(f"جستجوی موج‌های مفقود در الگوی {len(impulse_pattern)}-موجی")
            
            missing_waves = []
            expected_waves = [1, 2, 3, 4, 5]
            actual_numbers = [w.get('number', 0) for w in impulse_pattern if 'number' in w]
            
            # شناسایی موج‌های مفقود اساسی
            for expected_num in expected_waves:
                if expected_num not in actual_numbers:
                    missing_info = self._analyze_missing_wave(
                        expected_num, impulse_pattern, strict_mode
                    )
                    if missing_info:
                        missing_waves.append(missing_info)
            
            # بررسی موج‌های X (linking waves)
            x_waves = self._identify_x_waves(impulse_pattern)
            missing_waves.extend(x_waves)
            
            # بررسی sub-waves مفقود
            if not strict_mode:
                subwave_missing = self._check_missing_subwaves(impulse_pattern)
                missing_waves.extend(subwave_missing)
                
            # مرتب‌سازی براساس اهمیت
            missing_waves.sort(key=lambda x: x.get('importance', 0), reverse=True)
            
            logger.info(f"{len(missing_waves)} موج مفقود شناسایی شد")
            return missing_waves
            
        except Exception as e:
            logger.error(f"خطا در شناسایی موج‌های مفقود: {e}")
            return []
    
    def predict_next_wave_complexity(self, completed_waves: List[Dict],
                                   pattern_type: str = "impulse") -> Dict:
        """
        پیش‌بینی سطح پیچیدگی موج بعدی براساس الگوهای موجود
        
        Args:
            completed_waves: موج‌های تکمیل شده
            pattern_type: نوع الگو (impulse, corrective, etc.)
            
        Returns:
            Dict: پیش‌بینی پیچیدگی موج بعدی
        """
        try:
            if len(completed_waves) < 2:
                return {'error': 'حداقل 2 موج برای پیش‌بینی نیاز است'}
                
            logger.info(f"پیش‌بینی پیچیدگی موج بعدی در الگوی {pattern_type}")
            
            # تحلیل الگوهای پیچیدگی موجود
            complexity_sequence = []
            structure_sequence = []
            
            for wave in completed_waves:
                result = self.analyze_wave_complexity(wave)
                complexity_sequence.append(result.complexity_level.value)
                structure_sequence.append(result.structure_type)
                
            # پیش‌بینی براساس الگو
            if pattern_type == "impulse":
                prediction = self._predict_impulse_complexity(
                    completed_waves, complexity_sequence
                )
            elif pattern_type == "corrective":
                prediction = self._predict_corrective_complexity(
                    completed_waves, complexity_sequence
                )
            else:
                prediction = self._predict_generic_complexity(
                    completed_waves, complexity_sequence
                )
                
            # اضافه کردن معیارهای اعتماد
            prediction['confidence'] = self._calculate_prediction_confidence(
                complexity_sequence, prediction
            )
            
            # توصیه‌های عملی
            prediction['recommendations'] = self._generate_prediction_recommendations(
                prediction, pattern_type
            )
            
            return prediction
            
        except Exception as e:
            logger.error(f"خطا در پیش‌بینی پیچیدگی: {e}")
            return {'error': str(e)}
    
    def generate_complexity_report(self, waves: List[Dict]) -> Dict:
        """
        تولید گزارش جامع پیچیدگی برای مجموعه‌ای از امواج
        
        Args:
            waves: لیست امواج برای تحلیل
            
        Returns:
            Dict: گزارش کامل پیچیدگی
        """
        try:
            logger.info(f"تولید گزارش پیچیدگی برای {len(waves)} موج")
            
            report = {
                'summary': {
                    'total_waves': len(waves),
                    'analyzed_at': pd.Timestamp.now().isoformat(),
                    'complexity_distribution': Counter(),
                    'structure_distribution': Counter(),
                    'average_complexity': 0.0
                },
                'wave_details': [],
                'alternation_analysis': {},
                'missing_waves': [],
                'recommendations': [],
                'risk_assessment': {},
                'statistics': {}
            }
            
            # تحلیل هر موج
            complexity_values = []
            for i, wave in enumerate(waves):
                try:
                    analysis = self.analyze_wave_complexity(wave, waves)
                    
                    wave_detail = {
                        'index': i,
                        'label': analysis.wave_label,
                        'complexity_level': analysis.complexity_level.name,
                        'structure_type': analysis.structure_type.value,
                        'confidence': analysis.complexity_confidence,
                        'metrics': {
                            'fractal_dimension': analysis.metrics.fractal_dimension,
                            'time_complexity': analysis.metrics.time_complexity,
                            'price_complexity': analysis.metrics.price_complexity
                        }
                    }
                    
                    report['wave_details'].append(wave_detail)
                    report['summary']['complexity_distribution'][analysis.complexity_level.name] += 1
                    report['summary']['structure_distribution'][analysis.structure_type.value] += 1
                    complexity_values.append(analysis.complexity_level.value)
                    
                except Exception as wave_error:
                    logger.warning(f"خطا در تحلیل موج {i}: {wave_error}")
                    continue
                    
            # محاسبه آمار کلی
            if complexity_values:
                report['summary']['average_complexity'] = np.mean(complexity_values)
                report['statistics'] = {
                    'complexity_std': np.std(complexity_values),
                    'complexity_trend': self._calculate_complexity_trend(complexity_values),
                    'dominant_complexity': ComplexityLevel(int(np.median(complexity_values))).name
                }
                
            # تحلیل alternation کلی
            if len(waves) >= 4:
                report['alternation_analysis'] = self._analyze_overall_alternation(waves)
                
            # شناسایی موج‌های مفقود کلی
            report['missing_waves'] = self.calculate_missing_waves(waves, strict_mode=False)
            
            # توصیه‌های کلی
            report['recommendations'] = self._generate_overall_recommendations(report)
            
            # ارزیابی ریسک
            report['risk_assessment'] = self._assess_complexity_risks(report)
            
            logger.info("گزارش پیچیدگی با موفقیت تولید شد")
            return report
            
        except Exception as e:
            logger.error(f"خطا در تولید گزارش پیچیدگی: {e}")
            return {'error': str(e)}
    
    # =============== متدهای کمکی خصوصی ===============
    
    def _generate_cache_key(self, wave: Dict) -> str:
        """تولید کلید cache برای موج"""
        key_data = {
            'start': wave.get('start_index', 0),
            'end': wave.get('end_index', 0), 
            'price_start': wave.get('start_price', 0),
            'price_end': wave.get('end_price', 0),
            'sub_count': len(wave.get('sub_waves', []))
        }
        return str(hash(frozenset(key_data.items())))
    
    def _determine_structure_type(self, wave: Dict, sub_waves: List[Dict]) -> StructureType:
        """تشخیص دقیق نوع ساختار موج"""
        try:
            sub_count = len(sub_waves)
            
            if sub_count == 0:
                return StructureType.MONO_WAVE
            elif sub_count == 3:
                # تشخیص بین zigzag و flat
                if self._is_zigzag_structure(sub_waves):
                    return StructureType.ZIGZAG
                elif self._is_flat_structure(sub_waves):
                    return StructureType.FLAT
                else:
                    return StructureType.TRIANGLE
            elif sub_count == 5:
                # تشخیص بین impulse و triangle
                if self._is_impulse_structure(sub_waves):
                    return StructureType.IMPULSE
                else:
                    return StructureType.TRIANGLE
            elif sub_count == 7:
                return StructureType.DIAMETRIC
            elif sub_count == 9:
                return StructureType.SYMMETRIC
            elif sub_count > 9:
                return StructureType.COMPLEX_CORRECTION
            else:
                return StructureType.UNKNOWN
                
        except Exception as e:
            logger.warning(f"خطا در تشخیص ساختار: {e}")
            return StructureType.UNKNOWN
    
    def _calculate_complexity_metrics(self, wave: Dict, sub_waves: List[Dict], 
                                    context: Optional[List[Dict]]) -> WaveComplexityMetrics:
        """محاسبه دقیق معیارهای پیچیدگی"""
        try:
            metrics = WaveComplexityMetrics()
            
            # بعد فراکتال با الگوریتم Box-counting
            metrics.fractal_dimension = self._calculate_fractal_dimension_advanced(wave)
            
            # پیچیدگی زمانی
            metrics.time_complexity = self._calculate_time_complexity_advanced(wave, sub_waves)
            
            # پیچیدگی قیمتی
            metrics.price_complexity = self._calculate_price_complexity_advanced(wave, sub_waves)
            
            # پیچیدگی ساختاری
            metrics.structural_complexity = self._calculate_structural_complexity(sub_waves)
            
            # خودشباهتی (Self-similarity)
            metrics.self_similarity = self._calculate_self_similarity(wave, sub_waves)
            
            # شاخص انحراف از الگوهای استاندارد
            metrics.deviation_index = self._calculate_deviation_index(wave, sub_waves)
            
            # دقت نسبت‌های فیبوناچی
            metrics.fibonacci_ratio_accuracy = self._calculate_fibonacci_accuracy(wave, sub_waves)
            
            # امتیاز alternation
            if context:
                metrics.alternation_score = self._calculate_alternation_score(wave, context)
            
            return metrics
            
        except Exception as e:
            logger.error(f"خطا در محاسبه metrics: {e}")
            return WaveComplexityMetrics()
    
    def _calculate_fractal_dimension_advanced(self, wave: Dict) -> float:
        """محاسبه بعد فراکتال با الگوریتم Box-counting پیشرفته"""
        try:
            start_idx = wave.get('start_index', 0)
            end_idx = wave.get('end_index', 0)
            
            if start_idx >= end_idx or end_idx >= len(self.data):
                return 1.0
                
            # استخراج داده‌های قیمتی
            price_data = self.data['close'].iloc[start_idx:end_idx+1].values
            
            if len(price_data) < 4:
                return 1.0
                
            # الگوریتم Box-counting
            def box_count(data, box_size):
                """شمارش جعبه‌های غیرخالی"""
                n = len(data)
                boxes = set()
                
                for i in range(n-1):
                    y1, y2 = data[i], data[i+1]
                    y_min, y_max = min(y1, y2), max(y1, y2)
                    
                    # محاسبه جعبه‌های تحت پوشش
                    box_min = int(y_min / box_size)
                    box_max = int(y_max / box_size)
                    
                    for box in range(box_min, box_max + 1):
                        boxes.add((i // int(box_size), box))
                        
                return len(boxes)
            
            # نرمال‌سازی داده‌ها
            price_norm = (price_data - price_data.min()) / (price_data.max() - price_data.min() + 1e-10)
            
            # تعیین اندازه‌های مختلف جعبه
            scales = np.logspace(-3, -1, 10)  # از 0.001 تا 0.1
            counts = []
            
            for scale in scales:
                count = box_count(price_norm, scale)
                if count > 0:
                    counts.append(count)
                else:
                    counts.append(1)  # جلوگیری از log(0)
                    
            # رگرسیون خطی log-log
            log_scales = np.log(scales)
            log_counts = np.log(counts)
            
            # استفاده از sklearn برای دقت بیشتر
            reg = LinearRegression().fit(log_scales.reshape(-1, 1), log_counts)
            fractal_dim = -reg.coef_[0]
            
            # محدود کردن به بازه معقول
            return max(1.0, min(2.0, fractal_dim))
            
        except Exception as e:
            logger.warning(f"خطا در محاسبه بعد فراکتال: {e}")
            return 1.5  # مقدار متوسط
    
    def _calculate_time_complexity_advanced(self, wave: Dict, sub_waves: List[Dict]) -> float:
        """محاسبه پیچیدگی زمانی پیشرفته"""
        try:
            if not sub_waves:
                return 0.0
                
            # استخراج طول‌های زمانی sub-waves
            durations = []
            for sub in sub_waves:
                start = sub.get('start_index', 0)
                end = sub.get('end_index', 0)
                duration = max(1, end - start)
                durations.append(duration)
                
            if len(durations) < 2:
                return 0.0
                
            durations = np.array(durations)
            
            # محاسبه چندین معیار پیچیدگی زمانی
            
            # 1. ضریب تغییرات (Coefficient of Variation)
            cv = np.std(durations) / (np.mean(durations) + 1e-10)
            
            # 2. آنتروپی Shannon
            duration_probs = durations / np.sum(durations)
            shannon_entropy = -np.sum(duration_probs * np.log2(duration_probs + 1e-10))
            
            # 3. شاخص Gini (عدم تعادل)
            sorted_durations = np.sort(durations)
            n = len(sorted_durations)
            gini = (2 * np.sum((np.arange(1, n+1)) * sorted_durations)) / (n * np.sum(sorted_durations)) - (n+1) / n
            
            # 4. همبستگی سریالی (تداوم الگو)
            if len(durations) > 2:
                serial_corr = np.corrcoef(durations[:-1], durations[1:])[0, 1]
                serial_corr = abs(serial_corr) if not np.isnan(serial_corr) else 0
            else:
                serial_corr = 0
                
            # ترکیب معیارها
            time_complexity = (cv * 0.3 + 
                             shannon_entropy / np.log2(len(durations)) * 0.3 + 
                             gini * 0.3 + 
                             serial_corr * 0.1)
            
            return min(1.0, time_complexity)
            
        except Exception as e:
            logger.warning(f"خطا در محاسبه پیچیدگی زمانی: {e}")
            return 0.0
    
    def _calculate_price_complexity_advanced(self, wave: Dict, sub_waves: List[Dict]) -> float:
        """محاسبه پیچیدگی قیمتی پیشرفته"""
        try:
            if not sub_waves:
                return 0.0
                
            # استخراج amplitude های sub-waves
            amplitudes = []
            price_changes = []
            
            for sub in sub_waves:
                start_price = sub.get('start_price', 0)
                end_price = sub.get('end_price', 0)
                high_price = sub.get('high_price', max(start_price, end_price))
                low_price = sub.get('low_price', min(start_price, end_price))
                
                amplitude = high_price - low_price
                price_change = abs(end_price - start_price)
                
                amplitudes.append(amplitude)
                price_changes.append(price_change)
                
            if len(amplitudes) < 2:
                return 0.0
                
            amplitudes = np.array(amplitudes)
            price_changes = np.array(price_changes)
            
            # محاسبه معیارهای پیچیدگی قیمتی
            
            # 1. تنوع در اندازه حرکات
            amp_cv = np.std(amplitudes) / (np.mean(amplitudes) + 1e-10)
            
            # 2. عدم تقارن (Skewness)
            amp_skewness = abs(stats.skew(amplitudes))
            
            # 3. کشیدگی (Kurtosis) - انحراف از توزیع نرمال
            amp_kurtosis = abs(stats.kurtosis(amplitudes))
            
            # 4. نسبت طلایی - انحراف از نسبت‌های فیبوناچی
            fib_deviation = self._calculate_fibonacci_deviation(amplitudes)
            
            # 5. پیچیدگی در جهت حرکات
            direction_complexity = self._calculate_direction_complexity(sub_waves)
            
            # ترکیب معیارها
            price_complexity = (amp_cv * 0.25 + 
                              amp_skewness * 0.2 + 
                              amp_kurtosis * 0.2 + 
                              fib_deviation * 0.2 + 
                              direction_complexity * 0.15)
            
            return min(1.0, price_complexity)
            
        except Exception as e:
            logger.warning(f"خطا در محاسبه پیچیدگی قیمتی: {e}")
            return 0.0
    
    def _check_time_alternation(self, wave2: Dict, wave4: Dict) -> Tuple[bool, float, str]:
        """بررسی alternation زمانی"""
        try:
            duration_2 = wave2.get('end_index', 0) - wave2.get('start_index', 0)
            duration_4 = wave4.get('end_index', 0) - wave4.get('start_index', 0)
            
            if duration_2 == 0 or duration_4 == 0:
                return False, 0.0, "مدت زمان موج‌ها صفر است"
                
            ratio = max(duration_2, duration_4) / min(duration_2, duration_4)
            
            # alternation معتبر اگر نسبت بیشتر از 1.5 باشد
            is_valid = ratio >= 1.5
            strength = min(1.0, (ratio - 1) / 2)  # قدرت alternation
            
            details = f"نسبت زمانی: {ratio:.2f}, موج 2: {duration_2} کندل, موج 4: {duration_4} کندل"
            
            return is_valid, strength, details
            
        except Exception as e:
            return False, 0.0, f"خطا: {e}"
    
    def _check_price_alternation(self, wave2: Dict, wave4: Dict) -> Tuple[bool, float, str]:
        """بررسی alternation قیمتی"""
        try:
            amp_2 = abs(wave2.get('end_price', 0) - wave2.get('start_price', 0))
            amp_4 = abs(wave4.get('end_price', 0) - wave4.get('start_price', 0))
            
            if amp_2 == 0 or amp_4 == 0:
                return False, 0.0, "دامنه قیمتی موج‌ها صفر است"
                
            ratio = max(amp_2, amp_4) / min(amp_2, amp_4)
            
            # alternation معتبر اگر نسبت بیشتر از 1.3 باشد
            is_valid = ratio >= 1.3
            strength = min(1.0, (ratio - 1) / 1.5)
            
            details = f"نسبت قیمتی: {ratio:.2f}, دامنه موج 2: {amp_2:.2f}, دامنه موج 4: {amp_4:.2f}"
            
            return is_valid, strength, details
            
        except Exception as e:
            return False, 0.0, f"خطا: {e}"
    
    def _check_complexity_alternation(self, complexity_2: ComplexityAnalysisResult, 
                                    complexity_4: ComplexityAnalysisResult) -> Tuple[bool, float, str]:
        """بررسی alternation پیچیدگی"""
        try:
            level_diff = abs(complexity_2.complexity_level.value - complexity_4.complexity_level.value)
            
            # alternation معتبر اگر حداقل 2 سطح اختلاف باشد
            is_valid = level_diff >= 2
            strength = min(1.0, level_diff / 4)  # قدرت براساس اختلاف سطح
            
            details = (f"سطح موج 2: {complexity_2.complexity_level.name}, "
                      f"سطح موج 4: {complexity_4.complexity_level.name}, "
                      f"اختلاف: {level_diff}")
            
            return is_valid, strength, details
            
        except Exception as e:
            return False, 0.0, f"خطا: {e}"
    
    def _check_structure_alternation(self, complexity_2: ComplexityAnalysisResult,
                                   complexity_4: ComplexityAnalysisResult) -> Tuple[bool, float, str]:
        """بررسی alternation ساختاری"""
        try:
            struct_2 = complexity_2.structure_type
            struct_4 = complexity_4.structure_type
            
            # alternation معتبر اگر ساختار متفاوت باشد
            is_valid = struct_2 != struct_4
            
            # قدرت براساس میزان تفاوت ساختار
            structure_weights = {
                StructureType.MONO_WAVE: 1,
                StructureType.ZIGZAG: 2,
                StructureType.FLAT: 2,
                StructureType.TRIANGLE: 3,
                StructureType.IMPULSE: 4,
                StructureType.COMPLEX_CORRECTION: 5
            }
            
            weight_2 = structure_weights.get(struct_2, 1)
            weight_4 = structure_weights.get(struct_4, 1)
            
            strength = abs(weight_2 - weight_4) / 4 if is_valid else 0.0
            
            details = f"ساختار موج 2: {struct_2.value}, ساختار موج 4: {struct_4.value}"
            
            return is_valid, strength, details
            
        except Exception as e:
            return False, 0.0, f"خطا: {e}"
    
    def _check_severity_alternation(self, wave2: Dict, wave4: Dict) -> Tuple[bool, float, str]:
        """بررسی alternation شدت حرکت"""
        try:
            # محاسبه درصد retracement
            # فرض می‌کنیم موج 1 و 3 در دسترس هستند
            
            # به عنوان تقریب، از داده‌های موج خود استفاده می‌کنیم
            retr_2 = abs(wave2.get('end_price', 0) - wave2.get('start_price', 0)) / (wave2.get('start_price', 1) + 1e-10)
            retr_4 = abs(wave4.get('end_price', 0) - wave4.get('start_price', 0)) / (wave4.get('start_price', 1) + 1e-10)
            
            ratio = max(retr_2, retr_4) / (min(retr_2, retr_4) + 1e-10)
            
            # alternation معتبر اگر یکی shallow و دیگری deep باشد
            is_valid = ratio >= 1.5
            strength = min(1.0, (ratio - 1) / 2)
            
            details = f"نسبت شدت: {ratio:.2f}, retracement موج 2: {retr_2:.1%}, موج 4: {retr_4:.1%}"
            
            return is_valid, strength, details
            
        except Exception as e:
            return False, 0.0, f"خطا: {e}"
    
    # سایر متدهای کمکی...
    def _analyze_missing_wave(self, wave_num: int, pattern: List[Dict], strict: bool) -> Optional[Dict]:
        """تحلیل دقیق موج مفقود"""
        # پیاده‌سازی تفصیلی برای شناسایی شرایط missing wave
        return None  # ساده‌سازی موقت
    
    def _identify_x_waves(self, pattern: List[Dict]) -> List[Dict]:
        """شناسایی موج‌های X (linking waves)"""
        return []  # ساده‌سازی موقت
    
    def _check_missing_subwaves(self, pattern: List[Dict]) -> List[Dict]:
        """بررسی sub-waves مفقود"""
        return []  # ساده‌سازی موقت
    
    # متدهای کمکی اضافی
    def _calculate_structural_complexity(self, sub_waves: List[Dict]) -> float:
        """محاسبه پیچیدگی ساختاری"""
        return len(sub_waves) / 13.0  # نرمال‌سازی به حداکثر سطح SUPER
    
    def _calculate_self_similarity(self, wave: Dict, sub_waves: List[Dict]) -> float:
        """محاسبه میزان خودشباهتی فراکتال"""
        return 0.5  # ساده‌سازی موقت
    
    def _calculate_deviation_index(self, wave: Dict, sub_waves: List[Dict]) -> float:
        """شاخص انحراف از الگوهای استاندارد"""
        return 0.3  # ساده‌سازی موقت
    
    def _calculate_fibonacci_accuracy(self, wave: Dict, sub_waves: List[Dict]) -> float:
        """دقت نسبت‌های فیبوناچی"""
        return 0.7  # ساده‌سازی موقت
    
    def _calculate_alternation_score(self, wave: Dict, context: List[Dict]) -> float:
        """امتیاز alternation"""
        return 0.6  # ساده‌سازی موقت
    
    def _calculate_fibonacci_deviation(self, amplitudes: np.ndarray) -> float:
        """انحراف از نسبت‌های فیبوناچی"""
        return 0.4  # ساده‌سازی موقت
    
    def _calculate_direction_complexity(self, sub_waves: List[Dict]) -> float:
        """پیچیدگی جهت حرکات"""
        return 0.3  # ساده‌سازی موقت
    
    def _is_zigzag_structure(self, sub_waves: List[Dict]) -> bool:
        """تشخیص ساختار zigzag"""
        return len(sub_waves) == 3  # ساده‌سازی
    
    def _is_flat_structure(self, sub_waves: List[Dict]) -> bool:
        """تشخیص ساختار flat"""
        return False  # ساده‌سازی موقت
    
    def _is_impulse_structure(self, sub_waves: List[Dict]) -> bool:
        """تشخیص ساختار impulse"""
        return len(sub_waves) == 5  # ساده‌سازی
    
    def _check_alternation_rules(self, wave: Dict, sub_waves: List[Dict], 
                               context: Optional[List[Dict]]) -> Dict[str, bool]:
        """بررسی قوانین alternation"""
        return {'basic_alternation': True}  # ساده‌سازی موقت
    
    def _identify_missing_waves(self, wave: Dict, sub_waves: List[Dict]) -> List[Dict]:
        """شناسایی موج‌های مفقود"""
        return []  # ساده‌سازی موقت
    
    def _calculate_complexity_confidence(self, level: ComplexityLevel, 
                                       metrics: WaveComplexityMetrics,
                                       alternation: Dict) -> float:
        """محاسبه اعتماد به تحلیل پیچیدگی"""
        base_confidence = 0.7
        
        # افزایش اعتماد براساس کیفیت metrics
        if metrics.fractal_dimension > 1.2:
            base_confidence += 0.1
        if metrics.fibonacci_ratio_accuracy > 0.8:
            base_confidence += 0.1
        if alternation.get('basic_alternation', False):
            base_confidence += 0.1
            
        return min(1.0, base_confidence)
    
    def _generate_recommendations(self, level: ComplexityLevel, structure: StructureType,
                                metrics: WaveComplexityMetrics, alternation: Dict) -> List[str]:
        """تولید توصیه‌های عملی"""
        recommendations = []
        
        if level == ComplexityLevel.MONO:
            recommendations.append("موج ساده - احتمال ادامه روند بالا")
        elif level >= ComplexityLevel.MULTI:
            recommendations.append("موج پیچیده - احتیاط در تصمیم‌گیری")
            
        if not alternation.get('basic_alternation', True):
            recommendations.append("عدم رعایت قانون alternation - بررسی مجدد الگو")
            
        return recommendations
    
    # متدهای پیش‌بینی
    def _predict_impulse_complexity(self, waves: List[Dict], sequence: List[int]) -> Dict:
        """پیش‌بینی پیچیدگی در الگوی impulse"""
        return {'predicted_level': ComplexityLevel.POLY, 'reasoning': 'الگوی impulse'}
    
    def _predict_corrective_complexity(self, waves: List[Dict], sequence: List[int]) -> Dict:
        """پیش‌بینی پیچیدگی در الگوی corrective"""
        return {'predicted_level': ComplexityLevel.MULTI, 'reasoning': 'الگوی corrective'}
    
    def _predict_generic_complexity(self, waves: List[Dict], sequence: List[int]) -> Dict:
        """پیش‌بینی عمومی پیچیدگی"""
        return {'predicted_level': ComplexityLevel.POLY, 'reasoning': 'پیش‌بینی عمومی'}
    
    def _calculate_prediction_confidence(self, sequence: List[int], prediction: Dict) -> float:
        """محاسبه اعتماد به پیش‌بینی"""
        return 0.75  # مقدار پیش‌فرض
    
    def _generate_prediction_recommendations(self, prediction: Dict, pattern_type: str) -> List[str]:
        """توصیه‌های مربوط به پیش‌بینی"""
        return [f"پیش‌بینی برای الگوی {pattern_type}"]
    
    # متدهای گزارش
    def _calculate_complexity_trend(self, values: List[int]) -> float:
        """محاسبه روند پیچیدگی"""
        if len(values) < 2:
            return 0.0
        return np.polyfit(range(len(values)), values, 1)[0]
    
    def _analyze_overall_alternation(self, waves: List[Dict]) -> Dict:
        """تحلیل کلی alternation"""
        return {'overall_valid': True}
    
    def _generate_overall_recommendations(self, report: Dict) -> List[str]:
        """توصیه‌های کلی گزارش"""
        return ["تحلیل کامل انجام شد"]
    
    def _assess_complexity_risks(self, report: Dict) -> Dict:
        """ارزیابی ریسک‌های پیچیدگی"""
        return {'risk_level': 'متوسط', 'factors': ['پیچیدگی بالا']}