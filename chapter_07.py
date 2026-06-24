# chapters/chapter_07.py

"""
فصل ۷: قانون خنثایی (Neutrality)
منبع: کتاب "امواج الیوت به سبک نئوویو" - گلن نیلی - صفحات ۴۳ تا ۴۸

═══════════════════════════════════════════════════════════════════
متن دقیق کتاب (صفحه ۴۳):

"در برخی از موارد در شمارش امواج با امواجی برخورد میکنید که به شکل اریب هستند
و لیکن بیشتر به صورت افقی در بعد زمان در حرکت هستند تا در بعد عمودی (قیمت).
قانون خنثایی نحوه مواجه شدن با این امواج را بیان میدارد."

"برای این منظور در ابتدای موجی که احتمال می رود در شمول این قانون قرار بگیرد،
دو محور مختصاتی که در برگیرنده موج مزبور باشد، رسم کنید به گونه ای که
محور X در راستای بعد زمان موج و محور عمودی در راستای بعد قیمت،
پوشش دهنده موج خنثی (موج دوم) باشد. حال یک خط ۴۵ درجه از مبدا مختصات رسم کنید."

═══════════════════════════════════════════════════════════════════
دو جنبه قانون خنثایی (صفحات ۴۵-۴۸):

جنبه اول (Aspect 1) - عکس ۴۶.jpg و ۴۸.jpg:
    اگر موج خنثی، دو موج خلاف جهت هم را از یکدیگر جدا کند و در راستای موج دوم باشد:
    1. موج اول و دوم با هم به صورت یک تک موج در نظر گرفته می‌شوند
    2. اگر انتهای موج اول پیش از آنکه به میزان ۶۱.۸٪ (توسط مجموع موج دوم و سوم) اصلاح شود،
       شکسته شود، موج دوم و سوم را به صورت تک موج در نظر بگیرید
    3. اگر موج دوم بیش از ۳۸.۲٪ موج اول را بازگشت کرده باشد، احتمالاً بهتر است
       موج دوم و سوم را به صورت تک موج در نظر بگیرید
    4. روش ساده‌تر: یک خط روند از نقطه High پیشین در روند صعودی (نزولی) رسم کنید.
       اگر این خط روند توسط موج مشکوک به خنثی لمس شود، انتهای آن را به عنوان
       انتهای موج پیشین در نظر بگیرید

جنبه دوم (Aspect 2) - عکس ۴۷.jpg و ۴۸.jpg:
    اگر موج خنثی، دو موج هم جهت را از یکدیگر جدا کند و در راستای موج دوم باشد:
    1. می‌توان هر سه موج را با هم به صورت یک تک موج در نظر گرفت
       یا اینکه به صورت سه موج مجزا در نظر گرفت
    2. اگر موج دوم بیش از یک واحد زمانی را به خود اختصاص دهد،
       بایستی موج اول و دوم مجزا در نظر گرفته شوند
    3. روش ساده‌تر: یک خط روند از نقطه High پیشین در روند صعودی (نزولی) رسم کنید.
       اگر این خط روند توسط موج مشکوک به خنثی لمس شود، انتهای آن را به عنوان
       انتهای موج پیشین در نظر بگیرید

═══════════════════════════════════════════════════════════════════
قوانین کلیدی استخراج‌شده از عکس‌ها:

از عکس ۴۳.jpg:
    - موج خنثی باید در ربع اول دستگاه مختصات قرار گیرد (نه حتی منطبق بر خط ۴۵ درجه)
    - موج خنثی باید هم‌راستا با موج بعد از خود باشد

از عکس ۴۴.jpg:
    - حرکت افقی واجد شرایط قانون خنثایی است اگر شیب آن کمتر از ۴۵ درجه باشد
    - زاویه ۹۰ درجه عمودی، زاویه ۰ درجه افقی

از عکس ۴۵.jpg:
    - جنبه اول: موج قبل و بعد خلاف جهت
    - جنبه دوم: موج قبل و بعد هم جهت

از عکس ۴۶.jpg:
    - شرط ۶۱.۸٪: اگر موج اول قبل از اصلاح ۶۱.۸٪ شکسته شود
    - شرط ۳۸.۲٪: اگر موج دوم بیش از ۳۸.۲٪ موج اول را بازگشت کند

از عکس ۴۷.jpg و ۴۸.jpg:
    - حرکت افقی می‌تواند نادیده گرفته شود یا به سه موج کوچکتر تقسیم شود
═══════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
import math
from scipy.signal import argrelextrema
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


# ════════════════════════════════════════════════════════════════
# بخش ۱: تعاریف پایه
# ════════════════════════════════════════════════════════════════

class NeutralityAspect(Enum):
    """دو جنبه قانون خنثایی (صفحه ۴۵)"""
    ASPECT_1 = "جنبه_اول"   # موج قبل و بعد خلاف جهت
    ASPECT_2 = "جنبه_دوم"   # موج قبل و بعد هم جهت
    NOT_APPLICABLE = "قابل_اعمال_نیست"


class NeutralityDecision(Enum):
    """تصمیم نهایی پس از اعمال قانون خنثایی"""
    MERGE_W1_W2 = "ادغام_موج_اول_و_دوم"      # موج اول و دوم با هم یک تک موج
    MERGE_W2_W3 = "ادغام_موج_دوم_و_سوم"      # موج دوم و سوم با هم یک تک موج
    MERGE_ALL_THREE = "ادغام_سه_موج_با_هم"   # هر سه موج با هم یک تک موج
    KEEP_SEPARATE = "حفظ_سه_موج_جداگانه"     # سه موج مجزا
    ADJUST_ENDPOINT = "تعدیل_نقطه_پایانی"    # تغییر نقطه پایان موج پیشین


@dataclass
class WaveSegment:
    """یک قطعه موج برای تحلیل خنثایی"""
    index: int
    start_idx: int
    end_idx: int
    start_price: float
    end_price: float
    direction: int          # +1 صعودی، -1 نزولی
    price_range: float
    duration: int
    start_type: str         # "PEAK" یا "TROUGH"
    end_type: str


@dataclass
class NeutralWave:
    """
    موج خنثی (Neutral Wave) - موجی که تحت شمول قانون خنثایی قرار می‌گیرد
    
    ویژگی‌ها (از عکس ۴۳.jpg و ۴۴.jpg):
    - حرکت افقی (زاویه کمتر از ۴۵ درجه)
    - در ربع اول دستگاه مختصات
    - هم‌راستا با موج بعد از خود
    """
    wave: WaveSegment
    angle_degrees: float            # زاویه موج (۰=افقی، ۹۰=عمودی)
    is_horizontal: bool             # آیا افقی است؟ (زاویه < ۴۵ درجه)
    in_first_quadrant: bool         # آیا در ربع اول است؟
    aligned_with_next: bool         # آیا هم‌راستا با موج بعد است؟
    aspect: NeutralityAspect        # جنبه قابل اعمال


@dataclass
class NeutralityResult:
    """نتیجه اعمال قانون خنثایی روی یک سه‌موجی"""
    aspect: NeutralityAspect
    decision: NeutralityDecision
    new_wave_start_idx: int
    new_wave_end_idx: int
    new_wave_start_price: float
    new_wave_end_price: float
    adjusted_endpoint_idx: Optional[int]
    adjusted_endpoint_price: Optional[float]
    reason: str
    confidence: float                # 0 تا 1


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
    
    مطابق صفحه ۳۲: هر تغییری در جهت قیمت با یک نقطه مشخص شده است.
    
    پارامترها:
        high: آرایه بالاترین قیمت‌ها
        low: آرایه پایین‌ترین قیمت‌ها
        close: آرایه قیمت بسته شدن
        order: حساسیت تشخیص نقاط چرخش
    
    خروجی:
        لیست WaveSegment
    """
    n = len(close)
    
    # ── شناسایی قله‌ها و دره‌ها ─────────────────────────────────
    peak_indices = argrelextrema(high, np.greater, order=order)[0]
    trough_indices = argrelextrema(low, np.less, order=order)[0]
    
    # ── ترکیب نقاط ────────────────────────────────────────────
    points = []
    for idx in peak_indices:
        points.append((int(idx), float(high[idx]), "PEAK"))
    for idx in trough_indices:
        points.append((int(idx), float(low[idx]), "TROUGH"))
    
    if len(points) < 2:
        return []
    
    points.sort(key=lambda x: x[0])
    
    # ── حذف نقاط هم‌نوع متوالی ────────────────────────────────
    filtered = []
    for pt in points:
        if not filtered:
            filtered.append(pt)
            continue
        last = filtered[-1]
        if last[2] == pt[2]:
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
        
        waves.append(WaveSegment(
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
        ))
    
    return waves


