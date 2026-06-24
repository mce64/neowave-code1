# chapters/chapter_11.py

"""
فصل ۱۱: دسته‌بندی امواج شتابدار (Impulse Waves Classification)
منبع: کتاب "استادی در امواج الیوت" - گلن نیلی - صفحات ۵۵ تا ۱۱۹

═══════════════════════════════════════════════════════════════════
متن دقیق کتاب (صفحه ۵۵):

"امواج شتابدار بر اساس میزان اصلاح موج ۳ توسط موج ۴ و همچنین ساختار 
داخلی امواج به دو دسته کلی تقسیم می‌شوند:
  - شتابدار روند دار (Trending Impulse)
  - شتابدار ترمینال (Terminal Impulse)
در امواج شتابدار روند دار، هیچ بخشی از موج ۴ نمی‌تواند وارد قلمرو 
(کمترین یا بیشترین قیمت) موج ۲ شود.
در امواج شتابدار ترمینال، این همپوشانی الزاماً بایستی وجود داشته باشد."

═══════════════════════════════════════════════════════════════════
دسته‌بندی کامل امواج شتابدار (صفحات ۵۵ تا ۱۱۹):

۱. شتابدار روند دار ساده (Simple Trending Impulse) - صفحه ۵۹
۲. شتابدار روند دار با موج ۱ ممتد (1st Extension Trending) - صفحه ۶۱
۳. شتابدار روند دار با موج ۳ ممتد (3rd Extension Trending) - صفحه ۶۳
۴. شتابدار روند دار با موج ۵ ممتد (5th Extension Trending) - صفحه ۶۷
۵. شتابدار روند دار با امتداد دوگانه (Double Extension Trending) - صفحه ۷۰
۶. شتابدار روند دار با موج ۵ کوتاه شده (Truncated Trending) - صفحه ۷۳
۷. الگوی قطری پیشرو (Leading Diagonal) - صفحه ۷۶
۸. شتابدار ترمینال ساده (Simple Terminal) - صفحه ۷۸
۹. شتابدار ترمینال با موج ۱ ممتد (1st Extension Terminal) - صفحه ۷۹
۱۰. شتابدار ترمینال با موج ۳ ممتد (3rd Extension Terminal) - صفحه ۸۵
۱۱. شتابدار ترمینال با موج ۵ ممتد (5th Extension Terminal) - صفحه ۸۶
۱۲. شتابدار ترمینال با موج ۵ کوتاه شده (5th Failure Terminal) - صفحه ۸۹
═══════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


# ════════════════════════════════════════════════════════════════
# بخش ۱: تعاریف پایه و مدل‌های داده
# ════════════════════════════════════════════════════════════════

class ImpulseCategory(Enum):
    """دسته‌بندی کلی امواج شتابدار"""
    TRENDING = "شتابدار_روند_دار"
    TERMINAL = "شتابدار_ترمینال"
    LEADING_DIAGONAL = "قطری_پیشرو"
    UNKNOWN = "نامشخص"


class ImpulseSubType(Enum):
    """زیرنوع‌های امواج شتابدار"""
    SIMPLE = "ساده"
    EXT_1 = "موج_۱_ممتد"
    EXT_3 = "موج_۳_ممتد"
    EXT_5 = "موج_۵_ممتد"
    DOUBLE_EXT = "امتداد_دوگانه"
    TRUNCATED = "موج_۵_کوتاه_شده"
    LEADING_DIAG = "قطری_پیشرو"
    TERMINAL_SIMPLE = "ترمینال_ساده"
    TERMINAL_EXT_1 = "ترمینال_موج_۱_ممتد"
    TERMINAL_EXT_3 = "ترمینال_موج_۳_ممتد"
    TERMINAL_EXT_5 = "ترمینال_موج_۵_ممتد"
    TERMINAL_TRUNCATED = "ترمینال_موج_۵_کوتاه_شده"
    NONE = "بدون_الگو"


@dataclass
class WavePoint:
    """نقطه قیمتی یک موج"""
    index: int
    price: float
    time: int  # ایندکس زمانی


@dataclass
class ImpulseWave:
    """ساختار یک الگوی شتابدار ۵ موجی"""
    w0: WavePoint
    w1: WavePoint
    w2: WavePoint
    w3: WavePoint
    w4: WavePoint
    w5: WavePoint
    
    # طول قیمتی امواج
    len_w1: float = 0.0
    len_w2: float = 0.0
    len_w3: float = 0.0
    len_w4: float = 0.0
    len_w5: float = 0.0
    
    # زمان امواج
    time_w1: int = 0
    time_w2: int = 0
    time_w3: int = 0
    time_w4: int = 0
    time_w5: int = 0


@dataclass
class ImpulseAnalysisResult:
    """نتیجه تحلیل یک الگوی شتابدار"""
    category: ImpulseCategory
    sub_type: ImpulseSubType
    has_overlap: bool
    extended_wave: Optional[int]  # 1, 3, 5 یا None
    is_truncated: bool
    
    # نسبت‌های قیمتی
    ratio_w3_to_w1: float
    ratio_w5_to_w3: float
    ratio_w5_to_w1: float
    ratio_w2_ret_w1: float  # درصد اصلاح موج ۲ از موج ۱
    ratio_w4_ret_w3: float  # درصد اصلاح موج ۴ از موج ۳
    ratio_w5_ret_w4: float  # درصد بازگشت موج ۵ از موج ۴
    
    # نسبت‌های زمانی
    time_ratio_w2_to_w1: float
    time_ratio_w4_to_w3: float
    time_ratio_w5_to_w3: float
    
    # کانال‌بندی
    channel_type: str  # همگرا، واگرا، موازی، مگافون
    
    # قانون برابری (صفحه ۱۱۶)
    equality_ratio: float  # نسبت دو موج غیر ممتد
    equality_status: str   # برابر، نزدیک_برابر، نامتوازن
    
    # نقض قوانین
    violations: List[str]
    
    # وضعیت ساختار داخلی
    internal_structure_status: str  # بررسی_نشده، فرض_۵_۳_۵_۳_۵، فرض_۳_۳_۳_۳_۳
    
    # توصیف و تفسیر
    description: str
    page_reference: str


# ════════════════════════════════════════════════════════════════
# بخش ۲: کلاس تحلیل‌گر امواج شتابدار
# ════════════════════════════════════════════════════════════════

class ImpulseAnalyzer:
    """
    کلاس اصلی برای تحلیل و دسته‌بندی امواج شتابدار.
    
    مطابق صفحات ۵۵ تا ۱۱۹ کتاب:
        - تشخیص شتابدار روند دار vs ترمینال vs قطری پیشرو
        - شناسایی موج ممتد
        - بررسی قانون برابری
        - بررسی نقض قوانین زمانی و قیمتی
        - محاسبه نسبت‌های فیبوناچی
        - بررسی کانال‌بندی
    """
    
    @staticmethod
    def calculate_wave_metrics(impulse: ImpulseWave) -> ImpulseWave:
        """محاسبه طول قیمتی و زمانی هر موج"""
        impulse.len_w1 = abs(impulse.w1.price - impulse.w0.price)
        impulse.len_w2 = abs(impulse.w2.price - impulse.w1.price)
        impulse.len_w3 = abs(impulse.w3.price - impulse.w2.price)
        impulse.len_w4 = abs(impulse.w4.price - impulse.w3.price)
        impulse.len_w5 = abs(impulse.w5.price - impulse.w4.price)
        
        impulse.time_w1 = impulse.w1.time - impulse.w0.time
        impulse.time_w2 = impulse.w2.time - impulse.w1.time
        impulse.time_w3 = impulse.w3.time - impulse.w2.time
        impulse.time_w4 = impulse.w4.time - impulse.w3.time
        impulse.time_w5 = impulse.w5.time - impulse.w4.time
        
        return impulse
    
    @staticmethod
    def check_overlap(impulse: ImpulseWave) -> bool:
        """
        بررسی همپوشانی موج ۴ با قلمرو موج ۲ (صفحه ۵۵)
        
        روند دار: هیچ بخشی از موج ۴ وارد قلمرو موج ۲ نمی‌شود
        ترمینال / قطری پیشرو: همپوشانی الزامی است
        """
        if impulse.w1.price < impulse.w3.price:  # روند صعودی
            w2_low = min(impulse.w1.price, impulse.w2.price)
            w4_low = min(impulse.w3.price, impulse.w4.price)
            return w4_low <= w2_low
        else:  # روند نزولی
            w2_high = max(impulse.w1.price, impulse.w2.price)
            w4_high = max(impulse.w3.price, impulse.w4.price)
            return w4_high >= w2_high
    
    @staticmethod
    def check_truncation(impulse: ImpulseWave) -> bool:
        """
        بررسی کوتاه‌شدگی موج ۵ (صفحه ۷۳)
        
        قله موج ۵ نمی‌تواند به ارتفاعی بالاتر از موج ۳ دست یابد.
        """
        if impulse.w1.price < impulse.w3.price:  # صعودی
            return impulse.w5.price < impulse.w3.price
        else:  # نزولی
            return impulse.w5.price > impulse.w3.price
    
    @staticmethod
    def identify_extended_wave(impulse: ImpulseWave) -> Optional[int]:
        """
        شناسایی موج ممتد بر اساس قانون امتداد (صفحه ۱۱۵)
        
        "موج ممتد بایستی ۱۶۱.۸ درصد موج بلند پیش از خود و یا 
         کوتاهترین موج از سه موج ۱، ۳ یا ۵ باشد."
        """
        lengths = [impulse.len_w1, impulse.len_w3, impulse.len_w5]
        max_len = max(lengths)
        min_len = min(lengths)
        
        # بررسی ۱۶۱.۸ درصدی
        for i, length in enumerate(lengths):
            if length == max_len:
                other_lengths = [l for j, l in enumerate(lengths) if j != i]
                if other_lengths:
                    if length >= 1.618 * max(other_lengths):
                        return i + 1  # 1, 2، یا 3
        
        # اگر هیچکدام ۱۶۱.۸ نبودند، بلندترین موج ممتد است
        # اصلاح: فقط موج‌های ۱، ۳ یا ۵ می‌توانند ممتد باشند
        if max_len == impulse.len_w1:
            return 1
        elif max_len == impulse.len_w3:
            return 3
        elif max_len == impulse.len_w5:
            return 5
        
        return None
    
    @staticmethod
    def calculate_equality(impulse: ImpulseWave, extended_wave: Optional[int]) -> Tuple[float, str]:
        """
        محاسبه قانون برابری (صفحه ۱۱۶)
        
        "دو موج غیر ممتد بایستی از نظر زمانی، قیمتی و یا سطح پیچیدگی 
         گرایش به برابری داشته باشند و با یک نسبت فیبوناچی (معمولاً ۶۱.۸) 
         در بعد زمان و یا قیمت با هم مرتبط باشند."
        """
        if extended_wave == 1:
            # قانون عطف به موج‌های ۳ و ۵
            if impulse.len_w5 > 0:
                ratio = impulse.len_w3 / impulse.len_w5
            else:
                ratio = 0.0
        elif extended_wave == 3:
            # قانون عطف به موج‌های ۱ و ۵
            if impulse.len_w5 > 0:
                ratio = impulse.len_w1 / impulse.len_w5
            else:
                ratio = 0.0
        elif extended_wave == 5:
            # قانون عطف به موج‌های ۱ و ۳
            if impulse.len_w3 > 0:
                ratio = impulse.len_w1 / impulse.len_w3
            else:
                ratio = 0.0
        else:
            ratio = 0.0
        
        # ارزیابی وضعیت برابری
        if 0.9 <= ratio <= 1.1:
            status = "برابر"
        elif 0.618 <= ratio <= 1.618:
            status = "نزدیک_برابر_فیبو"
        else:
            status = "نامتوازن"
        
        return ratio, status
    
    @staticmethod
    def check_trending_violations(impulse: ImpulseWave) -> List[str]:
        """
        بررسی نقض قوانین نقض‌ناپذیر شتابدار روند دار (صفحه ۵۶ و ۵۷)
        
        الزامات عمومی:
        - موج ۲ نمی‌تواند ۱۰۰٪ موج ۱ را اصلاح کند
        - موج ۴ نمی‌تواند ۱۰۰٪ موج ۳ را اصلاح کند
        - موج ۳ کوتاه‌ترین نباید باشد و باید فراتر از انتهای موج ۱ خاتمه یابد
        
        الزامات زمانی (صفحه ۵۷):
        - موج ۲ نباید زمانی کمتر از موج ۱ صرف کند
        - موج ۴ نباید زمانی کمتر از موج ۳ صرف کند
        - موج ۵ نباید زمانی بیش از مجموع موج ۱ تا ۳ داشته باشد
        """
        violations = []
        
        # قانون ۱: موج ۲ نباید ۱۰۰٪ موج ۱ را اصلاح کند
        if impulse.len_w2 >= impulse.len_w1:
            violations.append("نقض Q1: موج ۲، ۱۰۰٪ موج ۱ را اصلاح کرده است")
        
        # قانون ۲: موج ۴ نباید ۱۰۰٪ موج ۳ را اصلاح کند
        if impulse.len_w4 >= impulse.len_w3:
            violations.append("نقض Q2: موج ۴، ۱۰۰٪ موج ۳ را اصلاح کرده است")
        
        # قانون ۳: موج ۳ کوتاه‌ترین نباشد
        lengths = [impulse.len_w1, impulse.len_w3, impulse.len_w5]
        if impulse.len_w3 == min(lengths) and min(lengths) > 0:
            violations.append("نقض Q3: موج ۳ کوتاه‌ترین موج قیمتی است")
        
        # قانون ۴: موج ۳ باید فراتر از انتهای موج ۱ خاتمه یابد
        if impulse.w1.price < impulse.w3.price:  # صعودی
            if impulse.w3.price <= impulse.w1.price:
                violations.append("نقض Q4: موج ۳ فراتر از انتهای موج ۱ خاتمه نیافته است")
        else:
            if impulse.w3.price >= impulse.w1.price:
                violations.append("نقض Q4: موج ۳ فراتر از انتهای موج ۱ خاتمه نیافته است")
        
        # قانون ۵: عدم همپوشانی موج ۴ با موج ۲
        if ImpulseAnalyzer.check_overlap(impulse):
            violations.append("نقض Q5: همپوشانی موج ۴ با قلمرو موج ۲ (احتمال ترمینال)")
        
        # ── الزامات قیمتی (صفحه ۵۶) ──
        if impulse.len_w4 > 0:
            w5_ret = impulse.len_w5 / impulse.len_w4
            if w5_ret < 0.382:
                violations.append("هشدار قیمتی: موج ۵ کمتر از ۳۸.۲٪ موج ۴ را بازگشت کرده است")
        
        if impulse.len_w3 > 0:
            w4_ret = impulse.len_w4 / impulse.len_w3
            if w4_ret > 0.618:
                violations.append("هشدار قیمتی: موج ۴ بیش از ۶۱.۸٪ موج ۳ را اصلاح کرده است (احتمال ترمینال یا موج ۵ کوتاه شده)")
        
        if impulse.len_w1 > 0:
            w3_ratio = impulse.len_w3 / impulse.len_w1
            if w3_ratio < 0.618:
                violations.append("هشدار قیمتی: موج ۳ کمتر از ۶۱.۸٪ موج ۱ است")
        
        # ── الزامات زمانی (صفحه ۵۷) ──
        if impulse.time_w1 > 0 and impulse.time_w2 < impulse.time_w1:
            violations.append("هشدار زمانی: موج ۲ زمان کمتری نسبت به موج ۱ صرف کرده است")
        
        if impulse.time_w3 > 0 and impulse.time_w4 < impulse.time_w3:
            violations.append("هشدار زمانی: موج ۴ زمان کمتری نسبت به موج ۳ صرف کرده است")
            
        if impulse.time_w5 > (impulse.time_w1 + impulse.time_w2 + impulse.time_w3):
            violations.append("هشدار زمانی: موج ۵ زمانی بیش از مجموع زمان موج ۱ تا ۳ داشته است")
        
        return violations
    
    @staticmethod
    def check_terminal_violations(impulse: ImpulseWave) -> List[str]:
        """
        بررسی نقض قوانین نقض‌ناپذیر شتابدار ترمینال (صفحه ۷۸)
        
        الزامات:
        - همپوشانی موج ۴ با موج ۱ الزامی است
        - موج ۵ باید حداقل ۳۸.۲٪ موج ۴ را بازگشت کند
        - شیب کانال نمی‌تواند افقی باشد
        
        نکته زمانی ترمینال: موج ۲ و ۴ می‌توانند زمان کمتری صرف کنند
        """
        violations = []
        
        # قانون ۱: همپوشانی الزامی
        if not ImpulseAnalyzer.check_overlap(impulse):
            violations.append("نقض ترمینال Q1: همپوشانی موج ۴ با موج ۱ وجود ندارد")
        
        # قانون ۲: موج ۵ حداقل ۳۸.۲٪ موج ۴
        if impulse.len_w4 > 0:
            w5_ret = impulse.len_w5 / impulse.len_w4
            if w5_ret < 0.382:
                violations.append("نقض ترمینال Q2: موج ۵ کمتر از ۳۸.۲٪ موج ۴ را بازگشت کرده است")
        
        # قانون ۳: موج ۳ باید قله موج ۱ را فتح کند
        if impulse.w1.price < impulse.w3.price:  # صعودی
            if impulse.w3.price <= impulse.w1.price:
                violations.append("نقض ترمینال Q3: موج ۳ قله موج ۱ را فتح نکرده است")
        else:
            if impulse.w3.price >= impulse.w1.price:
                violations.append("نقض ترمینال Q3: موج ۳ کف موج ۱ را فتح نکرده است")
        
        # هشدار زمانی: موج ۵ نباید زمانی بیش از مجموع موج ۱ تا ۳ داشته باشد
        if impulse.time_w5 > (impulse.time_w1 + impulse.time_w2 + impulse.time_w3):
            violations.append("هشدار زمانی ترمینال: موج ۵ بیش از حد طولانی است")
        
        return violations
    
    @staticmethod
    def determine_channel_type(impulse: ImpulseWave) -> str:
        """
        تعیین نوع کانال‌بندی (صفحات ۱۰۲ تا ۱۰۸)
        
        - موج ۲ بلندتر از موج ۴: کانال‌بندی همگرا
        - موج ۴ بلندتر از موج ۲: کانال‌بندی واگرا (مگافون)
        - برابر: موازی
        """
        if impulse.len_w2 > impulse.len_w4 * 1.1:
            return "همگرا"
        elif impulse.len_w4 > impulse.len_w2 * 1.1:
            return "واگرا_مگافون"
        else:
            return "موازی"
    
    @staticmethod
    def classify_impulse(impulse: ImpulseWave, is_potential_start: bool = False) -> ImpulseAnalysisResult:
        """
        دسته‌بندی کامل یک الگوی شتابدار
        
        پارامتر جدید:
        is_potential_start: آیا این الگو در ابتدای یک حرکت بزرگتر قرار دارد؟
                           (برای تشخیص قطری پیشرو در موج ۱ یا A)
        
        بر اساس ۶۵ صفحه کتاب (صفحات ۵۵ تا ۱۱۹):
        ۱. بررسی همپوشانی -> تفکیک روند دار / ترمینال / قطری پیشرو
        ۲. شناسایی موج ممتد
        ۳. بررسی کوتاه‌شدگی
        ۴. بررسی قانون برابری
        ۵. بررسی نقض قوانین قیمتی و زمانی
        ۶. تعیین زیرنوع دقیق
        """
        # محاسبه متریک‌ها
        impulse = ImpulseAnalyzer.calculate_wave_metrics(impulse)
        
        # بررسی وضعیت‌های پایه
        has_overlap = ImpulseAnalyzer.check_overlap(impulse)
        is_truncated = ImpulseAnalyzer.check_truncation(impulse)
        extended_wave = ImpulseAnalyzer.identify_extended_wave(impulse)
        channel_type = ImpulseAnalyzer.determine_channel_type(impulse)
        
        # محاسبه نسبت‌های قیمتی
        ratio_w3_to_w1 = impulse.len_w3 / impulse.len_w1 if impulse.len_w1 > 0 else 0
        ratio_w5_to_w3 = impulse.len_w5 / impulse.len_w3 if impulse.len_w3 > 0 else 0
        ratio_w5_to_w1 = impulse.len_w5 / impulse.len_w1 if impulse.len_w1 > 0 else 0
        ratio_w2_ret_w1 = impulse.len_w2 / impulse.len_w1 if impulse.len_w1 > 0 else 0
        ratio_w4_ret_w3 = impulse.len_w4 / impulse.len_w3 if impulse.len_w3 > 0 else 0
        ratio_w5_ret_w4 = impulse.len_w5 / impulse.len_w4 if impulse.len_w4 > 0 else 0
        
        # محاسبه نسبت‌های زمانی
        time_ratio_w2_to_w1 = impulse.time_w2 / impulse.time_w1 if impulse.time_w1 > 0 else 0
        time_ratio_w4_to_w3 = impulse.time_w4 / impulse.time_w3 if impulse.time_w3 > 0 else 0
        time_ratio_w5_to_w3 = impulse.time_w5 / impulse.time_w3 if impulse.time_w3 > 0 else 0
        
        # محاسبه قانون برابری (صفحه ۱۱۶)
        equality_ratio, equality_status = ImpulseAnalyzer.calculate_equality(impulse, extended_wave)
        
        # ── دسته‌بندی اصلی ─────────────────────────────────────
        if has_overlap:
            # تشخیص قطری پیشرو (صفحه ۷۶)
            # اگر در ابتدای روند است و همپوشانی دارد -> قطری پیشرو
            if is_potential_start:
                category = ImpulseCategory.LEADING_DIAGONAL
                violations = []  # قوانین متفاوت دارد
                sub_type, description, page_ref = ImpulseAnalyzer._classify_leading_diagonal(
                    impulse, extended_wave, is_truncated, ratio_w3_to_w1, ratio_w5_to_w3,
                    ratio_w2_ret_w1, ratio_w4_ret_w3, channel_type
                )
                internal_structure = "فرض_۵_۳_۵_۳_۵"
            else:
                # شتابدار ترمینال
                category = ImpulseCategory.TERMINAL
                violations = ImpulseAnalyzer.check_terminal_violations(impulse)
                sub_type, description, page_ref = ImpulseAnalyzer._classify_terminal(
                    impulse, extended_wave, is_truncated, ratio_w3_to_w1, ratio_w5_to_w3,
                    ratio_w2_ret_w1, ratio_w4_ret_w3, ratio_w5_ret_w4, channel_type
                )
                internal_structure = "فرض_۳_۳_۳_۳_۳"
        else:
            category = ImpulseCategory.TRENDING
            violations = ImpulseAnalyzer.check_trending_violations(impulse)
            sub_type, description, page_ref = ImpulseAnalyzer._classify_trending(
                impulse, extended_wave, is_truncated, ratio_w3_to_w1, ratio_w5_to_w3,
                ratio_w2_ret_w1, ratio_w4_ret_w3, ratio_w5_ret_w4, channel_type
            )
            internal_structure = "فرض_۵_۳_۵_۳_۵"
        
        return ImpulseAnalysisResult(
            category=category,
            sub_type=sub_type,
            has_overlap=has_overlap,
            extended_wave=extended_wave,
            is_truncated=is_truncated,
            ratio_w3_to_w1=ratio_w3_to_w1,
            ratio_w5_to_w3=ratio_w5_to_w3,
            ratio_w5_to_w1=ratio_w5_to_w1,
            ratio_w2_ret_w1=ratio_w2_ret_w1,
            ratio_w4_ret_w3=ratio_w4_ret_w3,
            ratio_w5_ret_w4=ratio_w5_ret_w4,
            time_ratio_w2_to_w1=time_ratio_w2_to_w1,
            time_ratio_w4_to_w3=time_ratio_w4_to_w3,
            time_ratio_w5_to_w3=time_ratio_w5_to_w3,
            channel_type=channel_type,
            equality_ratio=equality_ratio,
            equality_status=equality_status,
            violations=violations,
            internal_structure_status=internal_structure,
            description=description,
            page_reference=page_ref
        )
    
    @staticmethod
    def _classify_leading_diagonal(
        impulse: ImpulseWave, extended_wave: Optional[int], is_truncated: bool,
        ratio_w3_to_w1: float, ratio_w5_to_w3: float, ratio_w2_ret_w1: float,
        ratio_w4_ret_w3: float, channel_type: str
    ) -> Tuple[ImpulseSubType, str, str]:
        """دسته‌بندی الگوی قطری پیشرو (صفحه ۷۶)"""
        
        if is_truncated:
            return (
                ImpulseSubType.LEADING_DIAG,
                "خطا: الگوی قطری پیشرو نمی‌تواند همراه با کوتاه‌شدگی باشد.",
                "صفحه ۷۶"
            )
        
        return (
            ImpulseSubType.LEADING_DIAG,
            "الگوی قطری پیشرو (Leading Diagonal). "
            "ساختار ۵-۳-۵-۳-۵. در جهت روند و در موج ۱ یا A رخ می‌دهد. "
            "نشان از شروع افت یا رشد شارپی دارد. معمولاً ۱۰۰٪ اصلاح می‌گردد. "
            "موج ۴ با موج ۱ همپوشانی دارد. موج ۲ نمی‌تواند به نقطه ابتدایی موج ۱ بازگردد. "
            "موج ۲ نمی‌تواند به شکل الگوی اصلاحی مثلث باشد. "
            "موج ۳ قله موج ۱ را همواره فتح می‌کند.",
            "صفحه ۷۶"
        )
    
    @staticmethod
    def _classify_trending(
        impulse: ImpulseWave, extended_wave: Optional[int], is_truncated: bool,
        ratio_w3_to_w1: float, ratio_w5_to_w3: float, ratio_w2_ret_w1: float,
        ratio_w4_ret_w3: float, ratio_w5_ret_w4: float, channel_type: str
    ) -> Tuple[ImpulseSubType, str, str]:
        """دسته‌بندی زیرنوع‌های شتابدار روند دار"""
        
        # موج ۵ کوتاه شده (صفحه ۷۳)
        if is_truncated:
            return (
                ImpulseSubType.TRUNCATED,
                "شتابدار روند دار با موج ۵ کوتاه شده (Truncated Impulse). "
                "قله موج ۵ به ارتفاع بالاتر از موج ۳ دست نیافته است. "
                "اخطاری است برای تضعیف و تغییر روند. موج ۴ پیچیده‌ترین بخش اصلاحی است "
                "و بایستی بیش از ۶۱.۸ درصد موج ۳ را اصلاح کرده و بلندتر از موج ۲ باشد. "
                "فقط و فقط در موج ۵ یا C روند می‌تواند رخ دهد. "
                "کل الگو بایستی توسط اصلاح متعاقب بازگشت شود.",
                "صفحه ۷۳"
            )
        
        # امتداد دوگانه (صفحه ۷۰)
        if ratio_w3_to_w1 > 1.618 and ratio_w5_to_w3 > 1.618:
            return (
                ImpulseSubType.DOUBLE_EXT,
                "شتابدار روند دار با امتداد دوگانه (Double Extension Trending). "
                "موج ۳ بایستی ورای ۱۶۱.۸ درصد موج ۱ پایان یابد. "
                "موج ۵ بایستی ورای ۱۶۱.۸ درصد موج ۳ یا ۱۰۰ درصد ابتدای موج ۱ تا انتهای موج ۳ پایان یابد. "
                "در این وضعیت اغلب موج ۴ زمانبرتر و پیچیده‌تر از موج ۲ است. "
                "پایان موج ۵ اغلب بایستی ورای خط روند ۱-۳ می‌باشد. "
                "الگوی بسیار نادری می‌باشد.",
                "صفحه ۷۰"
            )
        
        # موج ۱ ممتد (صفحه ۶۱)
        if extended_wave == 1:
            return (
                ImpulseSubType.EXT_1,
                "شتابدار روند دار با موج ۱ ممتد (1st Extension Trending). "
                "زمانی که موج ۱ امتداد پیدا می‌کند، توالی پنج موجی در قالب گوه‌ای شکل به پایان می‌رسد. "
                "موج ۲ معمولاً پیچیده‌تر از موج ۴ است و اغلب نبایستی بیش از ۳۸ درصد موج ۱ را اصلاح کند. "
                "موج ۲ نمی‌تواند یک اصلاح جاری باشد. "
                "موج ۵ نمی‌تواند بیش از ۹۹ درصد موج ۳ باشد. "
                "چنانچه موج ۱ اندکی کوتاهتر از ۱۶۱.۸ درصد موج ۳ باشد، موج ۳ نبایستی ورای ۶۱.۸ درصد موج ۱ باشد. "
                f"کانال‌بندی: {channel_type}.",
                "صفحه ۶۱"
            )
        
        # موج ۳ ممتد (صفحه ۶۳)
        if extended_wave == 3:
            return (
                ImpulseSubType.EXT_3,
                "شتابدار روند دار با موج ۳ ممتد (3rd Extension Trending). "
                "در این حالت موج ۲ بیش از ۶۱.۸ درصد موج ۱ را اصلاح می‌کند. "
                "موج ۴ معمولاً کمتر از ۳۸.۲ درصد موج ۳ را اصلاح می‌کند. "
                "در صورتی که موج ۴ بیش از ۶۱.۸ درصد موج ۳ باشد، موج ۵ کوتاه شده خواهد بود. "
                "موج ۳ بیش از ۱۶۱.۸ درصد موج ۱ و معمولاً تا ۲۶۱.۸ درصد آن خواهد بود. "
                "موج ۵ بایستی کمتر از ۶۱.۸ درصد موج ۳ باشد. "
                "چنانچه موج ۴ پیچیده‌تر از موج ۲ باشد، موج ۵ برابر یا بیشتر از موج ۱ خواهد بود. "
                "اغلب موج ۲ پیچیده‌تر از موج ۴ است. "
                f"کانال‌بندی: {channel_type}.",
                "صفحه ۶۳"
            )
        
        # موج ۵ ممتد (صفحه ۶۷)
        if extended_wave == 5:
            return (
                ImpulseSubType.EXT_5,
                "شتابدار روند دار با موج ۵ ممتد (5th Extension Trending). "
                "امواج ۱ و ۳ معمولاً از نظر زمانی برابر و یا با نسبت ۶۱.۸ درصد با هم مرتبط می‌باشند. "
                "موج ۳ بایستی حداقل ۱۰۰ و حداکثر ۱۶۱.۸ درصد موج ۱ باشد. "
                "در این وضعیت موج ۴ اغلب زمانبرتر و پیچیده‌تر از موج ۲ است. "
                "موج ۴ حداکثر ۶۱.۸ درصد موج ۳ را اصلاح می‌کند. "
                "معمولاً موج ۴ با یک موج C ناقص پایان می‌یابد یا به فرم اصلاح جاری خواهد بود. "
                "موج ۵ بایستی حداقل به میزان ابتدای موج ۱ تا انتهای موج ۳ و حداکثر ۲۶۱.۸ درصد آن باشد. "
                "پایان موج ۵ اغلب بایستی زیر خط روند ۱-۳ می‌باشد. "
                f"کانال‌بندی: {channel_type} (شپور).",
                "صفحه ۶۷"
            )
        
        # ساده (صفحه ۵۹)
        return (
            ImpulseSubType.SIMPLE,
            "شتابدار روند دار ساده (Simple Trending Impulse). "
            "این امواج بدون هر گونه ریزموج ظاهر می‌شوند. "
            "قوانین کلی الیوت در مورد آنها صدق می‌کند. "
            "رایج‌ترین نوع امواج شتابدار و در جهت روند بزرگتر می‌باشد. "
            "در هر یک از الگوهای شتابدار روند دار می‌تواند وجود داشته باشد.",
            "صفحه ۵۹"
        )
    
    @staticmethod
    def _classify_terminal(
        impulse: ImpulseWave, extended_wave: Optional[int], is_truncated: bool,
        ratio_w3_to_w1: float, ratio_w5_to_w3: float, ratio_w2_ret_w1: float,
        ratio_w4_ret_w3: float, ratio_w5_ret_w4: float, channel_type: str
    ) -> Tuple[ImpulseSubType, str, str]:
        """دسته‌بندی زیرنوع‌های شتابدار ترمینال"""
        
        # ترمینال با موج ۵ کوتاه شده (صفحه ۸۹)
        if is_truncated:
            return (
                ImpulseSubType.TERMINAL_TRUNCATED,
                "شتابدار ترمینال با موج ۵ کوتاه شده (5th Failure Terminal). "
                "موج ۳ الگو بایستی بلندترین موج باشد. "
                "موج ۵ بایستی حداقل ۳۸.۲ درصد موج ۱ و نبایستی از موج ۱ و ۳ پیچیده‌تر باشد. "
                "موج ۴ بایستی بیش از ۶۱.۸ درصد و تا ۹۹ درصد موج ۳ را بازگشت کند. "
                "موج ۴ بایستی بلندتر از موج ۲ باشد. "
                "خط روند ۱-۵ بایستی توسط موج ۳ شکسته شده باشد. "
                "تفاوت آشکار بین موج ۲ و ۴ در قیمت/زمان و پیچیدگی وجود دارد. "
                "کل الگو بایستی توسط اصلاح متعاقب بازگشت شود.",
                "صفحه ۸۹"
            )
        
        # ترمینال با موج ۳ ممتد (صفحه ۸۵) - بسیار نادر
        if extended_wave == 3 and ratio_w2_ret_w1 > 0.618:
            return (
                ImpulseSubType.TERMINAL_EXT_3,
                "شتابدار ترمینال با موج ۳ ممتد (3rd Extension Terminal). "
                "یکی از نادرترین الگوها می‌باشد. "
                "موج ۳ بایستی بلندترین موج نسبت به موج ۱ و ۵ باشد (ولی نه الزاماً ۱۶۱.۸ درصد). "
                "موج ۲ بایستی بیش از ۶۱.۸ درصد موج ۱ را بازگشت کند. "
                "موج ۴ معمولاً کمتر از ۳۸.۲ درصد موج ۳ را بازگشت می‌کند. "
                "موج ۵ نبایستی بیش از ۶۱.۸ درصد موج ۳ باشد. "
                "معمولاً در قالب موج C دیده می‌شود نه در موج ۵. "
                "خط روند ۱-۳ بایستی توسط موج ۵ شکسته شده باشد. "
                f"کانال‌بندی: {channel_type}. "
                "کل الگو بایستی توسط اصلاح متعاقب بازگشت شود.",
                "صفحه ۸۵"
            )
        
        # ترمینال با موج ۵ ممتد (صفحه ۸۶) - رایج‌ترین
        if extended_wave == 5 and ratio_w5_to_w3 > 1.0:
            return (
                ImpulseSubType.TERMINAL_EXT_5,
                "شتابدار ترمینال با موج ۵ ممتد (5th Extension Terminal). "
                "یکی از رایج‌ترین الگوها می‌باشد. "
                "موج ۵ بایستی بلندترین نسبت به موج ۱ و ۳ باشد (ولی نه الزاماً ۱۶۱.۸ درصد). "
                "موج ۳ بایستی بیش از ۱۰۰ درصد موج ۱ باشد. "
                "موج ۵ بایستی بیش از ۱۰۰ درصد مجموع موج ۱ تا ۳ و حداکثر ۱۶۱.۸ آن باشد. "
                "موج ۴ بایستی بیش از ۵۰ درصد موج ۳ را بازگشت کند. "
                "موج ۴ معمولاً بلندتر و زمانبرتر از موج ۲ می‌باشد. "
                "بر خلاف مثلث انبساطی، اندکی به سمت بالا (پایین) انحراف دارد. "
                "کل الگو بایستی توسط اصلاح متعاقب بازگشت شود.",
                "صفحه ۸۶"
            )
        
        # ترمینال با موج ۱ ممتد (صفحه ۷۹)
        if extended_wave == 1:
            return (
                ImpulseSubType.TERMINAL_EXT_1,
                "شتابدار ترمینال با موج ۱ ممتد (1st Extension Terminal). "
                "موج ۱ بایستی بلندترین موج نسبت به موج ۳ و ۵ باشد (ولی نه الزاماً ۱۶۱.۸ درصد). "
                "موج ۲ نبایستی بیش از ۶۱.۸ درصد موج ۱ را بازگشت کند. "
                "موج ۳ نبایستی بیش از ۶۱.۸ درصد و کمتر از ۳۸.۲ درصد موج ۱ باشد. "
                "موج ۵ نبایستی بیش از ۹۹ درصد موج ۳ باشد. "
                f"کانال‌بندی: {channel_type}. "
                "کل الگو بایستی توسط اصلاح متعاقب بازگشت شود.",
                "صفحه ۷۹"
            )
        
        # ترمینال ساده (صفحه ۷۸)
        return (
            ImpulseSubType.TERMINAL_SIMPLE,
            "شتابدار ترمینال ساده (Simple Terminal). "
            "ساختاری متفاوت با امواج شتابدار دارد و از ۳ ریزموج تشکیل می‌شود. "
            "از قانون ۳-۳-۳-۳-۳ پیروی می‌کند. "
            "در جهت روند می‌باشد. نشان از شروع یک افت یا رشد شارپی دارد که معمولاً ۱۰۰ درصد الگو اصلاح می‌گردد. "
            "معمولاً پس از یک رشد یا اصلاح شارپی (به ویژه پس از موج ۳) رخ می‌دهند. "
            "موج ۵ آن معمولاً همراه با کوتاه‌شدگی می‌باشد. "
            "موج ۴ (یا بخشی از آن) بایستی با موج ۱ همپوشانی داشته باشد. "
            "موج ۲ نمی‌تواند به شکل الگوی اصلاحی مثلث باشد مگر اینکه موج ۱ آن ممتد باشد. "
            "موج ۳ قله موج ۱ را همواره فتح می‌کند. "
            "موج ۵ بایستی حداقل ۳۸.۲ درصد موج ۴ را اصلاح کند. "
            "شیب کانال نمی‌تواند افقی باشد. "
            "فقط می‌تواند پایان‌بخش الگوی بزرگتر باشد، لذا فقط و فقط می‌تواند در موج ۵ یا موج C شتابدار روند دار رخ دهد.",
            "صفحه ۷۸"
        )


# ════════════════════════════════════════════════════════════════
# بخش ۳: تشخیص الگوهای شتابدار از داده خام (الگوریتم ZigZag بهبود یافته)
# ════════════════════════════════════════════════════════════════

def detect_pivots_zigzag(
    high: List[float],
    low: List[float],
    close: List[float],
    threshold_pct: float = 1.0
) -> List[Dict]:
    """
    تشخیص نقاط عطف با الگوریتم شبیه ZigZag برای کاهش نویز (پیشنهاد کلاد)
    
    به جای چک کردن تک‌کندل، از یک پنجره برای تشخیص سقف و کف استفاده می‌شود.
    فقط تغییرات قیمتی بزرگتر از threshold_pct به عنوان نقطه عطف در نظر گرفته می‌شود.
    """
    n = len(close)
    if n < 5:
        return []
    
    pivots = []
    last_pivot_price = close[0]
    last_pivot_type = None  # 'HIGH' or 'LOW'
    last_pivot_idx = 0
    
    for i in range(2, n - 2):
        current_price = close[i]
        change_pct = abs(current_price - last_pivot_price) / last_pivot_price * 100 if last_pivot_price != 0 else 0
        
        # بررسی سقف محلی
        if high[i] >= max(high[i-1], high[i-2]) and high[i] >= max(high[i+1], high[i+2]):
            if change_pct >= threshold_pct:
                if last_pivot_type != 'HIGH':
                    pivots.append({"type": "HIGH", "index": i, "price": high[i]})
                    last_pivot_price = high[i]
                    last_pivot_type = 'HIGH'
                    last_pivot_idx = i
        
        # بررسی کف محلی
        elif low[i] <= min(low[i-1], low[i-2]) and low[i] <= min(low[i+1], low[i+2]):
            if change_pct >= threshold_pct:
                if last_pivot_type != 'LOW':
                    pivots.append({"type": "LOW", "index": i, "price": low[i]})
                    last_pivot_price = low[i]
                    last_pivot_type = 'LOW'
                    last_pivot_idx = i
                    
    return pivots


def detect_impulse_patterns(
    prices: List[float],
    high_prices: List[float],
    low_prices: List[float],
    min_wave_bars: int = 3,
    pivot_threshold: float = 1.0
) -> List[Dict]:
    """
    تشخیص الگوهای شتابدار ۵ موجی از سری قیمتی
    
    با استفاده از الگوریتم ZigZag بهبود یافته، نقاط عطف استخراج شده
    و سپس الگوهای ۵ موجی شناسایی و توسط ImpulseAnalyzer دسته‌بندی می‌شوند.
    """
    patterns = []
    n = len(prices)
    
    if n < 15:
        return patterns
    
    # یافتن نقاط عطف با ZigZag
    pivots = detect_pivots_zigzag(high_prices, low_prices, prices, pivot_threshold)
    
    # جستجوی الگوهای ۵ موجی
    for i in range(len(pivots) - 5):
        p0, p1, p2, p3, p4, p5 = pivots[i:i+6]
        
        # بررسی الگوی صعودی: LOW-HIGH-LOW-HIGH-LOW-HIGH
        if (p0["type"] == "LOW" and p1["type"] == "HIGH" and p2["type"] == "LOW" and 
            p3["type"] == "HIGH" and p4["type"] == "LOW" and p5["type"] == "HIGH"):
            
            # بررسی سلسله مراتب قیمتی
            if p1["price"] > p0["price"] and p3["price"] > p1["price"] and p5["price"] > p3["price"]:
                
                # بررسی آیا در ابتدای حرکت قرار دارد (برای قطری پیشرو)
                # بررسی هوشمند آیا در ابتدای یک حرکت جدید قرار دارد (برای قطری پیشرو)
                # باید قبل از شروع الگو، یک اصلاح کامل (افت قابل توجه) وجود داشته باشد
                is_start = False
                if i == 0:
                    is_start = True
                else:
                    p_prev = pivots[i-1]
                    # اگر الگوی صعودی است، قبل از آن باید یک سقف بوده و سپس افت داشته باشیم
                    if p_prev["type"] == "HIGH":
                        drop_pct = (p_prev["price"] - p0["price"]) / p_prev["price"] * 100
                        if drop_pct > 1.0:  # حداقل ۱ درصد افت قبل از شروع حرکت جدید
                            is_start = True 
                
                impulse = ImpulseWave(
                    w0=WavePoint(p0["index"], p0["price"], p0["index"]),
                    w1=WavePoint(p1["index"], p1["price"], p1["index"]),
                    w2=WavePoint(p2["index"], p2["price"], p2["index"]),
                    w3=WavePoint(p3["index"], p3["price"], p3["index"]),
                    w4=WavePoint(p4["index"], p4["price"], p4["index"]),
                    w5=WavePoint(p5["index"], p5["price"], p5["index"]),
                )
                
                result = ImpulseAnalyzer.classify_impulse(impulse, is_potential_start=is_start)
                
                patterns.append({
                    "type": "صعودی",
                    "direction": "UP",
                    "category": result.category.value,
                    "sub_type": result.sub_type.value,
                    "start_idx": p0["index"],
                    "end_idx": p5["index"],
                    "start_price": p0["price"],
                    "end_price": p5["price"],
                    "has_overlap": result.has_overlap,
                    "is_truncated": result.is_truncated,
                    "extended_wave": result.extended_wave,
                    "channel_type": result.channel_type,
                    "equality_ratio": result.equality_ratio,
                    "equality_status": result.equality_status,
                    "internal_structure": result.internal_structure_status,
                    "violations": result.violations,
                    "description": result.description,
                    "page_reference": result.page_reference,
                    "ratio_w3_w1": round(result.ratio_w3_to_w1, 4),
                    "ratio_w5_w3": round(result.ratio_w5_to_w3, 4),
                    "ratio_w2_ret": round(result.ratio_w2_ret_w1, 4),
                    "ratio_w4_ret": round(result.ratio_w4_ret_w3, 4),
                })
        
        # بررسی الگوی نزولی: HIGH-LOW-HIGH-LOW-HIGH-LOW
        elif (p0["type"] == "HIGH" and p1["type"] == "LOW" and p2["type"] == "HIGH" and 
              p3["type"] == "LOW" and p4["type"] == "HIGH" and p5["type"] == "LOW"):
            
            # بررسی سلسله مراتب قیمتی
            if p1["price"] < p0["price"] and p3["price"] < p1["price"] and p5["price"] < p3["price"]:
                
                # بررسی هوشمند آیا در ابتدای یک حرکت جدید قرار دارد (برای قطری پیشرو)
                # باید قبل از شروع الگو، یک اصلاح کامل (صعود قابل توجه) وجود داشته باشد
                is_start = False
                if i == 0:
                    is_start = True
                else:
                    p_prev = pivots[i-1]
                    # اگر الگوی نزولی است، قبل از آن باید یک کف بوده و سپس صعود داشته باشیم
                    if p_prev["type"] == "LOW":
                        rise_pct = (p0["price"] - p_prev["price"]) / p_prev["price"] * 100
                        if rise_pct > 1.0:  # حداقل ۱ درصد صعود قبل از شروع حرکت جدید
                            is_start = True
                
                impulse = ImpulseWave(
                    w0=WavePoint(p0["index"], p0["price"], p0["index"]),
                    w1=WavePoint(p1["index"], p1["price"], p1["index"]),
                    w2=WavePoint(p2["index"], p2["price"], p2["index"]),
                    w3=WavePoint(p3["index"], p3["price"], p3["index"]),
                    w4=WavePoint(p4["index"], p4["price"], p4["index"]),
                    w5=WavePoint(p5["index"], p5["price"], p5["index"]),
                )
                
                result = ImpulseAnalyzer.classify_impulse(impulse, is_potential_start=is_start)
                
                patterns.append({
                    "type": "نزولی",
                    "direction": "DOWN",
                    "category": result.category.value,
                    "sub_type": result.sub_type.value,
                    "start_idx": p0["index"],
                    "end_idx": p5["index"],
                    "start_price": p0["price"],
                    "end_price": p5["price"],
                    "has_overlap": result.has_overlap,
                    "is_truncated": result.is_truncated,
                    "extended_wave": result.extended_wave,
                    "channel_type": result.channel_type,
                    "equality_ratio": result.equality_ratio,
                    "equality_status": result.equality_status,
                    "internal_structure": result.internal_structure_status,
                    "violations": result.violations,
                    "description": result.description,
                    "page_reference": result.page_reference,
                    "ratio_w3_w1": round(result.ratio_w3_to_w1, 4),
                    "ratio_w5_w3": round(result.ratio_w5_to_w3, 4),
                    "ratio_w2_ret": round(result.ratio_w2_ret_w1, 4),
                    "ratio_w4_ret": round(result.ratio_w4_ret_w3, 4),
                })
    
    return patterns


# ════════════════════════════════════════════════════════════════
# بخش ۴: تابع analyze (interface اصلی برای main.py)
# ════════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None, context=None) -> Dict:
    """
    فصل ۱۱: دسته‌بندی امواج شتابدار (Impulse Waves Classification)
    
    پیاده‌سازی کامل و دقیق مطابق صفحات ۵۵ تا ۱۱۹ کتاب گلن نیلی.
    
    این تابع:
        ۱. الگوهای ۵ موجی شتابدار را با الگوریتم ZigZag تشخیص می‌دهد
        ۲. هر الگو را به روند دار، ترمینال یا قطری پیشرو دسته‌بندی می‌کند
        ۳. موج ممتد را شناسایی می‌کند
        ۴. قانون برابری را محاسبه و ارزیابی می‌کند
        ۵. نقض قوانین قیمتی و زمانی را بررسی می‌کند
        ۶. نسبت‌های فیبوناچی را محاسبه می‌کند
        ۷. نوع کانال‌بندی را تعیین می‌کند
    
    پارامترها:
        data: DataFrame با ستون‌های open, high, low, close, volume
        logger: ResultsLogger (اختیاری)
    
    خروجی:
        دیکشنری با تمام نتایج تحلیل
    """
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۱: استخراج داده‌های قیمتی
    # ════════════════════════════════════════════════════════════
    close = data['close'].values if 'close' in data.columns else data['Close'].values
    high = data['high'].values if 'high' in data.columns else data['High'].values
    low = data['low'].values if 'low' in data.columns else data['Low'].values
    
    n = len(close)

    # ── دریافت موج‌ها از context (فصل ۵، ۶، ۷) ──────────────
    monowaves_from_ch5 = None
    context_used = False

    if context:
        if "chapter_5" in context and "_monowaves" in context["chapter_5"]:
            monowaves_from_ch5 = context["chapter_5"]["_monowaves"]
            context_used = True
    
    if n < 15:
        return {
            "عنوان": "فصل ۱۱: دسته‌بندی امواج شتابدار",
            "وضعیت": "داده_کافی_نیست",
            "تعداد_کندل": str(n),
            "پیام": "برای تحلیل حداقل ۱۵ کندل لازم است"
        }
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۲: تشخیص الگوهای شتابدار با ZigZag
    # ════════════════════════════════════════════════════════════
    patterns = []

    if monowaves_from_ch5 and len(monowaves_from_ch5) > 0:
        # استفاده از مونوویوهای فصل ۵
        # تبدیل مونوویوها به نقاط عطف برای تشخیص الگو
        points = []
        for mw in monowaves_from_ch5:
            points.append({
                "index": mw.start_bar,
                "price": mw.start_price,
                "type": "LOW" if mw.direction.value == "DOWN" else "HIGH"
            })
            points.append({
                "index": mw.end_bar,
                "price": mw.end_price,
                "type": "HIGH" if mw.direction.value == "UP" else "LOW"
            })
    
        # حذف نقاط تکراری و هم‌نوع متوالی
        filtered = []
        for pt in points:
            if not filtered:
                filtered.append(pt)
                continue
            last = filtered[-1]
            if last["type"] == pt["type"]:
                if pt["type"] == "HIGH" and pt["price"] > last["price"]:
                    filtered[-1] = pt
                elif pt["type"] == "LOW" and pt["price"] < last["price"]:
                    filtered[-1] = pt
            else:
                filtered.append(pt)
    
        # ساخت لیست pivots به فرمت مورد نیاز detect_impulse_patterns
        pivots = []
        for pt in filtered:
            pivots.append({
                "type": pt["type"],
                "index": pt["index"],
                "price": pt["price"]
            })
    
        # جستجوی الگوهای ۵ موجی
        for i in range(len(pivots) - 5):
            p0, p1, p2, p3, p4, p5 = pivots[i:i+6]
        
            # الگوی صعودی
            if (p0["type"] == "LOW" and p1["type"] == "HIGH" and p2["type"] == "LOW" and 
                p3["type"] == "HIGH" and p4["type"] == "LOW" and p5["type"] == "HIGH"):
                if p1["price"] > p0["price"] and p3["price"] > p1["price"] and p5["price"] > p3["price"]:
                    impulse = ImpulseWave(
                        w0=WavePoint(p0["index"], p0["price"], p0["index"]),
                        w1=WavePoint(p1["index"], p1["price"], p1["index"]),
                        w2=WavePoint(p2["index"], p2["price"], p2["index"]),
                        w3=WavePoint(p3["index"], p3["price"], p3["index"]),
                        w4=WavePoint(p4["index"], p4["price"], p4["index"]),
                        w5=WavePoint(p5["index"], p5["price"], p5["index"]),
                    )
                    result = ImpulseAnalyzer.classify_impulse(impulse, is_potential_start=(i==0))
                    patterns.append({
                        "type": "صعودی",
                        "direction": "UP",
                        "category": result.category.value,
                        "sub_type": result.sub_type.value,
                        "start_idx": p0["index"],
                        "end_idx": p5["index"],
                        "start_price": p0["price"],
                        "end_price": p5["price"],
                        "has_overlap": result.has_overlap,
                        "is_truncated": result.is_truncated,
                        "extended_wave": result.extended_wave,
                        "channel_type": result.channel_type,
                        "equality_ratio": result.equality_ratio,
                        "equality_status": result.equality_status,
                        "internal_structure": result.internal_structure_status,
                        "violations": result.violations,
                        "description": result.description,
                        "page_reference": result.page_reference,
                        "ratio_w3_w1": round(result.ratio_w3_to_w1, 4),
                        "ratio_w5_w3": round(result.ratio_w5_to_w3, 4),
                        "ratio_w2_ret": round(result.ratio_w2_ret_w1, 4),
                        "ratio_w4_ret": round(result.ratio_w4_ret_w3, 4),
                    })
        
            # الگوی نزولی
            elif (p0["type"] == "HIGH" and p1["type"] == "LOW" and p2["type"] == "HIGH" and 
                  p3["type"] == "LOW" and p4["type"] == "HIGH" and p5["type"] == "LOW"):
                if p1["price"] < p0["price"] and p3["price"] < p1["price"] and p5["price"] < p3["price"]:
                    impulse = ImpulseWave(
                        w0=WavePoint(p0["index"], p0["price"], p0["index"]),
                        w1=WavePoint(p1["index"], p1["price"], p1["index"]),
                        w2=WavePoint(p2["index"], p2["price"], p2["index"]),
                        w3=WavePoint(p3["index"], p3["price"], p3["index"]),
                        w4=WavePoint(p4["index"], p4["price"], p4["index"]),
                        w5=WavePoint(p5["index"], p5["price"], p5["index"]),
                    )
                    result = ImpulseAnalyzer.classify_impulse(impulse, is_potential_start=(i==0))
                    patterns.append({
                        "type": "نزولی",
                        "direction": "DOWN",
                        "category": result.category.value,
                        "sub_type": result.sub_type.value,
                        "start_idx": p0["index"],
                        "end_idx": p5["index"],
                        "start_price": p0["price"],
                        "end_price": p5["price"],
                        "has_overlap": result.has_overlap,
                        "is_truncated": result.is_truncated,
                        "extended_wave": result.extended_wave,
                        "channel_type": result.channel_type,
                        "equality_ratio": result.equality_ratio,
                        "equality_status": result.equality_status,
                        "internal_structure": result.internal_structure_status,
                        "violations": result.violations,
                        "description": result.description,
                        "page_reference": result.page_reference,
                        "ratio_w3_w1": round(result.ratio_w3_to_w1, 4),
                        "ratio_w5_w3": round(result.ratio_w5_to_w3, 4),
                        "ratio_w2_ret": round(result.ratio_w2_ret_w1, 4),
                        "ratio_w4_ret": round(result.ratio_w4_ret_w3, 4),
                    })

    # اگر از context دریافت نشد، خودمان استخراج می‌کنیم
    if not patterns:
        patterns = detect_impulse_patterns(
            close.tolist(), 
            high.tolist(), 
            low.tolist(),
            pivot_threshold=0.5
        )
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۳: فیلتر کردن الگوهای نامعتبر و آمار الگوها
    # ════════════════════════════════════════════════════════════
    
    # فیلتر کردن الگوهای با نقض شدید (بیش از ۲ نقض)
    valid_patterns = [p for p in patterns if len(p["violations"]) <= 2]
    
    # استفاده از valid_patterns برای آمارگیری به جای patterns خام
    total_patterns = len(valid_patterns)
    trending_count = len([p for p in valid_patterns if p["category"] == "شتابدار_روند_دار"])
    terminal_count = len([p for p in valid_patterns if p["category"] == "شتابدار_ترمینال"])
    leading_diag_count = len([p for p in valid_patterns if p["category"] == "قطری_پیشرو"])
    truncated_count = len([p for p in valid_patterns if p["is_truncated"]])
    with_violations = len([p for p in valid_patterns if p["violations"]])
    
    # بقیه آمارها نیز باید از valid_patterns محاسبه شوند
    ext_1_count = len([p for p in valid_patterns if p["extended_wave"] == 1])
    ext_3_count = len([p for p in valid_patterns if p["extended_wave"] == 3])
    ext_5_count = len([p for p in valid_patterns if p["extended_wave"] == 5])
    double_ext_count = len([p for p in valid_patterns if p["sub_type"] == "امتداد_دوگانه"])
    
    converging = len([p for p in valid_patterns if p["channel_type"] == "همگرا"])
    diverging = len([p for p in valid_patterns if p["channel_type"] == "واگرا_مگافون"])
    parallel = len([p for p in valid_patterns if p["channel_type"] == "موازی"])
    
    equal_count = len([p for p in valid_patterns if p["equality_status"] == "برابر"])
    fib_equal_count = len([p for p in valid_patterns if p["equality_status"] == "نزدیک_برابر_فیبو"])
    unbalanced_count = len([p for p in valid_patterns if p["equality_status"] == "نامتوازن"])
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۴: ساخت خروجی
    # ════════════════════════════════════════════════════════════
    results = {
        # ── شناسنامه ──
        "عنوان": "فصل ۱۱: دسته‌بندی امواج شتابدار (Impulse Waves Classification)",
        "مرجع_کتاب": "صفحات ۵۵ تا ۱۱۹ - گلن نیلی",
        "وضعیت": "تحلیل_کامل",
        
        # ── اطلاعات پایه ──
        "تعداد_کندل": str(n),
        "قیمت_شروع": str(round(close[0], 4)),
        "قیمت_پایانی": str(round(close[-1], 4)),
        "بالاترین_قیمت": str(round(float(np.max(high)), 4)),
        "پایین‌ترین_قیمت": str(round(float(np.min(low)), 4)),
        
        # ── آمار کلی الگوها ──
        "تعداد_کل_الگوهای_شتابدار": str(total_patterns),
        "شتابدار_روند_دار": str(trending_count),
        "شتابدار_ترمینال": str(terminal_count),
        "قطری_پیشرو": str(leading_diag_count),
        "موج_۵_کوتاه_شده": str(truncated_count),
        "الگوهای_با_نقض_قانون": str(with_violations),
        
        # ── آمار موج ممتد ──
        "موج_۱_ممتد": str(ext_1_count),
        "موج_۳_ممتد": str(ext_3_count),
        "موج_۵_ممتد": str(ext_5_count),
        "امتداد_دوگانه": str(double_ext_count),
        
        # ── آمار کانال‌بندی ──
        "کانال_همگرا": str(converging),
        "کانال_واگرا_مگافون": str(diverging),
        "کانال_موازی": str(parallel),
        
        # ── آمار قانون برابری ──
        "قانون_برابری_کامل": str(equal_count),
        "قانون_برابری_فیبوناچی": str(fib_equal_count),
        "قانون_برابری_نامتوازن": str(unbalanced_count),
        
        # ── اصول اساسی (صفحه ۵۵) ──
        "اصل_دسته‌بندی": "امواج شتابدار بر اساس میزان اصلاح موج ۳ توسط موج ۴ و ساختار داخلی به دو دسته تقسیم می‌شوند",
        "شرط_روند_دار": "هیچ بخشی از موج ۴ نمی‌تواند وارد قلمرو موج ۲ شود",
        "شرط_ترمینال": "همپوشانی موج ۴ با قلمرو موج ۲ الزامی است",
        "نقطه_مشترک": "عدم اصلاح ۱۰۰ درصدی موج ۳ توسط موج ۴",
        
        # ── قوانین نقض‌ناپذیر عمومی (صفحه ۵۶) ──
        "قانون_۱_موج_۲": "موج ۲ نمی‌تواند ۱۰۰٪ موج ۱ را اصلاح کند",
        "قانون_۲_موج_۴": "موج ۴ نمی‌تواند ۱۰۰٪ موج ۳ را اصلاح کند",
        "قانون_۳_موج_۳_کوتاه": "موج ۳ هیچگاه کوتاه‌ترین موج قیمتی در میان ۱، ۳ و ۵ نیست",
        "قانون_۴_موج_۳_پایان": "موج ۳ بایستی فراتر از انتهای موج ۱ خاتمه یابد",
        "قانون_۵_کانال_۰_۲": "هیچ بخشی از موج ۱ و ۳ نبایستی از خط کانال ۲-۰ عبور کند (مگر ترمینال)",
        "قانون_۶_کانال_۲_۴": "هیچ بخشی از موج ۳ و ۵ نبایستی از خط کانال ۲-۴ عبور کند (مگر ترمینال)",
        "قانون_۷_موج_۲_مثلث": "موج ۲ نمی‌تواند به فرم الگوی مثلثی باشد، مگر در ترمینال با موج ۱ ممتد",
        "قانون_۸_موج_۲_جاری": "در موج ۲ جاری، موج B نبایستی از ۶۱.۸ درصد موج ۱ + انتهای موج ۱ فراتر رود",
        
        # ── الزامات قیمتی (صفحه ۵۶) ──
        "الزام_موج_۵_حداقل_۳۸": "موج ۵ باید حداقل ۳۸.۲٪ موج ۴ را بازگشت کند",
        "الزام_موج_۵_حداکثر_۳۳": "موج ۵ نباید کمتر از ۳۳٪ موج ۱ یا ۳ باشد (مگر کوتاه شده)",
        "الزام_موج_۴_حداکثر_۶۱": "موج ۴ نباید بیش از ۶۱.۸٪ موج ۳ را اصلاح کند (مگر ترمینال یا کوتاه شده)",
        "الزام_موج_ممتد_۱۶۱": "بلندترین موج باید ۱۶۱.۸٪ موج بلند پیش از خود باشد",
        "الزام_اصلاح_موج_۲_۴_حداقل_۳۳": "موج ۲ و ۴ ترجیحاً حداقل ۳۳ درصد موج بیش از خود را اصلاح کنند",
        "الزام_موج_۳_حداقل_۶۱": "موج ۳ باید حداقل ۶۱.۸٪ موج ۱ باشد",
        "الزام_حداکثر_رشد_۲۶۱": "امواج شتابدار نباید بیش از ۲۶۱.۸٪ موج پیشین باشند (نهایت ۳۶۱.۸٪)",
        
        # ── الزامات زمانی (صفحه ۵۷) ──
        "زمان_موج_۲_تک_موج_روند_دار": "موج ۲ تک‌موج در روند دار هرگز نمی‌تواند بیش از ۶۱.۸٪ موج ۱ را اصلاح کند",
        "زمان_موج_۲_تک_موج_ترمینال": "موج ۲ تک‌موج در ترمینال می‌تواند تا ۹۹٪ موج ۱ را اصلاح کند",
        "زمان_موج_۳_تک_موج_روند_دار": "موج A تا ۷۰٪ اصلاح، موج C نبایستی بیش از ۶۱.۸ موج ۱ خاتمه یابد",
        "زمان_موج_۳_تک_موج_ترمینال": "موج A و C می‌توانند تا ۹۹٪ موج ۱ را اصلاح کنند",
        "زمان_موج_۲_کمتر_از_موج_۱": "موج ۲ و ۴ نبایستی زمانی کمتر از موج ۱ و ۳ صرف کنند (مگر ترمینال)",
        "زمان_موج_۴_حداکثر_۳۰_درصد": "موج ۴ اغلب حداکثر ۳۰٪ زمان موج ۱ را صرف می‌کند",
        "زمان_موج_۵_حداکثر_۳۰_درصد": "موج ۵ اغلب حداکثر ۳۰٪ زمان موج ۳ را صرف می‌کند",
        "زمان_موج_۵_مجموع_۱_تا_۳": "موج ۵ نباید زمانی بیش از مجموع زمان موج ۱ تا ۳ داشته باشد",
        "زمان_قانون_نصف_مجموع": "اگر زمان دو موج اول متفاوت باشد، موج سوم برابر نصف مجموع آن‌هاست",
        "زمان_موج_۲_کمتر_۲_برابر": "اگر زمان موج ۲ کمتر از ۲ برابر موج ۱ باشد، موج ۳ حداقل به اندازه زمان موج ۱ است",
        "زمان_موج_۲_حدود_۱۶۱_موج_۱": "اگر زمان موج ۲ حدود ۱۶۱.۸٪ موج ۱ باشد، موج ۳ برابر زمان از ابتدای ۱ تا انتهای ۲ است",
        "زمان_موج_۲_و_۴_۱۶۱_پیشین": "زمان صرف شده توسط موج ۲ و ۴ معمولاً ۱۶۱.۸٪ زمان امواج شتابدار پیشین است",
        "قانون_شتاب_زمانی": "شتاب‌های زمانی در الگوهای شتابدار رایج‌تر از شتاب‌های قیمتی است",
        
        # ── قوانین کلی تکمیلی (صفحه ۵۸) ──
        "قانون_زمان_موج_سوم_نصف": "اگر دو موج اول زمانی متفاوت باشند، موج سوم برابر نصف مجموع آن‌هاست",
        "قانون_زمان_بیشتر_از_۳_قطعه": "قطعه در حال تکمیل نباید زمانی بیش از مجموع ۳ قطعه پیشین داشته باشد",
        "قانون_پیچیدگی_موج_۲_و_۴": "سطح پیچیدگی موج ۲ و ۴ نباید کمتر از سطح پیچیدگی موج شتابدار پیشین باشد",
        "قانون_درجه_کوچکتر_قلمرو": "امواج درجه کوچکتر نبایستی قلمرو قیمتی و زمانی بیشتری نسبت به درجه بالاتر داشته باشند",
        "قانون_شیب_درجه_کوچکتر": "شیب امواج درجه کوچکتر اغلب بیشتر از شیب امواج درجه بالاتر است",
        "قانون_اصلاح_قبل_ممتد": "موج اصلاحی قبل از موج ممتد معمولاً بیش از ۶۱.۸٪ اصلاح نمی‌کند",
        "قانون_اصلاح_بعد_ممتد": "موج اصلاحی بعد از موج ممتد معمولاً کمتر از ۶۱.۸٪ بازگشت می‌شود",
        "قانون_بسط_بعد_اصلاح_بسط": "موج شتابدار بخشیده شده بایستی بعد از یک اصلاح بخشیده شده قرار گیرد",
        "قانون_نقض_رفتن_به_اصلاحی": "در صورت نقض هر یک از قوانین فوق، بایستی به بخش الگوهای اصلاحی مراجعه شود",
        
        # ── انواع شتابدار روند دار ──
        "روند_دار_ساده_نام": "شتابدار روند دار ساده (Simple Trending Impulse)",
        "روند_دار_ساده_صفحه": "صفحه ۵۹",
        "روند_دار_ساده_توضیح": "بدون هر گونه ریزموج. قوانین کلی الیوت صدق می‌کند. رایج‌ترین نوع. در جهت روند بزرگتر.",
        
        "روند_دار_موج_۱_نام": "شتابدار روند دار با موج ۱ ممتد (1st Extension Trending)",
        "روند_دار_موج_۱_صفحه": "صفحه ۶۱",
        "روند_دار_موج_۱_توضیح": "توالی پنج موجی در قالب گوه‌ای شکل به پایان می‌رسد. موج ۲ پیچیده‌تر از موج ۴. اغلب نباید بیش از ۳۸٪ اصلاح کند. موج ۲ نمی‌تواند جاری باشد. موج ۵ نمی‌تواند بیش از ۹۹٪ موج ۳ باشد.",
        
        "روند_دار_موج_۳_نام": "شتابدار روند دار با موج ۳ ممتد (3rd Extension Trending)",
        "روند_دار_موج_۳_صفحه": "صفحه ۶۳",
        "روند_دار_موج_۳_توضیح": "موج ۲ بیش از ۶۱.۸٪ اصلاح. موج ۴ معمولاً کمتر از ۳۸.۲٪ اصلاح. موج ۳ بیش از ۱۶۱.۸٪ و معمولاً تا ۲۶۱.۸٪ موج ۱. موج ۵ کمتر از ۶۱.۸٪ موج ۳. اغلب موج ۲ پیچیده‌تر از موج ۴.",
        
        "روند_دار_موج_۵_نام": "شتابدار روند دار با موج ۵ ممتد (5th Extension Trending)",
        "روند_دار_موج_۵_صفحه": "صفحه ۶۷",
        "روند_دار_موج_۵_توضیح": "امواج ۱ و ۳ زمانی برابر یا با نسبت ۶۱.۸. موج ۳ حداقل ۱۰۰ و حداکثر ۱۶۱.۸٪ موج ۱. موج ۴ زمانبر و پیچیده. موج ۴ حداکثر ۶۱.۸٪ موج ۳. موج ۵ حداقل به اندازه ۱ تا ۳ و حداکثر ۲۶۱.۸٪ آن. پایان زیر خط روند ۱-۳.",
        
        "روند_دار_دوگانه_نام": "شتابدار روند دار با امتداد دوگانه (Double Extension Trending)",
        "روند_دار_دوگانه_صفحه": "صفحه ۷۰",
        "روند_دار_دوگانه_توضیح": "موج ۳ ورای ۱۶۱.۸٪ موج ۱. موج ۵ ورای ۱۶۱.۸٪ موج ۳ یا ۱۰۰٪ ۱ تا ۳. موج ۴ زمانبر و پیچیده. پایان ورای خط روند ۱-۳. بسیار نادر.",
        
        "روند_دار_کوتاه_نام": "شتابدار روند دار با موج ۵ کوتاه شده (Truncated Impulse)",
        "روند_دار_کوتاه_صفحه": "صفحه ۷۳",
        "روند_دار_کوتاه_توضیح": "قله موج ۵ زیر موج ۳. واگرایی منفی. امتداد در موج ۳ الزامی. اخطار تضعیف و تغییر روند. موج ۴ پیچیده‌ترین و بیش از ۶۱.۸٪ موج ۳. فقط در موج ۵ یا C. کل الگو باید بازگشت شود.",
        
        # ── قطری پیشرو ──
        "قطری_پیشرو_نام": "الگوی قطری پیشرو (Leading Diagonal)",
        "قطری_پیشرو_صفحه": "صفحه ۷۶",
        "قطری_پیشرو_ساختار": "۵-۳-۵-۳-۵",
        "قطری_پیشرو_مکان": "فقط در موج ۱ یا A رخ می‌دهد",
        "قطری_پیشرو_همپوشانی": "موج ۴ با موج ۱ همپوشانی دارد",
        "قطری_پیشرو_کوتاه_شدگی": "نمی‌تواند همراه با کوتاه‌شدگی باشد",
        "قطری_پیشرو_موج_۲_بازگشت": "موج ۲ نمی‌تواند به نقطه ابتدایی موج ۱ بازگردد",
        "قطری_پیشرو_موج_۲_مثلث": "موج ۲ نمی‌تواند به شکل الگوی اصلاحی مثلث باشد",
        "قطری_پیشرو_موج_۳_قله": "موج ۳ قله موج ۱ را همواره فتح می‌کند و شتابدار است",
        "قطری_پیشرو_توضیح": "نشان از شروع افت یا رشد شارپی. معمولاً ۱۰۰٪ اصلاح می‌گردد.",
        
        # ── انواع شتابدار ترمینال ──
        "ترمینال_ساده_نام": "شتابدار ترمینال ساده (Simple Terminal)",
        "ترمینال_ساده_صفحه": "صفحه ۷۸",
        "ترمینال_ساده_ساختار": "۳-۳-۳-۳-۳",
        "ترمینال_ساده_توضیح": "ساختار متفاوت. در جهت روند. شروع افت یا رشد شارپی (۱۰۰٪ اصلاح). پس از حرکت شارپی رخ می‌دهد. موج ۵ اغلب کوتاه شده. همپوشانی الزامی. موج ۲ مثلث ممنوع مگر با موج ۱ ممتد. موج ۳ قله موج ۱ را فتح می‌کند. موج ۵ حداقل ۳۸.۲٪ موج ۴. شیب کانال غیر افقی. فقط در موج ۵ یا C.",
        
        "ترمینال_موج_۱_نام": "ترمینال با موج ۱ ممتد (1st Extension Terminal)",
        "ترمینال_موج_۱_صفحه": "صفحه ۷۹",
        "ترمینال_موج_۱_توضیح": "موج ۱ بلندترین (نه الزاماً ۱۶۱.۸٪). موج ۲ حداکثر ۶۱.۸٪. موج ۳ بین ۳۸.۲ تا ۶۱.۸٪ موج ۱. موج ۵ حداکثر ۹۹٪ موج ۳. کانال‌بندی بر اساس نسبت موج ۲ و ۴.",
        
        "ترمینال_موج_۳_نام": "ترمینال با موج ۳ ممتد (3rd Extension Terminal)",
        "ترمینال_موج_۳_صفحه": "صفحه ۸۵",
        "ترمینال_موج_۳_توضیح": "بسیار نادر. موج ۳ بلندترین (نه الزاماً ۱۶۱.۸٪). موج ۲ بیش از ۶۱.۸٪. موج ۴ کمتر از ۳۸.۲٪. موج ۵ حداکثر ۶۱.۸٪ موج ۳. معمولاً در موج C. خط روند ۱-۳ توسط موج ۵ شکسته شود. کانال‌بندی بر اساس نسبت موج ۲ و ۴.",
        
        "ترمینال_موج_۵_نام": "ترمینال با موج ۵ ممتد (5th Extension Terminal)",
        "ترمینال_موج_۵_صفحه": "صفحه ۸۶",
        "ترمینال_موج_۵_توضیح": "رایج‌ترین ترمینال. موج ۵ بلندترین (نه الزاماً ۱۶۱.۸٪). موج ۳ بیش از ۱۰۰٪ موج ۱. موج ۵ بیش از ۱۰۰٪ مجموع ۱ تا ۳ و حداکثر ۱۶۱.۸٪ آن. موج ۴ بیش از ۵۰٪ موج ۳. موج ۴ بلندتر و زمانبرتر از موج ۲. اندکی انحراف (برخلاف مثلث انبساطی).",
        
        "ترمینال_کوتاه_نام": "ترمینال با موج ۵ کوتاه شده (5th Failure Terminal)",
        "ترمینال_کوتاه_صفحه": "صفحه ۸۹",
        "ترمینال_کوتاه_توضیح": "موج ۳ بلندترین. موج ۵ حداقل ۳۸.۲٪ موج ۱ و نه پیچیده‌تر از ۱ و ۳. موج ۴ بیش از ۶۱.۸ تا ۹۹٪ موج ۳. موج ۴ بلندتر از موج ۲. خط روند ۱-۵ توسط موج ۳ شکسته شده. تفاوت آشکار موج ۲ و ۴.",
        
        # ── خطوط روند (صفحات ۹۰ تا ۱۰۱) ──
        "خط_روند_۰_۲_تعریف": "از ابتدای موج صعودی تا نقطه احتمالی پایان موج ۲ رسم می‌شود",
        "خط_روند_۰_۲_تایید": "تا زمانی که به سمت پایین شکسته نشود، موج ۲ خاتمه نیافته",
        "خط_روند_۰_۲_نقض_موج_۱_و_۳": "هیچ بخشی از موج ۱ و ۳ نباید آن را بشکند (مگر ترمینال با شدت کم)",
        "خط_روند_۰_۲_مجاز_موج_۲": "مجاز است بخشی از موج ۲ آن را partially بشکند",
        "خط_روند_۲_۴_تعریف": "پس از تأیید شروع موج ۳، از انتهای موج ۲ و ۴ رسم می‌شود",
        "خط_روند_۲_۴_نقض_موج_۳_و_۵": "هیچ بخشی از موج ۳ و ۵ نباید آن را بشکند (مگر ترمینال با شدت کم)",
        "خط_روند_۲_۴_شکست_پس_از_۵": "پس از تکمیل ۵، باید در زمان کمتر از موج ۵ شکسته شود",
        "خط_روند_۲_۴_موج_۴_در_حال_توسعه": "اگر پیش از انتهای ۳ بشکند و اصلاح عمیق نباشد، موج ۴ در حال توسعه است",
        "خط_روند_۲_۴_شکست_سریع_ناقص": "اگر به سرعت و شدت شکسته شود، موج ۵ ناقص رخ داده است",
        "خط_روند_۲_۴_بازنگری_مثلث": "بازنگری مکرر خط روند ۲-۴ نشانه در حال توسعه بودن مثلث است",
        "خط_روند_۲_۴_شکست_کاذب_ترمینال": "شکست بی‌اهمیت و مکرر خط ۲-۴ نشانه تشخیص ترمینال در موج ۵ است",
        "خط_روند_۲_۴_زمان_بازگشت_ترمینال": "اگر شکست در زمان کمتر از زمان موج ۵ رخ داد، پایان موج ۵ تایید می‌گردد",
        
        # ── کانال‌بندی (صفحات ۹۸ تا ۱۰۸) ──
        "کانال_موج_۴_محدوده": "به موازات خط ۱-۳ از انتهای موج ۲ خطی رسم کنیم تا محدوده موج ۴ یافت شود",
        "کانال_موج_۴_نقض": "اگر روند بدون سقف جدید خط ۴-۲ را بشکند، موج ۴ تکمیل نشده است",
        "کانال_موج_۵_خطوط": "پس از موج ۴، خط موازی ۲-۴ از انتهای ۱-۳ و خط وسط رسم می‌شود",
        "کانال_موج_۵_پتانسیل": "این خطوط پتانسیل شکل‌گیری سقف موج ۵ را دارند",
        "کانال_موج_۱_ممتد_همگرا": "به هم فشردگی خطوط خصیصه طبیعی موج ۱ ممتد است",
        "کانال_موج_۳_ممتد_شیب_ملایم": "اگر شیب موج ۳ ملایم باشد و کانال ۰-۲ را نشکند، موج ۵ زیر خط روند باقی می‌ماند",
        "کانال_موج_۳_ممتد_شیب_تند": "اگر شیب موج ۳ تند باشد، کانال ۰-۲ را می‌شکند",
        "کانال_موج_۵_ممتد_شپور": "شکل شپور (مگافون) کانال‌بندی نمونه موج ۵ ممتد است. موج ۵ زیر خط روند باقی می‌ماند.",
        
        # ── تایید پساالگو (صفحات ۱۱۰ تا ۱۱۳) ──
        "تایید_پساالگو_مرحله_۱_تعریف": "حرکت پسا الگو طی دو مرحله آن را تایید می‌کند",
        "تایید_مرحله_۱_شکست_زمان": "خط روند ۲-۴ باید در زمان کوتاهتر یا برابر موج ۵ شکسته شود",
        "تایید_مرحله_۱_اصلاح_موج_۵": "اغلب بیشتر از ۶۱.۸٪ موج ۵ را اصلاح می‌کند",
        "تایید_مرحله_۲_موج_۱_ممتد": "اصلاح تا قلمرو موج ۴ پنج موجی (کمتر از ۶۱.۸٪ کل)",
        "تایید_مرحله_۲_موج_۳_ممتد": "اصلاح تا حوالی موج ۴ پنج موجی (کمتر از ۶۱.۸٪ کل)",
        "تایید_مرحله_۲_موج_۵_ممتد": "اصلاح تا حوالی موج ۲ پنج موجی (حدود ۶۱.۸٪ کل)",
        "تایید_مرحله_۲_موج_۵_کوتاه": "موج ۵ کوتاه شده دلیل محکمی بر قدرت روند اصلاحی پس از آن است",
        "تایید_مرحله_۲_ترمینال_زمان": "کل ترمینال در زمان ۵۰٪ یا کمتر از زمان تکمیل، اصلاح می‌شود",
        "تایید_مرحله_۲_ترمینال_کف_سقف": "کف یا سقف ترمینال حداقل برای دو برابر مدت زمان این الگو شکسته نخواهد شد",
        
        # ── قانون امتداد (صفحه ۱۱۵) ──
        "قانون_امتداد_حیاتی": "امتداد یک عنصر حیاتی در هر الگوی شتابدار روند دار است",
        "قانون_امتداد_کاندیدا": "بلندترین موج کاندیدای موج ممتد خواهد بود",
        "قانون_امتداد_۱۶۱_یا_کوتاهترین": "موج ممتد باید ۱۶۱.۸٪ موج بلند پیشین یا کوتاهترین موج باشد",
        "قانون_امتداد_ترمینال_استثنا": "در الگوی شتابدار ترمینال الزامی نسبت به ۱۶۱.۸ درصد نمی‌باشد",
        "قانون_امتداد_استثنا_۱": "موج ۱ ممتد ممکن است اندکی کوتاهتر از ۱۶۱.۸٪ موج ۳ باشد",
        "قانون_امتداد_استثنا_۲": "موج ۳ ممتد کمتر از ۱۶۱.۸٪ موج ۱ + موج ۵ کوتاهتر = احتمالاً ترمینال",
        "قانون_امتداد_نقض_نتیجه": "نقض قانون امتداد بدون استثناها = قطعاً الگوی اصلاحی",
        
        # ── قانون برابری (صفحه ۱۱۶) ──
        "قانون_برابری_تعریف": "دو موج غیر ممتد باید از نظر زمان، قیمت یا پیچیدگی گرایش به برابری داشته باشند",
        "قانون_برابری_نسبت_فیبو": "با یک نسبت فیبوناچی (معمولاً ۶۱.۸) در بعد زمان یا قیمت مرتبط می‌شوند",
        "قانون_برابری_بیشترین_نمود": "بیشترین نمود زمانی که موج ۳ ممتد باشد",
        "قانون_برابری_کمترین_نمود": "کمترین نمود در ترمینال یا موج ۱ ممتد",
        "قانون_برابری_موج_۱_ممتد": "اگر موج ۱ ممتد باشد قانون عطف به موج‌های ۳ و ۵ می‌شود",
        "قانون_برابری_موج_۳_ممتد": "اگر موج ۳ ممتد باشد قانون عطف به موج‌های ۱ و ۵ می‌شود",
        "قانون_برابری_موج_۵_ممتد": "اگر موج ۵ ممتد باشد قانون عطف به موج‌های ۱ و ۳ می‌شود",
        
        # ── مکان وقوع (صفحه ۱۱۷) ──
        "مکان_شتابدار_روند_دار": "در موج‌های ۱، ۳، ۵، A، C",
        "مکان_ترمینال": "فقط و فقط در موج ۵ یا موج C شتابدار روند دار",
        "مکان_قطری_پیشرو": "فقط و فقط در موج ۱ یا A",
        
        # ── وضعیت ساختار داخلی ──
        "ساختار_داخلی_توضیح": "بررسی دقیق ساختار داخلی (۵-۳-۵-۳-۵ یا ۳-۳-۳-۳-۳) نیاز به داده‌های فریم زمانی پایین‌تر دارد. در این تحلیل بر اساس نوع الگو فرض می‌شود.",
    }
    
    # ── اضافه کردن جزئیات الگوهای شناسایی‌شده ────────────────
    for idx, pattern in enumerate(valid_patterns[:15]):
        prefix = f"الگو_{idx + 1}"
        results[f"{prefix}_نوع"] = pattern["type"]
        results[f"{prefix}_دسته"] = pattern["category"]
        results[f"{prefix}_زیرنوع"] = pattern["sub_type"]
        results[f"{prefix}_شروع"] = str(round(pattern["start_price"], 4))
        results[f"{prefix}_پایان"] = str(round(pattern["end_price"], 4))
        results[f"{prefix}_موج_ممتد"] = str(pattern["extended_wave"]) if pattern["extended_wave"] else "خیر"
        results[f"{prefix}_همپوشانی"] = "بله" if pattern["has_overlap"] else "خیر"
        results[f"{prefix}_کوتاه_شده"] = "بله" if pattern["is_truncated"] else "خیر"
        results[f"{prefix}_کانال"] = pattern["channel_type"]
        results[f"{prefix}_برابری_نسبت"] = str(round(pattern["equality_ratio"], 4))
        results[f"{prefix}_برابری_وضعیت"] = pattern["equality_status"]
        results[f"{prefix}_ساختار_داخلی"] = pattern["internal_structure"]
        results[f"{prefix}_نسبت_موج_۳_به_۱"] = str(pattern["ratio_w3_w1"])
        results[f"{prefix}_نسبت_موج_۵_به_۳"] = str(pattern["ratio_w5_w3"])
        results[f"{prefix}_اصلاح_موج_۲"] = f"{pattern['ratio_w2_ret'] * 100:.1f}%"
        results[f"{prefix}_اصلاح_موج_۴"] = f"{pattern['ratio_w4_ret'] * 100:.1f}%"
        results[f"{prefix}_مرجع"] = pattern["page_reference"]
        if pattern["violations"]:
            results[f"{prefix}_نقض_قوانین"] = " | ".join(pattern["violations"][:3])
    
    # ── تفسیر نهایی ──
    results["تفسیر_نهایی"] = _build_final_interpretation(results, valid_patterns, n)
    
    # ── ثبت در لاگ ──
    if logger:
        _write_to_logger(logger, results, valid_patterns)
    
    return results


# ════════════════════════════════════════════════════════════════
# بخش ۵: تفسیر نهایی
# ════════════════════════════════════════════════════════════════

def _build_final_interpretation(results: Dict, patterns: List[Dict], n: int) -> str:
    """تولید تفسیر متنی کامل مطابق کتاب"""
    
    pattern_summary = ""
    if patterns:
        pattern_lines = []
        for idx, p in enumerate(patterns[:5]):
            pattern_lines.append(
                f"  {idx + 1}. {p['type']} | {p['sub_type']} | "
                f"موج ممتد: {p['extended_wave'] if p['extended_wave'] else 'خیر'} | "
                f"برابری: {p['equality_status']} ({p['equality_ratio']:.2f}) | "
                f"اصلاح ۲: {p['ratio_w2_ret'] * 100:.1f}% | اصلاح ۴: {p['ratio_w4_ret'] * 100:.1f}% | "
                f"ساختار: {p['internal_structure']} | "
                f"مرجع: {p['page_reference']}"
            )
        pattern_summary = "\n".join(pattern_lines)
    else:
        pattern_summary = "  هیچ الگوی شتابدار معتبر در داده‌های فعلی شناسایی نشد."
    
    violation_warning = ""
    violated = [p for p in patterns if p["violations"]]
    if violated:
        violation_warning = f"\n  ⚠️ {len(violated)} الگو دارای نقض قانون (قیمتی یا زمانی) هستند. نیاز به بازبینی برچسب‌گذاری دارد."
    else:
        violation_warning = "\n  ✓ تمام الگوهای شناسایی‌شده قوانین نقض‌ناپذیر قیمتی و زمانی را رعایت کرده‌اند."
    
    equality_summary = f"\n  • برابر کامل: {results.get('قانون_برابری_کامل', '0')} | فیبوناچی: {results.get('قانون_برابری_فیبوناچی', '0')} | نامتوازن: {results.get('قانون_برابری_نامتوازن', '0')}"
    
    return f"""
