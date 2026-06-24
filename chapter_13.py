# chapters/chapter_13.py

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    فصل 13: صفات و مشخصات موج‌ها                               ║
║                    (Wave Characteristics)                                     ║
║                                                                               ║
║  منبع: کتاب "استادی در امواج الیوت" - گلن نیلی (نئوویو)                       ║
║  صفحات: 324 تا 329                                                           ║
║                                                                               ║
║  این فایل مطابق با interface تعریف شده در main.py پیاده‌سازی شده است.        ║
╚═══════════════════════════════════════════════════════════════════════════════╝

پوشش کامل صفحات:

┌─────────────────────────────────────────────────────────────────────────────┐
│ صفحه 324: محدودیت‌های زمانی در اصلاحات (Time Limits in Corrections)        │
│   - قوانین زمانی بخش دوم نسبت به بخش اول                                      │
│   - جدول مقایسه الگوها از نظر شباهت قیمتی، زمانی و پیچیدگی                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ صفحه 325: مشخصات موج 1                                                       │
│   - 10 مشخصه کلیدی موج 1                                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ صفحه 326: مشخصات موج 2                                                       │
│   - 7 مشخصه کلیدی موج 2                                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ صفحه 327: مشخصات موج 3                                                       │
│   - 14 مشخصه کلیدی موج 3                                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ صفحه 328: مشخصات موج 4                                                       │
│   - 14 مشخصه کلیدی موج 4                                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ صفحه 329: مشخصات موج 5                                                       │
│   - 12 مشخصه کلیدی موج 5                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════════════════════
# بخش 1: تعاریف پایه و انواع شمارشی
# ═══════════════════════════════════════════════════════════════════════════════


class WaveNumber(Enum):
    """شماره موج در یک سیکل 5 موجی"""
    WAVE_1 = 1
    WAVE_2 = 2
    WAVE_3 = 3
    WAVE_4 = 4
    WAVE_5 = 5


class SimilarityType(Enum):
    """نوع شباهت بین امواج (صفحه 323)"""
    PRICE = "قیمتی"
    TIME = "زمانی"
    COMPLEXITY = "پیچیدگی"


class PatternSimilarity(Enum):
    """میزان شباهت در الگوهای مختلف (صفحه 323)"""
    ZIGZAG = "زیگزاگ"
    FLAT = "مسطح"
    TRIANGLE = "مثلث"
    DIAMETRIC = "دیامتریک"
    SYMMETRICAL = "سیمتریک"


class TimeLimitStatus(Enum):
    """وضعیت محدودیت زمانی در اصلاحات (صفحه 324)"""
    UNACCEPTABLE_SHORT = "غیرقابل_قبول_کوتاه"
    MINIMUM_EQUAL = "حداقل_برابر"
    COMMON = "متداول"
    UNACCEPTABLE_LONG = "غیرقابل_قبول_بلند"


# ═══════════════════════════════════════════════════════════════════════════════
# بخش 2: مشخصات موج 1 (صفحه 325) - 10 مشخصه
# ═══════════════════════════════════════════════════════════════════════════════