# ════════════════════════════════════════════════════════════════
# بخش ۳: شناسایی موج خنثی (Neutral Wave)
# ════════════════════════════════════════════════════════════════

def calculate_wave_angle(wave: WaveSegment) -> float:
    """
    محاسبه زاویه موج (بر حسب درجه).
    
    زاویه ۰ درجه = کاملاً افقی (حرکت در زمان بدون تغییر قیمت)
    زاویه ۹۰ درجه = کاملاً عمودی (حرکت در قیمت بدون گذر زمان)
    
    عکس ۴۴.jpg: "این حرکت «افقی» واجد شرایط است" - زاویه کمتر از ۴۵ درجه
    """
    if wave.duration == 0:
        return 90.0  # عمودی کامل
    
    # نسبت تغییر قیمت به تغییر زمان
    slope = wave.price_range / wave.duration
    
    # تبدیل به زاویه (arctan)
    angle_rad = math.atan(slope)
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg


def is_in_first_quadrant(wave: WaveSegment, prev_wave: WaveSegment) -> bool:
    """
    بررسی اینکه موج خنثی در ربع اول دستگاه مختصات قرار دارد یا خیر.
    
    عکس ۴۳.jpg: "قانون زمانی کاربرد دارد که این موج در ربع اول دستگاه مختصات
    قرار گیرد نه حتی منطبق بر خط ۴۵ درجه"
    
    ربع اول = محور X (زمان) مثبت، محور Y (قیمت) مثبت
    در اینجا منظور: موج در فاز صعودی قرار دارد و زمان مثبت است
    """
    # موج باید صعودی باشد (قیمت افزایش یابد)
    if wave.direction != 1:
        return False
    
    # موج باید زمان مثبت داشته باشد (که همیشه دارد)
    return True


def is_aligned_with_next(wave: WaveSegment, next_wave: WaveSegment) -> bool:
    """
    بررسی هم‌راستایی موج خنثی با موج بعد از خود.
    
    عکس ۴۳.jpg: "موج خنثی در هر دو جنبه قانون، بایستی هم راستا با موج بعد از خود باشد"
    """
    return wave.direction == next_wave.direction


