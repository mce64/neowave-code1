# chapters/chapter_08.py

"""
فصل ۸: نمودار لگاریتمی یا حسابی (Logarithmic or Arithmetic)
منبع: کتاب "امواج الیوت به سبک نئوویو" - گلن نیلی - صفحات ۴۹ تا ۵۱

═══════════════════════════════════════════════════════════════════
متن دقیق کتاب (صفحه ۴۹):

"در حالت ایده آل، تمام نمودار ها باید به صورت لگاریتمی ترسیم شوند.
در دنیای واقعی، شما باید برای الگوهای موجی که محدوده وسیعی از قیمت را
پوشش می‌دهند، از نمودارهای لگاریتمی استفاده کنید.

یک محدوده قیمتی بزرگ با درصد تفاوت بین بالاترین و کمترین قیمت در نمودار
شما تعریف می‌شود. اگر قیمت بالا بیش از دو برابر ارزش قیمت پایین باشد،
نمودار لگاریتمی برای شمارش موجی و کانال بندی دقیق مناسب است.
هر چقدر اختلاف درصد بین سطح قیمت بالا و پایین بیشتر باشد،
اهمیت استفاده از مقیاس لگاریتمی بیشتر است.

رشد قیمت‌ها، به صورت درصدی نه به صورت خطی رخ می‌دهند، بهتر است که
داده ها را به صورت لگاریتمی ترسیم کنیم و روابط فیبوناچی را نیز بر اساس
فاصله فیزیکی تحت پوشش در نمودار لگاریتمی مقایسه کنیم."

═══════════════════════════════════════════════════════════════════
فرمول‌های صفحه ۵۰ و ۵۱:

محاسبه بر اساس تغییرات قیمتی (Linear/Arithmetic):
    C = B - F * Δ
    D = C + F * Δ
    (برای محاسبه سطوح پایین‌تر و بالاتر)

محاسبه بر اساس مقیاس لگاریتمی (Logarithmic):
    log(B/C) = F * log(B/A)
    log(C/D) = F * log(A/B)
    log(C/B) = F * log(A/B)

که در آن:
    A = قیمت شروع
    B = قیمت پایان (یا نقطه مرجع)
    C = سطح پایین‌تر
    D = سطح بالاتر
    F = نسبت فیبوناچی (0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618, 2.618)
    Δ = اختلاف قیمت مطلق
    n = نرخ رشد نسبی (n = (B - A)/A)
    m = نرخ افت نسبی (m = (A - B)/A)
═══════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


# ════════════════════════════════════════════════════════════════
# بخش ۱: تعاریف پایه
# ════════════════════════════════════════════════════════════════

class ScaleType(Enum):
    """نوع مقیاس نمودار"""
    LINEAR = "حسابی (Linear)"
    LOGARITHMIC = "لگاریتمی (Logarithmic)"
    AUTO = "خودکار"


class FibonacciRatio(Enum):
    """نسبت‌های فیبوناچی استاندارد در نئوویو"""
    RET_0_236 = 0.236
    RET_0_382 = 0.382
    RET_0_500 = 0.500
    RET_0_618 = 0.618
    RET_0_786 = 0.786
    EXT_1_000 = 1.000
    EXT_1_272 = 1.272
    EXT_1_618 = 1.618
    EXT_2_000 = 2.000
    EXT_2_618 = 2.618


@dataclass
class FibonacciLevel:
    """یک سطح فیبوناچی محاسبه‌شده"""
    ratio: float
    ratio_name: str
    price_level: float
    is_support: bool
    is_resistance: bool
    scale_used: ScaleType


@dataclass
class PriceRange:
    """محدوده قیمتی برای تحلیل مقیاس"""
    start_price: float
    end_price: float
    high_price: float
    low_price: float
    ratio: float                    # high/low نسبت
    use_log_scale: bool             # آیا باید لگاریتمی استفاده شود؟
    reason: str                     # دلیل انتخاب مقیاس


# ════════════════════════════════════════════════════════════════
# بخش ۲: تشخیص مقیاس مناسب (صفحه ۴۹)
# ════════════════════════════════════════════════════════════════

def determine_scale_type(
    high_price: float,
    low_price: float,
    force_scale: Optional[ScaleType] = None
) -> Tuple[ScaleType, str]:
    """
    تشخیص مقیاس مناسب برای نمودار.
    
    قانون کلیدی (صفحه ۴۹):
        "اگر قیمت بالا بیش از دو برابر ارزش قیمت پایین باشد،
         نمودار لگاریتمی برای شمارش موجی و کانال بندی دقیق مناسب است.
         هر چقدر اختلاف درصد بین سطح قیمت بالا و پایین بیشتر باشد،
         اهمیت استفاده از مقیاس لگاریتمی بیشتر است."
    
    پارامترها:
        high_price: بالاترین قیمت در بازه
        low_price: پایین‌ترین قیمت در بازه
        force_scale: اجباری کردن نوع مقیاس (برای تست)
    
    خروجی:
        (نوع_مقیاس, دلیل)
    """
    if force_scale and force_scale != ScaleType.AUTO:
        if force_scale == ScaleType.LINEAR:
            return ScaleType.LINEAR, "اجبار کاربر به مقیاس حسابی"
        else:
            return ScaleType.LOGARITHMIC, "اجبار کاربر به مقیاس لگاریتمی"
    
    if low_price <= 0:
        return ScaleType.LINEAR, "قیمت پایین صفر یا منفی - استفاده از مقیاس حسابی"
    
    ratio = high_price / low_price
    
    if ratio >= 3.0:
        # بیش از ۳ برابر → لگاریتمی الزامی
        return ScaleType.LOGARITHMIC, f"نسبت قیمت بالا به پایین = {ratio:.2f} (> 3.0) - استفاده از مقیاس لگاریتمی الزامی است"
    elif ratio >= 2.0:
        # بین ۲ تا ۳ برابر → لگاریتمی توصیه می‌شود
        return ScaleType.LOGARITHMIC, f"نسبت قیمت بالا به پایین = {ratio:.2f} (> 2.0) - مقیاس لگاریتمی توصیه می‌شود"
    elif ratio >= 1.5:
        # بین ۱.۵ تا ۲ برابر → می‌توان هر دو را استفاده کرد
        return ScaleType.LINEAR, f"نسبت قیمت بالا به پایین = {ratio:.2f} - هر دو مقیاس قابل استفاده هستند، حسابی پیش‌فرض"
    else:
        # کمتر از ۱.۵ برابر → حسابی کافی است
        return ScaleType.LINEAR, f"نسبت قیمت بالا به پایین = {ratio:.2f} (< 1.5) - مقیاس حسابی کافی است"


def analyze_price_range(
    prices: np.ndarray,
    lookback: Optional[int] = None
) -> PriceRange:
    """
    تحلیل محدوده قیمتی و تعیین مقیاس مناسب.
    
    پارامترها:
        prices: آرایه قیمت‌ها (می‌تواند close, high, low باشد)
        lookback: تعداد کندل‌های آخر برای تحلیل (None = همه)
    
    خروجی:
        PriceRange
    """
    if lookback is not None and lookback < len(prices):
        prices = prices[-lookback:]
    
    start_price = float(prices[0])
    end_price = float(prices[-1])
    high_price = float(np.max(prices))
    low_price = float(np.min(prices))
    ratio = high_price / low_price if low_price > 0 else float('inf')
    
    scale_type, reason = determine_scale_type(high_price, low_price)
    use_log = (scale_type == ScaleType.LOGARITHMIC)
    
    return PriceRange(
        start_price=start_price,
        end_price=end_price,
        high_price=high_price,
        low_price=low_price,
        ratio=ratio,
        use_log_scale=use_log,
        reason=reason
    )


# ════════════════════════════════════════════════════════════════
# بخش ۳: محاسبه سطوح فیبوناچی – مقیاس خطی (صفحه ۵۰)
# ════════════════════════════════════════════════════════════════

def calculate_fibonacci_linear(
    start_price: float,
    end_price: float,
    is_uptrend: bool = True
) -> List[FibonacciLevel]:
    """
    محاسبه سطوح فیبوناچی با مقیاس خطی (حسابی).
    
    فرمول‌های صفحه ۵۰:
        C = B - F * Δ
        D = C + F * Δ
    
    که در آن:
        Δ = |B - A|
        A = قیمت شروع
        B = قیمت پایان
        F = نسبت فیبوناچی
    
    برای روند صعودی:
        - سطوح اصلاحی (Support): B - F * (B - A)
        - سطوح توسعه (Resistance): B + F * (B - A)
    
    برای روند نزولی:
        - سطوح اصلاحی (Resistance): B + F * (A - B)
        - سطوح توسعه (Support): B - F * (A - B)
    """
    levels = []
    diff = abs(end_price - start_price)
    
    ratios = [
        (0.236, "23.6%"),
        (0.382, "38.2%"),
        (0.500, "50.0%"),
        (0.618, "61.8%"),
        (0.786, "78.6%"),
        (1.000, "100%"),
        (1.272, "127.2%"),
        (1.618, "161.8%"),
        (2.000, "200%"),
        (2.618, "261.8%"),
    ]
    
    if is_uptrend:
        # روند صعودی: A = پایین، B = بالا
        low_price = min(start_price, end_price)
        high_price = max(start_price, end_price)
        
        for ratio, name in ratios:
            # سطوح اصلاحی (زیر قیمت فعلی) - حمایت
            retrace = high_price - (diff * ratio)
            levels.append(FibonacciLevel(
                ratio=ratio,
                ratio_name=name,
                price_level=round(retrace, 4),
                is_support=True,
                is_resistance=False,
                scale_used=ScaleType.LINEAR
            ))
            
            # سطوح توسعه (بالای قیمت فعلی) - مقاومت
            if ratio <= 1.0:
                extension = high_price + (diff * ratio)
            else:
                extension = high_price + (diff * ratio)
            levels.append(FibonacciLevel(
                ratio=ratio,
                ratio_name=f"{name} (Ext)",
                price_level=round(extension, 4),
                is_support=False,
                is_resistance=True,
                scale_used=ScaleType.LINEAR
            ))
    else:
        # روند نزولی: A = بالا، B = پایین
        high_price = max(start_price, end_price)
        low_price = min(start_price, end_price)
        
        for ratio, name in ratios:
            # سطوح اصلاحی (بالای قیمت فعلی) - مقاومت
            retrace = low_price + (diff * ratio)
            levels.append(FibonacciLevel(
                ratio=ratio,
                ratio_name=name,
                price_level=round(retrace, 4),
                is_support=False,
                is_resistance=True,
                scale_used=ScaleType.LINEAR
            ))
            
            # سطوح توسعه (پایین قیمت فعلی) - حمایت
            extension = low_price - (diff * ratio)
            levels.append(FibonacciLevel(
                ratio=ratio,
                ratio_name=f"{name} (Ext)",
                price_level=round(extension, 4),
                is_support=True,
                is_resistance=False,
                scale_used=ScaleType.LINEAR
            ))
    
    return levels


# ════════════════════════════════════════════════════════════════
# بخش ۴: محاسبه سطوح فیبوناچی – مقیاس لگاریتمی (صفحه ۵۰-۵۱)
# ════════════════════════════════════════════════════════════════

def calculate_fibonacci_logarithmic(
    start_price: float,
    end_price: float,
    is_uptrend: bool = True
) -> List[FibonacciLevel]:
    """
    محاسبه سطوح فیبوناچی با مقیاس لگاریتمی.
    
    فرمول‌های صفحه ۵۰-۵۱:
    
    برای محاسبه سطح پایین‌تر (C) از نقطه مرجع (B):
        log(B/C) = F * log(B/A)
        
    برای محاسبه سطح بالاتر (D) از نقطه مرجع (C):
        log(C/D) = F * log(A/B)
        
    یا:
        log(C/B) = F * log(A/B)
    
    که در آن:
        A = قیمت شروع موج
        B = قیمت پایان موج (نقطه مرجع)
        C = سطح پایین‌تر هدف
        D = سطح بالاتر هدف
        F = نسبت فیبوناچی
    
    در عمل:
        اگر C < B (سطح پایین‌تر):
            C = B * (B/A)^(-F)
        
        اگر D > B (سطح بالاتر):
            D = B * (B/A)^(F)
    
    پیاده‌سازی با استفاده از روابط لگاریتمی:
        log(B/C) = F * log(B/A)  →  B/C = (B/A)^F  →  C = B / (B/A)^F
        log(D/C) = F * log(A/B)  →  D/C = (A/B)^F  →  D = C * (A/B)^F
    """
    levels = []
    
    if start_price <= 0 or end_price <= 0:
        return calculate_fibonacci_linear(start_price, end_price, is_uptrend)
    
    ratios = [
        (0.236, "23.6%"),
        (0.382, "38.2%"),
        (0.500, "50.0%"),
        (0.618, "61.8%"),
        (0.786, "78.6%"),
        (1.000, "100%"),
        (1.272, "127.2%"),
        (1.618, "161.8%"),
        (2.000, "200%"),
        (2.618, "261.8%"),
    ]
    
    # نسبت B/A در مقیاس لگاریتمی
    ratio_ba = end_price / start_price
    
    if is_uptrend:
        # روند صعودی: A = پایین، B = بالا
        base_price = end_price
        
        for fib, name in ratios:
            # سطح پایین‌تر (اصلاحی) - با فرمول: C = B / (B/A)^F
            lower_price = base_price / (ratio_ba ** fib)
            levels.append(FibonacciLevel(
                ratio=fib,
                ratio_name=f"{name}",
                price_level=round(lower_price, 4),
                is_support=True,
                is_resistance=False,
                scale_used=ScaleType.LOGARITHMIC
            ))
            
            # سطح بالاتر (توسعه) - با فرمول: D = B * (B/A)^F
            higher_price = base_price * (ratio_ba ** fib)
            levels.append(FibonacciLevel(
                ratio=fib,
                ratio_name=f"{name} (Ext)",
                price_level=round(higher_price, 4),
                is_support=False,
                is_resistance=True,
                scale_used=ScaleType.LOGARITHMIC
            ))
    else:
        # روند نزولی: A = بالا، B = پایین
        base_price = end_price
        ratio_ab = start_price / end_price  # A/B (بزرگتر از 1)
        
        for fib, name in ratios:
            # سطح بالاتر (اصلاحی) - مقاومت
            higher_price = base_price * (ratio_ab ** fib)
            levels.append(FibonacciLevel(
                ratio=fib,
                ratio_name=f"{name}",
                price_level=round(higher_price, 4),
                is_support=False,
                is_resistance=True,
                scale_used=ScaleType.LOGARITHMIC
            ))
            
            # سطح پایین‌تر (توسعه) - حمایت
            lower_price = base_price / (ratio_ab ** fib)
            levels.append(FibonacciLevel(
                ratio=fib,
                ratio_name=f"{name} (Ext)",
                price_level=round(lower_price, 4),
                is_support=True,
                is_resistance=False,
                scale_used=ScaleType.LOGARITHMIC
            ))
    
    return levels


# ════════════════════════════════════════════════════════════════
# بخش ۵: تبدیل قیمت‌ها بین مقیاس‌های خطی و لگاریتمی
# ════════════════════════════════════════════════════════════════

def to_log_price(price: float, base: Optional[float] = None) -> float:
    """تبدیل قیمت به مقیاس لگاریتمی"""
    if price <= 0:
        return 0
    if base is not None and base > 0:
        return math.log(price / base)
    return math.log(price)


def from_log_price(log_price: float, base: Optional[float] = None) -> float:
    """تبدیل از مقیاس لگاریتمی به قیمت واقعی"""
    if base is not None and base > 0:
        return base * math.exp(log_price)
    return math.exp(log_price)


def convert_price_series(
    prices: np.ndarray,
    to_log: bool = True,
    base: Optional[float] = None
) -> np.ndarray:
    """
    تبدیل کل سری قیمت به مقیاس دیگر.
    
    پارامترها:
        prices: آرایه قیمت‌ها
        to_log: True = تبدیل به لگاریتم، False = تبدیل از لگاریتم
        base: پایه برای تبدیل (اختیاری)
    
    خروجی:
        آرایه تبدیل‌شده
    """
    result = []
    for p in prices:
        if to_log:
            if base is not None:
                result.append(math.log(p / base) if p > 0 and base > 0 else 0)
            else:
                result.append(math.log(p) if p > 0 else 0)
        else:
            if base is not None:
                result.append(base * math.exp(p))
            else:
                result.append(math.exp(p))
    return np.array(result)


# ════════════════════════════════════════════════════════════════
# بخش ۶: محاسبه سطوح فیبوناچی با تشخیص خودکار مقیاس
# ════════════════════════════════════════════════════════════════

def calculate_fibonacci_levels(
    start_price: float,
    end_price: float,
    high_price: float,
    low_price: float,
    scale_type: ScaleType = ScaleType.AUTO,
    is_uptrend: Optional[bool] = None
) -> Dict:
    """
    محاسبه سطوح فیبوناچی با مقیاس مناسب.
    
    مطابق صفحه ۴۹ و ۵۰-۵۱:
        - تشخیص خودکار نیاز به مقیاس لگاریتمی
        - محاسبه سطوح با فرمول صحیح
    
    پارامترها:
        start_price: قیمت شروع موج
        end_price: قیمت پایان موج
        high_price: بالاترین قیمت در بازه
        low_price: پایین‌ترین قیمت در بازه
        scale_type: نوع مقیاس (خودکار/حسابی/لگاریتمی)
        is_uptrend: جهت روند (اگر None باشد از مقایسه start/end تشخیص داده می‌شود)
    
    خروجی:
        دیکشنری شامل سطوح، نوع مقیاس و توضیحات
    """
    if is_uptrend is None:
        is_uptrend = end_price > start_price
    
    # ── تشخیص مقیاس ───────────────────────────────────────────
    if scale_type == ScaleType.AUTO:
        used_scale, scale_reason = determine_scale_type(high_price, low_price)
    else:
        used_scale = scale_type
        scale_reason = f"مقیاس {used_scale.value} توسط کاربر انتخاب شده"
    
    # ── محاسبه سطوح بر اساس مقیاس ────────────────────────────
    if used_scale == ScaleType.LOGARITHMIC:
        levels = calculate_fibonacci_logarithmic(start_price, end_price, is_uptrend)
    else:
        levels = calculate_fibonacci_linear(start_price, end_price, is_uptrend)
    
    # ── تفکیک سطوح ────────────────────────────────────────────
    supports = [l for l in levels if l.is_support]
    resistances = [l for l in levels if l.is_resistance]
    
    return {
        "scale_used": used_scale,
        "scale_reason": scale_reason,
        "is_uptrend": is_uptrend,
        "start_price": round(start_price, 4),
        "end_price": round(end_price, 4),
        "price_range": round(abs(end_price - start_price), 4),
        "percent_change": round((end_price - start_price) / start_price * 100, 2) if start_price > 0 else 0,
        "high_price": round(high_price, 4),
        "low_price": round(low_price, 4),
        "price_ratio": round(high_price / low_price, 2) if low_price > 0 else 0,
        "supports": supports,
        "resistances": resistances,
        "all_levels": levels,
    }


# ════════════════════════════════════════════════════════════════
# بخش ۷: تابع analyze (interface اصلی برای main.py)
# ════════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None) -> Dict:
    """
    فصل ۸: نمودار لگاریتمی یا حسابی (Logarithmic or Arithmetic)
    
    پیاده‌سازی کامل مطابق صفحات ۴۹-۵۱ کتاب گلن نیلی.
    
    این تابع:
        ۱. محدوده قیمتی داده را تحلیل می‌کند
        ۲. تشخیص می‌دهد که آیا به مقیاس لگاریتمی نیاز است یا خیر
        ۳. سطوح فیبوناچی را با مقیاس صحیح محاسبه می‌کند
        ۴. توصیه مقیاس مناسب برای نمودار را ارائه می‌دهد
    
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
    open_prices = data['open'].values if 'open' in data.columns else data['Open'].values
    
    n = len(close)
    
    if n < 2:
        return {
            "عنوان": "فصل ۸: نمودار لگاریتمی یا حسابی",
            "وضعیت": "داده_کافی_نیست",
            "تعداد_کندل": str(n),
            "پیام": "برای تحلیل حداقل ۲ کندل لازم است"
        }
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۲: تحلیل محدوده قیمتی کل داده
    # ════════════════════════════════════════════════════════════
    global_range = analyze_price_range(close)
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۳: تحلیل محدوده قیمتی آخرین N کندل
    # ════════════════════════════════════════════════════════════
    lookback_options = [50, 100, 200, 500]
    ranges_by_lookback = {}
    
    for lb in lookback_options:
        if n >= lb:
            ranges_by_lookback[lb] = analyze_price_range(close, lookback=lb)
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۴: تشخیص روند کلی
    # ════════════════════════════════════════════════════════════
    first_price = float(close[0])
    last_price = float(close[-1])
    is_uptrend = last_price > first_price
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۵: محاسبه سطوح فیبوناچی با مقیاس مناسب
    # ════════════════════════════════════════════════════════════
    fib_result = calculate_fibonacci_levels(
        start_price=first_price,
        end_price=last_price,
        high_price=float(np.max(high)),
        low_price=float(np.min(low)),
        scale_type=ScaleType.AUTO,
        is_uptrend=is_uptrend
    )
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۶: محاسبه مقایسه‌ای سطوح فیبوناچی در هر دو مقیاس
    # ════════════════════════════════════════════════════════════
    linear_fib = calculate_fibonacci_levels(
        start_price=first_price,
        end_price=last_price,
        high_price=float(np.max(high)),
        low_price=float(np.min(low)),
        scale_type=ScaleType.LINEAR,
        is_uptrend=is_uptrend
    )
    
    log_fib = calculate_fibonacci_levels(
        start_price=first_price,
        end_price=last_price,
        high_price=float(np.max(high)),
        low_price=float(np.min(low)),
        scale_type=ScaleType.LOGARITHMIC,
        is_uptrend=is_uptrend
    )
    
    # ── تفاوت بین سطوح کلیدی در دو مقیاس ──────────────────────
    key_ratios = ["23.6%", "38.2%", "50.0%", "61.8%", "78.6%", "100%", "161.8%", "261.8%"]
    scale_comparison = []
    
    for ratio_name in key_ratios:
        linear_levels = [l for l in linear_fib["all_levels"] if ratio_name in l.ratio_name]
        log_levels = [l for l in log_fib["all_levels"] if ratio_name in l.ratio_name]
        
        if linear_levels and log_levels:
            linear_price = linear_levels[0].price_level
            log_price = log_levels[0].price_level
            diff_percent = abs(linear_price - log_price) / max(linear_price, log_price) * 100 if max(linear_price, log_price) > 0 else 0
            
            scale_comparison.append({
                "ratio": ratio_name,
                "linear_price": round(linear_price, 4),
                "log_price": round(log_price, 4),
                "difference_percent": round(diff_percent, 2),
                "significant": diff_percent > 5
            })
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۷: ساخت خروجی
    # ════════════════════════════════════════════════════════════
    results = {
        # ── شناسنامه ──
        "عنوان": "فصل ۸: نمودار لگاریتمی یا حسابی",
        "مرجع_کتاب": "صفحات ۴۹-۵۱ - گلن نیلی",
        "وضعیت": "تحلیل_کامل",
        
        # ── اطلاعات پایه ──
        "تعداد_کندل": str(n),
        "قیمت_شروع": str(round(first_price, 4)),
        "قیمت_پایانی": str(round(last_price, 4)),
        "بالاترین_قیمت": str(round(float(np.max(high)), 4)),
        "پایین‌ترین_قیمت": str(round(float(np.min(low)), 4)),
        "نسبت_بالا_به_پایین": str(round(global_range.ratio, 2)),
        "تغییر_کل_درصد": f"{((last_price - first_price) / first_price * 100) if first_price > 0 else 0:+.2f}%",
        
        # ── تشخیص مقیاس ──
        "مقیاس_توصیه‌شده": global_range.use_log_scale,
        "مقیاس_توصیه_نوع": "لگاریتمی" if global_range.use_log_scale else "حسابی",
        "دلیل_توصیه": global_range.reason,
        
        # ── قانون دو برابر (صفحه ۴۹) ──
        "قانون_دو_برابر": "قیمت بالا بیش از دو برابر قیمت پایین است - مقیاس لگاریتمی مناسب است" if global_range.ratio >= 2.0 else "قیمت بالا کمتر از دو برابر قیمت پایین است - مقیاس حسابی کافی است",
        "نسبت_قیمت_بالا_به_پایین": f"{global_range.ratio:.2f}",
        
        # ── سطوح فیبوناچی با مقیاس مناسب ──
        "نوع_مقیاس_استفاده‌شده": fib_result["scale_used"].value,
        "دلیل_انتخاب_مقیاس": fib_result["scale_reason"],
        "جهت_روند": "صعودی" if fib_result["is_uptrend"] else "نزولی",
        
        # ── فرمول‌های صفحه ۵۰-۵۱ ──
        "فرمول_حسابی_پایین‌تر": "C = B - F × Δ",
        "فرمول_حسابی_بالاتر": "D = C + F × Δ",
        "فرمول_لگاریتمی_پایین‌تر": "log(B/C) = F × log(B/A)  →  C = B / (B/A)^F",
        "فرمول_لگاریتمی_بالاتر": "log(C/D) = F × log(A/B)  →  D = C × (A/B)^F",
        
        # ── سطوح حمایت و مقاومت ──
        "تعداد_سطوح_حمایت": str(len(fib_result["supports"])),
        "تعداد_سطوح_مقاومت": str(len(fib_result["resistances"])),
    }
    
    # ── اضافه کردن سطوح کلیدی حمایت ───────────────────────────
    for i, level in enumerate(fib_result["supports"][:10]):
        prefix = f"حمایت_{i+1}"
        results[f"{prefix}_نسبت"] = level.ratio_name
        results[f"{prefix}_قیمت"] = str(level.price_level)
    
    # ── اضافه کردن سطوح کلیدی مقاومت ──────────────────────────
    for i, level in enumerate(fib_result["resistances"][:10]):
        prefix = f"مقاومت_{i+1}"
        results[f"{prefix}_نسبت"] = level.ratio_name
        results[f"{prefix}_قیمت"] = str(level.price_level)
    
    # ── اضافه کردن مقایسه مقیاس‌ها برای سطوح مهم ──────────────
    for comp in scale_comparison[:8]:
        prefix = f"مقایسه_فیبو_{comp['ratio'].replace('%', '').replace('.', '_')}"
        results[f"{prefix}_خطی"] = str(comp["linear_price"])
        results[f"{prefix}_لگاریتمی"] = str(comp["log_price"])
        results[f"{prefix}_تفاوت"] = f"{comp['difference_percent']}%"
        results[f"{prefix}_توجه"] = "⚠️ تفاوت قابل توجه" if comp["significant"] else "تفاوت ناچیز"
    
    # ── اصول کلیدی از کتاب ──
    results["اصل_1"] = "در حالت ایده آل، تمام نمودارها باید به صورت لگاریتمی ترسیم شوند"
    results["اصل_2"] = "اگر قیمت بالا بیش از دو برابر قیمت پایین باشد، نمودار لگاریتمی مناسب است"
    results["اصل_3"] = "رشد قیمت‌ها به صورت درصدی رخ می‌دهد، نه خطی"
    results["اصل_4"] = "روابط فیبوناچی باید بر اساس فاصله فیزیکی در نمودار لگاریتمی مقایسه شوند"
    
    # ── تفسیر نهایی ──
    results["تفسیر_نهایی"] = _build_final_interpretation(
        results, global_range, fib_result, scale_comparison
    )

    # ⭐ داده‌های خام برای استفاده فصل‌های دیگر
    results["_scale_info"] = "ذخیره‌شده"  # فقط برای نمایش
    results["_scale_type"] = fib_result["scale_used"].value
    results["_is_log_recommended"] = "بله" if global_range.use_log_scale else "خیر"
    results["_price_ratio"] = round(global_range.ratio, 2)
    
    # ── ثبت در لاگ ──
    if logger:
        _write_to_logger(logger, results, fib_result, scale_comparison)
    
    return results


