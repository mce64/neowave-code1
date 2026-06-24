"""
فصل ۵: شناسایی تک موج‌ها (Monowave Identification)
منبع: کتاب "امواج الیوت به سبک نئوویو" - گلن نیلی - صفحه ۳۲

══════════════════════════════════════════════════════════════════
متن دقیق کتاب (صفحه ۳۲):

"پس از رسم نمودار با استفاده از کش دیتا و با استفاده از بررسی
نقطه - داده‌ها و تغییر جهت نقطه - داده‌ها میتوان تک موج‌ها
را به صورت عمومی شناسایی کرد. ولیکن به صورت تخصصی هر موج
در الگوهای الیوتی فاصله بین دو برچسب پیشرفت (۵-۴-۳-۲-۱ یا
... C-B-A) مجاور از درجه یکسان میباشد."

"هر تغییری در جهت قیمت بر روی نمودار با یک نقطه مشخص شده است.
نقاط ابتدا و انتهای هر تک موج را مشخص می‌کنند.
این کرانه‌ها در معرض بازنگری هستند اگر حرکت قیمت تحت
شمول قانون خنثایی قرار گیرد. وقتی این قانون لحاظ شده
-و در جای مناسب به کار بسته شده- باشد، وضعیت نقاط
نهایی شده تلقی خواهد شد."

قوانین مستقیم از صفحه ۳۲:
۱. هر تغییر جهت قیمت = یک تک‌موج جدید
۲. نقاط ابتدا و انتها با کرانه‌های قیمتی (نقطه) مشخص می‌شوند
۳. کف «مهم»: اولین کف که با دایره در دیاگرام نشان داده شده
   (نقطه شروع کل ساختار موجی)
۴. تک‌موج = فاصله بین دو برچسب مجاور الیوتی از درجه یکسان
   مثال: بین ۱ و ۲، یا بین A و B
۵. کرانه‌ها (نقاط ابتدا/انتها) در معرض بازنگری هستند تا قانون
   خنثایی (فصل بعدی) اعمال شود
══════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from enum import Enum


# ══════════════════════════════════════════════════════════════
# بخش ۱: انواع داده
# ══════════════════════════════════════════════════════════════

class MonowaveDirection(Enum):
    UP      = "UP"
    DOWN    = "DOWN"
    UNKNOWN = "UNKNOWN"


class MonowaveStatus(Enum):
    """
    وضعیت تک‌موج - مطابق متن صفحه ۳۲:
    "وضعیت نقاط نهایی شده تلقی خواهد شد"
    """
    CONFIRMED  = "confirmed"   # نقاط نهایی شده
    TENTATIVE  = "tentative"   # در معرض بازنگری (قانون خنثایی هنوز اعمال نشده)
    INCOMPLETE = "incomplete"  # آخرین موج - هنوز در حال شکل‌گیری


class PointType(Enum):
    """
    نوع نقطه کرانه تک‌موج (ابتدا یا انتها)
    مطابق دیاگرام صفحه ۳۲ - نقاط با دایره مشخص شده‌اند
    """
    SWING_HIGH    = "swing_high"    # قله - سقف نوسانی
    SWING_LOW     = "swing_low"     # کف نوسانی
    IMPORTANT_LOW = "important_low" # کف «مهم» - با دایره در دیاگرام
    CLOSE_BASED   = "close_based"   # بر اساس قیمت بسته شدن (پشتیبان)


# ══════════════════════════════════════════════════════════════
# بخش ۲: ساختار داده تک‌موج
# ══════════════════════════════════════════════════════════════

@dataclass
class Monowave:
    """
    تک‌موج (Monowave) - واحد پایه تحلیل نئوویو
    مطابق تعریف صفحه ۳۲ کتاب نیلی:
    "فاصله بین دو نقطه تغییر جهت قیمت"
    """
    # شناسه
    index           : int

    # موقعیت زمانی
    start_bar       : int     # ایندکس کندل شروع
    end_bar         : int     # ایندکس کندل پایان

    # قیمت‌های کرانه (نقاط ابتدا و انتها)
    start_price     : float   # قیمت نقطه شروع
    end_price       : float   # قیمت نقطه پایان

    # مشخصات اصلی
    direction       : MonowaveDirection
    price_range     : float   # دامنه قیمتی = |end - start|
    duration        : int     # مدت زمانی = تعداد کندل

    # نوع نقاط کرانه
    start_type      : PointType
    end_type        : PointType

    # وضعیت (مطابق متن صفحه ۳۲)
    status          : MonowaveStatus

    # کف مهم (دیاگرام صفحه ۳۲: کف «مهم» با دایره)
    is_important_low: bool = False

    # Inside Bar: آیا کندل‌های داخلی در این تک‌موج ادغام شده‌اند؟
    has_inside_bars : bool = False
    inside_bar_count: int  = 0

    def __post_init__(self):
        # محاسبه مجدد برای اطمینان
        self.price_range = round(abs(self.end_price - self.start_price), 8)
        self.duration    = max(1, int(self.end_bar) - int(self.start_bar))

    @property
    def dir_str(self) -> str:
        return "صعودی" if self.direction == MonowaveDirection.UP else "نزولی"

    @property
    def slope(self) -> float:
        """شیب: دامنه قیمتی تقسیم بر مدت زمانی"""
        return self.price_range / self.duration if self.duration > 0 else 0.0

    @property
    def is_confirmed(self) -> bool:
        return self.status == MonowaveStatus.CONFIRMED


# ══════════════════════════════════════════════════════════════
# بخش ۳: شناسایی تک‌موج‌ها
# ══════════════════════════════════════════════════════════════

class MonowaveIdentifier:
    """
    شناسایی تک‌موج‌ها از داده OHLC
    مطابق فصل ۵ کتاب نیلی (صفحه ۳۲)

    الگوریتم چهار مرحله:
    ۱. ادغام Inside Bars (کندل‌های کاملاً درون کندل قبلی)
    ۲. شناسایی نقاط عطف (Swing High / Swing Low)
    ۳. حذف نقاط عطف هم‌نوع متوالی
    ۴. ساخت Monowave از نقاط عطف متوالی
    """

    def __init__(
        self,
        high   : np.ndarray,
        low    : np.ndarray,
        close  : np.ndarray,
        open_  : np.ndarray,
    ):
        self.high   = np.asarray(high,  dtype=float)
        self.low    = np.asarray(low,   dtype=float)
        self.close  = np.asarray(close, dtype=float)
        self.open_  = np.asarray(open_, dtype=float)
        self.n      = len(self.high)

    # ─────────────────────────────────────────────────────────
    # مرحله ۱: ادغام Inside Bars
    # ─────────────────────────────────────────────────────────

    def _merge_inside_bars(self) -> Tuple[
        np.ndarray, np.ndarray, List[int], List[int]
    ]:
        """
        ادغام کندل‌های Inside Bar با کندل مادر.

        Inside Bar = کندلی که:
            High آن ≤ High کندل قبلی
            Low  آن ≥ Low  کندل قبلی

        چنین کندلی اطلاعات جهت جدیدی اضافه نمی‌کند.
        با ادغام، کندل مادر همان High و Low را حفظ می‌کند.

        خروجی:
            merged_high    : آرایه High ادغام‌شده
            merged_low     : آرایه Low  ادغام‌شده
            orig_indices   : ایندکس اول هر گروه در داده اصلی
            inside_counts  : تعداد Inside Bar در هر گروه
        """
        merged_high  : List[float] = []
        merged_low   : List[float] = []
        orig_indices : List[int]   = []
        inside_counts: List[int]   = []

        i = 0
        while i < self.n:
            g_high    = float(self.high[i])
            g_low     = float(self.low[i])
            g_start   = i
            g_inside  = 0

            j = i + 1
            while j < self.n:
                nh = float(self.high[j])
                nl = float(self.low[j])
                if nh <= g_high and nl >= g_low:
                    # Inside Bar → ادغام: High/Low گروه تغییر نمی‌کند
                    g_inside += 1
                    j        += 1
                else:
                    break

            merged_high.append(g_high)
            merged_low.append(g_low)
            orig_indices.append(g_start)
            inside_counts.append(g_inside)
            i = j

        return (
            np.array(merged_high,  dtype=float),
            np.array(merged_low,   dtype=float),
            orig_indices,
            inside_counts,
        )

    # ─────────────────────────────────────────────────────────
    # مرحله ۲: شناسایی نقاط عطف
    # ─────────────────────────────────────────────────────────

    def _find_swing_points(
        self,
        m_high     : np.ndarray,
        m_low      : np.ndarray,
        orig_indices: List[int],
    ) -> List[Tuple[int, float, str]]:
        """
        شناسایی نقاط عطف روی داده ادغام‌شده.

        Swing High = نقطه‌ای که High آن از همسایگان بالاتر است
        Swing Low  = نقطه‌ای که Low  آن از همسایگان پایین‌تر است

        خروجی: لیست (orig_index, price, "HIGH"/"LOW")
        """
        n   = len(m_high)
        pts : List[Tuple[int, float, str]] = []

        if n == 0:
            return pts

        if n == 1:
            pts.append((orig_indices[0], float(m_high[0]), "HIGH"))
            pts.append((orig_indices[0], float(m_low[0]),  "LOW"))
            return pts

        if n == 2:
            if float(m_high[0]) >= float(m_high[1]):
                pts.append((orig_indices[0], float(m_high[0]), "HIGH"))
                pts.append((orig_indices[1], float(m_low[1]),  "LOW"))
            else:
                pts.append((orig_indices[0], float(m_low[0]),  "LOW"))
                pts.append((orig_indices[1], float(m_high[1]), "HIGH"))
            return pts

        # ── نقطه اول
        if float(m_high[0]) > float(m_high[1]):
            pts.append((orig_indices[0], float(m_high[0]), "HIGH"))
        elif float(m_low[0]) < float(m_low[1]):
            pts.append((orig_indices[0], float(m_low[0]), "LOW"))
        else:
            # اگر هر دو یکسان بودند: High را به عنوان اول قرار می‌دهیم
            pts.append((orig_indices[0], float(m_high[0]), "HIGH"))

        # ── نقاط میانی
        for i in range(1, n - 1):
            h_curr = float(m_high[i])
            h_prev = float(m_high[i - 1])
            h_next = float(m_high[i + 1])
            l_curr = float(m_low[i])
            l_prev = float(m_low[i - 1])
            l_next = float(m_low[i + 1])

            is_swing_high = (h_curr > h_prev) and (h_curr > h_next)
            is_swing_low  = (l_curr < l_prev) and (l_curr < l_next)

            if is_swing_high and is_swing_low:
                # هر دو در یک نقطه؟ → با توجه به آخرین نقطه تصمیم می‌گیریم
                last = pts[-1] if pts else None
                if last and last[2] == "HIGH":
                    pts.append((orig_indices[i], l_curr, "LOW"))
                else:
                    pts.append((orig_indices[i], h_curr, "HIGH"))
            elif is_swing_high:
                pts.append((orig_indices[i], h_curr, "HIGH"))
            elif is_swing_low:
                pts.append((orig_indices[i], l_curr, "LOW"))

        # ── نقطه آخر
        last_type = pts[-1][2] if pts else "HIGH"
        if last_type == "HIGH":
            pts.append((orig_indices[-1], float(m_low[-1]),  "LOW"))
        else:
            pts.append((orig_indices[-1], float(m_high[-1]), "HIGH"))

        return pts

    # ─────────────────────────────────────────────────────────
    # مرحله ۳: حذف نقاط هم‌نوع متوالی
    # ─────────────────────────────────────────────────────────

    @staticmethod
    def _remove_consecutive_same_type(
        pts: List[Tuple[int, float, str]]
    ) -> List[Tuple[int, float, str]]:
        """
        اگر دو HIGH یا دو LOW پشت‌سر هم آمدند:
        - دو HIGH: فقط بالاترین را نگه می‌داریم
        - دو LOW:  فقط پایین‌ترین را نگه می‌داریم

        این تضمین می‌کند که توالی همیشه HIGH→LOW→HIGH→...
        یا LOW→HIGH→LOW→... باشد.
        """
        if not pts:
            return []

        filtered = [pts[0]]

        for pt in pts[1:]:
            last = filtered[-1]
            if last[2] == pt[2]:
                # هم‌نوع: بهترین را نگه می‌داریم
                if pt[2] == "HIGH" and float(pt[1]) > float(last[1]):
                    filtered[-1] = pt
                elif pt[2] == "LOW" and float(pt[1]) < float(last[1]):
                    filtered[-1] = pt
                # در غیر این صورت: آخری را نگه می‌داریم (ایندکس بزرگتر)
                elif pt[0] > last[0]:
                    filtered[-1] = (pt[0], last[1], last[2])
            else:
                filtered.append(pt)

        return filtered

    # ─────────────────────────────────────────────────────────
    # مرحله ۴: ساخت Monowave از نقاط عطف
    # ─────────────────────────────────────────────────────────

    @staticmethod
    def _build_monowaves(
        pts          : List[Tuple[int, float, str]],
        inside_counts: List[int],
        orig_indices : List[int],
    ) -> List[Monowave]:
        """
        ساخت لیست Monowave از نقاط عطف متوالی.

        هر جفت نقطه عطف متوالی = یک تک‌موج.

        مطابق کتاب:
        - تک‌موج = فاصله بین دو نقطه تغییر جهت
        - وضعیت تأییدشده برای همه به‌جز آخری
        - آخری = ناتمام (در حال شکل‌گیری)
        """
        monowaves: List[Monowave] = []
        n_pts = len(pts)

        if n_pts < 2:
            return monowaves

        # محاسبه Inside Bar برای هر بازه
        def count_inside_in_range(start_orig: int, end_orig: int) -> int:
            total = 0
            for k, orig in enumerate(orig_indices):
                if start_orig <= orig < end_orig and k < len(inside_counts):
                    total += inside_counts[k]
            return total

        for i in range(n_pts - 1):
            idx0,  price0, type0 = pts[i]
            idx1,  price1, type1 = pts[i + 1]

            # جهت
            if price1 > price0:
                direction = MonowaveDirection.UP
            elif price1 < price0:
                direction = MonowaveDirection.DOWN
            else:
                continue  # دامنه صفر را نادیده می‌گیریم

            # نوع نقاط
            start_pt = PointType.SWING_LOW  if type0 == "LOW"  else PointType.SWING_HIGH
            end_pt   = PointType.SWING_HIGH if type1 == "HIGH" else PointType.SWING_LOW

            # وضعیت: آخرین = ناتمام، بقیه = در معرض بازنگری تا اعمال قانون خنثایی
            if i == n_pts - 2:
                status = MonowaveStatus.INCOMPLETE
            else:
                status = MonowaveStatus.TENTATIVE

            # شمارش Inside Bar
            ib_count = count_inside_in_range(int(idx0), int(idx1))

            # کف «مهم»: اولین نقطه عطف Low = کف «مهم» دیاگرام صفحه ۳۲
            is_imp_low = (i == 0 and type0 == "LOW")

            mw = Monowave(
                index=i,
                start_bar=int(idx0),
                end_bar=int(idx1),
                start_price=float(price0),
                end_price=float(price1),
                direction=direction,
                price_range=abs(float(price1) - float(price0)),
                duration=max(1, int(idx1) - int(idx0)),
                start_type=start_pt,
                end_type=end_pt,
                status=status,
                is_important_low=is_imp_low,
                has_inside_bars=ib_count > 0,
                inside_bar_count=ib_count,
            )
            monowaves.append(mw)

        # ── تأیید: موج‌هایی که دو موج بعد از آن‌ها تکمیل شده
        # مطابق منطق کتاب: وقتی موج بعدی کامل شد، موج قبلی تأیید می‌شود
        for i in range(len(monowaves)):
            if monowaves[i].status == MonowaveStatus.TENTATIVE:
                monowaves[i].status = MonowaveStatus.CONFIRMED

        # آخرین موج همچنان INCOMPLETE باقی می‌ماند
        if monowaves:
            monowaves[-1].status = MonowaveStatus.INCOMPLETE

        return monowaves

    # ─────────────────────────────────────────────────────────
    # روش پشتیبان: از Close
    # ─────────────────────────────────────────────────────────

    def _identify_from_close(self) -> List[Monowave]:
        """
        روش پشتیبان: شناسایی تک‌موج از قیمت بسته شدن
        در صورتی که داده کافی برای swing point نبود.
        """
        monowaves : List[Monowave] = []
        n = self.n

        if n < 2:
            return monowaves

        # پیدا کردن اولین تغییر جهت واقعی
        start_idx   = 0
        start_price = float(self.close[0])
        direction   : Optional[MonowaveDirection] = None

        for i in range(1, n):
            curr = float(self.close[i])
            if curr == start_price:
                continue

            new_dir = (
                MonowaveDirection.UP
                if curr > start_price
                else MonowaveDirection.DOWN
            )

            if direction is None:
                direction = new_dir
                continue

            if new_dir != direction:
                # تغییر جهت: تک‌موج قبلی کامل شد
                mw = Monowave(
                    index       = len(monowaves),
                    start_bar   = start_idx,
                    end_bar     = i - 1,
                    start_price = start_price,
                    end_price   = float(self.close[i - 1]),
                    direction   = direction,
                    price_range = abs(float(self.close[i - 1]) - start_price),
                    duration    = max(1, i - 1 - start_idx),
                    start_type  = PointType.CLOSE_BASED,
                    end_type    = PointType.CLOSE_BASED,
                    status      = MonowaveStatus.CONFIRMED,
                )
                monowaves.append(mw)
                start_idx   = i - 1
                start_price = float(self.close[i - 1])
                direction   = new_dir

        # آخرین تک‌موج ناتمام
        if direction is not None and start_idx < n - 1:
            monowaves.append(Monowave(
                index       = len(monowaves),
                start_bar   = start_idx,
                end_bar     = n - 1,
                start_price = start_price,
                end_price   = float(self.close[-1]),
                direction   = direction,
                price_range = abs(float(self.close[-1]) - start_price),
                duration    = max(1, n - 1 - start_idx),
                start_type  = PointType.CLOSE_BASED,
                end_type    = PointType.CLOSE_BASED,
                status      = MonowaveStatus.INCOMPLETE,
            ))

        return monowaves

    # ─────────────────────────────────────────────────────────
    # تابع اصلی: identify
    # ─────────────────────────────────────────────────────────

    def identify(self) -> List[Monowave]:
        """
        شناسایی کامل تک‌موج‌ها
        مطابق الگوریتم فصل ۵ کتاب نیلی (صفحه ۳۲)

        خروجی: لیست Monowave های شناسایی‌شده، مرتب از قدیم به جدید
        """
        if self.n < 2:
            return []

        # ── مرحله ۱: ادغام Inside Bars
        m_high, m_low, orig_idx, inside_cnts = self._merge_inside_bars()

        if len(m_high) < 2:
            return self._identify_from_close()

        # ── مرحله ۲: نقاط عطف
        pts = self._find_swing_points(m_high, m_low, orig_idx)

        if len(pts) < 2:
            return self._identify_from_close()

        # ── مرحله ۳: حذف هم‌نوع‌های متوالی
        pts = self._remove_consecutive_same_type(pts)

        if len(pts) < 2:
            return self._identify_from_close()

        # ── مرحله ۴: ساخت Monowave
        monowaves = self._build_monowaves(pts, inside_cnts, orig_idx)

        if not monowaves:
            return self._identify_from_close()

        return monowaves


# ══════════════════════════════════════════════════════════════
# بخش ۴: آمار و تحلیل
# ══════════════════════════════════════════════════════════════

def _compute_stats(monowaves: List[Monowave]) -> Dict:
    """محاسبه آمار کامل مجموعه تک‌موج‌ها"""
    if not monowaves:
        return {}

    up   = [m for m in monowaves if m.direction == MonowaveDirection.UP]
    down = [m for m in monowaves if m.direction == MonowaveDirection.DOWN]
    conf = [m for m in monowaves if m.status == MonowaveStatus.CONFIRMED]

    ranges    = [m.price_range for m in monowaves if m.price_range > 0]
    durations = [m.duration    for m in monowaves]
    slopes    = [m.slope       for m in monowaves if m.slope > 0]

    up_ranges   = [m.price_range for m in up   if m.price_range > 0]
    down_ranges = [m.price_range for m in down if m.price_range > 0]
    up_durs     = [m.duration    for m in up]
    down_durs   = [m.duration    for m in down]

    last = monowaves[-1]

    # نسبت دامنه صعودی به نزولی
    avg_up   = float(np.mean(up_ranges))   if up_ranges   else 0.0
    avg_down = float(np.mean(down_ranges)) if down_ranges else 0.0
    ratio_ud = round(avg_up / avg_down, 3) if avg_down > 0 else 0.0

    # پایین‌ترین کف (نقطه شروع کف «مهم»)
    low_prices  = [m.start_price for m in up]
    high_prices = [m.start_price for m in down]

    return {
        # شمارش
        "تعداد_کل"              : len(monowaves),
        "تعداد_صعودی"           : len(up),
        "تعداد_نزولی"           : len(down),
        "تعداد_تأییدشده"        : len(conf),
        "تعداد_ناتمام"          : sum(1 for m in monowaves if m.status == MonowaveStatus.INCOMPLETE),
        "تعداد_با_inside_bar"   : sum(1 for m in monowaves if m.has_inside_bars),

        # دامنه
        "میانگین_دامنه"         : round(float(np.mean(ranges)),   4) if ranges else 0.0,
        "بیشترین_دامنه"         : round(float(np.max(ranges)),    4) if ranges else 0.0,
        "کمترین_دامنه"          : round(float(np.min(ranges)),    4) if ranges else 0.0,
        "انحراف_معیار_دامنه"    : round(float(np.std(ranges)),    4) if ranges else 0.0,
        "میانه_دامنه"           : round(float(np.median(ranges)), 4) if ranges else 0.0,

        # مدت
        "میانگین_مدت"           : round(float(np.mean(durations)), 2) if durations else 0.0,
        "بیشترین_مدت"           : int(np.max(durations)) if durations else 0,
        "کمترین_مدت"            : int(np.min(durations)) if durations else 0,

        # شیب
        "میانگین_شیب"           : round(float(np.mean(slopes)), 6) if slopes else 0.0,
        "بیشترین_شیب"           : round(float(np.max(slopes)),  6) if slopes else 0.0,

        # صعودی
        "میانگین_دامنه_صعودی"   : round(avg_up,                  4),
        "میانگین_مدت_صعودی"     : round(float(np.mean(up_durs)), 2) if up_durs   else 0.0,

        # نزولی
        "میانگین_دامنه_نزولی"   : round(avg_down,                  4),
        "میانگین_مدت_نزولی"     : round(float(np.mean(down_durs)), 2) if down_durs else 0.0,

        # نسبت
        "نسبت_دامنه_صعودی_نزولی": ratio_ud,

        # سطوح
        "پایین‌ترین_کف"         : round(min(low_prices),   4) if low_prices   else 0.0,
        "بالاترین_سقف"          : round(max(high_prices),  4) if high_prices  else 0.0,

        # آخرین موج
        "آخرین_جهت"             : last.dir_str,
        "آخرین_شروع_قیمت"       : round(float(last.start_price), 4),
        "آخرین_پایان_قیمت"      : round(float(last.end_price),   4),
        "آخرین_دامنه"           : round(float(last.price_range), 4),
        "آخرین_مدت_کندل"        : last.duration,
        "آخرین_شروع_کندل"       : last.start_bar,
        "آخرین_پایان_کندل"      : last.end_bar,
        "آخرین_وضعیت"           : last.status.value,
        "آخرین_نوع_شروع"        : last.start_type.value,
        "آخرین_نوع_پایان"        : last.end_type.value,
    }


def _check_alternation(monowaves: List[Monowave]) -> Dict:
    """
    بررسی تناوب صحیح جهت‌ها
    (شرط اولیه قبل از اعمال قوانین فصل‌های بعدی)
    """
    if len(monowaves) < 2:
        return {"تناوب_صحیح": True, "تعداد_خطا": 0, "اولین_خطا": ""}

    errors = []
    for i in range(1, len(monowaves)):
        if monowaves[i].direction == monowaves[i - 1].direction:
            errors.append(
                f"موج {i} و {i-1}: هر دو {monowaves[i].dir_str} — "
                f"احتمال نیاز به بازبینی Inside Bar"
            )

    return {
        "تناوب_صحیح"  : len(errors) == 0,
        "تعداد_خطا"   : len(errors),
        "اولین_خطا"   : errors[0] if errors else "",
    }


# ══════════════════════════════════════════════════════════════
# بخش ۵: تابع analyze — interface کد هسته (main.py)
# ══════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None, context=None) -> Dict:
    """
    فصل ۵: شناسایی تک موج‌ها (Monowave Identification)

    Interface مطابق main.py:
        data   : pd.DataFrame با ستون‌های open/high/low/close/volume
        logger : ResultsLogger | None
        return : dict — همه key و value از نوع str
    """

    # ── استخراج ایمن ستون‌ها ──────────────────────────────────
    def _col(df: pd.DataFrame, *names) -> np.ndarray:
        for nm in names:
            if nm in df.columns:
                return df[nm].astype(float).values
        return np.zeros(len(df), dtype=float)

    close  = _col(data, "close",  "Close")
    high   = _col(data, "high",   "High")
    low    = _col(data, "low",    "Low")
    open_  = _col(data, "open",   "Open")
    n      = len(close)

    # ── دریافت اطلاعات از فصل‌های ۲، ۳، ۴، ۹ ────────────────
    monowaves_from_ch2 = None
    cycles_from_ch3 = None
    cash_data_from_ch4 = None
    gaps_from_ch9 = None
    context_used = False
    
    if context:
        if "chapter_2" in context and "_monowaves" in context["chapter_2"]:
            monowaves_from_ch2 = context["chapter_2"]["_monowaves"]
            context_used = True
        if "chapter_3" in context and "_complete_cycles" in context["chapter_3"]:
            cycles_from_ch3 = context["chapter_3"]["_complete_cycles"]
        if "chapter_4" in context and "_cash_data_full" in context["chapter_4"]:
            cash_data_from_ch4 = context["chapter_4"]["_cash_data_full"]
        if "chapter_9" in context and "_gaps" in context["chapter_9"]:
            gaps_from_ch9 = context["chapter_9"]["_gaps"]

    # ── حداقل داده ────────────────────────────────────────────
    if n < 3:
        out = {
            "عنوان"     : "فصل ۵: شناسایی تک موج‌ها",
            "وضعیت"     : "داده_کافی_نیست",
            "تعداد_کندل": str(n),
        }
        if logger:
            logger.add_section("فصل ۵: شناسایی تک موج‌ها", level=1)
            logger.add_result("وضعیت", "داده کافی نیست")
        return out

    # ── شناسایی تک‌موج‌ها ────────────────────────────────────
    monowaves = []
    context_used = False

    # اولویت ۱: از فصل ۴ (کش دیتا)
    if cash_data_from_ch4:
        cd_mw_raw = cash_data_from_ch4.get("monowaves", [])
        if cd_mw_raw and len(cd_mw_raw) > 0:
            for idx, mw_raw in enumerate(cd_mw_raw):
                direction = MonowaveDirection.UP if mw_raw.get("direction", 1) == 1 else MonowaveDirection.DOWN
                status = MonowaveStatus.INCOMPLETE if idx == len(cd_mw_raw) - 1 else MonowaveStatus.CONFIRMED
                start_type = PointType.SWING_LOW if direction == MonowaveDirection.DOWN else PointType.SWING_HIGH
                end_type = PointType.SWING_HIGH if direction == MonowaveDirection.UP else PointType.SWING_LOW
            
                new_mw = Monowave(
                    index=idx,
                    start_bar=int(mw_raw.get("start_bar", 0)),
                    end_bar=int(mw_raw.get("end_bar", 0)),
                    start_price=float(mw_raw.get("start_price", 0)),
                    end_price=float(mw_raw.get("end_price", 0)),
                    direction=direction,
                    price_range=float(mw_raw.get("price_range", 0)),
                    duration=max(1, int(mw_raw.get("end_bar", 0)) - int(mw_raw.get("start_bar", 0))),
                    start_type=start_type,
                    end_type=end_type,
                    status=status,
                    is_important_low=(idx == 0 and direction == MonowaveDirection.DOWN),
                    has_inside_bars=False,
                    inside_bar_count=0
                )
                monowaves.append(new_mw)
            context_used = True

    # اولویت ۲: از فصل ۲
    if not monowaves and monowaves_from_ch2 and len(monowaves_from_ch2) > 0:
        for idx, mw in enumerate(monowaves_from_ch2):
            direction = MonowaveDirection.UP if mw.direction == 1 else MonowaveDirection.DOWN
            status = MonowaveStatus.INCOMPLETE if idx == len(monowaves_from_ch2) - 1 else     MonowaveStatus.CONFIRMED
            start_type = PointType.SWING_LOW if mw.direction == -1 else PointType.SWING_HIGH
            end_type = PointType.SWING_HIGH if mw.direction == 1 else PointType.SWING_LOW
        
            new_mw = Monowave(
                index=idx,
                start_bar=mw.start_idx,
                end_bar=mw.end_idx,
                start_price=mw.start_price,
                end_price=mw.end_price,
                direction=direction,
                price_range=mw.price_range,
                duration=mw.duration,
                start_type=start_type,
                end_type=end_type,
                status=status,
                is_important_low=(idx == 0 and direction == MonowaveDirection.DOWN),
                has_inside_bars=False,
                inside_bar_count=0
            )
            monowaves.append(new_mw)
        context_used = True

    # اولویت ۳: خودمون استخراج
    if not monowaves:
        identifier = MonowaveIdentifier(high=high, low=low, close=close, open_=open_)
        monowaves = identifier.identify()
    
    stats  = _compute_stats(monowaves)
    altchk = _check_alternation(monowaves)

    

    # کف‌های مهم
    important_lows = [m for m in monowaves if m.is_important_low]

    # ── ساخت dict خروجی (همه value → str) ────────────────────
    results: Dict = {
        # ─ شناسنامه
        "عنوان"                          : "فصل ۵: شناسایی تک موج‌ها (Monowave Identification)",
        "مرجع"                           : "صفحه ۳۲ - گلن نیلی",
        "وضعیت"                          : "تحلیل_کامل",

        # ─ تعاریف کتاب
        "تعریف"                          : "هر تغییری در جهت قیمت = یک تک‌موج جدید",
        "کرانه‌ها"                       : "نقاط ابتدا و انتها کرانه‌های هر تک‌موج هستند",
        "کف_مهم"                         : "اولین کف - با دایره در دیاگرام صفحه ۳۲ مشخص شده",
        "وضعیت_نقاط"                     : "در معرض بازنگری تا قانون خنثایی (فصل بعدی) اعمال شود",

        # ─ آمار پایه
        "تعداد_کندل"                     : str(n),
        "تعداد_کل_تک‌موج"               : str(stats.get("تعداد_کل", 0)),
        "تعداد_صعودی"                    : str(stats.get("تعداد_صعودی", 0)),
        "تعداد_نزولی"                    : str(stats.get("تعداد_نزولی", 0)),
        "تعداد_تأییدشده"                 : str(stats.get("تعداد_تأییدشده", 0)),
        "تعداد_ناتمام"                   : str(stats.get("تعداد_ناتمام", 0)),
        "تعداد_با_inside_bar"            : str(stats.get("تعداد_با_inside_bar", 0)),
        "تعداد_کف_مهم"                   : str(len(important_lows)),

        # ─ دامنه قیمتی
        "میانگین_دامنه"                  : str(stats.get("میانگین_دامنه", 0)),
        "بیشترین_دامنه"                  : str(stats.get("بیشترین_دامنه", 0)),
        "کمترین_دامنه"                   : str(stats.get("کمترین_دامنه", 0)),
        "انحراف_معیار_دامنه"             : str(stats.get("انحراف_معیار_دامنه", 0)),
        "میانه_دامنه"                    : str(stats.get("میانه_دامنه", 0)),

        # ─ مدت زمانی
        "میانگین_مدت_کندل"               : str(stats.get("میانگین_مدت", 0)),
        "بیشترین_مدت_کندل"               : str(stats.get("بیشترین_مدت", 0)),
        "کمترین_مدت_کندل"                : str(stats.get("کمترین_مدت", 0)),

        # ─ مقایسه صعودی و نزولی
        "میانگین_دامنه_صعودی"            : str(stats.get("میانگین_دامنه_صعودی", 0)),
        "میانگین_دامنه_نزولی"            : str(stats.get("میانگین_دامنه_نزولی", 0)),
        "میانگین_مدت_صعودی"              : str(stats.get("میانگین_مدت_صعودی", 0)),
        "میانگین_مدت_نزولی"              : str(stats.get("میانگین_مدت_نزولی", 0)),
        "نسبت_دامنه_صعودی_به_نزولی"      : str(stats.get("نسبت_دامنه_صعودی_نزولی", 0)),

        # ─ سطوح
        "پایین‌ترین_کف"                  : str(stats.get("پایین‌ترین_کف", 0)),
        "بالاترین_سقف"                   : str(stats.get("بالاترین_سقف", 0)),

        # ─ بررسی تناوب
        "تناوب_جهت_صحیح"                 : "بله" if altchk["تناوب_صحیح"] else "خیر",
        "تعداد_خطای_تناوب"               : str(altchk["تعداد_خطا"]),

        # ─ آخرین تک‌موج
        "آخرین_جهت"                      : str(stats.get("آخرین_جهت", "")),
        "آخرین_شروع_قیمت"                : str(stats.get("آخرین_شروع_قیمت", 0)),
        "آخرین_پایان_قیمت"               : str(stats.get("آخرین_پایان_قیمت", 0)),
        "آخرین_دامنه"                    : str(stats.get("آخرین_دامنه", 0)),
        "آخرین_مدت_کندل"                 : str(stats.get("آخرین_مدت_کندل", 0)),
        "آخرین_وضعیت"                    : str(stats.get("آخرین_وضعیت", "")),
        "آخرین_نوع_شروع"                 : str(stats.get("آخرین_نوع_شروع", "")),
        "آخرین_نوع_پایان"                : str(stats.get("آخرین_نوع_پایان", "")),

        # ─ وضعیت قیمتی
        "قیمت_فعلی"                      : str(round(float(close[-1]), 4)),
        "بالاترین_قیمت_کل"               : str(round(float(np.max(high)), 4)),
        "پایین‌ترین_قیمت_کل"             : str(round(float(np.min(low)),  4)),
    }

    # ─ جزئیات ۱۰ تک‌موج آخر ───────────────────────────────
    last_mws = monowaves[-10:] if len(monowaves) >= 10 else monowaves
    for rank, mw in enumerate(reversed(last_mws), start=1):
        p = f"موج_آخر_{rank}"
        results[f"{p}_جهت"]        = mw.dir_str
        results[f"{p}_شروع_قیمت"]  = str(round(float(mw.start_price), 4))
        results[f"{p}_پایان_قیمت"] = str(round(float(mw.end_price),   4))
        results[f"{p}_دامنه"]      = str(round(float(mw.price_range), 4))
        results[f"{p}_مدت_کندل"]   = str(mw.duration)
        results[f"{p}_وضعیت"]      = mw.status.value
        results[f"{p}_نوع_شروع"]   = mw.start_type.value
        results[f"{p}_نوع_پایان"]  = mw.end_type.value

    # ─ تفسیر نهایی ─────────────────────────────────────────
    results["تفسیر_نهایی"] = _build_interpretation(
        n, monowaves, stats, altchk, important_lows
    )

    # ⭐ منبع داده
    results["_source"] = "از_فصل_2_3_4_9" if context_used else "مستقل"
    results["_monowaves_from_ch2"] = len(monowaves_from_ch2) if monowaves_from_ch2 else 0
    results["_cycles_from_ch3"] = len(cycles_from_ch3) if cycles_from_ch3 else 0
    results["_cash_data_used"] = "بله" if cash_data_from_ch4 else "خیر"
    results["_gaps_from_ch9"] = len(gaps_from_ch9) if gaps_from_ch9 else 0
    results["_monowaves"] = monowaves

    # ─ لاگ ──────────────────────────────────────────────────
    if logger:
        _write_log(logger, results, monowaves, important_lows)

    return results


# ══════════════════════════════════════════════════════════════
# بخش ۶: تفسیر متنی
# ══════════════════════════════════════════════════════════════

def _build_interpretation(
    n          : int,
    monowaves  : List[Monowave],
    stats      : Dict,
    altchk     : Dict,
    imp_lows   : List[Monowave],
) -> str:

    seq_st  = "✓ تناوب صحیح" if altchk["تناوب_صحیح"] else f"⚠ {altchk['تعداد_خطا']} خطا"
    last    = monowaves[-1] if monowaves else None
    n_total = stats.get("تعداد_کل", 0)

    # ۵ تک‌موج آخر
    last5_lines = ""
    for mw in reversed(monowaves[-5:]):
        last5_lines += (
            f"\n    [{mw.index:3d}] {mw.dir_str:6s} | "
            f"{mw.start_price:>10.4f} → {mw.end_price:>10.4f} | "
            f"دامنه={mw.price_range:>9.4f} | {mw.duration:3d} کندل | "
            f"{mw.status.value}"
        )

    # کف مهم
    imp_str = ""
    for il in imp_lows[:2]:
        imp_str += (
            f"\n    کف مهم: قیمت={il.start_price:.4f} | "
            f"کندل={il.start_bar}"
        )

    last_line = ""
    if last:
        last_line = (
            f"\n    جهت: {last.dir_str} | "
            f"از {last.start_price:.4f} به {last.end_price:.4f} | "
            f"دامنه={last.price_range:.4f} | {last.duration} کندل | "
            f"وضعیت: {last.status.value}"
        )

    return f"""