def identify_neutral_wave(
    w1: WaveSegment,
    w2: WaveSegment,
    w3: WaveSegment
) -> Optional[NeutralWave]:
    """
    شناسایی اینکه آیا موج دوم (w2) یک موج خنثی است یا خیر.
    
    شرایط (از عکس ۴۳.jpg و ۴۴.jpg):
    1. موج دوم باید افقی باشد (زاویه < ۴۵ درجه)
    2. باید در ربع اول دستگاه مختصات قرار گیرد
    3. باید هم‌راستا با موج بعد از خود (w3) باشد
    
    همچنین باید مشخص شود که موج دوم دو موج خلاف جهت را جدا می‌کند
    (جنبه اول) یا دو موج هم جهت را (جنبه دوم).
    """
    # ── شرط ۱: موج دوم باید افقی باشد ──────────────────────────
    angle = calculate_wave_angle(w2)
    is_horizontal = angle < 45.0
    
    if not is_horizontal:
        return None
    
    # ── شرط ۲: باید در ربع اول باشد (صعودی) ───────────────────
    in_first_quadrant = is_in_first_quadrant(w2, w1)
    
    # ── شرط ۳: باید هم‌راستا با موج بعد باشد ─────────────────
    aligned_with_next = is_aligned_with_next(w2, w3)
    
    if not aligned_with_next:
        return None
    
    # ── تشخیص جنبه (صفحه ۴۵) ─────────────────────────────────
    # جنبه اول: موج قبل و بعد خلاف جهت
    # جنبه دوم: موج قبل و بعد هم جهت
    if w1.direction != w3.direction:
        aspect = NeutralityAspect.ASPECT_1
    else:
        aspect = NeutralityAspect.ASPECT_2
    
    return NeutralWave(
        wave=w2,
        angle_degrees=round(angle, 2),
        is_horizontal=is_horizontal,
        in_first_quadrant=in_first_quadrant,
        aligned_with_next=aligned_with_next,
        aspect=aspect
    )


# ════════════════════════════════════════════════════════════════
# بخش ۴: اعمال جنبه اول قانون خنثایی
# ════════════════════════════════════════════════════════════════

def apply_aspect_1(
    w1: WaveSegment,
    w2: WaveSegment,
    w3: WaveSegment,
    trend_line_touch: bool = False
) -> NeutralityResult:
    """
    اعمال جنبه اول قانون خنثایی.
    
    عکس ۴۵.jpg و ۴۶.jpg و ۴۸.jpg:
    "اگر موج قبل و بعد از موج خنثی خلاف جهت هم باشند"
    
    قوانین (صفحه ۴۵):
    1. موج اول و دوم با هم به صورت یک تک موج در نظر گرفته می‌شوند
    2. اگر انتهای موج اول پیش از آنکه به میزان ۶۱.۸٪ (توسط مجموع موج دوم و سوم)
       اصلاح شود، شکسته شود، موج دوم و سوم را به صورت تک موج در نظر بگیرید
    3. اگر موج دوم بیش از ۳۸.۲٪ موج اول را بازگشت کرده باشد، احتمالاً بهتر است
       موج دوم و سوم را به صورت تک موج در نظر بگیرید
    4. روش ساده‌تر: اگر خط روند توسط موج مشکوک به خنثی لمس شود،
       انتهای آن را به عنوان انتهای موج پیشین در نظر بگیرید
    
    پارامترها:
        w1: موج قبل از موج خنثی
        w2: موج خنثی (مشکوک)
        w3: موج بعد از موج خنثی
        trend_line_touch: آیا خط روند توسط موج خنثی لمس شده؟
    
    خروجی:
        NeutralityResult
    """
    # ── محاسبه نسبت‌های فیبوناچی ──────────────────────────────
    # نسبت اصلاح موج دوم نسبت به موج اول
    retrace_w2_w1 = w2.price_range / w1.price_range if w1.price_range > 0 else 0
    
    # مجموع موج دوم و سوم
    total_w2_w3 = w2.price_range + w3.price_range
    
    # نسبت اصلاح کل موج دوم و سوم نسبت به موج اول
    retrace_total_w2w3_w1 = total_w2_w3 / w1.price_range if w1.price_range > 0 else 0
    
    # ── قانون ۴: بررسی خط روند (ساده‌ترین روش) ────────────────
    if trend_line_touch:
        return NeutralityResult(
            aspect=NeutralityAspect.ASPECT_1,
            decision=NeutralityDecision.ADJUST_ENDPOINT,
            new_wave_start_idx=w1.start_idx,
            new_wave_end_idx=w2.end_idx,
            new_wave_start_price=w1.start_price,
            new_wave_end_price=w2.end_price,
            adjusted_endpoint_idx=w2.end_idx,
            adjusted_endpoint_price=w2.end_price,
            reason="لمس خط روند توسط موج خنثی - نقطه پایان موج پیشین تعدیل شد",
            confidence=0.85
        )
    
    # ── قانون ۲: بررسی شرط ۶۱.۸٪ ──────────────────────────────
    # اگر انتهای موج اول قبل از اصلاح ۶۱.۸٪ توسط مجموع موج دوم و سوم شکسته شود
    # توجه: "شکسته شود" به معنی عبور قیمت از انتهای موج اول است
    # در اینجا، اگر موج سوم از انتهای موج اول عبور کند
    exceeds_w1_end = (w3.direction == 1 and w3.end_price > w1.end_price) or \
                     (w3.direction == -1 and w3.end_price < w1.end_price)
    
    if exceeds_w1_end and retrace_total_w2w3_w1 < 0.618:
        return NeutralityResult(
            aspect=NeutralityAspect.ASPECT_1,
            decision=NeutralityDecision.MERGE_W2_W3,
            new_wave_start_idx=w2.start_idx,
            new_wave_end_idx=w3.end_idx,
            new_wave_start_price=w2.start_price,
            new_wave_end_price=w3.end_price,
            adjusted_endpoint_idx=None,
            adjusted_endpoint_price=None,
            reason=f"موج اول قبل از اصلاح {retrace_total_w2w3_w1*100:.1f}% (<61.8%) شکسته شد - ادغام موج دوم و سوم",
            confidence=0.9
        )
    
    # ── قانون ۳: بررسی شرط ۳۸.۲٪ ──────────────────────────────
    # اگر موج دوم بیش از ۳۸.۲٪ موج اول را بازگشت کرده باشد
    if retrace_w2_w1 > 0.382:
        return NeutralityResult(
            aspect=NeutralityAspect.ASPECT_1,
            decision=NeutralityDecision.MERGE_W2_W3,
            new_wave_start_idx=w2.start_idx,
            new_wave_end_idx=w3.end_idx,
            new_wave_start_price=w2.start_price,
            new_wave_end_price=w3.end_price,
            adjusted_endpoint_idx=None,
            adjusted_endpoint_price=None,
            reason=f"موج دوم {retrace_w2_w1*100:.1f}% از موج اول را بازگشت کرده (>38.2%) - ادغام موج دوم و سوم",
            confidence=0.75
        )
    
    # ── قانون ۱ (پیش‌فرض): موج اول و دوم را با هم ادغام کن ────
    return NeutralityResult(
        aspect=NeutralityAspect.ASPECT_1,
        decision=NeutralityDecision.MERGE_W1_W2,
        new_wave_start_idx=w1.start_idx,
        new_wave_end_idx=w2.end_idx,
        new_wave_start_price=w1.start_price,
        new_wave_end_price=w2.end_price,
        adjusted_endpoint_idx=None,
        adjusted_endpoint_price=None,
        reason="شرط پیش‌فرض جنبه اول - ادغام موج اول و دوم به صورت یک تک موج",
        confidence=0.7
    )