# ════════════════════════════════════════════════════════════════
# بخش ۸: تفسیر نهایی
# ════════════════════════════════════════════════════════════════

def _build_final_interpretation(
    results: Dict,
    global_range: PriceRange,
    fib_result: Dict,
    scale_comparison: List[Dict]
) -> str:
    """تولید تفسیر متنی کامل مطابق کتاب"""
    
    if global_range.use_log_scale:
        scale_icon = "📐"
        scale_text = "مقیاس لگاریتمی توصیه می‌شود"
        warning = ""
    else:
        scale_icon = "📏"
        scale_text = "مقیاس حسابی کافی است"
        warning = ""
    
    # ── بررسی تفاوت‌های قابل توجه ──
    significant_diffs = [c for c in scale_comparison if c.get("significant", False)]
    diff_warning = ""
    if significant_diffs:
        diff_warning = f"\n  ⚠️ توجه: تفاوت قابل توجه بین سطوح فیبوناچی در مقیاس‌های مختلف برای نسبت‌های {', '.join([c['ratio'] for c in significant_diffs[:3]])}"
    
    return f"""
═══════════════════════════════════════════════════════════════════
  فصل ۸: نمودار لگاریتمی یا حسابی (Logarithmic or Arithmetic)
  مرجع: صفحات ۴۹-۵۱ | گلن نیلی | سبک نئوویو
═══════════════════════════════════════════════════════════════════

📐 {scale_icon} {scale_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 محدوده قیمتی داده:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • بالاترین قیمت: {global_range.high_price:.4f}
  • پایین‌ترین قیمت: {global_range.low_price:.4f}
  • نسبت بالا به پایین: {global_range.ratio:.2f}
  • {results.get('قانون_دو_برابر', '')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 قانون کلیدی صفحه ۴۹:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  "اگر قیمت بالا بیش از دو برابر ارزش قیمت پایین باشد،
   نمودار لگاریتمی برای شمارش موجی و کانال بندی دقیق مناسب است.
   هر چقدر اختلاف درصد بین سطح قیمت بالا و پایین بیشتر باشد،
   اهمیت استفاده از مقیاس لگاریتمی بیشتر است."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔢 فرمول‌های محاسبه (صفحات ۵۰-۵۱):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  مقیاس حسابی (Linear):
    C = B - F × Δ    (سطح پایین‌تر)
    D = C + F × Δ    (سطح بالاتر)

  مقیاس لگاریتمی (Logarithmic):
    log(B/C) = F × log(B/A)  →  C = B / (B/A)^F
    log(C/D) = F × log(A/B)  →  D = C × (A/B)^F

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 سطوح فیبوناچی کلیدی (با مقیاس {fib_result['scale_used'].value}):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  سطوح حمایت (Support):
"""
    + "\n".join([f"    • {l.ratio_name}: {l.price_level:.4f}" for l in fib_result["supports"][:6]]) + f"""

  سطوح مقاومت (Resistance):"""
    + "\n".join([f"    • {l.ratio_name}: {l.price_level:.4f}" for l in fib_result["resistances"][:6]]) + f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚖️ مقایسه سطوح فیبوناچی در دو مقیاس:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    + "\n".join([f"  • {c['ratio']}: خطی={c['linear_price']:.4f} | لگاریتمی={c['log_price']:.4f} | تفاوت={c['difference_percent']}%" for c in scale_comparison[:8]]) + f"""
{diff_warning}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 نتیجه نئوویو:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {results.get('دلیل_توصیه', '')}
  
  {results.get('اصل_1', '')}
  {results.get('اصل_2', '')}
  {results.get('اصل_3', '')}
  {results.get('اصل_4', '')}

⚠️ نکته مهم (صفحه ۴۹):
   "رسانه‌ها دوست دارند نمودارهای حسابی بلند مدت را ارائه دهند،
    چرا که آنها یک اثر چشمگیر را ایجاد می‌کنند و پیشرفت‌های اخیر
    بازار را بزرگنمایی می‌کنند. در حالی که در بازار، آنچه نشاندهنده
    واقعیت میباشد درصد افزایش یا کاهش سرمایه افراد میباشد نه مبلغ."

═══════════════════════════════════════════════════════════════════
"""


