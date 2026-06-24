"""
فصل ۱۴: تحلیل نسبت‌های فیبوناچی (Ratio Analysis)
منبع: کتاب "استادی در امواج الیوت" - گلن نیلی (NeoWave)
صفحات: ۳۳۰ تا ۳۴۲

اصلاحات تحلیلی اعمال‌شده (بر اساس دستورالعمل):
═══════════════════════════════════════════════════════════════════
۱. شناسایی امواج بر اساس Pivot High/Low (الگوریتم نقاط چرخش قیمت)
   - حذف کامل روش تقسیم زمانی مساوی
   - استفاده از left_bars=2 و right_bars=2 برای تأیید نقاط چرخش
   - محاسبه قدرت (Strength) هر نقطه چرخش

۲. پشتیبانی از مقیاس لگاریتمی (use_log=True)
   - فرمول: log_price_range = abs(log(end) - log(start))
   - محاسبه سطوح فیبوناچی با فرمول لگاریتمی

۳. تلورانس فیبوناچی پویا (Dynamic Tolerance)
   - حداقل ۳٪ (0.03)
   - افزایش بر اساس دامنه قیمتی موج (volatility)
   - حداکثر ۱۰٪ (0.10)

۴. قوانین امتداد (Extension) کامل
   - موج ۱ ممتد: انتهای موج ۲ کل الگو را به نسبت طلایی تقسیم می‌کند
   - موج ۳ ممتد: موج ۳ ≥ ۱۶۱.۸٪ موج ۱
   - موج ۵ ممتد: دو شرط (۱) ≥ ۱۶۱.۸٪ موج ۳ و (۲) ≥ ۱۰۰٪ فاصله ۱-۳

۵. محاسبه صحیح نسبت خارجی (External Ratio)
   - بر اساس پروجکشن از انتهای موج مبنا
   - در نظر گرفتن جهت حرکت موج هدف

۶. تمایز نسبت داخلی و خارجی بر اساس همپوشانی
   - Internal: فقط با همپوشانی قیمتی
   - External: فقط بدون همپوشانی قیمتی

۷. ساختار داخلی (Sub-waves)
   - شناسایی خودکار ریزموج‌ها
   - بررسی ساختار ۵تایی یا ۳تایی

۸. تصحیح خطاهای املایی
   - تمام کامنت‌ها و پیام‌ها اصلاح شده‌اند
═══════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
import math
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


# ══════════════════════════════════════════════════════════════════
# ۱. تعاریف پایه و نسبت‌های فیبوناچی (صفحات ۳۳۰-۳۳۱)
# ══════════════════════════════════════════════════════════════════

class FibRatioType(Enum):
    """نوع نسبت فیبوناچی"""
    INTERNAL = "internal"   # نسبت داخلی - با همپوشانی قیمتی
    EXTERNAL = "external"   # نسبت خارجی - بدون همپوشانی قیمتی


class WavePattern(Enum):
    """نوع الگوی موجی (صفحات ۳۳۴-۳۴۲)"""
    IMPULSE = "impulse"           # الگوی شتابدار
    ZIGZAG = "zigzag"             # زیگزاگ (صفحه ۳۴۰)
    FLAT = "flat"                 # مسطح (صفحه ۳۴۱)
    TRIANGLE = "triangle"         # مثلث (صفحه ۳۴۲)
    DOUBLE_THREE = "double_three" # ترکیبی دوگانه
    TRIPLE_THREE = "triple_three" # ترکیبی سه‌گانه
    UNKNOWN = "unknown"


# نسبت‌های فیبوناچی استاندارد نئوویو (صفحه ۳۳۰)
FIB_RATIOS = {
    0.236: 3,      # 3/13
    0.382: 5,      # 5/13
    0.500: 8,      # 8/16 (نسبت میانی)
    0.618: 13,     # 13/21 (نسبت طلایی)
    0.786: 21,     # 21/27
    1.000: 34,     # نسبت پایه
    1.272: 55,     # 55/43
    1.618: 89,     # 89/55 (نسبت طلایی معکوس)
    2.000: 144,    # 144/72 (نسبت دو برابر)
    2.618: 233,    # 233/89
}

KEY_FIB_RATIOS = sorted(FIB_RATIOS.keys())

# تلورانس پایه فیبوناچی - حداقل ۳٪ (صفحه ۳۳۰، مفهوم "Zone")
BASE_TOLERANCE = 0.03
MAX_TOLERANCE = 0.10  # حداکثر تلورانس برای نوسانات بالا


@dataclass
class PivotPoint:
    """
    نقطه چرخش قیمتی (Pivot High/Low)
    شناسایی شده بر اساس مقایسه با کندل‌های اطراف
    """
    price: float
    index: int
    is_high: bool  # True = Pivot High, False = Pivot Low
    strength: int = 1  # تعداد کندل‌های تأیید


@dataclass
class WavePoint:
    """نقطه موج با قیمت و اندیس زمانی"""
    price: float
    index: int
    label: str = ""  # نام موج (مثلاً "1", "2", "a", "b", "c")
    
    @property
    def log_price(self) -> float:
        """قیمت لگاریتمی برای محاسبات بلندمدت"""
        return math.log(self.price) if self.price > 0 else 0.0


@dataclass
class WaveSegment:
    """
    یک بخش از موج با نقطه شروع و پایان
    
    ویژگی‌ها:
    - price_range: دامنه قیمتی حسابی
    - log_price_range: دامنه قیمتی لگاریتمی
    - has_5_subwaves: آیا ساختار ۵تایی دارد
    - has_3_subwaves: آیا ساختار ۳تایی دارد
    """
    start: WavePoint
    end: WavePoint
    label: str = ""
    sub_waves: List['WaveSegment'] = field(default_factory=list)  # ساختار داخلی
    
    @property
    def price_range(self) -> float:
        """دامنه قیمتی موج (مقیاس حسابی)"""
        return abs(self.end.price - self.start.price)
    
    @property
    def log_price_range(self) -> float:
        """دامنه قیمتی لگاریتمی (برای مقیاس لگاریتمی)"""
        if self.start.price <= 0 or self.end.price <= 0:
            return 0.0
        return abs(math.log(self.end.price) - math.log(self.start.price))
    
    @property
    def direction(self) -> str:
        """جهت موج: UP یا DOWN"""
        return "UP" if self.end.price > self.start.price else "DOWN"
    
    @property
    def length(self) -> int:
        """تعداد کندل‌های موج"""
        return abs(self.end.index - self.start.index)
    
    @property
    def has_5_subwaves(self) -> bool:
        """
        آیا موج از ۵ ریزموج تشکیل شده است (ساختار شتابدار)
        طبق صفحه ۳۳۰: موج شتابدار از ۵ ریزموج تشکیل می‌شود
        """
        if len(self.sub_waves) < 5:
            return False
        dirs = [w.direction for w in self.sub_waves[:5]]
        return dirs in [["UP", "DOWN", "UP", "DOWN", "UP"],
                        ["DOWN", "UP", "DOWN", "UP", "DOWN"]]
    
    @property
    def has_3_subwaves(self) -> bool:
        """
        آیا موج از ۳ ریزموج تشکیل شده است (ساختار اصلاحی)
        طبق صفحه ۳۳۰: موج اصلاحی از ۳ ریزموج تشکیل می‌شود
        """
        if len(self.sub_waves) < 3:
            return False
        dirs = [w.direction for w in self.sub_waves[:3]]
        return dirs in [["UP", "DOWN", "UP"], ["DOWN", "UP", "DOWN"]]


@dataclass
class FibLevel:
    """یک سطح فیبوناچی با مقدار و توضیحات"""
    ratio: float
    price: float
    level_type: FibRatioType
    description: str = ""
    is_log_scale: bool = False


# ══════════════════════════════════════════════════════════════════
# ۲. شناسایی امواج بر اساس Pivot Points (صفحات ۳۳۲-۳۳۳)
# ══════════════════════════════════════════════════════════════════

class PivotDetector:
    """
    شناسایی نقاط چرخش قیمتی (Pivot High/Low)
    جایگزین روش تقسیم زمانی مساوی
    
    طبق صفحه ۳۳۲: نقاط چرخش بر اساس تغییرات قیمت شناسایی می‌شوند
    """
    
    def __init__(self, data: pd.DataFrame, left_bars: int = 2, right_bars: int = 2):
        """
        پارامترها:
            data: DataFrame با ستون‌های high و low
            left_bars: تعداد کندل‌های سمت چپ برای تأیید
            right_bars: تعداد کندل‌های سمت راست برای تأیید
        """
        self.data = data.copy()
        self.high = data["high"].values if "high" in data.columns else data["High"].values
        self.low = data["low"].values if "low" in data.columns else data["Low"].values
        self.n = len(self.high)
        self.left_bars = left_bars
        self.right_bars = right_bars
    
    def find_pivots(self) -> List[PivotPoint]:
        """
        یافتن تمام نقاط چرخش قیمتی
        
        یک نقطه High به عنوان Pivot High محسوب می‌شود اگر:
        - از left_bars کندل قبلی و right_bars کندل بعدی بالاتر باشد
        
        یک نقطه Low به عنوان Pivot Low محسوب می‌شود اگر:
        - از left_bars کندل قبلی و right_bars کندل بعدی پایین‌تر باشد
        """
        pivots = []
        
        for i in range(self.left_bars, self.n - self.right_bars):
            # بررسی Pivot High
            is_high = True
            for j in range(i - self.left_bars, i + self.right_bars + 1):
                if j == i:
                    continue
                if self.high[j] >= self.high[i]:
                    is_high = False
                    break
            
            if is_high:
                pivots.append(PivotPoint(
                    price=float(self.high[i]),
                    index=i,
                    is_high=True,
                    strength=self._calculate_strength(i, True)
                ))
                continue
            
            # بررسی Pivot Low
            is_low = True
            for j in range(i - self.left_bars, i + self.right_bars + 1):
                if j == i:
                    continue
                if self.low[j] <= self.low[i]:
                    is_low = False
                    break
            
            if is_low:
                pivots.append(PivotPoint(
                    price=float(self.low[i]),
                    index=i,
                    is_high=False,
                    strength=self._calculate_strength(i, False)
                ))
        
        return pivots
    
    def _calculate_strength(self, index: int, is_high: bool) -> int:
        """
        محاسبه قدرت یک نقطه چرخش بر اساس فاصله از نقاط اطراف
        قدرت بیشتر = نقطه معتبرتر
        """
        strength = 1
        price = self.high[index] if is_high else self.low[index]
        
        # بررسی تعداد کندل‌های اطراف که قیمت را تأیید می‌کنند
        for j in range(max(0, index - 10), min(self.n, index + 11)):
            if j == index:
                continue
            if is_high:
                if self.high[j] < price:
                    strength += 1
            else:
                if self.low[j] > price:
                    strength += 1
        
        return min(strength, 10)  # حداکثر قدرت 10
    
    def extract_waves(self, pivots: List[PivotPoint]) -> List[WaveSegment]:
        """
        استخراج امواج از نقاط چرخش
        
        هر دو نقطه چرخش متوالی یک موج را تشکیل می‌دهند
        (صفحه ۳۳۲: هر تغییر جهت = یک تک موج جدید)
        """
        if len(pivots) < 2:
            return []
        
        waves = []
        for i in range(len(pivots) - 1):
            start = WavePoint(
                price=pivots[i].price,
                index=pivots[i].index,
                label=f"{i+1}"
            )
            end = WavePoint(
                price=pivots[i+1].price,
                index=pivots[i+1].index,
                label=f"{i+2}"
            )
            
            wave = WaveSegment(
                start=start,
                end=end,
                label=f"W{i+1}"
            )
            waves.append(wave)
        
        # شناسایی ساختار داخلی (sub-waves) برای هر موج
        self._identify_sub_waves(waves)
        
        return waves
    
    def _identify_sub_waves(self, waves: List[WaveSegment]):
        """
        شناسایی ساختار داخلی (ریزموج‌ها) برای هر موج
        طبق صفحه ۳۳۰: هر موج از ریزموج‌های کوچک‌تر تشکیل می‌شود
        """
        for wave in waves:
            start_idx = wave.start.index
            end_idx = wave.end.index
            
            if end_idx - start_idx > 3:
                # نقاط چرخش داخلی را پیدا کن
                inner_pivots = self.find_pivots_range(start_idx, end_idx)
                if len(inner_pivots) >= 2:
                    sub_waves = []
                    for j in range(len(inner_pivots) - 1):
                        sub_wave = WaveSegment(
                            start=WavePoint(inner_pivots[j].price, inner_pivots[j].index),
                            end=WavePoint(inner_pivots[j+1].price, inner_pivots[j+1].index),
                            label=f"{wave.label}_sub{j+1}"
                        )
                        sub_waves.append(sub_wave)
                    wave.sub_waves = sub_waves
    
    def find_pivots_range(self, start_idx: int, end_idx: int) -> List[PivotPoint]:
        """یافتن نقاط چرخش در یک بازه مشخص"""
        pivots = []
        
        for i in range(start_idx + self.left_bars, end_idx - self.right_bars):
            # بررسی Pivot High
            is_high = True
            for j in range(max(start_idx, i - self.left_bars), min(end_idx, i + self.right_bars + 1)):
                if j == i:
                    continue
                if self.high[j] >= self.high[i]:
                    is_high = False
                    break
            
            if is_high:
                pivots.append(PivotPoint(
                    price=float(self.high[i]),
                    index=i,
                    is_high=True
                ))
                continue
            
            # بررسی Pivot Low
            is_low = True
            for j in range(max(start_idx, i - self.left_bars), min(end_idx, i + self.right_bars + 1)):
                if j == i:
                    continue
                if self.low[j] <= self.low[i]:
                    is_low = False
                    break
            
            if is_low:
                pivots.append(PivotPoint(
                    price=float(self.low[i]),
                    index=i,
                    is_high=False
                ))
        
        return pivots


# ══════════════════════════════════════════════════════════════════
# ۳. کلاس اصلی تحلیل نسبت‌های فیبوناچی
# ══════════════════════════════════════════════════════════════════

class FibonacciRatioAnalyzer:
    """
    تحلیل‌گر نسبت‌های فیبوناچی در نئوویو
    
    این کلاس تمام قوانین و نسبت‌های مطرح شده در فصل ۱۴ کتاب را
    پیاده‌سازی می‌کند.
    """
    
    def __init__(self, data: pd.DataFrame, use_log: bool = False, tolerance: float = BASE_TOLERANCE):
        """
        پارامترها:
            data: DataFrame با ستون‌های open, high, low, close
            use_log: استفاده از مقیاس لگاریتمی برای محاسبات
            tolerance: تلورانس پایه برای تطابق با نسبت‌های فیبوناچی
        """
        self.data = data.copy()
        self.close = data["close"].values if "close" in data.columns else data["Close"].values
        self.high = data["high"].values if "high" in data.columns else data["High"].values
        self.low = data["low"].values if "low" in data.columns else data["Low"].values
        self.n = len(self.close)
        self.use_log = use_log
        self.base_tolerance = tolerance
        
        # ذخیره نتایج تحلیل
        self.analysis_results: Dict[str, Any] = {}
        self.fib_levels: List[FibLevel] = []
        self.wave_patterns: List[Dict] = []
    
    # ─── ۳-۱. توابع کمکی برای محاسبات ──────────────────────────
    
    def _get_range(self, wave: WaveSegment) -> float:
        """دریافت دامنه موج با توجه به مقیاس انتخاب‌شده"""
        if self.use_log:
            return wave.log_price_range
        return wave.price_range
    
    def _get_price_at_ratio(self, start: WavePoint, end: WavePoint, ratio: float) -> float:
        """
        محاسبه قیمت در یک نسبت مشخص بین دو نقطه
        
        مقیاس حسابی: قیمت = شروع + (پایان - شروع) × نسبت
        مقیاس لگاریتمی: log(قیمت) = log(شروع) + (log(پایان) - log(شروع)) × نسبت
        """
        if self.use_log:
            if start.price <= 0 or end.price <= 0:
                return start.price + (end.price - start.price) * ratio
            log_start = math.log(start.price)
            log_end = math.log(end.price)
            log_result = log_start + (log_end - log_start) * ratio
            return math.exp(log_result)
        else:
            return start.price + (end.price - start.price) * ratio
    
    def _get_ratio_between(self, wave1: WaveSegment, wave2: WaveSegment) -> float:
        """
        محاسبه نسبت بین دو موج
        
        نسبت = دامنه موج۲ / دامنه موج۱
        """
        range1 = self._get_range(wave1)
        range2 = self._get_range(wave2)
        
        if range1 == 0:
            return float('inf')
        return range2 / range1
    
    def _dynamic_tolerance(self, wave: WaveSegment) -> float:
        """
        تلورانس پویا بر اساس دامنه قیمتی موج
        
        طبق کتاب (صفحه ۳۳۰، مفهوم "Zone"):
        - حداقل ۳٪ (0.03)
        - با افزایش دامنه قیمتی، تلورانس افزایش می‌یابد
        - حداکثر ۱۰٪ (0.10)
        """
        price_range = self._get_range(wave)
        avg_price = (wave.start.price + wave.end.price) / 2
        
        if avg_price == 0:
            return self.base_tolerance
        
        # محاسبه نوسان‌پذیری نسبی
        vol = price_range / avg_price
        
        # تلورانس = base + (vol * 0.5) اما محدود به max
        dyn = self.base_tolerance + (vol * 0.5)
        return min(max(dyn, self.base_tolerance), MAX_TOLERANCE)
    
    def _is_in_fib_zone(self, value: float, target: float, tolerance: Optional[float] = None) -> bool:
        """
        بررسی قرارگیری مقدار در ناحیه مجاز فیبوناچی
        
        طبق صفحه ۳۳۰: نسبت‌ها در یک "ناحیه" قرار می‌گیرند، نه یک نقطه دقیق
        """
        if tolerance is None:
            tolerance = self.base_tolerance
        return abs(value - target) <= tolerance
    
    def _find_nearest_fib_ratio(self, value: float, wave: Optional[WaveSegment] = None) -> Tuple[float, bool, float]:
        """
        یافتن نزدیک‌ترین نسبت فیبوناچی با تلورانس پویا
        
        خروجی: (نزدیک‌ترین نسبت, آیا در ناحیه مجاز است, تلورانس استفاده‌شده)
        """
        if np.isnan(value) or np.isinf(value):
            return 0.0, False, self.base_tolerance
        
        tol = self._dynamic_tolerance(wave) if wave else self.base_tolerance
        nearest = 0.0
        in_zone = False
        min_diff = float('inf')
        
        for ratio in KEY_FIB_RATIOS:
            diff = abs(value - ratio)
            if diff <= tol and diff < min_diff:
                min_diff = diff
                nearest = ratio
                in_zone = True
        
        # اگر در هیچ منطقه‌ای نبود، نزدیک‌ترین را بدون منطقه برمی‌گردانیم
        if not in_zone:
            for ratio in KEY_FIB_RATIOS:
                diff = abs(value - ratio)
                if diff < min_diff:
                    min_diff = diff
                    nearest = ratio
        
        return nearest, in_zone, tol
    
    def _has_overlap(self, wave1: WaveSegment, wave2: WaveSegment) -> bool:
        """
        بررسی همپوشانی قیمتی بین دو موج
        
        دو موج همپوشانی دارند اگر محدوده قیمتی آنها با هم تداخل داشته باشد
        """
        min1 = min(wave1.start.price, wave1.end.price)
        max1 = max(wave1.start.price, wave1.end.price)
        min2 = min(wave2.start.price, wave2.end.price)
        max2 = max(wave2.start.price, wave2.end.price)
        
        return not (max1 < min2 or max2 < min1)
    
    # ─── ۳-۲. نسبت‌های داخلی (Internal Ratios) ──────────────
    
    def calculate_internal_ratio(self, wave1: WaveSegment, wave2: WaveSegment) -> Dict[str, Any]:
        """
        محاسبه نسبت داخلی بین دو موج (صفحات ۳۳۰-۳۳۱)
        
        نسبت داخلی: مقایسه قیمت دو موج نسبت به هم، با همپوشانی قیمتی
        
        نسبت = دامنه موج۲ / دامنه موج۱
        """
        # بررسی همپوشانی (شرط اصلی نسبت داخلی)
        if not self._has_overlap(wave1, wave2):
            return {
                "type": "internal",
                "ratio": None,
                "error": "امواج همپوشانی ندارند - نسبت داخلی معتبر نیست",
                "note": "برای امواج بدون همپوشانی از نسبت خارجی استفاده کنید"
            }
        
        ratio = self._get_ratio_between(wave1, wave2)
        
        if np.isinf(ratio) or np.isnan(ratio):
            return {
                "type": "internal",
                "ratio": None,
                "error": "دامنه موج اول صفر است"
            }
        
        nearest, in_zone, tol = self._find_nearest_fib_ratio(ratio, wave1)
        
        # بررسی ساختار داخلی (صفحه ۳۳۰)
        wave1_structure = "5_waves" if wave1.has_5_subwaves else ("3_waves" if wave1.has_3_subwaves else "unknown")
        wave2_structure = "5_waves" if wave2.has_5_subwaves else ("3_waves" if wave2.has_3_subwaves else "unknown")
        
        return {
            "type": "internal",
            "ratio": round(ratio, 4),
            "nearest_fib": nearest,
            "is_in_fib_zone": in_zone,
            "tolerance_used": round(tol, 3),
            "wave1_range": round(self._get_range(wave1), 4),
            "wave2_range": round(self._get_range(wave2), 4),
            "wave1_structure": wave1_structure,
            "wave2_structure": wave2_structure,
            "has_overlap": True,
            "use_log_scale": self.use_log,
            "description": f"نسبت داخلی: موج۲ به موج۱ = {ratio:.3f} ≈ {nearest} (منطقه: {in_zone})",
            "fib_series": FIB_RATIOS.get(nearest, "نامشخص")
        }
    
    # ─── ۳-۳. نسبت‌های خارجی (External Ratios) ──────────────
    
    def calculate_external_ratio(self, base_wave: WaveSegment, target_wave: WaveSegment) -> Dict[str, Any]:
        """
        محاسبه نسبت خارجی بین دو موج (صفحات ۳۳۲-۳۳۳)
        
        نسبت خارجی: مبتنی بر عدم همپوشانی قیمتی
        با استفاده از یک مقدار قیمتی مبنا و افزودن یا کسر کردن نسبت‌های فیبوناچی
        
        فرمول (صفحه ۳۳۳):
        - برای موج صعودی: هدف = پایان موج مبنا + (دامنه موج مبنا × نسبت)
        - برای موج نزولی: هدف = پایان موج مبنا - (دامنه موج مبنا × نسبت)
        
        نسبت واقعی = (قیمت هدف - قیمت پایان مبنا) / دامنه مبنا
        """
        # بررسی عدم همپوشانی (شرط اصلی نسبت خارجی)
        if self._has_overlap(base_wave, target_wave):
            return {
                "type": "external",
                "ratio": None,
                "error": "امواج همپوشانی دارند - نسبت خارجی معتبر نیست",
                "note": "برای امواج با همپوشانی از نسبت داخلی استفاده کنید"
            }
        
        base_range = self._get_range(base_wave)
        if base_range == 0:
            return {
                "type": "external",
                "ratio": None,
                "error": "دامنه موج مبنا صفر است"
            }
        
        # تشخیص جهت
        is_up = base_wave.direction == "UP"
        
        # محاسبه نسبت واقعی (پروجکشن از انتهای موج مبنا)
        if is_up:
            actual_ratio = (target_wave.end.price - base_wave.end.price) / base_range
        else:
            actual_ratio = (base_wave.end.price - target_wave.end.price) / base_range
        
        # اگر نسبت منفی شد (هدف در جهت مخالف)، آن را اصلاح می‌کنیم
        if actual_ratio < 0:
            # در عمل پروجکشن معمولاً در همان جهت است
            # اما اگر خلاف جهت بود، قدر مطلق را در نظر می‌گیریم
            actual_ratio = abs(actual_ratio)
        
        nearest, in_zone, tol = self._find_nearest_fib_ratio(actual_ratio, base_wave)
        
        # محاسبه سطوح فیبوناچی برای پروجکشن (صفحه ۳۳۳)
        fib_levels = {}
        for ratio in KEY_FIB_RATIOS:
            if is_up:
                target_price = base_wave.end.price + (base_range * ratio)
            else:
                target_price = base_wave.end.price - (base_range * ratio)
            fib_levels[ratio] = round(target_price, 4)
        
        return {
            "type": "external",
            "base_wave": {
                "start": base_wave.start.price,
                "end": base_wave.end.price,
                "range": round(base_range, 4),
                "direction": base_wave.direction
            },
            "target_wave": {
                "start": target_wave.start.price,
                "end": target_wave.end.price
            },
            "actual_ratio": round(actual_ratio, 4),
            "nearest_fib": nearest,
            "is_in_fib_zone": in_zone,
            "tolerance_used": round(tol, 3),
            "fib_levels": fib_levels,
            "has_overlap": False,
            "use_log_scale": self.use_log,
            "description": f"نسبت خارجی: {actual_ratio:.3f} ≈ {nearest} (منطقه: {in_zone})",
            "warning": self._check_external_warning(base_wave, target_wave, actual_ratio)
        }
    
    def _check_external_warning(self, base_wave: WaveSegment, target_wave: WaveSegment, ratio: float) -> Optional[str]:
        """
        بررسی هشدارهای نسبت خارجی طبق کتاب (صفحه ۳۳۳)
        
        اگر موج C به ورای سطح ۱.۰۰ نسبت خارجی برود،
        می‌تواند هشدار باشد که زیگزاگ بخشی از یک مثلث است.
        """
        if ratio > 1.0:
            return "نسبت خارجی > ۱.۰۰ - می‌تواند نشانه تشکیل مثلث باشد (صفحه ۳۳۳)"
        return None
    
    # ─── ۳-۴. قوانین امتداد (Extension Rules) ──────────────
    
    def analyze_impulse_extensions(self, w1: WaveSegment, w2: WaveSegment,
                                   w3: WaveSegment, w4: WaveSegment,
                                   w5: WaveSegment) -> Dict[str, Any]:
        """
        تحلیل قوانین امتداد در الگوی شتابدار (صفحات ۳۳۶-۳۳۸)
        
        ۱. موج ۱ امتداد یافته (صفحه ۳۳۶):
           - انتهای موج ۲ کل الگو را به نسبت ۶۱.۸٪ یا ۳۸.۲٪ تقسیم می‌کند
        
        ۲. موج ۳ امتداد یافته (صفحه ۳۳۷):
           - موج ۳ حداقل ۱۶۱.۸٪ موج ۱
           - موج ۵ بیش از ۶۱.۸٪ موج ۳ نخواهد بود
        
        ۳. موج ۵ امتداد یافته (صفحه ۳۳۸):
           - شرط ۱: موج ۵ ≥ ۱۶۱.۸٪ موج ۳
           - شرط ۲: موج ۵ ≥ ۱۰۰٪ فاصله شروع موج ۱ تا پایان موج ۳
           - موج ۵ حداکثر ۱۶۱.۸٪ فاصله شروع موج ۱ تا پایان موج ۳
        """
        results = {
            "wave_1_extended": False,
            "wave_3_extended": False,
            "wave_5_extended": False,
            "wave_5_shortened": False,
            "detailed_analysis": {},
            "validation": {
                "w1_rules": [],
                "w3_rules": [],
                "w5_rules": []
            }
        }
        
        # ── محاسبات پایه ──
        range1 = self._get_range(w1)
        range3 = self._get_range(w3)
        range5 = self._get_range(w5)
        
        # موج ۱ تا ۳ (کل حرکت) - برای پروجکشن موج ۵
        wave_1_to_3 = WaveSegment(
            start=w1.start,
            end=w3.end,
            label="1-3"
        )
        range_1_to_3 = self._get_range(wave_1_to_3)
        
        # ── تشخیص موج ۳ امتداد یافته (صفحه ۳۳۷) ──
        if range1 > 0 and range3 / range1 >= 1.618 - self.base_tolerance:
            results["wave_3_extended"] = True
            results["validation"]["w3_rules"].append({
                "rule": "موج ۳ ≥ ۱۶۱.۸٪ موج ۱",
                "value": round(range3 / range1, 3),
                "status": "پاس"
            })
        else:
            results["validation"]["w3_rules"].append({
                "rule": "موج ۳ ≥ ۱۶۱.۸٪ موج ۱",
                "value": round(range3 / range1, 3) if range1 > 0 else 0,
                "status": "نقض - موج ۳ امتداد ندارد"
            })
        
        # ── تشخیص موج ۵ امتداد یافته (صفحه ۳۳۸) ──
        # شرط ۱: موج ۵ ≥ ۱۶۱.۸٪ موج ۳
        # شرط ۲: موج ۵ ≥ ۱۰۰٪ فاصله شروع موج ۱ تا پایان موج ۳
        w5_condition_1 = False
        w5_condition_2 = False
        
        if range3 > 0 and range5 / range3 >= 1.618 - self.base_tolerance:
            w5_condition_1 = True
            results["validation"]["w5_rules"].append({
                "rule": "شرط ۱: موج ۵ ≥ ۱۶۱.۸٪ موج ۳",
                "value": round(range5 / range3, 3),
                "status": "پاس"
            })
        else:
            results["validation"]["w5_rules"].append({
                "rule": "شرط ۱: موج ۵ ≥ ۱۶۱.۸٪ موج ۳",
                "value": round(range5 / range3, 3) if range3 > 0 else 0,
                "status": "نقض"
            })
        
        if range_1_to_3 > 0 and range5 / range_1_to_3 >= 1.0 - self.base_tolerance:
            w5_condition_2 = True
            results["validation"]["w5_rules"].append({
                "rule": "شرط ۲: موج ۵ ≥ ۱۰۰٪ فاصله ۱-۳",
                "value": round(range5 / range_1_to_3, 3),
                "status": "پاس"
            })
        else:
            results["validation"]["w5_rules"].append({
                "rule": "شرط ۲: موج ۵ ≥ ۱۰۰٪ فاصله ۱-۳",
                "value": round(range5 / range_1_to_3, 3) if range_1_to_3 > 0 else 0,
                "status": "نقض"
            })
        
        # موج ۵ حداکثر ۱۶۱.۸٪ فاصله ۱-۳
        if range_1_to_3 > 0 and range5 / range_1_to_3 <= 1.618 + self.base_tolerance:
            results["validation"]["w5_rules"].append({
                "rule": "موج ۵ ≤ ۱۶۱.۸٪ فاصله ۱-۳",
                "value": round(range5 / range_1_to_3, 3),
                "status": "پاس"
            })
        else:
            results["validation"]["w5_rules"].append({
                "rule": "موج ۵ ≤ ۱۶۱.۸٪ فاصله ۱-۳",
                "value": round(range5 / range_1_to_3, 3) if range_1_to_3 > 0 else 0,
                "status": "هشدار - موج ۵ بیش از حد"
            })
        
        if w5_condition_1 and w5_condition_2:
            results["wave_5_extended"] = True
        
        # ── تشخیص موج ۱ امتداد یافته (صفحه ۳۳۶) ──
        # انتهای موج ۲ کل الگو را به نسبت ۶۱.۸٪ یا ۳۸.۲٪ تقسیم می‌کند
        if range_1_to_3 > 0:
            ratio_w2_to_total = self._get_ratio_between(w2, wave_1_to_3)
            
            if self._is_in_fib_zone(ratio_w2_to_total, 0.618) or \
               self._is_in_fib_zone(ratio_w2_to_total, 0.382):
                results["wave_1_extended"] = True
                results["validation"]["w1_rules"].append({
                    "rule": "موج ۲ کل الگو را به نسبت طلایی (۰.۶۱۸ یا ۰.۳۸۲) تقسیم می‌کند",
                    "value": round(ratio_w2_to_total, 3),
                    "status": "پاس"
                })
            else:
                results["validation"]["w1_rules"].append({
                    "rule": "موج ۲ کل الگو را به نسبت طلایی تقسیم می‌کند",
                    "value": round(ratio_w2_to_total, 3),
                    "status": "نقض - احتمالاً موج ۱ امتداد ندارد"
                })
        
        # ── تشخیص موج ۵ کوتاه شده (صفحه ۳۳۳) ──
        if range3 > 0 and range5 < range3 * 0.618:
            results["wave_5_shortened"] = True
            results["validation"]["w5_rules"].append({
                "rule": "موج ۵ کوتاه شده (< ۶۱.۸٪ موج ۳)",
                "value": round(range5 / range3, 3),
                "status": "هشدار تغییر روند"
            })
        
        # ── نتایج نهایی ──
        results["detailed_analysis"] = {
            "range_1": round(range1, 4),
            "range_3": round(range3, 4),
            "range_5": round(range5, 4),
            "range_1_to_3": round(range_1_to_3, 4),
            "w3_w1_ratio": round(range3 / range1, 4) if range1 > 0 else 0,
            "w5_w3_ratio": round(range5 / range3, 4) if range3 > 0 else 0,
            "w5_1to3_ratio": round(range5 / range_1_to_3, 4) if range_1_to_3 > 0 else 0,
            "w2_1to3_ratio": round(self._get_ratio_between(w2, wave_1_to_3), 4) if range_1_to_3 > 0 else 0
        }
        
        # تعیین نوع امتداد غالب
        if results["wave_3_extended"]:
            results["dominant_extension"] = "wave_3"
            results["page_reference"] = "صفحه ۳۳۷"
        elif results["wave_5_extended"]:
            results["dominant_extension"] = "wave_5"
            results["page_reference"] = "صفحه ۳۳۸"
        elif results["wave_1_extended"]:
            results["dominant_extension"] = "wave_1"
            results["page_reference"] = "صفحه ۳۳۶"
        else:
            results["dominant_extension"] = "none"
            results["page_reference"] = "صفحه ۳۳۵ - بدون امتداد مشخص"
        
        return results
    
    # ─── ۳-۵. تحلیل الگوهای اصلاحی (صفحات ۳۴۰-۳۴۲) ──────────
    
    def analyze_zigzag(self, wave_a: WaveSegment, wave_b: WaveSegment,
                       wave_c: WaveSegment) -> Dict[str, Any]:
        """
        تحلیل نسبت‌ها در الگوی زیگزاگ (صفحه ۳۴۰)
        
        - نسبت موثقی بین موج A و B وجود ندارد
        - موج C معمولاً ۱.۰۰ یا ۱.۶۱۸ یا ۲.۶۱۸ برابر موج A است
        """
        results = {
            "wave_pattern": "zigzag",
            "page_reference": "صفحه ۳۴۰",
            "ratios": {},
            "fibonacci_relationships": [],
            "valid": True,
            "violations": []
        }
        
        # ── نسبت موج C به موج A (نسبت خارجی) ──
        ratio_c_to_a = self.calculate_external_ratio(wave_a, wave_c)
        results["ratios"]["c_to_a"] = ratio_c_to_a
        
        if ratio_c_to_a.get("actual_ratio", 0) > 0:
            if ratio_c_to_a["actual_ratio"] < 0.618 - self.base_tolerance:
                results["violations"].append("موج C کمتر از ۶۱.۸٪ موج A است (صفحه ۳۴۰)")
                results["valid"] = False
            else:
                results["fibonacci_relationships"].append(
                    f"موج C = {ratio_c_to_a['actual_ratio']:.3f} × موج A"
                )
        
        # ── نسبت موج B به موج A (معمولاً معتبر نیست - صفحه ۳۴۰) ──
        ratio_b_to_a = self.calculate_internal_ratio(wave_a, wave_b)
        results["ratios"]["b_to_a"] = ratio_b_to_a
        results["fibonacci_relationships"].append(
            f"موج B نسبت به موج A (معمولاً نامعتبر): {ratio_b_to_a.get('description', 'N/A')}"
        )
        
        # ── ساختار داخلی ──
        results["structure"] = {
            "wave_a_structure": "5_waves" if wave_a.has_5_subwaves else ("3_waves" if wave_a.has_3_subwaves else "unknown"),
            "wave_b_structure": "5_waves" if wave_b.has_5_subwaves else ("3_waves" if wave_b.has_3_subwaves else "unknown"),
            "wave_c_structure": "5_waves" if wave_c.has_5_subwaves else ("3_waves" if wave_c.has_3_subwaves else "unknown")
        }
        
        return results
    
    def analyze_flat(self, wave_a: WaveSegment, wave_b: WaveSegment,
                     wave_c: WaveSegment) -> Dict[str, Any]:
        """
        تحلیل نسبت‌ها در الگوی مسطح (صفحه ۳۴۱)
        
        - موج B معمولاً ۱.۰۰ تا ۱.۶۱۸ برابر موج A است
        - موج C معمولاً ۱.۰۰ تا ۱.۶۱۸ برابر موج A است
        """
        results = {
            "wave_pattern": "flat",
            "page_reference": "صفحه ۳۴۱",
            "ratios": {},
            "fibonacci_relationships": [],
            "valid": True,
            "violations": []
        }
        
        # ── نسبت موج B به موج A ──
        ratio_b_to_a = self.calculate_external_ratio(wave_a, wave_b)
        results["ratios"]["b_to_a"] = ratio_b_to_a
        
        if ratio_b_to_a.get("actual_ratio", 0) > 0:
            if ratio_b_to_a["actual_ratio"] < 1.0 - self.base_tolerance:
                results["violations"].append("موج B کمتر از ۱.۰۰ برابر موج A است (صفحه ۳۴۱)")
                results["valid"] = False
            else:
                results["fibonacci_relationships"].append(
                    f"موج B = {ratio_b_to_a['actual_ratio']:.3f} × موج A"
                )
        
        # ── نسبت موج C به موج A ──
        ratio_c_to_a = self.calculate_external_ratio(wave_a, wave_c)
        results["ratios"]["c_to_a"] = ratio_c_to_a
        
        if ratio_c_to_a.get("actual_ratio", 0) > 0:
            if ratio_c_to_a["actual_ratio"] < 1.0 - self.base_tolerance:
                results["violations"].append("موج C کمتر از ۱.۰۰ برابر موج A است (صفحه ۳۴۱)")
                results["valid"] = False
            else:
                results["fibonacci_relationships"].append(
                    f"موج C = {ratio_c_to_a['actual_ratio']:.3f} × موج A"
                )
        
        # ── ساختار داخلی ──
        results["structure"] = {
            "wave_a_structure": "5_waves" if wave_a.has_5_subwaves else ("3_waves" if wave_a.has_3_subwaves else "unknown"),
            "wave_b_structure": "5_waves" if wave_b.has_5_subwaves else ("3_waves" if wave_b.has_3_subwaves else "unknown"),
            "wave_c_structure": "5_waves" if wave_c.has_5_subwaves else ("3_waves" if wave_c.has_3_subwaves else "unknown")
        }
        
        return results
    
    def analyze_triangle(self, waves: List[WaveSegment]) -> Dict[str, Any]:
        """
        تحلیل نسبت‌ها در الگوی مثلث (صفحه ۳۴۲)
        
        - موج a, b, c, d, e
        - نسبت‌های فیبوناچی بین موج‌های متوالی
        """
        if len(waves) < 5:
            return {"error": "الگوی مثلث به ۵ موج نیاز دارد"}
        
        results = {
            "wave_pattern": "triangle",
            "page_reference": "صفحه ۳۴۲",
            "ratios": {},
            "fibonacci_relationships": []
        }
        
        wave_a, wave_b, wave_c, wave_d, wave_e = waves[:5]
        
        # نسبت‌های متوالی (همگی داخلی چون همپوشانی دارند)
        results["ratios"]["b_to_a"] = self.calculate_internal_ratio(wave_a, wave_b)
        results["ratios"]["c_to_a"] = self.calculate_internal_ratio(wave_a, wave_c)
        results["ratios"]["d_to_b"] = self.calculate_internal_ratio(wave_b, wave_d)
        results["ratios"]["e_to_c"] = self.calculate_internal_ratio(wave_c, wave_e)
        
        results["fibonacci_relationships"] = [
            f"b/a: {results['ratios']['b_to_a'].get('description', 'N/A')}",
            f"c/a: {results['ratios']['c_to_a'].get('description', 'N/A')}",
            f"d/b: {results['ratios']['d_to_b'].get('description', 'N/A')}",
            f"e/c: {results['ratios']['e_to_c'].get('description', 'N/A')}"
        ]
        
        return results
    
    # ─── ۳-۶. تحلیل کامل ────────────────────────────────────────
    
    def full_analysis(self, waves: List[WaveSegment],
                      detect_pattern: bool = True) -> Dict[str, Any]:
        """
        تحلیل کامل نسبت‌های فیبوناچی بر روی لیست امواج
        
        خروجی شامل:
        - تحلیل الگوهای شتابدار
        - تحلیل الگوهای اصلاحی (زیگزاگ، مسطح، مثلث)
        - همه نسبت‌های داخلی و خارجی
        - قوانین امتداد
        """
        if len(waves) < 3:
            return {"error": "حداقل ۳ موج برای تحلیل نیاز است"}
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "wave_count": len(waves),
            "use_log_scale": self.use_log,
            "base_tolerance": self.base_tolerance,
            "analyses": {},
            "summary": {},
            "all_ratios": {
                "internal": [],
                "external": []
            }
        }
        
        # ── تشخیص نوع الگو ──
        if detect_pattern:
            pattern_type = self._detect_pattern_type(waves)
            results["pattern_type"] = pattern_type.value
        else:
            pattern_type = WavePattern.UNKNOWN
            results["pattern_type"] = "unknown"
        
        # ── تحلیل بر اساس نوع الگو ──
        if pattern_type == WavePattern.IMPULSE and len(waves) >= 5:
            results["analyses"]["impulse"] = self.analyze_impulse_extensions(
                waves[0], waves[1], waves[2], waves[3], waves[4]
            )
        
        elif pattern_type == WavePattern.ZIGZAG and len(waves) >= 3:
            results["analyses"]["zigzag"] = self.analyze_zigzag(
                waves[0], waves[1], waves[2]
            )
        
        elif pattern_type == WavePattern.FLAT and len(waves) >= 3:
            results["analyses"]["flat"] = self.analyze_flat(
                waves[0], waves[1], waves[2]
            )
        
        elif pattern_type == WavePattern.TRIANGLE and len(waves) >= 5:
            results["analyses"]["triangle"] = self.analyze_triangle(waves[:5])
        
        # ── محاسبه همه نسبت‌ها (با تمایز داخلی/خارجی بر اساس همپوشانی) ──
        for i in range(len(waves) - 1):
            for j in range(i + 1, len(waves)):
                if self._has_overlap(waves[i], waves[j]):
                    ratio = self.calculate_internal_ratio(waves[i], waves[j])
                    if ratio.get("ratio") is not None:
                        results["all_ratios"]["internal"].append({
                            "wave1": i,
                            "wave2": j,
                            "ratio": ratio
                        })
                else:
                    ratio = self.calculate_external_ratio(waves[i], waves[j])
                    if ratio.get("actual_ratio") is not None:
                        results["all_ratios"]["external"].append({
                            "wave1": i,
                            "wave2": j,
                            "ratio": ratio
                        })
        
        # ── خلاصه ──
        results["summary"]["total_internal_ratios"] = len(results["all_ratios"]["internal"])
        results["summary"]["total_external_ratios"] = len(results["all_ratios"]["external"])
        results["summary"]["fib_zone_hits"] = sum(
            1 for r in results["all_ratios"]["internal"]
            if r.get("ratio", {}).get("is_in_fib_zone", False)
        ) + sum(
            1 for r in results["all_ratios"]["external"]
            if r.get("ratio", {}).get("is_in_fib_zone", False)
        )
        
        return results
    
    def _detect_pattern_type(self, waves: List[WaveSegment]) -> WavePattern:
        """تشخیص نوع الگوی موجی بر اساس صفحات ۳۳۴-۳۴۲"""
        if len(waves) >= 5:
            dirs = [w.direction for w in waves[:5]]
            if dirs in [["UP", "DOWN", "UP", "DOWN", "UP"],
                        ["DOWN", "UP", "DOWN", "UP", "DOWN"]]:
                # بررسی همپوشانی موج ۴ با موج ۱
                if self._has_overlap(waves[0], waves[3]):
                    return WavePattern.TRIANGLE
                return WavePattern.IMPULSE
        
        if len(waves) >= 3:
            dirs = [w.direction for w in waves[:3]]
            if dirs in [["UP", "DOWN", "UP"], ["DOWN", "UP", "DOWN"]]:
                # بررسی زیگزاگ یا مسطح (صفحات ۳۴۰-۳۴۱)
                range_a = self._get_range(waves[0])
                range_b = self._get_range(waves[1])
                
                if range_a > 0 and range_b / range_a < 0.618 + self.base_tolerance:
                    return WavePattern.ZIGZAG
                else:
                    return WavePattern.FLAT
        
        return WavePattern.UNKNOWN


# ══════════════════════════════════════════════════════════════════
# ۴. تابع اصلی برای استفاده در سیستم نئوویو
# ══════════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None, use_log: bool = False,
            tolerance: float = BASE_TOLERANCE) -> Dict[str, Any]:
    """
    تحلیل فصل ۱۴ - نسبت‌های فیبوناچی
    
    پارامترها:
        data     : DataFrame با ستون‌های open, high, low, close
        logger   : آبجکت ResultsLogger برای ذخیره نتایج (اختیاری)
        use_log  : استفاده از مقیاس لگاریتمی برای محاسبات
        tolerance: تلورانس پایه برای تطابق با نسبت‌های فیبوناچی (حداقل ۰.۰۳)
    
    خروجی:
        دیکشنری کامل نتایج تحلیل نسبت‌های فیبوناچی
    """
    import numpy as np
    
    # ── آماده‌سازی داده ──
    close = data["close"].values if "close" in data.columns else data["Close"].values
    high = data["high"].values if "high" in data.columns else data["High"].values
    low = data["low"].values if "low" in data.columns else data["Low"].values
    n = len(close)
    
    # ── شناسایی امواج با Pivot Detector ──
    pivot_detector = PivotDetector(data, left_bars=2, right_bars=2)
    pivots = pivot_detector.find_pivots()
    waves = pivot_detector.extract_waves(pivots)
    
    # ── ایجاد تحلیل‌گر ──
    analyzer = FibonacciRatioAnalyzer(data, use_log=use_log, tolerance=tolerance)
    
    # ── اجرای تحلیل ──
    if len(waves) >= 3:
        results = analyzer.full_analysis(waves)
        
        # ── استخراج نتایج کلیدی ──
        key_results = {
            "عنوان": "فصل ۱۴ - تحلیل نسبت‌های فیبوناچی",
            "وضعیت": "تحلیل کامل",
            "مقیاس": "لگاریتمی" if use_log else "حسابی",
            "تلورانس_پایه": f"{tolerance*100:.0f}%",
            "تعداد_امواج": len(waves),
            "تعداد_نقاط_چرخش": len(pivots),
            "نوع_الگو": results.get("pattern_type", "نامشخص"),
            "تعداد_نسبت‌های_داخلی": results.get("summary", {}).get("total_internal_ratios", 0),
            "تعداد_نسبت‌های_خارجی": results.get("summary", {}).get("total_external_ratios", 0),
            "تطابق_با_نسبت‌های_فیبو": results.get("summary", {}).get("fib_zone_hits", 0),
            "آخرین_قیمت": round(float(close[-1]), 4) if n > 0 else 0,
            "بالاترین": round(float(np.max(high)), 4) if n > 0 else 0,
            "پایین‌ترین": round(float(np.min(low)), 4) if n > 0 else 0,
        }
        
        # ── اضافه کردن نتایج تفصیلی امتداد ──
        if "analyses" in results:
            if "impulse" in results["analyses"]:
                impulse = results["analyses"]["impulse"]
                key_results["امتداد_غالب"] = impulse.get("dominant_extension", "ندارد")
                key_results["مرجع_کتاب"] = impulse.get("page_reference", "")
                if "detailed_analysis" in impulse:
                    details = impulse["detailed_analysis"]
                    key_results["نسبت_W3_W1"] = details.get("w3_w1_ratio", 0)
                    key_results["نسبت_W5_W3"] = details.get("w5_w3_ratio", 0)
                    key_results["نسبت_W5_1to3"] = details.get("w5_1to3_ratio", 0)
        
        # ── نسبت‌های داخلی مهم ──
        if "all_ratios" in results and results["all_ratios"]["internal"]:
            valid_ratios = [r for r in results["all_ratios"]["internal"]
                          if r.get("ratio", {}).get("is_in_fib_zone", False)]
            for i, ratio_data in enumerate(valid_ratios[:5]):
                ratio = ratio_data.get("ratio", {})
                key_results[f"نسبت_داخلی_{i+1}"] = ratio.get("description", "")
        
        # ── نسبت‌های خارجی مهم ──
        if "all_ratios" in results and results["all_ratios"]["external"]:
            valid_ratios = [r for r in results["all_ratios"]["external"]
                          if r.get("ratio", {}).get("is_in_fib_zone", False)]
            for i, ratio_data in enumerate(valid_ratios[:5]):
                ratio = ratio_data.get("ratio", {})
                key_results[f"نسبت_خارجی_{i+1}"] = ratio.get("description", "")
        
    else:
        key_results = {
            "عنوان": "فصل ۱۴ - تحلیل نسبت‌های فیبوناچی",
            "وضعیت": "داده کافی نیست",
            "تعداد_امواج": len(waves),
            "تعداد_نقاط_چرخش": len(pivots),
            "تعداد_نسبت‌های_داخلی": 0,
            "تعداد_نسبت‌های_خارجی": 0,
            "آخرین_قیمت": round(float(close[-1]), 4) if n > 0 else 0,
            "بالاترین": round(float(np.max(high)), 4) if n > 0 else 0,
            "پایین‌ترین": round(float(np.min(low)), 4) if n > 0 else 0,
            "پیام": "حداقل ۳ موج برای تحلیل نسبت‌ها نیاز است"
        }
    
    # ── ذخیره در لاگر ──
    if logger:
        logger.add_section("فصل ۱۴ - تحلیل نسبت‌ها", level=1)
        for k, v in key_results.items():
            if not isinstance(v, (dict, list)):
                logger.add_result(k, str(v))
        
        if "امتداد_غالب" in key_results:
            logger.add_wave("امتداد غالب", {
                "نوع": key_results["امتداد_غالب"],
                "مرجع": key_results.get("مرجع_کتاب", "")
            })
    
    return key_results


# ══════════════════════════════════════════════════════════════════
# ۵. تست و نمونه اجرا
# ══════════════════════════════════════════════════════════════════

def create_test_data() -> pd.DataFrame:
    """ایجاد داده تست برای بررسی تحلیل"""
    np.random.seed(42)
    n = 200
    price = 100
    prices = [price]
    for _ in range(1, n):
        change = np.random.normal(0, 0.015)
        price = price * (1 + change)
        prices.append(max(price, 0.01))
    data = pd.DataFrame({
        'open': prices,
        'high': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
        'close': prices,
        'volume': np.random.randint(1000, 10000, n)
    })
    return data


if __name__ == "__main__":
    print("=" * 70)
    print("تست کامل تحلیل نسبت‌های فیبوناچی - فصل ۱۴")
    print("مرجع: کتاب گلن نیلی - صفحات ۳۳۰ تا ۳۴۲")
    print("=" * 70)

    data = create_test_data()
    print(f"\n📊 داده تست: {len(data)} کندل")
    print(f"   بازه قیمتی: {data['low'].min():.2f} - {data['high'].max():.2f}")

    print("\n" + "─" * 50)
    print("🔍 تحلیل با مقیاس حسابی (تلورانس ۳٪)")
    print("─" * 50)
    res_arith = analyze(data, use_log=False, tolerance=0.03)
    for k, v in res_arith.items():
        if not isinstance(v, (dict, list)):
            print(f"   {k}: {v}")

    print("\n" + "─" * 50)
    print("🔍 تحلیل با مقیاس لگاریتمی (تلورانس ۳٪)")
    print("─" * 50)
    res_log = analyze(data, use_log=True, tolerance=0.03)
    for k, v in res_log.items():
        if not isinstance(v, (dict, list)):
            print(f"   {k}: {v}")

    print("\n" + "=" * 70)
    print("✅ تحلیل فصل ۱۴ با تمام اصلاحات تحلیلی کامل شد.")
    print("=" * 70)