# ════════════════════════════════════════════════════════════════
# بخش ۵: اعمال جنبه دوم قانون خنثایی
# ════════════════════════════════════════════════════════════════

def apply_aspect_2(
    w1: WaveSegment,
    w2: WaveSegment,
    w3: WaveSegment,
    trend_line_touch: bool = False
) -> NeutralityResult:
    """
    اعمال جنبه دوم قانون خنثایی.
    
    عکس ۴۵.jpg و ۴۷.jpg و ۴۸.jpg:
    "اگر موج قبل و بعد موج دوم در جهت هم باشند"
    
    قوانین (صفحه ۴۵):
    1. می‌توان هر سه موج را با هم به صورت یک تک موج در نظر گرفت
       یا اینکه به صورت سه موج مجزا در نظر گرفت
    2. اگر موج دوم بیش از یک واحد زمانی را به خود اختصاص دهد،
       بایستی موج اول و دوم مجزا در نظر گرفته شوند
    3. روش ساده‌تر: اگر خط روند توسط موج مشکوک به خنثی لمس شود،
       انتهای آن را به عنوان انتهای موج پیشین در نظر بگیرید
    
    پارامترها:
        w1: موج قبل از موج خنثی
        w2: موج خنثی (مشکوک)
        w3: موج بعد از موج خنثی
        trend_line_touch: آیا خط روند توسط موج خنثی لمس شده؟
    
    خروجی:
        NeutralityResult
    """
    # ── قانون ۳: بررسی خط روند (ساده‌ترین روش) ────────────────
    if trend_line_touch:
        return NeutralityResult(
            aspect=NeutralityAspect.ASPECT_2,
            decision=NeutralityDecision.ADJUST_ENDPOINT,
            new_wave_start_idx=w1.start_idx,
            new_wave_end_idx=w2.end_idx,
            new_wave_start_price=w1.start_price,
            new_wave_end_price=w2.end_price,
            adjusted_endpoint_idx=w2.end_idx,
            adjusted_endpoint_price=w2.end_price,
            reason="لمس خط روند توسط موج خنثی - نقطه پایان موج پیشین تعدیل شد",
            confidence=0.85
        )
    
    # ── قانون ۲: بررسی شرط واحد زمانی ─────────────────────────
    # "اگر موج دوم بیش از یک واحد زمانی را به خود اختصاص دهد"
    # واحد زمانی = مدت زمان یک کندل (در اینجا duration > 1)
    if w2.duration > 1:
        return NeutralityResult(
            aspect=NeutralityAspect.ASPECT_2,
            decision=NeutralityDecision.KEEP_SEPARATE,
            new_wave_start_idx=w1.start_idx,
            new_wave_end_idx=w3.end_idx,
            new_wave_start_price=w1.start_price,
            new_wave_end_price=w3.end_price,
            adjusted_endpoint_idx=None,
            adjusted_endpoint_price=None,
            reason=f"موج دوم {w2.duration} واحد زمانی دارد (>1) - حفظ سه موج مجزا",
            confidence=0.8
        )
    
    # ── قانون ۱ (پیش‌فرض): دو گزینه ──────────────────────────
    # در جنبه دوم، دو انتخاب ممکن است:
    # گزینه A: ادغام هر سه موج
    # گزینه B: حفظ سه موج مجزا
    
    # بررسی جهت کلی حرکت
    total_direction = 1 if (w1.end_price + w3.end_price) > (w1.start_price + w3.start_price) else -1
    total_price_range = abs(w3.end_price - w1.start_price)
    total_duration = w3.end_idx - w1.start_idx
    
    # اگر حرکت کلی خیلی کوچک باشد، ادغام منطقی‌تر است
    if total_price_range < max(w1.price_range, w2.price_range, w3.price_range) * 0.5:
        return NeutralityResult(
            aspect=NeutralityAspect.ASPECT_2,
            decision=NeutralityDecision.MERGE_ALL_THREE,
            new_wave_start_idx=w1.start_idx,
            new_wave_end_idx=w3.end_idx,
            new_wave_start_price=w1.start_price,
            new_wave_end_price=w3.end_price,
            adjusted_endpoint_idx=None,
            adjusted_endpoint_price=None,
            reason="حرکت کلی کوچک - ادغام هر سه موج به صورت یک تک موج",
            confidence=0.6
        )
    
    # پیش‌فرض: حفظ سه موج مجزا
    return NeutralityResult(
        aspect=NeutralityAspect.ASPECT_2,
        decision=NeutralityDecision.KEEP_SEPARATE,
        new_wave_start_idx=w1.start_idx,
        new_wave_end_idx=w3.end_idx,
        new_wave_start_price=w1.start_price,
        new_wave_end_price=w3.end_price,
        adjusted_endpoint_idx=None,
        adjusted_endpoint_price=None,
        reason="پیش‌فرض جنبه دوم - حفظ سه موج مجزا (می‌توان به صورت یک موج نیز دید)",
        confidence=0.5
    )


