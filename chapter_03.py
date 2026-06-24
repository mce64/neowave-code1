"""
فصل ۳: ساختار دوره کامل امواج الیوت و اثر فراکتال در آن
منبع: کتاب "امواج الیوت به سبک نئوویو" - گلن نیلی - صفحه ۲۲

═══════════════════════════════════════════════════════════════════
محتوای دقیق فصل ۳ (صفحه ۲۲ کتاب):

دیاگرام Complete Market Cycle:
  ├── Motive Wave (Impulse)    : 5 موج شتابدار
  │     اعداد فیبو محور: 1 → 5 → 21 → 89
  └── Corrective Wave (Zigzag): 3 موج اصلاحی
        اعداد فیبو محور: 2 → 8 → 34 → 144
  مجموع چرخه کامل = 144 واحد فیبوناچی (Grand Supercycle)

قوانین نقض‌ناپذیر (فصل ۳ و ۱۱):
  قانون ۱: موج ۲ هرگز از شروع موج ۱ عبور نمی‌کند
  قانون ۲: موج ۳ هرگز کوتاه‌ترین موج شتابدار نیست
  قانون ۳: موج ۴ هرگز با قلمرو قیمتی موج ۱ همپوشانی ندارد
  قانون ۴: موج ۱، ۳، ۵ خود شتابدار (5 ریزموج)
  قانون ۵: موج ۲، ۴، A، B، C خود اصلاحی (3 ریزموج)

انواع Extension فاز شتابدار (فصل ۱۱):
  موج ۱ ممتد: موج ۱ بزرگ‌ترین، موج ۳ باید ≥ ۶۱.۸٪ موج ۱ باشد
               موج ۵ باید ≥ ۹۹٪ موج ۳ باشد
  موج ۳ ممتد: رایج‌ترین | موج ۳ ≥ ۱۶۱.۸٪ موج ۱
               موج ۲ بیش از ۶۱.۸٪ موج ۱ را اصلاح نمی‌کند
               موج ۴ معمولاً < ۳۸.۲٪ موج ۳
               موج ۵ باید < ۶۱.۸٪ موج ۳ باشد
  موج ۵ ممتد: امواج ۱ و ۳ معمولاً زمانی برابر
               موج ۳ باید ۱۰۰٪ تا ۱۶۱.۸٪ موج ۱ باشد
               موج ۴ حداکثر ۶۱.۸٪ موج ۳ را اصلاح کند
               موج ۵ باید ۱۰۰٪ تا ۱۶۱.۸٪ مجموع موج ۱ تا ۳ باشد
  امتداد دوگانه: موج ۳ > ۱۶۱.۸٪ موج ۱ AND موج ۵ > ۱۶۱.۸٪ موج ۳
  امتداد سه‌گانه: بسیار نادر
  موج ۵ کوتاه (Truncated): قله موج ۵ از قله موج ۳ فراتر نمی‌رود

انواع الگوی اصلاحی A-B-C (فصل ۱۲):
  ZigZag       : B/A < 0.618  →  C/A ≈ 0.618 تا 1.618
  Flat Common  : 0.618 ≤ B/A < 1.0  →  C/A ≈ 1.0
  Irregular Flat: 1.0 ≤ B/A ≤ 1.382  →  C/A ≈ 1.0 تا 1.618
  Running Corr : B/A > 1.382  →  موج C از شروع موج A فراتر نمی‌رود

نسبت اصلاح کل فاز اصلاحی (A-B-C) نسبت به فاز شتابدار:
  معمول: ۳۸.۲٪ تا ۶۱.۸٪ کل فاز شتابدار
  حداقل: ۲۳.۶٪  |  حداکثر: ۱۰۰٪

اثر فراکتال:
  هر موج شتابدار از 5 ریزموج همان فاز تشکیل شده
  هر موج اصلاحی از 3 ریزموج همان فاز تشکیل شده
  این تکرار در تمام درجات (Subminuette → Grand Supercycle) ادامه دارد
═══════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from enum import Enum


# ════════════════════════════════════════════════════════════════
# بخش ۱: Enum ها و ساختارهای داده
# ════════════════════════════════════════════════════════════════

class WaveType(Enum):
    MOTIVE     = "motive"
    CORRECTIVE = "corrective"
    UNKNOWN    = "unknown"


class WavePhase(Enum):
    IMPULSE_1    = "wave_1"
    IMPULSE_2    = "wave_2"
    IMPULSE_3    = "wave_3"
    IMPULSE_4    = "wave_4"
    IMPULSE_5    = "wave_5"
    CORRECTIVE_A = "wave_A"
    CORRECTIVE_B = "wave_B"
    CORRECTIVE_C = "wave_C"


class ExtensionType(Enum):
    """
    انواع Extension فاز شتابدار - فصل ۱۱ کتاب نیلی
    صفحات ۶۱، ۶۳، ۶۷، ۷۰
    """
    NO_EXTENSION     = "بدون_امتداد"
    FIRST_WAVE_EXT   = "موج_۱_ممتد"      # صفحه ۶۱ - نادرترین
    THIRD_WAVE_EXT   = "موج_۳_ممتد"      # صفحه ۶۳ - رایج‌ترین
    FIFTH_WAVE_EXT   = "موج_۵_ممتد"      # صفحه ۶۷ - رایج
    FIFTH_TRUNCATED  = "موج_۵_کوتاه_شده" # صفحه ۷۳ - Truncated/Failure
    DOUBLE_EXTENSION = "امتداد_دوگانه"   # صفحه ۷۲ - بسیار نادر
    TRIPLE_EXTENSION = "امتداد_سه‌گانه"  # نادرترین


class CorrectiveType(Enum):
    """
    انواع الگوی اصلاحی A-B-C - فصل ۱۲ کتاب نیلی
    بر اساس نسبت B/A
    """
    ZIGZAG         = "ZigZag"           # B/A < 0.618
    FLAT_COMMON    = "Flat_Common"      # 0.618 ≤ B/A < 1.0
    IRREGULAR_FLAT = "Irregular_Flat"   # 1.0 ≤ B/A ≤ 1.382
    RUNNING        = "Running"          # B/A > 1.382
    UNKNOWN        = "نامشخص"


class CycleCompleteness(Enum):
    COMPLETE         = "چرخه_کامل_8موجی"
    IMPULSE_ONLY     = "فقط_فاز_شتابدار"
    CORRECTIVE_ONLY  = "فقط_فاز_اصلاحی"
    INCOMPLETE       = "ناقص"


@dataclass
class Monowave:
    """تک‌موج پایه - کوچک‌ترین واحد تحلیل"""
    start_idx   : int
    end_idx     : int
    start_price : float
    end_price   : float
    direction   : int    # +1 صعودی، -1 نزولی
    price_range : float  # دامنه مطلق
    duration    : int    # تعداد کندل

    def __post_init__(self):
        self.price_range = abs(self.end_price - self.start_price)
        self.duration    = max(1, self.end_idx - self.start_idx)


@dataclass
class WaveSegment:
    """یک موج با جزئیات کامل در ساختار چرخه"""
    phase        : WavePhase
    start_idx    : int
    end_idx      : int
    start_price  : float
    end_price    : float
    direction    : int
    price_range  : float
    duration     : int
    wave_type    : WaveType
    is_extended  : bool  = False
    is_truncated : bool  = False
    fib_ratios   : Dict  = field(default_factory=dict)
    errors       : List  = field(default_factory=list)

    def __post_init__(self):
        self.price_range = abs(self.end_price - self.start_price)
        self.duration    = max(1, self.end_idx - self.start_idx)


@dataclass
class CompleteCycle:
    """چرخه کامل ۸ موجی - قلب فصل ۳"""
    start_idx        : int
    end_idx          : int
    start_price      : float
    end_price        : float
    direction        : int               # +1 صعودی، -1 نزولی
    impulse_phase    : List[WaveSegment] # 5 موج شتابدار
    corrective_phase : List[WaveSegment] # 3 موج اصلاحی
    extension_type   : ExtensionType
    corrective_type  : CorrectiveType
    completeness     : CycleCompleteness
    fractal_level    : int = 0
    fib_relationships: Dict = field(default_factory=dict)
    violations       : List = field(default_factory=list)


# ════════════════════════════════════════════════════════════════
# بخش ۲: استخراج تک‌موج‌ها (Monowaves)
# ════════════════════════════════════════════════════════════════

def _extract_monowaves(
    high  : np.ndarray,
    low   : np.ndarray,
    order : int = 3
) -> List[Monowave]:
    """
    استخراج Monowave ها از آرایه‌های قیمتی.
    نقاط عطف (peak/trough) شناسایی شده، هم‌نوع‌های متوالی حذف می‌شوند.
    """
    peak_idx   = argrelextrema(high, np.greater, order=order)[0]
    trough_idx = argrelextrema(low,  np.less,    order=order)[0]

    pts = []
    for i in peak_idx:
        pts.append((int(i), float(high[i]), "PEAK"))
    for i in trough_idx:
        pts.append((int(i), float(low[i]),  "TROUGH"))
    pts.sort(key=lambda x: x[0])

    # حذف هم‌نوع‌های متوالی - نگه‌داشتن بهترین
    filtered = []
    for pt in pts:
        if not filtered:
            filtered.append(pt)
            continue
        last = filtered[-1]
        if last[2] == pt[2]:
            if pt[2] == "PEAK"   and pt[1] > last[1]:  filtered[-1] = pt
            if pt[2] == "TROUGH" and pt[1] < last[1]:  filtered[-1] = pt
        else:
            filtered.append(pt)

    if len(filtered) < 2:
        return []

    monowaves = []
    for i in range(len(filtered) - 1):
        i0, p0, _ = filtered[i]
        i1, p1, _ = filtered[i + 1]
        monowaves.append(Monowave(
            start_idx=i0, end_idx=i1,
            start_price=float(p0), end_price=float(p1),
            direction=1 if p1 > p0 else -1,
            price_range=abs(p1 - p0),
            duration=max(1, i1 - i0)
        ))
    return monowaves


# ════════════════════════════════════════════════════════════════
# بخش ۳: اعتبارسنج فاز شتابدار (ImpulseValidator)
# ════════════════════════════════════════════════════════════════

class ImpulseValidator:
    """
    اعتبارسنجی کامل فاز شتابدار ۵ موجی.
    مطابق فصل ۳ (قوانین نقض‌ناپذیر) و فصل ۱۱ (انواع Extension).
    """

    # حدود Extension از کتاب نیلی
    EXT_MIN  = 1.618   # حداقل نسبت برای Extension (صفحه ۶۰)
    EXT_MAX  = 2.618   # حداکثر معمول

    @staticmethod
    def validate(
        waves: List[Monowave]
    ) -> Tuple[bool, List[str], Dict[str, float], ExtensionType, bool]:
        """
        اعتبارسنجی کامل ۵ موج شتابدار.

        خروجی:
            (is_valid, errors, ratios, extension_type, is_truncated)
        """
        errors     : List[str]       = []
        ratios     : Dict[str, float] = {}
        ext_type   : ExtensionType   = ExtensionType.NO_EXTENSION
        truncated  : bool            = False

        if len(waves) < 5:
            return False, ["طول باید ۵ باشد"], {}, ExtensionType.NO_EXTENSION, False

        w1, w2, w3, w4, w5 = waves[:5]
        base_dir = w1.direction

        # ── بررسی جهت‌های متناوب ──────────────────────────────
        expected_dirs = [base_dir, -base_dir, base_dir, -base_dir, base_dir]
        actual_dirs   = [w.direction for w in [w1, w2, w3, w4, w5]]
        if actual_dirs != expected_dirs:
            errors.append(
                f"جهت‌های متناوب نادرست: {actual_dirs} (انتظار: {expected_dirs})"
            )
            return False, errors, {}, ExtensionType.NO_EXTENSION, False

        # ── قانون ۱: موج ۲ از شروع موج ۱ عبور نمی‌کند ─────────
        # (فصل ۳، صفحه ۲۲)
        if base_dir == 1:   # صعودی
            if w2.end_price <= w1.start_price:
                errors.append(
                    f"نقض قانون ۱: موج۲ ({w2.end_price:.4f}) "
                    f"≤ شروع موج۱ ({w1.start_price:.4f})"
                )
        else:               # نزولی
            if w2.end_price >= w1.start_price:
                errors.append(
                    f"نقض قانون ۱: موج۲ ({w2.end_price:.4f}) "
                    f"≥ شروع موج۱ ({w1.start_price:.4f})"
                )

        # ── قانون ۲: موج ۳ کوتاه‌ترین نیست ────────────────────
        # (فصل ۳، صفحه ۲۲)
        motive_ranges = [w1.price_range, w3.price_range, w5.price_range]
        if w3.price_range == min(motive_ranges):
            errors.append(
                f"نقض قانون ۲: موج۳ ({w3.price_range:.4f}) "
                f"کوتاه‌ترین موج شتابدار است"
            )

        # ── قانون ۳: موج ۴ با قلمرو موج ۱ همپوشانی ندارد ─────
        # (فصل ۳، صفحه ۲۲)
        if base_dir == 1:
            w1_high = w1.end_price
            w4_low  = w4.end_price
            if w4_low < w1_high:
                errors.append(
                    f"نقض قانون ۳: موج۴ ({w4_low:.4f}) "
                    f"با قلمرو موج۱ (بالا={w1_high:.4f}) همپوشانی دارد"
                )
        else:
            w1_low  = w1.end_price
            w4_high = w4.end_price
            if w4_high > w1_low:
                errors.append(
                    f"نقض قانون ۳: موج۴ ({w4_high:.4f}) "
                    f"با قلمرو موج۱ (پایین={w1_low:.4f}) همپوشانی دارد"
                )

        # ── محاسبه نسبت‌های فیبوناچی ───────────────────────────
        if w1.price_range > 0:
            ratios["W3/W1"] = round(w3.price_range / w1.price_range, 3)
            ratios["W5/W1"] = round(w5.price_range / w1.price_range, 3)
            ratios["W2/W1"] = round(w2.price_range / w1.price_range, 3)
        if w3.price_range > 0:
            ratios["W4/W3"] = round(w4.price_range / w3.price_range, 3)
            ratios["W5/W3"] = round(w5.price_range / w3.price_range, 3)
        if w1.price_range > 0 and w3.price_range > 0:
            total_1_to_3 = abs(w3.end_price - w1.start_price)
            if total_1_to_3 > 0:
                ratios["W5/total_1_3"] = round(
                    w5.price_range / total_1_to_3, 3
                )

        # ── تشخیص نوع Extension (فصل ۱۱) ─────────────────────
        ext_type, truncated = ImpulseValidator._detect_extension(
            w1, w2, w3, w4, w5, ratios
        )

        is_valid = len(errors) == 0
        return is_valid, errors, ratios, ext_type, truncated

    @staticmethod
    def _detect_extension(
        w1: Monowave, w2: Monowave, w3: Monowave,
        w4: Monowave, w5: Monowave,
        ratios: Dict
    ) -> Tuple[ExtensionType, bool]:
        """
        تشخیص دقیق نوع Extension مطابق فصل ۱۱ کتاب.

        صفحه ۶۱ (موج ۱ ممتد):
            - موج ۱ بزرگ‌ترین موج
            - موج ۳ باید حداقل ۶۱.۸٪ موج ۱ باشد (نه الزاماً ۱۶۱.۸٪)
            - سطح پیچیدگی موج ۱ نمی‌تواند بیش از موج ۳ و ۵ باشد

        صفحه ۶۳ (موج ۳ ممتد):
            - رایج‌ترین نوع
            - موج ۳ ≥ ۱۶۱.۸٪ موج ۱
            - موج ۲ بیش از ۶۱.۸٪ موج ۱ را اصلاح نمی‌کند
            - موج ۴ معمولاً < ۳۸.۲٪ موج ۳
            - موج ۵ باید < ۶۱.۸٪ موج ۳ باشد

        صفحه ۶۷ (موج ۵ ممتد):
            - امواج ۱ و ۳ معمولاً زمانی برابر
            - موج ۳ باید ۱۰۰٪ تا ۱۶۱.۸٪ موج ۱ باشد
            - موج ۴ حداکثر ۶۱.۸٪ موج ۳ را اصلاح کند
            - موج ۵ باید ۱۰۰٪ تا ۱۶۱.۸٪ مجموع موج ۱ تا ۳ باشد

        صفحه ۷۳ (موج ۵ کوتاه / Truncated):
            - قله موج ۵ از قله موج ۳ فراتر نمی‌رود (صعودی)
            - وقوع امتداد یا کشیدگی در موج ۳ الزامی است

        صفحه ۷۲ (امتداد دوگانه):
            - موج ۳ > ۱۶۱.۸٪ موج ۱ AND موج ۵ > ۱۶۱.۸٪ موج ۳
        """
        r1 = w1.price_range
        r3 = w3.price_range
        r5 = w5.price_range
        EXT = ImpulseValidator.EXT_MIN  # 1.618

        # ── بررسی Truncated (موج ۵ کوتاه شده) - صفحه ۷۳ ──────
        base_dir = w1.direction
        if base_dir == 1:
            truncated = w5.end_price <= w3.end_price
        else:
            truncated = w5.end_price >= w3.end_price

        if truncated:
            return ExtensionType.FIFTH_TRUNCATED, True

        # ── بررسی امتداد دوگانه - صفحه ۷۲ ────────────────────
        if (r3 > 0 and r1 > 0 and
                r3 >= r1 * EXT and r5 >= r3 * EXT):
            return ExtensionType.DOUBLE_EXTENSION, False

        # ── بررسی موج ۳ ممتد - صفحه ۶۳ (رایج‌ترین) ───────────
        w2_retrace = ratios.get("W2/W1", 0)
        w4_retrace = ratios.get("W4/W3", 0)
        w5_w3_ratio = ratios.get("W5/W3", 0)
        if (r1 > 0 and r3 >= r1 * EXT):
            # تأییدهای اضافی از صفحه ۶۳:
            # موج ۲ بیش از ۶۱.۸٪ موج ۱ را اصلاح نمی‌کند
            # موج ۵ باید < ۶۱.۸٪ موج ۳ باشد
            if w2_retrace <= 0.618 and (w5_w3_ratio == 0 or w5_w3_ratio < 0.618):
                return ExtensionType.THIRD_WAVE_EXT, False
            return ExtensionType.THIRD_WAVE_EXT, False

        # ── بررسی موج ۵ ممتد - صفحه ۶۷ ──────────────────────
        w5_total_ratio = ratios.get("W5/total_1_3", 0)
        if (r5 > r3 and r5 > r1 and
                r3 > 0 and r1 > 0 and
                1.0 <= r3 / r1 <= 1.618):
            # موج ۵ باید ۱۰۰٪ تا ۱۶۱.۸٪ مجموع ۱ تا ۳
            if w5_total_ratio >= 1.0:
                return ExtensionType.FIFTH_WAVE_EXT, False

        # ── بررسی موج ۱ ممتد - صفحه ۶۱ ──────────────────────
        if (r1 > r3 and r1 > r5 and
                r3 > 0 and r3 <= r1 * 0.618):
            return ExtensionType.FIRST_WAVE_EXT, False

        return ExtensionType.NO_EXTENSION, False

    @staticmethod
    def find_all(
        monowaves: List[Monowave]
    ) -> List[Dict]:
        """جستجوی تمام الگوهای شتابدار ۵ موجی معتبر"""
        results = []
        n = len(monowaves)
        for i in range(n - 4):
            seg = monowaves[i: i + 5]
            is_valid, errors, ratios, ext_type, truncated = ImpulseValidator.validate(seg)

            # فقط الگوهای معتبر (بدون خطا یا با حداکثر ۱ خطا جزئی)
            if len(errors) <= 1:
                w1, w2, w3, w4, w5 = seg
                results.append({
                    "start_idx"    : w1.start_idx,
                    "end_idx"      : w5.end_idx,
                    "start_price"  : float(w1.start_price),
                    "end_price"    : float(w5.end_price),
                    "direction"    : w1.direction,
                    "dir_str"      : "صعودی" if w1.direction == 1 else "نزولی",
                    "is_valid"     : is_valid,
                    "errors"       : errors,
                    "ratios"       : ratios,
                    "ext_type"     : ext_type,
                    "is_truncated" : truncated,
                    "w1_range"     : float(w1.price_range),
                    "w2_range"     : float(w2.price_range),
                    "w3_range"     : float(w3.price_range),
                    "w4_range"     : float(w4.price_range),
                    "w5_range"     : float(w5.price_range),
                    "position"     : i,
                })
        return results


# ════════════════════════════════════════════════════════════════
# بخش ۴: اعتبارسنج فاز اصلاحی (CorrectiveValidator)
# ════════════════════════════════════════════════════════════════

class CorrectiveValidator:
    """
    اعتبارسنجی فاز اصلاحی ۳ موجی (A-B-C).
    مطابق فصل ۱۲ کتاب نیلی (صفحات ۷۱ به بعد).
    """

    @staticmethod
    def validate(
        waves: List[Monowave]
    ) -> Tuple[bool, List[str], Dict[str, float], CorrectiveType]:
        """
        اعتبارسنجی ۳ موج اصلاحی A-B-C.

        خروجی:
            (is_valid, errors, ratios, corrective_type)
        """
        errors  : List[str]       = []
        ratios  : Dict[str, float] = {}
        c_type  : CorrectiveType  = CorrectiveType.UNKNOWN

        if len(waves) < 3:
            return False, ["طول باید ۳ باشد"], {}, CorrectiveType.UNKNOWN

        wA, wB, wC = waves[:3]

        # ── بررسی جهت A و C هم‌جهت، B خلاف ──────────────────
        if wA.direction != wC.direction:
            errors.append(
                f"موج A (جهت={wA.direction}) و C (جهت={wC.direction}) "
                f"باید هم‌جهت باشند"
            )
        if wB.direction == wA.direction:
            errors.append(
                f"موج B باید خلاف جهت A باشد "
                f"(A={wA.direction}, B={wB.direction})"
            )

        # ── محاسبه نسبت‌های فیبوناچی ───────────────────────────
        if wA.price_range > 0:
            b_a = wB.price_range / wA.price_range
            c_a = wC.price_range / wA.price_range
            ratios["B/A"] = round(b_a, 3)
            ratios["C/A"] = round(c_a, 3)

            # ── طبقه‌بندی نوع اصلاحی مطابق فصل ۱۲ ────────────
            # صفحه ۷۶ و ۸۵ کتاب:
            # ZigZag: B/A < 0.618، B به شدت اصلاح می‌کند
            # Flat Common: 0.618 ≤ B/A < 1.0
            # Irregular Flat: 1.0 ≤ B/A ≤ 1.382
            # Running: B/A > 1.382، C از شروع A فراتر نمی‌رود
            if b_a < 0.618:
                c_type = CorrectiveType.ZIGZAG
                # تأیید ZigZag: C باید حداقل ۶۱.۸٪ A باشد
                if c_a < 0.618:
                    errors.append(
                        f"ZigZag: موج C ({c_a:.3f}) باید حداقل ۰.۶۱۸ برابر A باشد"
                    )
            elif b_a < 1.0:
                c_type = CorrectiveType.FLAT_COMMON
            elif b_a <= 1.382:
                c_type = CorrectiveType.IRREGULAR_FLAT
            else:
                c_type = CorrectiveType.RUNNING
                # Running: موج C نباید از شروع A فراتر رود
                if wA.direction == 1:  # اصلاح نزولی
                    if wC.end_price < wA.start_price:
                        errors.append(
                            f"Running Correction: موج C ({wC.end_price:.4f}) "
                            f"از شروع A ({wA.start_price:.4f}) گذشته است"
                        )
                else:
                    if wC.end_price > wA.start_price:
                        errors.append(
                            f"Running Correction: موج C ({wC.end_price:.4f}) "
                            f"از شروع A ({wA.start_price:.4f}) گذشته است"
                        )

        is_valid = len(errors) == 0
        return is_valid, errors, ratios, c_type

    @staticmethod
    def find_all(
        monowaves: List[Monowave]
    ) -> List[Dict]:
        """جستجوی تمام الگوهای اصلاحی ۳ موجی معتبر"""
        results = []
        n = len(monowaves)
        for i in range(n - 2):
            seg = monowaves[i: i + 3]
            is_valid, errors, ratios, c_type = CorrectiveValidator.validate(seg)
            if is_valid:
                wA, wB, wC = seg
                results.append({
                    "start_idx"   : wA.start_idx,
                    "end_idx"     : wC.end_idx,
                    "start_price" : float(wA.start_price),
                    "end_price"   : float(wC.end_price),
                    "direction"   : wA.direction,
                    "dir_str"     : "صعودی" if wA.direction == 1 else "نزولی",
                    "is_valid"    : is_valid,
                    "errors"      : errors,
                    "ratios"      : ratios,
                    "c_type"      : c_type,
                    "wA_range"    : float(wA.price_range),
                    "wB_range"    : float(wB.price_range),
                    "wC_range"    : float(wC.price_range),
                    "position"    : i,
                })
        return results


# ════════════════════════════════════════════════════════════════
# بخش ۵: سازنده چرخه کامل (CycleBuilder)
# ════════════════════════════════════════════════════════════════

class CycleBuilder:
    """
    ترکیب فاز شتابدار + فاز اصلاحی = چرخه کامل ۸ موجی.
    مطابق دیاگرام صفحه ۲۲ کتاب نیلی.
    """

    @staticmethod
    def _make_wave_segment(
        mw: Monowave, phase: WavePhase, wave_type: WaveType
    ) -> WaveSegment:
        return WaveSegment(
            phase=phase,
            start_idx=mw.start_idx, end_idx=mw.end_idx,
            start_price=float(mw.start_price), end_price=float(mw.end_price),
            direction=mw.direction,
            price_range=float(mw.price_range),
            duration=mw.duration,
            wave_type=wave_type,
        )

    @staticmethod
    def build_cycle(
        imp_pat   : Dict,
        corr_pat  : Dict,
        monowaves : List[Monowave],
        fractal_level: int = 0
    ) -> Optional[CompleteCycle]:
        """
        ساخت یک CompleteCycle از یک الگوی شتابدار + یک الگوی اصلاحی.
        شرط: فاز اصلاحی بلافاصله بعد از فاز شتابدار شروع می‌شود.
        """
        # اتصال: پایان شتابدار = شروع اصلاحی
        if imp_pat["end_idx"] != corr_pat["start_idx"]:
            return None

        # جهت فاز اصلاحی باید خلاف شتابدار باشد
        if imp_pat["direction"] == corr_pat["direction"]:
            return None

        # ساخت WaveSegment های فاز شتابدار
        imp_pos = imp_pat["position"]
        imp_phases_order = [
            WavePhase.IMPULSE_1, WavePhase.IMPULSE_2, WavePhase.IMPULSE_3,
            WavePhase.IMPULSE_4, WavePhase.IMPULSE_5
        ]
        imp_types_order = [
            WaveType.MOTIVE, WaveType.CORRECTIVE, WaveType.MOTIVE,
            WaveType.CORRECTIVE, WaveType.MOTIVE
        ]
        impulse_segs = []
        for k in range(5):
            mw = monowaves[imp_pos + k]
            impulse_segs.append(
                CycleBuilder._make_wave_segment(
                    mw, imp_phases_order[k], imp_types_order[k]
                )
            )

        # ساخت WaveSegment های فاز اصلاحی
        corr_pos = corr_pat["position"]
        corr_phases_order = [
            WavePhase.CORRECTIVE_A, WavePhase.CORRECTIVE_B, WavePhase.CORRECTIVE_C
        ]
        corrective_segs = []
        for k in range(3):
            mw = monowaves[corr_pos + k]
            corrective_segs.append(
                CycleBuilder._make_wave_segment(
                    mw, corr_phases_order[k], WaveType.CORRECTIVE
                )
            )

        # نسبت‌های فیبوناچی چرخه کامل
        imp_range  = abs(imp_pat["end_price"] - imp_pat["start_price"])
        corr_range = abs(corr_pat["end_price"] - corr_pat["start_price"])
        fib_rels   = {
            "corrective_to_impulse": round(corr_range / imp_range, 3) if imp_range > 0 else 0,
            **imp_pat.get("ratios", {}),
            **{f"corr_{k}": v for k, v in corr_pat.get("ratios", {}).items()},
        }

        # نقض‌های ترکیبی
        violations = imp_pat.get("errors", []) + corr_pat.get("errors", [])

        return CompleteCycle(
            start_idx=imp_pat["start_idx"],
            end_idx=corr_pat["end_idx"],
            start_price=float(imp_pat["start_price"]),
            end_price=float(corr_pat["end_price"]),
            direction=imp_pat["direction"],
            impulse_phase=impulse_segs,
            corrective_phase=corrective_segs,
            extension_type=imp_pat.get("ext_type", ExtensionType.NO_EXTENSION),
            corrective_type=corr_pat.get("c_type", CorrectiveType.UNKNOWN),
            completeness=CycleCompleteness.COMPLETE,
            fractal_level=fractal_level,
            fib_relationships=fib_rels,
            violations=violations
        )

    @staticmethod
    def find_all_cycles(
        monowaves: List[Monowave]
    ) -> List[CompleteCycle]:
        """
        جستجوی تمام چرخه‌های کامل ۸ موجی در داده.
        الگوریتم: ترکیب مستقیم ۵ موج + ۳ موج متوالی.
        """
        cycles = []
        n = len(monowaves)

        for i in range(n - 7):
            # فاز شتابدار: موج‌های i تا i+4
            imp_seg = monowaves[i: i + 5]
            is_imp, imp_err, imp_ratios, ext_type, truncated = \
                ImpulseValidator.validate(imp_seg)

            if len(imp_err) > 1:
                continue

            # فاز اصلاحی: موج‌های i+5 تا i+7
            corr_seg = monowaves[i + 5: i + 8]
            is_corr, corr_err, corr_ratios, c_type = \
                CorrectiveValidator.validate(corr_seg)

            if not is_corr:
                continue

            # جهت اصلاحی باید خلاف شتابدار باشد
            if imp_seg[0].direction == corr_seg[0].direction:
                continue

            # ساخت dict های pattern برای CycleBuilder.build_cycle
            w1, w2, w3, w4, w5 = imp_seg
            wA, wB, wC = corr_seg

            imp_pat = {
                "position"   : i,
                "start_idx"  : w1.start_idx,
                "end_idx"    : w5.end_idx,
                "start_price": float(w1.start_price),
                "end_price"  : float(w5.end_price),
                "direction"  : w1.direction,
                "errors"     : imp_err,
                "ratios"     : imp_ratios,
                "ext_type"   : ext_type,
                "is_truncated": truncated,
                "w1_range"   : float(w1.price_range),
                "w3_range"   : float(w3.price_range),
                "w5_range"   : float(w5.price_range),
            }
            corr_pat = {
                "position"   : i + 5,
                "start_idx"  : wA.start_idx,
                "end_idx"    : wC.end_idx,
                "start_price": float(wA.start_price),
                "end_price"  : float(wC.end_price),
                "direction"  : wA.direction,
                "errors"     : corr_err,
                "ratios"     : corr_ratios,
                "c_type"     : c_type,
            }

            cycle = CycleBuilder.build_cycle(imp_pat, corr_pat, monowaves, 0)
            if cycle:
                cycles.append(cycle)

        return cycles

    @staticmethod
    def build_fractal_levels(
        base_cycles: List[CompleteCycle],
        max_levels : int = 3
    ) -> List[CompleteCycle]:
        """
        ساخت سطوح فراکتالی بالاتر.
        هر چرخه کامل می‌تواند یک موج در چرخه بزرگ‌تر باشد.
        مطابق اصل فراکتال فصل ۲ و ۳ کتاب.
        """
        if not base_cycles or max_levels <= 0:
            return []

        # تبدیل چرخه‌ها به Monowave برای پردازش درجه بالاتر
        compressed = []
        for cyc in base_cycles:
            compressed.append(Monowave(
                start_idx=cyc.start_idx,
                end_idx=cyc.end_idx,
                start_price=cyc.start_price,
                end_price=cyc.end_price,
                direction=cyc.direction,
                price_range=abs(cyc.end_price - cyc.start_price),
                duration=cyc.end_idx - cyc.start_idx
            ))

        # جستجوی چرخه‌های درجه بالاتر
        higher = CycleBuilder.find_all_cycles(compressed)
        for c in higher:
            c.fractal_level = (base_cycles[0].fractal_level if base_cycles else 0) + 1

        result = list(higher)
        if higher and max_levels > 1:
            even_higher = CycleBuilder.build_fractal_levels(higher, max_levels - 1)
            result.extend(even_higher)

        return result


# ════════════════════════════════════════════════════════════════
# بخش ۶: تحلیل‌گر اثر فراکتال (FractalEffectAnalyzer)
# ════════════════════════════════════════════════════════════════

class FractalEffectAnalyzer:
    """
    تحلیل اثر فراکتال در چرخه‌های کامل.
    مطابق صفحه ۲۲ کتاب و فصل ۲.
    """

    # اعداد فیبوناچی صفحه ۲۲
    FIB_MOTIVE     = [1, 5, 21, 89]
    FIB_CORRECTIVE = [2, 8, 34, 144]

    @staticmethod
    def analyze(
        all_cycles: List[CompleteCycle],
        n_monowaves: int
    ) -> Dict:
        """
        بررسی خودتشابهی فراکتالی و نسبت‌های زمانی.
        """
        if not all_cycles:
            return {
                "self_similarity_detected": False,
                "fractal_levels"          : 0,
                "message"                 : "چرخه‌ای برای تحلیل فراکتال یافت نشد",
                "fib_motive_series"       : str(FractalEffectAnalyzer.FIB_MOTIVE),
                "fib_corrective_series"   : str(FractalEffectAnalyzer.FIB_CORRECTIVE),
            }

        # گروه‌بندی بر اساس سطح فراکتال
        by_level: Dict[int, List[CompleteCycle]] = {}
        for cyc in all_cycles:
            lv = cyc.fractal_level
            by_level.setdefault(lv, []).append(cyc)

        # بررسی نسبت اندازه بین سطوح
        level_ratios = []
        for lv in sorted(by_level.keys()):
            if lv + 1 in by_level:
                avg_low  = float(np.mean([
                    abs(c.end_price - c.start_price)
                    for c in by_level[lv]
                ]))
                avg_high = float(np.mean([
                    abs(c.end_price - c.start_price)
                    for c in by_level[lv + 1]
                ]))
                if avg_low > 0:
                    ratio = round(avg_high / avg_low, 3)
                    level_ratios.append({
                        "از_سطح": lv,
                        "به_سطح": lv + 1,
                        "نسبت"  : ratio,
                        "تأیید" : "بله" if 2 < ratio < 8 else "نیاز_به_بررسی"
                    })

        self_similar = (
            len(level_ratios) > 0 and
            all(r["نسبت"] > 2 for r in level_ratios)
        )

        # تطبیق تعداد موج‌ها با دنباله فیبوناچی
        fib_match_motive = [
            f for f in FractalEffectAnalyzer.FIB_MOTIVE
            if f <= n_monowaves
        ]
        fib_match_corr = [
            f for f in FractalEffectAnalyzer.FIB_CORRECTIVE
            if f <= n_monowaves
        ]

        return {
            "self_similarity_detected": self_similar,
            "fractal_levels"          : len(by_level),
            "level_ratios"            : level_ratios,
            "total_cycles"            : len(all_cycles),
            "fib_motive_match"        : fib_match_motive,
            "fib_corrective_match"    : fib_match_corr,
            "fib_motive_series"       : "1 → 5 → 21 → 89",
            "fib_corrective_series"   : "2 → 8 → 34 → 144",
            "message"                 : (
                f"{len(by_level)} سطح فراکتال شناسایی شد"
            ),
        }


# ════════════════════════════════════════════════════════════════
# بخش ۷: توابع کمکی
# ════════════════════════════════════════════════════════════════

def _nearest_fib(ratio: float) -> str:
    """نزدیک‌ترین نسبت فیبوناچی"""
    fibs = {
        "23.6%": 0.236, "38.2%": 0.382, "50.0%": 0.500,
        "61.8%": 0.618, "76.4%": 0.764, "100%":  1.000,
        "127.2%":1.272, "161.8%":1.618, "200%":  2.000,
        "261.8%":2.618,
    }
    best, best_d = "نامشخص", float("inf")
    for label, val in fibs.items():
        d = abs(ratio - val)
        if d < best_d:
            best_d, best = d, label
    return best if best_d < 0.08 else f"{ratio:.1%}"


def _assess_market_position(
    monowaves   : List[Monowave],
    cycles      : List[CompleteCycle],
    imp_patterns: List[Dict],
    corr_patterns: List[Dict],
) -> Dict:
    """ارزیابی موقعیت فعلی بازار در چرخه"""
    if not monowaves:
        return {"phase": "داده_کافی_نیست", "last_price": 0}

    last = monowaves[-1]
    last_dir = "صعودی" if last.direction == 1 else "نزولی"

    n = len(monowaves)
    in_motive     = any(p["position"] + 4 >= n - 1 for p in imp_patterns)
    in_corrective = any(p["position"] + 2 >= n - 1 for p in corr_patterns)

    if in_motive:
        phase = "در_فاز_شتابدار_(Impulse)"
    elif in_corrective:
        phase = "در_فاز_اصلاحی_(Corrective)"
    else:
        phase = "بین_موج‌ها"

    retrace_info = "نامشخص"
    if len(cycles) > 0:
        last_cycle = cycles[-1]
        r = last_cycle.fib_relationships.get("corrective_to_impulse", 0)
        retrace_info = f"{r:.1%} ({_nearest_fib(r)})"

    return {
        "phase"              : phase,
        "last_direction"     : last_dir,
        "last_price"         : round(float(last.end_price), 4),
        "cycles_count"       : len(cycles),
        "last_cycle_retrace" : retrace_info,
    }


# ════════════════════════════════════════════════════════════════
# بخش ۸: تابع analyze — interface کد هسته (main.py)
# ════════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None, context=None) -> Dict:
    """
    فصل ۳: ساختار دوره کامل امواج الیوت و اثر فراکتال در آن

    Interface مطابق کد هسته (main.py):
        data   : pd.DataFrame با ستون‌های open/high/low/close/volume
        logger : ResultsLogger | None
        return : dict — همه key ها str، همه value ها str یا عدد ساده
    """

    # ── استخراج ایمن داده‌ها ──────────────────────────────────
    def _col(df, *names):
        for n in names:
            if n in df.columns:
                return df[n].astype(float).values
        return np.zeros(len(df))

    close = _col(data, "close", "Close")
    high  = _col(data, "high",  "High")
    low   = _col(data, "low",   "Low")
    n     = len(close)

    # ── حداقل داده ────────────────────────────────────────────
    if n < 8:
        out = {
            "عنوان"     : "فصل ۳: ساختار دوره کامل امواج الیوت",
            "وضعیت"     : "داده_کافی_نیست",
            "تعداد_کندل": str(n),
            "پیام"       : "حداقل ۸ کندل لازم است",
        }
        if logger:
            logger.add_section("فصل ۳: ساختار دوره کامل امواج الیوت", level=1)
            logger.add_result("وضعیت", "داده کافی نیست")
        return out

    # ── مرحله ۱: استخراج تک‌موج‌ها ───────────────────────────
    monowaves = []
    context_used = False
    
    if context and "chapter_2" in context:
        ch2 = context["chapter_2"]
        if "_monowaves" in ch2 and ch2["_monowaves"]:
            monowaves = ch2["_monowaves"]
            context_used = True
    
    # اگر از context دریافت نشد، خودمان استخراج می‌کنیم
    if not monowaves:
        monowaves = _extract_monowaves(high, low, order=3)

    if len(monowaves) < 8:
        out = {
            "عنوان"           : "فصل ۳: ساختار دوره کامل امواج الیوت",
            "وضعیت"           : "موج_کافی_نیست",
            "تعداد_کندل"      : str(n),
            "تعداد_تک‌موج"    : str(len(monowaves)),
            "پیام"            : "برای تشخیص چرخه کامل حداقل ۸ مونوویو لازم است",
        }
        if logger:
            logger.add_section("فصل ۳: ساختار دوره کامل امواج الیوت", level=1)
            logger.add_result("وضعیت", "مونوویو کافی نیست")
        return out

    # ── مرحله ۲: تشخیص الگوهای شتابدار و اصلاحی ──────────────
    imp_patterns  = ImpulseValidator.find_all(monowaves)
    corr_patterns = CorrectiveValidator.find_all(monowaves)

    # ── مرحله ۳: ساخت چرخه‌های کامل ──────────────────────────
    base_cycles    = CycleBuilder.find_all_cycles(monowaves)
    fractal_cycles = CycleBuilder.build_fractal_levels(base_cycles, max_levels=3)
    all_cycles     = base_cycles + fractal_cycles
    valid_cycles   = [c for c in base_cycles if len(c.violations) == 0]

    # ── مرحله ۴: تحلیل فراکتال ───────────────────────────────
    fractal_info = FractalEffectAnalyzer.analyze(all_cycles, len(monowaves))

    # ── مرحله ۵: ارزیابی وضعیت بازار ──────────────────────────
    market_pos = _assess_market_position(
        monowaves, base_cycles, imp_patterns, corr_patterns
    )

    # ── مرحله ۶: آمار نقض قوانین ─────────────────────────────
    q1 = q2 = q3 = 0
    for p in imp_patterns:
        for e in p.get("errors", []):
            if "قانون ۱" in e: q1 += 1
            elif "قانون ۲" in e: q2 += 1
            elif "قانون ۳" in e: q3 += 1

    # ── مرحله ۷: شمارش انواع Extension و اصلاح ───────────────
    ext_counts  : Dict[str, int] = {}
    corr_counts : Dict[str, int] = {}
    for p in imp_patterns:
        k = p.get("ext_type", ExtensionType.NO_EXTENSION).value
        ext_counts[k] = ext_counts.get(k, 0) + 1
    for p in corr_patterns:
        k = p.get("c_type", CorrectiveType.UNKNOWN).value
        corr_counts[k] = corr_counts.get(k, 0) + 1

    # ── مرحله ۸: ساخت dict خروجی (همه value ها str) ──────────
    results: Dict = {
        # شناسنامه
        "عنوان"                     : "فصل ۳: ساختار دوره کامل امواج الیوت و اثر فراکتال در آن",
        "مرجع_کتاب"                 : "صفحه ۲۲ - گلن نیلی",
        "وضعیت"                     : "تحلیل_کامل",

        # آمار پایه
        "تعداد_کندل"                : str(n),
        "تعداد_تک‌موج"              : str(len(monowaves)),
        "قیمت_فعلی"                 : str(round(float(close[-1]), 4)),
        "بالاترین_قیمت"             : str(round(float(np.max(high)), 4)),
        "پایین‌ترین_قیمت"           : str(round(float(np.min(low)), 4)),

        # نتایج اصلی فصل ۳
        "تعداد_الگوی_شتابدار_5موجی" : str(len(imp_patterns)),
        "تعداد_الگوی_اصلاحی_3موجی"  : str(len(corr_patterns)),
        "تعداد_چرخه_کامل_8موجی"     : str(len(base_cycles)),
        "تعداد_چرخه_کامل_معتبر"     : str(len(valid_cycles)),
        "تعداد_سطح_فراکتال"         : str(fractal_info["fractal_levels"]),
        "خودتشابهی_فراکتالی"        : "تأیید_شد" if fractal_info["self_similarity_detected"] else "نیاز_به_داده_بیشتر",

        # قوانین نقض‌ناپذیر
        "قانون_1"                   : "موج ۲ هرگز از شروع موج ۱ عبور نمی‌کند",
        "قانون_2"                   : "موج ۳ هرگز کوتاه‌ترین موج شتابدار نیست",
        "قانون_3"                   : "موج ۴ هرگز با قلمرو قیمتی موج ۱ همپوشانی ندارد",
        "قانون_4"                   : "موج ۱، ۳، ۵ خود شتابدار هستند (5 ریزموج)",
        "قانون_5"                   : "موج ۲، ۴، A، B، C خود اصلاحی هستند (3 ریزموج)",
        "قانون_6"                   : "ساختار در تمام درجات فراکتالی تکرار می‌شود",
        "نقض_قانون_1"               : str(q1),
        "نقض_قانون_2"               : str(q2),
        "نقض_قانون_3"               : str(q3),

        # اعداد فیبوناچی صفحه ۲۲
        "فیبو_شتابدار"              : "1 → 5 → 21 → 89",
        "فیبو_اصلاحی"               : "2 → 8 → 34 → 144",
        "فیبو_چرخه_کامل"            : "144 واحد = 1 Grand Supercycle",

        # انواع Extension (فصل ۱۱)
        "ext_موج_3_ممتد"            : str(ext_counts.get("موج_۳_ممتد", 0)),
        "ext_موج_5_ممتد"            : str(ext_counts.get("موج_۵_ممتد", 0)),
        "ext_موج_1_ممتد"            : str(ext_counts.get("موج_۱_ممتد", 0)),
        "ext_موج_5_کوتاه"           : str(ext_counts.get("موج_۵_کوتاه_شده", 0)),
        "ext_امتداد_دوگانه"         : str(ext_counts.get("امتداد_دوگانه", 0)),
        "ext_بدون_امتداد"           : str(ext_counts.get("بدون_امتداد", 0)),

        # انواع اصلاح (فصل ۱۲)
        "corr_ZigZag"               : str(corr_counts.get("ZigZag", 0)),
        "corr_Flat_Common"          : str(corr_counts.get("Flat_Common", 0)),
        "corr_Irregular_Flat"       : str(corr_counts.get("Irregular_Flat", 0)),
        "corr_Running"              : str(corr_counts.get("Running", 0)),

        # وضعیت فعلی
        "فاز_احتمالی_فعلی"          : market_pos["phase"],
        "آخرین_جهت"                 : market_pos["last_direction"],
        "آخرین_قیمت_موج"           : str(market_pos["last_price"]),
        "اصلاح_آخرین_چرخه"         : market_pos["last_cycle_retrace"],
    }

    # ── جزئیات چرخه‌های معتبر (حداکثر ۵ تا) ─────────────────
    for idx, cyc in enumerate(valid_cycles[:5]):
        pfx = f"چرخه_{idx+1}"
        imp_range  = abs(cyc.impulse_phase[-1].end_price - cyc.impulse_phase[0].start_price)
        corr_range = abs(cyc.corrective_phase[-1].end_price - cyc.corrective_phase[0].start_price)
        retrace    = round(corr_range / imp_range, 3) if imp_range > 0 else 0

        results[f"{pfx}_جهت"]          = "صعودی" if cyc.direction == 1 else "نزولی"
        results[f"{pfx}_شروع"]         = str(round(cyc.start_price, 4))
        results[f"{pfx}_پایان_شتابدار"] = str(round(cyc.impulse_phase[-1].end_price, 4))
        results[f"{pfx}_پایان_اصلاحی"]  = str(round(cyc.end_price, 4))
        results[f"{pfx}_نسبت_اصلاح"]   = str(retrace)
        results[f"{pfx}_فیبو_اصلاح"]   = _nearest_fib(retrace)
        results[f"{pfx}_نوع_اصلاح"]    = cyc.corrective_type.value
        results[f"{pfx}_نوع_امتداد"]   = cyc.extension_type.value
        results[f"{pfx}_W3_W1"]        = str(cyc.fib_relationships.get("W3/W1", 0))
        results[f"{pfx}_W5_W1"]        = str(cyc.fib_relationships.get("W5/W1", 0))
        results[f"{pfx}_نقض"]          = str(len(cyc.violations))

    # ── جزئیات الگوهای شتابدار (حداکثر ۳ تا) ─────────────────
    for idx, ph in enumerate(imp_patterns[:3]):
        pfx = f"شتابدار_{idx+1}"
        results[f"{pfx}_جهت"]          = ph["dir_str"]
        results[f"{pfx}_امتداد"]       = ph["ext_type"].value
        results[f"{pfx}_W3_W1"]        = str(ph["ratios"].get("W3/W1", 0))
        results[f"{pfx}_اصلاح_W2"]     = _nearest_fib(ph["ratios"].get("W2/W1", 0))
        results[f"{pfx}_اصلاح_W4"]     = _nearest_fib(ph["ratios"].get("W4/W3", 0))
        results[f"{pfx}_کوتاه_شده"]    = "بله" if ph.get("is_truncated") else "خیر"

    # ── تفسیر نهایی ───────────────────────────────────────────
    results["تفسیر_نهایی"] = _build_interpretation(
        n, len(monowaves),
        len(imp_patterns), len(corr_patterns),
        len(base_cycles), len(valid_cycles),
        fractal_info, market_pos,
        q1, q2, q3,
        valid_cycles[:3],
        ext_counts, corr_counts,
    )


    # ── اضافه کردن منبع داده به نتایج ────────────────────────
    results["_source"] = "از_فصل_2" if context_used else "مستقل"
    results["_monowaves_used"] = len(monowaves)

    # ── ثبت در لاگ ────────────────────────────────────────────
    if logger:
        _write_log(logger, results, valid_cycles, imp_patterns, corr_patterns)

    return results


# ════════════════════════════════════════════════════════════════
# بخش ۹: تفسیر متنی
# ════════════════════════════════════════════════════════════════

def _build_interpretation(
    n, n_waves, n_imp, n_corr,
    n_base_cycles, n_valid_cycles,
    fractal_info, market_pos,
    q1, q2, q3,
    top_cycles,
    ext_counts, corr_counts,
) -> str:

    viol = (
        "✓ هیچ نقضی یافت نشد"
        if (q1 + q2 + q3) == 0
        else f"⚠ مجموع: {q1+q2+q3} (Q1={q1}, Q2={q2}, Q3={q3})"
    )

    cycles_detail = ""
    for i, c in enumerate(top_cycles):
        imp_range  = abs(c.impulse_phase[-1].end_price - c.impulse_phase[0].start_price)
        corr_range = abs(c.corrective_phase[-1].end_price - c.corrective_phase[0].start_price)
        ret = corr_range / imp_range if imp_range > 0 else 0
        cycles_detail += (
            f"\n    چرخه {i+1}: {'صعودی' if c.direction==1 else 'نزولی'} | "
            f"اصلاح={ret:.1%} ({_nearest_fib(ret)}) | "
            f"نوع={c.corrective_type.value} | "
            f"Extension={c.extension_type.value}"
        )

    ext_summary = ", ".join(
        f"{k}:{v}" for k, v in ext_counts.items() if v > 0
    ) or "یافت نشد"

    corr_summary = ", ".join(
        f"{k}:{v}" for k, v in corr_counts.items() if v > 0
    ) or "یافت نشد"

    return f"""
