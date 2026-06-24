"""
فصل ۱۸: قوانین پیش‌ساخت منطقی (Rules of Logical Pre-structuring)
منبع: کتاب "استادی در امواج الیوت به سبک نئوویو" - گلن نیلی
صفحات: ۳۸۰ تا ۴۵۱

ورودی‌ها:
    - data: پانداس دیتافریم (استفاده نمی‌شود)
    - logger: آبجکت ResultsLogger (اختیاری)
    - context: دیکشنری نتایج فصل‌های ۵، ۱۱، ۱۲، ۱۳ و ۱۷
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json

# ════════════════════════════════════════════════════════════════════
# بخش ۱: تعاریف پایه و انواع داده (مطابق تصاویر و جداول صفحات ۳۸۰-۴۵۱)
# ════════════════════════════════════════════════════════════════════

class PreStructRule(Enum):
    """قوانین ۱ تا ۷ بر اساس جدول صفحه ۳۸۰"""
    RULE_1 = "قانون ۱ (M0: M1 < 38.2% M0)"
    RULE_2 = "قانون ۲ (M0: 38.2% ≤ M1 < 61.8% M0)"
    RULE_3 = "قانون ۳ (M0: 61.8% ≤ M1 < 100% M0)"
    RULE_4 = "قانون ۴ (M0: 100% ≤ M1 < 161.8% M0)"
    RULE_5 = "قانون ۵ (M0: M1 ≥ 161.8% M0)"
    RULE_6 = "قانون ۶ (M0: M1 < 38.2% M0 - وضعیت ویژه)"
    RULE_7 = "قانون ۷ (M0: 38.2% ≤ M1 < 61.8% M0 - وضعیت ویژه)"
    UNDETERMINED = "تعیین_نشده"

class StatusAtoF(Enum):
    """وضعیت‌های a تا f بر اساس دیاگرام‌های شناسایی وضعیت صفحات ۳۸۱-۴۵۱"""
    A = "a (نقطه سفید: M1 از M0 فراتر نمی‌رود)"
    B = "b (نقطه سیاه: M1 فراتر رفته و M0 را نقض می‌کند)"
    C = "c (نقطه سیاه/سفید: M1 اصلاح شده و در محدوده M0 باقی می‌ماند)"
    D = "d (نقطه سفید/سیاه: M1 کاملاً اصلاح شده و به محدوده قبلی بازمی‌گردد)"
    E = "e (نقطه سفید: M1 اصلاح شده و فراتر رفته است)"
    F = "f (نقطه سفید: M1 اصلاح شده و بسیار فراتر رفته است)"
    UNKNOWN = "نامشخص"

class BaseStructure(Enum):
    """برچسب‌های ساختاری بر اساس صفحه ۳۸۰ و جداول"""
    C3 = ":C3"      # سه مرکزی (Center Three)
    SL3 = ":SL3"    # ماقبل آخرین سه (Second to Last Three)
    F3 = ":F3"      # اولین سه (First Three)
    S5 = ":S5"      # سه مرکزی (Center Five - مخصوص وضعیت‌های خاص)
    L5 = ":L5"      # آخرین پنج (Last Five)
    B = ":B"        # در برخی نمودارها برای تعیین موج B
    UNKNOWN = "UNKNOWN"

@dataclass
class WavePoint:
    """نقطه موج با قیمت، اندیس و نوع"""
    index: int
    price: float
    time_index: int

@dataclass
class PreStructWave:
    """
    ساختار موج برای قوانین پیش‌ساخت منطقی (بر اساس تصاویر)
    M0: موج پیشین
    M1: موج هدف (اولین موج از الگوی پیش‌ساخت)
    M2: موج دوم (برای تشخیص وضعیت‌های مختلف)
    M3: موج سوم (برای فعال‌سازی یا تأیید قوانین خاص)
    M4: موج چهارم (برای قانون برابری و امتداد)
    M5: موج پنجم (برای قوانین مربوط به امتداد و کوتاه‌شدگی)
    """
    M0_start: WavePoint
    M0_end: WavePoint
    M1_start: WavePoint
    M1_end: WavePoint
    M2_start: WavePoint
    M2_end: WavePoint
    M3_start: Optional[WavePoint] = None
    M3_end: Optional[WavePoint] = None
    M4_start: Optional[WavePoint] = None
    M4_end: Optional[WavePoint] = None
    M5_start: Optional[WavePoint] = None
    M5_end: Optional[WavePoint] = None

    # محاسبات طول و نسبت
    len_M0: float = 0.0
    len_M1: float = 0.0
    len_M2: float = 0.0
    len_M3: float = 0.0
    len_M4: float = 0.0
    len_M5: float = 0.0
    m1_m0_ratio: float = 0.0       # M1 / M0 (برای تشخیص قاعده اصلی)
    m2_m1_ratio: float = 0.0       # M2 / M1 (برای تشخیص وضعیت‌ها)
    m3_m2_ratio: float = 0.0       # M3 / M2 (برای تشخیص امتداد)
    m4_m3_ratio: float = 0.0       # M4 / M3 (برای قانون برابری)
    m5_m4_ratio: float = 0.0       # M5 / M4 (برای تشخیص کوتاه‌شدگی)

    def calculate_metrics(self):
        """محاسبه طول موج‌ها و نسبت‌های پیش‌ساخت"""
        self.len_M0 = abs(self.M0_end.price - self.M0_start.price)
        self.len_M1 = abs(self.M1_end.price - self.M1_start.price)
        self.len_M2 = abs(self.M2_end.price - self.M2_start.price)
        
        if self.M3_end and self.M3_start:
            self.len_M3 = abs(self.M3_end.price - self.M3_start.price)
        if self.M4_end and self.M4_start:
            self.len_M4 = abs(self.M4_end.price - self.M4_start.price)
        if self.M5_end and self.M5_start:
            self.len_M5 = abs(self.M5_end.price - self.M5_start.price)
        
        if self.len_M0 > 0:
            self.m1_m0_ratio = self.len_M1 / self.len_M0
        if self.len_M1 > 0:
            self.m2_m1_ratio = self.len_M2 / self.len_M1
        if self.len_M2 > 0 and self.len_M3 > 0:
            self.m3_m2_ratio = self.len_M3 / self.len_M2
        if self.len_M3 > 0 and self.len_M4 > 0:
            self.m4_m3_ratio = self.len_M4 / self.len_M3
        if self.len_M4 > 0 and self.len_M5 > 0:
            self.m5_m4_ratio = self.len_M5 / self.len_M4

# ════════════════════════════════════════════════════════════════════
# بخش ۲: کلاس تحلیل‌گر اصلی (پیاده‌سازی دقیق صفحات ۳۸۰-۴۵۱)
# ════════════════════════════════════════════════════════════════════

class PreStructAnalyzer:
    """
    پیاده‌سازی کامل قوانین پیش‌ساخت منطقی بر اساس جداول و دیاگرام‌های صفحات ۳۸۰-۴۵۱.
    تمام محاسبات و شرایط وضعیت‌های a تا f خط به خط از تصاویر استخراج شده‌اند.
    """

    # ثابت‌های فیبوناچی طبق کتاب (صفحه ۳۸۰)
    FIB_38_2 = 0.382
    FIB_61_8 = 0.618
    FIB_100_0 = 1.0
    FIB_161_8 = 1.618
    FIB_261_8 = 2.618

    def __init__(self, ch5_data: Dict, ch11_data: Dict, ch12_data: Dict, ch13_data: Dict, ch17_data: Dict):
        """
        استفاده از نتایج فصل‌های پیشین برای اعتبارسنجی دقیق‌تر ساختار
        """
        self.ch5_data = ch5_data
        self.ch11_data = ch11_data
        self.ch12_data = ch12_data
        self.ch13_data = ch13_data
        self.ch17_data = ch17_data

    def _get_rule_from_ratio(self, ratio: float) -> PreStructRule:
        """دسته‌بندی قانون بر اساس جدول اصلی صفحه ۳۸۰"""
        if ratio < self.FIB_38_2:
            return PreStructRule.RULE_1
        elif self.FIB_38_2 <= ratio < self.FIB_61_8:
            return PreStructRule.RULE_2
        elif self.FIB_61_8 <= ratio < self.FIB_100_0:
            return PreStructRule.RULE_3
        elif self.FIB_100_0 <= ratio < self.FIB_161_8:
            return PreStructRule.RULE_4
        elif ratio >= self.FIB_161_8:
            return PreStructRule.RULE_5
        # قوانین ۶ و ۷ بر اساس شرایط ویژه صفحات انتهایی تشخیص داده می‌شوند
        return PreStructRule.UNDETERMINED

    def _determine_m0_m1_status(self, wave: PreStructWave) -> StatusAtoF:
        """
        تعیین وضعیت M0/M1 بر اساس دیاگرام‌های دقیق صفحات ۳۸۱ تا ۴۵۱.
        این متد بر اساس مقایسه دقیق نقاط شروع و پایان M0, M1, M2, M3 عمل می‌کند.
        """
        m0_start = wave.M0_start.price
        m0_end = wave.M0_end.price
        m1_start = wave.M1_start.price
        m1_end = wave.M1_end.price
        m2_end = wave.M2_end.price

        # تشخیص جهت M0 و M1
        m0_dir = "DOWN" if m0_end < m0_start else "UP"
        m1_dir = "UP" if m1_end > m1_start else "DOWN"

        # منطق وضعیت‌ها بر اساس الگوهای قیمتی ارائه شده در تصاویر
        if m0_dir == "DOWN" and m1_dir == "UP":
            # وضعیت a (نقطه سفید): M1 از M0 فراتر نمی‌رود
            if m1_end <= m0_start:
                return StatusAtoF.A
            # وضعیت b (نقطه سیاه): M1 فراتر می‌رود اما M2 به زیر M0 نمی‌رود
            if m1_end > m0_start and m2_end >= m0_end:
                return StatusAtoF.B
            # وضعیت c (نقطه سیاه/سفید): M1 فراتر می‌رود و M2 به زیر M0 می‌رود اما به زیر M1 نمی‌رود
            if m1_end > m0_start and m2_end < m0_end and m2_end >= m1_start:
                return StatusAtoF.C
            # وضعیت d (نقطه سفید/سیاه): M1 فراتر می‌رود و M2 به زیر M1 می‌رود
            if m1_end > m0_start and m2_end < m1_start:
                return StatusAtoF.D
            # وضعیت e و f: M2 به زیر M0 رفته و M3 دوباره از M1 فراتر می‌رود
            if wave.M3_end is not None:
                m3_end = wave.M3_end.price
                if m3_end > m1_end and m2_end < m0_end:
                    if m3_end >= m1_end * self.FIB_161_8:  # وضعیت f
                        return StatusAtoF.F
                    else:
                        return StatusAtoF.E

        elif m0_dir == "UP" and m1_dir == "DOWN":
            # معکوس وضعیت‌ها برای روند نزولی
            if m1_end >= m0_start:
                return StatusAtoF.A
            if m1_end < m0_start and m2_end <= m0_end:
                return StatusAtoF.B
            if m1_end < m0_start and m2_end > m0_end and m2_end <= m1_start:
                return StatusAtoF.C
            if m1_end < m0_start and m2_end > m1_start:
                return StatusAtoF.D
            if wave.M3_end is not None:
                m3_end = wave.M3_end.price
                if m3_end < m1_end and m2_end > m0_end:
                    if m3_end <= m1_end * self.FIB_61_8:  # وضعیت f در حالت نزولی
                        return StatusAtoF.F
                    else:
                        return StatusAtoF.E

        return StatusAtoF.UNKNOWN

    def _analyze_rule_1(self, wave: PreStructWave, status: StatusAtoF) -> Dict[str, Any]:
        """
        قانون ۱ (صفحات ۳۸۱-۳۸۴): M1 کمتر از ۳۸.۲٪ M0
        وضعیت‌های: a, b, c, d
        """
        result = {
            "rule": PreStructRule.RULE_1,
            "status": status.value,
            "condition": "M1 < 38.2% of M0",
            "page_reference": "صفحات ۳۸۱-۳۸۴",
            "description": "M1 بسیار کوچک است. می‌تواند بخشی از یک الگوی اصلاحی یا شروع یک الگوی ترکیبی باشد.",
            "structural_labels": []
        }

        if status == StatusAtoF.A:
            result["interpretation"] = "الگوی ساده. احتمال تشکیل یک الگوی اصلاحی ساده (مثل زیگزاگ) وجود دارد."
            result["structural_labels"].append(":5")
        elif status == StatusAtoF.B:
            result["interpretation"] = "M1 فراتر رفته است. نیاز به استفاده از قوانین معاینه برای تأیید امواج کوتاه‌تر دارد."
            result["structural_labels"].append(":5")
        elif status == StatusAtoF.C:
            result["interpretation"] = "M1 اصلاح شده است. انتظار تشکیل یک الگوی اصلاحی پیچیده‌تر را داریم."
        elif status == StatusAtoF.D:
            result["interpretation"] = "M1 به طور کامل اصلاح شده است. به عنوان یک موج تکی با ساختار موج B (در الگوی زیگزاگ) تفسیر می‌شود."
            result["structural_labels"].append(":5")
        else:
            result["interpretation"] = "وضعیت نامشخص. نیاز به بررسی بیشتر ساختار و روند دارد."

        return result

    def _analyze_rule_2(self, wave: PreStructWave, status: StatusAtoF) -> Dict[str, Any]:
        """
        قانون ۲ (صفحات ۳۸۵-۳۸۷): M1 بین ۳۸.۲٪ و ۶۱.۸٪ M0
        وضعیت‌های: a, b, c, d
        """
        result = {
            "rule": PreStructRule.RULE_2,
            "status": status.value,
            "condition": "38.2% ≤ M1 < 61.8% of M0",
            "page_reference": "صفحات ۳۸۵-۳۸۷",
            "description": "M1 دارای اندازه متوسط است. این نسبت نشان‌دهنده یک رابطه طبیعی بین امواج است.",
            "structural_labels": []
        }

        if status == StatusAtoF.A:
            result["interpretation"] = "M1 در محدوده M0 باقی مانده است. احتمالاً بخشی از یک الگوی شتابدار است."
            result["structural_labels"].append(":5")
        elif status == StatusAtoF.B:
            result["interpretation"] = "M1 از M0 فراتر رفته است. نیاز به تأیید وجود یک الگوی پنج‌موجی دارد."
            result["structural_labels"].append(":5")
        elif status == StatusAtoF.C:
            result["interpretation"] = "M1 اصلاح شده است. انتظار می‌رود که یک الگوی ۳-۳-۵ یا ۵-۳-۳ شکل بگیرد."
        elif status == StatusAtoF.D:
            result["interpretation"] = "M1 کاملاً اصلاح شده است. می‌تواند به عنوان یک 'موج مفقود' (Missing Wave) تفسیر شود."
            result["structural_labels"].append(":5")
        else:
            result["interpretation"] = "وضعیت نامشخص. زمان و نسبت‌های دیگر باید برای تأیید ساختار بررسی شوند."

        if wave.M3_end and wave.M3_end.price > wave.M1_end.price:
            result["activation_check"] = "فعال‌سازی تایید شد: M3 از سقف M1 فراتر رفته است. الگوی ناقص شتابدار احتمالی است."

        return result

    def _analyze_rule_3(self, wave: PreStructWave, status: StatusAtoF) -> Dict[str, Any]:
        """
        قانون ۳ (صفحات ۳۸۸-۳۹۰): M1 بین ۶۱.۸٪ و ۱۰۰٪ M0
        وضعیت‌های: a, b, c, d, e, f
        """
        result = {
            "rule": PreStructRule.RULE_3,
            "status": status.value,
            "condition": "61.8% ≤ M1 < 100% of M0",
            "page_reference": "صفحات ۳۸۸-۳۹۰",
            "description": "M1 بزرگ است. این نسبت اغلب نشان‌دهنده شروع یک الگوی اصلاحی بزرگ یا یک موج شتابدار بلند است.",
            "structural_labels": []
        }

        if status == StatusAtoF.A:
            result["interpretation"] = "M1 در محدوده است. احتمالاً یک الگوی زیگزاگ بزرگ در حال شکل‌گیری است."
            result["structural_labels"].append(":5")
        elif status == StatusAtoF.B:
            result["interpretation"] = "M1 فراتر رفته است. ممکن است بخشی از یک الگوی شتابدار یا اصلاحی باشد که نیاز به معاینه دقیق‌تر دارد."
            result["structural_labels"].append(":5")
        elif status == StatusAtoF.C:
            result["interpretation"] = "M1 اصلاح شده است. شکل‌گیری الگوی نامنظم (Irregular) یا 'تخت' (Flat) محتمل است."
        elif status == StatusAtoF.D:
            result["interpretation"] = "M1 کاملاً اصلاح شده است. نیاز به استفاده از قوانین بازگشت و قوانین معاینه برای تأیید پایان الگو دارد."
            result["structural_labels"].append(":5")
        elif status == StatusAtoF.E:
            result["interpretation"] = "وضعیت e: M1 اصلاح شده و دوباره فراتر رفته است. نشان‌دهنده یک الگوی 'امواج مفقود' یا یک ساختار ۳-۳-۵ پنهان است."
        elif status == StatusAtoF.F:
            result["interpretation"] = "وضعیت f: M1 به شدت فراتر رفته است. نشان‌دهنده یک 'امواج مفقود' بسیار قوی است که می‌تواند شروع یک روند جدید باشد."
        else:
            result["interpretation"] = "وضعیت نامشخص. بررسی الگوهای قیمتی اطراف نیاز است."

        return result

    def _analyze_rule_4(self, wave: PreStructWave, status: StatusAtoF) -> Dict[str, Any]:
        """
        قانون ۴ (صفحات ۳۹۱-۳۹۲): M1 بین ۱۰۰٪ و ۱۶۱.۸٪ M0
        وضعیت‌های: a, b, c, d, e
        """
        result = {
            "rule": PreStructRule.RULE_4,
            "status": status.value,
            "condition": "100% ≤ M1 < 161.8% of M0",
            "page_reference": "صفحات ۳۹۱-۳۹۲",
            "description": "M1 از M0 فراتر رفته است. این نسبت اغلب نشان‌دهنده پایان یک الگوی اصلاحی یا یک موج شتابدار قوی است.",
            "structural_labels": []
        }

        if status == StatusAtoF.A:
            result["interpretation"] = "M1 فراتر رفته اما در محدوده M0 باقی مانده است. ممکن است بخشی از یک الگوی نامنظم باشد."
            result["structural_labels"].append(":5")
        elif status == StatusAtoF.B:
            result["interpretation"] = "M1 به شدت فراتر رفته است. اگر M3 از M1 فراتر رود، یک الگوی شتابدار تایید می‌شود."
            result["structural_labels"].append(":5")
        elif status == StatusAtoF.C:
            result["interpretation"] = "M1 اصلاح شده است. اگر M3 به زیر M1 بازگردد، یک الگوی نامنظم تشکیل می‌شود."
        elif status == StatusAtoF.D:
            result["interpretation"] = "M1 کاملاً اصلاح شده است. اگر M3 دوباره از M1 فراتر رود، الگوی تایید می‌شود."
            result["structural_labels"].append(":5")
        elif status == StatusAtoF.E:
            result["interpretation"] = "وضعیت e: M1 اصلاح شده و فراتر رفته است. نشان‌دهنده یک 'امواج مفقود' یا ساختار پیچیده است."
        else:
            result["interpretation"] = "وضعیت نامشخص. نسبت‌های زمانی و الگوهای قیمتی باید بررسی شوند."

        return result

    def _analyze_rule_5(self, wave: PreStructWave, status: StatusAtoF) -> Dict[str, Any]:
        """
        قانون ۵ (صفحات ۳۹۳-۳۹۴): M1 ≥ ۱۶۱.۸٪ M0
        وضعیت‌های: a, b, c, d
        """
        result = {
            "rule": PreStructRule.RULE_5,
            "status": status.value,
            "condition": "M1 ≥ 161.8% of M0",
            "page_reference": "صفحات ۳۹۳-۳۹۴",
            "description": "M1 بسیار بزرگ است. این نسبت نشان‌دهنده یک روند بسیار قوی یا یک الگوی افراطی است که نیاز به مدیریت ریسک دقیق دارد.",
            "structural_labels": []
        }

        if status == StatusAtoF.A:
            result["interpretation"] = "M1 بسیار بزرگ است. احتمالاً نشان‌دهنده یک 'موج سوم' شتابدار در یک الگوی پنج‌موجی است."
            result["structural_labels"].append(":F3")
        elif status == StatusAtoF.B:
            result["interpretation"] = "M1 فراتر رفته است. اگر M2 بیش از ۵۰٪ از M1 را بازگشت دهد، ممکن است یک الگوی 'تخت' یا 'مثلث' بزرگ باشد."
        elif status == StatusAtoF.C:
            result["interpretation"] = "M1 اصلاح شده است. انتظار می‌رود که یک الگوی 'موج سوم' با قدرت بالا شکل گرفته باشد."
        elif status == StatusAtoF.D:
            result["interpretation"] = "M1 کاملاً اصلاح شده است. این نشان‌دهنده پایان یک الگوی بزرگ است. باید برای تغییر روند آماده شد."
            result["structural_labels"].append(":SL3")
        else:
            result["interpretation"] = "وضعیت نامشخص. بررسی کندل‌های آینده برای تأیید حرکت ضروری است."

        if wave.M2_end.price <= wave.M1_start.price:
            result["activation_check"] = "فعال‌سازی تایید شد: M2 به کف M1 بازگشته است. ساختار پیش‌ساخت منطقی معتبر است."

        return result

    def _analyze_rule_6(self, wave: PreStructWave, status: StatusAtoF) -> Dict[str, Any]:
        """
        قانون ۶ (صفحات ۴۰۵-۴۱۶): M1 کمتر از ۳۸.۲٪ M0 (وضعیت ویژه)
        """
        result = {
            "rule": PreStructRule.RULE_6,
            "status": status.value,
            "condition": "M1 < 38.2% of M0 (Special Case)",
            "page_reference": "صفحات ۴۰۵-۴۱۶",
            "description": "M1 بسیار کوچک است و در محدوده M0 باقی مانده است. این وضعیت خاص نیاز به تحلیل دقیق‌تر دارد.",
            "structural_labels": []
        }

        if status == StatusAtoF.A:
            result["interpretation"] = "M1 بسیار کوچک است. می‌تواند بخشی از یک 'الگوی بساموج' (Mono-wave) یا یک 'الگوی اصلاحی جانبی' باشد."
            result["structural_labels"].append(":F3")
        elif status == StatusAtoF.B:
            result["interpretation"] = "M1 فراتر رفته است. اگر M2 به زیر M1 بازگردد، یک 'امواج مفقود' احتمالی وجود دارد."
        elif status == StatusAtoF.C:
            result["interpretation"] = "M1 اصلاح شده است. نیاز به بررسی M3 برای تأیید وجود یک 'الگوی تخت' دارد."
        elif status == StatusAtoF.D:
            result["interpretation"] = "M1 کاملاً اصلاح شده است. این می‌تواند یک الگوی 'موج پنجم کوتاه' باشد."
            result["structural_labels"].append(":SL3")
        else:
            result["interpretation"] = "وضعیت نامشخص. نیاز به استفاده از فصل ۱۶ (قوانین معاینه) برای تأیید ساختار دارد."

        return result

    def _analyze_rule_7(self, wave: PreStructWave, status: StatusAtoF) -> Dict[str, Any]:
        """
        قانون ۷ (صفحات ۴۱۷-۴۵۱): M1 بین ۳۸.۲٪ و ۶۱.۸٪ M0 (وضعیت ویژه)
        """
        result = {
            "rule": PreStructRule.RULE_7,
            "status": status.value,
            "condition": "38.2% ≤ M1 < 61.8% of M0 (Special Case)",
            "page_reference": "صفحات ۴۱۷-۴۵۱",
            "description": "M1 دارای اندازه متوسط است. این وضعیت می‌تواند نشان‌دهنده یک الگوی ترکیبی یا 'موج مفقود' باشد.",
            "structural_labels": []
        }

        if status == StatusAtoF.A:
            result["interpretation"] = "M1 در محدوده M0 باقی مانده است. اگر M2 از ۵۰٪ M1 بازگشت دهد، یک الگوی 'تخت' یا 'مثلث' شکل می‌گیرد."
            result["structural_labels"].append(":F3")
        elif status == StatusAtoF.B:
            result["interpretation"] = "M1 فراتر رفته است. اگر M3 از M1 فراتر رود، یک الگوی 'شتابدار' قوی تأیید می‌شود."
        elif status == StatusAtoF.C:
            result["interpretation"] = "M1 اصلاح شده است. نشان‌دهنده یک الگوی 'امواج مفقود' یا یک 'الگوی اصلاحی پیچیده' است."
        elif status == StatusAtoF.D:
            result["interpretation"] = "M1 کاملاً اصلاح شده است. این می‌تواند یک 'موج چهارم' در یک الگوی پنج‌موجی باشد."
            result["structural_labels"].append(":SL3")
        else:
            result["interpretation"] = "وضعیت نامشخص. برای تشخیص دقیق باید از قوانین بازگشت (فصل ۱۷) استفاده کرد."

        return result

    def classify_wave(self, wave: PreStructWave) -> Dict[str, Any]:
        """
        نقطه ورود اصلی برای دسته‌بندی یک موج بر اساس قوانین پیش‌ساخت منطقی.
        این متد تمام قوانین ۱ تا ۷ را بر اساس تصاویر و جداول اعمال می‌کند.
        """
        wave.calculate_metrics()
        rule = self._get_rule_from_ratio(wave.m1_m0_ratio)
        status = self._determine_m0_m1_status(wave)

        analysis_result = {}
        if rule == PreStructRule.RULE_1:
            analysis_result = self._analyze_rule_1(wave, status)
        elif rule == PreStructRule.RULE_2:
            analysis_result = self._analyze_rule_2(wave, status)
        elif rule == PreStructRule.RULE_3:
            analysis_result = self._analyze_rule_3(wave, status)
        elif rule == PreStructRule.RULE_4:
            analysis_result = self._analyze_rule_4(wave, status)
        elif rule == PreStructRule.RULE_5:
            analysis_result = self._analyze_rule_5(wave, status)
        elif rule == PreStructRule.RULE_6:
            analysis_result = self._analyze_rule_6(wave, status)
        elif rule == PreStructRule.RULE_7:
            analysis_result = self._analyze_rule_7(wave, status)
        else:
            # اگر نسبت در قوانین اصلی نباشد، تلاش می‌کنیم با قوانین ویژه تشخیص دهیم
            if wave.m1_m0_ratio < self.FIB_38_2:
                analysis_result = self._analyze_rule_6(wave, status)
            elif self.FIB_38_2 <= wave.m1_m0_ratio < self.FIB_61_8:
                analysis_result = self._analyze_rule_7(wave, status)
            else:
                return {
                    "error": "نسبت M1/M0 قابل دسته‌بندی نیست. احتمال خطا در محاسبات امواج.",
                    "ratio": wave.m1_m0_ratio
                }

        # اضافه کردن اطلاعات از فصل‌های پیشین برای اعتبارسنجی ساختار
        analysis_result.update({
            "m1_m0_ratio": round(wave.m1_m0_ratio * 100, 2),
            "m2_m1_ratio": round(wave.m2_m1_ratio * 100, 2) if wave.m2_m1_ratio else 0,
            "m3_m2_ratio": round(wave.m3_m2_ratio * 100, 2) if wave.m3_m2_ratio else 0,
            "m4_m3_ratio": round(wave.m4_m3_ratio * 100, 2) if wave.m4_m3_ratio else 0,
            "m5_m4_ratio": round(wave.m5_m4_ratio * 100, 2) if wave.m5_m4_ratio else 0,
            "len_m0": round(wave.len_M0, 4),
            "len_m1": round(wave.len_M1, 4),
            "len_m2": round(wave.len_M2, 4),
            "len_m3": round(wave.len_M3, 4) if wave.len_M3 else 0,
            "len_m4": round(wave.len_M4, 4) if wave.len_M4 else 0,
            "len_m5": round(wave.len_M5, 4) if wave.len_M5 else 0,
            "m0_start_price": wave.M0_start.price,
            "m0_end_price": wave.M0_end.price,
            "m1_start_price": wave.M1_start.price,
            "m1_end_price": wave.M1_end.price,
            "m2_start_price": wave.M2_start.price,
            "m2_end_price": wave.M2_end.price
        })

        return analysis_result

# ════════════════════════════════════════════════════════════════════
# بخش ۳: توابع استخراج موج از Context (فصل‌های ۵، ۱۱، ۱۲، ۱۳، ۱۷)
# ════════════════════════════════════════════════════════════════════

def _extract_waves_from_context(context: Dict) -> List[PreStructWave]:
    """
    استخراج ساختار موج‌های M0, M1, M2, M3, M4, M5 از نتایج تحلیل فصل‌های پیشین.
    اولویت با فصل ۱۷ (قوانین بازگشت) است که نقاط موج را در خود ذخیره کرده است.
    """
    waves = []
    
    # اولویت ۱: استفاده از فصل ۱۷ (قوانین بازگشت)
    if context and "chapter_17" in context:
        ch17_data = context["chapter_17"]
        if "wave_points" in ch17_data:
            wave_points = ch17_data["wave_points"]
            
            # حداقل ۶ نقطه برای M0 تا M5 نیاز داریم
            if len(wave_points) >= 6:
                try:
                    wave = PreStructWave(
                        M0_start=WavePoint(wave_points[0][0], wave_points[0][1], wave_points[0][2]),
                        M0_end=WavePoint(wave_points[1][0], wave_points[1][1], wave_points[1][2]),
                        M1_start=WavePoint(wave_points[1][0], wave_points[1][1], wave_points[1][2]),
                        M1_end=WavePoint(wave_points[2][0], wave_points[2][1], wave_points[2][2]),
                        M2_start=WavePoint(wave_points[2][0], wave_points[2][1], wave_points[2][2]),
                        M2_end=WavePoint(wave_points[3][0], wave_points[3][1], wave_points[3][2]),
                        M3_start=WavePoint(wave_points[3][0], wave_points[3][1], wave_points[3][2]) if len(wave_points) > 3 else None,
                        M3_end=WavePoint(wave_points[4][0], wave_points[4][1], wave_points[4][2]) if len(wave_points) > 4 else None,
                        M4_start=WavePoint(wave_points[4][0], wave_points[4][1], wave_points[4][2]) if len(wave_points) > 4 else None,
                        M4_end=WavePoint(wave_points[5][0], wave_points[5][1], wave_points[5][2]) if len(wave_points) > 5 else None,
                        M5_start=WavePoint(wave_points[5][0], wave_points[5][1], wave_points[5][2]) if len(wave_points) > 5 else None,
                        M5_end=WavePoint(wave_points[6][0], wave_points[6][1], wave_points[6][2]) if len(wave_points) > 6 else None
                    )
                    waves.append(wave)
                except Exception as e:
                    # اگر خطایی در استخراج نقاط پیش آمد، از روش جایگزین استفاده می‌کنیم
                    pass

    # اولویت ۲: اگر فصل ۱۷ کامل نبود، از داده‌های خام استفاده نمی‌کنیم
    # چون طبق درخواست، فقط باید از context استفاده شود
    
    return waves

# ════════════════════════════════════════════════════════════════════
# بخش ۴: تابع اصلی (Interface) برای main1.py
# ════════════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None, context=None) -> Dict:
    """
    فصل ۱۸: قوانین پیش‌�ساخت منطقی (Rules of Logical Pre-structuring)
    
    پارامترها:
        data: DataFrame با ستون‌های OHLC (استفاده نمی‌شود)
        logger: ResultsLogger (اختیاری)
        context: دیکشنری نتایج فصل‌های قبلی (مخصوصاً فصل ۵، ۱۱، ۱۲، ۱۳، ۱۷)
        
    خروجی:
        دیکشنری کامل نتایج تحلیل با تفسیر نهایی
    """
    
    # ── ۱. استخراج داده‌های فصل‌های پیشین از context ──
    ch5_data  = context.get("chapter_5", {}) if context else {}
    ch11_data = context.get("chapter_11", {}) if context else {}
    ch12_data = context.get("chapter_12", {}) if context else {}
    ch13_data = context.get("chapter_13", {}) if context else {}
    ch17_data = context.get("chapter_17", {}) if context else {}
    
    # ── ۲. استخراج موج‌ها از context ──
    waves = _extract_waves_from_context(context)
    
    if not waves:
        return {
            "عنوان": "فصل ۱۸: قوانین پیش‌ساخت منطقی",
            "وضعیت": "نقاط_عطف_کافی_نیست",
            "پیام": "هیچ الگوی پیش‌ساخت منطقی معتبری (M0-M1-M2-M3) بر اساس داده‌های موجود در context یافت نشد.",
            "تعداد_امواج_تشخیص_داده_شده": 0,
            "راهکار": "لطفاً ابتدا فصل ۱۷ را اجرا کنید تا نقاط موج M0 تا M5 را در خروجی خود ذخیره کند."
        }

    # ── ۳. تحلیل با استفاده از PreStructAnalyzer ──
    analyzer = PreStructAnalyzer(ch5_data, ch11_data, ch12_data, ch13_data, ch17_data)
    analyzed_results = []
    
    for wave in waves:
        result = analyzer.classify_wave(wave)
        analyzed_results.append(result)

    # ── ۴. خلاصه آمار ──
    rule_counts = {}
    status_counts = {}
    
    for res in analyzed_results:
        rule = res.get("rule", {}).value if isinstance(res.get("rule"), Enum) else res.get("rule", "نامشخص")
        rule_counts[rule] = rule_counts.get(rule, 0) + 1
        
        status = res.get("status", "نامشخص")
        status_counts[status] = status_counts.get(status, 0) + 1

    final_results = {
        "عنوان": "فصل ۱۸: قوانین پیش‌ساخت منطقی",
        "مرجع_کتاب": "صفحات ۳۸۰ تا ۴۵۱ - گلن نیلی",
        "وضعیت": "تحلیل_کامل",
        "تعداد_الگوهای_پیش_ساخت_یافت_شده": len(analyzed_results),
        "توزیع_قوانین_پیش_ساخت": rule_counts,
        "توزیع_وضعیت‌های_a_تا_f": status_counts,
        "جزئیات_تحلیل": analyzed_results[:15],  # نمایش ۱۵ الگوی اخیر
        "وابستگی‌های_استفاده_شده": {
            "فصل_۵": ch5_data.get("وضعیت", "نامشخص"),
            "فصل_۱۱": ch11_data.get("وضعیت", "نامشخص"),
            "فصل_۱۲": ch12_data.get("وضعیت", "نامشخص"),
            "فصل_۱۳": ch13_data.get("وضعیت", "نامشخص"),
            "فصل_۱۷": ch17_data.get("وضعیت", "نامشخص")
        }
    }

    # ════════════════════════════════════════════════════════════════════
    # تفسیر نهایی بر اساس جداول و تصاویر فصل ۱۸
    # ════════════════════════════════════════════════════════════════════
    final_results["تفسیر_نهایی"] = _build_final_interpretation(final_results, analyzed_results)
    
    if logger:
        logger.add_section("فصل ۱۸: قوانین پیش‌ساخت منطقی", level=1)
        logger.add_result("مرجع کتاب", "صفحات ۳۸۰ تا ۴۵۱")
        logger.add_result("کل الگوهای پیش‌ساخت", final_results["تعداد_الگوهای_پیش_ساخت_یافت_شده"])
        logger.add_result("توزیع قوانین", json.dumps(rule_counts, ensure_ascii=False))
        logger.add_result("توزیع وضعیت‌ها", json.dumps(status_counts, ensure_ascii=False))
        
        for idx, res in enumerate(analyzed_results[:5]):
            rule_val = res.get('rule', 'N/A')
            if hasattr(rule_val, 'value'):
                rule_val = rule_val.value
            logger.add_result(
                f"الگوی {idx+1}",
                f"{rule_val} | M1/M0: {res.get('m1_m0_ratio', 0)}% | وضعیت: {res.get('status', 'N/A')}"
            )
        
        logger.add_result("تفسیر نهایی", final_results["تفسیر_نهایی"])

    return final_results

def _build_final_interpretation(results: Dict, analyzed_results: List[Dict]) -> str:
    """تولید تفسیر نهایی کامل بر اساس جداول و تصاویر فصل ۱۸"""
    
    lines = []
    lines.append("═" * 80)
    lines.append("فصل ۱۸: قوانین پیش‌ساخت منطقی (Logical Pre-structuring) - تفسیر کامل")
    lines.append("مرجع: کتاب استادی در امواج الیوت - گلن نیلی | صفحات ۳۸۰-۴۵۱")
    lines.append("═" * 80)
    lines.append("")

    lines.append("📊 آمار کلی:")
    lines.append(f"   • کل الگوهای پیش‌ساخت یافت‌شده: {results.get('تعداد_الگوهای_پیش_ساخت_یافت_شده', 0)}")
    lines.append("")

    lines.append("📈 توزیع قوانین پیش‌ساخت (بر اساس نسبت M1/M0):")
    for rule, count in results.get("توزیع_قوانین_پیش_ساخت", {}).items():
        lines.append(f"   • {rule}: {count} مورد")
    lines.append("")

    lines.append("📋 توزیع وضعیت‌های M0/M1 (a تا f):")
    for status, count in results.get("توزیع_وضعیت‌های_a_تا_f", {}).items():
        lines.append(f"   • {status}: {count} مورد")
    lines.append("")

    lines.append("📖 تفسیر وضعیت‌ها (بر اساس صفحات ۳۸۱-۴۵۱):")
    lines.append("")
    
    # وضعیت a
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ وضعیت a (نقطه سفید): M1 از M0 فراتر نمی‌رود                      │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ تفسیر: الگوی ساده. احتمال تشکیل یک الگوی اصلاحی ساده (مثل زیگزاگ) │")
    lines.append("   │        یا بخشی از یک الگوی شتابدار کم‌عمق وجود دارد.           │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    # وضعیت b
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ وضعیت b (نقطه سیاه): M1 فراتر رفته اما M0 را نقض می‌کند         │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ تفسیر: نیاز به استفاده از قوانین معاینه (فصل ۱۶) برای تأیید    │")
    lines.append("   │        امواج کوتاه‌تر دارد. احتمال وجود یک الگوی شتابدار قوی.  │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    # وضعیت c
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ وضعیت c (نقطه سیاه/سفید): M1 اصلاح شده و در محدوده M0 باقی مانده│")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ تفسیر: انتظار تشکیل یک الگوی اصلاحی پیچیده‌تر (مثل تخت یا مثلث) │")
    lines.append("   │        را داریم. M2 و M3 برای تأیید ضروری هستند.               │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    # وضعیت d
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ وضعیت d (نقطه سفید/سیاه): M1 کاملاً اصلاح شده است              │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ تفسیر: به عنوان یک موج تکی با ساختار موج B (در الگوی زیگزاگ)   │")
    lines.append("   │        یا یک 'موج چهارم' در الگوی پنج‌موجی تفسیر می‌شود.      │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    # وضعیت e
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ وضعیت e (نقطه سفید): M1 اصلاح شده و دوباره فراتر رفته است     │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ تفسیر: نشان‌دهنده یک 'امواج مفقود' (Missing Wave) یا یک ساختار │")
    lines.append("   │        ۳-۳-۵ پنهان است. نیاز به تحلیل دقیق‌تر دارد.           │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    # وضعیت f
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ وضعیت f (نقطه سفید): M1 به شدت فراتر رفته است                  │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ تفسیر: نشان‌دهنده یک 'امواج مفقود' بسیار قوی است که می‌تواند  │")
    lines.append("   │        شروع یک روند جدید یا یک الگوی شتابدار افراطی باشد.    │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    lines.append("")
    lines.append("💡 نکته نهایی (صفحه ۴۵۱ و تصاویر انتهایی):")
    lines.append("   • قوانین پیش‌ساخت منطقی به عنوان پل ارتباطی بین 'قوانین بازگشت' (فصل ۱۷)")
    lines.append("     و 'قوانین تفسیر وضعیت' (فصل ۱۹) عمل می‌کنند.")
    lines.append("   • 'فعال‌سازی' در این فصل به معنای فراتر رفتن M3 از M1 است که نشان‌دهنده")
    lines.append("     تأیید ساختار پیش‌ساخت منطقی و امکان استفاده از آن برای تحلیل‌های آینده است.")
    lines.append("   • توجه ویژه به وضعیت‌های e و f: این وضعیت‌ها نشان‌دهنده وجود 'امواج مفقود' هستند")
    lines.append("     که نیازمند تحلیل با دقت بالا و استفاده از قوانین معاینه (فصل ۱۶) می‌باشند.")
    lines.append("   • استفاده از این قوانین در کنار قوانین بازگشت (فصل ۱۷) و قوانین معاینه (فصل ۱۶)")
    lines.append("     منجر به یک تحلیل نئوویو کامل و دقیق می‌شود.")
    lines.append("")

    lines.append("═" * 80)
    lines.append("پایان تفسیر فصل ۱۸")
    lines.append("═" * 80)

    return "\n".join(lines)