# ════════════════════════════════════════════════════════════════
# بخش ۶: تابع اصلی تحلیل قانون خنثایی
# ════════════════════════════════════════════════════════════════

def analyze_neutrality(
    waves: List[WaveSegment],
    use_trend_line: bool = True
) -> List[NeutralityResult]:
    """
    تحلیل کامل قانون خنثایی روی تمام سه‌موجی‌های متوالی.
    
    برای هر سه موج متوالی (w1, w2, w3):
        1. بررسی می‌شود که آیا موج دوم موج خنثی است یا خیر
        2. اگر بله، جنبه مناسب تشخیص داده می‌شود
        3. قوانین مربوط به آن جنبه اعمال می‌شود
        4. نتیجه برگردانده می‌شود
    
    پارامترها:
        waves: لیست WaveSegment
        use_trend_line: آیا از روش ساده‌تر خط روند استفاده شود؟
    
    خروجی:
        لیست NeutralityResult
    """
    if len(waves) < 3:
        return []
    
    results = []
    
    # ── برای هر سه موج متوالی ─────────────────────────────────
    for i in range(len(waves) - 2):
        w1 = waves[i]
        w2 = waves[i + 1]
        w3 = waves[i + 2]
        
        # ── شناسایی موج خنثی ──────────────────────────────────
        neutral_wave = identify_neutral_wave(w1, w2, w3)
        
        if neutral_wave is None:
            continue
        
        # ── تشخیص لمس خط روند (در صورت نیاز) ──────────────────
        trend_line_touch = False
        if use_trend_line:
            # روش ساده‌تر: بررسی لمس خط روند
            # خط روند از High/قبلی در روند صعودی یا Low قبلی در روند نزولی
            if w1.direction == 1:  # روند صعودی
                # خط روند از قله قبلی
                trend_line_price = w1.end_price
                # آیا موج خنثی این خط را لمس کرده؟
                if neutral_wave.wave.direction == 1:
                    trend_line_touch = neutral_wave.wave.end_price >= trend_line_price
                else:
                    trend_line_touch = neutral_wave.wave.start_price >= trend_line_price
            else:  # روند نزولی
                trend_line_price = w1.end_price
                if neutral_wave.wave.direction == -1:
                    trend_line_touch = neutral_wave.wave.end_price <= trend_line_price
                else:
                    trend_line_touch = neutral_wave.wave.start_price <= trend_line_price
        
        # ── اعمال جنبه مناسب ──────────────────────────────────
        if neutral_wave.aspect == NeutralityAspect.ASPECT_1:
            result = apply_aspect_1(w1, w2, w3, trend_line_touch)
        else:
            result = apply_aspect_2(w1, w2, w3, trend_line_touch)
        
        results.append(result)
    
    return results


