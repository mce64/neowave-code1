"""
فصل ۴: کش دیتا (Cash Data)
منبع: کتاب "امواج الیوت به سبک نئوویو" - گلن نیلی - صفحات ۲۳ تا ۳۱

══════════════════════════════════════════════════════════════════
محتوای کامل فصل ۴ (مطابق متن و دیاگرام‌های کتاب):

مشکل اصلی (صفحه ۲۳):
    استفاده از قیمت‌های نهایی (Close) در هر تایم‌فریم نامطمئن‌ترین
    راه برای نشان دادن حرکت امواج است. در داده‌های نقدی (Cash Data)،
    برای هر واحد زمانی دو نقطه قیمتی وجود دارد (High و Low)،
    نه یک نقطه.

اصل اساسی کش دیتا (صفحه ۲۳):
    "برای ایجاد نمودار موجی به روش گلن نیلی، نیاز به ترسیم
    نقاط بالا و پایین بازار، به ترتیب وقوع آن‌ها دارید."
    - شیار زمانی باید به ۴۰ قسمت تقسیم شود
    - High و Low هر کندل به ترتیب وقوع رسم می‌شوند
    - عرض شیارها باید ثابت باشد

نکته مهم (صفحه ۲۴):
    اگر در یک شیار زمانی کمترین و بیشترین قیمت دو بار تکرار شود،
    شیار از نقطه ۳۰۰ شروع و تا ۷۰۰ می‌رود → بهترین گزینه: جریان قیمتی

قوانین تشخیص ترتیب High/Low (صفحه ۲۴):
    وضعیت ۱: آخرین نقطه شیار زمانی قبل = Low بوده:
        اگر نقاط جاری Low-High-Low → اولین نقطه Low، دومین High
        اگر نقاط جاری High-Low-High → روش سه‌نقطه‌ای (احتیاط!)

    وضعیت ۲: آخرین نقطه شیار زمانی قبل = High بوده:
        اگر نقاط جاری Low-High-Low → روش سه‌نقطه‌ای (احتیاط!)
        اگر نقاط جاری High-Low-High → اولین نقطه High، دومین Low

روش سه‌نقطه‌ای (صفحه ۲۵):
    - هر شیار به دو شیار تبدیل می‌شود (عرض هر یک = نصف شیار اولیه)
    - باید با احتیاط استفاده شود
    - در صورت ناچاری، Low-High-Low یا High-Low-High شکل می‌گیرد

سه مرحله ایجاد کش دیتا (صفحه ۲۷):
    مرحله ۱: شناسایی کوچکترین واحد زمانی
    مرحله ۲: رسم نقاط به روش تقدم و تاخر بالاترین/پایین‌ترین قیمت
    مرحله ۳: اتصال نقاط با خطوط قطری

NEoWave Plots (صفحه ۲۹-۳۰):
    "Highs and lows plotted in real-time order"
    - One Time Unit = divided into two equal segments
    - هر Monowave از High و Low یک کندل با ترتیب وقوع تشکیل می‌شود
    - Low of day came first → Low plotted first, then High
    - High of day came first → High plotted first, then Low

قانون نهایی ترسیم (صفحه ۳۱):
    خطوط پررنگ = اتصال بیشترین قیمت در هر شیار زمانی
    خطوط کم‌رنگ = اتصال کمترین قیمت در هر شیار زمانی
══════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


# ══════════════════════════════════════════════════════════════
# بخش ۱: انواع و ساختارهای داده
# ══════════════════════════════════════════════════════════════

class BarType(Enum):
    """
    نوع کندل بر اساس ترتیب وقوع High/Low
    مطابق دیاگرام صفحه ۲۹ کتاب نیلی
    """
    HIGH_FIRST = "high_first"  # High قبل از Low رخ داده
    LOW_FIRST  = "low_first"   # Low قبل از High رخ داده
    DOJI       = "doji"        # High ≈ Low (تفاوت ناچیز)
    UNKNOWN    = "unknown"     # قابل تشخیص نیست


class PlotMethod(Enum):
    """
    روش ترسیم کش دیتا (صفحه ۲۳-۲۵)
    """
    HIGH_LOW_SEQUENCE  = "high_low_sequence"   # ترتیب High-Low یا Low-High
    THREE_POINT        = "three_point"          # روش سه‌نقطه‌ای (احتیاط!)
    PRICE_FLOW         = "price_flow"           # جریان قیمتی (بهترین)
    CLOSE_APPROXIMATION = "close_approx"        # تقریب با Close


class PreviousPointType(Enum):
    """
    آخرین نقطه شیار زمانی قبلی (صفحه ۲۴)
    """
    HIGH = "high"
    LOW  = "low"
    NONE = "none"


@dataclass
class CashDataPoint:
    """
    یک نقطه در کش دیتا - دقیقاً مطابق مفهوم صفحه ۲۳ کتاب:
    "برای هر واحد زمانی دو نقطه قیمتی وجود دارد"
    """
    bar_idx     : int          # ایندکس کندل اصلی
    sub_idx     : int          # زیرایندکس (0=اول، 1=دوم)
    price       : float        # قیمت
    point_type  : str          # "HIGH" یا "LOW"
    is_first    : bool         # اولین نقطه در شیار زمانی است؟
    time_slot   : float        # موقعیت در شیار زمانی (0 تا 1)


@dataclass
class CashDataBar:
    """
    یک کندل تبدیل‌شده به کش دیتا
    هر کندل = دو نقطه به ترتیب وقوع
    """
    bar_idx      : int
    open_price   : float
    high_price   : float
    low_price    : float
    close_price  : float
    volume       : float
    bar_type     : BarType          # ترتیب وقوع High/Low
    first_point  : CashDataPoint    # اولین نقطه
    second_point : CashDataPoint    # دومین نقطه
    plot_method  : PlotMethod       # روش ترسیم انتخاب‌شده
    is_three_point: bool = False    # آیا روش سه‌نقطه‌ای اعمال شده؟
    three_point_sequence: str = ""  # "LHL" یا "HLH"
    monowave_direction: int = 0     # +1 یا -1 (جهت Monowave)
    monowave_range: float = 0.0     # دامنه Monowave


@dataclass
class CashDataResult:
    """نتیجه کامل تبدیل داده به کش دیتا"""
    bars             : List[CashDataBar]
    all_points       : List[CashDataPoint]  # همه نقاط به ترتیب
    monowaves        : List[Dict]           # Monowave های استخراج‌شده
    quality_score    : float                # امتیاز کیفیت (0-100)
    warnings         : List[str]


# ══════════════════════════════════════════════════════════════
# بخش ۲: تشخیص ترتیب وقوع High/Low
# ══════════════════════════════════════════════════════════════

class BarTypeDetector:
    """
    تشخیص اینکه در هر کندل، High اول رخ داده یا Low
    مطابق قوانین صفحه ۲۴ کتاب نیلی
    """

    # اگر تفاوت High و Low کمتر از این درصد باشد = Doji
    DOJI_THRESHOLD = 0.001  # 0.1%

    @staticmethod
    def detect(
        open_price  : float,
        high_price  : float,
        low_price   : float,
        close_price : float,
        prev_close  : Optional[float] = None,
        prev_point_type: PreviousPointType = PreviousPointType.NONE,
    ) -> Tuple[BarType, PlotMethod, str]:
        """
        تشخیص نوع کندل و روش ترسیم بهینه.

        قوانین کتاب (صفحه ۲۴):
        - اگر close < open: احتمالاً Low بعد از High رخ داده → HIGH_FIRST
        - اگر close > open: احتمالاً High بعد از Low رخ داده → LOW_FIRST
        - اگر open نزدیک high: کندل از بالا شروع کرده → احتمال HIGH_FIRST
        - اگر open نزدیک low: کندل از پایین شروع کرده → احتمال LOW_FIRST

        خروجی: (BarType, PlotMethod, sequence_string)
        """
        price_range = high_price - low_price

        # ── Doji بررسی
        if price_range == 0 or (high_price > 0 and price_range / high_price < BarTypeDetector.DOJI_THRESHOLD):
            return BarType.DOJI, PlotMethod.CLOSE_APPROXIMATION, "DOJI"

        # ── فاصله open از High و Low
        dist_to_high = high_price - open_price
        dist_to_low  = open_price - low_price

        # ── نسبت close به range
        close_ratio = (close_price - low_price) / price_range if price_range > 0 else 0.5

        # ── روش اول: بر اساس جهت حرکت (open→close)
        body = close_price - open_price

        if abs(body) > price_range * 0.3:
            # کندل با بدنه مشخص
            if body > 0:
                # صعودی: Low قبل از High
                bar_type = BarType.LOW_FIRST
                sequence = "L→H"
            else:
                # نزولی: High قبل از Low
                bar_type = BarType.HIGH_FIRST
                sequence = "H→L"
        else:
            # کندل با بدنه کوچک - از open استفاده می‌کنیم
            if dist_to_high < dist_to_low:
                # open نزدیک High → از بالا شروع کرده
                bar_type = BarType.HIGH_FIRST
                sequence = "H→L"
            else:
                bar_type = BarType.LOW_FIRST
                sequence = "L→H"

        # ── بررسی قانون وضعیت‌های ۱ و ۲ (صفحه ۲۴)
        # بررسی نیاز به روش سه‌نقطه‌ای
        needs_three_point = False
        plot_method = PlotMethod.HIGH_LOW_SEQUENCE

        if prev_point_type == PreviousPointType.LOW:
            # وضعیت ۱: شیار قبل به Low ختم شده
            if bar_type == BarType.HIGH_FIRST:
                # High-Low-High → نیاز به سه‌نقطه‌ای
                needs_three_point = True
                plot_method = PlotMethod.THREE_POINT
                sequence = "HLH→three_point"
        elif prev_point_type == PreviousPointType.HIGH:
            # وضعیت ۲: شیار قبل به High ختم شده
            if bar_type == BarType.LOW_FIRST:
                # Low-High-Low → نیاز به سه‌نقطه‌ای
                needs_three_point = True
                plot_method = PlotMethod.THREE_POINT
                sequence = "LHL→three_point"

        if not needs_three_point:
            plot_method = PlotMethod.PRICE_FLOW

        return bar_type, plot_method, sequence

    @staticmethod
    def detect_from_intraday(
        prices_in_order: List[float]
    ) -> BarType:
        """
        اگر داده درون‌روزی داریم، ترتیب واقعی را تشخیص می‌دهیم.
        مطابق مفهوم "Real-Time Order" صفحه ۳۰ کتاب.
        """
        if not prices_in_order or len(prices_in_order) < 2:
            return BarType.UNKNOWN

        max_val = max(prices_in_order)
        min_val = min(prices_in_order)
        max_idx = prices_in_order.index(max_val)
        min_idx = prices_in_order.index(min_val)

        if min_idx < max_idx:
            return BarType.LOW_FIRST
        elif max_idx < min_idx:
            return BarType.HIGH_FIRST
        else:
            return BarType.DOJI


# ══════════════════════════════════════════════════════════════
# بخش ۳: مبدل کش دیتا (CashDataConverter)
# ══════════════════════════════════════════════════════════════

class CashDataConverter:
    """
    تبدیل داده OHLC به کش دیتا مطابق روش گلن نیلی

    اصل کار (صفحه ۲۳-۲۷):
    ۱. هر شیار زمانی به ۴۰ قسمت تقسیم می‌شود
    ۲. High و Low به ترتیب وقوع رسم می‌شوند
    ۳. نقاط با خطوط قطری به هم وصل می‌شوند
    ۴. عرض شیارها ثابت است
    """

    # تعداد تقسیمات هر شیار زمانی (صفحه ۲۳: ۴۰ قسمت)
    TIME_SLOT_DIVISIONS = 40

    def __init__(self, data: pd.DataFrame):
        """
        data: DataFrame با ستون‌های open/high/low/close/volume
        """
        self._data = data.copy()
        self._normalize_columns()
        self.n = len(self._data)

    def _normalize_columns(self):
        """نرمال‌سازی نام ستون‌ها"""
        col_map = {}
        for col in self._data.columns:
            cl = col.lower()
            if cl in ("open", "باز"):          col_map[col] = "open"
            elif cl in ("high", "بالاترین"):   col_map[col] = "high"
            elif cl in ("low",  "پایین‌ترین"): col_map[col] = "low"
            elif cl in ("close","بسته"):        col_map[col] = "close"
            elif cl in ("volume","حجم"):        col_map[col] = "volume"
        self._data.rename(columns=col_map, inplace=True)

        for c in ("open", "high", "low", "close"):
            if c in self._data.columns:
                self._data[c] = self._data[c].astype(float)
        if "volume" not in self._data.columns:
            self._data["volume"] = 0.0

    def convert(self) -> CashDataResult:
        """
        تبدیل کامل داده به کش دیتا

        خروجی: CashDataResult با همه اطلاعات
        """
        bars          : List[CashDataBar]    = []
        all_points    : List[CashDataPoint]  = []
        warnings      : List[str]            = []
        three_pt_count: int                  = 0
        doji_count    : int                  = 0

        prev_point_type = PreviousPointType.NONE

        opens   = self._data["open"].values.astype(float)
        highs   = self._data["high"].values.astype(float)
        lows    = self._data["low"].values.astype(float)
        closes  = self._data["close"].values.astype(float)
        volumes = self._data["volume"].values.astype(float)

        for i in range(self.n):
            o = float(opens[i])
            h = float(highs[i])
            l = float(lows[i])
            c = float(closes[i])
            v = float(volumes[i])

            # ── تشخیص نوع کندل
            bar_type, plot_method, sequence = BarTypeDetector.detect(
                open_price=o, high_price=h, low_price=l, close_price=c,
                prev_close=float(closes[i-1]) if i > 0 else None,
                prev_point_type=prev_point_type
            )

            # ── ساخت دو نقطه کش دیتا
            if bar_type == BarType.DOJI:
                doji_count += 1
                first_price  = c
                second_price = c
                first_type   = "CLOSE"
                second_type  = "CLOSE"
            elif bar_type == BarType.HIGH_FIRST:
                first_price  = h
                second_price = l
                first_type   = "HIGH"
                second_type  = "LOW"
            else:  # LOW_FIRST
                first_price  = l
                second_price = h
                first_type   = "LOW"
                second_type  = "HIGH"

            # ── اعمال روش سه‌نقطه‌ای (صفحه ۲۵)
            is_three_point = False
            three_pt_seq   = ""
            if plot_method == PlotMethod.THREE_POINT:
                three_pt_count += 1
                is_three_point = True
                warnings.append(
                    f"کندل {i}: روش سه‌نقطه‌ای اعمال شد ({sequence})"
                )
                three_pt_seq = sequence

            # ── ساخت آبجکت‌های CashDataPoint
            first_pt = CashDataPoint(
                bar_idx=i, sub_idx=0,
                price=float(first_price),
                point_type=first_type,
                is_first=True,
                time_slot=i + 0.25  # ربع اول شیار
            )
            second_pt = CashDataPoint(
                bar_idx=i, sub_idx=1,
                price=float(second_price),
                point_type=second_type,
                is_first=False,
                time_slot=i + 0.75  # ربع سوم شیار
            )

            # ── جهت Monowave
            mw_dir   = 1 if second_price > first_price else -1
            mw_range = abs(second_price - first_price)

            # ── بروزرسانی prev_point_type
            if second_type == "HIGH":
                prev_point_type = PreviousPointType.HIGH
            elif second_type == "LOW":
                prev_point_type = PreviousPointType.LOW
            else:
                prev_point_type = PreviousPointType.NONE

            # ── ساخت CashDataBar
            bar = CashDataBar(
                bar_idx=i, open_price=o, high_price=h,
                low_price=l, close_price=c, volume=v,
                bar_type=bar_type,
                first_point=first_pt,
                second_point=second_pt,
                plot_method=plot_method,
                is_three_point=is_three_point,
                three_point_sequence=three_pt_seq,
                monowave_direction=mw_dir,
                monowave_range=float(mw_range)
            )

            bars.append(bar)
            all_points.extend([first_pt, second_pt])

        # ── استخراج Monowave ها
        monowaves = self._extract_monowaves(all_points)

        # ── محاسبه امتیاز کیفیت
        quality = self._calc_quality_score(
            n_bars=self.n,
            three_pt_count=three_pt_count,
            doji_count=doji_count,
            n_monowaves=len(monowaves)
        )

        return CashDataResult(
            bars=bars,
            all_points=all_points,
            monowaves=monowaves,
            quality_score=quality,
            warnings=warnings
        )

    @staticmethod
    def _extract_monowaves(points: List[CashDataPoint]) -> List[Dict]:
        """
        استخراج Monowave ها از نقاط کش دیتا.
        هر تغییر جهت = یک Monowave جدید.
        مطابق تعریف صفحه ۳۲ کتاب نیلی.
        """
        if len(points) < 2:
            return []

        monowaves = []
        start_pt  = points[0]

        for i in range(1, len(points)):
            curr_pt = points[i]
            prev_pt = points[i-1]

            # تغییر جهت = پایان Monowave قبلی و شروع جدید
            prev_dir = 1 if prev_pt.price > start_pt.price else -1
            curr_dir = 1 if curr_pt.price > prev_pt.price  else -1

            if curr_dir != prev_dir and i > 1:
                # یک Monowave کامل شد
                mw_range = abs(prev_pt.price - start_pt.price)
                if mw_range > 0:
                    monowaves.append({
                        "start_bar"  : start_pt.bar_idx,
                        "end_bar"    : prev_pt.bar_idx,
                        "start_price": round(float(start_pt.price), 4),
                        "end_price"  : round(float(prev_pt.price),  4),
                        "direction"  : 1 if prev_pt.price > start_pt.price else -1,
                        "dir_str"    : "صعودی" if prev_pt.price > start_pt.price else "نزولی",
                        "price_range": round(float(mw_range), 4),
                        "start_type" : start_pt.point_type,
                        "end_type"   : prev_pt.point_type,
                        "bars_count" : prev_pt.bar_idx - start_pt.bar_idx + 1,
                    })
                start_pt = prev_pt

        # آخرین Monowave ناتمام
        last_pt  = points[-1]
        mw_range = abs(last_pt.price - start_pt.price)
        if mw_range > 0:
            monowaves.append({
                "start_bar"  : start_pt.bar_idx,
                "end_bar"    : last_pt.bar_idx,
                "start_price": round(float(start_pt.price), 4),
                "end_price"  : round(float(last_pt.price),  4),
                "direction"  : 1 if last_pt.price > start_pt.price else -1,
                "dir_str"    : "صعودی" if last_pt.price > start_pt.price else "نزولی",
                "price_range": round(float(mw_range), 4),
                "start_type" : start_pt.point_type,
                "end_type"   : last_pt.point_type,
                "bars_count" : last_pt.bar_idx - start_pt.bar_idx + 1,
                "is_incomplete": True,
            })

        return monowaves

    @staticmethod
    def _calc_quality_score(
        n_bars: int,
        three_pt_count: int,
        doji_count: int,
        n_monowaves: int
    ) -> float:
        """
        محاسبه امتیاز کیفیت کش دیتا (0-100)

        کیفیت بالا = سه‌نقطه‌ای کم، Doji کم، Monowave کافی
        """
        if n_bars == 0:
            return 0.0

        # جریمه برای سه‌نقطه‌ای (هر کدام -2)
        three_pt_penalty = (three_pt_count / n_bars) * 20

        # جریمه برای Doji (هر کدام -1)
        doji_penalty = (doji_count / n_bars) * 10

        # امتیاز Monowave (بیشتر بهتر تا حد معقول)
        mw_ratio = min(n_monowaves / (n_bars * 0.5), 1.0) if n_bars > 0 else 0
        mw_bonus  = mw_ratio * 30

        score = 100 - three_pt_penalty - doji_penalty + mw_bonus - 30
        return round(max(0.0, min(100.0, score)), 1)


# ══════════════════════════════════════════════════════════════
# بخش ۴: تحلیل‌گر کش دیتا
# ══════════════════════════════════════════════════════════════

class CashDataAnalyzer:
    """
    تحلیل آماری نتایج کش دیتا مطابق فصل ۴ کتاب
    """

    @staticmethod
    def analyze_bar_types(bars: List[CashDataBar]) -> Dict:
        """آمار توزیع انواع کندل"""
        total        = len(bars)
        high_first   = sum(1 for b in bars if b.bar_type == BarType.HIGH_FIRST)
        low_first    = sum(1 for b in bars if b.bar_type == BarType.LOW_FIRST)
        doji_count   = sum(1 for b in bars if b.bar_type == BarType.DOJI)
        three_pt     = sum(1 for b in bars if b.is_three_point)

        return {
            "کل_کندل"                   : total,
            "High_اول"                  : high_first,
            "Low_اول"                   : low_first,
            "دوجی"                      : doji_count,
            "سه‌نقطه‌ای"               : three_pt,
            "درصد_High_اول"             : round(high_first/total*100, 1) if total else 0,
            "درصد_Low_اول"              : round(low_first/total*100,  1) if total else 0,
            "درصد_دوجی"                 : round(doji_count/total*100, 1) if total else 0,
            "درصد_سه‌نقطه‌ای"          : round(three_pt/total*100,   1) if total else 0,
        }

    @staticmethod
    def analyze_monowaves(monowaves: List[Dict]) -> Dict:
        """آمار Monowave های استخراج‌شده"""
        if not monowaves:
            return {"وضعیت": "هیچ Monowave ای یافت نشد"}

        up_waves   = [m for m in monowaves if m["direction"] ==  1]
        down_waves = [m for m in monowaves if m["direction"] == -1]

        ranges = [m["price_range"] for m in monowaves if m["price_range"] > 0]
        bars_c = [m["bars_count"]  for m in monowaves]

        return {
            "تعداد_کل_Monowave"         : len(monowaves),
            "تعداد_صعودی"               : len(up_waves),
            "تعداد_نزولی"               : len(down_waves),
            "میانگین_دامنه"             : round(float(np.mean(ranges)), 4) if ranges else 0,
            "بیشترین_دامنه"             : round(float(np.max(ranges)),  4) if ranges else 0,
            "کمترین_دامنه"              : round(float(np.min(ranges)),  4) if ranges else 0,
            "میانگین_تعداد_کندل"        : round(float(np.mean(bars_c)), 2) if bars_c else 0,
            "آخرین_جهت"                 : monowaves[-1]["dir_str"] if monowaves else "نامشخص",
            "آخرین_قیمت"               : monowaves[-1]["end_price"] if monowaves else 0,
        }

    @staticmethod
    def detect_intraday_order(
        high: float, low: float, open_price: float, close_price: float
    ) -> Dict:
        """
        تشخیص ترتیب وقوع High/Low مطابق قوانین صفحه ۲۴

        قانون ۱ (صفحه ۲۴ - وضعیت ۱):
        اگر نقطه قبل = Low بوده:
            نقاط LHL → اولین نقطه Low، دومین High
            نقاط HLH → روش سه‌نقطه‌ای

        قانون ۲ (صفحه ۲۴ - وضعیت ۲):
        اگر نقطه قبل = High بوده:
            نقاط HLH → اولین نقطه High، دومین Low
            نقاط LHL → روش سه‌نقطه‌ای
        """
        body      = close_price - open_price
        body_pct  = abs(body) / (high - low) if (high - low) > 0 else 0
        is_bullish = body > 0

        if body_pct > 0.5:
            method = "بدنه_قوی"
            if is_bullish:
                order = "LOW_FIRST: کندل صعودی → Low قبل از High"
                first, second = "LOW", "HIGH"
            else:
                order = "HIGH_FIRST: کندل نزولی → High قبل از Low"
                first, second = "HIGH", "LOW"
        elif abs(close_price - high) < abs(close_price - low):
            method = "close_نزدیک_به_High"
            order  = "LOW_FIRST: قیمت از پایین بالا آمده"
            first, second = "LOW", "HIGH"
        else:
            method = "close_نزدیک_به_Low"
            order  = "HIGH_FIRST: قیمت از بالا پایین آمده"
            first, second = "HIGH", "LOW"

        return {
            "ترتیب_وقوع"    : order,
            "اولین_نقطه"    : first,
            "دومین_نقطه"    : second,
            "روش_تشخیص"    : method,
            "درصد_بدنه"     : round(body_pct * 100, 1),
        }


# ══════════════════════════════════════════════════════════════
# بخش ۵: تابع analyze — interface کد هسته
# ══════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None) -> Dict:
    """
    فصل ۴: کش دیتا (Cash Data)
    interface: analyze(data, logger) → dict  (همه value ها str)

    پیاده‌سازی کامل مطابق صفحات ۲۳-۳۱ کتاب گلن نیلی:
    - تشخیص ترتیب وقوع High/Low هر کندل
    - اعمال قوانین وضعیت ۱ و ۲ (صفحه ۲۴)
    - روش سه‌نقطه‌ای در موارد ضروری (صفحه ۲۵)
    - استخراج Monowave های کش دیتا
    - محاسبه امتیاز کیفیت
    """

    # ── حداقل داده ────────────────────────────────────────────
    if len(data) < 2:
        out = {
            "عنوان"     : "فصل ۴: کش دیتا (Cash Data)",
            "وضعیت"     : "داده_کافی_نیست",
            "تعداد_کندل": str(len(data)),
        }
        if logger:
            logger.add_section("فصل ۴: کش دیتا", level=1)
            logger.add_result("وضعیت", "داده کافی نیست")
        return out

    # ── مرحله ۱: تبدیل به کش دیتا ────────────────────────────
    converter = CashDataConverter(data)
    cd_result = converter.convert()

    # ── مرحله ۲: تحلیل انواع کندل ────────────────────────────
    bar_stats = CashDataAnalyzer.analyze_bar_types(cd_result.bars)

    # ── مرحله ۳: تحلیل Monowave ها ───────────────────────────
    mw_stats = CashDataAnalyzer.analyze_monowaves(cd_result.monowaves)

    # ── مرحله ۴: تحلیل اولین و آخرین کندل ───────────────────
    def _col(df, *names):
        for nm in names:
            if nm in df.columns:
                return df[nm].astype(float).values
        return np.zeros(len(df))

    close  = _col(data, "close", "Close")
    high   = _col(data, "high",  "High")
    low    = _col(data, "low",   "Low")
    opens  = _col(data, "open",  "Open")
    n      = len(close)

    # تحلیل آخرین کندل
    last_order = CashDataAnalyzer.detect_intraday_order(
        high=float(high[-1]), low=float(low[-1]),
        open_price=float(opens[-1]), close_price=float(close[-1])
    )

    # ── مرحله ۵: آمار کلی ─────────────────────────────────────
    high_arr = high.astype(float)
    low_arr  = low.astype(float)

    avg_bar_range = float(np.mean(high_arr - low_arr))
    max_bar_range = float(np.max(high_arr  - low_arr))
    min_bar_range = float(np.min(high_arr  - low_arr))

    # ── مرحله ۶: ساخت خروجی ──────────────────────────────────
    results: Dict = {
        # شناسنامه
        "عنوان"                        : "فصل ۴: کش دیتا (Cash Data)",
        "مرجع"                         : "صفحات ۲۳-۳۱ - گلن نیلی",
        "وضعیت"                        : "تحلیل_کامل",

        # اصل کش دیتا (صفحه ۲۳)
        "اصل_کش_دیتا"                  : "هر کندل = دو نقطه قیمتی به ترتیب وقوع",
        "روش_نیلی"                     : "ترسیم High و Low به ترتیب وقوع واقعی",
        "تقسیمات_شیار_زمانی"           : "۴۰ قسمت مساوی",
        "قانون_عرض_شیار"               : "عرض شیارها باید ثابت باشد",

        # آمار پایه
        "تعداد_کندل"                   : str(n),
        "تعداد_نقطه_کش_دیتا"           : str(len(cd_result.all_points)),
        "قیمت_فعلی"                    : str(round(float(close[-1]), 4)),
        "بالاترین_قیمت"                : str(round(float(np.max(high_arr)), 4)),
        "پایین‌ترین_قیمت"              : str(round(float(np.min(low_arr)), 4)),

        # توزیع انواع کندل (مطابق قوانین صفحه ۲۴)
        "کندل_High_اول"                : str(bar_stats["High_اول"]),
        "کندل_Low_اول"                 : str(bar_stats["Low_اول"]),
        "کندل_دوجی"                    : str(bar_stats["دوجی"]),
        "کندل_سه‌نقطه‌ای"             : str(bar_stats["سه‌نقطه‌ای"]),
        "درصد_High_اول"                : str(bar_stats["درصد_High_اول"]) + "%",
        "درصد_Low_اول"                 : str(bar_stats["درصد_Low_اول"]) + "%",
        "درصد_سه‌نقطه‌ای"             : str(bar_stats["درصد_سه‌نقطه‌ای"]) + "%",

        # Monowave های کش دیتا (صفحه ۳۲)
        "تعداد_Monowave"               : str(mw_stats.get("تعداد_کل_Monowave", 0)),
        "Monowave_صعودی"               : str(mw_stats.get("تعداد_صعودی", 0)),
        "Monowave_نزولی"               : str(mw_stats.get("تعداد_نزولی", 0)),
        "میانگین_دامنه_Monowave"       : str(mw_stats.get("میانگین_دامنه", 0)),
        "بیشترین_دامنه_Monowave"       : str(mw_stats.get("بیشترین_دامنه", 0)),
        "آخرین_جهت_Monowave"          : str(mw_stats.get("آخرین_جهت", "نامشخص")),
        "آخرین_قیمت_Monowave"         : str(mw_stats.get("آخرین_قیمت", 0)),

        # آمار دامنه کندل‌ها
        "میانگین_دامنه_کندل"           : str(round(avg_bar_range, 4)),
        "بیشترین_دامنه_کندل"           : str(round(max_bar_range, 4)),
        "کمترین_دامنه_کندل"            : str(round(min_bar_range, 4)),

        # امتیاز کیفیت کش دیتا
        "امتیاز_کیفیت_کش_دیتا"        : str(cd_result.quality_score),
        "تفسیر_کیفیت"                  : _quality_label(cd_result.quality_score),

        # آخرین کندل
        "آخرین_کندل_ترتیب"            : last_order["ترتیب_وقوع"],
        "آخرین_کندل_اولین_نقطه"        : last_order["اولین_نقطه"],
        "آخرین_کندل_دومین_نقطه"        : last_order["دومین_نقطه"],

        # قوانین فصل ۴
        "قانون_وضعیت_1"               : "اگر قبل=Low: LHL→(Low,High) | HLH→سه‌نقطه‌ای",
        "قانون_وضعیت_2"               : "اگر قبل=High: HLH→(High,Low) | LHL→سه‌نقطه‌ای",
        "قانون_سه‌نقطه‌ای"            : "هر شیار به دو شیار با نصف عرض تبدیل می‌شود",
        "قانون_جریان_قیمتی"           : "بهترین گزینه برای بازارهای ۲۴ساعته",

        # هشدارها
        "تعداد_هشدار"                  : str(len(cd_result.warnings)),
        "هشدار_اول"                    : cd_result.warnings[0] if cd_result.warnings else "بدون_هشدار",
    }

    # ── جزئیات ۵ Monowave آخر ─────────────────────────────────
    for idx, mw in enumerate(cd_result.monowaves[-5:]):
        p = f"Monowave_آخر_{5-idx}"
        results[f"{p}_جهت"]   = mw["dir_str"]
        results[f"{p}_دامنه"] = str(mw["price_range"])
        results[f"{p}_شروع"]  = str(mw["start_price"])
        results[f"{p}_پایان"] = str(mw["end_price"])

    # ── تفسیر نهایی ───────────────────────────────────────────
    results["تفسیر_نهایی"] = _build_interpretation(
        n, len(cd_result.all_points), bar_stats,
        mw_stats, cd_result.quality_score,
        cd_result.warnings, last_order
    )

    # ⭐ داده‌های خام برای استفاده فصل‌های دیگر (دیکشنری کامل)
    results["_cash_data_full"] = {
        "bars": cd_result.bars,
        "all_points": cd_result.all_points,
        "monowaves": cd_result.monowaves,
        "quality_score": cd_result.quality_score,
    }
    # ⭐ داده‌های خام برای استفاده فصل‌های دیگر
    results["_cash_data"] = "ذخیره‌شده"  # فقط برای نمایش
    results["_cash_data_monowaves"] = len(cd_result.monowaves)
    results["_cash_data_quality"] = cd_result.quality_score

    # ── ثبت در لاگ ────────────────────────────────────────────
    if logger:
        _write_log(logger, results, cd_result)

    return results


def _quality_label(score: float) -> str:
    if score >= 80: return "عالی (کش دیتا قابل اعتماد)"
    if score >= 60: return "خوب (قابل استفاده)"
    if score >= 40: return "متوسط (با احتیاط استفاده شود)"
    return "ضعیف (نیاز به داده بهتر)"


# ══════════════════════════════════════════════════════════════
# بخش ۶: تفسیر و لاگ
# ══════════════════════════════════════════════════════════════

def _build_interpretation(
    n, n_points, bar_stats, mw_stats,
    quality, warnings, last_order
) -> str:

    warn_str = f"{len(warnings)} هشدار" if warnings else "بدون هشدار"

    return f"""