═══════════════════════════════════════════════════════════════════
  فصل ۱۱: دسته‌بندی امواج شتابدار (Impulse Waves Classification)
  مرجع: صفحات ۵۵ تا ۱۱۹ | گلن نیلی | سبک نئوویو
═══════════════════════════════════════════════════════════════════

📐 اصل اساسی دسته‌بندی (صفحه ۵۵):

  "امواج شتابدار بر اساس میزان اصلاح موج ۳ توسط موج ۴ و همچنین ساختار 
   داخلی امواج به دو دسته کلی تقسیم می‌شوند:
   - شتابدار روند دار (Trending Impulse): بدون همپوشانی موج ۴ با موج ۲
   - شتابدار ترمینال (Terminal Impulse): همپوشانی الزامی
   - قطری پیشرو (Leading Diagonal): همپوشانی دارد اما فقط در موج ۱ یا A"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 آمار داده‌های فعلی:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • تعداد کندل‌ها: {n}
  • کل الگوهای شناسایی‌شده: {len(patterns)}
  • شتابدار روند دار: {results.get('شتابدار_روند_دار', '0')}
  • شتابدار ترمینال: {results.get('شتابدار_ترمینال', '0')}
  • قطری پیشرو: {results.get('قطری_پیشرو', '0')}
  • موج ۵ کوتاه شده: {results.get('موج_۵_کوتاه_شده', '0')}
{violation_warning}

