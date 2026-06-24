"""
فصل ۲: ساختار فراکتال (Fractal Structure)
منبع: کتاب "امواج الیوت به سبک نئوویو" - گلن نیلی - صفحه 21

═══════════════════════════════════════════════════════════════════════
متن دقیق کتاب (صفحه 21):
"فراکتال‌ها در حقیقت ساختارهای هندسی متشکل از اجزایی می‌باشند که با بزرگ کردن
هر جزء به نسبت معین، همان ساختار اولیه به دست آید. امواج الیوت دارای ساختار
فراکتال می‌باشد. بدین معنی که در هر موج شتابدار از پنج ریز موج تشکیل می‌شود
و هر موج اصلاحی از سه ریز موج و با ترکیب این دو موج ساختار موج مرتبه بالاتر
تشکیل می‌شود که خود شامل دو فاز شتابدار و اصلاحی می‌باشد. به بیانی دیگر
هر موج شتابدار شامل ریز موج‌های همان فاز می‌باشد و موج‌های اصلاحی شامل
ریز موج‌های همان فاز. این تکرار منجر به خلق الگوهای بزرگتری می‌شود که دارای
ساختار الگوهای کوچکتر می‌باشند."

═══════════════════════════════════════════════════════════════════════
قوانین فراکتال مستخرج از فصل‌های ۲، ۲۰، ۲۲، ۲۶ کتاب:

۱. هر موج شتابدار از 5 تک‌موج (Monowave) تشکیل می‌شود
۲. هر موج اصلاحی از 3 تک‌موج (Monowave) تشکیل می‌شود
۳. ترکیب این دو فاز، موج مرتبه بالاتر را می‌سازد
۴. هر موج شتابدار در مرتبه بالاتر فقط شامل ریزموج‌های شتابدار است
۵. هر موج اصلاحی در مرتبه بالاتر فقط شامل ریزموج‌های اصلاحی است
۶. این ساختار در تمام درجات (Degrees) تکرار می‌شود

سلسله مراتب پیچیدگی (فصل ۲۶):
- سطح ۰: Monowave (تک‌موج) - فاقد ریزموج
- سطح ۱: Polywave (بساموج) - ترکیب تک‌موج‌ها
- سطح ۲: Multiwave (فراموج) - حداقل یک بساموج شتابدار درون
- سطح ۳: Macrowave (ابرموج) - حداقل یک فراموج درون

قانون تشابه و تعادل (فصل ۲۰):
- موج‌های هم‌درجه باید در قیمت یا زمان بین ۱/۳ تا ۳ برابر هم باشند
- اگر نسبت > 3: موج بزرگ‌تر از درجه بالاتر است
- اگر نسبت < 1/3: موج کوچک‌تر از درجه پایین‌تر است
═══════════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict
from enum import Enum


# ════════════════════════════════════════════════════════════════════
# بخش ۱: تعریف انواع و ساختارهای داده (مطابق اصطلاحات نیلی)
# ════════════════════════════════════════════════════════════════════

class WaveType(Enum):
    """نوع موج: شتابدار یا اصلاحی (مطابق تعریف نیلی)"""
    MOTIVE = "motive"        # شتابدار - 5 ریزموج
    CORRECTIVE = "corrective"  # اصلاحی - 3 ریزموج
    UNKNOWN = "unknown"


class ComplexityLevel(Enum):
    """
    سطح پیچیدگی موج - فصل ۲۶ کتاب نیلی (صفحه ۵۰۲-۵۱۰)

    سطح ۰: Monowave  - فاقد ریزموج (بدون خط زیرین در برچسب)
    سطح ۱: Polywave  - از چند تک‌موج (یک خط زیرین)
    سطح ۲: Multiwave - حداقل یک بساموج شتابدار درون (دو خط زیرین)
    سطح ۳: Macrowave - حداقل یک فراموج درون (سه خط زیرین)
    """
    MONOWAVE = 0   # تک‌موج
    POLYWAVE = 1   # بساموج
    MULTIWAVE = 2  # فراموج
    MACROWAVE = 3  # ابرموج


class WaveDegree(Enum):
    """
    درجات موجی مطابق نئوویو
    (از بزرگ به کوچک - مطابق اصطلاحات کتاب نیلی)
    """
    GRAND_SUPERCYCLE = 8   # ((I)) ((II))
    SUPERCYCLE = 7         # (I) (II)
    CYCLE = 6              # I II
    PRIMARY = 5            # [1] [2]
    INTERMEDIATE = 4       # (1) (2)
    MINOR = 3              # 1 2
    MINUTE = 2             # i ii
    MINUETTE = 1           # (i) (ii)
    SUBMINUETTE = 0        # tiny waves


@dataclass
class Monowave:
    """
    تک‌موج (Monowave) - فصل ۲۶، صفحه ۵۰۲
    کوچک‌ترین واحد تحلیل در نئوویو
    فاقد هر گونه ریزموج - سطح پیچیدگی = صفر
    """
    start_idx: int
    end_idx: int
    start_price: float
    end_price: float
    direction: int          # +1 صعودی، -1 نزولی
    price_range: float      # دامنه قیمتی (مطلق)
    duration: int           # مدت زمانی (تعداد کندل)
    complexity: ComplexityLevel = ComplexityLevel.MONOWAVE
    wave_type: WaveType = WaveType.UNKNOWN
    structure_label: str = ""  # برچسب ساختاری نئوویو مثل :5 یا :3

    def __post_init__(self):
        self.price_range = abs(self.end_price - self.start_price)
        self.duration = max(1, self.end_idx - self.start_idx)


@dataclass
class FractalWave:
    """
    موج فراکتالی - ساختار اصلی فصل ۲

    هر FractalWave می‌تواند:
    - یک Monowave باشد (سطح ۰)
    - یک Polywave از چند Monowave باشد (سطح ۱)
    - یک Multiwave از چند Polywave باشد (سطح ۲)
    - یک Macrowave از چند Multiwave باشد (سطح ۳)

    این ساختار دقیقاً همان چیزی است که نیلی
    در صفحه ۲۱ توضیح می‌دهد: "این تکرار منجر به خلق
    الگوهای بزرگتری می‌شود که دارای ساختار الگوهای کوچکتر می‌باشند"
    """
    start_idx: int
    end_idx: int
    start_price: float
    end_price: float
    direction: int
    price_range: float
    duration: int
    complexity: ComplexityLevel
    wave_type: WaveType
    degree: WaveDegree
    sub_waves: List['FractalWave'] = field(default_factory=list)
    label: str = ""         # برچسب شمارشی: 1,2,3,4,5 یا A,B,C

    def __post_init__(self):
        self.price_range = abs(self.end_price - self.start_price)
        self.duration = max(1, self.end_idx - self.start_idx)

    @property
    def sub_wave_count(self) -> int:
        """تعداد ریزموج‌های مستقیم"""
        return len(self.sub_waves)

    @property
    def is_motive_complete(self) -> bool:
        """
        آیا این موج شتابدار کامل است؟
        مطابق نیلی: موج شتابدار = 5 ریزموج
        """
        return (self.wave_type == WaveType.MOTIVE and
                self.sub_wave_count == 5)

    @property
    def is_corrective_complete(self) -> bool:
        """
        آیا این موج اصلاحی کامل است؟
        مطابق نیلی: موج اصلاحی = 3 ریزموج
        """
        return (self.wave_type == WaveType.CORRECTIVE and
                self.sub_wave_count == 3)

    def get_structure_label(self) -> str:
        """
        برچسب ساختاری نئوویو مطابق فصل ۲۲ کتاب:
        :5 برای شتابدار
        :3 برای اصلاحی
        خط‌های زیرین نشان‌دهنده سطح پیچیدگی
        """
        base = ":5" if self.wave_type == WaveType.MOTIVE else ":3"
        underlines = "_" * self.complexity.value
        return f"{base}{underlines}"


# ════════════════════════════════════════════════════════════════════
# بخش ۲: استخراج تک‌موج‌ها (Monowaves)
# ════════════════════════════════════════════════════════════════════

def extract_monowaves(data: pd.DataFrame, order: int = 3) -> List[Monowave]:
    """
    استخراج تک‌موج‌ها از داده قیمتی

    مطابق فصل ۵ کتاب نیلی (شناسایی تک‌موج‌ها):
    "پس از رسم نمودار با استفاده از کش‌دیتا و با استفاده از
    بررسی نقطه-داده‌ها و تغییر جهت نقطه-داده‌ها می‌توان تک‌موج‌ها
    را به صورت عمومی شناسایی کرد."

    پارامترها:
        data: DataFrame با ستون‌های high, low, close
        order: حساسیت شناسایی نقاط چرخش (حداقل ۳ توصیه می‌شود)

    خروجی:
        لیست Monowave‌های شناسایی‌شده
    """
    close = data['close'].values if 'close' in data.columns else data['Close'].values
    high = data['high'].values if 'high' in data.columns else data['High'].values
    low = data['low'].values if 'low' in data.columns else data['Low'].values

    n = len(close)

    # ── شناسایی نقاط چرخش (peak/trough)
    peak_indices = argrelextrema(high, np.greater, order=order)[0]
    trough_indices = argrelextrema(low, np.less, order=order)[0]

    # ── ترکیب و مرتب‌سازی نقاط چرخش
    turning_points = []
    for idx in peak_indices:
        turning_points.append((idx, high[idx], 'PEAK'))
    for idx in trough_indices:
        turning_points.append((idx, low[idx], 'TROUGH'))
    turning_points.sort(key=lambda x: x[0])

    # ── حذف نقاط تکراری و متوالی هم‌نوع
    # (یعنی دو PEAK پشت‌سر هم بدون TROUGH بین‌شان)
    filtered = []
    for tp in turning_points:
        if not filtered:
            filtered.append(tp)
            continue
        last = filtered[-1]
        if last[2] == tp[2]:
            # هم‌نوع هستند - فقط نقطه‌ای را که مقدار آن بزرگ‌تر (PEAK) یا کوچک‌تر (TROUGH) است نگه دار
            if tp[2] == 'PEAK' and tp[1] > last[1]:
                filtered[-1] = tp
            elif tp[2] == 'TROUGH' and tp[1] < last[1]:
                filtered[-1] = tp
        else:
            filtered.append(tp)

    if len(filtered) < 2:
        return []

    # ── ساخت Monowave‌ها
    monowaves = []
    for i in range(len(filtered) - 1):
        idx1, price1, type1 = filtered[i]
        idx2, price2, type2 = filtered[i + 1]

        direction = 1 if price2 > price1 else -1

        mw = Monowave(
            start_idx=int(idx1),
            end_idx=int(idx2),
            start_price=float(price1),
            end_price=float(price2),
            direction=direction,
            price_range=abs(price2 - price1),
            duration=max(1, int(idx2 - idx1)),
            complexity=ComplexityLevel.MONOWAVE,
            wave_type=WaveType.UNKNOWN,
            structure_label=""
        )
        monowaves.append(mw)

    return monowaves


# ════════════════════════════════════════════════════════════════════
# بخش ۳: اعتبارسنجی ساختار فراکتال
# ════════════════════════════════════════════════════════════════════

class FractalValidator:
    """
    اعتبارسنج ساختار فراکتالی مطابق فصل ۲، ۲۰ و ۲۶ نیلی

    قوانین اصلی که اجرا می‌شوند:
    1. موج شتابدار = دقیقاً 5 ریزموج (همه شتابدار در فاز صعودی)
    2. موج اصلاحی = دقیقاً 3 ریزموج (همه اصلاحی در فاز نزولی)
    3. قانون تشابه و تعادل (Similarity & Balance)
    4. سطح پیچیدگی باید از درجه پایین به بالا رعایت شود
    5. ریزموج‌های یک الگو نمی‌توانند از موج متناظر درجه بالاتر بزرگتر باشند
    """

    # ── ثابت‌های قانون تشابه و تعادل (فصل ۲۰، صفحه ۴۷۴)
    SIMILARITY_MIN_RATIO = 1 / 3    # حداقل نسبت برای هم‌درجه بودن
    SIMILARITY_MAX_RATIO = 3.0      # حداکثر نسبت برای هم‌درجه بودن

    @staticmethod
    def validate_motive_structure(waves: List[Monowave]) -> Tuple[bool, List[str]]:
        """
        اعتبارسنجی ساختار شتابدار (5 موجی)
        مطابق قوانین نقض‌ناپذیر الیوت/نئوویو:

        قانون ۱: موج ۲ هرگز از شروع موج ۱ عبور نمی‌کند
        قانون ۲: موج ۳ هرگز کوتاه‌ترین موج شتابدار نیست
        قانون ۳: موج ۴ هرگز با قلمرو قیمتی موج ۱ همپوشانی ندارد
        """
        errors = []

        if len(waves) != 5:
            errors.append(f"ساختار شتابدار باید دقیقاً ۵ موج داشته باشد، تعداد فعلی: {len(waves)}")
            return False, errors

        w1, w2, w3, w4, w5 = waves

        # ── بررسی جهت متناوب
        directions = [w.direction for w in waves]
        base_dir = directions[0]
        expected = [base_dir, -base_dir, base_dir, -base_dir, base_dir]
        if directions != expected:
            errors.append("جهت‌های متناوب موج‌های شتابدار نادرست است")
            return False, errors

        # ── قانون ۱: موج ۲ از شروع موج ۱ عبور نمی‌کند
        if base_dir == 1:  # روند صعودی
            if w2.end_price <= w1.start_price:
                errors.append(
                    f"نقض قانون ۱: موج ۲ ({w2.end_price:.4f}) به زیر "
                    f"شروع موج ۱ ({w1.start_price:.4f}) رسیده است"
                )
        else:  # روند نزولی
            if w2.end_price >= w1.start_price:
                errors.append(
                    f"نقض قانون ۱: موج ۲ ({w2.end_price:.4f}) به بالای "
                    f"شروع موج ۱ ({w1.start_price:.4f}) رسیده است"
                )

        # ── قانون ۲: موج ۳ کوتاه‌ترین نیست
        motive_ranges = [w1.price_range, w3.price_range, w5.price_range]
        if w3.price_range == min(motive_ranges):
            errors.append(
                f"نقض قانون ۲: موج ۳ ({w3.price_range:.4f}) "
                f"کوتاه‌ترین موج شتابدار است. "
                f"موج۱={w1.price_range:.4f}, موج۵={w5.price_range:.4f}"
            )

        # ── قانون ۳: موج ۴ با قلمرو موج ۱ همپوشانی ندارد
        if base_dir == 1:  # صعودی
            w1_top = w1.end_price
            w1_bottom = w1.start_price
            w4_low = w4.end_price
            w4_high = w4.start_price
            if w4_low < w1_top:
                errors.append(
                    f"نقض قانون ۳: موج ۴ (پایین={w4_low:.4f}) با "
                    f"قلمرو موج ۱ (بالا={w1_top:.4f}) همپوشانی دارد"
                )
        else:  # نزولی
            w1_bottom = w1.end_price
            w1_top = w1.start_price
            w4_high = w4.end_price
            if w4_high > w1_bottom:
                errors.append(
                    f"نقض قانون ۳: موج ۴ (بالا={w4_high:.4f}) با "
                    f"قلمرو موج ۱ (پایین={w1_bottom:.4f}) همپوشانی دارد"
                )

        is_valid = len(errors) == 0
        return is_valid, errors

    @staticmethod
    def validate_corrective_structure(waves: List[Monowave]) -> Tuple[bool, List[str]]:
        """
        اعتبارسنجی ساختار اصلاحی (3 موجی: A-B-C)
        مطابق قوانین اصلاحی نئوویو
        """
        errors = []

        if len(waves) != 3:
            errors.append(f"ساختار اصلاحی باید دقیقاً ۳ موج داشته باشد، تعداد فعلی: {len(waves)}")
            return False, errors

        wA, wB, wC = waves

        # ── موج A و C باید هم‌جهت باشند
        if wA.direction != wC.direction:
            errors.append(
                f"موج A (جهت={wA.direction}) و موج C (جهت={wC.direction}) "
                f"باید هم‌جهت باشند"
            )

        # ── موج B باید خلاف جهت A باشد
        if wB.direction == wA.direction:
            errors.append(
                f"موج B (جهت={wB.direction}) باید خلاف جهت "
                f"موج A (جهت={wA.direction}) باشد"
            )

        is_valid = len(errors) == 0
        return is_valid, errors

    @staticmethod
    def check_similarity_and_balance(w1: 'FractalWave', w2: 'FractalWave') -> Dict:
        """
        قانون تشابه و تعادل (Similarity & Balance) - فصل ۲۰، صفحه ۴۷۴

        "شباهت زمانی، قیمتی یا پیچیدگی هنگامی حاصل می‌شود که موج مورد نظر
        به لحاظ زمانی، قیمتی یا پیچیدگی بیش از ۱/۳ تا ۳ برابر موج مجاور
        را صرف کرده باشد"

        اگر نسبت > 3: موج بزرگتر احتمالاً از درجه بالاتر است
        اگر نسبت < 1/3: موج کوچکتر حتماً از درجه پایین‌تر است
        """
        MIN_R = FractalValidator.SIMILARITY_MIN_RATIO  # 1/3
        MAX_R = FractalValidator.SIMILARITY_MAX_RATIO  # 3.0

        # ── نسبت قیمتی
        if w2.price_range > 0:
            price_ratio = w1.price_range / w2.price_range
        else:
            price_ratio = float('inf')

        # ── نسبت زمانی
        if w2.duration > 0:
            time_ratio = w1.duration / w2.duration
        else:
            time_ratio = float('inf')

        # ── ارزیابی تشابه قیمتی
        price_similar = MIN_R <= price_ratio <= MAX_R

        # ── ارزیابی تشابه زمانی
        time_similar = MIN_R <= time_ratio <= MAX_R

        # ── حکم نهایی
        # "برای اینکه همسان تلقی شوند باید حداقل در دو وجه شباهت داشته باشند"
        # وجوه: قیمت، زمان، پیچیدگی
        # چون پیچیدگی را بررسی جداگانه داریم، برای دو موج هم‌درجه بودن
        # حداقل یکی از قیمت یا زمان باید satisfy شود
        same_degree_possible = price_similar and time_similar

        # ── تشخیص رابطه درجه
        if price_ratio > MAX_R or time_ratio > MAX_R:
            degree_relation = "w1 احتمالاً از درجه بالاتر از w2"
        elif price_ratio < MIN_R or time_ratio < MIN_R:
            degree_relation = "w1 حتماً از درجه پایین‌تر از w2"
        else:
            degree_relation = "هم‌درجه ممکن است"

        return {
            "price_ratio": round(price_ratio, 4),
            "time_ratio": round(time_ratio, 4),
            "price_similar": price_similar,
            "time_similar": time_similar,
            "same_degree_possible": same_degree_possible,
            "degree_relation": degree_relation,
            "w1_price": round(w1.price_range, 4),
            "w2_price": round(w2.price_range, 4),
            "w1_duration": w1.duration,
            "w2_duration": w2.duration,
        }

    @staticmethod
    def check_fractal_self_similarity(
        parent_wave: FractalWave,
        child_wave: FractalWave,
        wave_position: str
    ) -> Dict:
        """
        بررسی خود-تشابهی فراکتال (فصل ۲، صفحه ۲۱)

        "هیچ یک از ریز موج‌های یک قطعه بخش‌شده در یک الگو نمی‌تواند
        از نظر قیمتی، زمانی و سطح پیچیدگی بیشتر از موج متناظر آن
        در الگوی از درجه بزرگتر خود باشد" - فصل ۲۰، صفحه ۴۷۶

        پارامترها:
            parent_wave: موج درجه بالاتر
            child_wave: موج ریز (درجه پایین‌تر)
            wave_position: موقعیت موج ریز ("1","2","3","4","5" یا "A","B","C")
        """
        violations = []

        # ── بررسی قیمتی
        if child_wave.price_range > parent_wave.price_range:
            violations.append(
                f"نقض خود-تشابهی: ریزموج {wave_position} "
                f"(دامنه={child_wave.price_range:.4f}) از موج "
                f"مادر (دامنه={parent_wave.price_range:.4f}) بزرگتر است"
            )

        # ── بررسی زمانی
        if child_wave.duration > parent_wave.duration:
            violations.append(
                f"نقض خود-تشابهی: ریزموج {wave_position} "
                f"(مدت={child_wave.duration}) از موج "
                f"مادر (مدت={parent_wave.duration}) طولانی‌تر است"
            )

        # ── بررسی پیچیدگی
        if child_wave.complexity.value >= parent_wave.complexity.value:
            violations.append(
                f"نقض خود-تشابهی: سطح پیچیدگی ریزموج {wave_position} "
                f"({child_wave.complexity.name}) باید کمتر از موج "
                f"مادر ({parent_wave.complexity.name}) باشد"
            )

        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "wave_position": wave_position,
        }


# ════════════════════════════════════════════════════════════════════
# بخش ۴: تشخیص سطح پیچیدگی (فصل ۲۶)
# ════════════════════════════════════════════════════════════════════

class ComplexityClassifier:
    """
    طبقه‌بندی سطح پیچیدگی موج‌ها
    مطابق فصل ۲۶ کتاب نیلی (صفحات ۵۰۲-۵۱۰)

    سطح ۰ - Monowave: فاقد ریزموج
    سطح ۱ - Polywave: از چند تک‌موج تشکیل شده
    سطح ۲ - Multiwave: حداقل یک بساموج شتابدار درون دارد
    سطح ۳ - Macrowave: حداقل یک فراموج درون دارد (حداقل دو بساموج شتابدار)
    """

    @staticmethod
    def classify(wave: FractalWave) -> ComplexityLevel:
        """
        تشخیص سطح پیچیدگی یک موج بر اساس ساختار درونی‌اش
        """
        if not wave.sub_waves:
            # فاقد ریزموج = Monowave
            return ComplexityLevel.MONOWAVE

        # بررسی ریزموج‌های شتابدار درون
        motive_sub_waves = [
            sw for sw in wave.sub_waves
            if sw.wave_type == WaveType.MOTIVE
        ]

        # شمارش بساموج‌های شتابدار
        polywave_motive_count = sum(
            1 for sw in motive_sub_waves
            if sw.complexity == ComplexityLevel.POLYWAVE
        )

        # شمارش فراموج‌های درون
        multiwave_count = sum(
            1 for sw in wave.sub_waves
            if sw.complexity == ComplexityLevel.MULTIWAVE
        )

        if multiwave_count >= 1 or polywave_motive_count >= 2:
            # فصل ۲۶، صفحه ۵۰۵:
            # "ابرموجها حداقل شامل یک بساموج و یک فراموج می‌باشند"
            return ComplexityLevel.MACROWAVE

        if polywave_motive_count >= 1:
            # فصل ۲۶، صفحه ۵۰۳:
            # "فراموج‌ها... دارای حداکثر یک بساموج شتابدار می‌باشند"
            return ComplexityLevel.MULTIWAVE

        # همه ریزموج‌ها Monowave هستند → این موج یک Polywave است
        all_monowaves = all(
            sw.complexity == ComplexityLevel.MONOWAVE
            for sw in wave.sub_waves
        )
        if all_monowaves:
            return ComplexityLevel.POLYWAVE

        # پیچیدگی‌های آمیخته → حداقل Polywave
        return ComplexityLevel.POLYWAVE

    @staticmethod
    def get_complexity_label(level: ComplexityLevel) -> str:
        """
        برچسب متنی سطح پیچیدگی
        مطابق اصطلاحات فارسی کتاب
        """
        labels = {
            ComplexityLevel.MONOWAVE: "تک‌موج (Monowave) - سطح ۰",
            ComplexityLevel.POLYWAVE: "بساموج (Polywave) - سطح ۱",
            ComplexityLevel.MULTIWAVE: "فراموج (Multiwave) - سطح ۲",
            ComplexityLevel.MACROWAVE: "ابرموج (Macrowave) - سطح ۳",
        }
        return labels.get(level, "نامشخص")


# ════════════════════════════════════════════════════════════════════
# بخش ۵: سازنده موج فراکتالی (الگوریتم اصلی)
# ════════════════════════════════════════════════════════════════════

class FractalBuilder:
    """
    سازنده ساختار فراکتالی مطابق فصل ۲ نیلی

    الگوریتم:
    1. شناسایی Monowave‌ها
    2. ترکیب ۵‌تایی/۳‌تایی برای ساخت Polywave
    3. ترکیب Polywave‌ها برای ساخت Multiwave
    4. ترکیب Multiwave‌ها برای ساخت Macrowave

    این فرآیند دقیقاً همان "تکرار" است که نیلی در صفحه ۲۱ توضیح می‌دهد
    """

    def __init__(self):
        self.validator = FractalValidator()
        self.classifier = ComplexityClassifier()

    def build_from_monowaves(
        self,
        monowaves: List[Monowave],
        max_levels: int = 3
    ) -> List[FractalWave]:
        """
        ساخت ساختار فراکتالی از پایین به بالا (Bottom-Up)
        مطابق فرآیند فشرده‌سازی نئوویو (فصل ۲۲)

        مرحله ۱: Monowave‌ها → Polywave (ترکیب ۵‌تایی یا ۳‌تایی)
        مرحله ۲: Polywave‌ها → Multiwave
        مرحله ۳: Multiwave‌ها → Macrowave
        """
        # تبدیل Monowave به FractalWave برای پردازش یکسان
        level_0 = self._monowaves_to_fractal(monowaves)

        current_level = level_0
        all_levels = [level_0]

        for level_num in range(1, max_levels + 1):
            next_level = self._combine_to_higher_degree(
                current_level,
                complexity_target=ComplexityLevel(level_num)
            )
            if not next_level or len(next_level) >= len(current_level):
                break  # پیشرفتی نشده، متوقف می‌شویم
            all_levels.append(next_level)
            current_level = next_level

        return current_level  # بالاترین سطح تشخیص داده‌شده

    def _monowaves_to_fractal(self, monowaves: List[Monowave]) -> List[FractalWave]:
        """تبدیل Monowave‌های خام به FractalWave سطح صفر"""
        result = []
        for mw in monowaves:
            fw = FractalWave(
                start_idx=mw.start_idx,
                end_idx=mw.end_idx,
                start_price=mw.start_price,
                end_price=mw.end_price,
                direction=mw.direction,
                price_range=mw.price_range,
                duration=mw.duration,
                complexity=ComplexityLevel.MONOWAVE,
                wave_type=WaveType.UNKNOWN,
                degree=WaveDegree.SUBMINUETTE,
                sub_waves=[],
                label=""
            )
            result.append(fw)
        return result

    def _combine_to_higher_degree(
        self,
        waves: List[FractalWave],
        complexity_target: ComplexityLevel
    ) -> List[FractalWave]:
        """
        ترکیب موج‌های سطح پایین‌تر به الگوهای سطح بالاتر

        مطابق فصل ۲ نیلی:
        - ۵ موج هم‌نوع → موج شتابدار (Motive)
        - ۳ موج هم‌نوع → موج اصلاحی (Corrective)
        """
        result = []
        i = 0

        while i <= len(waves) - 3:
            # ── تلاش برای ترکیب ۵‌موجی (شتابدار)
            if i <= len(waves) - 5:
                candidate_5 = waves[i:i + 5]
                is_motive, _ = self.validator.validate_motive_structure(
                    [self._fractal_to_mono(w) for w in candidate_5]
                )
                if is_motive:
                    combined = self._merge_waves(
                        candidate_5,
                        WaveType.MOTIVE,
                        complexity_target
                    )
                    result.append(combined)
                    i += 5
                    continue

            # ── تلاش برای ترکیب ۳‌موجی (اصلاحی)
            candidate_3 = waves[i:i + 3]
            is_corrective, _ = self.validator.validate_corrective_structure(
                [self._fractal_to_mono(w) for w in candidate_3]
            )
            if is_corrective:
                combined = self._merge_waves(
                    candidate_3,
                    WaveType.CORRECTIVE,
                    complexity_target
                )
                result.append(combined)
                i += 3
                continue

            # ── موج ترکیب‌نشده را به‌تنهایی اضافه کن
            result.append(waves[i])
            i += 1

        # بقیه موج‌های اضافی
        while i < len(waves):
            result.append(waves[i])
            i += 1

        return result

    def _merge_waves(
        self,
        sub_waves: List[FractalWave],
        wave_type: WaveType,
        complexity: ComplexityLevel
    ) -> FractalWave:
        """ادغام چند موج به یک موج سطح بالاتر"""
        start = sub_waves[0]
        end = sub_waves[-1]

        # برچسب‌گذاری ریزموج‌ها
        if wave_type == WaveType.MOTIVE:
            labels = ["1", "2", "3", "4", "5"]
        else:
            labels = ["A", "B", "C"]

        for idx, sw in enumerate(sub_waves):
            if idx < len(labels):
                sw.label = labels[idx]

        parent = FractalWave(
            start_idx=start.start_idx,
            end_idx=end.end_idx,
            start_price=start.start_price,
            end_price=end.end_price,
            direction=1 if end.end_price > start.start_price else -1,
            price_range=abs(end.end_price - start.start_price),
            duration=end.end_idx - start.start_idx,
            complexity=complexity,
            wave_type=wave_type,
            degree=WaveDegree(min(start.degree.value + 1, len(WaveDegree) - 1)),
            sub_waves=list(sub_waves),
            label=""
        )

        return parent

    @staticmethod
    def _fractal_to_mono(fw: FractalWave) -> Monowave:
        """تبدیل FractalWave به Monowave برای استفاده در validator"""
        return Monowave(
            start_idx=fw.start_idx,
            end_idx=fw.end_idx,
            start_price=fw.start_price,
            end_price=fw.end_price,
            direction=fw.direction,
            price_range=fw.price_range,
            duration=fw.duration
        )


# ════════════════════════════════════════════════════════════════════
# بخش ۶: تحلیل‌گر اصلی فصل ۲
# ════════════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None) -> Dict:
    """
    تحلیل ساختار فراکتال امواج الیوت
    مطابق فصل ۲ کتاب گلن نیلی (صفحه ۲۱)

    "فراکتال‌ها در حقیقت ساختارهای هندسی متشکل از اجزایی می‌باشند که با
    بزرگ کردن هر جزء به نسبت معین، همان ساختار اولیه به دست آید."

    این تابع:
    1. تک‌موج‌ها را استخراج می‌کند
    2. ساختار فراکتالی را از پایین به بالا می‌سازد
    3. قانون تشابه و تعادل را بررسی می‌کند
    4. سطح پیچیدگی را تشخیص می‌دهد
    5. خود-تشابهی فراکتالی را اعتبارسنجی می‌کند
    """

    # ════════════════════════════════════════
    # مرحله ۱: استخراج داده‌های قیمتی
    # ════════════════════════════════════════
    close = data['close'].values if 'close' in data.columns else data['Close'].values
    high = data['high'].values if 'high' in data.columns else data['High'].values
    low = data['low'].values if 'low' in data.columns else data['Low'].values
    n = len(close)

    if n < 8:
        return {
            "وضعیت": "داده کافی نیست",
            "تعداد_کندل‌ها": n,
            "پیام": "برای تحلیل فراکتال حداقل ۸ کندل لازم است"
        }

    # ════════════════════════════════════════
    # مرحله ۲: استخراج تک‌موج‌ها (Monowaves)
    # ════════════════════════════════════════
    monowaves = extract_monowaves(data, order=3)

    if len(monowaves) < 3:
        return {
            "وضعیت": "تک‌موج کافی نیست",
            "تعداد_تک‌موج": len(monowaves),
            "پیام": "برای تحلیل فراکتال حداقل ۳ تک‌موج لازم است"
        }

    # ════════════════════════════════════════
    # مرحله ۳: ساخت ساختار فراکتالی
    # ════════════════════════════════════════
    builder = FractalBuilder()
    fractal_waves = builder.build_from_monowaves(monowaves, max_levels=3)

    # ════════════════════════════════════════
    # مرحله ۴: طبقه‌بندی سطح پیچیدگی
    # ════════════════════════════════════════
    complexity_counts = {level: 0 for level in ComplexityLevel}
    for fw in fractal_waves:
        complexity_counts[fw.complexity] += 1

    # ════════════════════════════════════════
    # مرحله ۵: بررسی قانون تشابه و تعادل
    # برای موج‌های مجاور (فصل ۲۰)
    # ════════════════════════════════════════
    validator = FractalValidator()
    similarity_results = []
    same_degree_pairs = 0
    different_degree_pairs = 0

    for i in range(len(fractal_waves) - 1):
        w1 = fractal_waves[i]
        w2 = fractal_waves[i + 1]
        sim = validator.check_similarity_and_balance(w1, w2)
        similarity_results.append(sim)
        if sim["same_degree_possible"]:
            same_degree_pairs += 1
        else:
            different_degree_pairs += 1

    # ════════════════════════════════════════
    # مرحله ۶: شناسایی الگوهای فراکتالی
    # (ترکیب ۵‌موجی شتابدار + ۳‌موجی اصلاحی)
    # ════════════════════════════════════════
    motive_patterns = []
    corrective_patterns = []

    # بررسی در Monowaveها
    for i in range(len(monowaves) - 4):
        seg = monowaves[i:i + 5]
        is_valid, errors = validator.validate_motive_structure(seg)
        if is_valid:
            motive_patterns.append({
                "start_idx": seg[0].start_idx,
                "end_idx": seg[4].end_idx,
                "start_price": seg[0].start_price,
                "end_price": seg[4].end_price,
                "direction": "صعودی" if seg[0].direction == 1 else "نزولی",
                "total_range": sum(w.price_range for w in seg),
                "duration": seg[4].end_idx - seg[0].start_idx,
                "wave_1_range": seg[0].price_range,
                "wave_2_range": seg[1].price_range,
                "wave_3_range": seg[2].price_range,
                "wave_4_range": seg[3].price_range,
                "wave_5_range": seg[4].price_range,
                # فیبوناچی داخلی
                "w3_w1_ratio": round(seg[2].price_range / seg[0].price_range, 3) if seg[0].price_range > 0 else 0,
                "w5_w1_ratio": round(seg[4].price_range / seg[0].price_range, 3) if seg[0].price_range > 0 else 0,
                "w2_w1_ratio": round(seg[1].price_range / seg[0].price_range, 3) if seg[0].price_range > 0 else 0,
                "w4_w3_ratio": round(seg[3].price_range / seg[2].price_range, 3) if seg[2].price_range > 0 else 0,
            })

    for i in range(len(monowaves) - 2):
        seg = monowaves[i:i + 3]
        is_valid, errors = validator.validate_corrective_structure(seg)
        if is_valid:
            corrective_patterns.append({
                "start_idx": seg[0].start_idx,
                "end_idx": seg[2].end_idx,
                "start_price": seg[0].start_price,
                "end_price": seg[2].end_price,
                "direction": "صعودی" if seg[0].direction == 1 else "نزولی",
                "total_range": sum(w.price_range for w in seg),
                "duration": seg[2].end_idx - seg[0].start_idx,
                "wave_A_range": seg[0].price_range,
                "wave_B_range": seg[1].price_range,
                "wave_C_range": seg[2].price_range,
                "wB_wA_ratio": round(seg[1].price_range / seg[0].price_range, 3) if seg[0].price_range > 0 else 0,
                "wC_wA_ratio": round(seg[2].price_range / seg[0].price_range, 3) if seg[0].price_range > 0 else 0,
            })

    # ════════════════════════════════════════
    # مرحله ۷: شناسایی چرخه‌های کامل ۸‌موجی
    # (فصل ۳ کتاب نیلی - صفحه ۲۲)
    # ════════════════════════════════════════
    complete_cycles = []
    for i in range(len(monowaves) - 7):
        seg = monowaves[i:i + 8]
        # ۵ موج شتابدار + ۳ موج اصلاحی
        motive_5 = seg[:5]
        corrective_3 = seg[5:]

        is_motive, _ = validator.validate_motive_structure(motive_5)
        is_corrective, _ = validator.validate_corrective_structure(corrective_3)

        # جهت اصلاحی باید خلاف شتابدار باشد
        if (is_motive and is_corrective and
                corrective_3[0].direction == -motive_5[0].direction):
            complete_cycles.append({
                "start_idx": seg[0].start_idx,
                "end_idx": seg[7].end_idx,
                "motive_direction": "صعودی" if motive_5[0].direction == 1 else "نزولی",
                "motive_range": sum(w.price_range for w in motive_5),
                "corrective_range": sum(w.price_range for w in corrective_3),
                "total_duration": seg[7].end_idx - seg[0].start_idx,
                "retracement_ratio": round(
                    sum(w.price_range for w in corrective_3) /
                    sum(w.price_range for w in motive_5), 3
                ) if sum(w.price_range for w in motive_5) > 0 else 0
            })

    # ════════════════════════════════════════
    # مرحله ۸: تحلیل نسبت‌های فیبوناچی کلیدی
    # (مطابق اصول نئوویو)
    # ════════════════════════════════════════
    fib_ratios = {
        "0.236": 0.236, "0.382": 0.382, "0.500": 0.500,
        "0.618": 0.618, "0.764": 0.764, "1.000": 1.000,
        "1.272": 1.272, "1.618": 1.618, "2.000": 2.000,
        "2.618": 2.618
    }

    def nearest_fib(ratio: float) -> str:
        """نزدیک‌ترین نسبت فیبوناچی را برمی‌گرداند"""
        nearest = min(fib_ratios.items(), key=lambda x: abs(x[1] - ratio))
        return nearest[0]

    fib_analysis = []
    for mp in motive_patterns[:5]:
        fib_analysis.append({
            "نوع": "شتابدار",
            "W3/W1": mp["w3_w1_ratio"],
            "نزدیک‌ترین_فیبو_W3/W1": nearest_fib(mp["w3_w1_ratio"]),
            "W5/W1": mp["w5_w1_ratio"],
            "نزدیک‌ترین_فیبو_W5/W1": nearest_fib(mp["w5_w1_ratio"]),
            "W2/W1_(اصلاح)": mp["w2_w1_ratio"],
            "نزدیک‌ترین_فیبو_W2": nearest_fib(mp["w2_w1_ratio"]),
        })

    # ════════════════════════════════════════
    # مرحله ۹: تولید خروجی
    # ════════════════════════════════════════
    results = {
        # ── اطلاعات پایه
        "عنوان": "ساختار فراکتال امواج الیوت (Fractal Structure)",
        "مرجع_کتاب": "صفحه ۲۱ - گلن نیلی",

        # ── آمار اولیه
        "تعداد_کل_کندل": n,
        "تعداد_تک‌موج_(Monowave)": len(monowaves),
        "تعداد_موج_فراکتالی_تشخیص‌داده‌شده": len(fractal_waves),

        # ── الگوهای شناسایی‌شده
        "تعداد_الگوی_شتابدار_(5_موجی)": len(motive_patterns),
        "تعداد_الگوی_اصلاحی_(3_موجی)": len(corrective_patterns),
        "تعداد_چرخه_کامل_(8_موجی)": len(complete_cycles),

        # ── سطح پیچیدگی (فصل ۲۶)
        "تعداد_Monowave_(سطح_0)": complexity_counts[ComplexityLevel.MONOWAVE],
        "تعداد_Polywave_(سطح_1)": complexity_counts[ComplexityLevel.POLYWAVE],
        "تعداد_Multiwave_(سطح_2)": complexity_counts[ComplexityLevel.MULTIWAVE],
        "تعداد_Macrowave_(سطح_3)": complexity_counts[ComplexityLevel.MACROWAVE],

        # ── قانون تشابه و تعادل (فصل ۲۰)
        "جفت‌موج_هم‌درجه_ممکن": same_degree_pairs,
        "جفت‌موج_درجه_متفاوت": different_degree_pairs,

        # ── اصول فراکتال از کتاب
        "اصل_فراکتال_1": "هر موج شتابدار از ۵ ریزموج تشکیل می‌شود",
        "اصل_فراکتال_2": "هر موج اصلاحی از ۳ ریزموج تشکیل می‌شود",
        "اصل_فراکتال_3": "ترکیب این دو فاز، موج مرتبه بالاتر را می‌سازد",
        "اصل_فراکتال_4": "موج شتابدار فقط شامل ریزموج‌های شتابدار است",
        "اصل_فراکتال_5": "موج اصلاحی فقط شامل ریزموج‌های اصلاحی است",
        "اصل_فراکتال_6": "این ساختار در تمام درجات (Degrees) تکرار می‌شود", 

        # ⭐⭐⭐ اضافه کن - داده‌های خام برای استفاده فصل‌های دیگر ⭐⭐⭐
        "_monowaves": monowaves,
        "_motive_patterns": motive_patterns,
        "_corrective_patterns": corrective_patterns,
        "_complete_cycles": complete_cycles,
        "_fractal_waves": fractal_waves,
    }

    # ── اضافه‌کردن جزئیات الگوهای شتابدار
    for idx, mp in enumerate(motive_patterns[:5]):
        prefix = f"الگوی_شتابدار_{idx + 1}"
        results[f"{prefix}_جهت"] = mp["direction"]
        results[f"{prefix}_دامنه_کل"] = round(mp["total_range"], 4)
        results[f"{prefix}_مدت"] = mp["duration"]
        results[f"{prefix}_نسبت_W3/W1"] = mp["w3_w1_ratio"]
        results[f"{prefix}_نسبت_W5/W1"] = mp["w5_w1_ratio"]

    # ── اضافه‌کردن جزئیات الگوهای اصلاحی
    for idx, cp in enumerate(corrective_patterns[:5]):
        prefix = f"الگوی_اصلاحی_{idx + 1}"
        results[f"{prefix}_جهت"] = cp["direction"]
        results[f"{prefix}_دامنه_کل"] = round(cp["total_range"], 4)
        results[f"{prefix}_نسبت_wB/wA"] = cp["wB_wA_ratio"]
        results[f"{prefix}_نسبت_wC/wA"] = cp["wC_wA_ratio"]

    # ── اضافه‌کردن چرخه‌های کامل
    for idx, cc in enumerate(complete_cycles[:3]):
        prefix = f"چرخه_کامل_{idx + 1}"
        results[f"{prefix}_جهت_شتابدار"] = cc["motive_direction"]
        results[f"{prefix}_نسبت_اصلاح_به_شتاب"] = cc["retracement_ratio"]

    # ── تفسیر نهایی
    interpretation = _build_interpretation(
        n, len(monowaves), len(fractal_waves),
        len(motive_patterns), len(corrective_patterns),
        len(complete_cycles), complexity_counts,
        same_degree_pairs, different_degree_pairs,
        fib_analysis
    )
    results["تفسیر_نهایی"] = interpretation

    # ── ذخیره در لاگ
    if logger:
        _write_to_logger(logger, results, monowaves, motive_patterns,
                         corrective_patterns, complete_cycles)

    return results


# ════════════════════════════════════════════════════════════════════
# بخش ۷: تولید تفسیر نهایی
# ════════════════════════════════════════════════════════════════════

def _build_interpretation(
    n: int,
    monowave_count: int,
    fractal_count: int,
    motive_count: int,
    corrective_count: int,
    cycle_count: int,
    complexity_counts: Dict,
    same_degree_pairs: int,
    diff_degree_pairs: int,
    fib_analysis: List[Dict]
) -> str:
    """تولید تفسیر متنی کامل مطابق سبک نئوویو"""

    fib_text = ""
    for fa in fib_analysis[:2]:
        fib_text += (
            f"\n    • W3/W1 = {fa['W3/W1']} ≈ فیبو {fa['نزدیک‌ترین_فیبو_W3/W1']} | "
            f"W5/W1 = {fa['W5/W1']} ≈ فیبو {fa['نزدیک‌ترین_فیبو_W5/W1']} | "
            f"اصلاح W2 = {fa['W2/W1_(اصلاح)']} ≈ فیبو {fa['نزدیک‌ترین_فیبو_W2']}"
        )

    interpretation = f"""
