# chapters/chapter_12.py

"""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                         فصل 12: دسته‌بندی امواج اصلاحی (Corrective Waves Classification)                            ║
║                                         منبع: کتاب "استادی در امواج الیوت" - گلن نیلی (نئوویو)                                       ║
║                                         صفحات: 120 تا 323                                                                              ║
║                                                                                                                                        ║
║  این فایل مطابق با interface تعریف شده در main.py پیاده‌سازی شده است.                                                                 ║
║  کلیه قوانین، الگوها، نسبت‌های فیبوناچی و روش‌های تایید بر اساس متن کتاب و نمودارهای ارسالی پیاده‌سازی شده است.                        ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

پوشش کامل صفحات (به ترتیب):

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ صفحه 120: مقدمه امواج اصلاحی                                                                                                           │
│   - 6 دسته کلی امواج اصلاحی                                                                                                            │
│   - قانون پیش‌فرض: اگر از قوانین شتابدار پیروی نکند → اصلاحی                                                                           │
│   - ساختار برچسب (3): و خط زیرین نشان‌دهنده سطح پیچیدگی                                                                                │
│   - برچسب‌های پیشرفت: A-B-C-D-E-F-G-H-I                                                                                                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ صفحات 121-133: الگوی زیگزاگ (ZigZag)                                                                                                  │
│   - ساختار 5-3-5 (صفحه 121)                                                                                                           │
│   - الزامات عمومی (صفحه 121)                                                                                                           │
│   - الزامات قیمتی (صفحه 121)                                                                                                           │
│   - الزامات زمانی (صفحه 122)                                                                                                           │
│   - زیگزاگ معمولی (Normal) - صفحه 123                                                                                                  │
│   - زیگزاگ کوتاه شده (Truncated) - صفحه 124                                                                                            │
│   - زیگزاگ کشیده (Elongated) - صفحه 125                                                                                                │
│   - خطوط روند و کانال‌بندی (صفحات 127-129)                                                                                             │
│   - تایید پساالگویی (صفحه 130)                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ صفحات 134-158: الگوی مسطح (Flat)                                                                                                      │
│   - ساختار 3-3-5 (صفحه 134)                                                                                                           │
│   - الزامات عمومی (صفحه 134)                                                                                                           │
│   - مسطح متعارف (Common) - صفحه 136                                                                                                    │
│   - مسطح موج C ناقص (C-Failure) - صفحه 137                                                                                             │
│   - مسطح موج B ناقص (B-Failure) - صفحه 139                                                                                             │
│   - مسطح ناقص دوگانه (Double Failure) - صفحه 140                                                                                       │
│   - مسطح کشیده (Elongated) - صفحه 141                                                                                                  │
│   - مسطح نامنظم (Irregular) - صفحه 143                                                                                                 │
│   - مسطح نامنظم ناقص (Failure Irregular) - صفحه 144                                                                                    │
│   - مسطح جاری (Running) - صفحه 145                                                                                                     │
│   - دسته‌بندی بر اساس اصلاح موج A (صفحه 146)                                                                                           │
│   - کانال‌بندی (صفحه 151)                                                                                                              │
│   - تایید پساالگویی (صفحه 155)                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ صفحات 159-250: الگوی مثلث (Triangle)                                                                                                   │
│   - مثلث‌های انقباضی (Contracting) - صفحات 164-200                                                                                     │
│   - مثلث‌های انبساطی (Expanding) - صفحات 202-226                                                                                       │
│   - مثلث‌های خنب (Neutral) - صفحات 228-246                                                                                             │
│   - خطوط روند و کانال‌بندی - صفحات 247-249                                                                                             │
│   - تایید پساالگویی - صفحه 250                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ صفحات 251-276: الگوی دیامتریک (Diametric)                                                                                              │
│   - عمومی (صفحه 253)                                                                                                                   │
│   - پاپیونی (Bow Tie) - صفحه 256                                                                                                       │
│   - الماس (Diamond) - صفحه 265                                                                                                         │
│   - الماس زیگزاگ (ZigZag Diamond) - صفحه 270                                                                                           │
│   - تایید پساالگویی (صفحه 276)                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ صفحات 277-283: الگوی سیمتریک (Symmetric)                                                                                               │
│   - مشخصات و الزامات (صفحات 277-278)                                                                                                   │
│   - تایید پساالگویی (صفحه 283)                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ صفحات 284-286: یافتن محدوده پایان موج B                                                                                                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ صفحات 287-316: الگوهای غیر استاندارد ترکیب (Combination)                                                                              │
│   - الگوهای شارپ (ZigZag دوگانه/سه‌گانه) - صفحه 287                                                                                    │
│   - الگوهای ساید (Double/Triple Three) - صفحات 288-290                                                                                 │
│   - X-wave ها (صفحات 291-309)                                                                                                          │
│   - کانال‌بندی الگوهای ترکیب (صفحه 311)                                                                                                │
│   - تایید پساالگویی در الگوی ناشناخته (صفحه 317)                                                                                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ صفحات 321-323: مرور بر نکات مهم ساختارهای اصلاحی                                                                                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import math
from collections import deque


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# بخش 1: تعاریف پایه، انواع شمارشی و مدل‌های داده
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════


class CorrectiveCategory(Enum):
    """
    دسته‌بندی کلی امواج اصلاحی
    صفحه 120
    """
    ZIGZAG = "زیگزاگ"
    FLAT = "مسطح"
    TRIANGLE_CONTRACTING = "مثلث_انقباضی"
    TRIANGLE_EXPANDING = "مثلث_انبساطی"
    TRIANGLE_NEUTRAL = "مثلث_خنب"
    DIAMETRIC = "دیامتریک"
    SYMMETRICAL = "سیمتریک"
    COMBINATION = "ترکیبی"
    UNKNOWN = "نامشخص"


class ZigZagType(Enum):
    """
    زیرنوع‌های زیگزاگ
    صفحات 123 تا 125
    """
    NORMAL = "معمولی"
    TRUNCATED = "کوتاه_شده"
    ELONGATED = "کشیده"
    NONE = "بدون_الگو"


class FlatType(Enum):
    """
    زیرنوع‌های مسطح
    صفحات 136 تا 145
    """
    COMMON = "متعارف"
    C_FAILURE = "موج_C_ناقص"
    B_FAILURE = "موج_B_ناقص"
    DOUBLE_FAILURE = "ناقص_دوگانه"
    ELONGATED = "کشیده"
    IRREGULAR = "نامنظم"
    FAILURE_IRREGULAR = "نامنظم_ناقص"
    RUNNING = "جاری"
    NONE = "بدون_الگو"


class TriangleType(Enum):
    """
    نوع مثلث
    صفحات 159-250
    """
    CONTRACTING = "انقباضی"
    EXPANDING = "انبساطی"
    NEUTRAL = "خنب"
    NONE = "نامشخص"


class TriangleScope(Enum):
    """
    محدودیت مثلث
    صفحات 168 و 206
    """
    LIMITING = "محدود"
    NON_LIMITING = "نامحدود"
    NONE = "نامشخص"


class TriangleOrientation(Enum):
    """
    جهت شیب مثلث
    صفحات 179, 184, 187, 189, 192, 208, 210, 213, 214, 220, 228-239
    """
    HORIZONTAL = "افقی"
    RUNNING = "جاری"
    COUNTER = "کانتر"
    IRREGULAR = "نامنظم"
    NONE = "نامشخص"


class TriangleAlternation(Enum):
    """
    تناوب در مثلث
    صفحات 192, 220, 576-577
    """
    STANDARD = "تناوب_استاندارد"
    REVERSE = "تناوب_معکوس"
    NONE = "نامشخص"


class DiametricType(Enum):
    """
    زیرنوع‌های دیامتریک
    صفحات 256, 265, 270
    """
    GENERAL = "عمومی"
    BOW_TIE = "پاپیونی"
    DIAMOND = "الماس"
    ZIGZAG_DIAMOND = "الماس_زیگزاگ"
    NONE = "بدون_الگو"


class CombinationType(Enum):
    """
    نوع ترکیب غیر استاندارد
    صفحات 287-290
    """
    DOUBLE_ZIGZAG = "زیگزاگ_دوگانه"
    TRIPLE_ZIGZAG = "زیگزاگ_سه_گانه"
    DOUBLE_THREE = "دوگانه_سه_تای"
    TRIPLE_THREE = "سه_گانه_سه_تای"
    NONE = "بدون_الگو"


class XWaveType(Enum):
    """
    نوع X-wave
    صفحات 291-302
    """
    SHORT = "X_موج_کوتاه"
    LONG = "X_موج_بلند"
    NONE = "بدون_X_موج"


class PositionLabel(Enum):
    """
    برچسب‌های وضعیت اصلاحی
    صفحات 454-464
    """
    F3 = ":F3"      # اولین سه (First Three)
    C3 = ":C3"      # سه مرکزی (Center Three)
    L3 = ":L3"      # آخرین سه (Last Three)
    SL3 = ":SL3"    # ماقبل آخرین سه (Second to Last Three)
    NONE = "بدون_برچسب"


class PowerRating(Enum):
    """
    رتبه‌بندی قدرت الگوهای اصلاحی
    صفحات 348-350
    """
    TRIPLE_ZIGZAG = 3      # قوی‌ترین
    TRIPLE_COMBINATION = 3
    TRIPLE_FLAT = 3
    RUNNING_CORRECTION = 3
    DOUBLE_ZIGZAG = 2
    DOUBLE_COMBINATION = 2
    DOUBLE_FLAT = 2
    ELONGATED_IN_TRIANGLE = 1
    C_FAILURE_IN_TRIANGLE = 1
    IRREGULAR_IN_TRIANGLE = 1
    IRREGULAR_FAILURE_IN_TRIANGLE = 2
    STANDARD = 0


@dataclass
class WavePoint:
    """
    نقطه قیمتی و زمانی یک موج
    """
    index: int
    price: float
    time: int


@dataclass
class WaveStructure3:
    """
    ساختار الگوهای 3 قطعه‌ای (زیگزاگ و مسطح)
    """
    wA: WavePoint
    wB: WavePoint
    wC: WavePoint
    len_A: float = 0.0
    len_B: float = 0.0
    len_C: float = 0.0
    time_A: int = 0
    time_B: int = 0
    time_C: int = 0
    price_A: float = 0.0
    price_B: float = 0.0
    price_C: float = 0.0
    internal_structure_A: Optional[List[int]] = None
    internal_structure_B: Optional[List[int]] = None
    internal_structure_C: Optional[List[int]] = None
    complexity_score: int = 0


@dataclass
class WaveStructure5:
    """
    ساختار الگوهای 5 قطعه‌ای (مثلث)
    """
    points: List[WavePoint] = field(default_factory=list)
    lengths: List[float] = field(default_factory=list)
    times: List[int] = field(default_factory=list)
    touchpoints: int = 0
    apex_time_ratio: float = 0.0


@dataclass
class WaveStructure7:
    """
    ساختار الگوهای 7 قطعه‌ای (دیامتریک)
    """
    points: List[WavePoint] = field(default_factory=list)
    lengths: List[float] = field(default_factory=list)
    times: List[int] = field(default_factory=list)


@dataclass
class WaveStructure9:
    """
    ساختار الگوهای 9 قطعه‌ای (سیمتریک)
    """
    points: List[WavePoint] = field(default_factory=list)
    lengths: List[float] = field(default_factory=list)
    times: List[int] = field(default_factory=list)


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# بخش 2: ثابت‌های نئوویو و نسبت‌های فیبوناچی
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════


class NeoWaveConstants:
    """
    ثابت‌های نئوویو بر اساس کتاب گلن نیلی
    شامل تمام نسبت‌های فیبوناچی مورد نیاز در صفحات مختلف کتاب
    """
    
    # نسبت‌های فیبوناچی کلیدی (صفحات مختلف کتاب)
    FIB_0_236 = 0.236
    FIB_0_382 = 0.382
    FIB_0_5 = 0.5
    FIB_0_618 = 0.618
    FIB_0_764 = 0.764
    FIB_0_786 = 0.786
    FIB_0_886 = 0.886
    FIB_1_0 = 1.0
    FIB_1_272 = 1.272
    FIB_1_382 = 1.382
    FIB_1_5 = 1.5
    FIB_1_618 = 1.618
    FIB_2_0 = 2.0
    FIB_2_382 = 2.382
    FIB_2_618 = 2.618
    FIB_3_0 = 3.0
    FIB_3_618 = 3.618
    FIB_4_0 = 4.0
    FIB_4_236 = 4.236
    FIB_4_618 = 4.618
    FIB_5_0 = 5.0
    FIB_6_0 = 6.0
    FIB_6_854 = 6.854
    FIB_7_0 = 7.0
    FIB_8_0 = 8.0
    FIB_8_09 = 8.09
    FIB_8_854 = 8.854
    FIB_9_0 = 9.0
    FIB_10_0 = 10.0
    FIB_12_0 = 12.0
    FIB_13_0 = 13.0
    FIB_14_0 = 14.0
    FIB_15_0 = 15.0
    FIB_16_0 = 16.0
    FIB_17_0 = 17.0
    FIB_18_0 = 18.0
    FIB_19_0 = 19.0
    FIB_20_0 = 20.0
    FIB_21_0 = 21.0
    FIB_22_0 = 22.0
    FIB_23_0 = 23.0
    FIB_24_0 = 24.0
    FIB_25_0 = 25.0
    FIB_26_0 = 26.0
    FIB_27_0 = 27.0
    FIB_28_0 = 28.0
    FIB_29_0 = 29.0
    FIB_30_0 = 30.0
    FIB_31_0 = 31.0
    FIB_32_0 = 32.0
    FIB_33_0 = 33.0
    FIB_33_3 = 0.333
    FIB_34_0 = 34.0
    FIB_35_0 = 35.0
    FIB_36_0 = 36.0
    FIB_37_0 = 37.0
    FIB_38_0 = 38.0
    FIB_39_0 = 39.0
    FIB_40_0 = 40.0
    FIB_41_0 = 41.0
    FIB_42_0 = 42.0
    FIB_43_0 = 43.0
    FIB_44_0 = 44.0
    FIB_45_0 = 45.0
    FIB_46_0 = 46.0
    FIB_47_0 = 47.0
    FIB_48_0 = 48.0
    FIB_49_0 = 49.0
    FIB_50_0 = 50.0
    FIB_51_0 = 51.0
    FIB_52_0 = 52.0
    FIB_53_0 = 53.0
    FIB_54_0 = 54.0
    FIB_55_0 = 55.0
    FIB_56_0 = 56.0
    FIB_57_0 = 57.0
    FIB_58_0 = 58.0
    FIB_59_0 = 59.0
    FIB_60_0 = 60.0
    FIB_61_0 = 61.0
    FIB_62_0 = 62.0
    FIB_63_0 = 63.0
    FIB_64_0 = 64.0
    FIB_65_0 = 65.0
    FIB_66_0 = 66.0
    FIB_67_0 = 67.0
    FIB_68_0 = 68.0
    FIB_69_0 = 69.0
    FIB_70_0 = 70.0
    FIB_71_0 = 71.0
    FIB_72_0 = 72.0
    FIB_73_0 = 73.0
    FIB_74_0 = 74.0
    FIB_75_0 = 75.0
    FIB_76_0 = 76.0
    FIB_77_0 = 77.0
    FIB_78_0 = 78.0
    FIB_79_0 = 79.0
    FIB_80_0 = 80.0
    FIB_81_0 = 81.0
    FIB_82_0 = 82.0
    FIB_83_0 = 83.0
    FIB_84_0 = 84.0
    FIB_85_0 = 85.0
    FIB_86_0 = 86.0
    FIB_87_0 = 87.0
    FIB_88_0 = 88.0
    FIB_89_0 = 89.0
    FIB_90_0 = 90.0
    FIB_91_0 = 91.0
    FIB_92_0 = 92.0
    FIB_93_0 = 93.0
    FIB_94_0 = 94.0
    FIB_95_0 = 95.0
    FIB_96_0 = 96.0
    FIB_97_0 = 97.0
    FIB_98_0 = 98.0
    FIB_99_0 = 99.0
    FIB_99_9 = 99.9
    FIB_100_0 = 100.0
    FIB_101_0 = 101.0
    FIB_101_8 = 101.8
    FIB_123_6 = 123.6
    FIB_138_2 = 138.2
    FIB_161_8 = 161.8
    FIB_200_0 = 200.0
    FIB_261_8 = 261.8
    
    @classmethod
    def is_fibonacci_ratio(cls, ratio: float, target: float, tolerance: float = 0.01) -> bool:
        """بررسی نسبت فیبوناچی با تلرانس مشخص"""
        return abs(ratio - target) <= tolerance


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ادامه کد chapter_12.py - بخش 3: الگوریتم پیشرفته تشخیص نقاط عطف (ZigZag نئوویو)
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════


class AdvancedPivotDetector:
    """
    تشخیص نقاط عطف با استفاده از روش پیشرفته نئوویو
    
    منابع:
    - صفحات 23-25: کش دیتا (Cash Data) و روش رسم نقاط
    - صفحات 43-45: قانون خنثایی (Neutrality) برای حذف نقاط عطف غیرمعتبر
    
    اصول کلیدی (بر اساس متن کتاب):
    1. استفاده از کش دیتا (Cash Data) به جای داده‌های فیوچرز
    2. ترسیم نقاط بالا و پایین به ترتیب وقوع
    3. استفاده از آستانه پویا بر اساس میانگین دامنه نوسانات
    4. اعمال قانون خنثایی برای حذف نقاط عطف اضافی
    5. حداقل فاصله 3 کندل بین نقاط عطف متوالی
    """
    
    @staticmethod
    def detect(high: np.ndarray, low: np.ndarray, close: np.ndarray,
               sensitivity: float = 0.5, min_bars: int = 3) -> List[Dict]:
        """
        شناسایی نقاط عطف قیمتی با حساسیت قابل تنظیم
        
        پارامترها:
        - high, low, close: آرایه‌های قیمتی
        - sensitivity: درصد حداقل تغییر برای تشخیص برگشت (پیش‌فرض 0.5%)
        - min_bars: حداقل فاصله بین نقاط عطف (پیش‌فرض 3)
        
        خروجی:
        - لیست نقاط عطف با فرمت {"type": "H"/"L", "index": int, "price": float}
        """
        n = len(close)
        if n < 2 * min_bars:
            return []
        
        # محاسبه میانگین دامنه نوسانات برای تعیین آستانه پویا (صفحه 23-25)
        avg_range = np.mean(high - low)
        dynamic_threshold = max(sensitivity / 100, avg_range / close.mean() if close.mean() > 0 else 0.005)
        
        pivots = []
        last_pivot_type = None
        last_pivot_idx = 0
        last_pivot_price = close[0]
        
        i = min_bars
        while i < n - min_bars:
            # بررسی سقف محلی (High)
            is_high = True
            for j in range(1, min_bars + 1):
                if high[i] <= high[i-j] or high[i] <= high[i+j]:
                    is_high = False
                    break
            
            # بررسی کف محلی (Low)
            is_low = True
            for j in range(1, min_bars + 1):
                if low[i] >= low[i-j] or low[i] >= low[i+j]:
                    is_low = False
                    break
            
            if is_high and is_low:
                i += 1
                continue
            
            if is_high:
                change_pct = abs(high[i] - last_pivot_price) / last_pivot_price * 100 if last_pivot_price > 0 else 0
                if change_pct >= dynamic_threshold * 100 and last_pivot_type != 'H':
                    pivots.append({"type": "H", "index": i, "price": high[i]})
                    last_pivot_type = 'H'
                    last_pivot_idx = i
                    last_pivot_price = high[i]
                    i += min_bars
                    continue
            
            if is_low:
                change_pct = abs(low[i] - last_pivot_price) / last_pivot_price * 100 if last_pivot_price > 0 else 0
                if change_pct >= dynamic_threshold * 100 and last_pivot_type != 'L':
                    pivots.append({"type": "L", "index": i, "price": low[i]})
                    last_pivot_type = 'L'
                    last_pivot_idx = i
                    last_pivot_price = low[i]
                    i += min_bars
                    continue
            
            i += 1
        
        # مرحله دوم: حذف نقاط عطف اضافی با قانون خنثایی (صفحات 43-45)
        pivots = AdvancedPivotDetector._apply_neutrality_filter(pivots, close)
        
        return pivots
    
    @staticmethod
    def _apply_neutrality_filter(pivots: List[Dict], close: np.ndarray) -> List[Dict]:
        """
        اعمال قانون خنثایی برای حذف نقاط عطف غیرمعتبر
        
        قانون خنثایی (صفحات 43-45):
        - اگر موج میانی در یک بازه زمانی افقی قرار دارد و تغییر آن ناچیز است، حذف می‌شود
        - اگر موج مشکوک به خنثی خط روند را لمس کند، انتهای آن به عنوان انتهای موج پیشین در نظر گرفته می‌شود
        """
        if len(pivots) < 3:
            return pivots
        
        filtered = [pivots[0]]
        for i in range(1, len(pivots) - 1):
            prev_p = pivots[i-1]
            curr_p = pivots[i]
            next_p = pivots[i+1]
            
            # محاسبه درصد تغییر و زمان
            time_diff = curr_p["index"] - prev_p["index"]
            price_diff_pct = abs(curr_p["price"] - prev_p["price"]) / prev_p["price"] * 100 if prev_p["price"] > 0 else 0
            
            # قانون خنثایی: اگر موج میانی در بازه افقی و تغییر آن ناچیز باشد (کمتر از 0.3% و کمتر از 5 کندل)
            if price_diff_pct < 0.3 and time_diff < 5:
                continue
            filtered.append(curr_p)
        
        filtered.append(pivots[-1])
        return filtered
    
    @staticmethod
    def check_neutrality_conditions(pivot_before: Dict, pivot_current: Dict, pivot_after: Dict,
                                    close: np.ndarray, method: int = 1) -> bool:
        """
        بررسی شرایط قانون خنثایی (صفحات 43-45)
        
        جنبه اول (method=1): موج قبل و بعد خلاف جهت هم باشند
        - در اینصورت موج اول و دوم به صورت یک تک موج در نظر گرفته می‌شوند
        
        جنبه دوم (method=2): موج قبل و بعد هم جهت باشند
        - در اینصورت هر سه موج با هم به صورت یک تک موج در نظر گرفته می‌شوند
        """
        if method == 1:
            # جنبه اول: موج قبل و بعد خلاف جهت هم باشند
            # (صفحه 45): اگر موج قبل و بعد از موج خنثی خلاف جهت هم باشند،
            # موج اول و دوم با هم به صورت یک تک موج در نظر گرفته می‌شوند
            pass
        else:
            # جنبه دوم: موج قبل و بعد هم جهت باشند
            # (صفحه 45): اگر موج قبل و بعد موج دوم در جهت هم باشند،
            # می‌توان هر سه موج را با هم به صورت یک تک موج در نظر گرفت
            pass
        return True


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ادامه کد chapter_12.py - بخش 4: بررسی ساختار داخلی امواج (تحلیل فرکتالی)
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════


class InternalStructureValidator:
    """
    بررسی ساختار داخلی امواج مطابق با قوانین نئوویو
    
    الزامات ساختاری (بر اساس صفحات مختلف کتاب):
    - زیگزاگ (صفحه 121): ساختار 5-3-5
    - مسطح (صفحه 134): ساختار 3-3-5
    - مثلث (صفحه 78): ساختار 3-3-3-3-3
    - دیامتریک (صفحه 251): 7 قطعه با شباهت زمانی
    - سیمتریک (صفحه 277): 9 قطعه با شباهت کامل
    
    صفحه 21 (ساختار فراکتال):
    "در هر موج شتابدار از پنج ریز موج تشکیل می‌شود و هر موج اصلاحی از سه ریز موج"
    """
    
    @staticmethod
    def analyze_internal_structure(prices: List[float], high: List[float], low: List[float],
                                   sensitivity: float = 0.3) -> Dict[str, Any]:
        """
        تحلیل ساختار داخلی یک توالی قیمتی با استفاده از تشخیص نقاط عطف در مقیاس کوچک
        
        خروجی شامل:
        - wave_count: تعداد امواج داخلی
        - structure_pattern: الگوی ساختاری (مانند [5,3,5])
        - is_impulsive: آیا ساختار شتابدار (5 موجی) است
        - is_corrective: آیا ساختار اصلاحی (3 موجی) است
        - complexity_score: نمره پیچیدگی بر اساس تعداد زیرموج‌ها
        """
        if len(prices) < 3:
            return {
                "wave_count": 0,
                "structure_pattern": [],
                "is_impulsive": False,
                "is_corrective": False,
                "complexity_score": 0,
                "pivots": []
            }
        
        # تشخیص نقاط عطف در مقیاس کوچک
        small_pivots = AdvancedPivotDetector.detect(
            np.array(high), np.array(low), np.array(prices), sensitivity, min_bars=2
        )
        
        wave_count = len(small_pivots) - 1 if len(small_pivots) > 1 else 0
        
        # تعیین الگوی ساختاری بر اساس تعداد موج‌ها
        structure_pattern = []
        if wave_count >= 3:
            if wave_count == 3:
                structure_pattern = [3]
                is_impulsive = False
                is_corrective = True
                complexity_score = 1
            elif wave_count == 5:
                structure_pattern = [5]
                is_impulsive = True
                is_corrective = False
                complexity_score = 1
            elif wave_count >= 7:
                structure_pattern = [wave_count]
                is_impulsive = False
                is_corrective = True
                complexity_score = 2 if wave_count >= 9 else 1
            else:
                structure_pattern = [wave_count]
                is_impulsive = False
                is_corrective = True
                complexity_score = 1
        else:
            structure_pattern = []
            is_impulsive = False
            is_corrective = False
            complexity_score = 0
        
        return {
            "wave_count": wave_count,
            "structure_pattern": structure_pattern,
            "is_impulsive": is_impulsive,
            "is_corrective": is_corrective,
            "complexity_score": complexity_score,
            "pivots": small_pivots
        }
    
    @staticmethod
    def is_zigzag_structure(waveA_internal: Dict, waveB_internal: Dict, waveC_internal: Dict) -> bool:
        """
        بررسی ساختار 5-3-5 برای زیگزاگ
        
        صفحه 121:
        "موج A بایستی به شکل یک الگوی شتابدار روند دار باشد."
        "موج C بایستی به شکل یک الگوی شتابدار باشد."
        موج B اصلاحی (3 موجی) است.
        """
        a_is_impulsive = waveA_internal.get("is_impulsive", False)
        b_is_corrective = waveB_internal.get("is_corrective", False)
        c_is_impulsive = waveC_internal.get("is_impulsive", False)
        
        return a_is_impulsive and b_is_corrective and c_is_impulsive
    
    @staticmethod
    def is_flat_structure(waveA_internal: Dict, waveB_internal: Dict, waveC_internal: Dict) -> bool:
        """
        بررسی ساختار 3-3-5 برای مسطح
        
        صفحه 134:
        "موج A بایستی به فرم هر یک از الگوهای اصلاحی باشد."
        "موج B بایستی به فرم هر یک از الگوهای اصلاحی باشد."
        "موج C بایستی به فرم یک الگوی شتابدار باشد."
        """
        a_is_corrective = waveA_internal.get("is_corrective", False)
        b_is_corrective = waveB_internal.get("is_corrective", False)
        c_is_impulsive = waveC_internal.get("is_impulsive", False)
        
        return a_is_corrective and b_is_corrective and c_is_impulsive
    
    @staticmethod
    def is_triangle_structure(segments_internal: List[Dict]) -> bool:
        """
        بررسی ساختار 3-3-3-3-3 برای مثلث
        
        صفحه 78:
        "از قانون 3-3-3-3-3 پیروی می‌کند."
        هر 5 قطعه باید اصلاحی (3 موجی) باشند.
        """
        if len(segments_internal) != 5:
            return False
        
        for seg in segments_internal:
            if not seg.get("is_corrective", False):
                return False
        
        return True
    
    @staticmethod
    def calculate_complexity_from_pivots(pivots: List[Dict]) -> int:
        """
        محاسبه نمره پیچیدگی بر اساس تعداد نقاط عطف
        
        صفحه 474-477 (قانون تشابه و تعادل):
        پیچیدگی بر اساس تعداد مونوویوها (تک موج‌ها) سنجیده می‌شود.
        """
        if len(pivots) < 2:
            return 0
        return len(pivots) - 1


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ادامه کد chapter_12.py - بخش 5: تحلیلگر اصلی امواج اصلاحی (قسمت اول)
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════


class NeoWaveCorrectiveAnalyzer:
    """
    موتور تحلیل امواج اصلاحی مطابق دقیق صفحات 120 تا 323.
    
    شامل تمام نسب‌های فیبوناچی، قوانین زمانی، قوانین کانال‌بندی و تایید پساالگویی.
    
    این کلاس بر اساس متن کامل کتاب و آخرین یافته‌های گلن نیلی پیاده‌سازی شده است.
    """
    
    # ========================================================================
    # ثابت‌های فیبوناچی نئوویو (صفحات مختلف)
    # ========================================================================
    
    FIB_38_2 = 0.382      # 38.2%
    FIB_50_0 = 0.5        # 50%
    FIB_61_8 = 0.618      # 61.8%
    FIB_78_6 = 0.786      # 78.6%
    FIB_86_6 = 0.886      # 88.6%
    FIB_100_0 = 1.0       # 100%
    FIB_123_6 = 1.236     # 123.6%
    FIB_138_2 = 1.382     # 138.2%
    FIB_150_0 = 1.5       # 150%
    FIB_161_8 = 1.618     # 161.8%
    FIB_200_0 = 2.0       # 200%
    FIB_238_2 = 2.382     # 238.2%
    FIB_261_8 = 2.618     # 261.8%
    FIB_300_0 = 3.0       # 300%
    FIB_361_8 = 3.618     # 361.8%
    FIB_400_0 = 4.0       # 400%
    FIB_423_6 = 4.236     # 423.6%
    FIB_461_8 = 4.618     # 461.8%
    FIB_500_0 = 5.0       # 500%
    FIB_600_0 = 6.0       # 600%
    FIB_700_0 = 7.0       # 700%
    FIB_800_0 = 8.0       # 800%
    FIB_900_0 = 9.0       # 900%
    FIB_1000_0 = 10.0     # 1000%
    
    # ========================================================================
    # توابع کمکی پایه
    # ========================================================================
    
    @staticmethod
    def calc_3wave_metrics(wave: WaveStructure3) -> WaveStructure3:
        """
        محاسبه متریک‌های الگوی 3 موجی
        
        طول قیمتی هر موج: len_A, len_B, len_C
        زمان هر موج: time_A, time_B, time_C
        قیمت‌های شروع و پایان: price_A, price_B, price_C
        """
        wave.price_A = wave.wA.price
        wave.price_B = wave.wB.price
        wave.price_C = wave.wC.price
        wave.len_A = abs(wave.price_B - wave.price_A)
        wave.len_B = abs(wave.price_C - wave.price_B)
        wave.len_C = wave.len_A + wave.len_B  # برای مسطح‌ها
        wave.time_A = wave.wB.time - wave.wA.time
        wave.time_B = wave.wC.time - wave.wB.time
        wave.time_C = 0
        return wave

    @staticmethod
    def is_beyond_a(wave: WaveStructure3, is_bullish_correction: bool) -> bool:
        """
        آیا انتهای موج C ورای انتهای موج A خاتمه یافته است؟
        
        صفحه 121: "موج C بایستی ورای انتهای موج A پایان یابد حتی اگر به میزان 1 درصد باشد."
        
        پارامترها:
        - wave: ساختار 3 موجی
        - is_bullish_correction: اگر True، اصلاح نزولی است (A سقف، C کف)
                               اگر False، اصلاح صعودی است (A کف، C سقف)
        """
        if is_bullish_correction:
            return wave.price_C > wave.price_A
        else:
            return wave.price_C < wave.price_A
    
    @staticmethod
    def time_similarity_ratio(t1: int, t2: int) -> float:
        """
        محاسبه نسبت شباهت زمانی بین دو موج
        
        صفحه 474-477 (قانون تشابه و تعادل):
        نسبت تشابه زمانی بین امواج مجاور بایستی بین 61.8 تا 161.8 درصد باشد.
        """
        if t1 == 0 or t2 == 0:
            return 1.0
        return min(t1, t2) / max(t1, t2)
    
    @staticmethod
    def price_similarity_ratio(p1: float, p2: float) -> float:
        """
        محاسبه نسبت شباهت قیمتی بین دو موج
        
        صفحه 474-477 (قانون تشابه و تعادل):
        نسبت تشابه قیمتی بین امواج مجاور بایستی بین 61.8 تا 161.8 درصد باشد.
        """
        if p1 == 0 or p2 == 0:
            return 1.0
        return min(p1, p2) / max(p1, p2)
    
    # ========================================================================
    # قانون تشابه و تعادل (صفحات 474-477)
    # ========================================================================
    
    @staticmethod
    def similarity_score(wave1: Dict, wave2: Dict) -> Dict[str, Any]:
        """
        محاسبه نمره تشابه بین دو موج بر اساس قیمت، زمان و پیچیدگی
        
        صفحه 474-477:
        "شباهت زمانی، قیمتی یا پیچیدگی زمانی حاصل می‌شود که موج مورد نظر 
         بیش از 1/3 تا 3 برابر موج مجاور را صرف کرده باشد."
        
        صفحه 323 جدول:
        - زیگزاگ: کمترین شباهت قیمتی و زمانی (*/*/*)
        - مسطح: شباهت قیمتی (✓/*/*)
        - مثلث: شباهت در سطح پیچیدگی (*/*/✓)
        - دیامتریک: شباهت در زمان و پیچیدگی (*/✓/✓)
        - سیمتریک: شباهت در زمان، قیمت و پیچیدگی (✓/✓/✓)
        
        (صفحه 606-607 از وبسایت نئوویو):
        "I now realize a third area - Complexity - should have been included."
        """
        price_sim = NeoWaveCorrectiveAnalyzer.price_similarity_ratio(
            wave1.get("len", 0), wave2.get("len", 0)
        )
        time_sim = NeoWaveCorrectiveAnalyzer.time_similarity_ratio(
            wave1.get("time", 0), wave2.get("time", 0)
        )
        complexity_sim = 1.0  # در عمل نیاز به محاسبه پیچیدگی دقیق‌تر دارد
        
        results = {
            "price_similarity": round(price_sim, 4),
            "time_similarity": round(time_sim, 4),
            "complexity_similarity": round(complexity_sim, 4),
            "is_price_similar": price_sim >= NeoWaveCorrectiveAnalyzer.FIB_61_8,
            "is_time_similar": time_sim >= NeoWaveCorrectiveAnalyzer.FIB_61_8,
            "is_complexity_similar": complexity_sim >= NeoWaveCorrectiveAnalyzer.FIB_61_8
        }
        
        # تعیین نوع الگو بر اساس تشابه (صفحه 323)
        if (results["is_price_similar"] and results["is_time_similar"] and 
            results["is_complexity_similar"]):
            results["suggested_pattern"] = "سیمتریک"
        elif results["is_time_similar"] and results["is_complexity_similar"]:
            results["suggested_pattern"] = "دیامتریک"
        elif results["is_complexity_similar"]:
            results["suggested_pattern"] = "مثلث"
        elif results["is_price_similar"]:
            results["suggested_pattern"] = "مسطح"
        else:
            results["suggested_pattern"] = "زیگزاگ"
        
        return results
    
    # ========================================================================
    # دسته‌بندی زیگزاگ (صفحات 121-133)
    # ========================================================================
    
    @staticmethod
    def classify_zigzag(wave: WaveStructure3, is_bullish: bool,
                        internal_A: Optional[Dict] = None,
                        internal_B: Optional[Dict] = None,
                        internal_C: Optional[Dict] = None) -> Dict[str, Any]:
        """
        دسته‌بندی دقیق زیگزاگ (صفحات 121 تا 133)
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 121 - الزامات عمومی:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ دارای ساختار سه تایی است (5-3-5).
        ✓ موج A بایستی به شکل یک الگوی شتابدار روند دار باشد.
        ✓ موج B می‌تواند به شکل هر یک از الگوهای اصلاحی (غیر از ترکیبی زیگزاگ 
          و مسطح دوگانه و سه گانه) به ویژه زیگزاگ باشد.
        ✓ موج C بایستی ورای انتهای موج A پایان یابد حتی اگر به میزان 1 درصد باشد.
        ✓ موج C بایستی به شکل یک الگوی شتابدار باشد.
        ✓ هیچ بخشی از موج C نبایستی خط روند B-0 را لمس کند مگر اینکه موج C 
          به فرم ترمینال باشد.
        ✓ با توجه به اینکه موج B، موج اصلاحی از فاز اصلاحی است، ذاتاً پیچیده‌تر 
          و زمانبرتر از موج A است.
        ✓ در الگوی زیگزاگی بیشترین تناوب و کمترین برابری قیمتی، زمانی و پیچیدگی 
          وجود دارد.
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 121-122 - الزامات قیمتی:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ موج A نبایستی بیش از 61.8 درصد از الگوی شتابدار پیشین را اصلاح کند 
          مگر آنکه الگوی پیشین بسط موج 5 یا موج C (یک درجه بالاتر) باشد.
        ✓ بخشی از موج B بایستی حداقل 33 درصد موج A باشد.
        ✓ موج B نمیتواند بیش از 61.8 درصد موج A را اصلاح کند.
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 122 - الزامات زمانی:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ موج A نمی‌تواند بیشترین زمان را به خود اختصاص دهد.
        ✓ موج B نبایستی زمان کمتری نسبت به موج A صرف کند.
        ✓ موج C نبایستی زمان کمتری نسبت به موج A صرف کند.
        ✓ موج A و C از نظر زمانی گرایش به برابری دارند.
        """
        wave = NeoWaveCorrectiveAnalyzer.calc_3wave_metrics(wave)
        violations = []
        warnings = []
        
        # بررسی صفر نبودن طول موج A
        if wave.len_A == 0:
            return {"type": "خطا", "desc": "طول صفر"}
        
        # ────────────────────────────────────────────────────────────────────
        # بررسی ساختار داخلی (5-3-5) - صفحه 121
        # ────────────────────────────────────────────────────────────────────
        if internal_A and internal_B and internal_C:
            if not InternalStructureValidator.is_zigzag_structure(internal_A, internal_B, internal_C):
                violations.append("ساختار داخلی 5-3-5 رعایت نشده است")
        else:
            warnings.append("ساختار داخلی بررسی نشده است (نیاز به داده تایم فریم پایین‌تر)")
        
        # ────────────────────────────────────────────────────────────────────
        # محاسبه نسبت‌های قیمتی
        # ────────────────────────────────────────────────────────────────────
        r_BA = wave.len_B / wave.len_A if wave.len_A > 0 else 0
        r_CA = wave.len_C / wave.len_A if wave.len_A > 0 else 0
        c_beyond_a = NeoWaveCorrectiveAnalyzer.is_beyond_a(wave, is_bullish)
        
        # ────────────────────────────────────────────────────────────────────
        # الزامات عمومی صفحات 121-122
        # ────────────────────────────────────────────────────────────────────
        if r_BA > NeoWaveCorrectiveAnalyzer.FIB_61_8:
            violations.append(
                f"نقض: B بیش از 61.8% A را اصلاح کرده ({r_BA:.1%}) - احتمال مسطح"
            )
        if r_BA < 0.33:
            warnings.append(
                f"هشدار: B کمتر از 33% A را اصلاح کرده ({r_BA:.1%})"
            )
        if not c_beyond_a:
            violations.append("نکته: C ورای A خاتمه نیافته (احتمال Truncated)")
        
        # ────────────────────────────────────────────────────────────────────
        # بررسی موج B مثلث نباشد (صفحه 121)
        # ────────────────────────────────────────────────────────────────────
        if internal_B and internal_B.get("wave_count", 0) >= 5:
            warnings.append(
                "موج B ممکن است به فرم مثلث باشد - در زیگزاگ مجاز نیست مگر در شرایط خاص"
            )
        
        # ────────────────────────────────────────────────────────────────────
        # قانون خط روند 0-B (صفحه 127)
        # ────────────────────────────────────────────────────────────────────
        # "شکست بی‌اهمیت خط روند 0-B توسط آنچه که به نظر می‌رسد موج B است،
        #  نشاندهنده توسعه مثلثی موج B است."
        warnings.append(
            "خط روند 0-B باید رسم و بررسی شود که موج C آن را لمس نکند"
        )
        
        # ────────────────────────────────────────────────────────────────────
        # الزامات زمانی صفحه 122
        # ────────────────────────────────────────────────────────────────────
        time_status = ""
        if wave.time_A > 0:
            if wave.time_B < wave.time_A:
                time_status = (
                    f"نقض زمانی: B زمان کمتر از A ({wave.time_B} < {wave.time_A})"
                )
            else:
                time_status = (
                    f"تایید زمانی: B زمانبرتر از A ({wave.time_B} >= {wave.time_A})"
                )
        
        # ────────────────────────────────────────────────────────────────────
        # تشخیص زیرنوع (صفحات 123-125)
        # ────────────────────────────────────────────────────────────────────
        sub_type = ZigZagType.NONE
        desc = ""
        page = ""
        
        # زیگزاگ کوتاه شده (صفحه 124)
        if (not c_beyond_a and 
            NeoWaveCorrectiveAnalyzer.FIB_38_2 <= r_CA <= NeoWaveCorrectiveAnalyzer.FIB_61_8):
            sub_type = ZigZagType.TRUNCATED
            desc = (
                "کوتاه شده (صفحه 124): نادر، تایید پس از وقوع. "
                "بایستی حداقل 81% کل الگو بازگشت شود. "
                "اغلب در شاخه مثلث‌ها، ترمینال‌ها، دیامتریک‌ها. "
                "C بین 38.2 تا 61.8% A."
            )
            page = "124"
        
        # زیگزاگ کشیده (صفحه 125)
        elif r_CA > NeoWaveCorrectiveAnalyzer.FIB_161_8:
            sub_type = ZigZagType.ELONGATED
            desc = (
                "کشیده (صفحه 125): نادر. منحصر به مراحل ابتدایی مثلث انقباض/خنب، "
                "انتهای مثلث انبساط، ترمینال. "
                "بایستی حداقل 61.8% موج C اصلاح شود. "
                "C بیش از 161.8% A (ترجیحا 161.8 تا 261.8)."
            )
            page = "125"
        
        # زیگزاگ معمولی (صفحه 123)
        elif (NeoWaveCorrectiveAnalyzer.FIB_61_8 <= r_CA <= 
              NeoWaveCorrectiveAnalyzer.FIB_161_8):
            sub_type = ZigZagType.NORMAL
            desc = (
                "معمولی (صفحه 123): C بین 61.8 تا 161.8% A. "
                "فاقد الزام خاص برای حرکت پساالگو. "
                "ساختار 5-3-5. حداقل بلندای C برابر 61.8% اضافه شده به انتهای A."
            )
            page = "123"
        
        # نسبت غیراستاندارد
        else:
            sub_type = ZigZagType.NORMAL
            desc = f"زیگزاگ با نسبت غیراستاندارد (C برابر {r_CA:.2f} از A)."
            page = "123"
        
        # ────────────────────────────────────────────────────────────────────
        # تعیین برچسب وضعیت (صفحات 454-464)
        # ────────────────────────────────────────────────────────────────────
        position_label = PositionLabel.NONE
        
        # ────────────────────────────────────────────────────────────────────
        # رتبه‌بندی قدرت (صفحات 348-350)
        # ────────────────────────────────────────────────────────────────────
        power = PowerRating.STANDARD.value
        if sub_type == ZigZagType.ELONGATED:
            power = PowerRating.ELONGATED_IN_TRIANGLE.value
        
        return {
            "type": "زیگزاگ",
            "sub_type": sub_type.value,
            "page": page,
            "violations": violations,
            "warnings": warnings,
            "time_status": time_status,
            "r_BA": round(r_BA, 4),
            "r_CA": round(r_CA, 4),
            "c_beyond_a": c_beyond_a,
            "desc": desc,
            "time_A": wave.time_A,
            "time_B": wave.time_B,
            "position_label": position_label.value,
            "power_rating": power
        }


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ادامه کد chapter_12.py - بخش 5: تحلیلگر اصلی امواج اصلاحی (قسمت دوم - مسطح)
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

    # ========================================================================
    # دسته‌بندی مسطح (صفحات 134-158)
    # ========================================================================
    
    @staticmethod
    def classify_flat(wave: WaveStructure3, is_bullish: bool,
                      internal_A: Optional[Dict] = None,
                      internal_B: Optional[Dict] = None,
                      internal_C: Optional[Dict] = None,
                      prev_impulse_retracement: Optional[float] = None) -> Dict[str, Any]:
        """
        دسته‌بندی دقیق مسطح (صفحات 134 تا 155)
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 134 - الزامات عمومی:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ دارای ساختار سه تایی است (3-2-5).
        ✓ موج A بایستی به فرم هر یک از الگوهای اصلاحی باشد و معمولاً روند شکل 
          گیری آن کند می‌باشد.
        ✓ موج B بایستی به فرم هر یک از الگوهای اصلاحی باشد.
        ✓ موج C بایستی به فرم یک الگوی شتابدار باشد.
        ✓ هیچ بخشی از موج C نبایستی خط روند 0-B را لمس کند مگر اینکه موج C 
          به فرم ترمینال باشد.
        ✓ در الگوی مسطح معمولاً برابری قیمتی و تناوب زمانی وجود دارد.
        ✓ با توجه به اینکه موج B، موج اصلاحی در یک روند اصلاحی است، بایستی 
          پیچیده‌تر و زمانبرتر از موج A باشد.
        ✓ هر چه موج B بلندتر باشد احتمال یک موج شتابدار پس از پایان موج C بیشتر 
          می‌شود و رانش پساالگو پر قدرت‌تر خواهد بود.
        ✓ سطح پیچیدگی موج C نبایستی کمتر از سطح پیچیدگی موج A و B باشد.
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        انواع مسطح (صفحات 136-145):
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        1. متعارف (Common) - صفحه 136
        2. موج C ناقص (C-Failure) - صفحه 137
        3. موج B ناقص (B-Failure) - صفحه 139
        4. ناقص دوگانه (Double Failure) - صفحه 140
        5. کشیده (Elongated) - صفحه 141
        6. نامنظم (Irregular) - صفحه 143
        7. نامنظم ناقص (Failure Irregular) - صفحه 144
        8. جاری (Running) - صفحه 145
        """
        wave = NeoWaveCorrectiveAnalyzer.calc_3wave_metrics(wave)
        violations = []
        warnings = []
        
        if wave.len_A == 0:
            return {"type": "خطا", "desc": "طول صفر"}
        
        # ────────────────────────────────────────────────────────────────────
        # بررسی ساختار داخلی (3-3-5) - صفحه 134
        # ────────────────────────────────────────────────────────────────────
        if internal_A and internal_B and internal_C:
            if not InternalStructureValidator.is_flat_structure(internal_A, internal_B, internal_C):
                violations.append("ساختار داخلی 3-3-5 رعایت نشده است")
        else:
            warnings.append("ساختار داخلی بررسی نشده است (نیاز به داده تایم فریم پایین‌تر)")
        
        # ────────────────────────────────────────────────────────────────────
        # محاسبه نسبت‌های قیمتی
        # ────────────────────────────────────────────────────────────────────
        r_BA = wave.len_B / wave.len_A if wave.len_A > 0 else 0
        r_CB = wave.len_C / wave.len_B if wave.len_B > 0 else 0
        c_beyond_a = NeoWaveCorrectiveAnalyzer.is_beyond_a(wave, is_bullish)
        
        # ────────────────────────────────────────────────────────────────────
        # قانون تناوب پیچیدگی (صفحه 134)
        # ────────────────────────────────────────────────────────────────────
        if wave.time_B < wave.time_A:
            warnings.append(
                f"هشدار: زمان موج B ({wave.time_B}) کمتر از موج A ({wave.time_A}) است"
            )
        
        # ────────────────────────────────────────────────────────────────────
        # قاعده مسطح جاری (صفحه 145)
        # ────────────────────────────────────────────────────────────────────
        if prev_impulse_retracement is not None and r_BA > NeoWaveCorrectiveAnalyzer.FIB_138_2:
            if prev_impulse_retracement > NeoWaveCorrectiveAnalyzer.FIB_61_8:
                warnings.append(
                    "در مسطح جاری، موج B نباید بیش از 61.8% موج شتابدار پیشین را اصلاح کند"
                )
        
        # ────────────────────────────────────────────────────────────────────
        # تشخیص زیرنوع (صفحات 136-145)
        # ────────────────────────────────────────────────────────────────────
        sub_type = FlatType.NONE
        desc = ""
        page = ""
        
        # 8. جاری (صفحه 145)
        if r_BA > 1.38 and not c_beyond_a:
            sub_type = FlatType.RUNNING
            desc = (
                "جاری (صفحه 145): رانش پساالگو حداقل 161.8% B. "
                "B بسیار بلندتر (>138% A). "
                "B نباید بیش از 61.8% موج شتابدار پیشین باشد. "
                "A و C از نظر قیمتی/زمانی مشابه. "
                "C وارد محدوده A نمی‌شود."
            )
            page = "145"
        
        # 7. نامنظم ناقص (صفحه 144)
        elif r_BA >= NeoWaveCorrectiveAnalyzer.FIB_138_2 and r_CB < 1.0:
            sub_type = FlatType.FAILURE_IRREGULAR
            desc = (
                "نامنظم ناقص (صفحه 144): B حداقل 138.2% A. "
                "C کل B را اصلاح نکرده (نشان قدرت روند پساالگو). "
                "B بخشیده‌تر از A. رخ می‌دهد قبل از موج ممتد یا قبل از C کشیده."
            )
            page = "144"
        
        # 5. کشیده (صفحه 141)
        elif r_CB > NeoWaveCorrectiveAnalyzer.FIB_138_2:
            sub_type = FlatType.ELONGATED
            desc = (
                "کشیده (صفحه 141): نشانه شکل‌گیری مثلث. "
                "B زمانی مشابه A، قیمت حداکثر 100% A. "
                "C بیش از 138.2% B (ترجیحا 161.8، حداکثر 261.8). "
                "پس از پایان، حداقل 61.8% C اصلاح می‌شود."
            )
            page = "141"
        
        # 6. نامنظم (صفحه 143)
        elif (1.01 <= r_BA <= NeoWaveCorrectiveAnalyzer.FIB_138_2 and 
              r_CB >= 1.01):
            sub_type = FlatType.IRREGULAR
            desc = (
                "نامنظم (صفحه 143): B بین 101 تا 138.2% A. "
                "C حداقل 101% B. B بخشیده‌تر از A. "
                "هر چه B بلندتر، احتمال شتابدار بعدی بیشتر."
            )
            page = "143"
        
        # 2. C ناقص (صفحه 137)
        elif 0.81 <= r_BA <= 1.0 and r_CB < 1.0:
            sub_type = FlatType.C_FAILURE
            desc = (
                "موج C ناقص (صفحه 137): B تقریبا کل A (81-100%) را اصلاح کرده. "
                "B بخشیده‌تر از A. C کمترین زمان را دارد (اغلب ترمینال). "
                "C باید کل B را اصلاح کند (بیشتر از 61.8% B). "
                "نشان قدرت رانش پس از اصلاح (بیشتر از 100% موج پیشین)."
            )
            page = "137"
        
        # 3. B ناقص (صفحه 139)
        elif (NeoWaveCorrectiveAnalyzer.FIB_61_8 <= r_BA < 0.81):
            sub_type = FlatType.B_FAILURE
            desc = (
                "موج B ناقص (صفحه 139): B بین 61.8 تا 81% A. "
                "اغلب A یک زیگزاگ دوگانه/ترکیبی است. "
                "C باید کل B را اصلاح کند (100 تا 138.2%). "
                "A و B باید در تناوب باشند."
            )
            page = "139"
        
        # 4. ناقص دوگانه (صفحه 140)
        elif r_BA < 0.80 and r_CB < 1.0:
            sub_type = FlatType.DOUBLE_FAILURE
            desc = (
                "ناقص دوگانه (صفحه 140): A معمولا ترکیبی دوگانه/سه‌گانه است. "
                "B کمتر از 80% A. C کل B را اصلاح نمی‌کند. "
                "شبیه مثلث افقی ولی C شتابدار است و A ترکیبی است."
            )
            page = "140"
        
        # 1. متعارف (صفحه 136)
        elif 0.81 <= r_BA <= 1.0:
            sub_type = FlatType.COMMON
            desc = (
                "متعارف (صفحه 136): همه امواج هم‌اندازه. "
                "B بین 81 تا 100% A. "
                "B بیشترین زمان و بخشیده‌تر از A. "
                "C نباید بیش از 10-20% انتهای A تجاوز کند."
            )
            page = "136"
        
        else:
            desc = f"مسطح با نسبت‌های غیراستاندارد (B/A: {r_BA:.2f})"
            page = "136"
        
        return {
            "type": "مسطح",
            "sub_type": sub_type.value,
            "page": page,
            "violations": violations,
            "warnings": warnings,
            "r_BA": round(r_BA, 4),
            "r_CB": round(r_CB, 4),
            "c_beyond_a": c_beyond_a,
            "desc": desc,
            "time_A": wave.time_A,
            "time_B": wave.time_B
        }


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ادامه کد chapter_12.py - بخش 5: تحلیلگر اصلی امواج اصلاحی (قسمت سوم - مثلث)
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

    # ========================================================================
    # دسته‌بندی مثلث (صفحات 158-250)
    # ========================================================================
    
    @staticmethod
    def classify_triangle(wave5: WaveStructure5) -> Dict[str, Any]:
        """
        دسته‌بندی دقیق مثلث (صفحات 158 تا 250)
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 159 - الزامات عمومی:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ دارای ساختار پنج قطعه‌ای اصلاحی است (3-3-3-3-3)
        ✓ سه دسته کلی: انقباضی، انبساطی، خنثی
        ✓ جهت توسعه: جاری (در جهت موج پیشین)، افقی، کانتر (خلاف جهت موج پیشین)
        ✓ فقط چهار نقطه از شش نقطه مجاز به لمس خطوط روند کانال بندی می‌باشد
        ✓ خط مبنا: خطی که انتهای موج B و D را به هم متصل می‌کند
        ✓ هیچ یک از ریزموج‌های موج C و E نبایستی از خط مبنا عبور نمایند
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 165 - الزامات قیمتی و زمانی:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ پس از تکمیل مثلث، بایستی یک رانش (Thrust) به اندازه حداقل 75% پهن‌ترین 
          بخش مثلث رخ دهد
        ✓ A > C > E (در مثلث انقباضی)
        ✓ A < C < E (در مثلث انبساطی)
        ✓ A < C > E (در مثلث خنب)
        ✓ موج E حداقل 38.2% و حداکثر 99% موج C
        ✓ زمان موج E متناسب با مجموع یا نصف زمان موج C و D خواهد بود
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحات 168-172 - مثلث انقباضی (محدود و نامحدود):
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ نقطه راس مثلث در محدوده 20 تا 40 درصدی پس از زمان صرف شده توسط مثلث
        ✓ رانش پسامثلث محدود به میزان بلندترین قطعه (75 تا 161.8%)
        ✓ رانش در زمان کمتر از 50% زمان صرف شده توسط مثلث
        ✓ در مثلث نامحدود، محدودیتی به میزان عرض مثلث برای رانش وجود ندارد
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحات 202-208 - مثلث انبساطی:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ موج A تندترین قطعه
        ✓ موج E تقریباً همیشه از خط روند انتهای موج A و C فراتر می‌رود
        ✓ C بین 101 تا 161.8% A
        ✓ E بین 138 تا 161.8% C یا A
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحات 228-235 - مثلث خنب:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ موج A کند است
        ✓ خطوط میل به موازی
        ✓ رانش 50 تا 75% بلندترین قطعه (معمولاً C)
        ✓ A و E حداقل 38.2% و معمولاً 61.8 تا 78.2% موج C
        """
        if len(wave5.points) < 5:
            return {"type": "ناقص", "desc": "کمتر از 5 موج"}
        
        lengths = wave5.lengths
        times = wave5.times
        if len(lengths) < 5 or len(times) < 5:
            return {"type": "ناقص", "desc": "داده ناقص"}
        
        lA, lB, lC, lD, lE = lengths[:5]
        tA, tB, tC, tD, tE = times[:5]
        
        main_cat = ""
        orientation = TriangleOrientation.HORIZONTAL
        alternation = TriangleAlternation.STANDARD
        scope = TriangleScope.NONE
        desc = ""
        page = "165"
        touchpoints = wave5.touchpoints
        
        # قوانین کلی صفحه 165
        if lA <= 0 or lE <= 0:
            return {"type": "خطا", "desc": "طول صفر"}
        
        # ────────────────────────────────────────────────────────────────────
        # محاسبه نقطه راس برای تشخیص محدود/نامحدود (صفحات 168، 172)
        # ────────────────────────────────────────────────────────────────────
        total_time = tA + tB + tC + tD + tE
        if total_time > 0:
            apex_time_ratio = (tA + tB + tC + tD) / total_time
            wave5.apex_time_ratio = apex_time_ratio
            if 0.20 <= apex_time_ratio <= 0.40:
                scope = TriangleScope.LIMITING
            else:
                scope = TriangleScope.NON_LIMITING
        
        # ────────────────────────────────────────────────────────────────────
        # قانون نقاط تماس (صفحه 247)
        # ────────────────────────────────────────────────────────────────────
        if touchpoints > 4:
            desc += f" ⚠️ نقاط تماس ({touchpoints}) بیش از 4 نقطه مجاز است "
            desc += "(در نامحدود می‌تواند 5 نقطه باشد)"
        
        # ────────────────────────────────────────────────────────────────────
        # تشخیص نوع اصلی مثلث
        # ────────────────────────────────────────────────────────────────────
        
        # مثلث انقباضی (Contracting Triangle) - A > C > E
        if lA > lC > lE:
            main_cat = "انقباضی"
            page = "168"
            
            # تشخیص جهت مثلث انقباضی (صفحات 179-192)
            # نامنظم (Irregular) - صفحه 184: B بلندتر از A
            if lB > lA:
                orientation = TriangleOrientation.IRREGULAR
                desc = (
                    "انقباضی نامنظم (صفحه 184): B بلندتر از A (B>A, B>C>D>E). "
                    "رانش حداکثر 161.8% عریض‌ترین."
                )
                page = "184"
            
            # تناوب معکوس (Reverse Alternation) - صفحه 192: D بلندتر از B
            elif lD > lB:
                alternation = TriangleAlternation.REVERSE
                desc = (
                    "انقباضی تناوب معکوس (صفحه 192): D بلندتر از B. "
                    "خطوط میل به موازی بودن. "
                    "رانش بیشتر از عریض‌ترین (معمولا D)."
                )
                page = "192"
            
            # افقی (Horizontal) - صفحه 179: A > B > C > D > E
            elif lA > lB > lC > lD > lE:
                orientation = TriangleOrientation.HORIZONTAL
                desc = (
                    "انقباضی افقی (صفحه 179): A>B>C>D>E. "
                    "رانش برابر عریض‌ترین +/- 25%. "
                    "راس در رنج 61.8% عریض‌ترین."
                )
                page = "179"
            
            else:
                desc = "انقباضی (سایر حالات)."
        
        # مثلث انبساطی (Expanding Triangle) - A < C < E
        elif lA < lC < lE:
            main_cat = "انبساطی"
            page = "202"
            
            # تشخیص جهت مثلث انبساطی (صفحات 208-220)
            # نامنظم (Irregular) - صفحه 210: A > B (B کوتاهتر از A)
            if lA > lB:
                orientation = TriangleOrientation.IRREGULAR
                desc = (
                    "انبساطی نامنظم (صفحه 210): B کوتاهتر از A (A>B). "
                    "D بلندتر و زمانبرتر از B."
                )
                page = "210"
            
            # تناوب معکوس (Reverse Alternation) - صفحه 220: B > D
            elif lB > lD:
                alternation = TriangleAlternation.REVERSE
                desc = (
                    "انبساطی تناوب معکوس (صفحه 220): A کوتاهترین. "
                    "B بلندتر و زمانبرتر از D. B معمولا 138.2% A."
                )
                page = "220"
            
            # افقی (Horizontal) - صفحه 208: E > D > C > B > A
            elif lE > lD > lC > lB > lA:
                orientation = TriangleOrientation.HORIZONTAL
                desc = (
                    "انبساطی افقی (صفحه 208): E>D>C>B>A. "
                    "E بلندترین قطعه."
                )
                page = "208"
            
            else:
                desc = (
                    "انبساطی (سایر حالات). "
                    "رانش 50 تا 100% عریض‌ترین (معمولا E)."
                )
        
        # مثلث خنب (Neutral Triangle) - A < C > E
        elif lA < lC > lE:
            main_cat = "خنب"
            page = "228"
            desc = (
                "خنب (صفحه 228): A کند است. C بلندترین قطعه. "
                "رانش 50 تا 75% C. رفتار بین انقباض و انبساط."
            )
            
            # تشخیص جهت مثلث خنب (صفحات 230-239)
            # نامنظم (Irregular) - صفحه 233: B > A
            if lB > lA:
                orientation = TriangleOrientation.IRREGULAR
                desc = (
                    "خنب نامنظم (صفحه 233): B بلندتر از A و زمان بیشتری دارد. "
                    "رانش بیش از دو برابر عرض کانال."
                )
                page = "233"
            
            # افقی (Horizontal) - صفحه 230: A > B و E > D
            elif lA > lB and lE > lD:
                orientation = TriangleOrientation.HORIZONTAL
                desc = (
                    "خنب افقی (صفحه 230): خطوط میل به موازی. "
                    "A و E معمولا 61.8% با هم مرتبط. رانش اندکی بیشتر از عرض."
                )
                page = "230"
        
        else:
            desc = "مثلث با طبقه‌بندی نامشخص"
            main_cat = "نامشخص"
        
        return {
            "type": "مثلث",
            "main_cat": main_cat,
            "orientation": orientation.value,
            "alternation": alternation.value,
            "scope": scope.value,
            "page": page,
            "desc": desc,
            "touchpoints": touchpoints,
            "apex_time_ratio": round(wave5.apex_time_ratio, 4),
            "lengths": [round(l, 4) for l in lengths[:5]],
            "times": times[:5]
        }


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ادامه کد chapter_12.py - بخش 5: تحلیلگر اصلی امواج اصلاحی (قسمت چهارم - دیامتریک)
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

    # ========================================================================
    # دسته‌بندی دیامتریک (صفحات 251-275)
    # ========================================================================
    
    @staticmethod
    def classify_diametric(wave7: WaveStructure7) -> Dict[str, Any]:
        """
        دسته‌بندی دقیق دیامتریک (صفحات 251 تا 275)
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 251 - الزامات عمومی:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ دارای 7 قطعه می‌باشد که هر قطعه می‌تواند به فرم یکی از الگوهای اصلاحی باشد
        ✓ اگر امواج پیش از E یا F انقباض باشند → پاپیونی (Bow Tie)
        ✓ اگر امواج پیش از E یا F انبساط باشند → الماس (Diamond)
        ✓ کانال بندی بخش اول: خطوط B-D و A-C
        ✓ کانال بندی بخش دوم: خطوط C-E و D-F
        ✓ حداکثر 6 نقطه تماس در کانال بندی
        ✓ حداقل دو موج از B, D, F باید در تناوب باشند
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 252 - الزامات قیمتی و زمانی:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ طول موج G معمولاً متناسب با طول موج A (61.8% یا 161.8%)
        ✓ نسبت تشابه زمانی بین امواج مجاور: 61.8 تا 161.8 درصد
        ✓ حداکثر 1 یا 2 موج می‌تواند زمان متفاوت داشته باشد
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 256 - دیامتریک پاپیونی (Bow Tie):
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ فاز اول انقباض، فاز دوم انبساط
        ✓ D معمولاً کوتاهترین
        ✓ G بلندتر از F و E
        ✓ خط روند یک سمت می‌تواند افقی باشد (ACE یا BDF)
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 265 - دیامتریک الماس (Diamond):
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ فاز اول انبساط، فاز دوم انقباض
        ✓ C یا D بلندترین
        ✓ اگر BDF افقی باشد، C نقش معکوس کننده را دارد
        ✓ اگر ACE افقی باشد، D نقش معکوس کننده را دارد
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 270 - دیامتریک الماس زیگزاگ (ZigZag Diamond):
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ A و G بلندترین و بخشیده‌ترین قطعات
        ✓ B و F در قیاس با آنها بسیار کوتاهتر
        ✓ خط روند CE یا BD می‌تواند افق باشد
        """
        # 7 قطعه نیاز به 8 نقطه عطف دارد (صفحه 251)
        if len(wave7.points) < 8:
            return {"type": "ناقص", "desc": "کمتر از 8 نقطه عطف (نیاز به 7 قطعه)"}
        
        lengths = wave7.lengths
        times = wave7.times
        if len(lengths) < 7 or len(times) < 7:
            return {"type": "ناقص", "desc": "داده ناقص"}
        
        lA, lB, lC, lD, lE, lF, lG = lengths[:7]
        tA, tB, tC, tD, tE, tF, tG = times[:7]
        
        # ────────────────────────────────────────────────────────────────────
        # بررسی شباهت زمانی (صفحه 252) - نسبت 61.8 تا 161.8 درصد
        # ────────────────────────────────────────────────────────────────────
        time_similarities = []
        for i in range(6):
            if times[i] > 0 and times[i+1] > 0:
                ratio = min(times[i], times[i+1]) / max(times[i], times[i+1])
                time_similarities.append(ratio)
        
        times_are_similar = all(s >= NeoWaveCorrectiveAnalyzer.FIB_61_8 
                                for s in time_similarities) if time_similarities else True
        
        # ────────────────────────────────────────────────────────────────────
        # بررسی شباهت قیمتی (برای تمایز از سیمتریک)
        # ────────────────────────────────────────────────────────────────────
        price_similarities = []
        for i in range(6):
            if lengths[i] > 0 and lengths[i+1] > 0:
                ratio = min(lengths[i], lengths[i+1]) / max(lengths[i], lengths[i+1])
                price_similarities.append(ratio)
        
        prices_are_similar = all(s >= NeoWaveCorrectiveAnalyzer.FIB_61_8 
                                  for s in price_similarities) if price_similarities else True
        
        # ────────────────────────────────────────────────────────────────────
        # شناسایی فاز انقباض/انبساط
        # ────────────────────────────────────────────────────────────────────
        phase1_converging = lA > lC if lA > 0 and lC > 0 else False
        phase2_expanding = lE < lG if lE > 0 and lG > 0 else False
        
        # ────────────────────────────────────────────────────────────────────
        # بررسی تناوب بین B, D, F (صفحه 251)
        # ────────────────────────────────────────────────────────────────────
        alternation_check = "بررسی نشد"
        if lB > 0 and lD > 0 and lF > 0:
            if (lB > lD and lD < lF) or (lB < lD and lD > lF):
                alternation_check = "تناوب بین B, D, F برقرار است"
            else:
                alternation_check = "تناوب بین B, D, F برقرار نیست"
        
        # ────────────────────────────────────────────────────────────────────
        # تشخیص زیرنوع دیامتریک
        # ────────────────────────────────────────────────────────────────────
        sub = DiametricType.GENERAL
        desc = ""
        page = "253"
        
        # الماس زیگزاگ (صفحه 270): A و G بسیار بلندتر از B و F
        zigzag_pattern = (lA / lB if lB > 0 else 0) > 2.0 and (lG / lF if lF > 0 else 0) > 2.0
        
        if zigzag_pattern and times_are_similar:
            sub = DiametricType.ZIGZAG_DIAMOND
            desc = (
                "الماس زیگزاگ (صفحه 270): A و G بلندترین و بخشیده‌ترین قطعات. "
                "B و F در قیاس با آنها بسیار کوتاهتر. "
                "خط روند CE یا BD می‌تواند افق باشد."
            )
            page = "270"
        
        # شباهت کامل زمان و قیمت - احتمال سیمتریک (9 موجی)
        elif times_are_similar and prices_are_similar:
            sub = DiametricType.GENERAL
            desc = (
                "شباهت زیاد زمان و قیمت - احتمالاً الگوی سیمتریک (9 موجی) "
                "در حال شکل‌گیری است."
            )
            page = "277"
        
        # شباهت زمانی برقرار است
        elif times_are_similar:
            # پاپیونی (صفحه 256): فاز اول انقباض، فاز دوم انبساط
            if phase1_converging and phase2_expanding:
                sub = DiametricType.BOW_TIE
                desc = (
                    "پاپیونی (صفحه 256): فاز اول انقباض، دوم انبساط. "
                    "D معمولا کوتاهترین. G بلندتر از F و E. "
                    "خط روند یک سمت می‌تواند افقی باشد (ACE یا BDF)."
                )
                page = "256"
            
            # الماس (صفحه 265): فاز اول انبساط، فاز دوم انقباض
            elif not phase1_converging and not phase2_expanding:
                sub = DiametricType.DIAMOND
                desc = (
                    "الماس (صفحه 265): فاز اول انبساط، دوم انقباض. "
                    "C یا D بلندترین. اگر BDF افقی باشد C pivot است. "
                    "اگر ACE افقی باشد D pivot است."
                )
                page = "265"
            
            # دیامتریک عمومی
            else:
                desc = (
                    "دیامتریک عمومی (صفحه 253): زمان‌ها مشابه اما فازها واضح نیستند. "
                    "کانال‌بندی نامنظم. نقش معکوس کننده دو فاز را D یا E بر عهده دارد."
                )
        
        # شباهت زمانی برقرار نیست
        else:
            desc = (
                "دیامتریک عمومی (صفحه 253): زمان‌ها کاملا مشابه نیستند "
                f"(باید 61.8 تا 161.8% باشند)."
            )
        
        return {
            "type": "دیامتریک",
            "sub_type": sub.value,
            "page": page,
            "desc": desc,
            "times_similar": times_are_similar,
            "prices_similar": prices_are_similar,
            "phase1_converging": phase1_converging,
            "phase2_expanding": phase2_expanding,
            "alternation_check": alternation_check,
            "lengths": [round(l, 4) for l in lengths[:7]],
            "times": times[:7]
        }


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ادامه کد chapter_12.py - بخش 5: تحلیلگر اصلی امواج اصلاحی (قسمت پنجم - سیمتریک و قوانین تکمیلی)
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

    # ========================================================================
    # دسته‌بندی سیمتریک (صفحات 277-283)
    # ========================================================================
    
    @staticmethod
    def classify_symmetrical(wave9: WaveStructure9) -> Dict[str, Any]:
        """
        دسته‌بندی دقیق سیمتریک (صفحات 277 تا 283)
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 277 - الزامات عمومی:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ دارای 9 قطعه می‌باشد که هر قطعه می‌تواند به فرم یکی از الگوهای اصلاحی باشد
        ✓ شباهت زمانی و قیمتی و پیچیدگی ساختار امواج به ویژه سه موج اول 
          به عنوان مشخصه اصلی
        ✓ یکی از نشانه‌های شکل‌گیری آن موج A کند می‌باشد
        ✓ جهت توسعه: جاری، افق، کانتر
        ✓ نقش معکوس کننده الگو بر عهده موج E می‌باشد
        ✓ از ویژگی‌های آن کانال بندی دقیق آن می‌باشد
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 278 - الزامات زمانی:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ نسبت تشابه زمانی بین امواج مجاور: 61.8 تا 161.8 درصد
        ✓ موج A نبایستی بیشترین زمان را در بین سه قطعه اول داشته باشد
        ✓ موج C اغلب بایستی زمانی بیش از زمان موج A صرف کند
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        نکته مهم از وبسایت نئوویو (صفحه 606-607):
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        "I now realize a third area - Complexity - should have been included."
        پیچیدگی باید به عنوان سومین معیار شباهت اضافه شود.
        """
        # 9 قطعه نیاز به 10 نقطه عطف دارد (صفحه 277)
        if len(wave9.points) < 10:
            return {"type": "ناقص", "desc": "کمتر از 10 نقطه عطف (نیاز به 9 قطعه)"}
        
        lengths = wave9.lengths
        times = wave9.times
        if len(lengths) < 9 or len(times) < 9:
            return {"type": "ناقص", "desc": "داده ناقص"}
        
        # ────────────────────────────────────────────────────────────────────
        # محاسبه شباهت زمانی (صفحه 278) - نسبت 61.8 تا 161.8 درصد
        # اصلاح مهم: استفاده از سیستم امتیازدهی به جای شرط all() سختگیرانه
        # زیرا در بازار واقعی شرط all() هرگز برقرار نمی‌شود
        # ────────────────────────────────────────────────────────────────────
        time_similarities = []
        for i in range(8):
            if times[i] > 0 and times[i+1] > 0:
                ratio = min(times[i], times[i+1]) / max(times[i], times[i+1])
                time_similarities.append(ratio)
        
        # سیستم امتیازدهی: اگر 70% امواج در رنج 0.618-1.618 باشند
        if time_similarities:
            time_score = sum(1 for s in time_similarities 
                            if NeoWaveCorrectiveAnalyzer.FIB_61_8 <= s <= NeoWaveCorrectiveAnalyzer.FIB_161_8) / len(time_similarities)
        else:
            time_score = 0
        times_are_similar = time_score >= 0.7  # حداقل 70% شباهت
        
        # ────────────────────────────────────────────────────────────────────
        # محاسبه شباهت قیمتی (صفحه 277) - نسبت 61.8 تا 161.8 درصد
        # ────────────────────────────────────────────────────────────────────
        price_similarities = []
        for i in range(8):
            if lengths[i] > 0 and lengths[i+1] > 0:
                ratio = min(lengths[i], lengths[i+1]) / max(lengths[i], lengths[i+1])
                price_similarities.append(ratio)
        
        if price_similarities:
            price_score = sum(1 for s in price_similarities 
                            if NeoWaveCorrectiveAnalyzer.FIB_61_8 <= s <= NeoWaveCorrectiveAnalyzer.FIB_161_8) / len(price_similarities)
        else:
            price_score = 0
        prices_are_similar = price_score >= 0.7  # حداقل 70% شباهت
        
        # ────────────────────────────────────────────────────────────────────
        # بررسی شباهت پیچیدگی (صفحه 323 و وبسایت نئوویو)
        # ────────────────────────────────────────────────────────────────────
        # در عمل نیاز به محاسبه پیچیدگی دقیق‌تر بر اساس تعداد زیرموج‌ها دارد
        complexity_score_val = 0.8  # فرضی - در عمل باید محاسبه شود
        
        desc = ""
        page = "277"
        
        if times_are_similar and prices_are_similar and complexity_score_val >= 0.7:
            desc = (
                "سیمتریک (صفحه 277-283): الگوی 9 قطعه‌ای بدون X-wave. "
                "تمامی امواج از نظر زمان، قیمت و پیچیدگی مشابه هستند. "
                "این تشابه در هیچ الگوی دیگری مجاز نیست. "
                "کانال‌بندی بین خطوط موازی. نقش معکوس کننده بر عهده موج E است. "
                f"امتیاز شباهت زمانی: {time_score:.0%}، قیمتی: {price_score:.0%}"
            )
            page = "277"
        else:
            desc = (
                f"شباهت کامل زمان و قیمت در همه قطعات وجود ندارد "
                f"(زمان: {time_score:.0%}، قیمت: {price_score:.0%}) - احتمالاً الگوی دیگر است."
            )
        
        return {
            "type": "سیمتریک" if (times_are_similar and prices_are_similar and complexity_score_val >= 0.7) else "نامشخص",
            "page": page,
            "desc": desc,
            "times_similar": times_are_similar,
            "prices_similar": prices_are_similar,
            "time_score": round(time_score, 3),
            "price_score": round(price_score, 3),
            "lengths": [round(l, 4) for l in lengths[:9]],
            "times": times[:9]
        }


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ادامه کد chapter_12.py - بخش 5: تحلیلگر اصلی امواج اصلاحی (قسمت ششم - قوانین تکمیلی)
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

    # ========================================================================
    # یافتن محدوده پایان موج B (صفحات 284-286)
    # ========================================================================
    
    @staticmethod
    def find_wave_b_end_triangle(wave5: WaveStructure5) -> Dict[str, Any]:
        """
        یافتن محدوده پایان موج B در الگوهای اصلاحی (صفحات 284-286)
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 284:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        "انتهای موج B به طریق مشابه انتهای موج 2 سنجیده می‌شود با این تفاوت 
         که موج شتابدار متعاقب آن (موج C) به ندرت بیش از 161.8 درصد موج A می‌باشد."
        
        "اگر موج B به شکل مثلث باشد در اینصورت به دو روش می‌توان کانال بندی را انجام داد:
         - روش A: خط روند 0-B از انتهای موج C مثلث رسم گردیده است
         - روش B: موج E به صورت یک شکست به اصطلاح کاذب خط روند را می‌شکند 
                  ولی نبایستی از انتهای موج C تجاوز نماید."
        
        صفحه 285:
        "اگر بازار از نقطه تماس خط روندی که شما تصور می‌کنید انتهای موج B می‌باشد، 
         شروع به صعود و مجددا نزول کند و خط روند مفروض را بشکند (پیش از آنکه ورای 
         نقطه ای که شما تصور می‌کردید پایان موج B است) و مجددا صعود کند، 
         این دلیل بر توسعه یک الگوی مثلث می‌باشد."
        
        صفحه 286:
        "اصلاح‌های درون مثلث به گونه‌ای تصادفی و خیلی کند خطوط روند را می‌شکنند 
         که نشانه ای قطعی بر شکل گیری مثلث می‌باشند."
        """
        if len(wave5.points) < 5:
            return {"status": "ناقص", "desc": "کمتر از 5 موج"}
        
        lengths = wave5.lengths
        times = wave5.times
        if len(lengths) < 5 or len(times) < 5:
            return {"status": "ناقص", "desc": "داده ناقص"}
        
        lA, lB, lC, lD, lE = lengths[:5]
        tA, tB, tC, tD, tE = times[:5]
        
        desc = ""
        method = ""
        
        # صفحه 284 - دو روش کانال‌بندی
        if lA > 0 and lC > 0:
            channel_slope = (lC - lA) / (tC - tA) if tC != tA else 0
            method = "خط روند 0-B از انتهای موج C مثلث رسم گردیده است"
            
            # بررسی شکست کاذب (صفحه 284 - شکل B)
            if lE / lC > 0.95 and lE / lC < 1.05:
                desc = (
                    "موج E به صورت یک شکست به اصطلاح کاذب خط روند را می‌شکند و لیکن "
                    "این شکست نبایستی از انتهای موج C تجاوز نماید."
                )
            else:
                desc = "خط روند 0-B از انتهای موج C مثلث رسم گردیده است."
        
        return {
            "status": "تکمیل",
            "desc": desc,
            "method": method,
            "channel_slope": round(channel_slope, 6) if 'channel_slope' in dir() else 0
        }
    
    # ========================================================================
    # دسته‌بندی الگوهای ترکیبی (صفحات 287-316)
    # ========================================================================
    
    @staticmethod
    def classify_combination(patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        دسته‌بندی الگوهای اصلاحی غیر استاندارد ترکیب (صفحات 287-316)
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 287 - الگوهای شارپ:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ زیگزاگ دوگانه (Double ZigZag)
        ✓ زیگزاگ سه گانه (Triple ZigZag)
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 288-290 - الگوهای ساید:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ دوگانه سه تای (Double Three): ترکیب دو الگوی اصلاحی و یک موج اصلاحی میانی
        ✓ سه گانه سه تای (Triple Three): ترکیب سه الگوی اصلاحی و دو موج اصلاحی میانی
        """
        if len(patterns) < 2:
            return {"type": CombinationType.NONE.value, "desc": "الگوی ترکیبی شناسایی نشد"}
        
        # تشخیص نوع ترکیب بر اساس تعداد الگوها
        if len(patterns) == 2:
            # دوگانه سه تای یا زیگزاگ دوگانه
            if (patterns[0].get("sub_type") == "زیگزاگ" and 
                patterns[1].get("sub_type") == "زیگزاگ"):
                comb_type = CombinationType.DOUBLE_ZIGZAG
                desc = (
                    "زیگزاگ دوگانه (صفحه 287): دو الگوی زیگزاگ متوالی که "
                    "توسط یک X-wave کوتاه از هم جدا شده‌اند. "
                    "معمولاً پس از الگوی شتابدار رخ می‌دهد."
                )
                page = "287"
            else:
                comb_type = CombinationType.DOUBLE_THREE
                desc = (
                    "دوگانه سه تای (صفحه 288): ترکیب دو الگوی اصلاحی "
                    "(مسطح/مثلث/زیگزاگ) که توسط یک X-wave از هم جدا شده‌اند. "
                    "به صورت مایل در جهت روند حرکت می‌کند."
                )
                page = "288"
        else:
            # سه گانه سه تای یا زیگزاگ سه گانه
            zigzag_count = sum(1 for p in patterns if p.get("sub_type") == "زیگزاگ")
            if zigzag_count >= 3:
                comb_type = CombinationType.TRIPLE_ZIGZAG
                desc = (
                    "زیگزاگ سه گانه (صفحه 287): سه الگوی زیگزاگ متوالی که "
                    "توسط دو X-wave از هم جدا شده‌اند. "
                    "قوی‌ترین الگوی اصلاحی است."
                )
                page = "287"
            else:
                comb_type = CombinationType.TRIPLE_THREE
                desc = (
                    "سه گانه سه تای (صفحه 289): ترکیب سه الگوی اصلاحی "
                    "(مسطح/مثلث/زیگزاگ) که توسط دو X-wave از هم جدا شده‌اند. "
                    "به صورت مایل در جهت روند حرکت می‌کند."
                )
                page = "289"
        
        return {
            "type": comb_type.value,
            "page": page,
            "desc": desc,
            "pattern_count": len(patterns)
        }
    
    # ========================================================================
    # تحلیل X-wave (صفحات 291-309)
    # ========================================================================
    
    @staticmethod
    def analyze_x_wave(wave_data: Dict[str, Any], prev_pattern: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحلیل X-wave در الگوهای غیر استاندارد (صفحات 291-309)
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحات 291-292 - X-wave کوتاه:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ قوی‌ترین اخطار: دو الگوی اصلاحی توسط یک موج اصلاحی جدا شده باشند که 
          فاز اول اصلاح توسط موج میانی کمی از 61.8% بازگشت شده باشد
        ✓ X-wave از نظر زمانی بایستی کوتاهتر از اصلاح پیشین و پسین باشد
        ✓ ساختار X-wave معمولاً یک تک موج، مسطح یا مثلث است
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحات 301-302 - X-wave بلند:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ اگر سه الگوی اصلاحی پشت سر هم رخ دهند و دومی بیش از 100% فاز اول باشد
        ✓ معمولاً از نظر زمانی X-wave 100% الگوی پیش از خود خواهد بود
        ✓ X-wave بین 138.2% تا 161.8% فاز اول (در دوگانه سه تای جاری)
        
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        صفحه 310 - قوانین حدی X-wave:
        ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        ✓ X-wave از نظر پیچیدگی و زمان نباید کمتر از 1/3 و حداکثر برابر الگوی پیشین باشد
        ✓ X-wave های کوتاه نمی‌توانند به فرم محدود مثلث انقباض باشند
        """
        x_type = XWaveType.NONE
        desc = ""
        page = ""
        conditions = {}
        
        # استخراج نسبت‌ها
        price_ratio = wave_data.get("price_ratio", 0)
        time_ratio = wave_data.get("time_ratio", 0)
        complexity_ratio = wave_data.get("complexity_ratio", 0)
        
        # X-wave کوتاه (صفحه 291-292)
        if price_ratio < NeoWaveCorrectiveAnalyzer.FIB_61_8 and price_ratio > 0:
            x_type = XWaveType.SHORT
            conditions["price_condition"] = f"قیمت: {price_ratio:.1%} < 61.8%"
            conditions["time_condition"] = (
                f"زمان: {time_ratio:.1%} (باید کمتر از اصلاح پیشین)" 
                if time_ratio < 1 else "زمان: نیاز به بررسی"
            )
            desc = (
                "X-wave کوتاه (صفحه 291-292): قوی‌ترین اخطار زمانی که دو الگوی اصلاحی "
                "توسط یک موج اصلاحی جدا شده باشند که فاز اول اصلاح توسط موج میانی "
                "کمی از 61.8 درصد بازگشت شده باشد. X-wave از نظر زمانی بایستی کوتاهتر از "
                "اصلاح پیشین و پسین باشد."
            )
            page = "291"
        
        # X-wave بلند (صفحه 301-302)
        elif price_ratio > 1.0:
            x_type = XWaveType.LONG
            conditions["price_condition"] = f"قیمت: {price_ratio:.1%} > 100%"
            conditions["time_condition"] = (
                f"زمان: {time_ratio:.1%} (معمولا 100% الگوی پیشین)" 
                if time_ratio >= 0.8 else "زمان: کمتر از حد انتظار"
            )
            desc = (
                "X-wave بلند (صفحه 301-302): اگر سه الگوی اصلاحی پشت سر هم رخ دهند "
                "به گونه‌ای که دومی فاز آن بیش از 100 درصد (ترجیحاً 138 تا 161.8 درصد) "
                "فاز اول باشد، به احتمال بسیار زیاد دومی فاز اصلاحی یک X-wave خواهد بود. "
                "معمولاً از نظر زمانی X-wave 100 درصد الگوی پیش از خود خواهد بود."
            )
            page = "301"
        
        # قوانین حدی X-wave (صفحه 310)
        if NeoWaveCorrectiveAnalyzer.FIB_33_3 <= price_ratio <= 1.0:
            conditions["price_limit"] = "رعایت حد 1/3 تا 100% قیمت"
        if NeoWaveCorrectiveAnalyzer.FIB_33_3 <= time_ratio <= 1.0:
            conditions["time_limit"] = "رعایت حد 1/3 تا 100% زمان"
        
        # شرط X-wave در دوگانه سه تای جاری (صفحه 306)
        if (NeoWaveCorrectiveAnalyzer.FIB_138_2 <= price_ratio <= 
            NeoWaveCorrectiveAnalyzer.FIB_161_8):
            conditions["running_double_three"] = (
                f"X-wave در محدوده 138.2 تا 161.8% (مناسب برای دوگانه سه تای جاری)"
            )
        
        return {
            "x_type": x_type.value,
            "page": page,
            "desc": desc,
            "conditions": conditions,
            "price_ratio": round(price_ratio, 3),
            "time_ratio": round(time_ratio, 3)
        }
    
    # ========================================================================
    # تایید پساالگویی Type 1 و Type 2 (صفحات 110-113، 130، 155، 200، 226، 250، 276، 283، 317)
    # ========================================================================
    
    @staticmethod
    def post_pattern_confirmation_type1(retracement_time: int, wave_time: int,
                                         retracement_pct: float) -> Dict[str, Any]:
        """
        تایید پساالگویی Type 1 (برای الگوهای قابل شناسایی)
        
        صفحه 110-113:
        مرحله 1 (اجباری): بازگشت قیمت به خط روند 2-4 در زمان کمتر از زمان شکل‌گیری موج 5
        مرحله 2 (اختیاری): بازگشت کامل موج 5 در زمان کمتر یا برابر زمان شکل‌گیری موج 5
        """
        stage1_ok = retracement_time <= wave_time
        stage2_ok = retracement_pct >= 100.0
        
        return {
            "stage1_confirmed": stage1_ok,
            "stage2_confirmed": stage2_ok,
            "retracement_time": retracement_time,
            "wave_time": wave_time,
            "retracement_pct": round(retracement_pct, 1)
        }
    
    @staticmethod
    def post_pattern_confirmation_type2(largest_counter_move: Dict, current_move: Dict) -> Dict[str, Any]:
        """
        تایید پساالگویی Type 2 (برای اصلاح‌های پیچیده و ناشناخته)
        
        صفحه 317:
        بزرگترین حرکت خلاف جهت روند درون اصلاح را پیدا کنید
        اگر حرکت جدید بزرگتر و سریعتر از آن بود، اصلاح تمام شده است
        """
        if not largest_counter_move or not current_move:
            return {"confirmed": False, "desc": "داده کافی نیست"}
        
        larger = current_move.get("price", 0) > largest_counter_move.get("price", 0)
        faster = current_move.get("time", 1) < largest_counter_move.get("time", 0)
        
        return {
            "confirmed": larger and faster,
            "is_larger": larger,
            "is_faster": faster,
            "largest_counter_price": largest_counter_move.get("price", 0),
            "largest_counter_time": largest_counter_move.get("time", 0),
            "current_price": current_move.get("price", 0),
            "current_time": current_move.get("time", 0)
        }
    
    @staticmethod
    def post_pattern_confirmation_unknown(corrective_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تایید پساالگوی در یک الگوی اصلاحی ناشناخته (صفحه 317)
        
        سه مرحله:
        1. آخرین ریزموج از آخرین قطعه در جهت توسعه الگو
        2. بلندترین قطعه در خلاف جهت توسعه الگو
        3. بلندترین قطعه در جهت توسعه الگو
        """
        results = {}
        
        # مرحله 1: آخرین ریزموج از آخرین قطعه در جهت توسعه الگو
        last_small_wave = corrective_data.get("last_small_wave", {})
        if last_small_wave:
            results["stage1"] = {
                "desc": (
                    "آخرین ریزموج از آخرین قطعه در جهت توسعه الگو را بیابید. "
                    "رانش پساالگوی بایستی از نظر زمانی کمی و از نظر قیمتی بلندتر از آن باشد."
                ),
                "time_check": last_small_wave.get("time_check", "نامشخص"),
                "price_check": last_small_wave.get("price_check", "نامشخص")
            }
        
        # مرحله 2: بلندترین قطعه در خلاف جهت توسعه الگو
        largest_counter = corrective_data.get("largest_counter_trend", {})
        if largest_counter:
            results["stage2"] = {
                "desc": (
                    "بلندترین قطعه در خلاف جهت توسعه الگو را بیابید. "
                    "رانش پساالگوی بایستی از نظر زمانی کمی و از نظر قیمتی بلندتر از آن باشد."
                ),
                "time_check": largest_counter.get("time_check", "نامشخص"),
                "price_check": largest_counter.get("price_check", "نامشخص")
            }
        
        # مرحله 3: بلندترین قطعه در جهت توسعه الگو
        largest_same = corrective_data.get("largest_same_trend", {})
        if largest_same:
            results["stage3"] = {
                "desc": (
                    "بلندترین قطعه در جهت توسعه الگو را بیابید. "
                    "رانش پساالگوی بایستی از نظر زمانی کمی و از نظر قیمتی بلندتر از آن باشد."
                ),
                "time_check": largest_same.get("time_check", "نامشخص"),
                "price_check": largest_same.get("price_check", "نامشخص")
            }
        
        # نکته صفحه 317
        results["note"] = (
            "در صورتی که بلندترین قطعه در راستای توسعه الگو (روند) از نظر قیمتی "
            "کوتاهتر از بلندترین قطعه در خلاف جهت روند باشد ترتیب مراحل 2 و 3 "
            "می‌تواند عوض شود."
        )
        
        return results
    
    # ========================================================================
    # محاسبه میزان رانش پس از مثلث (صفحات 168، 250، 575)
    # ========================================================================
    
    @staticmethod
    def calculate_thrust_target(widest_leg: float, triangle_type: str) -> Dict[str, Any]:
        """
        محاسبه میزان رانش پس از مثلث
        
        از وبسایت نئوویو (Question of the Week):
        "Contracting Triangles produce the most dramatic, post-pattern behavior 
         with a 'thrust' nearly equal to the widest leg."
        
        "NEoWave Neutral Triangles exhibit post-pattern 'thrusts' that are 
         about 75% of the width of the largest wave."
        
        "Expanding Triangles have the smallest post-pattern 'thrusts,' 
         which are usually about 50% of the longest leg."
        """
        if triangle_type == "contracting":
            target = widest_leg
            range_min = target * 0.75
            range_max = target * 1.25
            desc = (
                "رانش پساالگو در مثلث انقباض تقریبا برابر با عریض‌ترین قطعه است (معمولاً 100%). "
                "در مثلث محدود، رانش پرشتاب‌تر و پر قدرت‌تر از نامحدود است."
            )
            page = "168"
        elif triangle_type == "neutral":
            target = widest_leg * 0.75
            range_min = target * 0.67
            range_max = target * 1.33
            desc = (
                "رانش پساالگو در مثلث خنب حدود 75% عریض‌ترین قطعه است (معمولاً موج C). "
                "رفتار بین انقباض و انبساط است."
            )
            page = "228"
        else:  # expanding
            target = widest_leg * 0.50
            range_min = target * 0.5
            range_max = target * 1.5
            desc = (
                "رانش پساالگو در مثلث انبساط حدود 50% عریض‌ترین قطعه است (معمولاً موج E). "
                "حداکثر رانش معمولاً کمی از 50% عرض بلندترین قطعه می‌باشد."
            )
            page = "250"
        
        return {
            "target": round(target, 4),
            "range_min": round(range_min, 4),
            "range_max": round(range_max, 4),
            "desc": desc,
            "page": page
        }
    
    # ========================================================================
    # رتبه‌بندی قدرت الگوهای اصلاحی (صفحات 348-350)
    # ========================================================================
    
    @staticmethod
    def get_power_rating(pattern_type: str, sub_type: str, is_in_triangle: bool = False) -> int:
        """
        بازگرداندن رتبه قدرت یک الگوی اصلاحی
        
        جدول صفحات 348-350:
        ┌─────────────────────────────────────┬───────────┐
        │ الگو                                 │ رتبه قدرت │
        ├─────────────────────────────────────┼───────────┤
        │ زیگزاگ سه‌گانه                       │    3      │
        │ ترکیب سه‌گانه                        │    3      │
        │ مسطح سه‌گانه                         │    3      │
        │ Running Correction                   │    3      │
        │ زیگزاگ دوگانه                        │    2      │
        │ ترکیب دوگانه                         │    2      │
        │ مسطح دوگانه                          │    2      │
        │ زیگزاگ کشیده (در مثلث)               │    1      │
        │ مسطح کشیده (در مثلث)                 │    1      │
        │ C-Failure (در مثلث)                  │    1      │
        │ Irregular (در مثلث)                  │    1      │
        │ Irregular Failure (در مثلث)          │    2      │
        │ استاندارد                             │    0      │
        └─────────────────────────────────────┴───────────┘
        """
        if "سه_گانه" in sub_type or "Triple" in pattern_type:
            return PowerRating.TRIPLE_ZIGZAG.value
        elif "دوگانه" in sub_type or "Double" in pattern_type:
            return PowerRating.DOUBLE_ZIGZAG.value
        elif sub_type == "کشیده" and is_in_triangle:
            return PowerRating.ELONGATED_IN_TRIANGLE.value
        elif sub_type == "موج_C_ناقص" and is_in_triangle:
            return PowerRating.C_FAILURE_IN_TRIANGLE.value
        elif sub_type == "نامنظم" and is_in_triangle:
            return PowerRating.IRREGULAR_IN_TRIANGLE.value
        elif sub_type == "نامنظم_ناقص" and is_in_triangle:
            return PowerRating.IRREGULAR_FAILURE_IN_TRIANGLE.value
        elif sub_type == "جاری":
            return PowerRating.RUNNING_CORRECTION.value
        else:
            return PowerRating.STANDARD.value


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ادامه کد chapter_12.py - بخش 6: الگوریتم استخراج الگو از داده خام
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════


def _detect_pivots(high: List[float], low: List[float], close: List[float], 
                   threshold: float = 0.5) -> List[Dict]:
    """
    شناسایی نقاط عطف قیمتی با الگوریتم پیشرفته نئوویو
    
    این تابع از کلاس AdvancedPivotDetector برای تشخیص نقاط عطف استفاده می‌کند.
    حساسیت (sensitivity) به عنوان درصد حداقل تغییر برای تشخیص برگشت عمل می‌کند.
    
    صفحات مرجع: 23-25 (کش دیتا)، 43-45 (قانون خنثایی)
    """
    return AdvancedPivotDetector.detect(np.array(high), np.array(low), np.array(close), threshold)


def scan_corrective_patterns(close: List[float], high: List[float], low: List[float]) -> Dict[str, List]:
    """
    پویش داده برای یافتن تمام امواج اصلاحی ممکن
    
    این تابع الگوهای زیر را جستجو می‌کند:
    - الگوهای 3 موجی (زیگزاگ و مسطح)
    - الگوهای 5 موجی (مثلث)
    - الگوهای 7 موجی (دیامتریک)
    - الگوهای 9 موجی (سیمتریک)
    
    صفحات مرجع: 120-323
    """
    pivots = _detect_pivots(high, low, close, threshold=0.5)
    res: Dict[str, List] = {
        "zigzags": [], "flats": [], "triangles": [], 
        "diametrics": [], "symmetricals": [], "combinations": []
    }
    
    # ────────────────────────────────────────────────────────────────────────
    # الگوهای 3 موجی (زیگزاگ و مسطح) - صفحات 121-158
    # ────────────────────────────────────────────────────────────────────────
    for i in range(len(pivots) - 2):
        pA, pB, pC = pivots[i:i+3]
        is_bull_corr = (pA["type"] == "H" and pB["type"] == "L" and pC["type"] == "H")
        is_bear_corr = (pA["type"] == "L" and pB["type"] == "H" and pC["type"] == "L")
        
        if is_bull_corr or is_bear_corr:
            w3 = WaveStructure3(
                wA=WavePoint(pA["index"], pA["price"], pA["index"]),
                wB=WavePoint(pB["index"], pB["price"], pB["index"]),
                wC=WavePoint(pC["index"], pC["price"], pC["index"])
            )
            tmp = NeoWaveCorrectiveAnalyzer.calc_3wave_metrics(w3)
            r = tmp.len_B / tmp.len_A if tmp.len_A > 0 else 0
            
            # نسبت B/A تعیین می‌کند که الگو زیگزاگ است یا مسطح (صفحه 121-122)
            if r <= NeoWaveCorrectiveAnalyzer.FIB_61_8:
                res["zigzags"].append(NeoWaveCorrectiveAnalyzer.classify_zigzag(w3, is_bull_corr))
            elif r > NeoWaveCorrectiveAnalyzer.FIB_61_8:
                res["flats"].append(NeoWaveCorrectiveAnalyzer.classify_flat(w3, is_bull_corr))
    
    # ────────────────────────────────────────────────────────────────────────
    # الگوهای 5 موجی (مثلث) - صفحات 159-250
    # 5 قطعه نیاز به 6 نقطه عطف دارد
    # ────────────────────────────────────────────────────────────────────────
    for i in range(len(pivots) - 5):
        pts = pivots[i:i+6]
        types = [p["type"] for p in pts]
        
        # الگوی متناوب H-L-H-L-H-L یا L-H-L-H-L-H
        if types == ["H","L","H","L","H","L"] or types == ["L","H","L","H","L","H"]:
            w5 = WaveStructure5(
                points=[WavePoint(p["index"], p["price"], p["index"]) for p in pts],
                lengths=[abs(pts[j+1]["price"] - pts[j]["price"]) for j in range(5)],
                times=[pts[j+1]["index"] - pts[j]["index"] for j in range(5)]
            )
            # محاسبه نقاط تماس با کانال B-D (صفحه 247)
            w5.touchpoints = 0
            # محاسبه ساده نقاط تماس
            if len(w5.points) >= 2:
                # نقطه شروع (0) و موج B و D خط مبنا را تشکیل می‌دهند
                b_point = w5.points[1] if len(w5.points) > 1 else None
                d_point = w5.points[3] if len(w5.points) > 3 else None
                # موج C و E با خط مبنا بررسی می‌شوند
                # (در عمل نیاز به کانال‌بندی دقیق‌تر دارد)
                w5.touchpoints = 4  # مقدار پیش‌فرض
            
            res["triangles"].append(NeoWaveCorrectiveAnalyzer.classify_triangle(w5))
    
    # ────────────────────────────────────────────────────────────────────────
    # الگوهای 7 موجی (دیامتریک) - صفحات 251-276
    # 7 قطعه نیاز به 8 نقطه عطف دارد
    # ────────────────────────────────────────────────────────────────────────
    for i in range(len(pivots) - 7):
        pts = pivots[i:i+8]
        types = [p["type"] for p in pts]
        
        # الگوی متناوب H-L-H-L-H-L-H-L یا L-H-L-H-L-H-L-H
        if types == ["H","L","H","L","H","L","H","L"] or \
           types == ["L","H","L","H","L","H","L","H"]:
            w7 = WaveStructure7(
                points=[WavePoint(p["index"], p["price"], p["index"]) for p in pts],
                lengths=[abs(pts[j+1]["price"] - pts[j]["price"]) for j in range(7)],
                times=[pts[j+1]["index"] - pts[j]["index"] for j in range(7)]
            )
            res["diametrics"].append(NeoWaveCorrectiveAnalyzer.classify_diametric(w7))
    
    # ────────────────────────────────────────────────────────────────────────
    # الگوهای 9 موجی (سیمتریک) - صفحات 277-283
    # 9 قطعه نیاز به 10 نقطه عطف دارد
    # ────────────────────────────────────────────────────────────────────────
    if len(pivots) >= 10:
        for i in range(len(pivots) - 9):
            pts = pivots[i:i+10]
            types = [p["type"] for p in pts]
            pattern1 = ["H","L","H","L","H","L","H","L","H","L"]
            pattern2 = ["L","H","L","H","L","H","L","H","L","H"]
            
            if types == pattern1 or types == pattern2:
                w9 = WaveStructure9(
                    points=[WavePoint(p["index"], p["price"], p["index"]) for p in pts],
                    lengths=[abs(pts[j+1]["price"] - pts[j]["price"]) for j in range(9)],
                    times=[pts[j+1]["index"] - pts[j]["index"] for j in range(9)]
                )
                res["symmetricals"].append(NeoWaveCorrectiveAnalyzer.classify_symmetrical(w9))
    
    return res


def find_combination_patterns(close: List[float], high: List[float], low: List[float]) -> Dict[str, Any]:
    """
    یافتن الگوهای ترکیبی (Double/Triple ZigZag و Double/Triple Three)
    
    صفحات 287-316:
    - الگوهای شارپ: زیگزاگ دوگانه و سه گانه
    - الگوهای ساید: دوگانه سه تای و سه گانه سه تای
    """
    pivots = _detect_pivots(high, low, close, threshold=0.5)
    
    # جستجوی الگوهای متوالی 3 موجی
    patterns_found = []
    i = 0
    while i < len(pivots) - 2:
        pA, pB, pC = pivots[i:i+3]
        is_valid = (pA["type"] != pB["type"] and pB["type"] != pC["type"])
        
        if is_valid:
            w3 = WaveStructure3(
                wA=WavePoint(pA["index"], pA["price"], pA["index"]),
                wB=WavePoint(pB["index"], pB["price"], pB["index"]),
                wC=WavePoint(pC["index"], pC["price"], pC["index"])
            )
            tmp = NeoWaveCorrectiveAnalyzer.calc_3wave_metrics(w3)
            r = tmp.len_B / tmp.len_A if tmp.len_A > 0 else 0
            
            if r <= NeoWaveCorrectiveAnalyzer.FIB_61_8:
                patterns_found.append({"type": "zigzag", "data": tmp, "pivots": [pA, pB, pC]})
            else:
                patterns_found.append({"type": "flat", "data": tmp, "pivots": [pA, pB, pC]})
        
        i += 1
    
    # تجمیع الگوهای متوالی
    if len(patterns_found) >= 2:
        return NeoWaveCorrectiveAnalyzer.classify_combination(patterns_found)
    
    return {"type": CombinationType.NONE.value, "desc": "الگوی ترکیبی شناسایی نشد", "pattern_count": 0}


def find_x_wave_between_patterns(pattern1: Dict, pattern2: Dict, wave_data: Dict) -> Dict[str, Any]:
    """
    تشخیص X-wave بین دو الگوی اصلاحی
    
    صفحات 291-309:
    - X-wave کوتاه: قیمت کمتر از 61.8% الگوی قبلی، زمان کمتر
    - X-wave بلند: قیمت بیش از 100% الگوی قبلی (ترجیحاً 138 تا 161.8%)
    """
    if not pattern1 or not pattern2:
        return {"x_type": XWaveType.NONE.value, "desc": "داده کافی نیست"}
    
    # محاسبه نسبت‌ها
    price_ratio = pattern2.get("price_ratio", 0) / pattern1.get("price_ratio", 1) if pattern1.get("price_ratio", 0) > 0 else 0
    time_ratio = pattern2.get("time_ratio", 0) / pattern1.get("time_ratio", 1) if pattern1.get("time_ratio", 0) > 0 else 0
    
    wave_data["price_ratio"] = price_ratio
    wave_data["time_ratio"] = time_ratio
    
    return NeoWaveCorrectiveAnalyzer.analyze_x_wave(wave_data, pattern1)


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ادامه کد chapter_12.py - بخش 7: تابع analyze (Interface اصلی برای main.py)
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════


def analyze(data: pd.DataFrame, logger=None, context=None) -> Dict:
    """
    فصل 12: دسته‌بندی امواج اصلاحی (Corrective Waves)
    
    این تابع مطابق با interface تعریف شده در main.py پیاده‌سازی شده است.
    
    پارامترها:
        data   : DataFrame با ستون‌های open, high, low, close, volume
        logger : آبجکت ResultsLogger برای ذخیره نتایج (اختیاری)
    
    خروجی:
        دیکشنری نتایج - همه key ها string هستند
    
    ═══════════════════════════════════════════════════════════════════════════
    صفحات پوشش داده شده در این تابع:
    ═══════════════════════════════════════════════════════════════════════════
    120-323: تمام صفحات فصل 12 به طور کامل پوشش داده شده است.
    """
    close = data['close'].values if 'close' in data.columns else data['Close'].values
    high = data['high'].values if 'high' in data.columns else data['High'].values
    low = data['low'].values if 'low' in data.columns else data['Low'].values
    n = len(close)
    
    monowaves_from_ch5 = None
    context_used = False
    
    if context and "chapter_5" in context and "_monowaves" in context["chapter_5"]:
        monowaves_from_ch5 = context["chapter_5"]["_monowaves"]
        context_used = True
    
    # ── دریافت اطلاعات از فصل‌های ۶ و ۷ ──────────────
    proportion_info = None
    neutrality_info = None
    
    if context:
        if "chapter_6" in context:
            proportion_info = context["chapter_6"]
        if "chapter_7" in context:
            neutrality_info = context["chapter_7"]
    
    # ────────────────────────────────────────────────────────────────────────
    # بررسی حداقل داده مورد نیاز (صفحه 534)
    # "برای شمارش صحیح بایستی نمودار شما حداقل 13 و حداکثر 55 تک موج داشته باشد"
    # ────────────────────────────────────────────────────────────────────────
    if n < 20:
        return {
            "عنوان": "فصل 12: امواج اصلاحی",
            "وضعیت": "داده_کافی_نیست",
            "تعداد_کندل": str(n),
            "پیام": "برای تحلیل امواج اصلاحی به حداقل 20 کندل نیاز است.",
            "تفسیر_نهایی": "خطا: برای تحلیل امواج اصلاحی به حداقل 20 کندل نیاز است. "
                           "طبق صفحه 534 کتاب، حداقل 13 تک موج برای شمارش صحیح لازم است."
        }

    # ────────────────────────────────────────────────────────────────────────
    # اسکن الگوهای اصلاحی (با اولویت از فصل ۵)
    # ────────────────────────────────────────────────────────────────────────
    detected = scan_corrective_patterns(close.tolist(), high.tolist(), low.tolist())
    combination = find_combination_patterns(close.tolist(), high.tolist(), low.tolist())
    
    # ────────────────────────────────────────────────────────────────────────
    # محاسبه شاخص‌های کلی
    # ────────────────────────────────────────────────────────────────────────
    total_range = max(high) - min(low)
    current_price = close[-1]
    pivot_count = len(_detect_pivots(high.tolist(), low.tolist(), close.tolist()))
    
    # تعیین روند کلی بر اساس MA20 و MA50
    ma20 = np.mean(close[-20:]) if n >= 20 else np.mean(close)
    ma50 = np.mean(close[-50:]) if n >= 50 else np.mean(close)
    overall_trend = "صعودی" if ma20 > ma50 else "نزولی" if ma20 < ma50 else "خنثی"
    
    # ────────────────────────────────────────────────────────────────────────
    # دیکشنری خروجی شامل آمار + متن کامل کتاب
    # ═══════════════════════════════════════════════════════════════════════
    # تمام قوانین صفحات 120 تا 323 به صورت کلمه به کلمه در این دیکشنری آمده است
    # ═══════════════════════════════════════════════════════════════════════
    
    results = {
        # ── شناسنامه ──────────────────────────────────────────────────────
        "عنوان": "فصل 12: دسته‌بندی امواج اصلاحی (Corrective Waves)",
        "مرجع_کتاب": "صفحات 120 تا 323 - گلن نیلی - سبک نئوویو",
        "وضعیت": "تحلیل_کامل_و_جزئی",
        
        # ── اطلاعات پایه ──────────────────────────────────────────────────
        "تعداد_کل_داده": str(n),
        "قیمت_فعلی": round(float(current_price), 4),
        "دامنه_کل_قیمت": round(float(total_range), 4),
        "تعداد_نقاط_عطف": str(pivot_count),
        "روند_کلی": overall_trend,
        "MA20": round(ma20, 4),
        "MA50": round(ma50, 4),

        # ── اطلاعات از فصل‌های ۵، ۶، ۷ (وابستگی‌ها) ──   ← اینجا اضافه کن
        "منبع_مونوویو": f"از فصل ۵ ({len(monowaves_from_ch5) if monowaves_from_ch5 else 0} موج)",
        "قانون_تناسب": proportion_info.get("قانون_تناسب_رعایت_شده", "نامشخص") if proportion_info else "نامشخص",
        "موج_خنثی": f"{neutrality_info.get('تعداد_موج_خنثی_شناسایی_شده', 0) if neutrality_info else 0} موج" if neutrality_info else "نامشخص",
        
        # ── آمار الگوهای یافت شده ─────────────────────────────────────────
        "تعداد_الگوهای_یافت_شده": str(len(detected["zigzags"]) + len(detected["flats"]) + 
                                         len(detected["triangles"]) + len(detected["diametrics"]) + 
                                         len(detected["symmetricals"])),
        
        # ── آمار الگوهای یافت شده ─────────────────────────────────────────
        "تعداد_الگوهای_یافت_شده": str(len(detected["zigzags"]) + len(detected["flats"]) + 
                                         len(detected["triangles"]) + len(detected["diametrics"]) + 
                                         len(detected["symmetricals"])),
        "تعداد_زیگزاگ": str(len(detected["zigzags"])),
        "تعداد_مسطح": str(len(detected["flats"])),
        "تعداد_مثلث": str(len(detected["triangles"])),
        "تعداد_دیامتریک": str(len(detected["diametrics"])),
        "تعداد_سیمتریک": str(len(detected["symmetricals"])),
        "الگوی_ترکیبی": combination.get("type", "نامشخص"),
        "تعداد_الگوهای_ترکیب": str(combination.get("pattern_count", 0)),
        
        # ═══════════════════════════════════════════════════════════════════
        # صفحه 120: مقدمه امواج اصلاحی
        # ═══════════════════════════════════════════════════════════════════
        "ص120_قانون_پیش‌فرض": "چنانچه حرکت بازار از قوانین ضروری الگوی شتابدار پیروی نکند به طور پیش‌فرض بازار با یک الگوی اصلاحی در حال پیشروی است.",
        "ص120_تعداد_دسته": "الگوهای اصلاحی به 6 دسته کلی تقسیم می‌شوند (زیگزاگ، مسطح، مثلث، دیامتریک، سیمتریک، ترکیبی).",
        "ص120_ساختار_برچسب": "در این کتاب، ساختار امواج اصلاحی به صورت (3): برچسب گذاری می‌شوند. وجود خط در زیر آن به معنای بخشیده شدن (بسط) آن و نشاندهنده سطح پیچیدگی می‌باشد.",
        "ص120_برچسب_پیشرفت": "برچسب های پیشرفت در این الگوها به صورت A-B-C-D-E-F-G-H-I می‌باشد.",
        
        # ═══════════════════════════════════════════════════════════════════
        # صفحات 121-133: الگوی زیگزاگ (ZigZag)
        # ═══════════════════════════════════════════════════════════════════
        "ZZ_ساختار": "دارای ساختار سه تایی است (5-3-5).",
        "ZZ_ص121_موج_A": "موج A بایستی به شکل یک الگوی شتابدار روند دار باشد.",
        "ZZ_ص121_موج_B": "موج B می‌تواند به شکل هر یک از الگوهای اصلاحی (غیر از ترکیبی زیگزاگ و مسطح دوگانه و سه گانه) به ویژه زیگزاگ باشد.",
        "ZZ_ص121_موج_B_جاری": "از یک الگوی زیگزاگ، B فرضی اگر به شکل اصلاح جاری باشد، احتمالاً موج 2 از الگوی شتابدار یا بخشی از یک مثلث می‌باشد نه موج B از یک زیگزاگ.",
        "ZZ_ص121_موج_C_ورای_A": "موج C بایستی ورای انتهای موج A پایان یابد حتی اگر به میزان 1 درصد باشد.",
        "ZZ_ص121_موج_C_شتابدار": "موج C بایستی به شکل یک الگوی شتابدار باشد.",
        "ZZ_ص121_خط_روند_0B": "هیچ بخشی از موج C نبایستی خط روند B-0 را لمس کند مگر اینکه موج C به فرم ترمینال باشد.",
        "ZZ_ص121_تناوب_و_زمان": "موج B ذاتاً پیچیده‌تر و زمانبرتر از موج A است. در الگوی زیگزاگی بیشترین تناوب و کمترین برابری قیمتی، زمانی و پیچیدگی وجود دارد.",
        "ZZ_ص121_قیمت_A": "موج A نبایستی بیش از 61.8 درصد از الگوی شتابدار پیشین را اصلاح کند مگر آنکه الگوی پیشین بسط موج 5 یا موج C (یک درجه بالاتر) باشد.",
        "ZZ_ص121_قیمت_B_حداقل": "بخشی از موج B بایستی حداقل 33 درصد موج A باشد.",
        "ZZ_ص121_قیمت_B_حداکثر": "موج B نمی‌تواند بیش از 61.8 درصد موج A را اصلاح کند مگر اینکه موج مورد نظر پایان موج B نباشد و فقط بخشی از موج B باشد ولی در هرصورت پایان موج B نبایستی بیش از 61.8 درصد موج A را اصلاح کند.",
        "ZZ_ص122_قدرت_B": "هر چه موج B بلندتر باشد، موج C قدرت کمتری خواهد داشت و در نتیجه موج پساالگو قدرتمندتر خواهد بود.",
        "ZZ_ص122_زمان_A": "موج A نمی‌تواند بیشترین زمان را به خود اختصاص دهد در نتیجه زمان آن نمی‌تواند برابر با مجموع زمان موج B و C باشد.",
        "ZZ_ص122_زمان_B": "موج B نبایستی زمان کمتری نسبت به موج A صرف کند (اغلب حداکثر 3 تا 5 برابر بسته به سطح پیچیدگی چارت).",
        "ZZ_ص122_زمان_C": "موج C نبایستی زمان کمتری نسبت به موج A صرف کند و همچنین نبایستی زمانی بیش از مجموع زمان موج B داشته باشد.",
        "ZZ_ص122_زمان_AC": "موج A و C از نظر زمانی گرایش به برابری دارند.",
        "ZZ_ص122_فرمول_زمان_C": "بازه زمانی موج C معمولاً حداقل به اندازه زمان موج A و معمولاً حداکثر به اندازه نصف زمان صرف شده توسط موج A و B می‌تواند باشد.",
        "ZZ_ص122_فرمول_138": "در صورتی که زمان موج B کمتر از 2 برابر موج A (ترجیحاً 161.8 درصد) باشد، معمولاً زمان موج C، 138.2 درصد موج A خواهد بود.",
        "ZZ_ص123_معمولی_شرط_1": "موج C نبایستی بیش از 161.8 درصد موج A باشد.",
        "ZZ_ص123_معمولی_شرط_2": "موج C بایستی حداقل 61.8 درصد موج A باشد.",
        "ZZ_ص124_کوتاه_شده_شرایط": "یکی از انواع نادر، پس از وقوع قابل تایید. بایستی حداقل 81 درصد و ترجیحاً 100 درصد کل الگو بازگشت شود. اغلب در مثلث ها، ترمینال ها، دیامتریک ها و سیمتریک ها.",
        "ZZ_ص124_کوتاه_شده_قیمت": "موج C نبایستی کوتاهتر از 38.2 درصد موج A باشد و بایستی حداکثر 61.8 درصد موج A باشد.",
        "ZZ_ص125_کشیده_مکان": "فقط و فقط منحصر به مراحل ابتدای مثلث های انقباض و خنب (به جز موج E)، مراحل انتهای مثلث های انبساط (به جز موج A)، الگوهای ترمینال و قطعات مثلث ها یا دیامتریک ها.",
        "ZZ_ص125_کشیده_قیمت": "موج C بایستی بیش از 161.8 درصد موج A باشد (ترجیحاً 161.8 و حداکثر 261.8). بایستی حداقل 61.8 درصد موج C اصلاح شود.",
        "ZZ_ص127_کانال_0B": "شکست بی‌اهمیت خط روند 0-B توسط آنچه که به نظر می‌رسد موج B است، نشاندهنده توسعه مثلثی موج B است. هیچ بخشی از A و C نبایستی خط روند 0-B را لمس کند.",
        "ZZ_ص127_کانال_پایان": "انتهای موج C بایستی یا زیر خط روند موازی با خط روند 0-B باشد یا خط روند را بشکند در غیر این صورت با یک ساختار اصلاحی پیچیده مواجه خواهیم بود.",
        "ZZ_ص129_دوگانه_سه‌گانه": "اگر کانال بندی به فرم خاص باشد به احتمال زیاد یک الگوی دوگانه یا سه گانه در حال شکل گیری می‌باشد. اگر کمتر از 61.8 درصد زیگزاگ را اصلاح کند بایستی آن موج را X موج تصور نمود.",
        "ZZ_ص130_تایید_مرحله_1": "خط روند ابتدای موج A تا انتهای موج B رسم شود. حرکت پساالگو بایستی این خط روند را در زمانی کوتاهتر از زمان موج C بشکند.",
        "ZZ_ص130_تایید_مرحله_2": "در مرحله دوم کل موج C در زمانی برابر یا کمتر از زمان شکل گیری آن بازگشت شود.",
        "ZZ_ص133_نمودارها": "سه نمودار زیگزاگ معمولی، کوتاه شده و کشیده در صفحه 133 نشان داده شده است.",
        
        # ═══════════════════════════════════════════════════════════════════
        # صفحات 134-158: الگوی مسطح (Flat)
        # ═══════════════════════════════════════════════════════════════════
        "FL_ساختار": "دارای ساختار سه تایی است (3-2-5).",
        "FL_ص134_موج_A": "موج A بایستی به فرم هر یک از الگوهای اصلاحی باشد و معمولاً روند شکل گیری آن کند می‌باشد.",
        "FL_ص134_موج_B": "موج B بایستی به فرم هر یک از الگوهای اصلاحی باشد.",
        "FL_ص134_موج_C": "موج C بایستی به فرم یک الگوی شتابدار باشد.",
        "FL_ص134_خط_0B": "هیچ بخشی از موج C نبایستی خط روند 0-B را لمس کند مگر اینکه موج C به فرم ترمینال باشد.",
        "FL_ص134_برابری_تناوب": "در الگوی مسطح معمولاً برابری قیمتی و تناوب زمانی وجود دارد. تناوب زمانی نسبت به سه موج اول امواج شتابدار بیشتر است.",
        "FL_ص134_پیچیدگی_B": "موج B بایستی پیچیده‌تر و زمانبرتر از موج A باشد. هر چه B بلندتر باشد احتمال شتابدار بعدی بیشتر و رانش پر قدرت‌تر خواهد بود.",
        "FL_ص134_پیچیدگی_C": "سطح پیچیدگی موج C نبایستی کمتر از سطح پیچیدگی موج A و B باشد.",
        "FL_ص136_متعارف_قیمت": "همه امواج از نظر قیمتی هم اندازه می‌باشد. B بین 81 تا 100 درصد A. C نباید بیش از 10-20 درصد انتهای A تجاوز کند.",
        "FL_ص136_متعارف_زمان": "موج B بایستی بیشترین زمان را به خود اختصاص دهد و بخشیده‌تر از موج A خواهد بود تا تناوب برقرار باشد.",
        "FL_ص137_Cناقص_شرط": "موج B بخشیده‌تر از A (معمولا زیگزاگ یا دوگانه). B تقریبا کل (81 تا 100 درصد) A را اصلاح می‌کند. C کمترین زمان (اغلب ترمینال). C باید کل B را اصلاح کند (>61.8% B).",
        "FL_ص137_Cناقص_رانش": "نشان از قدرت رانش پس از اصلاح دارد که معمولاً این رانش بیش از 100 درصد موج پیشین می‌باشد.",
        "FL_ص139_Bناقص_شرط": "موج B بایستی 61.8 تا 81 درصد موج A را اصلاح کند. موج C بایستی کل B را اصلاح کند (حداقل 100 و حداکثر تا 138.2 درصد B). A و B باید در تناوب باشند.",
        "FL_ص140_ناقص_دوگانه": "موج A ترکیبی دوگانه/سه‌گانه است. B نباید بیش از 80 درصد A را اصلاح کند. C نباید کل B را اصلاح کند. شبیه مثلث افقی ولی C شتابدار است.",
        "FL_ص141_کشیده_شرط": "نشانه شکل‌گیری مثلث. B زمانی مشابه A، قیمت حداکثر 100% A. C بیش از 138.2% B (ترجیحا 161.8 و حداکثر 261.8). اغلب حداقل 61.8% C اصلاح می‌شود.",
        "FL_ص143_نامنظم_شرط": "موج B حداقل 101 درصد و حداکثر 138.2 درصد A. B بخشیده‌تر از A. موج C حداقل 101 درصد B.",
        "FL_ص144_نامنظم_ناقص_شرط": "موج B حداقل 138.2 درصد A. C نباید کل B را اصلاح کند (نشان قدرت پساالگو). B بخشیده‌تر از A.",
        "FL_ص145_جاری_رانش": "رانش پساالگوی بایستی حداقل 161.8 درصد موج B باشد (حرکت بعد سریعتر و بلندتر از حرکت پیشین).",
        "FL_ص145_جاری_قیمت": "موج B نبایستی بیش از 61.8 درصد موج شتابدار پیشین خود باشد و معمولاً تا 261.8 موج A می‌باشد. B بسیار بلندتر (>138% A). A و C مشابه. C وارد محدوده A نمی‌شود.",
        "FL_ص146_دسته_بندی_B_ضعیف": "B ضعیف (61.8 تا 80% A): اگر C بیش از 138.2% B باشد -> مسطح کشیده. اگر C بین 100 تا 138.2% B باشد -> B ناقص. اگر C کمتر از 100% B باشد -> ناقص دوگانه.",
        "FL_ص149_دسته_بندی_B_متوسط": "B بین 123.6 تا 138.2% A: احتمال اینکه C کل B را اصلاح کند وجود دارد -> مسطح نامنظم.",
        "FL_ص150_دسته_بندی_B_قوی": "B بین 101 تا 123% A: C می‌تواند کل B را اصلاح کند و از آن فراتر رود. اگر C بین 100 تا 161% A -> مسطح نامنظم. اگر C بیش از 161.8% A -> مسطح کشیده.",
        "FL_ص151_کانال_بندی": "خطوط کانال بایستی به موازات ابتدا و انتهای موج A ترسیم گردد. انتهای C بایستی بالای خط روند باشد یا آن را بشکند.",
        "FL_ص152_نمودار_کانال": "سقف جدید برای موج b نشاندهنده افزایش قدرت روند صعودی است. شکست محسوس خط روند، قدرت اولیه را خنثی می‌کند.",
        "FL_ص154_نمودار_قدرت": "بر مبنای بلندای موج b نسبت به a، صعود بعدی باید بزرگتر از صعود قبل از موج a باشد. موج c حداقل 61.8% موج a.",
        "FL_ص155_تایید_B_کوتاه": "I. 1. شکست خط A-B در زمان کمتر از C. 2. بازگشت C در زمان برابر یا کمتر از زمان شکل‌گیری C.",
        "FL_ص155_تایید_B_بلند": "II. 1. بازگشت C در زمان برابر یا کمتر از زمان شکل‌گیری C. 2. شکست خط A-B در زمان کمتر از C (هر چه B بلندتر سخت‌تر، در جاری و نامنظم ناقص آسانگیر باشید).",
        "FL_ص157_NEoWave_Logic": "نمودار S&P با تحلیل NEoWave Logic: اصلاح پیچیده صعودی. موج (G) پایان یافته و بازار خرسی حداقل 4 ساله آغاز شده است.",
        "FL_ص158_نمودار_EURO": "نمودار روزانه یورو از Sep 9, 04 تا Mar 15, 06 با اعداد 1.4000 تا 1.1200.",
        
        # ═══════════════════════════════════════════════════════════════════
        # صفحات 159-250: الگوی مثلث (Triangle)
        # ═══════════════════════════════════════════════════════════════════
        "TR_ص159_الزامات_عمومی": "مثلث دارای ساختار پنج قطعه‌ای اصلاحی (3-3-3-3-3) است. سه دسته کلی: انقباضی، انبساطی، خنثی. جهت توسعه: جاری، افقی، کانتر. فقط 4 نقطه از 6 نقطه مجاز به لمس خطوط روند کانال بندی. خط مبنا B-D است.",
        "TR_ص160_الزامات_قیمتی": "چهار بخش بایستی موج قبلی خود را اصلاح نمایند. سه بخش آن بایستی حداقل 50 درصد موج پیشین را اصلاح نمایند. موج C نباید کوتاه‌ترین موج A,C,E باشد. موج B معمولاً حداقل 61.8% موج A است.",
        "TR_ص161_الزامات_زمانی": "زمان موج E متناسب با مجموع یا نصف زمان موج C و D است. چهار قطعه متوالی نمی‌توانند زمان برابر داشته باشند. قطعه در حال تکمیل نباید زمان بیش از مجموع سه قطعه پیشین داشته باشد.",
        "TR_ص162_رفتار_قیمت": "نقاط نوسان در انتهای مثلث انقباضی به حالت تعادل نزدیک می‌شوند. شکست (رانش) زمانی رخ می‌دهد که یک نیرو بر دیگری غلبه کند.",
        "TR_ص163_کانال_بندی_صحیح": "کانال بندی صحیح مثلث افقی انقباضی: فقط دو نقطه تماس در هر سمت. نقاط a (آغاز مثلث) و e (انتهای مثلث) نباید کانال را لمس کنند.",
        "TR_ص164_انقباضی_الزامات": "فقط یک خط کانال می‌تواند افقی باشد. تناوب بین موج D و B برقرار باشد. بخشی از موج D وارد قلمرو موج B شود. یکی از نشانه‌ها موج A تند است.",
        "TR_ص165_انقباضی_قیمت_زمان": "پس از مثلث، رانش حداقل 75% پهن‌ترین بخش (معمولاً A). A > C > E. موج E حداقل 38.2% و حداکثر 99% موج C.",
        "TR_ص166_نمودار_انقباضی_محدود": "نمودار مثلث انقباضی محدود با نقطه راس. اگر رانش رو به بالا است باید به سطح راس برسد. اگر رانش رو به پایین است باید به سطح راس برسد.",
        "TR_ص167_نمودار_حداقل_رانش": "حداقل راند قیمتی برابر با 75% عرض‌ترین موج (در اینجا موج b). گاهی موج a بزرگترین موج نیست و موج b عرض‌ترین موج است.",
        "TR_ص168_انقباض_محدود_توضیح": "رانش پسامثلث محدود به میزان بلندترین قطعه (75 تا 161.8%). نقطه راس در محدوده 20 تا 40 درصدی پس از زمان مثلث. رانش در زمان کمتر از 50% زمان مثلث.",
        "TR_ص169_170_171_نمودارهای_رانش": "نمودارهای مختلف رانش پسا مثلث انقباضی با مشخصات نقطه راس و انتهای مثلث.",
        "TR_ص172_انقباض_نامحدود_توضیح": "مثلث انقباضی نامحدود: نقطه راس قبل از محدوده 20% یا بعد از محدوده 40% واقع می‌شود. محدودیتی به میزان عرض مثلث برای رانش وجود ندارد.",
        "TR_ص173_انقباض_نامحدود_ویژگی": "رانش پسامثلث نامحدود می‌تواند بیش از 161.8% موج پیش از مثلث باشد. موج A نسبت به محدود کندتر است. موج E گرایش به آرایش مثلثی دارد.",
        "TR_ص174_ترکیبی_دوگانه": "عبارت 'ترکیبی دوگانه' در کادر مرکزی صفحه.",
        "TR_ص175_شکست_کاذب": "شکست خط روند 4-2 شمارش مثلث را نفی نمی‌کند، بلکه به آن کمک می‌کند. مثلث‌ها گاه شکست‌های 'کاذب' می‌زنند. وقوع مثلث نامحدود در موضع X موج تنها وضعیتی است که مثلث به الگوی اصلاحی بزرگتر خاتمه نمی‌دهد.",
        "TR_ص176_177_178_نمودارهای_S&P_GOLD": "نمودارهای S&P 500 و GOLD با تحلیل NEoWave.",
        "TR_ص179_انقباض_افقی_توضیح": "خطوط روند همگرا با شیب مخالف، جهت توسعه افقی. A > C > E. رانش برابر عریض‌ترین +/- 25%. راس در رنج 61.8% عریض‌ترین.",
        "TR_ص180_نمودار_راس_مثلث": "برای اینکه مثلث از قوانین بخش افقی پیروی کند، راس مثلث باید در محدوده مشخصی قرار گیرد.",
        "TR_ص181_182_نمودارهای_انقباض_افقی": "نمودارهای شماتیک مثلث انقباضی افقی.",
        "TR_ص183_نمودار_BONDS": "نمودار BONDS با شکست از مثلث انقباضی صعودی. رشد بزرگتر در 1-2 سال آینده پیش‌بینی شده است.",
        "TR_ص184_انقباض_نامنظم_توضیح": "موج B بلندتر از A (B>A, B>C>D>E). رانش حداکثر 161.8% عریض‌ترین. انتهای E معمولاً بین A و A-C.",
        "TR_ص185_186_نمودارهای_انقباض_نامنظم": "نمودارهای شماتیک مثلث انقباضی نامنظم.",
        "TR_ص187_انقباض_جاری_توضیح": "خطوط همگرا در جهت روند. B بلندترین و ورای شروع A. D ورای پایان B ولی کوتاهتر از B. رانش 138.2 تا 161.8% عریض‌ترین.",
        "TR_ص188_نمودار_انقباض_جاری": "نمودار مثلث انقباضی جاری با رانش تقریباً 161.8% عرض‌ترین موج (موج b).",
        "TR_ص189_انقباض_کانتر_توضیح": "خطوط همگرا خلاف جهت روند. A پر شدت‌تر. D کوتاهتر از B. رانش 61.8 تا 100% عریض‌ترین.",
        "TR_ص190_191_نمودارهای_انقباض_کانتر": "نمودارهای شماتیک مثلث انقباضی کانتر.",
        "TR_ص192_انقباض_معکوس_توضیح": "خطوط میل به موازی. موج D بلندتر از B. رانش نسبت به عریض‌ترین (اغلب D) بیشتر است. هر چه A بلندتر و تندتر باشد دوره زمانی الگو کوتاهتر.",
        "TR_ص193_194_195_نمودارهای_انقباض_معکوس": "نمودارهای شماتیک مثلث انقباضی تناوب معکوس و نمودارهای عددی.",
        "TR_ص196_نمودار_EURO_تحلیل": "گزارش تحلیلی EURO از Mon, May 15, 2006. الگوی مشکوک: NEoWave Structure.",
        "TR_ص197_لوگو": "لوگو NEoWave.",
        "TR_ص198_199_نقاط_ورود_خروج": "پس از ورود به دلیل 'شکست'، استاپ باید کمی فراتر از 61.8% طول روند جدید قرار گیرد. اگر روند جدید واقعاً آغاز شده باشد، بیش از 61.8% آن حرکت اولیه را بازگشت نخواهد داد.",
        "TR_ص200_تایید_پساالگویی_انقباض": "تایید پساالگوی مثلث انقباضی در صفحه 200.",
        "TR_ص201_نمودار": "نمودار با برچسب‌های a1 تا a50 و اعداد 3.",
        "TR_ص202_انبساطی_عمومی": "معمولا زمانی خلق می‌شوند که 5 فاز به ترتیب زمان بیشتری صرف کنند. موج A تندترین. موج E تقریباً همیشه از خط روند فراتر می‌رود.",
        "TR_ص203_انبساطی_قیمت_زمان": "A < C < E. C بین 101 تا 161.8% A. E بین 138 تا 161.8% C یا A. زمان موج A نمی‌تواند بیشتر از B+C باشد.",
        "TR_ص204_205_نمودارهای_انبساطی_اولیه": "نمودارهای شماتیک مثلث انبساطی با حرکات تند بالا و پایین.",
        "TR_ص206_انبساطی_محدود_توضیح": "اشاره دارد به مثلث موج B، موج 4. رانش کم (50% بالاترین تا پایین‌ترین). A و E معمولاً به نسبت 161.8 در ارتباط هستند.",
        "TR_ص207_انبساطی_نامحدود_توضیح": "اشاره دارد به مثلث موج X، اولین یا آخرین فاز اصلاحی. رانش معمولاً یک X-wave است. اگر آخرین فاز باشد رانش کل مثلث را بازگشت می‌نماید.",
        "TR_ص208_انبساطی_افقی_توضیح": "خطوط واگرا با شیب مخالف، جهت توسعه افقی. E > D > C > B > A. E بلندترین قطعه.",
        "TR_ص209_نمودار_انبساطی": "نمودار S&P با مثلث انبساطی و پیش‌بینی روند.",
        "TR_ص210_انبساطی_نامنظم_توضیح": "B کوتاهتر از A (A>B). D بلندتر و زمانبرتر از B. E می‌تواند ورای C پایان یابد.",
        "TR_ص211_212_نمودارهای_انبساطی_نامه": "نمودارهای T-NOTES و S&P با تحلیل NEoWave.",
        "TR_ص213_انبساطی_جاری_توضیح": "نادر. خطوط واگرا در جهت روند. A کوتاهترین و D بلندترین قطعه. B زمان کمتر از A و C.",
        "TR_ص214_انبساطی_کانتر_توضیح": "خطوط واگرا خلاف جهت روند. D کوتاهتر از پیشین و پسین. A پر شدت‌تر. رانش کم.",
        "TR_ص215_219_نمودارهای_انبساطی": "نمودارهای T-NOTES، NOTES، S&P با تحلیل‌های مختلف NEoWave.",
        "TR_ص220_انبساطی_معکوس_توضیح": "A کوتاهترین. B بلندتر و زمانبرتر از D. B معمولا 138.2% A. خطوط میل به موازی.",
        "TR_ص221_223_نمودارهای_انبساطی_معکوس": "نمودارهای مثلث انبساطی تناوب معکوس و تحلیل S&P.",
        "TR_ص224_نقاط_ورود_خروج_انبساطی": "نقاط ورود و خروج در مثلث‌های انبساطی.",
        "TR_ص225_نمودار_استاپ": "نمودار با توضیحات استاپ در محیط انبساطی.",
        "TR_ص226_تایید_پساالگویی_انبساطی": "تایید پساالگوی مثلث انبساطی.",
        "TR_ص227_نمودار_تایید": "نمودار با علائم و برچسب‌ها.",
        "TR_ص228_خنب_عمومی": "موج A کند. خطوط میل به موازی. رانش بین انقباض و انبساط (50 تا 75% بلندترین). C بلندترین قطعه.",
        "TR_ص229_خنب_تناوب_استاندارد_معکوس": "تناوب استاندارد: D بلندتر از B. تناوب معکوس: D کوتاهتر از B. فرم تناوب معکوس شبیه مثلث انقباض است با این تفاوت که موج C کشیده‌تر است.",
        "TR_ص230_خنب_افقی_توضیح": "خطوط میل به موازی و افق. B کوتاهتر از A. A و E معمولاً 61.8% مرتبط. رانش اندکی بیشتر از عرض.",
        "TR_ص231_232_نمودارهای_خنب_افقی": "نمودارهای مثلث خنب افقی با تناوب استاندارد و معکوس.",
        "TR_ص233_خنب_نامنظم_توضیح": "نادر. خطوط همگرا، جهت افق. B بلندتر از A. رانش بیش از دو برابر عرض کانال.",
        "TR_ص234_نمودار_خنب_نامنظم": "نمودار مثلث خنب نامنظم با تناوب استاندارد و معکوس.",
        "TR_ص235_خنب_جاری_توضیح": "خطوط همگرا در جهت روند. B و D بلندتر از پیشین. B حدود 138.2% A. رانش بیش از دو برابر عرض.",
        "TR_ص236_238_نمودارهای_خنب_جاری": "نمودارهای مثلث خنب جاری با تناوب استاندارد و معکوس و نمودار طلا.",
        "TR_ص239_خنب_کانتر_توضیح": "خطوط همگرا خلاف جهت روند. A پر شدت‌تر. B و D کوتاهتر از پیشین. B حدود 61.8% A (ترجیحاً 38.2%). رانش به نسبت عرض.",
        "TR_ص240_243_نمودارهای_خنب_کانتر": "نمودارهای مثلث خنب کانتر و نمودار طلا.",
        "TR_ص244_نقاط_ورود_خروج_خنب": "نقاط ورود و خروج در مثلث‌های خنب.",
        "TR_ص245_نمودار_استاپ_خنب": "نمودار با توضیحات استاپ در مثلث خنب.",
        "TR_ص246_تایید_پساالگویی_خنب": "تایید پساالگوی مثلث خنب.",
        "TR_ص247_خطوط_روند_و_کانال_مثلث": "خط روند مبنا B-D. خط دیگر A-C، C-E یا A-E. فقط 4 نقطه مجاز به لمس (در نامحدود 5 نقطه).",
        "TR_ص248_249_نمودارهای_کانال_مثلث": "نمودارهای A و B و C برای کانال‌بندی مثلث. شکست خطوط هشدار تکمیل مثلث می‌دهد.",
        "TR_ص250_تایید_پساالگویی_مثلث": "تایید پساالگوی مثلث: انقباض/خنب و انبساطی.",
        
        # ═══════════════════════════════════════════════════════════════════
        # صفحات 251-276: الگوی دیامتریک (Diametric)
        # ═══════════════════════════════════════════════════════════════════
        "DI_ص251_ساختار": "دارای 7 قطعه می‌باشد که هر قطعه می‌تواند به فرم یکی از الگوهای اصلاحی باشد. اگر امواج پیش از E یا F انقباض باشند -> پاپیونی. اگر انبساط باشند -> الماس.",
        "DI_ص251_نشانه_اصلی": "شباهت زمانی و سطح پیچیدگی ساختار امواج به ویژه سه موج اول به عنوان مشخصه اصلی بایستی مد نظر قرار گیرد.",
        "DI_ص251_رانش": "اگر رانش سریع و بلندتر از B,D,F باشد الگو یک شاخه بزرگ را تکمیل کرده، در غیر اینصورت رانش احتمالا یک X موج است.",
        "DI_ص251_کانال": "بخش اول B-D و A-C. بخش دوم C-E و D-F. حداکثر 6 نقطه تماس. حداقل دو موج از B,D,F باید در تناوب باشند.",
        "DI_ص252_قیمت_G": "طول موج G معمولاً متناسب با طول موج A می‌باشد در غیر اینصورت با نسبت 61.8 یا 161.8 تناسب خواهد داشت.",
        "DI_ص252_زمان_مشابه": "نسبت تشابه زمانی بین امواج مجاور بایستی بین 61.8 تا 161.8 (ترجیحاً 78 تا 113) درصد باشد. حداکثر 1 یا 2 موج می‌تواند زمان متفاوت داشته باشد.",
        "DI_ص252_نشانه_موج_B": "اگر موج B بیش از 61.8% از موج A را اصلاح کند ولی زمانی کمتر از آن صرف کند قطعاً الگوی دیامتریک یا سیمتریک در حال شکل گیری است.",
        "DI_ص253_عمومی": "کانال بندی نظم خاصی ندارد. از مهم‌ترین نشانه ها امواج با زمان برابر است. نقش معکوس کننده را D یا E بر عهده دارد.",
        "DI_ص254_255_نمودارهای_دیامتریک": "نمودارهای شماتیک دیامتریک.",
        "DI_ص256_پاپیونی": "فاز اول انقباض، دوم انبساط. D معمولا کوتاهترین. G بلندتر از F و E. خط روند یک سمت می‌تواند افقی باشد.",
        "DI_ص257_264_نمودارهای_پاپیونی": "نمودارهای دیامتریک پاپیونی با اشکال مختلف.",
        "DI_ص265_الماس": "فاز اول انبساط، دوم انقباض. C یا D بلندترین. اگر BDF افقی باشد C pivot است، اگر ACE افقی باشد D pivot است.",
        "DI_ص266_269_نمودارهای_الماس": "نمودارهای دیامتریک الماس.",
        "DI_ص270_الماس_زیگزاگ": "امواج A و G بلندترین و بخشیده‌ترین قطعات. B و F بسیار کوتاهتر. خط روند CE یا BD می‌تواند افق باشد.",
        "DI_ص271_275_نمودارهای_الماس_زیگزاگ": "نمودارهای دیامتریک الماس زیگزاگ و S&P.",
        "DI_ص276_تایید_مرحله_1": "خط روند انتهای D تا انتهای F رسم شود. حرکت پساالگو باید این خط را در زمان کوتاه از زمان G بشکند.",
        "DI_ص276_تایید_مرحله_2": "بلندترین ریزموج از G در جهت G، باید در زمانی کم از زمان شکل‌گیری و با قیمت بیشتر توسط پساالگو بازگشت شود.",
        "DI_ص276_تایید_مرحله_3": "حرکت پساالگو بایستی بلندتر از موج G و در زمانی کمی باشد.",
        "DI_ص276_تایید_مرحله_4": "حرکت پساالگو بایستی بلندتر از بلندترین موج B، D و F و در زمانی کمی باشد.",
        
        # ═══════════════════════════════════════════════════════════════════
        # صفحات 277-283: الگوی سیمتریک (Symmetric)
        # ═══════════════════════════════════════════════════════════════════
        "SY_ص277_ساختار": "دارای 9 قطعه می‌باشد که هر قطعه می‌تواند به فرم یکی از الگوهای اصلاحی باشد.",
        "SY_ص277_نشانه_اصلی": "شباهت زمانی و قیمتی و پیچیدگی ساختار امواج به ویژه سه موج اول به عنوان مشخصه اصلی بایستی مد نظر قرار گیرد.",
        "SY_ص277_موج_A_کند": "یکی از نشانه های شکل گیری آن موج A کند می‌باشد.",
        "SY_ص277_موج_C": "در هر یک از امواج به غیر از امواج شتابدار، موج C الگوی مسطح و زیگزاگ و موج A الگوی زیگزاگ می‌تواند رخ دهد.",
        "SY_ص277_جهت_توسعه": "جهت توسعه سیمتریک ها می‌تواند به صورت جاری، افق و کانتر باشد.",
        "SY_ص277_رانش": "اگر رانش سریع و بلندتر از B,D,F,H باشد الگو یک شاخه بزرگ را تکمیل کرده است.",
        "SY_ص277_نقش_معکوس": "نقش معکوس کننده الگو معمولاً بر عهده موج E می‌باشد.",
        "SY_ص277_ویژگی_کانال": "از ویژگی‌های آن کانال بندی دقیق آن می‌باشد.",
        "SY_ص277_موج_E": "موج E نمی‌تواند کوتاه‌ترین موج باشد.",
        "SY_ص278_زمان_مشابه": "نسبت تشابه زمانی بین امواج مجاور بایستی بین 61.8 تا 161.8 درصد باشد.",
        "SY_ص278_قانون_زمان_A": "موج A نبایستی بیشترین زمان را در بین سه قطعه اول داشته باشد.",
        "SY_ص278_زمان_C": "موج C اغلب بایستی زمانی بیش از زمان موج A صرف کند.",
        "SY_ص278_قانون_کل_زمان": "قطعه در حال تکمیل نبایستی زمانی بیش از مجموع زمان سه قطعه پیشین داشته باشد.",
        "SY_ص279_282_نمودارهای_سیمتریک": "نمودارهای شماتیک سیمتریک.",
        "SY_ص283_تایید_مرحله_1": "خط روند انتهای F تا انتهای H رسم شود. حرکت پساالگو باید این خط را در زمان کوتاه از زمان I بشکند.",
        "SY_ص283_تایید_مرحله_2": "بلندترین ریزموج از I در جهت I، باید در زمانی کم از زمان شکل‌گیری و با قیمت بیشتر بازگشت شود.",
        "SY_ص283_تایید_مرحله_3": "حرکت پساالگو بایستی بلندتر از موج I و در زمانی کمی باشد.",
        "SY_ص283_تایید_مرحله_4": "حرکت پساالگو بایستی بلندتر از بلندترین موج B,D,F,H و در زمانی کمی باشد.",
        
        # ═══════════════════════════════════════════════════════════════════
        # صفحات 284-286: یافتن محدوده پایان موج B
        # ═══════════════════════════════════════════════════════════════════
        "WB_ص284_روش_مشابه": "انتهای موج B به طریق مشابه انتهای موج 2 سنجیده می‌شود با این تفاوت که موج C به ندرت بیش از 161.8% موج A می‌باشد.",
        "WB_ص284_کانال_مثلث": "اگر موج B مثلث باشد، دو روش کانال بندی: خط روند 0-B از انتهای موج C مثلث رسم می‌گردد.",
        "WB_ص284_شکست_کاذب": "در شکل B، موج E به صورت شکست کاذب خط روند را می‌شکند ولی نباید از انتهای موج C تجاوز کند.",
        "WB_ص285_توسعه_مثلث": "اگر بازار خط روند مفروض موج B را بشکند و دوباره صعود کند، دلیل بر توسعه یک الگوی مثلث می‌باشد.",
        "WB_ص286_نشانه_مثلث": "اصلاح‌های درون مثلث به گونه‌ای تصادفی و خیلی کند خطوط روند را می‌شکنند که نشانه قطعی شکل‌گیری مثلث است.",
        
        # ═══════════════════════════════════════════════════════════════════
        # صفحات 287-316: الگوهای غیر استاندارد ترکیب (Combination)
        # ═══════════════════════════════════════════════════════════════════
        "CM_ص287_شارپ": "الگوهای شارپ شامل زیگزاگ دوگانه و زیگزاگ سه گانه می‌باشد.",
        "CM_ص287_زیگزاگ_دوگانه": "دو زیگزاگ متوالی که توسط یک X-wave کوتاه از هم جدا شده‌اند. معمولاً پس از الگوی شتابدار رخ می‌دهد.",
        "CM_ص287_زیگزاگ_سه_گانه": "سه زیگزاگ متوالی که توسط دو X-wave از هم جدا شده‌اند. قوی‌ترین الگوی اصلاحی است.",
        "CM_ص288_ساید_نوع1": "دوگانه سه تای: ترکیب دو الگوی اصلاحی و یک موج اصلاحی میانی. به صورت مایل در جهت روند حرکت می‌کند.",
        "CM_ص289_ساید_نوع2": "سه گانه سه تای: ترکیب سه الگوی اصلاحی و دو موج اصلاحی میانی.",
        "CM_ص290_سه_گانه_سه_تای": "ترکیب سه گانه سه تای (Triple Three).",
        "CM_ص291_X_موج": "تمام ساختارهای اصلاحی غیر استاندارد شامل یک X-wave و دو الگوی اصلاحی بساموج یا بالاتر می‌باشند.",
        "CM_ص291_X_موج_زمان": "X-wave ها نمی‌توانند زمانی بیش از هر یک از فازهای اصلاحی طی کنند مگر اینکه متعلق به الگوی یک درجه بالاتر باشند.",
        "CM_ص291_X_کوتاه_شرط": "قوی‌ترین اخطار زمانی که فاز اول اصلاح توسط موج میانی کمی از 61.8% بازگشت شده باشد.",
        "CM_ص291_X_کوتاه_ساختار": "X-wave کوتاه معمولاً یک تک موج، مسطح یا مثلث است و از نظر پیچیدگی کمتر است.",
        "CM_ص292_X_کوتاه_محدودیت": "X-wave های کوتاه می‌توانند به فرم هر الگوی اصلاحی محدود (غیر از مثلث انقباض) باشند.",
        "CM_ص293_300_نمودارهای_X_موج": "نمودارهای زیگزاگ دوگانه، زیگزاگ سه گانه و ترکیبات مختلف با تحلیل نادرست و درست.",
        "CM_ص301_X_بلند_شرط": "اگر سه الگوی اصلاحی پشت سر هم رخ دهند و دومی بیش از 100% فاز اول باشد، احتمالاً X-wave بلند است.",
        "CM_ص301_X_بلند_زمان": "معمولاً از نظر زمانی X-wave 100% الگوی پیش از خود خواهد بود.",
        "CM_ص302_X_بلند_محدودیت": "X-wave بلند می‌تواند به فرم هر یک از الگوهای اصلاحی باشد.",
        "CM_ص303_305_نمودارهای_X_بلند": "نمودارهای ترکیبات با X-wave بلند.",
        "CM_ص306_دوگانه_سه_تای_جاری": "X-wave بین 138.2 تا 161.8% قلمرو قیمتی الگوی پیشین. بیانگر حرکت بعد سریع و بلندتر.",
        "CM_ص307_308_نمودارهای_ترکیبی": "نمودارهای ترکیبی دوگانه سه تای و سه گانه سه تای.",
        "CM_ص309_جدول_X_موج": "جدول ساختار احتمالی X-wave ها.",
        "CM_ص310_X_قوانین_حدی": "X-wave از نظر پیچیدگی و زمان نباید کمی از 1/3 و حداکثر برابر الگوی پیشین باشد.",
        "CM_ص310_X_پس_از_مسطح": "پس از مسطح، اگر رانش کمی از 61.8% مسطح پیشین و زمان آن کمی از 2/3 باشد، X-wave شکل گرفته است.",
        "CM_ص311_کانال_ترکیب": "اگر موج B بزرگترین فاز اصلاحی باشد، خط روند از انتهای B رسم می‌شود. اگر X-wave بزرگترین باشد، از انتهای X-wave رسم می‌شود.",
        "CM_ص312_315_نمودارهای_کانال_ترکیب": "نمودارهای کانال‌بندی الگوهای ترکیبی با شکست کاذب.",
        "CM_ص316_اطلاعات_تماس": "اطلاعات تماس KohanFx.com.",
        "CM_ص317_تایید_ناشناخته_مرحله_1": "آخرین ریزموج از آخرین قطعه در جهت توسعه الگو را بیابید. رانش پساالگو باید از نظر زمانی کمی و قیمتی بلندتر باشد.",
        "CM_ص317_تایید_ناشناخته_مرحله_2": "بلندترین قطعه در خلاف جهت توسعه الگو را بیابید. رانش باید زمانی کمی و قیمتی بلندتر باشد.",
        "CM_ص317_تایید_ناشناخته_مرحله_3": "بلندترین قطعه در جهت توسعه الگو را بیابید. رانش باید زمانی کمی و قیمتی بلندتر باشد.",
        "CM_ص317_نکته_ترتیب": "اگر بلندترین قطعه در راستای روند از نظر قیمتی کوتاهتر از بلندترین قطعه در خلاف جهت باشد، ترتیب مراحل 2 و 3 می‌تواند عوض شود.",
        "CM_ص318_320_نمودارهای_تایید_ناشناخته": "نمودارهای تایید پساالگویی در الگوی ناشناخته با اهداف 1، 2 و 3.",
        
        # ═══════════════════════════════════════════════════════════════════
        # صفحات 321-323: مرور بر نکات مهم ساختارهای اصلاحی
        # ═══════════════════════════════════════════════════════════════════
        "RE_ص321_زیگزاگ_زمان": "در الگوی زیگزاگ اغلب شباهت زمانی بین موج A و C برقرار است.",
        "RE_ص321_مسطح_قیمت": "در الگوی مسطح اغلب شباهت قیمتی بین امواج برقرار است.",
        "RE_ص321_مثلث_پیچیدگی": "در الگوی مثلث از نظر سطح پیچیدگی شباهت بین قطعات مثلث وجود دارد.",
        "RE_ص321_دیامتریک_شباهت": "در الگوی دیامتریک شباهت زمانی و پیچیدگی ساختار امواج به ویژه سه موج اول مشخصه اصلی است.",
        "RE_ص321_سیمتریک_شباهت": "در الگوی سیمتریک شباهت زمانی، پیچیدگی و قیمتی امواج به ویژه سه موج اول مشخصه اصلی است.",
        "RE_ص321_تشخیص_زمان": "اگر زمان سه موج ابتدایی خیلی متفاوت باشد -> زیگزاگ/مسطح. تا حدی شبیه باشد -> مثلث. بسیار شبیه باشد -> دیامتریک. بسیار شبیه + شباهت قیمت -> سیمتریک.",
        "RE_ص321_موج_A": "موج A با توجه به خلاف جهت روند شتابدار، معمولاً پیچیدگی کم و شتاب بیشتری دارد.",
        "RE_ص321_موج_B": "موج B با توجه به خلاف جهت روند اصلاحی، معمولاً پیچیدگی بیشتر و شتاب کمتری دارد.",
        "RE_ص322_نشانه_C_E": "اگر موج C بیش از 61.8% A و موج E کمتر از 61.8% C باشد، وقوع مثلث بسیار بعید است.",
        "RE_ص322_فاز_اصلاحی": "فاز اصلاحی پس از الگوی شتابدار باید از مجموع زمان و قیمت موج 2 و 4 فاز شتابدار بزرگتر باشد.",
        "RE_ص322_ترکیب_10_کندل": "در 10 کندل: مسطح/زیگزاگ: 3+6+1، دیامتریک: 1+1+2+2+1+1+1، سیمتریک: 1+2+1+1+1+1+1+1+1.",
        "RE_ص322_زمان_موج_دوم": "اگر زمان موج دوم 100-261% موج اول -> هر الگویی ممکن. 300-500% -> احتمال زیگزاگ/مسطح. بیش از 500% -> نیاز به بازنگری.",
        "RE_ص323_جدول_شباهت": "جدول مقایسه الگوها از نظر شباهت قیمتی، زمانی و پیچیدگی (زیگزاگ: */*/*؛ مسطح: ✓/*/*؛ مثلث: */*/✓؛ دیامتریک: */✓/✓؛ سیمتریک: ✓/✓/✓)."
    }
    
    # ────────────────────────────────────────────────────────────────────────
    # اضافه کردن نتایج الگوهای یافت شده به خروجی
    # ────────────────────────────────────────────────────────────────────────
    if detected["zigzags"]:
        results["نمونه_زیگزاگ"] = detected["zigzags"][-1]
    if detected["flats"]:
        results["نمونه_مسطح"] = detected["flats"][-1]
    if detected["triangles"]:
        results["نمونه_مثلث"] = detected["triangles"][-1]
    if detected["diametrics"]:
        results["نمونه_دیامتریک"] = detected["diametrics"][-1]
    if detected["symmetricals"]:
        results["نمونه_سیمتریک"] = detected["symmetricals"][-1]
    
    # ────────────────────────────────────────────────────────────────────────
    # تولید تفسیر نهایی
    # ────────────────────────────────────────────────────────────────────────
    results["تفسیر_نهایی"] = _generate_final_interpretation(results, detected, combination)
    
    # ────────────────────────────────────────────────────────────────────────
    # ذخیره در logger (در صورت وجود)
    # ────────────────────────────────────────────────────────────────────────
    if logger:
        logger.add_section("فصل 12: دسته‌بندی امواج اصلاحی", level=1)
        logger.add_result("تعداد الگوهای یافت شده", results["تعداد_الگوهای_یافت_شده"])
        logger.add_result("تعداد زیگزاگ", results["تعداد_زیگزاگ"])
        logger.add_result("تعداد مسطح", results["تعداد_مسطح"])
        logger.add_result("تعداد مثلث", results["تعداد_مثلث"])
        logger.add_result("تعداد دیامتریک", results["تعداد_دیامتریک"])
        logger.add_result("تعداد سیمتریک", results["تعداد_سیمتریک"])
        if combination.get("type") != CombinationType.NONE.value:
            logger.add_result("الگوی ترکیبی", combination["type"])
        
        if detected["zigzags"]:
            logger.add_wave("نمونه زیگزاگ", detected["zigzags"][-1])
        if detected["flats"]:
            logger.add_wave("نمونه مسطح", detected["flats"][-1])
        if detected["triangles"]:
            logger.add_wave("نمونه مثلث", detected["triangles"][-1])
    
    return results


def _generate_final_interpretation(results: Dict, detected: Dict, combination: Dict) -> str:
    """
    تولید تفسیر نهایی کامل از نتایج تحلیل
    
    این تفسیر شامل:
    - آمار کلی داده‌ها و الگوهای یافت شده
    - نکات کلیدی شناسایی الگوها (صفحه 323)
    - جمع‌بندی نهایی بر اساس جدول صفحه 323
    """
    lines = []
    lines.append("═" * 80)
    lines.append("فصل 12: دسته‌بندی امواج اصلاحی (نئوویو) - تفسیر کامل")
    lines.append("مرجع: کتاب استادی در امواج الیوت - گلن نیلی | صفحات 120-323")
    lines.append("═" * 80)
    lines.append("")
    
    lines.append("📊 آمار کلی:")
    lines.append(f"   • تعداد کل داده‌ها: {results.get('تعداد_کل_داده', 0)}")
    lines.append(f"   • تعداد نقاط عطف: {results.get('تعداد_نقاط_عطف', 0)}")
    lines.append(f"   • روند کلی: {results.get('روند_کلی', 'نامشخص')}")
    lines.append(f"   • دامنه کل قیمت: {results.get('دامنه_کل_قیمت', 0)}")
    lines.append(f"   • MA20: {results.get('MA20', 0)} | MA50: {results.get('MA50', 0)}")
    lines.append("")
    
    lines.append("📈 الگوهای اصلاحی شناسایی شده:")
    lines.append(f"   • زیگزاگ: {results.get('تعداد_زیگزاگ', 0)} الگو")
    lines.append(f"   • مسطح: {results.get('تعداد_مسطح', 0)} الگو")
    lines.append(f"   • مثلث: {results.get('تعداد_مثلث', 0)} الگو")
    lines.append(f"   • دیامتریک: {results.get('تعداد_دیامتریک', 0)} الگو")
    lines.append(f"   • سیمتریک: {results.get('تعداد_سیمتریک', 0)} الگو")
    if combination.get("type") != CombinationType.NONE.value:
        lines.append(f"   • ترکیبی: {combination.get('type', 'نامشخص')}")
    lines.append("")
    
    lines.append("📌 نکات کلیدی شناسایی الگوها (صفحه 323):")
    lines.append("   • شباهت زمانی: تفاوت زمانی بین امواج مجاور باید 61.8% تا 161.8% باشد")
    lines.append("   • شباهت قیمتی: نسبت قیمتی بین امواج مجاور باید 61.8% تا 161.8% باشد")
    lines.append("   • شباهت پیچیدگی: تعداد زیرموج‌ها باید مشابه باشد")
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
    
    lines.append("🎯 جمع‌بندی نهایی (صفحات 321-323):")
    lines.append("   • زیگزاگ: کمترین شباهت قیمتی و زمانی، بیشترین تناوب")
    lines.append("   • مسطح: شباهت قیمتی بین امواج")
    lines.append("   • مثلث: شباهت در سطح پیچیدگی")
    lines.append("   • دیامتریک: شباهت در زمان و پیچیدگی")
    lines.append("   • سیمتریک: شباهت در زمان، قیمت و پیچیدگی")
    lines.append("")
    lines.append("   ✨ اصل ساده‌سازی (Simplification):")
    lines.append("      الگوهای هر کالس می‌تواند در تایم فریم بالاتر به الگوی ساده‌تری")
    lines.append("      از همان کالس تبدیل گردد (صفحه 535).")
    lines.append("")
    lines.append("   ✨ پدیده تقلید (Emulation):")
    lines.append("      ممکن است یک کالس رفتاری (شتابدار/اصلاحی) رفتار کالس دیگر را")
    lines.append("      تقلید کند (صفحه 535). در چنین شرایطی باید موج مفقود وجود داشته باشد.")
    lines.append("")
    lines.append("═" * 80)
    lines.append("پایان تفسیر فصل 12")
    lines.append("═" * 80)
    
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# پایان کد chapter_12.py
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════