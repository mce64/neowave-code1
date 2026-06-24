# chapters/chapter_06.py

"""
فصل ۶: قانون تناسب (Proportion)
منبع: کتاب "امواج الیوت به سبک نئوویو" - گلن نیلی - صفحات ۳۳ تا ۴۲

═══════════════════════════════════════════════════════════════════
متن دقیق کتاب (صفحه ۳۳):

"زمانی که شما یک تایم فریم را برای موج شماری انتخاب میکنید، در حقیقت
شما انتخاب میکنید که کدام الگوهای الیوی آشکار شوند چرا که هر الگوی الیوی
در هر بازاری بر اساس مقیاس قیمتی و زمان منحصر به خود توسعه میآید.
بنابراین محدوده انتخابی شما بایستی دارای تناسب در بعد قیمت و زمان باشد.

در حقیقت قانون تناسب بیان میدارد که نسبت حرکت بازار در بعد قیمت و زمان
بایستی متناسب باشد.

قوانین مربوط به سبک نئو ویو در صورتی کاربرد دارد که قانون تناسب رعایت شده باشد."

═══════════════════════════════════════════════════════════════════
قوانین اصلی فصل ۶ (صفحات ۳۳ تا ۴۲):

۱. حرکت جهت‌دار (Directional) - صفحات ۳۷-۴۰:
   - داده‌ها باید درون یک مربع، حول خطی با زاویه ۴۵ درجه نوسان کنند
   - انحراف از این زاویه تا ۲۵ درصد در هر بعد (قیمت و زمان) مجاز است
   - اولین موج از یک تسلسل حرکت جهت‌دار: بیش از ۶۱.۸٪ اصلاح نمی‌شود
   - آخرین موج از یک تسلسل حرکت جهت‌دار: بیش از ۱۰۰٪ اصلاح می‌شود
   - هیچ صعودی بیش از ۱۰۰٪ بازگشت نشده است (عکس ۱.jpg)
   - بازگشت کامل تک موج قبلی = حرکت جهت‌دار تکمیل شده است (عکس ۳.jpg)
   - خط مرکزی نوسان در گذر زمان (عکس ۲.jpg و ۳.jpg)

۲. حرکت غیرجهت‌دار (Non-Directional) - صفحات ۴۱-۴۲:
   - داده‌ها باید تقریباً نیمی از مربع را پوشش دهند (۵۰٪)
   - بعد بزرگتر = بعد زمان (نه قیمت)
   - اولین موج: بیش از ۶۱.۸٪ اصلاح می‌شود
   - آخرین موج: بیش از ۱۶۱.۸٪ اصلاح می‌شود
   - خط مرکزی نوسان در گذر زمان

۳. مربع تناسب:
   - برای حرکت جهت‌دار: از شروع تا خاتمه حرکت را پیدا کرده
     متناسب با بعد بزرگتر (معمولاً بعد قیمت) مربع را ترسیم کنید
   - برای حرکت غیرجهت‌دار: متناسب با بعد بزرگتر (معمولاً بعد زمان)
     مربع را ترسیم کنید

۴. مقیاس لگاریتمی (صفحه ۴۹):
   - اگر قیمت بالا بیش از دو برابر قیمت پایین باشد، نمودار لگاریتمی مناسب است
   - هر چه اختلاف درصد بین سطح قیمت بالا و پایین بیشتر باشد،
     اهمیت استفاده از مقیاس لگاریتمی بیشتر است
═══════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
import math
from scipy.signal import argrelextrema
from scipy import stats
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


# ════════════════════════════════════════════════════════════════
# بخش ۱: تعاریف پایه
# ════════════════════════════════════════════════════════════════

class MovementType(Enum):
    """نوع حرکت: جهت‌دار (روند) یا غیرجهت‌دار (رنج)"""
    DIRECTIONAL = "جهت‌دار"
    NON_DIRECTIONAL = "غیرجهت‌دار"
    UNKNOWN = "نامشخص"


class RetracementType(Enum):
    """نوع اصلاح بر اساس نسبت فیبوناچی"""
    NONE = "بدون_اصلاح"
    SHALLOW = "کم_(کمتر_از_38.2%)"
    MODERATE = "متوسط_(38.2%_تا_61.8%)"
    DEEP = "عمیق_(61.8%_تا_100%)"
    FULL = "کامل_(100%_تا_161.8%)"
    EXTREME = "شدید_(بیشتر_از_161.8%)"


@dataclass
class WaveSegment:
    """
    یک قطعه موج برای تحلیل تناسب
    
    مطابق صفحه ۳۲: هر تغییری در جهت قیمت با یک نقطه مشخص شده است.
    نقاط ابتدا و انتهای هر تک موج را مشخص می‌کنند.
    """
    index: int
    start_idx: int
    end_idx: int
    start_price: float
    end_price: float
    direction: int          # +1 صعودی، -1 نزولی
    price_range: float      # دامنه قیمتی (مطلق)
    duration: int           # تعداد کندل‌های طی شده
    start_type: str         # "PEAK" یا "TROUGH"
    end_type: str           # "PEAK" یا "TROUGH"
    retrace_ratio: float = 0.0      # نسبت اصلاح نسبت به موج قبلی
    retrace_type: RetracementType = RetracementType.NONE
    is_complete: bool = True        # آیا موج کامل شده است


@dataclass
class WaveStructure:
    """ساختار کامل موج‌ها برای تحلیل تناسب"""
    waves: List[WaveSegment]
    total_duration: int
    total_price_range: float
    start_idx: int
    end_idx: int
    start_price: float
    end_price: float
    direction: int
    is_bullish: bool
    movement_type: MovementType = MovementType.UNKNOWN
    confidence: float = 0.0


@dataclass
class ProportionSquare:
    """
    مربع تناسب (صفحات ۳۷-۴۲)
    
    برای حرکت جهت‌دار:
        - مربع حول خط ۴۵ درجه
        - انحراف مجاز: ۲۵٪ در هر بعد (قیمت و زمان)
        - نقطه خاتمه باید نزدیک گوشه مقابل باشد
    
    برای حرکت غیرجهت‌دار:
        - داده‌ها باید تقریباً نیمی از مربع را پوشش دهند
        - بعد بزرگتر = بعد زمان
    """
    width: float                    # عرض مربع (بعد قیمت در مقیاس مناسب)
    height: float                   # ارتفاع مربع (بعد زمان)
    start_price: float              # قیمت شروع (گوشه اول)
    end_price: float                # قیمت هدف (گوشه مقابل)
    start_time: float               # زمان شروع (گوشه اول)
    end_time: float                 # زمان هدف (گوشه مقابل)
    diagonal_slope: float           # شیب خط ۴۵ درجه واقعی (قیمت/زمان در مقیاس مناسب)
    ideal_slope: float              # شیب ایده‌آل (۱.۰)
    deviation_percent: float        # انحراف از ۴۵ درجه (درصد)
    is_valid_slope: bool            # آیا انحراف کمتر از ۲۵٪ است؟
    price_distance_to_target: float # فاصله قیمتی تا هدف
    time_distance_to_target: float  # فاصله زمانی تا هدف
    price_reached_target: bool      # آیا قیمت به گوشه مقابل رسیده؟
    time_reached_target: bool       # آیا زمان به گوشه مقابل رسیده؟
    corner_reached: bool            # آیا نقطه خاتمه به گوشه مقابل رسیده؟
    coverage_50_percent: float      # درصد پوشش مربع (برای حرکت غیرجهت‌دار)
    coverage_50_valid: bool         # برای حرکت غیرجهت‌دار: پوشش ۵۰٪ مربع
    use_log_scale: bool             # آیا از مقیاس لگاریتمی استفاده شده؟
    log_scale_factor: float         # ضریب مقیاس لگاریتمی (۰ تا ۱)
    opposite_corner: str            # توصیف گوشه مقابل
    longer_dimension: str           # بعد بزرگتر ("price" یا "time")
    completion_status: str          # وضعیت خاتمه (مناسب/دیرهنگام/زودهنگام/نامناسب)


@dataclass
class CentralOscillationLine:
    """خط مرکزی نوسان (صفحه ۳۳)"""
    slope: float                    # شیب خط مرکزی
    intercept: float                # عرض از مبدا
    center_line_values: List[float] # مقادیر خط مرکزی در هر نقطه
    deviations: List[float]         # انحراف هر نقطه از خط مرکزی (درصد)
    avg_deviation: float            # میانگین انحراف
    max_deviation: float            # حداکثر انحراف
    min_deviation: float            # حداقل انحراف
    is_within_tolerance: bool       # آیا حداکثر انحراف ≤ ۲۵٪؟
    is_symmetric: bool              # آیا نوسان متقارن است؟
    points_above: int               # تعداد نقاط بالای خط
    points_below: int               # تعداد نقاط پایین خط
    r_squared: float                # ضریب تعیین رگرسیون
    valid: bool                     # آیا خط مرکزی معتبر است؟
    reason: str                     # دلیل عدم اعتبار


# ════════════════════════════════════════════════════════════════
# بخش ۲: استخراج موج‌ها از داده (مطابق فصل ۵)
# ════════════════════════════════════════════════════════════════

def extract_wave_segments(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    order: int = 2
) -> List[WaveSegment]:
    """
    استخراج موج‌ها (تک موج‌ها) از داده قیمتی.
    
    مطابق صفحه ۳۲:
        "پس از رسم نمودار با استفاده از کش دیتا و با استفاده از
        بررسی نقطه-داده‌ها و تغییر جهت نقطه-داده‌ها می‌توان تک‌موج‌ها
        را به صورت عمومی شناسایی کرد."
    
    هر تغییر جهت = یک موج جدید.
    
    پارامترها:
        high: آرایه بالاترین قیمت‌ها
        low: آرایه پایین‌ترین قیمت‌ها
        close: آرایه قیمت بسته شدن (برای بازگشتی‌ها)
        order: حساسیت تشخیص نقاط چرخش (عدد بیشتر = نویز کمتر)
    
    خروجی:
        لیست WaveSegment
    """
    n = len(close)
    
    # ── شناسایی قله‌ها (Peaks) ─────────────────────────────────
    peak_indices = argrelextrema(high, np.greater, order=order)[0]
    
    # ── شناسایی دره‌ها (Troughs) ──────────────────────────────
    trough_indices = argrelextrema(low, np.less, order=order)[0]
    
    # ── ترکیب نقاط ────────────────────────────────────────────
    points = []
    for idx in peak_indices:
        points.append((int(idx), float(high[idx]), "PEAK"))
    for idx in trough_indices:
        points.append((int(idx), float(low[idx]), "TROUGH"))
    
    if len(points) < 2:
        return []
    
    # ── مرتب‌سازی بر اساس زمان ────────────────────────────────
    points.sort(key=lambda x: x[0])
    
    # ── حذف نقاط هم‌نوع متوالی ────────────────────────────────
    # (مثلاً دو قله پشت سر هم بدون دره بین‌شان)
    filtered = []
    for pt in points:
        if not filtered:
            filtered.append(pt)
            continue
        last = filtered[-1]
        if last[2] == pt[2]:
            # هم‌نوع هستند: فقط نقطه برتر را نگه دار
            if pt[2] == "PEAK" and pt[1] > last[1]:
                filtered[-1] = pt
            elif pt[2] == "TROUGH" and pt[1] < last[1]:
                filtered[-1] = pt
        else:
            filtered.append(pt)
    
    if len(filtered) < 2:
        return []
    
    # ── ساخت موج‌ها ───────────────────────────────────────────
    waves = []
    for i, (idx1, price1, type1) in enumerate(filtered[:-1]):
        idx2, price2, type2 = filtered[i + 1]
        
        wave = WaveSegment(
            index=i,
            start_idx=int(idx1),
            end_idx=int(idx2),
            start_price=float(price1),
            end_price=float(price2),
            direction=1 if price2 > price1 else -1,
            price_range=abs(price2 - price1),
            duration=max(1, int(idx2 - idx1)),
            start_type=type1,
            end_type=type2,
        )
        waves.append(wave)
    
    # ── محاسبه نسبت اصلاح برای هر موج (نسبت به موج قبلی) ──────
    for i in range(1, len(waves)):
        prev = waves[i-1]
        curr = waves[i]
        if prev.price_range > 0 and curr.direction != prev.direction:
            retrace = curr.price_range / prev.price_range
            curr.retrace_ratio = retrace
            
            # تعیین نوع اصلاح بر اساس نسبت فیبوناچی
            if retrace < 0.382:
                curr.retrace_type = RetracementType.SHALLOW
            elif retrace < 0.618:
                curr.retrace_type = RetracementType.MODERATE
            elif retrace < 1.0:
                curr.retrace_type = RetracementType.DEEP
            elif retrace < 1.618:
                curr.retrace_type = RetracementType.FULL
            else:
                curr.retrace_type = RetracementType.EXTREME
    
    return waves


# ════════════════════════════════════════════════════════════════
# بخش ۳: تشخیص نوع حرکت (جهت‌دار / غیرجهت‌دار) – نسخه کامل
# ════════════════════════════════════════════════════════════════

def get_retracement_type(ratio: float) -> RetracementType:
    """تعیین نوع اصلاح بر اساس نسبت فیبوناچی"""
    if ratio < 0.382:
        return RetracementType.SHALLOW
    elif ratio < 0.618:
        return RetracementType.MODERATE
    elif ratio < 1.0:
        return RetracementType.DEEP
    elif ratio < 1.618:
        return RetracementType.FULL
    else:
        return RetracementType.EXTREME


def detect_movement_type_advanced(waves: List[WaveSegment]) -> Tuple[MovementType, Dict]:
    """
    تشخیص پیشرفته نوع حرکت مطابق صفحات ۳۳-۳۴ کتاب.
    
    این تابع از بررسی کامل حداقل ۵ موج متوالی استفاده می‌کند
    و قوانین زیر را اعمال می‌نماید:
    
    1. در حرکت جهت‌دار: موج‌های شتابدار (۱، ۳، ۵) اصلاح کم (< ۶۱.۸٪) دارند
    2. در حرکت غیرجهت‌دار: موج‌های شتابدار (۱، ۳، ۵) اصلاح عمیق (> ۶۱.۸٪) دارند
    3. آخرین موج در حرکت جهت‌دار: اصلاح کامل (> ۱۰۰٪)
    4. آخرین موج در حرکت غیرجهت‌دار: اصلاح شدید (> ۱۶۱.۸٪)
    5. قانون "هیچ صعودی بیش از ۱۰۰٪ بازگشت نشده است"
    
    پارامترها:
        waves: لیست WaveSegment
    
    خروجی:
        (نوع_حرکت, جزئیات_تشخیص)
    """
    if len(waves) < 5:
        return MovementType.UNKNOWN, {
            "reason": f"موج کافی نیست (حداقل ۵ موج نیاز است، {len(waves)} موج موجود)",
            "confidence": 0.0
        }
    
    # ── جمع‌آوری آمار موج‌های شتابدار (۱، ۳، ۵) ──────────────
    # موج شتابدار = موجی که جهت آن با جهت کلی حرکت هماهنگ است
    # جهت کلی حرکت = جهت موج اول
    main_direction = waves[0].direction
    
    motive_indices = [i for i, w in enumerate(waves) if w.direction == main_direction]
    corrective_indices = [i for i, w in enumerate(waves) if w.direction != main_direction]
    
    # ── محاسبه اصلاح موج‌های اول، سوم و آخر ───────────────────
    details = {
        "total_waves": len(waves),
        "main_direction": "صعودی" if main_direction == 1 else "نزولی",
        "motive_waves_count": len(motive_indices),
        "corrective_waves_count": len(corrective_indices),
        "wave_1_retrace": None,
        "wave_3_retrace": None,
        "wave_5_retrace": None,
        "last_retrace": None,
        "all_motive_retraces": [],
        "all_corrective_retraces": [],
        "max_retrace": 0.0,
        "has_over_100": False,
        "has_over_161_8": False,
        "all_under_100": True,
        "first_corrective_retrace": None,
        "second_corrective_retrace": None,
    }
    
    # موج اول (شتابدار) و اصلاح آن (موج دوم)
    if len(waves) >= 2 and waves[1].direction != main_direction:
        retrace_1 = waves[1].retrace_ratio
        details["wave_1_retrace"] = retrace_1
        details["all_motive_retraces"].append(retrace_1)
        details["first_corrective_retrace"] = retrace_1
        
        if retrace_1 > 1.0:
            details["has_over_100"] = True
            details["all_under_100"] = False
        if retrace_1 > 1.618:
            details["has_over_161_8"] = True
    
    # موج سوم (شتابدار) و اصلاح آن (موج چهارم)
    if len(waves) >= 4 and waves[3].direction != main_direction:
        retrace_3 = waves[3].retrace_ratio
        details["wave_3_retrace"] = retrace_3
        details["all_motive_retraces"].append(retrace_3)
        details["second_corrective_retrace"] = retrace_3
        
        if retrace_3 > 1.0:
            details["has_over_100"] = True
            details["all_under_100"] = False
        if retrace_3 > 1.618:
            details["has_over_161_8"] = True
    
    # موج پنجم (شتابدار) و اصلاح آن (موج ششم)
    if len(waves) >= 6 and waves[5].direction != main_direction:
        retrace_5 = waves[5].retrace_ratio
        details["wave_5_retrace"] = retrace_5
        details["all_motive_retraces"].append(retrace_5)
        
        if retrace_5 > 1.0:
            details["has_over_100"] = True
            details["all_under_100"] = False
        if retrace_5 > 1.618:
            details["has_over_161_8"] = True
    
    # آخرین موج اصلاحی
    if len(waves) >= 2 and waves[-1].direction != main_direction:
        details["last_retrace"] = waves[-1].retrace_ratio
        if waves[-1].retrace_ratio > 1.0:
            details["has_over_100"] = True
            details["all_under_100"] = False
        if waves[-1].retrace_ratio > 1.618:
            details["has_over_161_8"] = True
    
    # ── محاسبه حداکثر اصلاح ───────────────────────────────────
    for w in waves:
        if w.retrace_ratio > details["max_retrace"]:
            details["max_retrace"] = w.retrace_ratio
    
    # ── محاسبه میانگین اصلاح موج‌های شتابدار ──────────────────
    if details["all_motive_retraces"]:
        details["avg_motive_retrace"] = np.mean(details["all_motive_retraces"])
    else:
        details["avg_motive_retrace"] = 0
    
    # ── تشخیص بر اساس قوانین صفحه ۳۳ ─────────────────────────
    first = details["wave_1_retrace"]
    third = details["wave_3_retrace"]
    last = details["last_retrace"]
    avg_motive = details["avg_motive_retrace"]
    
    # محاسبه امتیاز اطمینان
    confidence = 0.0
    
    # تشخیص حرکت جهت‌دار
    # شرط ۱: موج اول و سوم هر دو کمتر از ۶۱.۸٪ اصلاح شده باشند
    if first is not None and third is not None:
        if first < 0.618 and third < 0.618:
            confidence += 0.4
            # شرط ۲: آخرین موج بیشتر از ۱۰۰٪ اصلاح شده باشد (تأیید پایان)
            if last is not None and last > 1.0:
                confidence += 0.3
                details["conclusion"] = "حرکت جهت‌دار - با تأیید بازگشت کامل آخرین موج"
                details["subtype"] = "جهت‌دار_تکمیل‌شده"
            # شرط ۳: هیچ بازگشتی بیش از ۱۰۰٪ نشده باشد (حرکت سالم)
            elif details["all_under_100"]:
                confidence += 0.2
                details["conclusion"] = "حرکت جهت‌دار - هیچ بازگشتی بیش از ۱۰۰٪ نشده است"
                details["subtype"] = "جهت‌دار_سالم"
            else:
                details["conclusion"] = "احتمالاً حرکت جهت‌دار (نیاز به تأیید)"
                details["subtype"] = "جهت‌دار_احتمالی"
            
            if confidence >= 0.5:
                return MovementType.DIRECTIONAL, details
    
    # تشخیص حرکت غیرجهت‌دار
    # شرط ۱: موج اول و سوم هر دو بیشتر از ۶۱.۸٪ اصلاح شده باشند
    if first is not None and third is not None:
        if first > 0.618 and third > 0.618:
            confidence += 0.4
            # شرط ۲: آخرین موج بیشتر از ۱۶۱.۸٪ اصلاح شده باشد (تأیید پایان)
            if last is not None and last > 1.618:
                confidence += 0.3
                details["conclusion"] = "حرکت غیرجهت‌دار (تکمیل شده) - آخرین موج بیش از ۱۶۱.۸٪ اصلاح"
                details["subtype"] = "غیرجهت‌دار_تکمیل‌شده"
            else:
                confidence += 0.1
                details["conclusion"] = "حرکت غیرجهت‌دار (در حال پیشروی)"
                details["subtype"] = "غیرجهت‌دار_درحال_پیشروی"
            
            if confidence >= 0.5:
                return MovementType.NON_DIRECTIONAL, details
    
    # ── حالت‌های مرزی ─────────────────────────────────────────
    if first is not None and third is not None:
        # تناوب در اصلاح (یک موج کم عمق، یک موج عمیق)
        if (first < 0.618 and third > 0.618) or (first > 0.618 and third < 0.618):
            details["conclusion"] = "تناوب در اصلاح - نیاز به بررسی ساختار کامل‌تر"
            details["subtype"] = "مرزی_تناوب"
            return MovementType.UNKNOWN, details
        
        # اولین موج مرزی (حدود ۶۱.۸٪)
        if 0.60 <= first <= 0.62:
            if details["has_over_100"]:
                details["conclusion"] = "نامشخص - اولین موج مرزی، بازگشت بیش از ۱۰۰٪ مشاهده شده"
            else:
                details["conclusion"] = "نامشخص - اولین موج مرزی، هیچ بازگشتی بیش از ۱۰۰٪ نشده"
            details["subtype"] = "مرزی_موج_اول"
            return MovementType.UNKNOWN, details
    
    # ── بررسی قانون "هیچ صعودی بیش از ۱۰۰٪ بازگشت نشده" ───────
    if details["all_under_100"] and avg_motive < 0.618:
        details["conclusion"] = "احتمالاً حرکت جهت‌دار (قانون بازگشت ۱۰۰٪ رعایت شده)"
        details["subtype"] = "جهت‌دار_محتمل"
        return MovementType.DIRECTIONAL, details
    
    details["conclusion"] = "نامشخص - قوانین کافی برای تشخیص قطعی وجود ندارد"
    details["subtype"] = "نامشخص"
    details["confidence"] = confidence
    return MovementType.UNKNOWN, details


# ════════════════════════════════════════════════════════════════
# بخش ۴: بررسی خط مرکزی نوسان – نسخه کامل با رگرسیون خطی
# ════════════════════════════════════════════════════════════════

def check_central_oscillation_line_advanced(waves: List[WaveSegment]) -> CentralOscillationLine:
    """
    بررسی خط مرکزی نوسان در گذر زمان (صفحه ۳۳، عکس ۲ و ۳).
    
    خط مرکزی = خط رگرسیون خطی (میانگین متحرک خطی) قیمت‌ها در طول زمان.
    
    حرکت جهت‌دار:
        قیمت‌ها باید حول این خط نوسان کنند.
        انحراف مجاز: ۲۵٪ از خط مرکزی.
    
    حرکت غیرجهت‌دار:
        خط مرکزی نشان‌دهنده مرکز نوسان است.
        داده‌ها باید به طور متقارن حول خط مرکزی نوسان کنند.
    
    پارامترها:
        waves: لیست WaveSegment
    
    خروجی:
        CentralOscillationLine
    """
    if len(waves) < 2:
        return CentralOscillationLine(
            slope=0, intercept=0, center_line_values=[], deviations=[],
            avg_deviation=0, max_deviation=0, min_deviation=0,
            is_within_tolerance=False, is_symmetric=False,
            points_above=0, points_below=0, r_squared=0,
            valid=False, reason="موج کافی نیست"
        )
    
    # ── جمع‌آوری همه نقاط قیمت با زمان متناظر ─────────────────
    points = []      # قیمت‌ها
    times = []       # زمان‌ها (ایندکس)
    
    for w in waves:
        points.append(w.start_price)
        times.append(w.start_idx)
        points.append(w.end_price)
        times.append(w.end_idx)
    
    if len(points) < 2:
        return CentralOscillationLine(
            slope=0, intercept=0, center_line_values=[], deviations=[],
            avg_deviation=0, max_deviation=0, min_deviation=0,
            is_within_tolerance=False, is_symmetric=False,
            points_above=0, points_below=0, r_squared=0,
            valid=False, reason="نقاط قیمتی کافی نیست"
        )
    
    # ── رگرسیون خطی برای بدست آوردن خط مرکزی ──────────────────
    slope, intercept, r_value, p_value, std_err = stats.linregress(times, points)
    r_squared = r_value ** 2
    
    # ── محاسبه مقادیر خط مرکزی در هر نقطه زمانی ──────────────
    center_line_values = [slope * t + intercept for t in times]
    
    # ── محاسبه انحراف هر نقطه از خط مرکزی (درصد) ─────────────
    deviations = []
    for i, (t, p) in enumerate(zip(times, points)):
        center = center_line_values[i]
        if center != 0:
            deviation = abs(p - center) / center * 100
            deviations.append(deviation)
        else:
            deviations.append(100.0)
    
    avg_deviation = np.mean(deviations) if deviations else 0
    max_deviation = np.max(deviations) if deviations else 0
    min_deviation = np.min(deviations) if deviations else 0
    
    # ── بررسی تقارن نوسان ─────────────────────────────────────
    # نقاط بالای خط مرکزی و پایین خط مرکزی
    above = [p for p, c in zip(points, center_line_values) if p > c]
    below = [p for p, c in zip(points, center_line_values) if p < c]
    
    points_above = len(above)
    points_below = len(below)
    
    if points_below > 0:
        symmetry_ratio = points_above / points_below
        is_symmetric = 0.5 <= symmetry_ratio <= 2.0
    else:
        is_symmetric = points_above == 0
    
    # ── انحراف مجاز: حداکثر ۲۵٪ از خط مرکزی ──────────────────
    is_within_tolerance = max_deviation <= 25.0
    
    # ── حکم نهایی ────────────────────────────────────────────
    valid = is_within_tolerance and is_symmetric
    
    reason = ""
    if not valid:
        if not is_within_tolerance:
            reason = f"حداکثر انحراف {max_deviation:.1f}% > 25%"
        if not is_symmetric:
            if reason:
                reason += " و "
            reason += f"نوسان متقارن نیست (نسبت نقاط بالا/پایین = {points_above}/{points_below})"
    else:
        reason = f"نوسان حول خط مرکزی با میانگین انحراف {avg_deviation:.1f}%"
    
    return CentralOscillationLine(
        slope=slope,
        intercept=intercept,
        center_line_values=center_line_values,
        deviations=deviations,
        avg_deviation=round(avg_deviation, 2),
        max_deviation=round(max_deviation, 2),
        min_deviation=round(min_deviation, 2),
        is_within_tolerance=is_within_tolerance,
        is_symmetric=is_symmetric,
        points_above=points_above,
        points_below=points_below,
        r_squared=round(r_squared, 4),
        valid=valid,
        reason=reason
    )


# ════════════════════════════════════════════════════════════════
# بخش ۵: محاسبه نسبت‌های فیبوناچی صفحه ۳۳ – نسخه کامل
# ════════════════════════════════════════════════════════════════

def calculate_fibonacci_ratios(waves: List[WaveSegment]) -> Dict:
    """
    محاسبه دقیق نسبت‌های فیبوناچی صفحه ۳۳.
    
    خروجی شامل:
        - نسبت اصلاح هر موج
        - نوع اصلاح هر موج (کم عمق، متوسط، عمیق، کامل، شدید)
        - قوانین نقض‌شده
    """
    if len(waves) < 2:
        return {"error": "موج کافی نیست"}
    
    main_direction = waves[0].direction
    
    results = {
        "wave_retraces": [],
        "motive_retraces": [],
        "corrective_retraces": [],
        "first_motive_retrace": None,
        "second_motive_retrace": None,
        "third_motive_retrace": None,
        "last_corrective_retrace": None,
        "max_retrace": 0.0,
        "has_retrace_over_100": False,
        "has_retrace_over_161_8": False,
        "all_retraces_under_100": True,
        "violations": []
    }
    
    for i, w in enumerate(waves):
        if w.retrace_ratio > 0:
            results["wave_retraces"].append({
                "wave_index": i,
                "retrace_ratio": w.retrace_ratio,
                "retrace_type": w.retrace_type.value,
                "is_corrective": w.direction != main_direction
            })
            
            if w.direction != main_direction:
                results["corrective_retraces"].append(w.retrace_ratio)
                results["last_corrective_retrace"] = w.retrace_ratio
            else:
                results["motive_retraces"].append(w.retrace_ratio)
            
            if w.retrace_ratio > results["max_retrace"]:
                results["max_retrace"] = w.retrace_ratio
            if w.retrace_ratio > 1.0:
                results["has_retrace_over_100"] = True
                results["all_retraces_under_100"] = False
            if w.retrace_ratio > 1.618:
                results["has_retrace_over_161_8"] = True
    
    # نسبت‌های موج‌های شتابدار اول، دوم و سوم
    motive_retraces = [r for r in results["wave_retraces"] if not r["is_corrective"]]
    for i, mr in enumerate(motive_retraces[:3]):
        if i == 0:
            results["first_motive_retrace"] = mr["retrace_ratio"]
        elif i == 1:
            results["second_motive_retrace"] = mr["retrace_ratio"]
        elif i == 2:
            results["third_motive_retrace"] = mr["retrace_ratio"]
    
    return results


# ════════════════════════════════════════════════════════════════
# بخش ۶: ساخت مربع تناسب – نسخه کامل با مقیاس لگاریتمی فازی
# ════════════════════════════════════════════════════════════════

def get_log_scale_factor_fuzzy(start_price: float, end_price: float) -> Tuple[bool, float]:
    """
    تعیین مقیاس لگاریتمی به صورت فازی (درجه‌بندی پیوسته).
    
    مطابق صفحه ۴۹:
        "اگر قیمت بالا بیش از دو برابر قیمت پایین باشد، نمودار لگاریتمی مناسب است.
        هر چه اختلاف درصد بیشتر باشد، اهمیت مقیاس لگاریتمی بیشتر است."
    
    پارامترها:
        start_price: قیمت شروع
        end_price: قیمت پایان
    
    خروجی:
        (use_log_scale, factor) – factor از ۰ تا ۱
    """
    if start_price <= 0 or end_price <= 0:
        return False, 0.0
    
    ratio = max(end_price, start_price) / min(end_price, start_price)
    
    if ratio >= 3.0:
        # بیش از ۳ برابر → لگاریتمی کامل
        return True, 1.0
    elif ratio >= 2.0:
        # بین ۲ تا ۳ برابر → لگاریتمی با ضریب فازی
        factor = (ratio - 2.0) / 1.0  # 2.0→0, 3.0→1
        return True, factor
    elif ratio >= 1.5:
        # بین ۱.۵ تا ۲ برابر → لگاریتمی ضعیف
        factor = (ratio - 1.5) / 0.5 * 0.5  # 1.5→0, 2.0→0.5
        return True, factor
    else:
        # کمتر از ۱.۵ برابر → خطی
        return False, 0.0


def build_proportion_square_advanced(
    start_price: float,
    end_price: float,
    start_time: int,
    end_time: int,
    movement_type: MovementType,
    waves: List[WaveSegment]
) -> ProportionSquare:
    """
    ساخت مربع تناسب کامل مطابق صفحات ۳۷-۴۲.
    
    برای حرکت جهت‌دار (صفحات ۳۷-۴۰):
        - بعد بزرگتر = قیمت (معمولاً)
        - مربع حول خط ۴۵ درجه
        - انحراف مجاز: ۲۵٪ در هر بعد
        - نقطه خاتمه باید نزدیک گوشه مقابل باشد
        - خاتمه دیرهنگام یا زودهنگام با انحراف حداکثر ۲۵٪ قابل قبول است (عکس ۵.jpg و ۶.jpg)
        - خاتمه نامناسب اگر انحراف بیش از ۲۵٪ باشد (عکس ۷.jpg)
    
    برای حرکت غیرجهت‌دار (صفحات ۴۱-۴۲):
        - بعد بزرگتر = زمان (معمولاً)
        - داده‌ها باید تقریباً نیمی از مربع را پوشش دهند
        - دورترین نقطه قیمتی باید به نقطه ۵۰٪ پایان نزدیک باشد (عکس ۸.jpg و ۹.jpg)
    
    قانون مقیاس لگاریتمی (صفحه ۴۹):
        - اگر قیمت بالا بیش از دو برابر قیمت پایین باشد، از مقیاس لگاریتمی استفاده کن
        - هر چه اختلاف درصد بیشتر باشد، اهمیت مقیاس لگاریتمی بیشتر است
    
    پارامترها:
        start_price: قیمت شروع حرکت
        end_price: قیمت پایان حرکت
        start_time: زمان شروع (ایندکس)
        end_time: زمان پایان (ایندکس)
        movement_type: نوع حرکت
        waves: لیست کامل موج‌ها (برای محاسبه دورترین نقطه)
    
    خروجی:
        ProportionSquare با همه جزئیات
    """
    time_range = abs(end_time - start_time)
    
    if time_range <= 0:
        return ProportionSquare(
            width=0, height=0,
            start_price=start_price, end_price=end_price,
            start_time=start_time, end_time=end_time,
            diagonal_slope=0, ideal_slope=1.0, deviation_percent=100,
            is_valid_slope=False,
            price_distance_to_target=0, time_distance_to_target=0,
            price_reached_target=False, time_reached_target=False,
            corner_reached=False, coverage_50_percent=0, coverage_50_valid=False,
            use_log_scale=False, log_scale_factor=0,
            opposite_corner="نامشخص", longer_dimension="نامشخص",
            completion_status="نامشخص"
        )
    
    # ════════════════════════════════════════════════════════════
    # قانون مقیاس لگاریتمی فازی (صفحه ۴۹)
    # ════════════════════════════════════════════════════════════
    use_log_scale, log_factor = get_log_scale_factor_fuzzy(start_price, end_price)
    
    # ════════════════════════════════════════════════════════════
    # محاسبه دامنه قیمتی در مقیاس مناسب
    # ════════════════════════════════════════════════════════════
    if use_log_scale and start_price > 0 and end_price > 0:
        # در مقیاس لگاریتمی، دامنه قیمت = اختلاف لگاریتم‌ها
        log_start = math.log(start_price)
        log_end = math.log(end_price)
        price_range = abs(log_end - log_start)
        price_range_linear = abs(end_price - start_price)
        price_range_log = price_range
    else:
        price_range = abs(end_price - start_price)
        price_range_linear = price_range
        price_range_log = price_range
    
    if price_range <= 0:
        return ProportionSquare(
            width=0, height=0,
            start_price=start_price, end_price=end_price,
            start_time=start_time, end_time=end_time,
            diagonal_slope=0, ideal_slope=1.0, deviation_percent=100,
            is_valid_slope=False,
            price_distance_to_target=0, time_distance_to_target=0,
            price_reached_target=False, time_reached_target=False,
            corner_reached=False, coverage_50_percent=0, coverage_50_valid=False,
            use_log_scale=use_log_scale, log_scale_factor=log_factor,
            opposite_corner="نامشخص", longer_dimension="نامشخص",
            completion_status="نامشخص"
        )
    
    # ════════════════════════════════════════════════════════════
    # تعیین بعد بزرگتر و ضلع مربع (صفحات ۳۷ و ۴۱)
    # ════════════════════════════════════════════════════════════
    if movement_type == MovementType.DIRECTIONAL:
        # برای حرکت جهت‌دار: بعد بزرگتر = بزرگتر بین قیمت و زمان
        longer_dimension = "price" if price_range > time_range else "time"
        square_side = max(price_range, time_range)
    else:
        # برای حرکت غیرجهت‌دار: بعد بزرگتر = زمان (صفحه ۴۱)
        longer_dimension = "time"
        square_side = time_range
    
    # ════════════════════════════════════════════════════════════════
    # محاسبه گوشه مقابل مربع
    # ════════════════════════════════════════════════════════════════
    is_uptrend = end_price > start_price
    
    # محاسبه target_price با مدیریت خطا برای log
    if use_log_scale and start_price > 0 and end_price > 0:
        try:
            log_start = math.log(start_price)
            log_end = math.log(end_price)
            price_range_log = abs(log_end - log_start)
            
            if movement_type == MovementType.DIRECTIONAL:
                if is_uptrend:
                    target_log = log_start + square_side
                    opposite_corner = "پایین-چپ → بالا-راست"
                else:
                    target_log = log_start - square_side
                    opposite_corner = "بالا-چپ → پایین-راست"
                target_price = math.exp(target_log) if target_log > -50 else start_price * 0.5
            else:
                # حرکت غیرجهت‌دار - محاسبه خطی
                if is_uptrend:
                    growth_rate = price_range_linear / time_range if time_range > 0 else 0
                    target_price = start_price + growth_rate * square_side
                    opposite_corner = "پایین-چپ → بالا-راست (غیرجهت‌دار)"
                else:
                    decline_rate = price_range_linear / time_range if time_range > 0 else 0
                    target_price = start_price - decline_rate * square_side
                    if target_price < 0:
                        target_price = start_price * 0.1
                    opposite_corner = "بالا-چپ → پایین-راست (غیرجهت‌دار)"
        except (ValueError, OverflowError):
            # در صورت خطا در log، به حالت خطی برگرد
            use_log_scale = False
            log_factor = 0.0
            if movement_type == MovementType.DIRECTIONAL:
                if is_uptrend:
                    target_price = start_price + square_side
                    opposite_corner = "پایین-چپ → بالا-راست"
                else:
                    target_price = start_price - square_side
                    opposite_corner = "بالا-چپ → پایین-راست"
            else:
                if is_uptrend:
                    growth_rate = price_range_linear / time_range if time_range > 0 else 0
                    target_price = start_price + growth_rate * square_side
                    opposite_corner = "پایین-چپ → بالا-راست (غیرجهت‌دار)"
                else:
                    decline_rate = price_range_linear / time_range if time_range > 0 else 0
                    target_price = start_price - decline_rate * square_side
                    if target_price < 0:
                        target_price = start_price * 0.1
                    opposite_corner = "بالا-چپ → پایین-راست (غیرجهت‌دار)"
    else:
        # حالت خطی
        if movement_type == MovementType.DIRECTIONAL:
            if is_uptrend:
                target_price = start_price + square_side
                opposite_corner = "پایین-چپ → بالا-راست"
            else:
                target_price = start_price - square_side
                opposite_corner = "بالا-چپ → پایین-راست"
        else:
            # حرکت غیرجهت‌دار خطی
            if is_uptrend:
                growth_rate = price_range_linear / time_range if time_range > 0 else 0
                target_price = start_price + growth_rate * square_side
                opposite_corner = "پایین-چپ → بالا-راست (غیرجهت‌دار)"
            else:
                decline_rate = price_range_linear / time_range if time_range > 0 else 0
                target_price = start_price - decline_rate * square_side
                if target_price < 0:
                    target_price = start_price * 0.1
                opposite_corner = "بالا-چپ → پایین-راست (غیرجهت‌دار)"
    
    # محاسبه زمان هدف
    if movement_type == MovementType.DIRECTIONAL and longer_dimension == "price":
        target_time = start_time + price_range
    else:
        target_time = start_time + square_side
    
    # ════════════════════════════════════════════════════════════
    # محاسبه شیب واقعی و انحراف از ۴۵ درجه
    # ════════════════════════════════════════════════════════════
    actual_slope = price_range / time_range if time_range > 0 else float('inf')
    ideal_slope = 1.0
    deviation = abs(actual_slope - ideal_slope) / ideal_slope * 100 if ideal_slope > 0 else 0
    is_slope_valid = deviation <= 25.0
    
    # ════════════════════════════════════════════════════════════
    # بررسی نزدیکی نقطه خاتمه به گوشه مقابل
    # ════════════════════════════════════════════════════════════
    max_deviation = square_side * 0.25  # ۲۵٪ از ضلع مربع
    
    if use_log_scale and end_price > 0 and target_price > 0:
        log_end = math.log(end_price)
        log_target = math.log(target_price)
        price_distance = abs(log_end - log_target)
        is_price_near_target = price_distance <= max_deviation
    else:
        price_distance = abs(end_price - target_price)
        is_price_near_target = price_distance <= max_deviation
    
    time_distance = abs(end_time - target_time)
    is_time_near_target = time_distance <= max_deviation
    
    corner_reached = is_price_near_target and is_time_near_target
    
    # تعیین وضعیت خاتمه (عکس ۵.jpg، ۶.jpg، ۷.jpg)
    if movement_type == MovementType.DIRECTIONAL:
        if deviation <= 25:
            if corner_reached:
                completion_status = "✅ خاتمه مناسب (در گوشه مربع)"
            elif is_time_near_target and not is_price_near_target:
                if end_time > target_time:
                    completion_status = "⚠️ خاتمه دیرهنگام (انحراف قابل قبول - عکس ۵.jpg)"
                else:
                    completion_status = "⚠️ خاتمه زودهنگام (انحراف قابل قبول - عکس ۶.jpg)"
            else:
                completion_status = "❌ خاتمه نامناسب (انحراف غیرقابل قبول - عکس ۷.jpg)"
        else:
            completion_status = "❌ خاتمه نامناسب (انحراف بیش از حد)"
    else:
        completion_status = "نامربوط (حرکت غیرجهت‌دار)"
    
    # ════════════════════════════════════════════════════════════
    # قانون پوشش ۵۰٪ مربع برای حرکت غیرجهت‌دار (صفحات ۴۱-۴۲)
    # ════════════════════════════════════════════════════════════
    coverage_50_percent = 0.0
    coverage_50_valid = False
        
    if movement_type == MovementType.NON_DIRECTIONAL and len(waves) > 0:
        # پیدا کردن دورترین نقطه قیمتی از ابتدای الگو
        is_uptrend = end_price > start_price
            
        if is_uptrend:
            farthest_price = max([w.end_price for w in waves] + [start_price])
            farthest_idx = max([w.end_idx for w in waves] + [start_time])
        else:
            farthest_price = min([w.end_price for w in waves] + [start_price])
            farthest_idx = min([w.end_idx for w in waves] + [start_time])
            
        # نقطه ۵۰٪ مربع - محاسبه با استفاده از start_price و target_price (بدون log_start)
        fifty_point = start_price + (target_price - start_price) * 0.5
        distance_to_50 = abs(end_price - fifty_point)
        coverage_50_valid = distance_to_50 <= max_deviation
            
        # محاسبه درصد پوشش برای حرکت غیرجهت‌دار (اختیاری)
        total_distance = abs(target_price - fifty_point) * 2
        if total_distance > 0:
            coverage_50_percent = (1 - abs(farthest_price - fifty_point) / total_distance) * 100
    
    # ════════════════════════════════════════════════════════════
    # ساخت خروجی
    # ════════════════════════════════════════════════════════════
    return ProportionSquare(
        width=price_range if not use_log_scale else price_range_log,
        height=time_range,
        start_price=start_price,
        end_price=target_price,
        start_time=start_time,
        end_time=target_time,
        diagonal_slope=round(actual_slope, 4),
        ideal_slope=ideal_slope,
        deviation_percent=round(deviation, 1),
        is_valid_slope=is_slope_valid,
        price_distance_to_target=round(price_distance, 4),
        time_distance_to_target=round(time_distance, 4),
        price_reached_target=is_price_near_target,
        time_reached_target=is_time_near_target,
        corner_reached=corner_reached,
        coverage_50_percent=round(coverage_50_percent, 1),
        coverage_50_valid=coverage_50_valid,
        use_log_scale=use_log_scale,
        log_scale_factor=round(log_factor, 2),
        opposite_corner=opposite_corner,
        longer_dimension=longer_dimension,
        completion_status=completion_status
    )


# ════════════════════════════════════════════════════════════════
# بخش ۷: تابع analyze (interface اصلی)
# ════════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None, context=None) -> Dict:
    """
    فصل ۶: قانون تناسب (Proportion)
    
    پیاده‌سازی کامل مطابق صفحات ۳۳-۴۲ کتاب گلن نیلی.
    
    پارامترها:
        data: DataFrame با ستون‌های open, high, low, close, volume
        logger: ResultsLogger (اختیاری)
        context: دیکشنری نتایج فصل‌های قبلی (وابستگی‌ها)
    """
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۱: استخراج داده‌های قیمتی
    # ════════════════════════════════════════════════════════════
    close = data['close'].values if 'close' in data.columns else data['Close'].values
    high = data['high'].values if 'high' in data.columns else data['High'].values
    low = data['low'].values if 'low' in data.columns else data['Low'].values
    
    n = len(close)
    
    if n < 10:
        return {
            "عنوان": "فصل ۶: قانون تناسب",
            "وضعیت": "داده_کافی_نیست",
            "تعداد_کندل": str(n),
            "پیام": "برای تحلیل قانون تناسب حداقل ۱۰ کندل لازم است"
        }
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۲: دریافت موج‌ها از فصل ۵ (از context)
    # ════════════════════════════════════════════════════════════
    waves = []
    context_used = False

    if context and "chapter_5" in context:
        ch5 = context["chapter_5"]
        if "_monowaves" in ch5 and ch5["_monowaves"]:
            # تبدیل مونوویوهای فصل ۵ به WaveSegment های فصل ۶
            mono_list = ch5["_monowaves"]
            for idx, mw in enumerate(mono_list):
                # direction رو به int تبدیل کن
                direction = 1 if mw.direction.value == "UP" else -1
            
                wave = WaveSegment(
                    index=idx,
                    start_idx=mw.start_bar,
                    end_idx=mw.end_bar,
                    start_price=mw.start_price,
                    end_price=mw.end_price,
                    direction=direction,
                    price_range=mw.price_range,
                    duration=mw.duration,
                    start_type="PEAK" if direction == 1 else "TROUGH",
                    end_type="TROUGH" if direction == 1 else "PEAK",
                )
                waves.append(wave)
            context_used = True

    # اگر از context دریافت نشد، خودمان استخراج می‌کنیم
    if not waves:
        waves = extract_wave_segments(high, low, close, order=2)
    
    if len(waves) < 5:
        return {
            "عنوان": "فصل ۶: قانون تناسب",
            "وضعیت": "موج_کافی_نیست",
            "تعداد_موج": str(len(waves)),
            "پیام": "برای تشخیص دقیق نوع حرکت حداقل ۵ موج لازم است"
        }
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۳: تشخیص نوع حرکت (صفحات ۳۳-۳۴)
    # ════════════════════════════════════════════════════════════
    movement_type, movement_details = detect_movement_type_advanced(waves)
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۴: محاسبه نسبت‌های فیبوناچی صفحه ۳۳
    # ════════════════════════════════════════════════════════════
    fib_ratios = calculate_fibonacci_ratios(waves)
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۵: بررسی خط مرکزی نوسان (صفحه ۳۳)
    # ════════════════════════════════════════════════════════════
    center_line_result = check_central_oscillation_line_advanced(waves)
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۶: ساخت مربع تناسب
    # ════════════════════════════════════════════════════════════
    first_wave = waves[0]
    last_wave = waves[-1]
    
    square = build_proportion_square_advanced(
        start_price=first_wave.start_price,
        end_price=last_wave.end_price,
        start_time=first_wave.start_idx,
        end_time=last_wave.end_idx,
        movement_type=movement_type,
        waves=waves
    )
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۷: ارزیابی قانون تناسب
    # ════════════════════════════════════════════════════════════
    violation_reasons = []
    
    if movement_type == MovementType.DIRECTIONAL:
        # حرکت جهت‌دار باید:
        # 1. شیب ۴۵ درجه با انحراف < ۲۵٪
        # 2. نقطه خاتمه نزدیک به گوشه مقابل
        # 3. نوسان حول خط مرکزی (انحراف < ۲۵٪)
        # 4. هیچ بازگشتی بیش از ۱۰۰٪ نباشد (قانون صفحه ۳۳)
        
        proportion_valid = (
            square.is_valid_slope and
            square.corner_reached and
            center_line_result.valid and
            movement_details.get("all_under_100", False)
        )
        
        if not square.is_valid_slope:
            violation_reasons.append(f"انحراف از خط ۴۵ درجه ({square.deviation_percent}% > 25%)")
        if not square.corner_reached:
            if not square.price_reached_target:
                violation_reasons.append(f"نقطه خاتمه از نظر قیمتی به گوشه مربع نزدیک نیست (فاصله {square.price_distance_to_target:.4f})")
            if not square.time_reached_target:
                violation_reasons.append(f"نقطه خاتمه از نظر زمانی به گوشه مربع نزدیک نیست (فاصله {square.time_distance_to_target:.0f})")
        if not center_line_result.valid:
            violation_reasons.append(f"نوسان حول خط مرکزی: {center_line_result.reason}")
        if not movement_details.get("all_under_100", False):
            violation_reasons.append("نقض قانون 'هیچ صعودی بیش از ۱۰۰٪ بازگشت نشده است'")
            
    elif movement_type == MovementType.NON_DIRECTIONAL:
        # حرکت غیرجهت‌دار باید:
        # 1. پوشش ۵۰٪ مربع (صفحه ۴۱)
        # 2. نوسان حول خط مرکزی
        # 3. اولین موج > ۶۱.۸٪ و آخرین موج > ۱۶۱.۸٪ اصلاح
        
        first_retrace = movement_details.get("wave_1_retrace", 0)
        last_retrace = movement_details.get("last_retrace", 0)
        
        proportion_valid = (
            square.coverage_50_valid and
            center_line_result.valid and
            first_retrace > 0.618 and
            last_retrace > 1.618
        )
        
        if not square.coverage_50_valid:
            violation_reasons.append(f"پوشش ۵۰٪ مربع رعایت نشده (پوشش فعلی {square.coverage_50_percent:.1f}%)")
        if not center_line_result.valid:
            violation_reasons.append(f"نوسان حول خط مرکزی: {center_line_result.reason}")
        if first_retrace <= 0.618:
            violation_reasons.append(f"اولین موج فقط {first_retrace*100:.1f}% اصلاح شده (باید > ۶۱.۸٪)")
        if last_retrace <= 1.618:
            violation_reasons.append(f"آخرین موج فقط {last_retrace*100:.1f}% اصلاح شده (باید > ۱۶۱.۸٪)")
        
    else:
        proportion_valid = False
        violation_reasons = ["نوع حرکت نامشخص است - قانون تناسب قابل اعمال نیست"]
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۸: ساخت خروجی
    # ════════════════════════════════════════════════════════════
    
    results = {
        # ── شناسنامه ──
        "عنوان": "فصل ۶: قانون تناسب (Proportion)",
        "مرجع_کتاب": "صفحات ۳۳-۴۲ - گلن نیلی",
        "وضعیت": "تحلیل_کامل",
        
        # ── اطلاعات پایه ──
        "تعداد_کندل": str(n),
        "تعداد_موج_استخراج‌شده": str(len(waves)),
        "قیمت_شروع_حرکت": str(round(first_wave.start_price, 4)),
        "قیمت_پایان_حرکت": str(round(last_wave.end_price, 4)),
        "بازه_قیمتی_خطی": str(round(abs(last_wave.end_price - first_wave.start_price), 4)),
        "بازه_زمانی": str(last_wave.end_idx - first_wave.start_idx),
        
        # ── تشخیص نوع حرکت ──
        "نوع_حرکت": movement_type.value,
        "جهت_اصلی": movement_details.get("main_direction", "نامشخص"),
        "اولین_موج_اصلاح": f"{movement_details.get('wave_1_retrace', 0) * 100:.1f}%",
        "نوع_اصلاح_اولین_موج": movement_details.get("first_corrective_retrace", 0) > 0.618 if movement_details.get("first_corrective_retrace") else "نامشخص",
        "سومین_موج_اصلاح": f"{movement_details.get('wave_3_retrace', 0) * 100:.1f}%",
        "پنجمین_موج_اصلاح": f"{movement_details.get('wave_5_retrace', 0) * 100:.1f}%",
        "آخرین_موج_اصلاح": f"{(movement_details.get('last_retrace') or 0) * 100:.1f}%",
        "بیشترین_اصلاح": f"{movement_details.get('max_retrace', 0) * 100:.1f}%",
        "میانگین_اصلاح_موج_شتابدار": f"{movement_details.get('avg_motive_retrace', 0) * 100:.1f}%",
        "بازگشت_بیش_از_100درصد": "بله" if movement_details.get("has_over_100") else "خیر",
        "بازگشت_بیش_از_161_8درصد": "بله" if movement_details.get("has_over_161_8") else "خیر",
        "تشخیص_جزئیات": movement_details.get("conclusion", ""),
        "تشخیص_زیرنوع": movement_details.get("subtype", ""),
        "امتیاز_اطمینان": str(round(movement_details.get("confidence", 0) * 100, 1)),
        
        # ── قانون مربع ۴۵ درجه (صفحات ۳۷-۴۰) ──
        "ضلع_مربع": str(round(square.height, 4)),
        "بعد_بزرگتر": square.longer_dimension,
        "شیب_ایده‌آل": str(square.ideal_slope),
        "شیب_واقعی": str(square.diagonal_slope),
        "انحراف_از_45_درجه": f"{square.deviation_percent}%",
        "حداکثر_انحراف_مجاز": "۲۵٪",
        "انحراف_قابل_قبول": "بله" if square.is_valid_slope else "خیر",
        "فاصله_قیمت_تا_گوشه": str(square.price_distance_to_target),
        "فاصله_زمان_تا_گوشه": str(square.time_distance_to_target),
        "نقطه_خاتمه_نزدیک_قیمت": "بله" if square.price_reached_target else "خیر",
        "نقطه_خاتمه_نزدیک_زمان": "بله" if square.time_reached_target else "خیر",
        "نقطه_خاتمه_در_گوشه_مقابل": "بله" if square.corner_reached else "خیر",
        "گوشه_مقابل": square.opposite_corner,
        "وضعیت_خاتمه": square.completion_status,
        "مقیاس_لگاریتمی": "بله" if square.use_log_scale else "خیر",
        "ضریب_لگاریتم": str(square.log_scale_factor),
        "دلیل_استفاده_از_لگاریتم": f"نسبت قیمت‌ها = {max(last_wave.end_price, first_wave.start_price) / min(last_wave.end_price, first_wave.start_price):.2f}" if square.use_log_scale else "نسبت قیمت‌ها ≤ ۱.۵",
        
        # ── قانون پوشش ۵۰٪ مربع (صفحات ۴۱-۴۲) ──
        "پوشش_50_درصد_مربع": "بله" if square.coverage_50_valid else "خیر",
        "درصد_پوشش_مربع": f"{square.coverage_50_percent}%",
        
        # ── خط مرکزی نوسان (صفحه ۳۳) ──
        "خط_مرکزی_شیب": str(round(center_line_result.slope, 4)),
        "خط_مرکزی_عرض_از_مبدا": str(round(center_line_result.intercept, 4)),
        "میانگین_انحراف_از_خط_مرکزی": f"{center_line_result.avg_deviation}%",
        "بیشترین_انحراف_از_خط_مرکزی": f"{center_line_result.max_deviation}%",
        "کمترین_انحراف_از_خط_مرکزی": f"{center_line_result.min_deviation}%",
        "نقاط_بالای_خط": str(center_line_result.points_above),
        "نقاط_پایین_خط": str(center_line_result.points_below),
        "تقارن_نوسان": "بله" if center_line_result.is_symmetric else "خیر",
        "نوسان_حول_خط_مرکزی": "بله" if center_line_result.valid else "خیر",
        "ضریب_تعیین_رگرسیون": str(center_line_result.r_squared),
        "دلیل_خط_مرکزی": center_line_result.reason,
        
        # ── قوانین صفحه ۳۳ ──
        "قانون_تناسب_1": "اولین موج از حرکت جهت‌دار: بیش از ۶۱.۸٪ اصلاح نمی‌شود",
        "قانون_تناسب_2": "آخرین موج از حرکت جهت‌دار: بیش از ۱۰۰٪ اصلاح می‌شود",
        "قانون_تناسب_3": "اولین موج از حرکت غیرجهت‌دار: بیش از ۶۱.۸٪ اصلاح می‌شود",
        "قانون_تناسب_4": "آخرین موج از حرکت غیرجهت‌دار: بیش از ۱۶۱.۸٪ اصلاح می‌شود",
        "قانون_بازگشت_100درصد": "هیچ صعودی بیش از ۱۰۰٪ بازگشت نشده است (عکس ۱.jpg)",
        "قانون_خط_مرکزی": "قیمت‌ها حول خط مرکزی نوسان در گذر زمان (عکس ۲.jpg و ۳.jpg)",
        "قانون_مربع_45_درجه": "داده‌ها باید درون مربع حول خط ۴۵ درجه نوسان کنند (انحراف مجاز ۲۵٪)",
        "قانون_پوشش_50_درصد": "در حرکت غیرجهت‌دار داده‌ها باید تقریباً نیمی از مربع را پوشش دهند (صفحات ۴۱-۴۲)",
        
        # ── نتیجه نهایی ──
        "قانون_تناسب_رعایت_شده": "بله" if proportion_valid else "خیر",
        "دلیل_نقض": " | ".join(violation_reasons) if violation_reasons else "هیچ",
        "نتیجه_نهایی": "✅ قانون تناسب رعایت شده است" if proportion_valid else "❌ قانون تناسب نقض شده است",
    }
    
    # ── تفسیر نهایی ──
    results["تفسیر_نهایی"] = _build_final_interpretation(
        results, square, movement_type, center_line_result, movement_details
    )
    
    # ── ثبت در لاگ ──
    if logger:
        _write_to_logger(logger, results, square, movement_details, center_line_result)
    
    return results


# ════════════════════════════════════════════════════════════════
# بخش ۸: تفسیر نهایی
# ════════════════════════════════════════════════════════════════

def _build_final_interpretation(
    results: Dict,
    square: ProportionSquare,
    movement_type: MovementType,
    center_line_result: CentralOscillationLine,
    movement_details: Dict
) -> str:
    """تولید تفسیر متنی کامل قانون تناسب مطابق کتاب"""
    
    proportion_ok = results.get("قانون_تناسب_رعایت_شده") == "بله"
    
    if proportion_ok:
        status_icon = "✅"
        status_text = "قانون تناسب رعایت شده است"
    else:
        status_icon = "❌"
        status_text = "قانون تناسب نقض شده است"
    
    retrace_info = ""
    if movement_type == MovementType.DIRECTIONAL:
        if movement_details.get("all_under_100", False):
            retrace_info = "\n  ✅ قانون بازگشت ۱۰۰٪ رعایت شده: هیچ بازگشتی بیش از ۱۰۰٪ نشده"
        else:
            retrace_info = "\n  ❌ نقض قانون بازگشت ۱۰۰٪: حداقل یک بازگشت بیش از ۱۰۰٪ داشته‌ایم"
    
    return f"""