═══════════════════════════════════════════════════════════════════
  فصل ۳: ساختار دوره کامل امواج الیوت و اثر فراکتال در آن
  مرجع: صفحه ۲۲ کتاب گلن نیلی
═══════════════════════════════════════════════════════════════════

📊 آمار کلی:
    کندل: {n}  |  تک‌موج: {n_waves}
    الگوی شتابدار ۵موجی: {n_imp}  |  الگوی اصلاحی ۳موجی: {n_corr}
    چرخه کامل ۸موجی: {n_base_cycles}  (معتبر: {n_valid_cycles})
    سطح فراکتال: {fractal_info["fractal_levels"]}

📐 قوانین نقض‌ناپذیر:  {viol}
    ✓ قانون ۱: موج ۲ هرگز از شروع موج ۱ عبور نمی‌کند
    ✓ قانون ۲: موج ۳ هرگز کوتاه‌ترین موج شتابدار نیست
    ✓ قانون ۳: موج ۴ هرگز با قلمرو قیمتی موج ۱ همپوشانی ندارد
    ✓ قانون ۴: موج ۱، ۳، ۵ خود شتابدار (5 ریزموج)
    ✓ قانون ۵: موج ۲، ۴، A، B، C خود اصلاحی (3 ریزموج)
    ✓ قانون ۶: ساختار در تمام درجات فراکتالی تکرار می‌شود