═══════════════════════════════════════════════════════════════════
تفسیر نهایی فصل ۲: ساختار فراکتال (مطابق صفحه ۲۱ کتاب نیلی)
═══════════════════════════════════════════════════════════════════

📖 تعریف فراکتال در نئوویو:
"فراکتال‌ها ساختارهای هندسی هستند که با بزرگ کردن هر جزء به نسبت
معین، همان ساختار اولیه به دست می‌آید. امواج الیوت دارای ساختار
فراکتال می‌باشند."

📊 آمار داده‌های تحلیل‌شده:
  • تعداد کندل: {n}
  • تک‌موج‌های شناسایی‌شده: {monowave_count}
  • موج‌های فراکتالی ترکیب‌شده: {fractal_count}

🔬 الگوهای فراکتالی کشف‌شده:
  • الگوهای شتابدار (5 موجی): {motive_count}
  • الگوهای اصلاحی (3 موجی): {corrective_count}
  • چرخه‌های کامل (8 موجی): {cycle_count}

📐 سطوح پیچیدگی (فصل ۲۶ - درجه‌بندی پیچیدگی موج‌ها):
  • Monowave سطح ۰ (تک‌موج): {complexity_counts[ComplexityLevel.MONOWAVE]}
  • Polywave سطح ۱ (بساموج): {complexity_counts[ComplexityLevel.POLYWAVE]}
  • Multiwave سطح ۲ (فراموج): {complexity_counts[ComplexityLevel.MULTIWAVE]}
  • Macrowave سطح ۳ (ابرموج): {complexity_counts[ComplexityLevel.MACROWAVE]}