# ════════════════════════════════════════════════════════════════
# بخش ۷: تابع analyze (interface اصلی برای main.py)
# ════════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None, context=None) -> Dict:
    """
    فصل ۷: قانون خنثایی (Neutrality)
    
    پیاده‌سازی کامل مطابق صفحات ۴۳-۴۸ کتاب گلن نیلی.
    
    این تابع:
        ۱. موج‌ها را از داده استخراج می‌کند (مطابق فصل ۵)
        ۲. سه‌موجی‌های متوالی را بررسی می‌کند
        ۳. موج‌های خنثی (افقی) را شناسایی می‌کند
        ۴. جنبه اول یا دوم را تشخیص می‌دهد
        ۵. قوانین مربوطه را اعمال می‌کند
        ۶. نتیجه نهایی را برمی‌گرداند
    
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
    
    if n < 10:
        return {
            "عنوان": "فصل ۷: قانون خنثایی",
            "وضعیت": "داده_کافی_نیست",
            "تعداد_کندل": str(n),
            "پیام": "برای تحلیل قانون خنثایی حداقل ۱۰ کندل لازم است"
        }
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۲: استخراج موج‌ها (مطابق فصل ۵)
    # ════════════════════════════════════════════════════════════
    waves = []
    context_used = False

    if context and "chapter_5" in context:
        ch5 = context["chapter_5"]
        if "_monowaves" in ch5 and ch5["_monowaves"]:
            mono_list = ch5["_monowaves"]
            for idx, mw in enumerate(mono_list):
                direction = 1 if mw.direction.value == "UP" else -1
                start_type = "PEAK" if direction == 1 else "TROUGH"
                end_type = "TROUGH" if direction == 1 else "PEAK"
            
                wave = WaveSegment(
                    index=idx,
                    start_idx=mw.start_bar,
                    end_idx=mw.end_bar,
                    start_price=mw.start_price,
                    end_price=mw.end_price,
                    direction=direction,
                    price_range=mw.price_range,
                    duration=mw.duration,
                    start_type=start_type,
                    end_type=end_type,
                )
                waves.append(wave)
            context_used = True

    # اگر از context دریافت نشد، خودمان استخراج می‌کنیم
    if not waves:
        waves = extract_wave_segments(high, low, close, order=2)
    
    if len(waves) < 3:
        return {
            "عنوان": "فصل ۷: قانون خنثایی",
            "وضعیت": "موج_کافی_نیست",
            "تعداد_موج": str(len(waves)),
            "پیام": "برای قانون خنثایی حداقل ۳ موج لازم است"
        }
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۳: تحلیل قانون خنثایی
    # ════════════════════════════════════════════════════════════
    results_list = analyze_neutrality(waves, use_trend_line=True)
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۴: آمارگیری
    # ════════════════════════════════════════════════════════════
    aspect_1_count = sum(1 for r in results_list if r.aspect == NeutralityAspect.ASPECT_1)
    aspect_2_count = sum(1 for r in results_list if r.aspect == NeutralityAspect.ASPECT_2)
    
    merge_w1_w2_count = sum(1 for r in results_list if r.decision == NeutralityDecision.MERGE_W1_W2)
    merge_w2_w3_count = sum(1 for r in results_list if r.decision == NeutralityDecision.MERGE_W2_W3)
    merge_all_count = sum(1 for r in results_list if r.decision == NeutralityDecision.MERGE_ALL_THREE)
    keep_separate_count = sum(1 for r in results_list if r.decision == NeutralityDecision.KEEP_SEPARATE)
    adjust_endpoint_count = sum(1 for r in results_list if r.decision == NeutralityDecision.ADJUST_ENDPOINT)
    
    # ── محاسبه میانگین زاویه موج‌های خنثی ─────────────────────
    neutral_angles = []
    for i in range(len(waves) - 2):
        w2 = waves[i + 1]
        angle = calculate_wave_angle(w2)
        if angle < 45:  # افقی
            neutral_angles.append(angle)
    
    avg_neutral_angle = np.mean(neutral_angles) if neutral_angles else 0
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۵: ساخت خروجی
    # ════════════════════════════════════════════════════════════
    results = {
        # ── شناسنامه ──
        "عنوان": "فصل ۷: قانون خنثایی (Neutrality)",
        "مرجع_کتاب": "صفحات ۴۳-۴۸ - گلن نیلی",
        "وضعیت": "تحلیل_کامل",
        
        # ── اطلاعات پایه ──
        "تعداد_کندل": str(n),
        "تعداد_موج_استخراج‌شده": str(len(waves)),
        
        # ── آمار موج‌های خنثی ──
        "تعداد_سه‌موجی_بررسی‌شده": str(len(waves) - 2),
        "تعداد_موج_خنثی_شناسایی‌شده": str(len(results_list)),
        "درصد_موج_خنثی": f"{len(results_list) / max(1, len(waves)-2) * 100:.1f}%",
        "میانگین_زاویه_موج_خنثی": f"{avg_neutral_angle:.1f}°",
        "شرط_افقی_بودن": "زاویه < ۴۵ درجه (عکس ۴۴.jpg)",
        
        # ── توزیع جنبه‌ها ──
        "تعداد_جنبه_اول": str(aspect_1_count),
        "تعداد_جنبه_دوم": str(aspect_2_count),
        "جنبه_اول_شرط": "موج قبل و بعد خلاف جهت (عکس ۴۵.jpg)",
        "جنبه_دوم_شرط": "موج قبل و بعد هم جهت (عکس ۴۵.jpg)",
        
        # ── تصمیمات اعمال‌شده ──
        "تعداد_ادغام_موج_اول_و_دوم": str(merge_w1_w2_count),
        "تعداد_ادغام_موج_دوم_و_سوم": str(merge_w2_w3_count),
        "تعداد_ادغام_سه_موج_با_هم": str(merge_all_count),
        "تعداد_حفظ_سه_موج_جداگانه": str(keep_separate_count),
        "تعداد_تعدیل_نقطه_پایانی": str(adjust_endpoint_count),
        
        # ── قوانین فیبوناچی جنبه اول (عکس ۴۶.jpg) ──
        "قانون_61_8_درصد": "اگر انتهای موج اول قبل از اصلاح ۶۱.۸٪ توسط مجموع موج دوم و سوم شکسته شود، موج دوم و سوم را ادغام کن",
        "قانون_38_2_درصد": "اگر موج دوم بیش از ۳۸.۲٪ موج اول را بازگشت کرده باشد، موج دوم و سوم را ادغام کن",
        
        # ── قوانین جنبه دوم (عکس ۴۷.jpg) ──
        "قانون_واحد_زمانی": "اگر موج دوم بیش از یک واحد زمانی را به خود اختصاص دهد، موج اول و دوم مجزا در نظر گرفته شوند",
        "قانون_خط_روند": "اگر خط روند توسط موج مشکوک به خنثی لمس شود، انتهای آن را به عنوان انتهای موج پیشین در نظر بگیرید",
        
        # ── شرایط اولیه از عکس ۴۳.jpg ──
        "شرط_ربع_اول": "موج خنثی باید در ربع اول دستگاه مختصات قرار گیرد (نه حتی منطبق بر خط ۴۵ درجه)",
        "شرط_هم_راستایی": "موج خنثی باید هم‌راستا با موج بعد از خود باشد",
        "نکته_تایم_فریم_پایین‌تر": "بهتر است برای تأیید به تایم فریم پایین‌تر مراجعه شود",
        
        # ── اصول کلیدی ──
        "اصل_جنبه_اول_1": "موج اول و دوم با هم یک تک موج (عکس ۴۸.jpg)",
        "اصل_جنبه_دوم_1": "هر سه موج با هم یک تک موج یا سه موج مجزا (عکس ۴۸.jpg)",
    }
    
    # ── اضافه کردن جزئیات ۵ نتیجه اول ──────────────────────────
    for idx, res in enumerate(results_list[:5]):
        prefix = f"نتیجه_{idx + 1}"
        results[f"{prefix}_جنبه"] = res.aspect.value
        results[f"{prefix}_تصمیم"] = res.decision.value
        results[f"{prefix}_دلیل"] = res.reason
        results[f"{prefix}_اطمینان"] = f"{res.confidence * 100:.0f}%"
    
    # ── تفسیر نهایی ──
    results["تفسیر_نهایی"] = _build_final_interpretation(
        results, results_list, avg_neutral_angle,
        aspect_1_count, aspect_2_count
    )
    
    # ── ثبت در لاگ ──
    if logger:
        _write_to_logger(logger, results, results_list, waves)
    
    return results


# ════════════════════════════════════════════════════════════════
# بخش ۸: تفسیر نهایی
# ════════════════════════════════════════════════════════════════

def _build_final_interpretation(
    results: Dict,
    results_list: List[NeutralityResult],
    avg_neutral_angle: float,
    aspect_1_count: int,
    aspect_2_count: int
) -> str:
    """تولید تفسیر متنی کامل قانون خنثایی مطابق کتاب"""
    
    total_found = len(results_list)
    
    if total_found == 0:
        return f"""