🔢 اعداد فیبوناچی صفحه ۲۲:
    فاز Motive   : 1 → 5 → 21 → 89
    فاز Corrective: 2 → 8 → 34 → 144
    چرخه کامل    : 144 واحد = Grand Supercycle

⚡ انواع Extension شناسایی‌شده (فصل ۱۱):  {ext_summary}
🔄 انواع اصلاح شناسایی‌شده (فصل ۱۲):  {corr_summary}

🔄 چرخه‌های معتبر:{cycles_detail if cycles_detail else chr(10) + '    چرخه معتبر شناسایی نشد'}

📍 وضعیت فعلی:
    جهت آخرین موج: {market_pos["last_direction"]}
    فاز احتمالی  : {market_pos["phase"]}
    آخرین قیمت  : {market_pos["last_price"]}
    اصلاح آخرین چرخه: {market_pos["last_cycle_retrace"]}

🔬 اثر فراکتال:
    {fractal_info["message"]}
    خودتشابهی: {"تأیید شد" if fractal_info["self_similarity_detected"] else "نیاز به داده بیشتر"}
═══════════════════════════════════════════════════════════════════"""


# ════════════════════════════════════════════════════════════════
# بخش ۱۰: ثبت در لاگ
# ════════════════════════════════════════════════════════════════

def _write_log(logger, results, valid_cycles, imp_patterns, corr_patterns):
    logger.add_section(
        "فصل ۳: ساختار دوره کامل امواج الیوت و اثر فراکتال", level=1
    )
    logger.add_result("مرجع کتاب", "صفحه ۲۲ - گلن نیلی")
    logger.add_result("تعداد کندل",               results["تعداد_کندل"])
    logger.add_result("تعداد تک‌موج",              results["تعداد_تک‌موج"])
    logger.add_result("الگوی شتابدار ۵موجی",       results["تعداد_الگوی_شتابدار_5موجی"])
    logger.add_result("الگوی اصلاحی ۳موجی",        results["تعداد_الگوی_اصلاحی_3موجی"])
    logger.add_result("چرخه کامل ۸موجی",          results["تعداد_چرخه_کامل_8موجی"])
    logger.add_result("چرخه کامل معتبر",          results["تعداد_چرخه_کامل_معتبر"])

    logger.add_section("قوانین نقض‌ناپذیر", level=2)
    for i in range(1, 7):
        logger.add_result(f"قانون {i}", results.get(f"قانون_{i}", ""))
    logger.add_result("نقض قانون ۱", results["نقض_قانون_1"])
    logger.add_result("نقض قانون ۲", results["نقض_قانون_2"])
    logger.add_result("نقض قانون ۳", results["نقض_قانون_3"])

    logger.add_section("اعداد فیبوناچی صفحه ۲۲", level=2)
    logger.add_result("فاز شتابدار",  results["فیبو_شتابدار"])
    logger.add_result("فاز اصلاحی",   results["فیبو_اصلاحی"])
    logger.add_result("چرخه کامل",    results["فیبو_چرخه_کامل"])

    logger.add_section("انواع Extension (فصل ۱۱)", level=2)
    for k in ["ext_موج_3_ممتد", "ext_موج_5_ممتد", "ext_موج_1_ممتد",
              "ext_موج_5_کوتاه", "ext_امتداد_دوگانه"]:
        logger.add_result(k, results.get(k, "0"))

    logger.add_section("انواع اصلاح (فصل ۱۲)", level=2)
    for k in ["corr_ZigZag", "corr_Flat_Common", "corr_Irregular_Flat", "corr_Running"]:
        logger.add_result(k, results.get(k, "0"))

    logger.add_section("چرخه‌های معتبر", level=2)
    for idx, cyc in enumerate(valid_cycles[:5]):
        logger.add_wave(f"چرخه {idx+1}", {
            "جهت"        : "صعودی" if cyc.direction == 1 else "نزولی",
            "Extension"  : cyc.extension_type.value,
            "نوع اصلاح" : cyc.corrective_type.value,
            "W3/W1"      : cyc.fib_relationships.get("W3/W1", "N/A"),
        })

    logger.add_section("وضعیت فعلی", level=2)
    logger.add_result("فاز احتمالی", results["فاز_احتمالی_فعلی"])
    logger.add_result("آخرین جهت",   results["آخرین_جهت"])
    logger.add_result("آخرین قیمت",  results["آخرین_قیمت_موج"])
    logger.add_result("تفسیر",       results["تفسیر_نهایی"])