class Wave1Characteristics:
    """
    مشخصات موج 1 بر اساس کتاب گلن نیلی - صفحه 325
    
    ویژگی‌های کلیدی موج 1 (10 مشخصه):
    1. دارای رای ضعیفی است و معمول بر اساس یک فرآیند بنیادی بدبینانه شکل می‌گیرد
    2. نسبت به آخرین نوسان اصلاحی از نظر زمانی کوچکتر و از نظر قیمتی بلندتر است
    3. افزایش حجم نامحسوس می‌باشد
    4. عقیده اکثریت معامله‌گران منفی است
    5. معمول کوتاه‌ترین موج می‌باشد
    6. ساختار فاز اصلاح بیش از آن کامل شده است
    7. ناامیدی در بازار وجود دارد
    8. واگرایی مثبت در اندیکاتورها دیده می‌شود
    9. از نوع الگوی شتابدار رونددار می‌باشد
    10. در صورتی که الگو از یک درجه بالاتر از سطح پیچیدگی ۱ برخوردار باشد در اینصورت بخشیزه‌ترین موج نخواهد بود
    """
    
    @staticmethod
    def get_characteristics() -> Dict[str, str]:
        """بازگرداندن لیست کامل 10 مشخصات موج 1"""
        return {
            "weak_sentiment": "دارای رای ضعیفی است و معمول بر اساس یک فرآیند بنیادی بدبینانه شکل می‌گیرد",
            "time_price_relation": "نسبت به آخرین نوسان اصلاحی از نظر زمانی کوچکتر و از نظر قیمتی بلندتر است",
            "volume": "افزایش حجم نامحسوس می‌باشد",
            "market_sentiment": "عقیده اکثریت معامله‌گران منفی است",
            "shortest_wave": "معمول کوتاه‌ترین موج می‌باشد",
            "correction_complete": "ساختار فاز اصلاح بیش از آن کامل شده است",
            "despair": "ناامیدی در بازار وجود دارد",
            "positive_divergence": "واگرایی مثبت در اندیکاتورها دیده می‌شود",
            "structure": "از نوع الگوی شتابدار رونددار می‌باشد",
            "complexity_condition": "در صورتی که الگو از یک درجه بالاتر از سطح پیچیدگی ۱ برخوردار باشد در اینصورت بخشیزه‌ترین موج نخواهد بود"
        }
    
    @staticmethod
    def check_characteristics(wave_data: Dict[str, Any]) -> Dict[str, bool]:
        """
        بررسی وجود مشخصات موج 1 در داده‌های ورودی
        
        پارامترها:
        - wave_data: دیکشنری شامل اطلاعات موج (حجم، زمان، قیمت، اندیکاتورها، complexity_level)
        
        خروجی:
        - دیکشنری از مشخصات و وضعیت وجود/عدم وجود آنها
        """
        results = {}
        
        # بررسی حجم نامحسوس
        if "volume" in wave_data:
            avg_volume = wave_data.get("avg_volume_prior", 1)
            results["volume_imperceptible"] = wave_data["volume"] <= avg_volume * 1.1
        
        # بررسی کوتاه بودن موج
        if "wave_lengths" in wave_data:
            lengths = wave_data["wave_lengths"]
            results["shortest_wave"] = wave_data.get("wave_length", 0) <= min(lengths) if lengths else True
        
        # بررسی واگرایی مثبت
        if "rsi" in wave_data and "price" in wave_data:
            results["positive_divergence"] = wave_data.get("positive_divergence", False)
        
        # بررسی شرط پیچیدگی (مشخصه دهم)
        complexity_level = wave_data.get("complexity_level", 0)
        if complexity_level > 1:
            results["not_shortest_by_complexity"] = True
        else:
            results["not_shortest_by_complexity"] = None  # شرط اعمال نمی‌شود
        
        return results
    
    @staticmethod
    def is_valid_wave1(wave_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        تشخیص معتبر بودن موج 1 بر اساس مشخصات کلیدی
        
        خروجی:
        - isValid: bool
        - violations: لیست مشخصات نقض شده
        """
        violations = []
        
        # موج 1 باید از نوع شتابدار باشد
        if wave_data.get("wave_type") not in ["impulse", "motive"]:
            violations.append("موج 1 باید از نوع الگوی شتابدار رونددار باشد")
        
        # موج 1 معمولاً کوتاه‌ترین است (اما الزامی نیست)
        # شرط پیچیدگی: اگر سطح پیچیدگی > 1 باشد، موج 1 کوتاه‌ترین نخواهد بود
        if wave_data.get("complexity_level", 0) > 1:
            wave_lengths = wave_data.get("wave_lengths", [])
            wave1_len = wave_data.get("wave_length", 0)
            if wave_lengths and wave1_len == min(wave_lengths):
                violations.append("با توجه به سطح پیچیدگی بالاتر از 1، موج 1 نباید کوتاه‌ترین موج باشد")
        
        return len(violations) == 0, violations


# ═══════════════════════════════════════════════════════════════════════════════
# بخش 3: مشخصات موج 2 (صفحه 326) - 7 مشخصه
# ═══════════════════════════════════════════════════════════════════════════════


class Wave2Characteristics:
    """
    مشخصات موج 2 بر اساس کتاب گلن نیلی - صفحه 326
    
    ویژگی‌های کلیدی موج 2 (7 مشخصه):
    1. تحلیلگران معتقد هستند که روند صعودی شکل نگرفته است
    2. در انتهای آن با کاهش حجم و نوسانات قیمتی همراه است
    3. به شکل هر یک از الگوهای اصلاحی می‌تواند باشد (غیر از الگوی مثلث)
    4. اگر کمتر از 50 درصد موج 1 را اصلاح کند، احتمالاً موج 3 انبساط پیدا خواهد کرد
    5. زمان موج 2 باید بیش از زمان صرف شده توسط موج 1 باشد
    6. زمانی که موج 2 به فرم زیگزاگ کشیده یا مسطح کشیده یا آرایش غیر استاندارد باشد، موج 3 معمولاً بسط نخواهد شد
    """
    
    @staticmethod
    def get_characteristics() -> Dict[str, str]:
        """بازگرداندن لیست کامل 7 مشخصات موج 2"""
        return {
            "trend_doubt": "تحلیلگران معتقد هستند که روند صعودی شکل نگرفته است",
            "end_characteristics": "در انتهای آن با کاهش حجم و نوسانات قیمتی همراه است",
            "pattern_type": "به شکل هر یک از الگوهای اصلاحی می‌تواند باشد (غیر از الگوی مثلث)",
            "shallow_retrace": "اگر کمتر از 50 درصد موج 1 را اصلاح کند، احتمالاً موج 3 انبساط پیدا خواهد کرد",
            "time_requirement": "زمان موج 2 باید بیش از زمان صرف شده توسط موج 1 باشد",
            "wave3_extension_prevention": "زمانی که موج 2 به فرم زیگزاگ کشیده یا مسطح کشیده یا آرایش غیر استاندارد باشد، موج 3 معمولاً بسط نخواهد شد"
        }
    
    @staticmethod
    def check_retracement(ratio: float) -> Dict[str, Any]:
        """
        بررسی درصد اصلاح موج 2 نسبت به موج 1
        
        صفحه 326: "اگر کمتر از 50 درصد موج 1 را اصلاح کند، احتمالاً موج 3 انبساط پیدا خواهد کرد"
        
        پارامترها:
        - ratio: درصد اصلاح (مقدار بین 0 تا 1)
        
        خروجی:
        - status: "shallow", "normal", "deep"
        - wave3_likely_extension: boolean
        """
        if ratio < 0.5:
            return {
                "status": "shallow",
                "wave3_likely_extension": True,
                "description": "اصلاح سطحی - موج 3 احتمالاً انبساط خواهد یافت"
            }
        elif ratio <= 0.618:
            return {
                "status": "normal",
                "wave3_likely_extension": False,
                "description": "اصلاح معمولی"
            }
        else:
            return {
                "status": "deep",
                "wave3_likely_extension": False,
                "description": "اصلاح عمیق"
            }
    
    @staticmethod
    def check_time_ratio(wave1_time: int, wave2_time: int) -> Dict[str, Any]:
        """
        بررسی نسبت زمانی موج 2 نسبت به موج 1
        
        صفحه 326: "زمان موج 2 باید بیش از زمان صرف شده توسط موج 1 باشد"
        
        خروجی:
        - is_valid: آیا نسبت زمانی معتبر است
        - ratio: نسبت زمانی (wave2_time / wave1_time)
        """
        if wave1_time == 0:
            return {"is_valid": True, "ratio": 0, "description": "داده زمانی کافی نیست"}
        
        ratio = wave2_time / wave1_time
        
        if ratio >= 1.0:
            return {
                "is_valid": True,
                "ratio": round(ratio, 2),
                "description": f"زمان موج 2 ({wave2_time}) بیش از موج 1 ({wave1_time}) است"
            }
        else:
            return {
                "is_valid": False,
                "ratio": round(ratio, 2),
                "description": f"نقض قانون: زمان موج 2 ({wave2_time}) کمتر از موج 1 ({wave1_time}) است"
            }
    
    @staticmethod
    def check_wave2_pattern_for_wave3_extension(wave2_pattern: str, wave2_subtype: str = "") -> Dict[str, Any]:
        """
        بررسی اینکه آیا الگوی موج 2 مانع بسط موج 3 می‌شود
        
        صفحه 326: "زمانی که موج 2 به فرم زیگزاگ کشیده یا مسطح کشیده یا آرایش غیر استاندارد باشد، موج 3 معمولاً بسط نخواهد شد"
        
        پارامترها:
        - wave2_pattern: نوع الگوی موج 2 ("zigzag", "flat", "irregular", "running", ...)
        - wave2_subtype: زیرنوع الگو ("elongated", "common", "running", ...)
        
        خروجی:
        - prevents_extension: bool - آیا موج 2 مانع بسط موج 3 می‌شود
        - description: توضیح
        """
        prevents_extension = False
        description = ""
        
        # زیگزاگ کشیده
        if wave2_pattern == "zigzag" and wave2_subtype == "elongated":
            prevents_extension = True
            description = "موج 2 به فرم زیگزاگ کشیده است - موج 3 معمولاً بسط نخواهد شد"
        
        # مسطح کشیده
        elif wave2_pattern == "flat" and wave2_subtype == "elongated":
            prevents_extension = True
            description = "موج 2 به فرم مسطح کشیده است - موج 3 معمولاً بسط نخواهد شد"
        
        # آرایش غیر استاندارد
        elif wave2_pattern in ["irregular", "running", "double_failure", "failure"]:
            prevents_extension = True
            description = f"موج 2 دارای آرایش غیر استاندارد ({wave2_pattern}) است - موج 3 معمولاً بسط نخواهد شد"
        
        else:
            description = "الگوی موج 2 استاندارد است - موج 3 احتمالاً بسط خواهد یافت"
        
        return {
            "prevents_extension": prevents_extension,
            "wave2_pattern": wave2_pattern,
            "wave2_subtype": wave2_subtype,
            "description": description
        }
    
    @staticmethod
    def is_valid_wave2(wave_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        تشخیص معتبر بودن موج 2 بر اساس مشخصات کلیدی
        
        خروجی:
        - isValid: bool
        - violations: لیست مشخصات نقض شده
        """
        violations = []
        
        # موج 2 باید اصلاحی باشد
        if wave_data.get("wave_type") not in ["corrective", "flat", "zigzag"]:
            violations.append("موج 2 باید به شکل یک الگوی اصلاحی باشد")
        
        # موج 2 نمی‌تواند مثلث کامل باشد (می‌تواند بخشی از مثلث باشد)
        if wave_data.get("pattern") == "triangle":
            violations.append("موج 2 نمی‌تواند به شکل مثلث کامل باشد (مثلث فقط بخشی از ساختار آن می‌تواند باشد)")
        
        # بررسی زمان
        time_check = Wave2Characteristics.check_time_ratio(
            wave_data.get("wave1_time", 0),
            wave_data.get("wave2_time", 0)
        )
        if not time_check["is_valid"]:
            violations.append(time_check["description"])
        
        return len(violations) == 0, violations


# ═══════════════════════════════════════════════════════════════════════════════
# بخش 4: مشخصات موج 3 (صفحه 327) - 14 مشخصه
# ═══════════════════════════════════════════════════════════════════════════════


class Wave3Characteristics:
    """
    مشخصات موج 3 بر اساس کتاب گلن نیلی - صفحه 327
    
    ویژگی‌های کلیدی موج 3 (14 مشخصه):
    1. شیب تند، یک مشخصه موج سه است
    2. حرکت سریع و تند معمول در این موج رخ می‌دهد
    3. فاکتورهای کلان اقتصادی تایید کننده روند می‌شوند
    4. فاکتورهای فاندامنتال نیز تایید کننده این روند هستند
    5. معمول طولانی‌ترین و قوی‌ترین موج است
    6. حجم بالا می‌رود
    7. بلندترین قله‌های اندیکاتوری در انتهای این موج دیده می‌شود
    8. صرفاً به شکل یک الگوی شتابدار می‌تواند باشد
    9. بین موج‌های 1 و 3 و 5 نمی‌تواند کوتاه‌ترین موج باشد
    10. از لحاظ زمانی بین 150 تا 500 درصد موج 1 می‌باشد
    11. از لحاظ قیمتی 1 تا 3 برابر موج 1 می‌باشد
    12. موج 3 نمی‌تواند بیش از 3 برابر رنج قیمتی و زمانی موج 1 باشد
    13. زمان موج 3 معمول حداقل بیش از نصف زمان صرف شده توسط موج 1 و 2 باشد
    """
    
    # نسبت‌های استاندارد نئوویو برای موج 3
    MIN_TIME_RATIO = 1.5      # 150%
    MAX_TIME_RATIO = 5.0      # 500%
    MIN_PRICE_RATIO = 1.0     # 100%
    MAX_PRICE_RATIO = 3.0     # 300%
    MAX_PRICE_TIME_MULTIPLIER = 3.0  # حداکثر 3 برابر موج 1
    
    @staticmethod
    def get_characteristics() -> Dict[str, str]:
        """بازگرداندن لیست کامل 14 مشخصات موج 3"""
        return {
            "steep_slope": "شیب تند، یک مشخصه موج سه است",
            "fast_movement": "حرکت سریع و تند معمول در این موج رخ می‌دهد",
            "economic_confirmation": "فاکتورهای کلان اقتصادی تایید کننده روند می‌شوند",
            "fundamental_confirmation": "فاکتورهای فاندامنتال نیز تایید کننده این روند هستند",
            "longest_strongest": "معمول طولانی‌ترین و قوی‌ترین موج است",
            "high_volume": "حجم بالا می‌رود",
            "indicator_peaks": "بلندترین قله‌های اندیکاتوری در انتهای این موج دیده می‌شود",
            "must_be_impulsive": "صرفاً به شکل یک الگوی شتابدار می‌تواند باشد",
            "not_shortest": "بین موج‌های 1 و 3 و 5 نمی‌تواند کوتاه‌ترین موج باشد",
            "time_range": "از لحاظ زمانی بین 150 تا 500 درصد موج 1 می‌باشد",
            "price_range": "از لحاظ قیمتی 1 تا 3 برابر موج 1 می‌باشد",
            "max_limit": "موج 3 نمی‌تواند بیش از 3 برابر رنج قیمتی و زمانی موج 1 باشد",
            "time_minimum": "زمان موج 3 معمول حداقل بیش از نصف زمان صرف شده توسط موج 1 و 2 باشد"
        }
    
    @staticmethod
    def check_time_ratio(wave1_time: int, wave3_time: int) -> Dict[str, Any]:
        """
        بررسی نسبت زمانی موج 3 نسبت به موج 1
        
        صفحه 327: "از لحاظ زمانی بین 150 تا 500 درصد موج 1 می‌باشد"
        
        خروجی:
        - status: "too_short", "normal", "too_long", "excessive"
        - is_valid: آیا در محدوده مجاز است
        """
        if wave1_time == 0:
            return {"is_valid": True, "ratio": 0, "status": "unknown"}
        
        ratio = wave3_time / wave1_time
        
        if ratio < Wave3Characteristics.MIN_TIME_RATIO:
            return {
                "is_valid": False,
                "ratio": round(ratio, 2),
                "status": "too_short",
                "description": f"زمان موج 3 ({ratio:.1%}) کمتر از حداقل 150% موج 1 است"
            }
        elif ratio <= Wave3Characteristics.MAX_TIME_RATIO:
            return {
                "is_valid": True,
                "ratio": round(ratio, 2),
                "status": "normal",
                "description": f"زمان موج 3 ({ratio:.1%}) در محدوده مجاز (150% تا 500%) است"
            }
        elif ratio <= Wave3Characteristics.MAX_TIME_RATIO * 2:
            return {
                "is_valid": False,
                "ratio": round(ratio, 2),
                "status": "too_long",
                "description": f"زمان موج 3 ({ratio:.1%}) بیشتر از 500% موج 1 است"
            }
        else:
            return {
                "is_valid": False,
                "ratio": round(ratio, 2),
                "status": "excessive",
                "description": f"زمان موج 3 ({ratio:.1%}) بیش از حد مجاز است"
            }
    
    @staticmethod
    def check_price_ratio(wave1_price: float, wave3_price: float) -> Dict[str, Any]:
        """
        بررسی نسبت قیمتی موج 3 نسبت به موج 1
        
        صفحه 327: "از لحاظ قیمتی 1 تا 3 برابر موج 1 می‌باشد"
        """
        if wave1_price == 0:
            return {"is_valid": True, "ratio": 0, "status": "unknown"}
        
        ratio = wave3_price / wave1_price
        
        if ratio < Wave3Characteristics.MIN_PRICE_RATIO:
            return {
                "is_valid": False,
                "ratio": round(ratio, 2),
                "status": "too_small",
                "description": f"قیمت موج 3 ({ratio:.1%}) کمتر از موج 1 است"
            }
        elif ratio <= Wave3Characteristics.MAX_PRICE_RATIO:
            return {
                "is_valid": True,
                "ratio": round(ratio, 2),
                "status": "normal",
                "description": f"قیمت موج 3 ({ratio:.1%}) در محدوده مجاز (100% تا 300%) است"
            }
        else:
            return {
                "is_valid": False,
                "ratio": round(ratio, 2),
                "status": "too_large",
                "description": f"قیمت موج 3 ({ratio:.1%}) بیشتر از 300% موج 1 است"
            }
    
    @staticmethod
    def check_not_shortest(wave1_len: float, wave3_len: float, wave5_len: float) -> Dict[str, Any]:
        """
        بررسی اینکه موج 3 کوتاه‌ترین نباشد
        
        صفحه 327: "بین موج‌های 1 و 3 و 5 نمی‌تواند کوتاه‌ترین موج باشد"
        """
        if wave1_len == 0 or wave3_len == 0 or wave5_len == 0:
            return {"is_valid": True, "is_shortest": False}
        
        lengths = [wave1_len, wave3_len, wave5_len]
        min_len = min(lengths)
        is_shortest = wave3_len == min_len
        
        return {
            "is_valid": not is_shortest,
            "is_shortest": is_shortest,
            "wave1_len": wave1_len,
            "wave3_len": wave3_len,
            "wave5_len": wave5_len,
            "description": "موج 3 کوتاه‌ترین موج است" if is_shortest else "موج 3 کوتاه‌ترین موج نیست"
        }
    
    @staticmethod
    def check_time_minimum_requirement(wave1_time: int, wave2_time: int, wave3_time: int) -> Dict[str, Any]:
        """
        بررسی شرط حداقل زمان موج 3
        
        صفحه 327: "زمان موج 3 معمول حداقل بیش از نصف زمان صرف شده توسط موج 1 و 2 باشد"
        
        خروجی:
        - is_valid: bool
        - ratio: نسبت زمان موج 3 به نصف مجموع زمان موج 1 و 2
        - description: توضیح
        """
        if wave1_time == 0 and wave2_time == 0:
            return {"is_valid": True, "ratio": 0, "description": "داده کافی نیست"}
        
        half_sum_time = (wave1_time + wave2_time) / 2
        if half_sum_time == 0:
            return {"is_valid": True, "ratio": 0, "description": "زمان موج 1 و 2 صفر است"}
        
        ratio = wave3_time / half_sum_time
        
        if ratio > 1.0:
            return {
                "is_valid": True,
                "ratio": round(ratio, 2),
                "description": f"زمان موج 3 ({wave3_time}) بیش از نصف زمان موج 1+2 ({half_sum_time:.1f}) است - شرط رعایت شده"
            }
        else:
            return {
                "is_valid": False,
                "ratio": round(ratio, 2),
                "description": f"نقض شرط: زمان موج 3 ({wave3_time}) کمتر از نصف زمان موج 1+2 ({half_sum_time:.1f}) است"
            }
    
    @staticmethod
    def is_valid_wave3(wave_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        تشخیص معتبر بودن موج 3 بر اساس مشخصات کلیدی
        """
        violations = []
        
        # موج 3 باید شتابدار باشد
        if wave_data.get("wave_type") != "impulse":
            violations.append("موج 3 باید به شکل یک الگوی شتابدار باشد")
        
        # بررسی زمان
        time_check = Wave3Characteristics.check_time_ratio(
            wave_data.get("wave1_time", 0),
            wave_data.get("wave3_time", 0)
        )
        if not time_check["is_valid"]:
            violations.append(time_check["description"])
        
        # بررسی قیمت
        price_check = Wave3Characteristics.check_price_ratio(
            wave_data.get("wave1_price", 0),
            wave_data.get("wave3_price", 0)
        )
        if not price_check["is_valid"]:
            violations.append(price_check["description"])
        
        # بررسی کوتاه‌ترین نبودن
        shortest_check = Wave3Characteristics.check_not_shortest(
            wave_data.get("wave1_len", 0),
            wave_data.get("wave3_len", 0),
            wave_data.get("wave5_len", 0)
        )
        if not shortest_check["is_valid"]:
            violations.append(shortest_check["description"])
        
        # بررسی شرط حداقل زمانی (مشخصه 13)
        time_min_check = Wave3Characteristics.check_time_minimum_requirement(
            wave_data.get("wave1_time", 0),
            wave_data.get("wave2_time", 0),
            wave_data.get("wave3_time", 0)
        )
        if not time_min_check["is_valid"]:
            violations.append(time_min_check["description"])
        
        return len(violations) == 0, violations


# ═══════════════════════════════════════════════════════════════════════════════
# بخش 5: مشخصات موج 4 (صفحه 328) - 14 مشخصه
# ═══════════════════════════════════════════════════════════════════════════════


class Wave4Characteristics:
    """
    مشخصات موج 4 بر اساس کتاب گلن نیلی - صفحه 328
    
    ویژگی‌های کلیدی موج 4 (14 مشخصه):
    1. موج شناسایی سود
    2. بسیاری شروع به شناسایی سود می‌کنند
    3. دارای ماهیت متفاوت با موج 2 می‌باشد
    4. بسیاری از سرمایه‌گذاران در موج 4 پول بسیاری از دست می‌دهند
    5. مدت زمان بسیار بیشتری طول می‌کشد
    6. با موج 2 در تناوب می‌باشد
    7. در ریز موج چهارم از موج 3 معمول خاتمه می‌یابد
    8. معمول حداکثر تا 50 درصد موج 3 را اصلاح می‌کند
    9. می‌تواند به شکل هر یک از انواع الگوی اصلی باشد و لیکن به ندرت به شکل الگوی زیگزاگ می‌باشد
    10. حداکثر زمان آن دو برابر موج 3 و تا 270 درصد موج 2 می‌باشد
    11. زمانی که موج 5 ممتد می‌باشد بلندتر از موج 2 خواهد بود و اغلب تا 61.8 درصد موج 3 را اصلاح خواهد کرد
    12. در موج 5 کوتاه شده نیز پیچیده‌ترین بخش خواهد بود و بیش از 38.2 و حداکثر تا 61.8 درصد موج 3 را اصلاح خواهد کرد
    13. زمان موج 4 باید بیش از زمان صرف شده توسط موج 3 باشد
    """
    
    MAX_RETRACEMENT_NORMAL = 0.5      # حداکثر 50% در حالت معمول
    MAX_RETRACEMENT_EXTENDED = 0.618  # حداکثر 61.8% در حالت ممتد
    MIN_RETRACEMENT_TRUNCATED = 0.382 # حداقل 38.2% در حالت کوتاه شده
    
    @staticmethod
    def get_characteristics() -> Dict[str, str]:
        """بازگرداندن لیست کامل 14 مشخصات موج 4"""
        return {
            "profit_taking": "موج شناسایی سود",
            "profit_taking_start": "بسیاری شروع به شناسایی سود می‌کنند",
            "different_nature": "دارای ماهیت متفاوت با موج 2 می‌باشد",
            "investor_loss": "بسیاری از سرمایه‌گذاران در موج 4 پول بسیاری از دست می‌دهند",
            "longer_duration": "مدت زمان بسیار بیشتری طول می‌کشد",
            "alternation_with_wave2": "با موج 2 در تناوب می‌باشد",
            "ends_in_subwave4": "در ریز موج چهارم از موج 3 معمول خاتمه می‌یابد",
            "max_retracement": "معمول حداکثر تا 50 درصد موج 3 را اصلاح می‌کند",
            "pattern_flexibility": "می‌تواند به شکل هر یک از انواع الگوی اصلی باشد و لیکن به ندرت به شکل الگوی زیگزاگ می‌باشد",
            "time_limits": "حداکثر زمان آن دو برابر موج 3 و تا 270 درصد موج 2 می‌باشد",
            "wave5_extended": "زمانی که موج 5 ممتد می‌باشد بلندتر از موج 2 خواهد بود و اغلب تا 61.8 درصد موج 3 را اصلاح خواهد کرد",
            "wave5_truncated": "در موج 5 کوتاه شده نیز پیچیده‌ترین بخش خواهد بود و بیش از 38.2 و حداکثر تا 61.8 درصد موج 3 را اصلاح خواهد کرد",
            "time_requirement": "زمان موج 4 باید بیش از زمان صرف شده توسط موج 3 باشد"
        }
    
    @staticmethod
    def check_retracement(retracement_pct: float, is_wave5_extended: bool = False, is_wave5_truncated: bool = False) -> Dict[str, Any]:
        """
        بررسی درصد اصلاح موج 4 نسبت به موج 3
        
        صفحه 328:
        - معمول حداکثر تا 50 درصد موج 3 را اصلاح می‌کند
        - در موج 5 ممتد: اغلب تا 61.8 درصد
        - در موج 5 کوتاه شده: بیش از 38.2 و حداکثر تا 61.8 درصد
        """
        if is_wave5_extended:
            is_valid = retracement_pct <= Wave4Characteristics.MAX_RETRACEMENT_EXTENDED
            description = f"در موج 5 ممتد، اصلاح موج 4 ({retracement_pct:.1%}) باید حداکثر 61.8% باشد"
        elif is_wave5_truncated:
            is_valid = Wave4Characteristics.MIN_RETRACEMENT_TRUNCATED < retracement_pct <= Wave4Characteristics.MAX_RETRACEMENT_EXTENDED
            description = f"در موج 5 کوتاه شده، اصلاح موج 4 ({retracement_pct:.1%}) باید بین 38.2% تا 61.8% باشد"
        else:
            is_valid = retracement_pct <= Wave4Characteristics.MAX_RETRACEMENT_NORMAL
            description = f"اصلاح موج 4 ({retracement_pct:.1%}) باید حداکثر 50% موج 3 باشد"
        
        return {
            "is_valid": is_valid,
            "retracement_pct": round(retracement_pct * 100, 1),
            "description": description
        }
    
    @staticmethod
    def check_time_ratio(wave3_time: int, wave4_time: int, wave2_time: int = 0) -> Dict[str, Any]:
        """
        بررسی محدودیت‌های زمانی موج 4
        
        صفحه 328:
        - زمان موج 4 باید بیش از زمان موج 3 باشد
        - حداکثر زمان آن دو برابر موج 3 و تا 270 درصد موج 2 می‌باشد
        """
        results = {}
        
        # شرط اول: زمان موج 4 > زمان موج 3 (مشخصه 13)
        if wave3_time > 0:
            ratio_vs_wave3 = wave4_time / wave3_time
            results["greater_than_wave3"] = {
                "is_valid": ratio_vs_wave3 > 1.0,
                "ratio": round(ratio_vs_wave3, 2),
                "description": f"زمان موج 4 ({wave4_time}) باید بیشتر از موج 3 ({wave3_time}) باشد"
            }
            
            # حداکثر دو برابر موج 3 (مشخصه 10 - بخش اول)
            results["max_vs_wave3"] = {
                "is_valid": ratio_vs_wave3 <= 2.0,
                "ratio": round(ratio_vs_wave3, 2),
                "description": f"حداکثر زمان موج 4 دو برابر موج 3 است (نسبت فعلی: {ratio_vs_wave3:.2f})"
            }
        
        # شرط دوم: حداکثر 270 درصد موج 2 (مشخصه 10 - بخش دوم)
        if wave2_time > 0:
            ratio_vs_wave2 = wave4_time / wave2_time
            results["max_vs_wave2"] = {
                "is_valid": ratio_vs_wave2 <= 2.7,
                "ratio": round(ratio_vs_wave2, 2),
                "description": f"حداکثر زمان موج 4 تا 270% موج 2 است (نسبت فعلی: {ratio_vs_wave2:.2f})"
            }
        
        return results
    
    @staticmethod
    def check_time_greater_than_wave3(wave3_time: int, wave4_time: int) -> Dict[str, Any]:
        """
        بررسی شرط مستقل زمان موج 4 بیشتر از موج 3 (مشخصه 13)
        
        صفحه 328: "زمان موج 4 باید بیش از زمان صرف شده توسط موج 3 باشد"
        """
        if wave3_time == 0:
            return {"is_valid": True, "description": "داده زمانی موج 3 کافی نیست"}
        
        if wave4_time > wave3_time:
            return {
                "is_valid": True,
                "wave3_time": wave3_time,
                "wave4_time": wave4_time,
                "description": f"زمان موج 4 ({wave4_time}) بیشتر از موج 3 ({wave3_time}) است - شرط رعایت شده"
            }
        else:
            return {
                "is_valid": False,
                "wave3_time": wave3_time,
                "wave4_time": wave4_time,
                "description": f"نقض شرط: زمان موج 4 ({wave4_time}) کمتر یا برابر موج 3 ({wave3_time}) است"
            }
    
    @staticmethod
    def is_valid_wave4(wave_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """تشخیص معتبر بودن موج 4 بر اساس مشخصات کلیدی"""
        violations = []
        
        # موج 4 باید اصلاحی باشد (به ندرت زیگزاگ)
        if wave_data.get("pattern") == "zigzag":
            violations.append("موج 4 به ندرت به شکل الگوی زیگزاگ می‌باشد")
        
        # بررسی زمان (مشخصه 13: زمان موج 4 باید بیشتر از موج 3 باشد)
        time_greater_check = Wave4Characteristics.check_time_greater_than_wave3(
            wave_data.get("wave3_time", 0),
            wave_data.get("wave4_time", 0)
        )
        if not time_greater_check["is_valid"]:
            violations.append(time_greater_check["description"])
        
        # بررسی سایر محدودیت‌های زمانی
        time_check = Wave4Characteristics.check_time_ratio(
            wave_data.get("wave3_time", 0),
            wave_data.get("wave4_time", 0),
            wave_data.get("wave2_time", 0)
        )
        
        if "max_vs_wave3" in time_check and not time_check["max_vs_wave3"]["is_valid"]:
            violations.append(time_check["max_vs_wave3"]["description"])
        
        if "max_vs_wave2" in time_check and not time_check["max_vs_wave2"]["is_valid"]:
            violations.append(time_check["max_vs_wave2"]["description"])
        
        # بررسی اصلاح
        retracement_check = Wave4Characteristics.check_retracement(
            wave_data.get("retracement_pct", 0),
            wave_data.get("is_wave5_extended", False),
            wave_data.get("is_wave5_truncated", False)
        )
        if not retracement_check["is_valid"]:
            violations.append(retracement_check["description"])
        
        return len(violations) == 0, violations


# ═══════════════════════════════════════════════════════════════════════════════
# بخش 6: مشخصات موج 5 (صفحه 329) - 12 مشخصه
# ═══════════════════════════════════════════════════════════════════════════════


class Wave5Characteristics:
    """
    مشخصات موج 5 بر اساس کتاب گلن نیلی - صفحه 329
    
    ویژگی‌های کلیدی موج 5 (12 مشخصه):
    1. آخرین امید و تلاش برای سود در بازار
    2. نسبت به موج 3 از پویایی کمتری برخوردار می‌باشد
    3. واگرایی منفی در اندیکاتورها قابل مشاهده است
    4. خوش‌بین‌ها بر حرفی می‌کنند
    5. صرفاً به شکل یک الگوی شتابدار یا الگوی ترمینال می‌تواند باشد
    6. گاهی موج 5 نمی‌تواند خودش را بالاتر از موج 3 بکشد (کوتاه شده)
    7. معمول نسبت به موج 3 از سرعت تغییرات قیمتی کمتری برخوردار است مگر آنکه انبساط یابد
    8. حجم نسبت به موج 3 کاهش می‌یابد
    9. اگر بلندتر از موج 3 باشد حتماً الگوی شتابدار می‌باشد
    10. بیش از 38.2 درصد موج 4 را باید اصلاح کند
    11. اگر موج 5 غیرممتد باشد، اصلاح متعاقب تا حوالی موج 4 خواهد بود
    12. در موج 5 غیر ممتد کل موج توسط اصلاح متعاقب باید اصلاح گردد
    """
    
    MIN_RETRACEMENT_OF_WAVE4 = 0.382  # حداقل 38.2% اصلاح موج 4
    
    @staticmethod
    def get_characteristics() -> Dict[str, str]:
        """بازگرداندن لیست کامل 12 مشخصات موج 5"""
        return {
            "last_hope": "آخرین امید و تلاش برای سود در بازار",
            "less_dynamic": "نسبت به موج 3 از پویایی کمتری برخوردار می‌باشد",
            "negative_divergence": "واگرایی منفی در اندیکاتورها قابل مشاهده است",
            "optimists_talk": "خوش‌بین‌ها بر حرفی می‌کنند",
            "pattern_type": "صرفاً به شکل یک الگوی شتابدار یا الگوی ترمینال می‌تواند باشد",
            "truncated_possible": "گاهی موج 5 نمی‌تواند خودش را بالاتر از موج 3 بکشد (کوتاه شده)",
            "slower_momentum": "معمول نسبت به موج 3 از سرعت تغییرات قیمتی کمتری برخوردار است مگر آنکه انبساط یابد",
            "volume_decrease": "حجم نسبت به موج 3 کاهش می‌یابد",
            "extended_impulsive": "اگر بلندتر از موج 3 باشد حتماً الگوی شتابدار می‌باشد",
            "min_retracement": "بیش از 38.2 درصد موج 4 را باید اصلاح کند",
            "post_pattern_correction": "اگر موج 5 غیرممتد باشد، اصلاح متعاقب تا حوالی موج 4 خواهد بود",
            "full_correction": "در موج 5 غیر ممتد کل موج توسط اصلاح متعاقب باید اصلاح گردد"
        }
    
    @staticmethod
    def check_retracement_of_wave4(retracement_pct: float) -> Dict[str, Any]:
        """
        بررسی اصلاح موج 5 نسبت به موج 4
        
        صفحه 329: "بیش از 38.2 درصد موج 4 را باید اصلاح کند"
        """
        is_valid = retracement_pct > Wave5Characteristics.MIN_RETRACEMENT_OF_WAVE4
        
        return {
            "is_valid": is_valid,
            "retracement_pct": round(retracement_pct * 100, 1),
            "min_required": f"{Wave5Characteristics.MIN_RETRACEMENT_OF_WAVE4 * 100:.0f}%",
            "description": f"اصلاح موج 5 نسبت به موج 4: {retracement_pct:.1%} (حداقل مورد نیاز: 38.2%)"
        }
    
    @staticmethod
    def check_negative_divergence(price_data: List[float], rsi_data: List[float], 
                                  lookback: int = 50) -> Dict[str, Any]:
        """
        بررسی واگرایی منفی بین قیمت و RSI (الگوریتم دقیق نئوویو)
        
        صفحه 329: "واگرایی منفی در اندیکاتورها قابل مشاهده است"
        
        واگرایی منفی (Negative Divergence / Bearish Divergence):
        قیمت قله بالاتر (Higher High) می‌زند اما RSI قله پایین‌تر (Lower High) می‌زند.
        
        پارامترها:
        - price_data: لیست قیمت‌های بسته شدن
        - rsi_data: لیست مقادیر RSI (متناسب با قیمت)
        - lookback: پنجره جستجو برای یافتن قله‌ها
        
        خروجی:
        - has_divergence: bool - آیا واگرایی منفی وجود دارد
        - divergence_type: str - نوع واگرایی (classic / hidden)
        - price_peaks: لیست قله‌های قیمتی شناسایی شده
        - rsi_at_peaks: لیست مقادیر RSI در قله‌های قیمتی
        - description: توضیح کامل
        - strength: قدرت واگرایی (weak/medium/strong)
        """
        if len(price_data) < 10 or len(rsi_data) < 10:
            return {
                "has_divergence": False,
                "divergence_type": None,
                "price_peaks": [],
                "rsi_at_peaks": [],
                "description": "داده کافی برای تشخیص واگرایی نیست (حداقل 10 کندل نیاز است)",
                "strength": None
            }
        
        # همگام‌سازی طول داده‌ها
        min_len = min(len(price_data), len(rsi_data))
        price = price_data[-min_len:]
        rsi = rsi_data[-min_len:]
        
        # ────────────────────────────────────────────────────────────────────
        # گام 1: یافتن قله‌های محلی در قیمت (حداقل 3 کندل فاصله)
        # ────────────────────────────────────────────────────────────────────
        price_peaks = []  # list of (index, price, rsi_value_at_peak)
        min_bars_between_peaks = 3
        
        for i in range(2, len(price) - 2):
            is_peak = True
            for j in range(1, 3):
                if i - j >= 0:
                    if price[i] <= price[i - j]:
                        is_peak = False
                        break
                if i + j < len(price):
                    if price[i] <= price[i + j]:
                        is_peak = False
                        break
            
            if is_peak:
                # بررسی فاصله از قله قبلی
                if len(price_peaks) > 0:
                    if i - price_peaks[-1][0] < min_bars_between_peaks:
                        # اگر قله جدید بالاتر است، قله قبلی را جایگزین کن
                        if price[i] > price_peaks[-1][1]:
                            price_peaks.pop()
                        else:
                            continue
                price_peaks.append((i, price[i], rsi[i]))
        
        # ────────────────────────────────────────────────────────────────────
        # گام 2: یافتن قله‌های محلی در RSI (برای تطبیق)
        # ────────────────────────────────────────────────────────────────────
        rsi_peaks = []
        for i in range(2, len(rsi) - 2):
            is_peak = True
            for j in range(1, 3):
                if i - j >= 0:
                    if rsi[i] <= rsi[i - j]:
                        is_peak = False
                        break
                if i + j < len(rsi):
                    if rsi[i] <= rsi[i + j]:
                        is_peak = False
                        break
            
            if is_peak:
                if len(rsi_peaks) > 0:
                    if i - rsi_peaks[-1][0] < min_bars_between_peaks:
                        if rsi[i] > rsi_peaks[-1][1]:
                            rsi_peaks.pop()
                        else:
                            continue
                rsi_peaks.append((i, rsi[i]))
        
        # ────────────────────────────────────────────────────────────────────
        # گام 3: تشخیص واگرایی کلاسیک (Classic Divergence)
        # قیمت قله بالاتر (Higher High) + RSI قله پایین‌تر (Lower High)
        # ────────────────────────────────────────────────────────────────────
        classic_divergence = False
        divergence_strength = "weak"
        price_peaks_info = []
        rsi_at_identified_peaks = []
        
        if len(price_peaks) >= 2:
            # دو قله آخر قیمت
            p1_idx, p1_price, p1_rsi = price_peaks[-2]
            p2_idx, p2_price, p2_rsi = price_peaks[-1]
            
            # شرط واگرایی کلاسیک: قیمت قله بالاتر + RSI قله پایین‌تر
            price_higher_high = p2_price > p1_price
            rsi_lower_high = p2_rsi < p1_rsi
            
            if price_higher_high and rsi_lower_high:
                classic_divergence = True
                # تعیین قدرت واگرایی بر اساس اختلاف درصدی
                price_diff_pct = (p2_price - p1_price) / p1_price * 100
                rsi_diff = p1_rsi - p2_rsi
                
                if price_diff_pct > 10 and rsi_diff > 10:
                    divergence_strength = "strong"
                elif price_diff_pct > 5 or rsi_diff > 5:
                    divergence_strength = "medium"
                else:
                    divergence_strength = "weak"
                
                price_peaks_info = [
                    {"index": p1_idx, "price": round(p1_price, 4), "rsi": round(p1_rsi, 1)},
                    {"index": p2_idx, "price": round(p2_price, 4), "rsi": round(p2_rsi, 1)}
                ]
                rsi_at_identified_peaks = [round(p1_rsi, 1), round(p2_rsi, 1)]
        
        # ────────────────────────────────────────────────────────────────────
        # گام 4: تشخیص واگرایی پنهان (Hidden Divergence) - کمتر رایج
        # قیمت قله پایین‌تر (Lower High) + RSI قله بالاتر (Higher High)
        # ────────────────────────────────────────────────────────────────────
        hidden_divergence = False
        
        if len(price_peaks) >= 2 and len(rsi_peaks) >= 2:
            p1_idx, p1_price, p1_rsi = price_peaks[-2]
            p2_idx, p2_price, p2_rsi = price_peaks[-1]
            
            price_lower_high = p2_price < p1_price
            rsi_higher_high = p2_rsi > p1_rsi
            
            if price_lower_high and rsi_higher_high:
                hidden_divergence = True
        
        # ────────────────────────────────────────────────────────────────────
        # گام 5: خروجی نهایی
        # ────────────────────────────────────────────────────────────────────
        has_divergence = classic_divergence or hidden_divergence
        divergence_type = None
        
        if classic_divergence:
            divergence_type = "کلاسیک (Bearish)"
        elif hidden_divergence:
            divergence_type = "پنهان"
        
        # ساخت توضیحات
        if classic_divergence:
            description = (
                f"✅ واگرایی منفی {divergence_type} تشخیص داده شد. "
                f"قیمت قله {price_peaks_info[-1]['price']:.2f} بالاتر از قله قبلی "
                f"({price_peaks_info[-2]['price']:.2f}) اما RSI قله {rsi_at_identified_peaks[-1]:.1f} "
                f"پایین‌تر از قله قبلی ({rsi_at_identified_peaks[-2]:.1f}) است. "
                f"قدرت واگرایی: {divergence_strength}"
            )
        elif hidden_divergence:
            description = (
                f"⚠️ واگرایی پنهان تشخیص داده شد. این نوع واگرایی نشانه ادامه روند است."
            )
        else:
            description = "واگرایی منفی تشخیص داده نشد. بازار در وضعیت عادی قرار دارد."
        
        return {
            "has_divergence": has_divergence,
            "divergence_type": divergence_type,
            "price_peaks": price_peaks_info,
            "rsi_at_peaks": rsi_at_identified_peaks,
            "description": description,
            "strength": divergence_strength if classic_divergence else None,
            "total_peaks_found": len(price_peaks),
            "lookback": lookback
        }
    
    @staticmethod
    def is_truncated(wave5_high: float, wave3_high: float) -> Dict[str, Any]:
        """
        بررسی کوتاه شدن موج 5
        
        صفحه 329: "گاهی موج 5 نمی‌تواند خودش را بالاتر از موج 3 بکشد (کوتاه شده)"
        """
        is_truncated = wave5_high <= wave3_high
        
        return {
            "is_truncated": is_truncated,
            "wave3_high": wave3_high,
            "wave5_high": wave5_high,
            "description": "موج 5 کوتاه شده است" if is_truncated else "موج 5 کوتاه نشده است"
        }
    
    @staticmethod
    def is_valid_wave5(wave_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """تشخیص معتبر بودن موج 5 بر اساس مشخصات کلیدی"""
        violations = []
        
        # موج 5 باید شتابدار یا ترمینال باشد
        wave_type = wave_data.get("wave_type", "")
        if wave_type not in ["impulse", "terminal"]:
            violations.append("موج 5 باید به شکل یک الگوی شتابدار یا الگوی ترمینال باشد")
        
        # بررسی اصلاح موج 4
        retracement_check = Wave5Characteristics.check_retracement_of_wave4(
            wave_data.get("retracement_of_wave4_pct", 0)
        )
        if not retracement_check["is_valid"]:
            violations.append(retracement_check["description"])
        
        # بررسی حجم (کاهش نسبت به موج 3)
        if "wave3_volume" in wave_data and "wave5_volume" in wave_data:
            if wave_data["wave5_volume"] > wave_data["wave3_volume"]:
                violations.append("حجم موج 5 باید نسبت به موج 3 کاهش یابد")
        
        return len(violations) == 0, violations


# ═══════════════════════════════════════════════════════════════════════════════
# بخش 7: جدول شباهت الگوها (صفحه 323)
# ═══════════════════════════════════════════════════════════════════════════════


class PatternSimilarityTable:
    """
    جدول مقایسه الگوها از نظر شباهت (صفحه 323)
    
    ┌─────────────────────────────────────────────────────────────────┐
    │ الگو       │ شباهت قیمتی │ شباهت زمانی │ شباهت پیچیدگی │
    ├─────────────────────────────────────────────────────────────────┤
    │ زیگزاگ    │      *      │      *      │       *       │
    │ مسطح      │      ✓      │      *      │       *       │
    │ مثلث      │      *      │      *      │       ✓       │
    │ دیامتریک  │      *      │      ✓      │       ✓       │
    │ سیمتریک   │      ✓      │      ✓      │       ✓       │
    └─────────────────────────────────────────────────────────────────┘
    (* = عدم تشابه، ✓ = تشابه)
    """
    
    # جدول شباهت‌ها
    SIMILARITY_MATRIX = {
        "زیگزاگ": {"price": False, "time": False, "complexity": False},
        "مسطح": {"price": True, "time": False, "complexity": False},
        "مثلث": {"price": False, "time": False, "complexity": True},
        "دیامتریک": {"price": False, "time": True, "complexity": True},
        "سیمتریک": {"price": True, "time": True, "complexity": True}
    }
    
    @classmethod
    def get_similarity(cls, pattern: str) -> Dict[str, bool]:
        """بازگرداندن شباهت‌های یک الگو"""
        return cls.SIMILARITY_MATRIX.get(pattern, {"price": False, "time": False, "complexity": False})
    
    @classmethod
    def get_all_similarities(cls) -> Dict[str, Dict[str, bool]]:
        """بازگرداندن جدول کامل شباهت‌ها"""
        return cls.SIMILARITY_MATRIX
    
    @classmethod
    def suggest_pattern_by_similarity(cls, price_similar: bool, time_similar: bool, complexity_similar: bool) -> str:
        """
        پیشنهاد نوع الگو بر اساس شباهت‌های مشاهده شده
        
        صفحه 323: جدول مقایسه الگوها
        """
        if price_similar and time_similar and complexity_similar:
            return "سیمتریک"
        elif time_similar and complexity_similar:
            return "دیامتریک"
        elif complexity_similar:
            return "مثلث"
        elif price_similar:
            return "مسطح"
        else:
            return "زیگزاگ"


# ═══════════════════════════════════════════════════════════════════════════════
# بخش 8: محدودیت‌های زمانی در اصلاحات (صفحه 324)
# ═══════════════════════════════════════════════════════════════════════════════


class TimeLimitsInCorrections:
    """
    محدودیت‌های زمانی در اصلاحات (صفحه 324)
    
    قوانین:
    - بخش دوم زمان کمتر از بخش اول: غیرقابل قبول (فقط در شبیه‌سازی X-wave ممکن است)
    - بخش دوم زمان 161.8 تا 261.8 درصد بخش اول: متداول
    - بخش اول و دوم برابر در زمان: حداقل
    - بخش دوم زمان بیشتر از 261.8 درصد بخش اول: غیرقابل قبول (فقط در شرایط نادر)
    """
    
    MIN_COMMON_RATIO = 1.618   # 161.8%
    MAX_COMMON_RATIO = 2.618   # 261.8%
    UNACCEPTABLE_LONG_RATIO = 2.618  # بیشتر از این مقدار غیرقابل قبول است
    
    @staticmethod
    def check_time_ratio(segment1_time: int, segment2_time: int) -> Dict[str, Any]:
        """
        بررسی نسبت زمانی بین دو بخش اصلاح
        
        خروجی:
        - status: TimeLimitStatus
        - is_valid: آیا نسبت زمانی قابل قبول است
        - description: توضیح وضعیت
        """
        if segment1_time == 0:
            return {"status": TimeLimitStatus.COMMON, "is_valid": True, "ratio": 0, "description": "داده کافی نیست"}
        
        ratio = segment2_time / segment1_time
        
        if ratio < 1.0:
            return {
                "status": TimeLimitStatus.UNACCEPTABLE_SHORT,
                "is_valid": False,
                "ratio": round(ratio, 2),
                "description": f"بخش دوم ({segment2_time}) زمان کمتر از بخش اول ({segment1_time}) - غیرقابل قبول (فقط در X-wave مجاز است)"
            }
        elif ratio == 1.0:
            return {
                "status": TimeLimitStatus.MINIMUM_EQUAL,
                "is_valid": True,
                "ratio": round(ratio, 2),
                "description": f"بخش اول و دوم برابر در زمان ({segment1_time} = {segment2_time}) - حداقل مجاز"
            }
        elif ratio <= TimeLimitsInCorrections.MAX_COMMON_RATIO:
            return {
                "status": TimeLimitStatus.COMMON,
                "is_valid": True,
                "ratio": round(ratio, 2),
                "description": f"بخش دوم ({ratio:.1%}) زمان بخش اول - در محدوده متداول (161.8% تا 261.8%)"
            }
        else:
            return {
                "status": TimeLimitStatus.UNACCEPTABLE_LONG,
                "is_valid": False,
                "ratio": round(ratio, 2),
                "description": f"بخش دوم ({ratio:.1%}) زمان بیشتر از 261.8% بخش اول - غیرقابل قبول (فقط در شرایط نادر)"
            }


# ═══════════════════════════════════════════════════════════════════════════════
# بخش 9: تابع اصلی analyze (Interface برای main.py)
# ═══════════════════════════════════════════════════════════════════════════════


def analyze(data: pd.DataFrame, logger=None) -> Dict:
    """
    فصل 13: صفات و مشخصات موج‌ها (Wave Characteristics)
    
    این تابع مطابق با interface تعریف شده در main.py پیاده‌سازی شده است.
    
    صفحات پوشش داده شده: 324 تا 329
    
    خروجی:
        دیکشنری شامل تمام مشخصات موج‌های 1 تا 5، جدول شباهت‌ها و محدودیت‌های زمانی
    """
    close = data['close'].values if 'close' in data.columns else data['Close'].values
    high = data['high'].values if 'high' in data.columns else data['High'].values
    low = data['low'].values if 'low' in data.columns else data['Low'].values
    volume = data['volume'].values if 'volume' in data.columns else None
    n = len(close)
    
    if n < 10:
        return {
            "عنوان": "فصل 13: صفات و مشخصات موج‌ها",
            "وضعیت": "داده_کافی_نیست",
            "تعداد_کندل": str(n),
            "تفسیر_نهایی": "خطا: برای تحلیل مشخصات موج‌ها به حداقل 10 کندل نیاز است."
        }
    
    # ========================================================================
    # محاسبات پایه برای شناسایی امواج
    # ========================================================================
    
    # تشخیص نقاط عطف ساده
    pivots = []
    window = 3
    for i in range(window, n - window):
        if high[i] == max(high[i - window:i + window + 1]):
            pivots.append({"type": "H", "index": i, "price": high[i]})
        if low[i] == min(low[i - window:i + window + 1]):
            pivots.append({"type": "L", "index": i, "price": low[i]})
    
    # تخمین موقعیت امواج اصلی
    # ========================================================================
    # الگوریتم پیشرفته شناسایی امواج 1 تا 5 (نئوویو - سطح حرفه‌ای)
    # ========================================================================
    
    def find_zigzag_pivots(data_high, data_low, data_close, min_bars=3, threshold_pct=0.5):
        """یافتن نقاط عطف زیگزاگ با حساسیت قابل تنظیم"""
        n = len(data_high)
        pivots = []
        i = min_bars
        last_price = data_close[0]
        
        while i < n - min_bars:
            # بررسی قله محلی
            is_high = all(data_high[i] >= data_high[i-j] for j in range(1, min_bars+1)) and \
                      all(data_high[i] >= data_high[i+j] for j in range(1, min_bars+1))
            
            # بررسی کف محلی
            is_low = all(data_low[i] <= data_low[i-j] for j in range(1, min_bars+1)) and \
                     all(data_low[i] <= data_low[i+j] for j in range(1, min_bars+1))
            
            if is_high:
                # بررسی درصد تغییر از آخرین نقطه عطف
                if pivots:
                    change_pct = abs(data_high[i] - pivots[-1]["price"]) / pivots[-1]["price"] * 100
                    if change_pct < threshold_pct:
                        i += 1
                        continue
                pivots.append({"type": "H", "index": i, "price": data_high[i]})
                i += min_bars
            elif is_low:
                if pivots:
                    change_pct = abs(data_low[i] - pivots[-1]["price"]) / pivots[-1]["price"] * 100
                    if change_pct < threshold_pct:
                        i += 1
                        continue
                pivots.append({"type": "L", "index": i, "price": data_low[i]})
                i += min_bars
            else:
                i += 1
        
        return pivots
    
    # شناسایی نقاط عطف اصلی
    main_pivots = find_zigzag_pivots(high, low, close, min_bars=5, threshold_pct=1.0)
    
    # ========================================================================
    # تشخیص ساختار 5 موجی با استفاده از قانون نقض‌ناپذیر نئوویو
    # ========================================================================
    
    wave_patterns = []  # ذخیره الگوهای 5 موجی پیدا شده
    
    for i in range(len(main_pivots) - 4):
        segment = main_pivots[i:i+5]
        types = [p["type"] for p in segment]
        
        # بررسی الگوی متناوب H,L,H,L,H یا L,H,L,H,L
        if types == ["H","L","H","L","H"] or types == ["L","H","L","H","L"]:
            # محاسبه نسبت‌های فیبوناچی
            w1_len = abs(segment[1]["price"] - segment[0]["price"])
            w2_len = abs(segment[2]["price"] - segment[1]["price"])
            w3_len = abs(segment[3]["price"] - segment[2]["price"])
            w4_len = abs(segment[4]["price"] - segment[3]["price"])
            
            # قانون 1: موج 2 نباید 100% موج 1 را اصلاح کند
            if w2_len >= w1_len:
                continue
            
            # قانون 3: موج 4 نباید با موج 1 همپوشانی داشته باشد
            if types[0] == "H":  # روند نزولی
                if segment[4]["price"] > segment[0]["price"]:
                    continue
            else:  # روند صعودی
                if segment[4]["price"] < segment[0]["price"]:
                    continue
            
            wave_patterns.append({
                "start_idx": segment[0]["index"],
                "end_idx": segment[4]["index"],
                "direction": "DOWN" if types[0] == "H" else "UP",
                "wave1": {"start": segment[0]["index"], "end": segment[1]["index"], "price": w1_len},
                "wave2": {"start": segment[1]["index"], "end": segment[2]["index"], "price": w2_len},
                "wave3": {"start": segment[2]["index"], "end": segment[3]["index"], "price": w3_len},
                "wave4": {"start": segment[3]["index"], "end": segment[4]["index"], "price": w4_len},
                "wave5_price": w3_len,  # تخمینی
            })
    
    # ========================================================================
    # انتخاب قوی‌ترین الگوی 5 موجی (با بیشترین تطابق با قوانین نئوویو)
    # ========================================================================
    
    best_pattern = None
    best_score = -1
    
    for pattern in wave_patterns:
        score = 0
        # موج 3 نباید کوتاه‌ترین باشد
        w1, w3, w5 = pattern["wave1"]["price"], pattern["wave3"]["price"], pattern.get("wave5_price", 0)
        if w3 >= w1 and w3 >= w5:
            score += 2
        
        # نسبت فیبوناچی موج 3 به موج 1 (ایده‌آل 1.618)
        if w1 > 0:
            ratio = w3 / w1
            if 1.5 <= ratio <= 2.618:
                score += 2
            elif 1.0 <= ratio <= 3.0:
                score += 1
        
        if score > best_score:
            best_score = score
            best_pattern = pattern
    
    # ========================================================================
    # استخراج موقعیت دقیق امواج 1 تا 5 از بهترین الگو
    # ========================================================================
    
    wave_positions = {
        "wave1": {"start": 0, "end": n // 5},
        "wave2": {"start": n // 5, "end": 2 * n // 5},
        "wave3": {"start": 2 * n // 5, "end": 3 * n // 5},
        "wave4": {"start": 3 * n // 5, "end": 4 * n // 5},
        "wave5": {"start": 4 * n // 5, "end": n - 1}
    }
    
    if best_pattern:
        # جایگزینی با موقعیت‌های دقیق از الگوی شناسایی شده
        total_bars = best_pattern["end_idx"] - best_pattern["start_idx"]
        if total_bars > 0:
            wave_positions["wave1"]["start"] = best_pattern["wave1"]["start"]
            wave_positions["wave1"]["end"] = best_pattern["wave1"]["end"]
            wave_positions["wave2"]["start"] = best_pattern["wave2"]["start"]
            wave_positions["wave2"]["end"] = best_pattern["wave2"]["end"]
            wave_positions["wave3"]["start"] = best_pattern["wave3"]["start"]
            wave_positions["wave3"]["end"] = best_pattern["wave3"]["end"]
            wave_positions["wave4"]["start"] = best_pattern["wave4"]["start"]
            wave_positions["wave4"]["end"] = best_pattern["wave4"]["end"]
            
            # تخمین موج 5 (آخرین موج تا پایان الگو)
            wave_positions["wave5"]["start"] = best_pattern["wave4"]["end"]
            wave_positions["wave5"]["end"] = best_pattern["end_idx"]
    
    # اطمینان از معتبر بودن بازه‌ها
    for wave_name in wave_positions:
        if wave_positions[wave_name]["start"] >= wave_positions[wave_name]["end"]:
            wave_positions[wave_name]["end"] = min(wave_positions[wave_name]["start"] + 1, n - 1)
        if wave_positions[wave_name]["end"] >= n:
            wave_positions[wave_name]["end"] = n - 1
    
    # محاسبه مشخصات هر موج
    wave_data = {}
    
    for wave_name, pos in wave_positions.items():
        if pos["start"] < pos["end"] and pos["end"] < n:
            wave_data[wave_name] = {
                "start_price": close[pos["start"]],
                "end_price": close[pos["end"]],
                "high": max(high[pos["start"]:pos["end"] + 1]),
                "low": min(low[pos["start"]:pos["end"] + 1]),
                "length": abs(close[pos["end"]] - close[pos["start"]]),
                "time": pos["end"] - pos["start"],
                "volume": sum(volume[pos["start"]:pos["end"] + 1]) if volume is not None else 0
            }
    
    # ========================================================================
    # محاسبه RSI برای تشخیص واگرایی
    # ========================================================================
    rsi_values = []
    period = 14
    if n > period:
        delta = np.diff(close)
        gain = np.where(delta > 0, delta, 0.0)
        loss = np.where(delta < 0, -delta, 0.0)
        
        # محاسبه RSI برای هر نقطه
        for i in range(period, n):
            avg_gain = np.mean(gain[i - period:i])
            avg_loss = np.mean(loss[i - period:i])
            if avg_loss == 0:
                rsi = 100.0
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)
        
        # همگام‌سازی طول با قیمت
        rsi_values = [50.0] * period + rsi_values
    
    # ========================================================================
    # تحلیل واگرایی منفی (صفحه 329)
    # ========================================================================
    divergence_analysis = Wave5Characteristics.check_negative_divergence(
        close.tolist(), rsi_values, lookback=min(50, n)
    )

    # ========================================================================
    # محدودیت‌های زمانی صفحه 324 (اعمال روی داده)
    # ========================================================================
    time_limit_analysis = {}
    if len(wave_data) >= 2:
        # بررسی بین موج 2 و موج 4 به عنوان دو بخش اصلاح
        if "wave2" in wave_data and "wave4" in wave_data:
            time_limit_analysis["تحلیل_محدودیت_زمانی_موج2_به_موج4"] = TimeLimitsInCorrections.check_time_ratio(
                wave_data["wave2"]["time"], wave_data["wave4"]["time"]
            )
        # بررسی بین موج 1 و موج 3
        if "wave1" in wave_data and "wave3" in wave_data:
            time_limit_analysis["تحلیل_محدودیت_زمانی_موج1_به_موج3"] = TimeLimitsInCorrections.check_time_ratio(
                wave_data["wave1"]["time"], wave_data["wave3"]["time"]
            )
    
    # ========================================================================
    # ساخت دیکشنری نتایج
    # ========================================================================
    
    results = {
        "عنوان": "فصل 13: صفات و مشخصات موج‌ها (Wave Characteristics)",
        "مرجع_کتاب": "صفحات 324 تا 329 - گلن نیلی - سبک نئوویو",
        "وضعیت": "تحلیل_کامل_و_جزئی",
        "تعداد_کل_داده": str(n),
        "قیمت_فعلی": round(float(close[-1]), 4),
        "بالاترین": round(float(np.max(high)), 4),
        "پایین‌ترین": round(float(np.min(low)), 4),
        
        # ====================================================================
        # مشخصات موج 1 (صفحه 325) - 10 مشخصه
        # ====================================================================
        "موج1_مشخصات": Wave1Characteristics.get_characteristics(),
        
        # ====================================================================
        # مشخصات موج 2 (صفحه 326) - 7 مشخصه
        # ====================================================================
        "موج2_مشخصات": Wave2Characteristics.get_characteristics(),
        
        # ====================================================================
        # مشخصات موج 3 (صفحه 327) - 14 مشخصه
        # ====================================================================
        "موج3_مشخصات": Wave3Characteristics.get_characteristics(),
        
        # ====================================================================
        # مشخصات موج 4 (صفحه 328) - 14 مشخصه
        # ====================================================================
        "موج4_مشخصات": Wave4Characteristics.get_characteristics(),
        
        # ====================================================================
        # مشخصات موج 5 (صفحه 329) - 12 مشخصه
        # ====================================================================
        "موج5_مشخصات": Wave5Characteristics.get_characteristics(),
        
        # ====================================================================
        # تحلیل واگرایی منفی (صفحه 329)
        # ====================================================================
        "تحلیل_واگرایی_منفی": divergence_analysis,
        
        # ====================================================================
        # جدول شباهت الگوها (صفحه 323)
        # ====================================================================
        "جدول_شباهت_الگوها": PatternSimilarityTable.get_all_similarities(),
        
        # ====================================================================
        # محدودیت‌های زمانی در اصلاحات (صفحه 324)
        # ====================================================================
        "محدودیت_زمانی_اصلاحات": {
            "غیرقابل_قبول_کوتاه": "بخش دوم زمان کمتر از بخش اول (فقط در X-wave مجاز است)",
            "متداول": "بخش دوم 161.8% تا 261.8% زمان بخش اول",
            "حداقل": "بخش اول و دوم برابر در زمان",
            "غیرقابل_قبول_بلند": "بخش دوم بیشتر از 261.8% بخش اول (فقط در شرایط نادر)"
        },
        
        # ====================================================================
        # تحلیل‌های کمی (در صورت وجود داده)
        # ====================================================================
    }
    
    # اضافه کردن تحلیل‌های کمی در صورت وجود داده کافی
    results.update(time_limit_analysis)
    if len(wave_data) >= 3:
        # محاسبه نسبت‌های موج 3
        if "wave1" in wave_data and "wave3" in wave_data:
            wave3_time_check = Wave3Characteristics.check_time_ratio(
                wave_data["wave1"]["time"],
                wave_data["wave3"]["time"]
            )
            wave3_price_check = Wave3Characteristics.check_price_ratio(
                wave_data["wave1"]["length"],
                wave_data["wave3"]["length"]
            )
            wave3_time_min_check = Wave3Characteristics.check_time_minimum_requirement(
                wave_data["wave1"]["time"],
                wave_data.get("wave2", {}).get("time", 0),
                wave_data["wave3"]["time"]
            )
            results["تحلیل_موج3_زمان"] = wave3_time_check
            results["تحلیل_موج3_قیمت"] = wave3_price_check
            results["تحلیل_موج3_شرط_حداقل_زمان"] = wave3_time_min_check
        
        # محاسبه شرط زمان موج 4 بیشتر از موج 3 (مشخصه 13)
        if "wave3" in wave_data and "wave4" in wave_data:
            wave4_time_check = Wave4Characteristics.check_time_greater_than_wave3(
                wave_data["wave3"]["time"],
                wave_data["wave4"]["time"]
            )
            results["تحلیل_موج4_زمان_بیشتر_از_موج3"] = wave4_time_check
    
    # ========================================================================
    # تولید تفسیر نهایی
    # ========================================================================
    
    results["تفسیر_نهایی"] = _generate_final_interpretation(results, wave_data, divergence_analysis)
    
    # ========================================================================
    # ذخیره در logger
    # ========================================================================
    
    if logger:
        logger.add_section("فصل 13: صفات و مشخصات موج‌ها", level=1)
        logger.add_result("منبع", "صفحات 324 تا 329 - گلن نیلی")
        logger.add_result("تعداد کل داده", str(n))
        logger.add_result("قیمت فعلی", results["قیمت_فعلی"])
        
        logger.add_section("مشخصات موج 1 (صفحه 325) - 10 مشخصه", level=2)
        for k, v in Wave1Characteristics.get_characteristics().items():
            logger.add_result(k, v)
        
        logger.add_section("مشخصات موج 2 (صفحه 326) - 7 مشخصه", level=2)
        for k, v in Wave2Characteristics.get_characteristics().items():
            logger.add_result(k, v)
        
        logger.add_section("مشخصات موج 3 (صفحه 327) - 14 مشخصه", level=2)
        for k, v in Wave3Characteristics.get_characteristics().items():
            logger.add_result(k, v)
        
        logger.add_section("مشخصات موج 4 (صفحه 328) - 14 مشخصه", level=2)
        for k, v in Wave4Characteristics.get_characteristics().items():
            logger.add_result(k, v)
        
        logger.add_section("مشخصات موج 5 (صفحه 329) - 12 مشخصه", level=2)
        for k, v in Wave5Characteristics.get_characteristics().items():
            logger.add_result(k, v)
        
        logger.add_section("تحلیل واگرایی", level=2)
        logger.add_result("واگرایی منفی", divergence_analysis["description"])
        
        logger.add_section("جدول شباهت الگوها (صفحه 323)", level=2)
        for pattern, sim in PatternSimilarityTable.get_all_similarities().items():
            logger.add_result(pattern, f"قیمتی: {'✓' if sim['price'] else '*'}, زمانی: {'✓' if sim['time'] else '*'}, پیچیدگی: {'✓' if sim['complexity'] else '*'}")
    
    return results


def _generate_final_interpretation(results: Dict, wave_data: Dict, divergence_analysis: Dict) -> str:
    """تولید تفسیر نهایی کامل از نتایج تحلیل"""
    lines = []
    lines.append("═" * 80)
    lines.append("فصل 13: صفات و مشخصات موج‌ها (نئوویو) - تفسیر کامل")
    lines.append("مرجع: کتاب استادی در امواج الیوت - گلن نیلی | صفحات 324-329")
    lines.append("═" * 80)
    lines.append("")
    
    lines.append("📊 آمار کلی:")
    lines.append(f"   • تعداد کل داده‌ها: {results.get('تعداد_کل_داده', 0)}")
    lines.append(f"   • قیمت فعلی: {results.get('قیمت_فعلی', 0)}")
    lines.append(f"   • بالاترین: {results.get('بالاترین', 0)}")
    lines.append(f"   • پایین‌ترین: {results.get('پایین‌ترین', 0)}")
    lines.append("")
    
    lines.append("📋 مشخصات موج 1 (صفحه 325) - 10 مشخصه:")
    for k, v in Wave1Characteristics.get_characteristics().items():
        lines.append(f"   • {v}")
    lines.append("")
    
    lines.append("📋 مشخصات موج 2 (صفحه 326) - 7 مشخصه:")
    for k, v in Wave2Characteristics.get_characteristics().items():
        lines.append(f"   • {v}")
    lines.append("")
    
    lines.append("📋 مشخصات موج 3 (صفحه 327) - 14 مشخصه:")
    for k, v in Wave3Characteristics.get_characteristics().items():
        lines.append(f"   • {v}")
    lines.append("")
    
    lines.append("📋 مشخصات موج 4 (صفحه 328) - 14 مشخصه:")
    for k, v in Wave4Characteristics.get_characteristics().items():
        lines.append(f"   • {v}")
    lines.append("")
    
    lines.append("📋 مشخصات موج 5 (صفحه 329) - 12 مشخصه:")
    for k, v in Wave5Characteristics.get_characteristics().items():
        lines.append(f"   • {v}")
    lines.append("")
    
    lines.append(f"📉 تحلیل واگرایی منفی:")
    lines.append(f"   • وضعیت: {divergence_analysis['description']}")
    if divergence_analysis.get('has_divergence'):
        lines.append(f"   • نوع واگرایی: {divergence_analysis.get('divergence_type', 'نامشخص')}")
        if divergence_analysis.get('strength'):
            lines.append(f"   • قدرت: {divergence_analysis.get('strength')}")
        if divergence_analysis.get('price_peaks'):
            for peak in divergence_analysis['price_peaks']:
                lines.append(f"   • قله قیمتی: {peak['price']} (RSI: {peak['rsi']})")
    lines.append("")
    
    lines.append("┌─────────────────────────────────────────────────────────────────┐")
    lines.append("│ جدول مقایسه الگوها از نظر شباهت (صفحه 323):                      │")
    lines.append("├─────────────────────────────────────────────────────────────────┤")
    lines.append("│ الگو       │ شباهت قیمتی │ شباهت زمانی │ شباهت پیچیدگی │")
    lines.append("├─────────────────────────────────────────────────────────────────┤")
    lines.append("│ زیگزاگ    │      *      │      *      │       *       │")
    lines.append("│ مسطح      │      ✓      │      *      │       *       │")
    lines.append("│ مثلث      │      *      │      *      │       ✓       │")
    lines.append("│ دیامتریک  │      *      │      ✓      │       ✓       │")
    lines.append("│ سیمتریک   │      ✓      │      ✓      │       ✓       │")
    lines.append("└─────────────────────────────────────────────────────────────────┘")
    lines.append("")
    lines.append("(* = عدم تشابه، ✓ = تشابه)")
    lines.append("")
    
    lines.append("⏱️ محدودیت‌های زمانی در اصلاحات (صفحه 324):")
    lines.append("   • غیرقابل قبول: بخش دوم زمان کمتر از بخش اول (فقط در X-wave ممکن است)")
    lines.append("   • متداول: بخش دوم 161.8% تا 261.8% زمان بخش اول")
    lines.append("   • حداقل: بخش اول و دوم برابر در زمان")
    lines.append("   • غیرقابل قبول: بخش دوم بیشتر از 261.8% بخش اول (فقط در شرایط نادر)")
    lines.append("")
    
    # اضافه کردن تحلیل‌های اضافی در صورت وجود
    if "تحلیل_موج3_شرط_حداقل_زمان" in results:
        lines.append("📐 تحلیل تکمیلی - شرط حداقل زمان موج 3 (صفحه 327):")
        min_time = results["تحلیل_موج3_شرط_حداقل_زمان"]
        lines.append(f"   • {min_time['description']}")
        lines.append("")
    
    if "تحلیل_موج4_زمان_بیشتر_از_موج3" in results:
        lines.append("📐 تحلیل تکمیلی - شرط زمان موج 4 (صفحه 328):")
        time_w4 = results["تحلیل_موج4_زمان_بیشتر_از_موج3"]
        lines.append(f"   • {time_w4['description']}")
        lines.append("")

    # اضافه کردن تحلیل محدودیت‌های زمانی صفحه 324
    if "تحلیل_محدودیت_زمانی_موج2_به_موج4" in results:
        lines.append("📐 اعمال محدودیت‌های زمانی صفحه 324 روی داده‌های فعلی:")
        time_limit = results["تحلیل_محدودیت_زمانی_موج2_به_موج4"]
        lines.append(f"   • {time_limit['description']}")
        lines.append("")
    
    # اضافه کردن تحلیل نسبت زمانی و قیمتی موج 3
    if "تحلیل_موج3_زمان" in results:
        lines.append("📐 تحلیل تکمیلی - نسبت زمانی موج 3 به موج 1 (صفحه 327):")
        time_check = results["تحلیل_موج3_زمان"]
        lines.append(f"   • {time_check['description']}")
        lines.append("")
    
    if "تحلیل_موج3_قیمت" in results:
        lines.append("📐 تحلیل تکمیلی - نسبت قیمتی موج 3 به موج 1 (صفحه 327):")
        price_check = results["تحلیل_موج3_قیمت"]
        lines.append(f"   • {price_check['description']}")
        lines.append("")
    
    lines.append("🎯 جمع‌بندی نهایی (صفحات 324-329):")
    lines.append("   • موج 1: آغاز روند، بدبینی، واگرایی مثبت، معمولاً کوتاه‌ترین موج")
    lines.append("   • موج 2: اصلاح، تردید در روند، نباید مثلث کامل باشد")
    lines.append("   • موج 3: قوی‌ترین و طولانی‌ترین موج، حجم بالا، تایید فاندامنتال")
    lines.append("   • موج 4: شناسایی سود، تناوب با موج 2، حداکثر 50% اصلاح موج 3")
    lines.append("   • موج 5: آخرین تلاش، واگرایی منفی، احتمال کوتاه شدن")
    lines.append("")
    
    if divergence_analysis.get('has_divergence'):
        lines.append("   ⚠️ هشدار نئوویو: واگرایی منفی تشخیص داده شده است. این نشانه ضعف روند")
        lines.append("      و احتمال تغییر جهت یا اصلاح قریب‌الوقوع می‌باشد.")
    else:
        lines.append("   ℹ️ نکته نئوویو: واگرایی منفی تشخیص داده نشد. روند فعلی از پویایی لازم")
        lines.append("      برخوردار است.")
    
    lines.append("")
    lines.append("═" * 80)
    lines.append("پایان تفسیر فصل 13")
    lines.append("═" * 80)
    
    return "\n".join(lines)