═══════════════════════════════════════════════════════════════════
  فصل ۶: قانون تناسب (Proportion) - صفحات ۳۳ تا ۴۲
  مرجع: گلن نیلی | سبک نئوویو
═══════════════════════════════════════════════════════════════════

📐 {status_icon} {status_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 تشخیص نوع حرکت (صفحات ۳۳-۳۴):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • نوع حرکت شناسایی‌شده: {movement_type.value}
  • جهت اصلی: {results.get('جهت_اصلی', 'نامشخص')}
  • اولین موج (اصلاح): {results.get('اولین_موج_اصلاح', 'نامشخص')}
  • سومین موج (اصلاح): {results.get('سومین_موج_اصلاح', 'نامشخص')}
  • آخرین موج (اصلاح): {results.get('آخرین_موج_اصلاح', 'نامشخص')}
  • بیشترین اصلاح: {results.get('بیشترین_اصلاح', 'نامشخص')}
  • میانگین اصلاح موج شتابدار: {results.get('میانگین_اصلاح_موج_شتابدار', 'نامشخص')}
  • {results.get('تشخیص_جزئیات', '')}
  {retrace_info}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📏 قانون مربع ۴۵ درجه (صفحات ۳۷-۴۰):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • مقیاس استفاده‌شده: {results.get('مقیاس_لگاریتمی', 'نامشخص')} (ضریب {results.get('ضریب_لگاریتم', '۰')})
  • شیب واقعی حرکت: {square.diagonal_slope} (ایده‌آل: {square.ideal_slope})
  • انحراف از خط ۴۵ درجه: {square.deviation_percent}%
  • انحراف مجاز: ۲۵٪ → {'✅ قبول' if square.is_valid_slope else '❌ رد'}
  • فاصله قیمت تا گوشه مقابل: {square.price_distance_to_target}
  • فاصله زمان تا گوشه مقابل: {square.time_distance_to_target}
  • نقطه خاتمه نسبت به گوشه مقابل: {results.get('نقطه_خاتمه_در_گوشه_مقابل', 'نامشخص')}
  • وضعیت خاتمه: {square.completion_status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 قانون پوشش ۵۰٪ مربع (صفحات ۴۱-۴۲):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • پوشش ۵۰٪ مربع: {results.get('پوشش_50_درصد_مربع', 'نامربوط')}
  • درصد پوشش: {results.get('درصد_پوشش_مربع', 'نامشخص')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 خط مرکزی نوسان (صفحه ۳۳، عکس ۲ و ۳):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • شیب خط مرکزی: {center_line_result.slope:.4f}
  • میانگین انحراف: {center_line_result.avg_deviation}%
  • بیشترین انحراف: {center_line_result.max_deviation}%
  • نقاط بالای خط: {center_line_result.points_above}
  • نقاط پایین خط: {center_line_result.points_below}
  • تقارن نوسان: {results.get('تقارن_نوسان', 'نامشخص')}
  • ضریب تعیین (R²): {center_line_result.r_squared}
  • {center_line_result.reason}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 چهار قانون اصلی صفحه ۳۳:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {results.get('قانون_تناسب_1', '')}
  {results.get('قانون_تناسب_2', '')}
  {results.get('قانون_تناسب_3', '')}
  {results.get('قانون_تناسب_4', '')}
  {results.get('قانون_بازگشت_100درصد', '')}
  {results.get('قانون_خط_مرکزی', '')}

💡 **نتیجه نئوویو:**
   {results.get('نتیجه_نهایی', 'نامشخص')}
   {results.get('دلیل_نقض', '')}
   {'✅ می‌توانید تحلیل موج‌شماری را ادامه دهید.' if proportion_ok else '❌ قبل از ادامه تحلیل، محدوده مناسبی انتخاب کنید که قانون تناسب در آن رعایت شود.'}

═══════════════════════════════════════════════════════════════════
"""


# ════════════════════════════════════════════════════════════════
# بخش ۹: ثبت در لاگ
# ════════════════════════════════════════════════════════════════

def _write_to_logger(logger, results: Dict, square: ProportionSquare, movement_details: Dict, center_line_result: CentralOscillationLine):
    """ثبت نتایج در لاگر"""
    logger.add_section("فصل ۶: قانون تناسب (Proportion)", level=1)
    logger.add_result("مرجع کتاب", "صفحات ۳۳-۴۲ - گلن نیلی")
    logger.add_result("تعداد کندل", results["تعداد_کندل"])
    logger.add_result("تعداد موج", results["تعداد_موج_استخراج‌شده"])
    logger.add_result("نوع حرکت", results["نوع_حرکت"])
    logger.add_result("اولین موج (اصلاح)", results["اولین_موج_اصلاح"])
    logger.add_result("سومین موج (اصلاح)", results["سومین_موج_اصلاح"])
    logger.add_result("آخرین موج (اصلاح)", results["آخرین_موج_اصلاح"])
    logger.add_result("امتیاز اطمینان", results["امتیاز_اطمینان"])
    logger.add_result("مقیاس لگاریتمی", results["مقیاس_لگاریتمی"])
    logger.add_result("شیب واقعی", results["شیب_واقعی"])
    logger.add_result("انحراف از ۴۵ درجه", results["انحراف_از_45_درجه"])
    logger.add_result("انحراف قابل قبول", results["انحراف_قابل_قبول"])
    logger.add_result("نقطه خاتمه در گوشه مقابل", results["نقطه_خاتمه_در_گوشه_مقابل"])
    logger.add_result("پوشش ۵۰٪ مربع", results["پوشش_50_درصد_مربع"])
    logger.add_result("نوسان حول خط مرکزی", results["نوسان_حول_خط_مرکزی"])
    logger.add_result("قانون تناسب رعایت شده", results["قانون_تناسب_رعایت_شده"])
    logger.add_result("تفسیر نهایی", results["تفسیر_نهایی"])
    
    logger.add_section("قوانین صفحه ۳۳", level=2)
    for i in range(1, 5):
        logger.add_result(f"قانون {i}", results.get(f"قانون_تناسب_{i}", ""))
    logger.add_result("قانون بازگشت ۱۰۰٪", results.get("قانون_بازگشت_100درصد", ""))
    logger.add_result("قانون خط مرکزی", results.get("قانون_خط_مرکزی", ""))


# ════════════════════════════════════════════════════════════════
# اجرای مستقیم برای تست
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # ایجاد داده تست با نسبت قیمت بالا (برای تست مقیاس لگاریتمی)
    test_data = pd.DataFrame({
        "close": [7000, 7200, 7100, 7500, 7300, 7800, 7600, 8200, 8000, 8500, 8300, 8800, 8600, 9000, 8800, 9200, 9000, 9500, 9300, 9800],
        "high": [7100, 7300, 7200, 7600, 7400, 7900, 7700, 8300, 8100, 8600, 8400, 8900, 8700, 9100, 8900, 9300, 9100, 9600, 9400, 9900],
        "low": [6900, 7100, 7000, 7400, 7200, 7700, 7500, 8100, 7900, 8400, 8200, 8700, 8500, 8900, 8700, 9100, 8900, 9400, 9200, 9700],
        "open": [7000, 7200, 7100, 7500, 7300, 7800, 7600, 8200, 8000, 8500, 8300, 8800, 8600, 9000, 8800, 9200, 9000, 9500, 9300, 9800],
    })
    
    result = analyze(test_data)
    print(result["تفسیر_نهایی"])