═══════════════════════════════════════════════════════════════════
  فصل ۷: قانون خنثایی (Neutrality) - صفحات ۴۳ تا ۴۸
  مرجع: گلن نیلی | سبک نئوویو
═══════════════════════════════════════════════════════════════════

📐 ✅ قانون خنثایی - هیچ موج خنثی شناسایی نشد

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 نتیجه بررسی:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • سه‌موجی‌های بررسی‌شده: {results.get('تعداد_سه‌موجی_بررسی‌شده', '۰')}
  • موج خنثی شناسایی‌شده: ۰
  • میانگین زاویه موج‌ها: {avg_neutral_angle:.1f}°

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 شرایط شناسایی موج خنثی (عکس ۴۳.jpg و ۴۴.jpg):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {results.get('شرط_ربع_اول', '')}
  {results.get('شرط_هم_راستایی', '')}
  {results.get('شرط_افقی_بودن', '')}

💡 نتیجه نئوویو:
   هیچ موج خنثی در داده‌های فعلی شناسایی نشد.
   موج‌ها به صورت استاندارد و بدون نیاز به تعدیل هستند.
═══════════════════════════════════════════════════════════════════
"""
    
    # تعیین جنبه غالب
    if aspect_1_count > aspect_2_count:
        dominant_aspect = "جنبه اول"
        aspect_desc = "موج قبل و بعد خلاف جهت هستند"
    else:
        dominant_aspect = "جنبه دوم"
        aspect_desc = "موج قبل و بعد هم جهت هستند"
    
    return f"""
═══════════════════════════════════════════════════════════════════
  فصل ۷: قانون خنثایی (Neutrality) - صفحات ۴۳ تا ۴۸
  مرجع: گلن نیلی | سبک نئوویو
═══════════════════════════════════════════════════════════════════