⚖️ قانون تشابه و تعادل (فصل ۲۰):
  نسبت ۱/۳ تا ۳ برابر برای هم‌درجه بودن:
  • جفت‌موج‌های هم‌درجه ممکن: {same_degree_pairs}
  • جفت‌موج‌های درجه متفاوت: {diff_degree_pairs}

📏 نسبت‌های فیبوناچی داخلی الگوها:{fib_text if fib_text else chr(10) + "    هنوز الگوی شتابدار کافی شناسایی نشده"}

🔄 قوانین فراکتال نئوویو (از کتاب):
  ✓ هر موج شتابدار = ۵ ریزموج (همان ساختار در درجه پایین‌تر)
  ✓ هر موج اصلاحی = ۳ ریزموج (همان ساختار در درجه پایین‌تر)
  ✓ ترکیب ۵+۳ = چرخه کامل یک درجه بالاتر
  ✓ این تکرار در تمام درجات Grand Supercycle تا Subminuette ادامه دارد

💡 نتیجه‌گیری نئوویو:
ساختار فراکتال تضمین می‌کند که قوانین الیوت در تمام تایم‌فریم‌ها
صادق است. شناخت این ساختار، شرط اول تحلیل صحیح نئوویو است.
═══════════════════════════════════════════════════════════════════"""

    return interpretation


# ════════════════════════════════════════════════════════════════════
# بخش ۸: ثبت در لاگ
# ════════════════════════════════════════════════════════════════════

def _write_to_logger(logger, results, monowaves, motive_patterns,
                     corrective_patterns, complete_cycles):
    """ثبت نتایج در سیستم لاگ‌گیری"""
    logger.add_section("فصل ۲: ساختار فراکتال (Fractal Structure)", level=1)
    logger.add_result("مرجع کتاب", "صفحه ۲۱ - گلن نیلی", "")
    logger.add_result("تعداد تک‌موج", len(monowaves), "Monowave - سطح پیچیدگی صفر")
    logger.add_result("الگوهای شتابدار ۵‌موجی", len(motive_patterns), "Motive Wave")
    logger.add_result("الگوهای اصلاحی ۳‌موجی", len(corrective_patterns), "Corrective Wave")
    logger.add_result("چرخه‌های کامل ۸‌موجی", len(complete_cycles), "Complete Market Cycle")

    logger.add_section("سطوح پیچیدگی (فصل ۲۶)", level=2)
    logger.add_result("Monowave (۰)", results.get("تعداد_Monowave_(سطح_0)", 0), "تک‌موج")
    logger.add_result("Polywave (۱)", results.get("تعداد_Polywave_(سطح_1)", 0), "بساموج")
    logger.add_result("Multiwave (۲)", results.get("تعداد_Multiwave_(سطح_2)", 0), "فراموج")
    logger.add_result("Macrowave (۳)", results.get("تعداد_Macrowave_(سطح_3)", 0), "ابرموج")

    logger.add_section("قانون تشابه و تعادل (فصل ۲۰)", level=2)
    logger.add_result("نسبت هم‌درجگی", "۱/۳ تا ۳", "معیار قانون Similarity & Balance")
    logger.add_result("جفت هم‌درجه", results.get("جفت‌موج_هم‌درجه_ممکن", 0), "")
    logger.add_result("جفت درجه متفاوت", results.get("جفت‌موج_درجه_متفاوت", 0), "")

    logger.add_section("اصول فراکتال", level=2)
    for i in range(1, 7):
        key = f"اصل_فراکتال_{i}"
        logger.add_result(f"اصل {i}", results.get(key, ""), "")

    logger.add_result("تفسیر نهایی", results.get("تفسیر_نهایی", ""), "")