📊 وضعیت قانون برابری (صفحه ۱۱۶):{equality_summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 الگوهای شناسایی‌شده:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pattern_summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 انواع شتابدار روند دار (صفحات ۵۹ تا ۷۵):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌─────────────────────────────────────────────────────────────────┐
  │ ساده (ص ۵۹): بدون ریزموج. رایج‌ترین نوع.                     │
  ├─────────────────────────────────────────────────────────────────┤
  │ موج ۱ ممتد (ص ۶۱): موج ۱ بلندترین. موج ۲ پیچیده. کانال همگرا. │
  │   توالی در قالب گوه‌ای. موج ۲ حداکثر ۳۸٪ اصلاح.               │
  ├─────────────────────────────────────────────────────────────────┤
  │ موج ۳ ممتد (ص ۶۳): موج ۲ عمیق (>۶۱.۸٪). موج ۴ کم عمق (<۳۸.۲٪). │
  │   موج ۳ تا ۲۶۱.۸٪ موج ۱. موج ۵ کمتر از ۶۱.۸٪ موج ۳.          │
  ├─────────────────────────────────────────────────────────────────┤
  │ موج ۵ ممتد (ص ۶۷): موج ۵ بلندترین. موج ۴ زمانبر. کانال مگافون.│
  │   موج ۳ بین ۱۰۰ تا ۱۶۱.۸٪ موج ۱. پایان زیر خط روند ۱-۳.      │
  ├─────────────────────────────────────────────────────────────────┤
  │ امتداد دوگانه (ص ۷۰): موج ۳ و ۵ هر دو >۱۶۱.۸٪ موج قبل. نادر.│
  ├─────────────────────────────────────────────────────────────────┤
  │ موج ۵ کوتاه (ص ۷۳): قله موج ۵ زیر موج ۳. واگرایی منفی.      │
  │   اخطار تغییر روند. موج ۴ پیچیده‌ترین و >۶۱.۸٪.               │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 الگوی قطری پیشرو (صفحه ۷۶):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌─────────────────────────────────────────────────────────────────┐
  │ ساختار: ۵-۳-۵-۳-۵. مکان: فقط در موج ۱ یا A.                  │
  │ همپوشانی الزامی. نمی‌تواند کوتاه شده باشد.                     │
  │ موج ۲ به ابتدای ۱ بازنمی‌گردد و مثلث نیست.                    │
  │ موج ۳ قله ۱ را فتح می‌کند. نشان شروع رشد/افت شارپی.           │
  │ معمولاً ۱۰۰٪ اصلاح می‌گردد.                                    │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 انواع شتابدار ترمینال (صفحات ۷۸ تا ۸۹):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌─────────────────────────────────────────────────────────────────┐
  │ ساده (ص ۷۸): ساختار ۳-۳-۳-۳-۳. همپوشانی الزامی. ۱۰۰٪ اصلاح.  │
  │   فقط در موج ۵ یا C. موج ۵ اغلب کوتاه شده. شیب غیر افقی.     │
  ├─────────────────────────────────────────────────────────────────┤
  │ موج ۱ ممتد (ص ۷۹): موج ۱ بلندترین. موج ۲ حداکثر ۶۱.۸٪.        │
  ├─────────────────────────────────────────────────────────────────┤
  │ موج ۳ ممتد (ص ۸۵): بسیار نادر. موج ۲ >۶۱.۸٪. موج ۴ <۳۸.۲٪.  │
  │   معمولاً در موج C. موج ۵ خط ۱-۳ را می‌شکند.                 │
  ├─────────────────────────────────────────────────────────────────┤
  │ موج ۵ ممتد (ص ۸۶): رایج‌ترین ترمینال. موج ۵ >۱۰۰٪ مجموع ۱-۳.  │
  │   موج ۴ >۵۰٪ موج ۳. موج ۴ بلندتر و زمانبرتر از موج ۲.        │
  ├─────────────────────────────────────────────────────────────────┤
  │ موج ۵ کوتاه (ص ۸۹): موج ۳ بلندترین. موج ۴ >۶۱.۸ تا ۹۹٪.     │
  │   تفاوت آشکار موج ۲ و ۴ در قیمت/زمان/پیچیدگی.                │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ قوانین نقض‌ناپذیر عمومی و زمانی (صفحات ۵۶ و ۵۷):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • موج ۲ نمی‌تواند ۱۰۰٪ موج ۱ را اصلاح کند
  • موج ۴ نمی‌تواند ۱۰۰٪ موج ۳ را اصلاح کند
  • موج ۳ کوتاه‌ترین موج در میان ۱، ۳ و ۵ نیست
  • موج ۳ فراتر از انتهای موج ۱ خاتمه می‌یابد
  • موج ۱ و ۳ از خط کانال ۰-۲ عبور نمی‌کنند (مگر ترمینال)
  • موج ۳ و ۵ از خط کانال ۲-۴ عبور نمی‌کنند (مگر ترمینال)
  • موج ۵ حداقل ۳۸.۲٪ موج ۴ را بازگشت می‌کند
  • موج ۳ حداقل ۶۱.۸٪ موج ۱ است
  • موج ۲ زمانی کمتر از موج ۱ صرف نمی‌کند (مگر ترمینال)
  • موج ۴ زمانی کمتر از موج ۳ صرف نمی‌کند (مگر ترمینال)
  • موج ۵ زمانی بیش از مجموع موج ۱ تا ۳ ندارد

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📏 قانون امتداد و برابری (صفحات ۱۱۵ و ۱۱۶):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  قانون امتداد: موج ممتد باید ۱۶۱.۸٪ موج بلند پیشین باشد
  قانون برابری: دو موج غیر ممتد گرایش به برابری دارند (نسبت ۶۱.۸)
  
  اگر قانون امتداد نقض شود (بدون استثناها) → قطعاً الگوی اصلاحی است

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 نتیجه نئوویو:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   دسته‌بندی صحیح امواج شتابدار به تشخیص روند آینده کمک می‌کند.
   شتابدار روند دار: ادامه روند
   شتابدار ترمینال: شروع افت یا رشد شارپی معکوس
   قطری پیشرو: شروع روند جدید (موج ۱ یا A)
   موج ۵ کوتاه شده: اخطار قوی تغییر روند
   
   {results.get('اصل_دسته‌بندی', '')}

═══════════════════════════════════════════════════════════════════
"""


# ════════════════════════════════════════════════════════════════
# بخش ۶: ثبت در لاگ
# ════════════════════════════════════════════════════════════════

def _write_to_logger(logger, results: Dict, patterns: List[Dict]):
    """ثبت نتایج در لاگر"""
    logger.add_section("فصل ۱۱: دسته‌بندی امواج شتابدار", level=1)
    logger.add_result("مرجع کتاب", "صفحات ۵۵ تا ۱۱۹ - گلن نیلی")
    logger.add_result("تعداد کندل", results["تعداد_کندل"])
    logger.add_result("کل الگوها", results["تعداد_کل_الگوهای_شتابدار"])
    logger.add_result("شتابدار روند دار", results["شتابدار_روند_دار"])
    logger.add_result("شتابدار ترمینال", results["شتابدار_ترمینال"])
    logger.add_result("قطری پیشرو", results["قطری_پیشرو"])
    logger.add_result("موج ۵ کوتاه شده", results["موج_۵_کوتاه_شده"])
    
    logger.add_section("آمار موج ممتد", level=2)
    logger.add_result("موج ۱ ممتد", results["موج_۱_ممتد"])
    logger.add_result("موج ۳ ممتد", results["موج_۳_ممتد"])
    logger.add_result("موج ۵ ممتد", results["موج_۵_ممتد"])
    logger.add_result("امتداد دوگانه", results["امتداد_دوگانه"])
    
    logger.add_section("آمار قانون برابری", level=2)
    logger.add_result("برابر کامل", results["قانون_برابری_کامل"])
    logger.add_result("نسبت فیبوناچی", results["قانون_برابری_فیبوناچی"])
    logger.add_result("نامتوازن", results["قانون_برابری_نامتوازن"])
    
    logger.add_section("الگوهای شناسایی‌شده", level=2)
    for idx, p in enumerate(patterns[:10]):
        logger.add_result(
            f"الگو {idx + 1} ({p['type']})",
            f"{p['sub_type']} | موج ممتد: {p['extended_wave'] if p['extended_wave'] else 'خیر'} | "
            f"برابری: {p['equality_status']} | "
            f"اصلاح ۲: {p['ratio_w2_ret'] * 100:.1f}% | اصلاح ۴: {p['ratio_w4_ret'] * 100:.1f}% | "
            f"ساختار: {p['internal_structure']}"
        )
        if p["violations"]:
            for v in p["violations"][:3]:
                logger.add_result(f"  نقض", v)
    
    logger.add_section("قوانین کلیدی", level=2)
    logger.add_result("قانون امتداد", results["قانون_امتداد_حیاتی"])
    logger.add_result("قانون برابری", results["قانون_برابری_تعریف"])
    logger.add_result("شرط روند دار", results["شرط_روند_دار"])
    logger.add_result("شرط ترمینال", results["شرط_ترمینال"])
    logger.add_result("مکان قطری پیشرو", results["مکان_قطری_پیشرو"])
    
    logger.add_result("تفسیر نهایی", results["تفسیر_نهایی"])


# ════════════════════════════════════════════════════════════════
# اجرای مستقیم برای تست
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # ایجاد داده تست با الگوی شتابدار روند دار با موج ۳ ممتد
    test_prices = [
        100, 105, 102, 108, 104,  # موج ۱
        100, 103, 98,               # موج ۲ (عمیق >۶۱.۸٪)
        115, 120, 118, 125, 130, 128, 135, 140, 138, 145,  # موج ۳ (ممتد)
        140, 142, 138, 141, 139,    # موج ۴ (کم عمق <۳۸.۲٪)
        148, 150, 147, 152,         # موج ۵
    ]
    
    test_high = [p + 2 for p in test_prices]
    test_low = [p - 2 for p in test_prices]
    
    test_data = pd.DataFrame({
        "close": test_prices,
        "high": test_high,
        "low": test_low,
        "open": test_prices,
        "volume": [1000] * len(test_prices),
    })
    
    result = analyze(test_data)
    print(result["تفسیر_نهایی"])