📐 ⚠️ قانون خنثایی - {total_found} موج خنثی شناسایی شد

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 نتیجه بررسی:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • سه‌موجی‌های بررسی‌شده: {results.get('تعداد_سه‌موجی_بررسی‌شده', '۰')}
  • موج خنثی شناسایی‌شده: {total_found}
  • میانگین زاویه موج خنثی: {avg_neutral_angle:.1f}°
  • جنبه اول (خلاف جهت): {aspect_1_count} مورد
  • جنبه دوم (هم جهت): {aspect_2_count} مورد
  • جنبه غالب: {dominant_aspect} ({aspect_desc})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 تصمیمات اعمال‌شده:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • ادغام موج اول و دوم: {results.get('تعداد_ادغام_موج_اول_و_دوم', '۰')}
  • ادغام موج دوم و سوم: {results.get('تعداد_ادغام_موج_دوم_و_سوم', '۰')}
  • ادغام سه موج با هم: {results.get('تعداد_ادغام_سه_موج_با_هم', '۰')}
  • حفظ سه موج جداگانه: {results.get('تعداد_حفظ_سه_موج_جداگانه', '۰')}
  • تعدیل نقطه پایانی: {results.get('تعداد_تعدیل_نقطه_پایانی', '۰')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 قوانین فیبوناچی جنبه اول (عکس ۴۶.jpg):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {results.get('قانون_61_8_درصد', '')}
  {results.get('قانون_38_2_درصد', '')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 قوانین جنبه دوم (عکس ۴۷.jpg):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {results.get('قانون_واحد_زمانی', '')}
  {results.get('قانون_خط_روند', '')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 جزئیات نتایج:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    + "\n".join([
        f"  {i+1}. {res.decision.value} | {res.reason} | اطمینان: {res.confidence*100:.0f}%"
        for i, res in enumerate(results_list[:5])
    ]) + f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 نتیجه نئوویو:
   {total_found} موج خنثی در داده‌ها شناسایی شد.
   طبق قانون خنثایی، این موج‌ها باید بازنگری و تعدیل شوند.
   {'جنبه اول غالب است - موج قبل و بعد خلاف جهت' if aspect_1_count > aspect_2_count else 'جنبه دوم غالب است - موج قبل و بعد هم جهت'}
   
📌 نکته (صفحه ۴۳):
   "این کره‌ها در معرض بازنگری هستند اگر حرکت قیمت تحت شمول
    قانون خنثایی قرار گیرد. وقتی این قانون لحاظ شده - و در جای
    مناسب به کار بسته شده - باشد، وضعیت نقاط نهایی شده تلقی خواهد شد."

═══════════════════════════════════════════════════════════════════
"""


# ════════════════════════════════════════════════════════════════
# بخش ۹: ثبت در لاگ
# ════════════════════════════════════════════════════════════════

def _write_to_logger(
    logger,
    results: Dict,
    results_list: List[NeutralityResult],
    waves: List[WaveSegment]
):
    """ثبت نتایج در لاگر"""
    logger.add_section("فصل ۷: قانون خنثایی (Neutrality)", level=1)
    logger.add_result("مرجع کتاب", "صفحات ۴۳-۴۸ - گلن نیلی")
    logger.add_result("تعداد کندل", results["تعداد_کندل"])
    logger.add_result("تعداد موج", results["تعداد_موج_استخراج‌شده"])
    logger.add_result("موج خنثی شناسایی‌شده", results["تعداد_موج_خنثی_شناسایی‌شده"])
    logger.add_result("میانگین زاویه موج خنثی", results["میانگین_زاویه_موج_خنثی"])
    logger.add_result("جنبه اول", results["تعداد_جنبه_اول"])
    logger.add_result("جنبه دوم", results["تعداد_جنبه_دوم"])
    
    logger.add_section("جزئیات نتایج", level=2)
    for i, res in enumerate(results_list[:10]):
        logger.add_result(
            f"نتیجه {i+1}",
            f"{res.decision.value} - {res.reason} (اطمینان: {res.confidence*100:.0f}%)"
        )
    
    logger.add_section("قوانین صفحه ۴۳-۴۸", level=2)
    logger.add_result("شرط ربع اول", results["شرط_ربع_اول"])
    logger.add_result("شرط هم‌راستایی", results["شرط_هم_راستایی"])
    logger.add_result("شرط افقی بودن", results["شرط_افقی_بودن"])
    logger.add_result("جنبه اول", results["جنبه_اول_شرط"])
    logger.add_result("جنبه دوم", results["جنبه_دوم_شرط"])
    logger.add_result("قانون ۶۱.۸٪", results["قانون_61_8_درصد"])
    logger.add_result("قانون ۳۸.۲٪", results["قانون_38_2_درصد"])
    logger.add_result("قانون واحد زمانی", results["قانون_واحد_زمانی"])
    logger.add_result("قانون خط روند", results["قانون_خط_روند"])
    
    logger.add_result("تفسیر نهایی", results["تفسیر_نهایی"])


# ════════════════════════════════════════════════════════════════
# اجرای مستقیم برای تست
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # ایجاد داده تست
    test_data = pd.DataFrame({
        "close": [100, 102, 101, 100.5, 101, 101.5, 102, 103, 102, 104, 103, 105],
        "high": [101, 103, 102, 101, 102, 102, 103, 104, 103, 105, 104, 106],
        "low": [99, 101, 100, 100, 100, 101, 101, 102, 101, 103, 102, 104],
        "open": [100, 102, 101, 100.5, 101, 101.5, 102, 103, 102, 104, 103, 105],
    })
    
    result = analyze(test_data)
    print(result["تفسیر_نهایی"])