# ════════════════════════════════════════════════════════════════
# بخش ۹: ثبت در لاگ
# ════════════════════════════════════════════════════════════════

def _write_to_logger(logger, results: Dict, fib_result: Dict, scale_comparison: List[Dict]):
    """ثبت نتایج در لاگر"""
    logger.add_section("فصل ۸: نمودار لگاریتمی یا حسابی", level=1)
    logger.add_result("مرجع کتاب", "صفحات ۴۹-۵۱ - گلن نیلی")
    logger.add_result("تعداد کندل", results["تعداد_کندل"])
    logger.add_result("نسبت بالا به پایین", results["نسبت_بالا_به_پایین"])
    logger.add_result("مقیاس توصیه‌شده", results["مقیاس_توصیه_نوع"])
    logger.add_result("دلیل توصیه", results["دلیل_توصیه"])
    logger.add_result("نوع مقیاس استفاده‌شده", results["نوع_مقیاس_استفاده‌شده"])
    
    logger.add_section("قانون دو برابر (صفحه ۴۹)", level=2)
    logger.add_result("قانون", results["قانون_دو_برابر"])
    
    logger.add_section("فرمول‌های صفحه ۵۰-۵۱", level=2)
    logger.add_result("حسابی - سطح پایین‌تر", results["فرمول_حسابی_پایین‌تر"])
    logger.add_result("حسابی - سطح بالاتر", results["فرمول_حسابی_بالاتر"])
    logger.add_result("لگاریتمی - سطح پایین‌تر", results["فرمول_لگاریتمی_پایین‌تر"])
    logger.add_result("لگاریتمی - سطح بالاتر", results["فرمول_لگاریتمی_بالاتر"])
    
    logger.add_section("سطوح فیبوناچی", level=2)
    for i in range(min(5, len(fib_result["supports"]))):
        logger.add_result(
            f"حمایت {i+1}",
            f"{results[f'حمایت_{i+1}_نسبت']}: {results[f'حمایت_{i+1}_قیمت']}"
        )
    for i in range(min(5, len(fib_result["resistances"]))):
        logger.add_result(
            f"مقاومت {i+1}",
            f"{results[f'مقاومت_{i+1}_نسبت']}: {results[f'مقاومت_{i+1}_قیمت']}"
        )
    
    logger.add_section("اصول کتاب", level=2)
    for i in range(1, 5):
        logger.add_result(f"اصل {i}", results.get(f"اصل_{i}", ""))
    
    logger.add_result("تفسیر نهایی", results["تفسیر_نهایی"])


# ════════════════════════════════════════════════════════════════
# اجرای مستقیم برای تست
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # ایجاد داده تست با نسبت قیمت بالا (بیت‌کوین مانند)
    test_data = pd.DataFrame({
        "close": [10000, 10500, 10200, 10800, 10600, 11000, 11500, 11200, 11800, 12000],
        "high": [10200, 10600, 10400, 10900, 10700, 11200, 11600, 11400, 11900, 12100],
        "low": [9900, 10400, 10100, 10700, 10500, 10900, 11400, 11100, 11700, 11900],
        "open": [10000, 10500, 10200, 10800, 10600, 11000, 11500, 11200, 11800, 12000],
    })
    
    result = analyze(test_data)
    print(result["تفسیر_نهایی"])