══════════════════════════════════════════════════════════════════
  فصل ۴: کش دیتا (Cash Data)
  مرجع: صفحات ۲۳-۳۱  |  گلن نیلی
══════════════════════════════════════════════════════════════════

📖 اصل اساسی (صفحه ۲۳):
   "داده‌های نقدی برای هر واحد زمانی دو نقطه دارند (High و Low)،
   نه یک نقطه. High و Low باید به ترتیب وقوع رسم شوند."

📊 آمار تبدیل:
   کندل‌های ورودی : {n}
   نقاط کش دیتا   : {n_points}
   Monowave استخراج: {mw_stats.get('تعداد_کل_Monowave', 0)}
   امتیاز کیفیت   : {quality}/100

📐 توزیع کندل‌ها (قوانین صفحه ۲۴):
   High اول  : {bar_stats['High_اول']} ({bar_stats['درصد_High_اول']}%)
   Low اول   : {bar_stats['Low_اول']} ({bar_stats['درصد_Low_اول']}%)
   دوجی      : {bar_stats['دوجی']}
   سه‌نقطه‌ای: {bar_stats['سه‌نقطه‌ای']} ({bar_stats['درصد_سه‌نقطه‌ای']}%)

🔄 Monowave های کش دیتا:
   صعودی    : {mw_stats.get('تعداد_صعودی', 0)}
   نزولی    : {mw_stats.get('تعداد_نزولی', 0)}
   آخرین جهت: {mw_stats.get('آخرین_جهت', 'نامشخص')}
   آخرین قیمت: {mw_stats.get('آخرین_قیمت', 0)}