══════════════════════════════════════════════════════════════════
  فصل ۵: شناسایی تک موج‌ها (Monowave Identification)
  مرجع: صفحه ۳۲  |  گلن نیلی
══════════════════════════════════════════════════════════════════

📖 تعریف کتاب (صفحه ۳۲):
   "هر تغییری در جهت قیمت بر روی نمودار با یک نقطه مشخص
   شده است. نقاط ابتدا و انتهای هر تک موج را مشخص می‌کنند."

📊 آمار کلی:
   کندل             : {n}
   کل تک‌موج        : {n_total}
   صعودی            : {stats.get('تعداد_صعودی', 0)}
   نزولی            : {stats.get('تعداد_نزولی', 0)}
   تأییدشده         : {stats.get('تعداد_تأییدشده', 0)}
   با Inside Bar    : {stats.get('تعداد_با_inside_bar', 0)}

📐 آمار دامنه قیمتی:
   میانگین          : {stats.get('میانگین_دامنه', 0)}
   بیشترین          : {stats.get('بیشترین_دامنه', 0)}
   کمترین           : {stats.get('کمترین_دامنه', 0)}
   انحراف معیار     : {stats.get('انحراف_معیار_دامنه', 0)}
   میانه            : {stats.get('میانه_دامنه', 0)}

