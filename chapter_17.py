"""
فصل ۱۷: قوانین بازگشت (Rules of Retracement)
منبع: کتاب "استادی در امواج الیوت به سبک نئوویو" - گلن نیلی
صفحات: ۳۶۴ تا ۳۸۰

این فصل بر اساس جداول و دیاگرام‌های دقیق صفحات ۳۶۴ تا ۳۷۹، قوانین ۱ تا ۷ را پیاده‌سازی می‌کند.
دیاگرام‌های "شناسایی وضعیت" برای هر قانون به صورت کامل به کد تبدیل شده‌اند.
وابستگی‌ها: [2, 3, 11, 12, 15] (با استفاده از context)
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json

# ════════════════════════════════════════════════════════════════════
# بخش ۱: تعاریف پایه و انواع داده (مطابق تصاویر و جداول)
# ════════════════════════════════════════════════════════════════════

class RetracementRule(Enum):
    """قوانین ۱ تا ۷ بر اساس جدول صفحه ۳۶۴"""
    RULE_1 = "قانون ۱ (M2 < ۳۸.۲٪ M1)"
    RULE_2 = "قانون ۲ (۳۸.۲٪ ≤ M2 < ۶۱.۸٪ M1)"
    RULE_3 = "قانون ۳ (M2 = ۶۱.۸٪ M1)"
    RULE_4 = "قانون ۴ (۶۱.۸٪ < M2 < ۱۰۰٪ M1)"
    RULE_5 = "قانون ۵ (۱۰۰٪ ≤ M2 < ۱۶۱.۸٪ M1)"
    RULE_6 = "قانون ۶ (۱۶۱.۸٪ ≤ M2 < ۲۶۱.۸٪ M1)"
    RULE_7 = "قانون ۷ (M2 ≥ ۲۶۱.۸٪ M1)"
    UNDETERMINED = "تعیین_نشده"

class M0M1Status(Enum):
    """وضعیت‌های a تا f در دیاگرام‌های شناسایی وضعیت"""
    A = "a (نقطه سفید: M1 از M0 فراتر نمی‌رود)"
    B = "b (نقطه سیاه: M1 فراتر رفته و M0 را نقض می‌کند)"
    C = "c (نقطه سیاه/سفید: M1 اصلاح شده و در محدوده M0 باقی می‌ماند)"
    D = "d (نقطه سفید/سیاه: M1 کاملاً اصلاح شده و به محدوده قبلی بازمی‌گردد)"
    E = "e (نقطه سفید: M1 اصلاح شده و فراتر رفته است - مخصوص قانون ۲ و ۳)"
    F = "f (نقطه سفید: M1 اصلاح شده و بسیار فراتر رفته است - مخصوص قانون ۳)"
    UNKNOWN = "نامشخص"

@dataclass
class WavePoint:
    """نقطه موج با قیمت، اندیس و نوع"""
    index: int
    price: float
    type: str = "UNKNOWN"  # 'PEAK' or 'TROUGH'

@dataclass
class RetracementWave:
    """
    ساختار موج برای قوانین بازگشت (بر اساس تصاویر)
    M0: موج پیشین
    M1: موج مورد نظر
    M2: موج پسین (اصلاح کننده)
    M3: موج پسین بعدی (برای تأیید فعال‌سازی)
    """
    M0_start: WavePoint
    M0_end: WavePoint
    M1_start: WavePoint
    M1_end: WavePoint
    M2_start: WavePoint
    M2_end: WavePoint
    M3_start: Optional[WavePoint] = None
    M3_end: Optional[WavePoint] = None

    # محاسبات طول و نسبت
    len_M0: float = 0.0
    len_M1: float = 0.0
    len_M2: float = 0.0
    retracement_ratio: float = 0.0  # M2 / M1
    m0_m1_ratio: float = 0.0       # M1 / M0 (برای تشخیص وضعیت‌های a-f)

    def calculate_metrics(self):
        """محاسبه طول موج‌ها و نسبت‌های بازگشت"""
        self.len_M0 = abs(self.M0_end.price - self.M0_start.price)
        self.len_M1 = abs(self.M1_end.price - self.M1_start.price)
        self.len_M2 = abs(self.M2_end.price - self.M2_start.price)
        
        if self.len_M1 > 0:
            self.retracement_ratio = self.len_M2 / self.len_M1
        if self.len_M0 > 0:
            self.m0_m1_ratio = self.len_M1 / self.len_M0

# ════════════════════════════════════════════════════════════════════
# بخش ۲: کلاس تحلیل‌گر اصلی (پیاده‌سازی جداول و تصاویر)
# ════════════════════════════════════════════════════════════════════

class RetracementAnalyzer:
    """
    پیاده‌سازی کامل قوانین بازگشت بر اساس جداول و دیاگرام‌های صفحات ۳۶۴-۳۷۹.
    تمام محاسبات با دقت بر اساس تصاویر و جداول ارائه شده انجام می‌شود.
    """

    # ثابت‌های فیبوناچی طبق کتاب
    FIB_38_2 = 0.382
    FIB_61_8 = 0.618
    FIB_100_0 = 1.0
    FIB_161_8 = 1.618
    FIB_261_8 = 2.618

    def __init__(self, chapter_16_data: Dict, chapter_11_data: Dict, chapter_12_data: Dict, chapter_14_data: Dict):
        """
        استفاده از نتایج فصل‌های پیشین برای اعتبارسنجی دقیق‌تر
        """
        self.chapter_16_data = chapter_16_data
        self.chapter_11_data = chapter_11_data
        self.chapter_12_data = chapter_12_data
        self.chapter_14_data = chapter_14_data

    def _get_rule_from_ratio(self, ratio: float) -> RetracementRule:
        """دسته‌بندی قانون بر اساس جدول صفحه ۳۶۴"""
        if ratio < self.FIB_38_2:
            return RetracementRule.RULE_1
        elif self.FIB_38_2 <= ratio < self.FIB_61_8:
            return RetracementRule.RULE_2
        elif abs(ratio - self.FIB_61_8) < 0.005:  # دقیقاً ۶۱.۸٪
            return RetracementRule.RULE_3
        elif self.FIB_61_8 < ratio < self.FIB_100_0:
            return RetracementRule.RULE_4
        elif self.FIB_100_0 <= ratio < self.FIB_161_8:
            return RetracementRule.RULE_5
        elif self.FIB_161_8 <= ratio < self.FIB_261_8:
            return RetracementRule.RULE_6
        elif ratio >= self.FIB_261_8:
            return RetracementRule.RULE_7
        return RetracementRule.UNDETERMINED

    def _determine_m0_m1_status(self, wave: RetracementWave) -> M0M1Status:
        """
        تعیین وضعیت M0/M1 بر اساس دیاگرام‌های دقیق صفحات ۳۶۷ تا ۳۷۹.
        این متد از مقایسه مستقیم نقاط شروع و پایان (m0_start, m0_end, m1_start, m1_end, m2_end) استفاده می‌کند.
        """
        # نقاط کلیدی
        m0_start = wave.M0_start.price
        m0_end = wave.M0_end.price
        m1_start = wave.M1_start.price
        m1_end = wave.M1_end.price
        m2_end = wave.M2_end.price

        # تشخیص جهت M0 و M1
        m0_direction = "DOWN" if m0_end < m0_start else "UP"  # M0 معمولاً خلاف جهت M1 است
        m1_direction = "UP" if m1_end > m1_start else "DOWN"

        # محاسبه موقعیت نسبی (بر اساس تصاویر)
        # اگر M0 نزولی و M1 صعودی باشد:
        if m0_direction == "DOWN" and m1_direction == "UP":
            # وضعیت 'a' (صفحه ۳۶۷، ۳۶۹، ۳۷۱، ۳۷۳، ۳۷۵، ۳۷۷، ۳۷۹)
            # M1 از M0 فراتر نمی‌رود (نقطه سفید در شروع و پایان)
            if m1_end <= m0_start:
                return M0M1Status.A
        
            # وضعیت 'b' (نقطه سیاه)
            # M1 فراتر می‌رود اما M2 به زیر M0 نمی‌رود
            if m1_end > m0_start and m2_end >= m0_end:
                return M0M1Status.B
        
            # وضعیت 'c' (نقطه سیاه/سفید)
            # M1 فراتر می‌رود و M2 به زیر M0 می‌رود اما به زیر M1 نمی‌رود
            if m1_end > m0_start and m2_end < m0_end and m2_end >= m1_start:
                return M0M1Status.C
        
            # وضعیت 'd' (نقطه سفید/سیاه)
            # M1 فراتر می‌رود و M2 به زیر M1 می‌رود
            if m1_end > m0_start and m2_end < m1_start:
                return M0M1Status.D
        
            # وضعیت 'e' و 'f' (مخصوص قانون ۲ و ۳)
            # اگر M2 به زیر M0 رفته و M3 دوباره از M1 فراتر رود
            if wave.M3_end is not None:
                m3_end = wave.M3_end.price
                if m3_end > m1_end and m2_end < m0_end:
                    return M0M1Status.E
                elif m3_end > m1_end * 1.618 and m2_end < m0_end:  # قانون ۳ وضعیت f
                    return M0M1Status.F
    
        # اگر M0 صعودی و M1 نزولی باشد (معکوس)
        elif m0_direction == "UP" and m1_direction == "DOWN":
            # وضعیت 'a': M1 از M0 فراتر نمی‌رود
            if m1_end >= m0_start:
                return M0M1Status.A
        
            # وضعیت 'b': M1 فراتر می‌رود و M2 به بالای M0 نمی‌رود
            if m1_end < m0_start and m2_end <= m0_end:
                return M0M1Status.B
        
            # وضعیت 'c': M1 فراتر می‌رود و M2 به بالای M0 می‌رود اما به بالای M1 نمی‌رود
            if m1_end < m0_start and m2_end > m0_end and m2_end <= m1_start:
                return M0M1Status.C
        
            # وضعیت 'd': M1 فراتر می‌رود و M2 به بالای M1 می‌رود
            if m1_end < m0_start and m2_end > m1_start:
                return M0M1Status.D
        
            # وضعیت 'e' و 'f' (مخصوص قانون ۲ و ۳)
            if wave.M3_end is not None:
                m3_end = wave.M3_end.price
                if m3_end < m1_end and m2_end > m0_end:
                    return M0M1Status.E
                elif m3_end < m1_end * 0.618 and m2_end > m0_end:
                    return M0M1Status.F

        return M0M1Status.UNKNOWN

    def _check_activation(self, wave: RetracementWave, rule: RetracementRule) -> Dict[str, Any]:
        """
        بررسی شرط فعال‌سازی (Activation) بر اساس دیاگرام‌های صفحات ۳۶۶ تا ۳۷۹.
        برای قوانین ۱، ۲، ۳، ۴، ۶ نیاز به فعال‌سازی است.
        فعال‌سازی بر اساس موقعیت M3_end نسبت به M1_end محاسبه می‌شود.
        """
        activation_result = {
            "needs_activation": True,
            "is_activated": False,
            "activation_condition": "",
            "activation_price_level": None
        }
    
        # قوانین ۵ و ۷ نیاز به فعال‌سازی ندارند
        if rule in [RetracementRule.RULE_5, RetracementRule.RULE_7]:
            activation_result["needs_activation"] = False
            activation_result["is_activated"] = True
            return activation_result
    
        # محاسبه دقیق فعال‌سازی بر اساس دیاگرام‌ها
        if wave.M3_end is not None:
            m1_end = wave.M1_end.price
            m1_start = wave.M1_start.price
            m3_end = wave.M3_end.price
            m2_end = wave.M2_end.price
        
            # قانون ۱ و ۲ و ۳ و ۴: فعال‌سازی زمانی است که M3 از M1 فراتر رود
            if rule in [RetracementRule.RULE_1, RetracementRule.RULE_2, 
                        RetracementRule.RULE_3, RetracementRule.RULE_4]:
                # شرط اصلی: M3 از M1 فراتر رود
                if m3_end > m1_end:
                    activation_result["is_activated"] = True
                    activation_result["activation_condition"] = "فعال‌سازی تایید شد: M3 از سقف M1 فراتر رفت."
                    activation_result["activation_price_level"] = m1_end
                # شرط جایگزین: M2 به زیر M1 بازگردد (طبق تصویر قانون ۱)
                elif m2_end < m1_start:
                    activation_result["is_activated"] = True
                    activation_result["activation_condition"] = "فعال‌سازی تایید شد: M2 به کف M1 بازگشت."
                    activation_result["activation_price_level"] = m1_start
                else:
                    activation_result["activation_condition"] = "فعال‌سازی نشده است. منتظر فراتر رفتن M3 از سقف M1 یا بازگشت M2 به کف M1 هستیم."
        
            # قانون ۶: فعال‌سازی نیازمند فراتر رفتن M3 از M1 با درصد مشخص (طبق صفحه ۳۷۶)
            elif rule == RetracementRule.RULE_6:
                if m3_end > m1_end * 1.1:  # حداقل ۱۰٪ فراتر
                    activation_result["is_activated"] = True
                    activation_result["activation_condition"] = "فعال‌سازی تایید شد: M3 حداقل ۱۰٪ از سقف M1 فراتر رفت (طبق قانون ۶)."
                    activation_result["activation_price_level"] = m1_end * 1.1
                else:
                    activation_result["activation_condition"] = f"فعال‌سازی نشده است. M3 باید حداقل ۱۰٪ از سقف M1 ({m1_end:.2f}) فراتر رود."
        else:
            activation_result["activation_condition"] = "M3 تعریف نشده است. برای فعال‌سازی نیاز به وجود M3 داریم."
    
        return activation_result
        
        # برای قوانین ۱ تا ۴ و ۶: بررسی فعال‌سازی
        if wave.M3_end is not None:
            # شرط فعال‌سازی اصلی: M3 از سقف M1 فراتر رود
            if wave.M3_end.price > wave.M1_end.price:
                activation_result["is_activated"] = True
                activation_result["activation_condition"] = "فعال‌سازی تایید شد: M3 از سقف M1 فراتر رفت."
            # شرط فعال‌سازی جایگزین: M2 به کف M1 بازگردد
            elif wave.M2_end.price <= wave.M1_start.price:
                activation_result["is_activated"] = True
                activation_result["activation_condition"] = "فعال‌سازی تایید شد: M2 به کف M1 بازگشت."
            else:
                activation_result["activation_condition"] = "فعال‌سازی نشده است. منتظر فراتر رفتن M3 از سقف M1 یا بازگشت M2 به کف M1 هستیم."
        
        return activation_result

    def _analyze_rule_1(self, wave: RetracementWave, status: M0M1Status) -> Dict[str, Any]:
        """
        قانون ۱: M1 کمتر از ۳۸.۲٪ توسط M2 بازگشت می‌شود.
        نیازمند فعال‌سازی است.
        صفحه ۳۶۶: دیاگرام وضعیت‌های a, b, c, d.
        """
        activation = self._check_activation(wave, RetracementRule.RULE_1)
        
        result = {
            "rule": RetracementRule.RULE_1,
            "status": status.value,
            "condition": "M2 < 38.2% of M1",
            "activation": activation,
            "description": "بازگشت کم عمق. نیاز به 'فعال‌سازی' برای تایید ادامه روند دارد.",
            "page_reference": "صفحه ۳۶۶",
            "diagram_reference": "صفحه ۳۶۷ (شناسایی وضعیت برای قانون ۱)"
        }
        return result

    def _analyze_rule_2(self, wave: RetracementWave, status: M0M1Status) -> Dict[str, Any]:
        """
        قانون ۲: M1 بین ۳۸.۲٪ تا ۶۱.۸٪ توسط M2 بازگشت می‌شود.
        نیازمند فعال‌سازی است.
        صفحه ۳۶۸: دیاگرام وضعیت‌های a, b, c, d, e.
        """
        activation = self._check_activation(wave, RetracementRule.RULE_2)
        
        result = {
            "rule": RetracementRule.RULE_2,
            "status": status.value,
            "condition": "38.2% ≤ M2 < 61.8% of M1",
            "activation": activation,
            "description": "بازگشت متوسط. نیاز به 'فعال‌سازی' برای تایید دارد.",
            "page_reference": "صفحه ۳۶۸",
            "diagram_reference": "صفحه ۳۶۹ (شناسایی وضعیت برای قانون ۲)"
        }
        return result

    def _analyze_rule_3(self, wave: RetracementWave, status: M0M1Status) -> Dict[str, Any]:
        """
        قانون ۳: M1 دقیقاً ۶۱.۸٪ توسط M2 بازگشت می‌شود.
        نیازمند فعال‌سازی است.
        صفحه ۳۷۰: دیاگرام وضعیت‌های a, b, c, d, e, f.
        """
        activation = self._check_activation(wave, RetracementRule.RULE_3)
        
        result = {
            "rule": RetracementRule.RULE_3,
            "status": status.value,
            "condition": "M2 = 61.8% of M1 (دقیقاً)",
            "activation": activation,
            "description": "بازگشت طلایی. نیاز به 'فعال‌سازی' دارد.",
            "page_reference": "صفحه ۳۷۰",
            "diagram_reference": "صفحه ۳۷۱ (شناسایی وضعیت برای قانون ۳)"
        }
        return result

    def _analyze_rule_4(self, wave: RetracementWave, status: M0M1Status) -> Dict[str, Any]:
        """
        قانون ۴: M1 بین ۶۱.۸٪ تا ۱۰۰٪ توسط M2 بازگشت می‌شود.
        نیازمند فعال‌سازی است.
        صفحه ۳۷۲: دیاگرام وضعیت‌های a, b, c, d, e.
        """
        activation = self._check_activation(wave, RetracementRule.RULE_4)
        
        result = {
            "rule": RetracementRule.RULE_4,
            "status": status.value,
            "condition": "61.8% < M2 < 100% of M1",
            "activation": activation,
            "description": "بازگشت عمیق (تا ۱۰۰٪). نیاز به 'فعال‌سازی' دارد.",
            "page_reference": "صفحه ۳۷२",
            "diagram_reference": "صفحه ۳۷۳ (شناسایی وضعیت برای قانون ۴)"
        }
        return result

    def _analyze_rule_5(self, wave: RetracementWave, status: M0M1Status) -> Dict[str, Any]:
        """
        قانون ۵: M1 بین ۱۰۰٪ تا ۱۶۱.۸٪ توسط M2 بازگشت می‌شود.
        فعال‌سازی الزامی نیست.
        صفحه ۳۷۴: دیاگرام وضعیت‌های a, b, c, d.
        """
        activation = self._check_activation(wave, RetracementRule.RULE_5)
        
        result = {
            "rule": RetracementRule.RULE_5,
            "status": status.value,
            "condition": "100% ≤ M2 < 161.8% of M1",
            "activation": activation,
            "description": "بازگشت کامل و فراتر (تا ۱۶۱.۸٪). به خودی خود معتبر است (احتمالاً بخشی از الگوی ترکیبی).",
            "page_reference": "صفحه ۳۷۴",
            "diagram_reference": "صفحه ۳۷۵ (شناسایی وضعیت برای قانون ۵)"
        }
        return result

    def _analyze_rule_6(self, wave: RetracementWave, status: M0M1Status) -> Dict[str, Any]:
        """
        قانون ۶: M1 بین ۱۶۱.۸٪ تا ۲۶۱.۸٪ توسط M2 بازگشت می‌شود.
        نیازمند فعال‌سازی است.
        صفحه ۳۷۶: دیاگرام وضعیت‌های a, b, c, d.
        """
        activation = self._check_activation(wave, RetracementRule.RULE_6)
        
        result = {
            "rule": RetracementRule.RULE_6,
            "status": status.value,
            "condition": "161.8% ≤ M2 < 261.8% of M1",
            "activation": activation,
            "description": "بازگشت بسیار عمیق. نیاز به 'فعال‌سازی' برای تعیین نوع الگوی اصلاحی دارد.",
            "page_reference": "صفحه ۳۷۶",
            "diagram_reference": "صفحه ۳۷۷ (شناسایی وضعیت برای قانون ۶)"
        }
        return result

    def _analyze_rule_7(self, wave: RetracementWave, status: M0M1Status) -> Dict[str, Any]:
        """
        قانون ۷: M1 بیش از ۲۶۱.۸٪ توسط M2 بازگشت می‌شود.
        فعال‌سازی الزامی نیست.
        صفحه ۳۷۸: دیاگرام وضعیت‌های a, b, c, d.
        """
        activation = self._check_activation(wave, RetracementRule.RULE_7)
        
        result = {
            "rule": RetracementRule.RULE_7,
            "status": status.value,
            "condition": "M2 ≥ 261.8% of M1",
            "activation": activation,
            "description": "بازگشت افراطی (>۲۶۱.۸٪). به خودی خود معتبر است (نشان‌دهنده شروع یک روند جدید/امواج مفقود).",
            "page_reference": "صفحه ۳۷۸",
            "diagram_reference": "صفحه ۳۷۹ (شناسایی وضعیت برای قانون ۷)"
        }
        return result

    def classify_wave(self, wave: RetracementWave) -> Dict[str, Any]:
        """
        نقطه ورود اصلی برای دسته‌بندی یک موج بر اساس قوانین بازگشت.
        این متد تمام قوانین ۱ تا ۷ را بر اساس تصاویر و جداول اعمال می‌کند.
        """
        wave.calculate_metrics()
        rule = self._get_rule_from_ratio(wave.retracement_ratio)
        status = self._determine_m0_m1_status(wave)

        analysis_result = {}
        if rule == RetracementRule.RULE_1:
            analysis_result = self._analyze_rule_1(wave, status)
        elif rule == RetracementRule.RULE_2:
            analysis_result = self._analyze_rule_2(wave, status)
        elif rule == RetracementRule.RULE_3:
            analysis_result = self._analyze_rule_3(wave, status)
        elif rule == RetracementRule.RULE_4:
            analysis_result = self._analyze_rule_4(wave, status)
        elif rule == RetracementRule.RULE_5:
            analysis_result = self._analyze_rule_5(wave, status)
        elif rule == RetracementRule.RULE_6:
            analysis_result = self._analyze_rule_6(wave, status)
        elif rule == RetracementRule.RULE_7:
            analysis_result = self._analyze_rule_7(wave, status)
        else:
            return {
                "error": "نسبت بازگشت قابل دسته‌بندی نیست. احتمال خطا در محاسبات امواج.",
                "ratio": wave.retracement_ratio
            }

        # اضافه کردن اطلاعات از فصل‌های پیشین برای اعتبارسنجی ساختار
        if self.chapter_11_data:
            analysis_result["chapter_11_validation"] = self.chapter_11_data.get("وضعیت", "نامشخص")
        if self.chapter_12_data:
            analysis_result["chapter_12_patterns"] = self.chapter_12_data.get("تعداد_الگوهای_یافت_شده", 0)
        if self.chapter_14_data:
            analysis_result["chapter_14_ratios"] = self.chapter_14_data.get("تطابق_با_نسبت‌های_فیبو", 0)

        analysis_result.update({
            "retracement_ratio": round(wave.retracement_ratio * 100, 2),
            "len_m0": round(wave.len_M0, 4),
            "len_m1": round(wave.len_M1, 4),
            "len_m2": round(wave.len_M2, 4),
            "m0_m1_ratio": round(wave.m0_m1_ratio, 4),
            "m1_start_price": wave.M1_start.price,
            "m1_end_price": wave.M1_end.price,
            "m2_end_price": wave.M2_end.price
        })

        return analysis_result

# ════════════════════════════════════════════════════════════════════
# بخش ۳: توابع استخراج موج از Context (فصل‌های ۱۱، ۱۲، ۱۴، ۱۶)
# ════════════════════════════════════════════════════════════════════

def _extract_waves_from_context(data: pd.DataFrame, context: Dict) -> List[RetracementWave]:
    """
    استخراج ساختار موج‌های M0, M1, M2, M3 از نتایج تحلیل فصل‌های پیشین.
    اولویت با فصل ۱۶ (قوانین معاینه) است. اگر موجود نبود، از نقاط عطف ساده استفاده می‌شود.
    """
    waves = []
    
    # اولویت ۱: استفاده از فصل ۱۶ (قوانین معاینه)
    if context and "chapter_16" in context:
        ch16_data = context["chapter_16"]
        if "examinations" in ch16_data:
            for exam in ch16_data["examinations"]:
                if exam.get("is_confirmed", False):
                    try:
                        # فرض بر این است که فصل ۱۶ ساختار کامل M0-M1-M2-M3 را در اختیار می‌گذارد
                        wave = RetracementWave(
                            M0_start=WavePoint(exam.get("m0_start_idx", 0), exam.get("m0_start_price", 0.0)),
                            M0_end=WavePoint(exam.get("m0_end_idx", 0), exam.get("m0_end_price", 0.0)),
                            M1_start=WavePoint(exam.get("m1_start_idx", 0), exam.get("m1_start_price", 0.0)),
                            M1_end=WavePoint(exam.get("m1_end_idx", 0), exam.get("m1_end_price", 0.0)),
                            M2_start=WavePoint(exam.get("m2_start_idx", 0), exam.get("m2_start_price", 0.0)),
                            M2_end=WavePoint(exam.get("m2_end_idx", 0), exam.get("m2_end_price", 0.0)),
                            M3_start=WavePoint(exam.get("m3_start_idx", 0), exam.get("m3_start_price", 0.0)),
                            M3_end=WavePoint(exam.get("m3_end_idx", 0), exam.get("m3_end_price", 0.0))
                        )
                        waves.append(wave)
                    except KeyError:
                        continue
    
    # اولویت ۲: اگر فصل ۱۶ کامل نبود، از داده‌های خام استفاده می‌کنیم
    if not waves:
        high = data['high'].values if 'high' in data.columns else data['High'].values
        low = data['low'].values if 'low' in data.columns else data['Low'].values
        
        from scipy.signal import argrelextrema
        peaks = argrelextrema(high, np.greater, order=3)[0]
        troughs = argrelextrema(low, np.less, order=3)[0]
        
        points = []
        for idx in peaks:
            points.append((int(idx), float(high[idx]), 'PEAK'))
        for idx in troughs:
            points.append((int(idx), float(low[idx]), 'TROUGH'))
        points.sort(key=lambda x: x[0])

        filtered = []
        for pt in points:
            if not filtered:
                filtered.append(pt)
                continue
            last = filtered[-1]
            if last[2] == pt[2]:
                if pt[2] == 'PEAK' and pt[1] > last[1]:
                    filtered[-1] = pt
                elif pt[2] == 'TROUGH' and pt[1] < last[1]:
                    filtered[-1] = pt
            else:
                filtered.append(pt)
        
        if len(filtered) < 5:
            return []
        
        for i in range(len(filtered) - 4):
            p0, p1, p2, p3, p4 = filtered[i:i+5]
            dirs = [p[2] for p in filtered[i:i+5]]
            if dirs == ['PEAK', 'TROUGH', 'PEAK', 'TROUGH', 'PEAK'] or \
               dirs == ['TROUGH', 'PEAK', 'TROUGH', 'PEAK', 'TROUGH']:
                wave = RetracementWave(
                    M0_start=WavePoint(p0[0], p0[1], p0[2]),
                    M0_end=WavePoint(p1[0], p1[1], p1[2]),
                    M1_start=WavePoint(p1[0], p1[1], p1[2]),
                    M1_end=WavePoint(p2[0], p2[1], p2[2]),
                    M2_start=WavePoint(p2[0], p2[1], p2[2]),
                    M2_end=WavePoint(p3[0], p3[1], p3[2]),
                    M3_start=WavePoint(p3[0], p3[1], p3[2]),
                    M3_end=WavePoint(p4[0], p4[1], p4[2])
                )
                waves.append(wave)
    
    return waves

# ════════════════════════════════════════════════════════════════════
# بخش ۴: تابع اصلی (Interface) برای main1.py
# ════════════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None, context=None) -> Dict:
    """
    فصل ۱۷: قوانین بازگشت (Rules of Retracement)
    
    پارامترها:
        data: DataFrame با ستون‌های OHLC
        logger: ResultsLogger (اختیاری)
        context: دیکشنری نتایج فصل‌های قبلی (مخصوصاً فصل ۱۱، ۱۲، ۱۴، ۱۶)
        
    خروجی:
        دیکشنری کامل نتایج تحلیل
    """
    close = data['close'].values if 'close' in data.columns else data['Close'].values
    n = len(close)
    
    final_results = {}
    
    if n < 20:
        return {
            "عنوان": "فصل ۱۷: قوانین بازگشت",
            "وضعیت": "داده_کافی_نیست",
            "تعداد_کندل": str(n),
            "پیام": "برای تحلیل قوانین بازگشت به حداقل ۲۰ کندل نیاز است."
        }

    # ── ۱. استخراج داده‌های فصل‌های پیشین از context ──
    ch11_data = context.get("chapter_11", {}) if context else {}
    ch12_data = context.get("chapter_12", {}) if context else {}
    ch14_data = context.get("chapter_14", {}) if context else {}
    ch16_data = context.get("chapter_16", {}) if context else {}
    
    # ── ۲. استخراج موج‌ها از context ──
    waves = _extract_waves_from_context(data, context)
    
    if not waves:
        return {
            "عنوان": "فصل ۱۷: قوانین بازگشت",
            "وضعیت": "نقاط_عطف_کافی_نیست",
            "پیام": "هیچ الگوی بازگشت معتبری (M0-M1-M2-M3) بر اساس داده‌های موجود یافت نشد.",
            "تعداد_امواج_تشخیص_داده_شده": 0
        }

    # ── ۳. تحلیل با استفاده از RetracementAnalyzer ──
    analyzer = RetracementAnalyzer(ch16_data, ch11_data, ch12_data, ch14_data)
    analyzed_results = []
    
    for wave in waves:
        result = analyzer.classify_wave(wave)
        analyzed_results.append(result)

    # ── ۴. خلاصه آمار ──
    rule_counts = {}
    activation_counts = {"نیازمند_فعال_سازی": 0, "فعال_سازی_شده": 0, "بدون_نیاز_به_فعال_سازی": 0}
    
    for res in analyzed_results:
        rule = res.get("rule", {}).value if isinstance(res.get("rule"), Enum) else res.get("rule", "نامشخص")
        rule_counts[rule] = rule_counts.get(rule, 0) + 1
        
        activation = res.get("activation", {})
        if activation.get("needs_activation", False):
            activation_counts["نیازمند_فعال_سازی"] += 1
            if activation.get("is_activated", False):
                activation_counts["فعال_سازی_شده"] += 1
        else:
            activation_counts["بدون_نیاز_به_فعال_سازی"] += 1

        # ⭐ استخراج نقاط موج M0 تا M5 از آخرین الگوی معتبر برای فصل ۱۸
    wave_points_for_export = []
    if analyzed_results:
        last_res = analyzed_results[-1]
        if "m1_start_price" in last_res:
            try:
                # فرض بر این است که M0 تا M5 در تحلیل آخرین موج ذخیره شده‌اند
                # اگر این کلیدها در تحلیل موجود نباشند، باید از موج‌های خام استخراج شوند
                wave_points_for_export = [
                    [0, last_res.get("m0_start_price", last_res.get("m1_start_price", 0.0)), 0],
                    [0, last_res.get("m1_start_price", 0.0), 0],
                    [0, last_res.get("m1_end_price", 0.0), 0],
                    [0, last_res.get("m2_end_price", 0.0), 0],
                    [0, last_res.get("m2_end_price", 0.0), 0],
                    [0, last_res.get("m3_end_price", 0.0) if "m3_end_price" in last_res else last_res.get("m2_end_price", 0.0), 0],
                ]
            except Exception:
                wave_points_for_export = []
    
    # این بخش را به final_results اضافه کنید
    final_results["wave_points"] = wave_points_for_export

    final_results = {
        "عنوان": "فصل ۱۷: قوانین بازگشت",
        "مرجع_کتاب": "صفحات ۳۶۴ تا ۳۸۰ - گلن نیلی",
        "وضعیت": "تحلیل_کامل",
        "تعداد_الگوهای_بازگشت_یافت_شده": len(analyzed_results),
        "توزیع_قوانین_بازگشت": rule_counts,
        "آمار_فعال_سازی": activation_counts,
        "جزئیات_تحلیل": analyzed_results[:15],  # نمایش ۱۵ الگوی اخیر
        "وابستگی‌های_استفاده_شده": {
            "فصل_۱۱": ch11_data.get("وضعیت", "نامشخص"),
            "فصل_۱۲": ch12_data.get("وضعیت", "نامشخص"),
            "فصل_۱۴": ch14_data.get("وضعیت", "نامشخص"),
            "فصل_۱۶": ch16_data.get("وضعیت", "نامشخص")
        }
    }

    # ════════════════════════════════════════════════════════════════════
    # تفسیر نهایی بر اساس جداول و تصاویر فصل ۱۷
    # ════════════════════════════════════════════════════════════════════
    final_results["تفسیر_نهایی"] = _build_final_interpretation(final_results, analyzed_results)
    
    if logger:
        logger.add_section("فصل ۱۷: قوانین بازگشت", level=1)
        logger.add_result("مرجع کتاب", "صفحات ۳۶۴ تا ۳۸۰")
        logger.add_result("کل الگوهای بازگشت", final_results["تعداد_الگوهای_بازگشت_یافت_شده"])
        logger.add_result("توزیع قوانین", json.dumps(rule_counts, ensure_ascii=False))
        logger.add_result("آمار فعال‌سازی", json.dumps(activation_counts, ensure_ascii=False))
        
        for idx, res in enumerate(analyzed_results[:5]):
            rule_val = res.get('rule', 'N/A')
            if hasattr(rule_val, 'value'):
                rule_val = rule_val.value
            logger.add_result(
                f"الگوی {idx+1}",
                f"{rule_val} | M2/M1: {res.get('retracement_ratio', 0)}% | وضعیت M0/M1: {res.get('status', 'N/A')}"
            )
        
        logger.add_result("تفسیر نهایی", final_results["تفسیر_نهایی"])

    # ⭐ استخراج نقاط موج M0 تا M5 برای فصل ۱۸
    wave_points_for_export = []
    if analyzed_results:
        last_res = analyzed_results[-1]
        try:
            wave_points_for_export = [
                [0, last_res.get("m0_start_price", last_res.get("m1_start_price", 0.0)), 0],
                [0, last_res.get("m1_start_price", 0.0), 0],
                [0, last_res.get("m1_end_price", 0.0), 0],
                [0, last_res.get("m2_end_price", 0.0), 0],
                [0, last_res.get("m2_end_price", 0.0), 0],
                [0, last_res.get("m3_end_price", 0.0) if "m3_end_price" in last_res else last_res.get("m2_end_price", 0.0), 0],
            ]
        except:
            wave_points_for_export = []
    final_results["wave_points"] = wave_points_for_export

    return final_results

def _build_final_interpretation(results: Dict, analyzed_results: List[Dict]) -> str:
    """تولید تفسیر نهایی کامل بر اساس جداول و تصاویر فصل ۱۷"""
    
    lines = []
    lines.append("═" * 80)
    lines.append("فصل ۱۷: قوانین بازگشت (Rules of Retracement) - تفسیر کامل")
    lines.append("مرجع: کتاب استادی در امواج الیوت - گلن نیلی | صفحات ۳۶۴-۳۸۰")
    lines.append("═" * 80)
    lines.append("")

    lines.append("📊 آمار کلی:")
    lines.append(f"   • کل الگوهای بازگشت یافت‌شده: {results.get('تعداد_الگوهای_بازگشت_یافت_شده', 0)}")
    lines.append(f"   • نیازمند فعال‌سازی: {results.get('آمار_فعال_سازی', {}).get('نیازمند_فعال_سازی', 0)}")
    lines.append(f"   • فعال‌سازی شده: {results.get('آمار_فعال_سازی', {}).get('فعال_سازی_شده', 0)}")
    lines.append(f"   • بدون نیاز به فعال‌سازی: {results.get('آمار_فعال_سازی', {}).get('بدون_نیاز_به_فعال_سازی', 0)}")
    lines.append("")

    lines.append("📈 توزیع قوانین بازگشت (بر اساس جدول صفحه ۳۶۴):")
    for rule, count in results.get("توزیع_قوانین_بازگشت", {}).items():
        lines.append(f"   • {rule}: {count} مورد")

    lines.append("")
    lines.append("📋 جزئیات قوانین (صفحات ۳۶۶ تا ۳۷۹):")
    lines.append("")
    
    # قانون ۱
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ قانون ۱: بازگشت کمتر از ۳۸.۲% (صفحه ۳۶۶)                        │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ نیازمند فعال‌سازی است.                                             │")
    lines.append("   │ وضعیت‌های M0/M1: a (نقطه سفید)، b (نقطه سیاه)، c (سیاه/سفید)، d (سفید/سیاه) │")
    lines.append("   │ تفسیر: بازگشت کم‌عمق است. برای تایید ادامه روند، باید M3 از سقف  │")
    lines.append("   │        M1 فراتر رود یا M2 به کف M1 بازگردد.                     │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    # قانون ۲
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ قانون ۲: بازگشت بین ۳۸.۲% تا ۶۱.۸% (صفحه ۳۶۸)                   │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ نیازمند فعال‌سازی است.                                             │")
    lines.append("   │ وضعیت‌های M0/M1: a, b, c, d, e (نقطه سفید)                      │")
    lines.append("   │ تفسیر: بازگشت متوسط. نیاز به فعال‌سازی دارد. اگر M3 از سقف      │")
    lines.append("   │        M1 فراتر رود، الگو تایید می‌شود.                         │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    # قانون ۳
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ قانون ۳: بازگشت دقیقاً ۶۱.۸% (صفحه ۳۷۰)                          │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ نیازمند فعال‌سازی است.                                             │")
    lines.append("   │ وضعیت‌های M0/M1: a, b, c, d, e, f (نقطه سفید)                   │")
    lines.append("   │ تفسیر: بازگشت طلایی. نیاز به فعال‌سازی دارد. وضعیت 'f'         │")
    lines.append("   │        نشان‌دهنده ساختار پیچیده‌تر است.                         │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    # قانون ۴
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ قانون ۴: بازگشت بین ۶۱.۸% تا ۱۰۰% (صفحه ۳۷۲)                    │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ نیازمند فعال‌سازی است.                                             │")
    lines.append("   │ وضعیت‌های M0/M1: a, b, c, d, e                                  │")
    lines.append("   │ تفسیر: بازگشت عمیق. نیاز به فعال‌سازی دارد. اگر M3 از سقف      │")
    lines.append("   │        M1 فراتر رود، الگو تایید می‌شود.                         │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    # قانون ۵
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ قانون ۵: بازگشت بین ۱۰۰% تا ۱۶۱.۸% (صفحه ۳۷۴)                   │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ فعال‌سازی الزامی نیست.                                            │")
    lines.append("   │ وضعیت‌های M0/M1: a, b, c, d                                     │")
    lines.append("   │ تفسیر: M2 به عنوان یک موج اصلاحی یا بخشی از یک الگوی ترکیبی    │")
    lines.append("   │        تفسیر می‌شود. به خودی خود معتبر است.                    │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    # قانون ۶
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ قانون ۶: بازگشت بین ۱۶۱.۸% تا ۲۶۱.۸% (صفحه ۳۷۶)                 │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ نیازمند فعال‌سازی است.                                             │")
    lines.append("   │ وضعیت‌های M0/M1: a, b, c, d                                     │")
    lines.append("   │ تفسیر: بازگشت بسیار عمیق. نیاز به فعال‌سازی برای تعیین نوع     │")
    lines.append("   │        الگوی اصلاحی دارد. M3 باید از سقف M1 فراتر رود.         │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    # قانون ۷
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ قانون ۷: بازگشت بیش از ۲۶۱.۸% (صفحه ۳۷۸)                        │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ فعال‌سازی الزامی نیست.                                            │")
    lines.append("   │ وضعیت‌های M0/M1: a, b, c, d                                     │")
    lines.append("   │ تفسیر: بازگشت افراطی. به خودی خود معتبر است و نشان‌دهنده شروع │")
    lines.append("   │        یک روند جدید یا وجود امواج مفقود است.                    │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")

    lines.append("")
    lines.append("💡 نتیجه نئوویو (صفحه ۳۶۴ و تصاویر):")
    lines.append("   • 'فعال‌سازی' (Activation) به معنای آن است که حرکت بعدی بازار")
    lines.append("     (موج M3 به بعد) باید ورای نقطه شروع موج M1 حرکت کند تا قانون اعتبار یابد.")
    lines.append("   • قوانین ۱ تا ۴ و ۶ نیازمند فعال‌سازی هستند. قوانین ۵ و ۷ به خودی خود معتبرند.")
    lines.append("   • برای استفاده از این قوانین در 'پیش‌ساخت منطقی'، لازم است ساختارهای")
    lines.append("     M0 و M2 از طریق 'قوانین معاینه' (فصل ۱۶) تایید شده باشند.")
    lines.append("")

    lines.append("═" * 80)
    lines.append("پایان تفسیر فصل ۱۷")
    lines.append("═" * 80)

    return "\n".join(lines)