📋 قوانین ترسیم (صفحه ۲۴):
   وضعیت ۱ (قبل=Low):
   ✓ LHL → اولین: Low | دومین: High
   ⚠ HLH → روش سه‌نقطه‌ای
   وضعیت ۲ (قبل=High):
   ✓ HLH → اولین: High | دومین: Low
   ⚠ LHL → روش سه‌نقطه‌ای

🔍 آخرین کندل:
   ترتیب: {last_order['ترتیب_وقوع']}

⚠ هشدارها: {warn_str}
══════════════════════════════════════════════════════════════════"""


def _write_log(logger, results, cd_result):
    logger.add_section("فصل ۴: کش دیتا (Cash Data)", level=1)
    logger.add_result("مرجع", results["مرجع"])
    logger.add_result("اصل کش دیتا",    results["اصل_کش_دیتا"])
    logger.add_result("تعداد کندل",      results["تعداد_کندل"])
    logger.add_result("نقاط کش دیتا",   results["تعداد_نقطه_کش_دیتا"])
    logger.add_result("تعداد Monowave",  results["تعداد_Monowave"])
    logger.add_result("امتیاز کیفیت",   results["امتیاز_کیفیت_کش_دیتا"])
    logger.add_result("تفسیر کیفیت",    results["تفسیر_کیفیت"])

    logger.add_section("توزیع کندل‌ها (قوانین صفحه ۲۴)", level=2)
    logger.add_result("High اول",     results["کندل_High_اول"])
    logger.add_result("Low اول",      results["کندل_Low_اول"])
    logger.add_result("سه‌نقطه‌ای",  results["کندل_سه‌نقطه‌ای"])
    logger.add_result("دوجی",        results["کندل_دوجی"])

    logger.add_section("Monowave های کش دیتا", level=2)
    logger.add_result("صعودی",       results["Monowave_صعودی"])
    logger.add_result("نزولی",       results["Monowave_نزولی"])
    logger.add_result("آخرین جهت",   results["آخرین_جهت_Monowave"])
    logger.add_result("میانگین دامنه", results["میانگین_دامنه_Monowave"])

    logger.add_section("قوانین فصل ۴", level=2)
    logger.add_result("وضعیت ۱", results["قانون_وضعیت_1"])
    logger.add_result("وضعیت ۲", results["قانون_وضعیت_2"])
    logger.add_result("سه‌نقطه‌ای", results["قانون_سه‌نقطه‌ای"])

    logger.add_section("هشدارها", level=2)
    for w in cd_result.warnings[:5]:
        logger.add_result("هشدار", w)

    logger.add_result("تفسیر", results["تفسیر_نهایی"])