📏 مقایسه صعودی / نزولی:
   میانگین دامنه ↑  : {stats.get('میانگین_دامنه_صعودی', 0)}
   میانگین دامنه ↓  : {stats.get('میانگین_دامنه_نزولی', 0)}
   نسبت ↑ / ↓       : {stats.get('نسبت_دامنه_صعودی_نزولی', 0)}
   میانگین مدت ↑    : {stats.get('میانگین_مدت_صعودی', 0)} کندل
   میانگین مدت ↓    : {stats.get('میانگین_مدت_نزولی', 0)} کندل

🔄 بررسی تناوب جهت: {seq_st}

🔵 کف مهم (دیاگرام صفحه ۳۲):{imp_str if imp_str else chr(10) + '   شناسایی نشد'}

📍 آخرین تک‌موج:{last_line}

📋 ۵ تک‌موج آخر:{last5_lines}
══════════════════════════════════════════════════════════════════"""


# ══════════════════════════════════════════════════════════════
# بخش ۷: ثبت در لاگ
# ══════════════════════════════════════════════════════════════

def _write_log(
    logger,
    results   : Dict,
    monowaves : List[Monowave],
    imp_lows  : List[Monowave],
) -> None:
    logger.add_section("فصل ۵: شناسایی تک موج‌ها", level=1)
    logger.add_result("مرجع",             results["مرجع"])
    logger.add_result("تعریف",            results["تعریف"])
    logger.add_result("تعداد کندل",       results["تعداد_کندل"])
    logger.add_result("کل تک‌موج",        results["تعداد_کل_تک‌موج"])
    logger.add_result("صعودی",            results["تعداد_صعودی"])
    logger.add_result("نزولی",            results["تعداد_نزولی"])
    logger.add_result("تأییدشده",         results["تعداد_تأییدشده"])
    logger.add_result("با Inside Bar",    results["تعداد_با_inside_bar"])
    logger.add_result("کف مهم",           results["تعداد_کف_مهم"])

    logger.add_section("آمار دامنه قیمتی", level=2)
    logger.add_result("میانگین",          results["میانگین_دامنه"])
    logger.add_result("بیشترین",          results["بیشترین_دامنه"])
    logger.add_result("کمترین",           results["کمترین_دامنه"])
    logger.add_result("انحراف معیار",     results["انحراف_معیار_دامنه"])
    logger.add_result("میانه",            results["میانه_دامنه"])

    logger.add_section("مقایسه صعودی / نزولی", level=2)
    logger.add_result("میانگین دامنه صعودی", results["میانگین_دامنه_صعودی"])
    logger.add_result("میانگین دامنه نزولی", results["میانگین_دامنه_نزولی"])
    logger.add_result("نسبت",               results["نسبت_دامنه_صعودی_به_نزولی"])
    logger.add_result("میانگین مدت صعودی",  results["میانگین_مدت_صعودی"])
    logger.add_result("میانگین مدت نزولی",  results["میانگین_مدت_نزولی"])

    logger.add_section("تناوب جهت", level=2)
    logger.add_result("تناوب صحیح",       results["تناوب_جهت_صحیح"])
    logger.add_result("تعداد خطا",        results["تعداد_خطای_تناوب"])

    logger.add_section("کف‌های مهم (صفحه ۳۲)", level=2)
    for mw in imp_lows[:5]:
        logger.add_wave(f"کف مهم {mw.index}", {
            "قیمت"        : round(float(mw.start_price), 4),
            "کندل"        : mw.start_bar,
            "جهت_بعدی"   : mw.dir_str,
            "دامنه_بعدی" : round(float(mw.price_range), 4),
        })

    logger.add_section("آخرین تک‌موج", level=2)
    logger.add_result("جهت",        results["آخرین_جهت"])
    logger.add_result("شروع",       results["آخرین_شروع_قیمت"])
    logger.add_result("پایان",      results["آخرین_پایان_قیمت"])
    logger.add_result("دامنه",      results["آخرین_دامنه"])
    logger.add_result("مدت کندل",   results["آخرین_مدت_کندل"])
    logger.add_result("وضعیت",      results["آخرین_وضعیت"])

    logger.add_result("تفسیر",      results["تفسیر_نهایی"])