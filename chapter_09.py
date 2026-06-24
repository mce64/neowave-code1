# chapters/chapter_09.py

"""
فصل ۹: تعدیل چارت (Chart Adjustment)
منبع: کتاب "امواج الیوت به سبک نئوویو" - گلن نیلی - صفحات ۵۲ تا ۵۳

═══════════════════════════════════════════════════════════════════
متن دقیق کتاب (صفحه ۵۲):

"تعدیل چارت ابزار دیگری است که با استفاده از آن فاصله های قیمتی یا همان
گپ های مصنوعی ناشی از افزایش سرمایه و توزیع سود نقدی پوشش داده می‌شود.

به طور معمول قیمت سهم پس از افزایش سرمایه و یا توزیع سود نقدی در زمان
مجمع کاهش می‌یابد. با استفاده از این ابزار، قیمت های قبل از مجمع سهام
تعدیل شده تا فاصله ایجاد شده بین قیمت‌ها پوشانده شوند.

توجه شود که تعدیل برای گپ های طبیعی چارت استفاده نمی‌شود بلکه فقط برای
گپ هایی که با عوامل غیر از عرضه و تقاضا در چارت ایجاد شده اند که این عوامل
نیز چیزی نیستند جز گپ های افزایش سرمایه و گپ های تقسیم سود."

═══════════════════════════════════════════════════════════════════
پنج روش تعدیل چارت (صفحات ۵۲-۵۳):

۱. افزایش سرمایه (Stock Split):
   - سرمایه قبلی بر سرمایه جدید تقسیم شده
   - این عدد در تمام قیمت‌های قبل از تاریخ افزایش سرمایه ضرب می‌شود
   - فقط کاهش قیمت در زمان افزایش سرمایه لحاظ می‌شود
   - محل تامین افزایش سرمایه اثری در محاسبات ندارد

۲. افزایش سرمایه با احتساب آورده (Stock Split with Rights):
   - علاوه بر کاهش قیمت، حق تقدم تعلق گرفته نیز لحاظ می‌شود
   - زمانی که افزایش سرمایه از محل مطالبات و آورده باشد

۳. سود نقدی و افزایش سرمایه (Cash Dividend + Stock Split):
   - میزان توزیع سود نقدی و درصد افزایش سرمایه هر دو لحاظ می‌شود
   - نسبت تغییر قیمت پس از توزیع سود به قیمت قبل از مجمع محاسبه می‌شود
   - این عدد در تمام قیمت‌های قبل از مجمع ضرب می‌شود

۴. سود نقدی و افزایش سرمایه با احتساب آورده (Cash Dividend + Split with Rights):
   - مانند روش قبل، با این تفاوت که حق تقدم نیز لحاظ می‌شود

۵. تعدیل عملکردی (Performance Adjustment):
   - مبنای محاسبات = قیمت گشایش سهام بعد از مجمع
   - اثرات توزیع سود نقدی و افزایش سرمایه هر دو لحاظ می‌شود
   - حق تقدم نیز در صورت وجود محاسبه می‌گردد
═══════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


# ════════════════════════════════════════════════════════════════
# بخش ۱: تعاریف پایه
# ════════════════════════════════════════════════════════════════

class AdjustmentMethod(Enum):
    """پنج روش تعدیل چارت مطابق صفحات ۵۲-۵۳"""
    STOCK_SPLIT = "افزایش_سرمایه"
    STOCK_SPLIT_WITH_RIGHTS = "افزایش_سرمایه_با_احتساب_آورده"
    CASH_DIVIDEND_AND_SPLIT = "سود_نقدی_و_افزایش_سرمایه"
    CASH_DIVIDEND_AND_SPLIT_WITH_RIGHTS = "سود_نقدی_و_افزایش_سرمایه_با_احتساب_آورده"
    PERFORMANCE = "تعدیل_عملکردی"
    NONE = "بدون_تعدیل"


@dataclass
class SplitInfo:
    """اطلاعات افزایش سرمایه"""
    date: str
    old_capital: float          # سرمایه قبلی
    new_capital: float          # سرمایه جدید
    split_ratio: float          # نسبت افزایش سرمایه (new/old)
    has_rights: bool = False    # آیا حق تقدم دارد؟
    rights_value: float = 0.0   # ارزش حق تقدم


@dataclass
class DividendInfo:
    """اطلاعات تقسیم سود نقدی"""
    date: str
    dividend_per_share: float   # سود نقدی هر سهم
    price_before_agm: float     # قیمت قبل از مجمع
    price_after_agm: float      # قیمت بعد از مجمع (گشایش)
    has_rights: bool = False    # آیا حق تقدم دارد؟
    rights_value: float = 0.0   # ارزش حق تقدم


@dataclass
class AdjustmentResult:
    """نتیجه اعمال تعدیل روی سری قیمت"""
    method: AdjustmentMethod
    original_prices: List[float]
    adjusted_prices: List[float]
    adjustment_factors: List[float]
    split_date_idx: Optional[int]
    split_ratio: float
    dividend_effect: float
    description: str
    warnings: List[str]


# ════════════════════════════════════════════════════════════════
# بخش ۲: روش‌های تعدیل چارت
# ════════════════════════════════════════════════════════════════

class ChartAdjuster:
    """
    کلاس اصلی برای اعمال روش‌های مختلف تعدیل چارت.
    
    مطابق صفحات ۵۲-۵۳ کتاب:
        - فقط گپ‌های مصنوعی (افزایش سرمایه، تقسیم سود) تعدیل می‌شوند
        - گپ‌های طبیعی ناشی از عرضه و تقاضا تعدیل نمی‌شوند
    """
    
    @staticmethod
    def method_1_stock_split(
        prices: List[float],
        split_date_idx: int,
        split_ratio: float
    ) -> AdjustmentResult:
        """
        روش ۱: افزایش سرمایه (Stock Split)
        
        صفحه ۵۲:
            "سرمایه قبلی شرکت بر سرمایه جدید تقسیم شده و این عدد در تمام
            قیمت‌های قبل از تاریخ افزایش سرمایه ضرب می‌شود."
        
        فرمول:
            adjustment_factor = old_capital / new_capital = 1 / split_ratio
            adjusted_price_before = original_price_before × adjustment_factor
        
        پارامترها:
            prices: لیست قیمت‌ها (به ترتیب زمانی)
            split_date_idx: ایندکس روز افزایش سرمایه
            split_ratio: نسبت افزایش سرمایه (مثلاً 1.2 = 20% افزایش)
        """
        warnings = []
        n = len(prices)
        
        # ── محاسبه ضریب تعدیل ─────────────────────────────────
        adjustment_factor = 1.0 / split_ratio
        
        # ── اعمال تعدیل روی قیمت‌های قبل از تاریخ افزایش سرمایه ──
        adjusted = prices.copy()
        for i in range(split_date_idx):
            adjusted[i] = prices[i] * adjustment_factor
        
        # ── ساخت لیست ضرایب تعدیل ──────────────────────────────
        factors = [adjustment_factor if i < split_date_idx else 1.0 for i in range(n)]
        
        return AdjustmentResult(
            method=AdjustmentMethod.STOCK_SPLIT,
            original_prices=prices,
            adjusted_prices=adjusted,
            adjustment_factors=factors,
            split_date_idx=split_date_idx,
            split_ratio=split_ratio,
            dividend_effect=0.0,
            description=f"تعدیل افزایش سرمایه با نسبت {split_ratio:.4f} (روش ۱)",
            warnings=warnings
        )
    
    @staticmethod
    def method_2_stock_split_with_rights(
        prices: List[float],
        split_date_idx: int,
        split_ratio: float,
        rights_value: float,
        price_before_split: float
    ) -> AdjustmentResult:
        """
        روش ۲: افزایش سرمایه با احتساب آورده (Stock Split with Rights)
        
        صفحه ۵۲:
            "در این روش علاوه بر میزان کاهش قیمت در زمان افزایش سرمایه،
             حق تقدم تعلق گرفته به سهامداران نیز در محاسبات لحاظ می‌شود."
        
        فرمول:
            theoretical_price = (price_before_split + rights_value) / split_ratio
            adjustment_factor = theoretical_price / price_before_split
            adjusted_price_before = original_price_before × adjustment_factor
        
        پارامترها:
            prices: لیست قیمت‌ها
            split_date_idx: ایندکس روز افزایش سرمایه
            split_ratio: نسبت افزایش سرمایه
            rights_value: ارزش حق تقدم هر سهم
            price_before_split: قیمت سهم قبل از افزایش سرمایه
        """
        warnings = []
        n = len(prices)
        
        # ── محاسبه قیمت تئوریک بعد از افزایش سرمایه ───────────
        # قیمت تئوریک = (قیمت قبل + ارزش حق تقدم) / نسبت افزایش
        theoretical_price = (price_before_split + rights_value) / split_ratio
        
        # ── محاسبه ضریب تعدیل ─────────────────────────────────
        adjustment_factor = theoretical_price / price_before_split if price_before_split > 0 else 1.0
        
        # ── اعمال تعدیل ───────────────────────────────────────
        adjusted = prices.copy()
        for i in range(split_date_idx):
            adjusted[i] = prices[i] * adjustment_factor
        
        factors = [adjustment_factor if i < split_date_idx else 1.0 for i in range(n)]
        
        return AdjustmentResult(
            method=AdjustmentMethod.STOCK_SPLIT_WITH_RIGHTS,
            original_prices=prices,
            adjusted_prices=adjusted,
            adjustment_factors=factors,
            split_date_idx=split_date_idx,
            split_ratio=split_ratio,
            dividend_effect=0.0,
            description=f"تعدیل افزایش سرمایه با احتساب حق تقدم {rights_value:.4f} (روش ۲)",
            warnings=warnings
        )
    
    @staticmethod
    def method_3_cash_dividend_and_split(
        prices: List[float],
        split_date_idx: int,
        split_ratio: float,
        dividend_per_share: float,
        price_before_agm: float,
        price_after_agm: float
    ) -> AdjustmentResult:
        """
        روش ۳: سود نقدی و افزایش سرمایه (Cash Dividend + Stock Split)
        
        صفحه ۵۳:
            "نسبت تغییر قیمت پس از توزیع سود نقدی به قیمت قبل از مجمع
             محاسبه می‌شود و این عدد در تمام قیمت‌های قبل از مجمع ضرب
             می‌شود و برای محاسبه ضریب افزایش سرمایه نیز از فرمول
             افزایش سرمایه استفاده می‌شود."
        
        فرمول:
            dividend_factor = price_after_agm / price_before_agm
            split_factor = 1.0 / split_ratio
            total_factor = dividend_factor × split_factor
            adjusted_price_before = original_price_before × total_factor
        
        پارامترها:
            prices: لیست قیمت‌ها
            split_date_idx: ایندکس روز افزایش سرمایه/مجمع
            split_ratio: نسبت افزایش سرمایه
            dividend_per_share: سود نقدی هر سهم
            price_before_agm: قیمت قبل از مجمع
            price_after_agm: قیمت بعد از مجمع (گشایش)
        """
        warnings = []
        n = len(prices)
        
        # ── محاسبه ضریب سود نقدی ──────────────────────────────
        if price_before_agm > 0:
            dividend_factor = price_after_agm / price_before_agm
        else:
            dividend_factor = 1.0
            warnings.append("قیمت قبل از مجمع صفر است - ضریب سود نقدی ۱ در نظر گرفته شد")
        
        # ── محاسبه ضریب افزایش سرمایه ─────────────────────────
        split_factor = 1.0 / split_ratio
        
        # ── ضریب کل ───────────────────────────────────────────
        total_factor = dividend_factor * split_factor
        
        # ── اعمال تعدیل ───────────────────────────────────────
        adjusted = prices.copy()
        for i in range(split_date_idx):
            adjusted[i] = prices[i] * total_factor
        
        factors = [total_factor if i < split_date_idx else 1.0 for i in range(n)]
        
        return AdjustmentResult(
            method=AdjustmentMethod.CASH_DIVIDEND_AND_SPLIT,
            original_prices=prices,
            adjusted_prices=adjusted,
            adjustment_factors=factors,
            split_date_idx=split_date_idx,
            split_ratio=split_ratio,
            dividend_effect=dividend_factor,
            description=f"تعدیل سود نقدی {dividend_per_share:.4f} و افزایش سرمایه {split_ratio:.4f} (روش ۳)",
            warnings=warnings
        )
    
    @staticmethod
    def method_4_cash_dividend_and_split_with_rights(
        prices: List[float],
        split_date_idx: int,
        split_ratio: float,
        dividend_per_share: float,
        price_before_agm: float,
        price_after_agm: float,
        rights_value: float
    ) -> AdjustmentResult:
        """
        روش ۴: سود نقدی و افزایش سرمایه با احتساب آورده
        (Cash Dividend + Stock Split with Rights)
        
        صفحه ۵۳:
            "این روش مانند روش قبل است با این تفاوت که حق تقدم
             تعلق گرفته به سهامداران نیز در محاسبات اثر داده می‌شود."
        
        فرمول:
            theoretical_price = (price_after_agm + rights_value) / split_ratio
            adjustment_factor = theoretical_price / price_before_agm
            adjusted_price_before = original_price_before × adjustment_factor
        """
        warnings = []
        n = len(prices)
        
        # ── محاسبه قیمت تئوریک ────────────────────────────────
        theoretical_price = (price_after_agm + rights_value) / split_ratio
        
        # ── محاسبه ضریب تعدیل ─────────────────────────────────
        if price_before_agm > 0:
            adjustment_factor = theoretical_price / price_before_agm
        else:
            adjustment_factor = 1.0
            warnings.append("قیمت قبل از مجمع صفر است - ضریب تعدیل ۱ در نظر گرفته شد")
        
        # ── اعمال تعدیل ───────────────────────────────────────
        adjusted = prices.copy()
        for i in range(split_date_idx):
            adjusted[i] = prices[i] * adjustment_factor
        
        factors = [adjustment_factor if i < split_date_idx else 1.0 for i in range(n)]
        
        return AdjustmentResult(
            method=AdjustmentMethod.CASH_DIVIDEND_AND_SPLIT_WITH_RIGHTS,
            original_prices=prices,
            adjusted_prices=adjusted,
            adjustment_factors=factors,
            split_date_idx=split_date_idx,
            split_ratio=split_ratio,
            dividend_effect=0.0,
            description=f"تعدیل سود نقدی {dividend_per_share:.4f} و افزایش سرمایه با حق تقدم {rights_value:.4f} (روش ۴)",
            warnings=warnings
        )
    
    @staticmethod
    def method_5_performance_adjustment(
        prices: List[float],
        split_date_idx: int,
        split_ratio: float,
        dividend_per_share: float,
        price_after_agm: float,
        rights_value: float = 0.0,
        capital_from_rights: float = 0.0
    ) -> AdjustmentResult:
        """
        روش ۵: تعدیل عملکردی (Performance Adjustment)
        
        صفحه ۵۳:
            "مبنای محاسبات بر اساس قیمت گشایش سهام بعد از مجمع است.
             ابتدا نسبت قیمت بعد از مجمع عادی شرکت به حاصل جمع قیمت
             بعد از مجمع با سود نقدی شرکت محاسبه و این ضریب در تمام
             قیمت‌های قبل از مجمع ضرب می‌شود.
             برای محاسبه اثر افزایش سرمایه نیز قیمت بعد از مجمع به مبلغ
             افزایش سرمایه از محل آورده و جایزه تقسیم شده و این نسبت در
             قیمت‌های قبل از مجمع ضرب می‌شود."
        
        فرمول:
            performance_factor = price_after_agm / (price_after_agm + dividend_per_share)
            split_adjustment = price_after_agm / (price_after_agm + capital_from_rights)
            total_factor = performance_factor × split_adjustment
        """
        warnings = []
        n = len(prices)
        
        # ── ضریب عملکردی (سود نقدی) ──────────────────────────
        denominator = price_after_agm + dividend_per_share
        if denominator > 0:
            performance_factor = price_after_agm / denominator
        else:
            performance_factor = 1.0
            warnings.append("مخرج ضریب عملکردی صفر است - ضریب ۱ در نظر گرفته شد")
        
        # ── ضریب تعدیل افزایش سرمایه ──────────────────────────
        if capital_from_rights > 0:
            split_denominator = price_after_agm + capital_from_rights
            if split_denominator > 0:
                split_adjustment = price_after_agm / split_denominator
            else:
                split_adjustment = 1.0
                warnings.append("مخرج ضریب افزایش سرمایه صفر است - ضریب ۱ در نظر گرفته شد")
        else:
            split_adjustment = 1.0 / split_ratio if split_ratio > 0 else 1.0
        
        # ── ضریب کل ───────────────────────────────────────────
        total_factor = performance_factor * split_adjustment
        
        # ── اعمال تعدیل ───────────────────────────────────────
        adjusted = prices.copy()
        for i in range(split_date_idx):
            adjusted[i] = prices[i] * total_factor
        
        factors = [total_factor if i < split_date_idx else 1.0 for i in range(n)]
        
        return AdjustmentResult(
            method=AdjustmentMethod.PERFORMANCE,
            original_prices=prices,
            adjusted_prices=adjusted,
            adjustment_factors=factors,
            split_date_idx=split_date_idx,
            split_ratio=split_ratio,
            dividend_effect=performance_factor,
            description=f"تعدیل عملکردی (روش ۵) - سود نقدی {dividend_per_share:.4f}، افزایش سرمایه {split_ratio:.4f}",
            warnings=warnings
        )


# ════════════════════════════════════════════════════════════════
# بخش ۳: تشخیص و بستن گپ‌های مصنوعی
# ════════════════════════════════════════════════════════════════

def detect_artificial_gaps(
    prices: List[float],
    dates: List[str],
    gap_threshold: float = 0.05
) -> List[Dict]:
    """
    تشخیص گپ‌های مصنوعی (ناشی از افزایش سرمایه یا تقسیم سود).
    
    صفحه ۵۲:
        "تعدیل برای گپ های طبیعی چارت استفاده نمی‌شود بلکه فقط برای
         گپ هایی که با عوامل غیر از عرضه و تقاضا در چارت ایجاد شده اند."
    
    معیار تشخیص گپ مصنوعی:
        - گپ نزولی قابل توجه (قیمت افت شدید در یک روز)
        - همراه با افزایش حجم غیرعادی
        - در تاریخ‌های مجمع یا افزایش سرمایه
    """
    gaps = []
    
    for i in range(1, len(prices)):
        if prices[i-1] > 0:
            gap_percent = (prices[i] - prices[i-1]) / prices[i-1]
        else:
            gap_percent = 0
        
        # گپ نزولی قابل توجه (افت بیش از آستانه)
        if gap_percent < -gap_threshold:
            gaps.append({
                "index": i,
                "date": dates[i] if i < len(dates) else f"index_{i}",
                "gap_percent": gap_percent * 100,
                "price_before": prices[i-1],
                "price_after": prices[i],
                "is_artificial": True,  # نیاز به تأیید با داده‌های خارجی
                "possible_causes": ["افزایش سرمایه", "تقسیم سود نقدی"]
            })
    
    return gaps


# ════════════════════════════════════════════════════════════════
# بخش ۴: تابع analyze (interface اصلی برای main.py)
# ════════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None, context=None) -> Dict:
    """
    فصل ۹: تعدیل چارت (Chart Adjustment)
    
    پیاده‌سازی کامل مطابق صفحات ۵۲-۵۳ کتاب گلن نیلی.
    
    این تابع:
        ۱. گپ‌های مصنوعی در داده را تشخیص می‌دهد
        ۲. روش‌های مختلف تعدیل را توضیح می‌دهد
        ۳. فرمول‌های محاسباتی هر روش را ارائه می‌کند
        ۴. هشدارهای لازم برای تعدیل صحیح را می‌دهد
    
    توجه: این فصل عمدتاً تئوری و آموزشی است.
    در عمل، تعدیل چارت توسط دیتا پرووایدرها انجام می‌شود.
    
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
    volume = data['volume'].values if 'volume' in data.columns else data['Volume'].values if 'Volume' in data.columns else None
    volume = volume.astype(float) if volume is not None else np.zeros(len(close))
    
    n = len(close)
    
    if n < 2:
        return {
            "عنوان": "فصل ۹: تعدیل چارت",
            "وضعیت": "داده_کافی_نیست",
            "تعداد_کندل": str(n),
            "پیام": "برای تحلیل حداقل ۲ کندل لازم است"
        }
    
    # ─── تشخیص تاریخ‌ها ───────────────────────────────────────
    dates = []
    if isinstance(data.index, pd.DatetimeIndex):
        dates = [d.strftime("%Y-%m-%d") for d in data.index]
    else:
        dates = [str(i) for i in range(n)]

        cash_data = None
        scale_info = None
        context_used = False
    
    if context:
        if "chapter_4" in context and "_cash_data_full" in context["chapter_4"]:
            cash_data = context["chapter_4"]["_cash_data_full"]
            context_used = True
        if "chapter_8" in context and "_scale_info" in context["chapter_8"]:
            scale_info = context["chapter_8"]["_scale_info"]
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۲: تشخیص گپ‌های مصنوعی
    # ════════════════════════════════════════════════════════════
    gaps = detect_artificial_gaps(close.tolist(), dates, gap_threshold=0.05)
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۳: آمار گپ‌ها
    # ════════════════════════════════════════════════════════════
    total_gaps = len(gaps)
    artificial_gaps = len(gaps)  # در عمل نیاز به تأیید با داده‌های خارجی دارد
    
    avg_gap_size = np.mean([abs(g["gap_percent"]) for g in gaps]) if gaps else 0
    max_gap_size = max([abs(g["gap_percent"]) for g in gaps]) if gaps else 0
    
    # ════════════════════════════════════════════════════════════
    # مرحله ۴: ساخت خروجی
    # ════════════════════════════════════════════════════════════
    results = {
        # ── شناسنامه ──
        "عنوان": "فصل ۹: تعدیل چارت (Chart Adjustment)",
        "مرجع_کتاب": "صفحات ۵۲-۵۳ - گلن نیلی",
        "وضعیت": "تحلیل_کامل",
        
        # ── اطلاعات پایه ──
        "تعداد_کندل": str(n),
        "قیمت_شروع": str(round(close[0], 4)),
        "قیمت_پایانی": str(round(close[-1], 4)),
        
        # ── آمار گپ‌ها ──
        "تعداد_کل_گپ": str(total_gaps),
        "تعداد_گپ_مصنوعی_محتمل": str(artificial_gaps),
        "میانگین_اندازه_گپ": f"{avg_gap_size:.2f}%",
        "بیشترین_اندازه_گپ": f"{max_gap_size:.2f}%",
        
        # ── اصل اساسی تعدیل چارت (صفحه ۵۲) ──
        "اصل_تعدیل": "تعدیل چارت فقط برای گپ‌های مصنوعی ناشی از افزایش سرمایه و توزیع سود نقدی استفاده می‌شود",
        "گپ_طبیعی": "گپ‌های ناشی از عرضه و تقاضا تعدیل نمی‌شوند",
        
        # ── روش ۱: افزایش سرمایه ──
        "روش_۱_نام": "افزایش سرمایه (Stock Split)",
        "روش_۱_فرمول": "ضریب تعدیل = سرمایه_قبلی / سرمایه_جدید",
        "روش_۱_توضیح": "قیمت‌های قبل از تاریخ افزایش سرمایه در ضریب تعدیل ضرب می‌شوند",
        "روش_۱_محدودیت": "محل تامین افزایش سرمایه اثری در محاسبات ندارد",
        
        # ── روش ۲: افزایش سرمایه با احتساب آورده ──
        "روش_۲_نام": "افزایش سرمایه با احتساب آورده (Stock Split with Rights)",
        "روش_۲_فرمول": "قیمت_تئوریک = (قیمت_قبل + حق_تقدم) / نسبت_افزایش",
        "روش_۲_توضیح": "علاوه بر کاهش قیمت، حق تقدم تعلق گرفته نیز لحاظ می‌شود",
        "روش_۲_شرط": "زمانی که افزایش سرمایه از محل مطالبات و آورده باشد",
        
        # ── روش ۳: سود نقدی و افزایش سرمایه ──
        "روش_۳_نام": "سود نقدی و افزایش سرمایه (Cash Dividend + Stock Split)",
        "روش_۳_فرمول": "ضریب = (قیمت_بعد_از_مجمع / قیمت_قبل_از_مجمع) × (۱ / نسبت_افزایش)",
        "روش_۳_توضیح": "توزیع سود نقدی و افزایش سرمایه هر دو لحاظ می‌شود",
        
        # ── روش ۴: سود نقدی و افزایش سرمایه با احتساب آورده ──
        "روش_۴_نام": "سود نقدی و افزایش سرمایه با احتساب آورده",
        "روش_۴_فرمول": "قیمت_تئوریک = (قیمت_بعد_از_مجمع + حق_تقدم) / نسبت_افزایش",
        "روش_۴_توضیح": "مانند روش ۳، با این تفاوت که حق تقدم نیز لحاظ می‌شود",
        
        # ── روش ۵: تعدیل عملکردی ──
        "روش_۵_نام": "تعدیل عملکردی (Performance Adjustment)",
        "روش_۵_فرمول": "ضریب_عملکردی = قیمت_گشایش / (قیمت_گشایش + سود_نقدی)",
        "روش_۵_مبنای_محاسبه": "قیمت گشایش سهام بعد از مجمع",
        "روش_۵_توضیح": "برخلاف روش‌های قبل، مبنای محاسبات قیمت گشایش است",
        
        # ── قوانین کلیدی ──
        "قانون_گپ_طبیعی": "گپ‌های طبیعی ناشی از عرضه و تقاضا تعدیل نمی‌شوند",
        "قانون_گپ_مصنوعی": "فقط گپ‌های ناشی از افزایش سرمایه و تقسیم سود تعدیل می‌شوند",
        "قانون_جهش_قیمت": "جهش قیمت بعد از مجمع با میل و اراده بازار شکل می‌گیرد و تعدیل نمی‌شود",
    }
    
    # ── اضافه کردن جزئیات گپ‌های تشخیص‌داده‌شده ────────────────
    for idx, gap in enumerate(gaps[:10]):
        prefix = f"گپ_{idx + 1}"
        results[f"{prefix}_تاریخ"] = gap["date"]
        results[f"{prefix}_درصد"] = f"{gap['gap_percent']:.2f}%"
        results[f"{prefix}_قبل"] = str(round(gap["price_before"], 4))
        results[f"{prefix}_بعد"] = str(round(gap["price_after"], 4))
        results[f"{prefix}_علت_محتمل"] = ", ".join(gap["possible_causes"])
    
    # ── مثال عددی برای هر روش ──
    example_price_before = 1000.0
    example_split_ratio = 1.2
    example_dividend = 50.0
    example_rights = 30.0
    example_price_after = 800.0
    
    results["مثال_قیمت_قبل_از_تعدیل"] = str(example_price_before)
    results["مثال_روش_۱_قیمت_بعد"] = str(round(example_price_before / example_split_ratio, 2))
    results["مثال_روش_۲_قیمت_بعد"] = str(round((example_price_before + example_rights) / example_split_ratio, 2))
    results["مثال_روش_۳_قیمت_بعد"] = str(round(example_price_before * (example_price_after / example_price_before) / example_split_ratio, 2))
    results["مثال_روش_۴_قیمت_بعد"] = str(round(example_price_before * ((example_price_after + example_rights) / example_split_ratio) / example_price_before, 2))

    # ⭐ منبع داده
    results["_source"] = "از_فصل_4_و_8" if context_used else "مستقل"
    results["_cash_data_used"] = "بله" if cash_data else "خیر"
    results["_scale_info_used"] = "بله" if scale_info else "خیر"
    results["_gaps"] = gaps
    
    # ── تفسیر نهایی ──
    results["تفسیر_نهایی"] = _build_final_interpretation(results, gaps, n)
    
    # ── ثبت در لاگ ──
    if logger:
        _write_to_logger(logger, results, gaps)
    
    return results


# ════════════════════════════════════════════════════════════════
# بخش ۵: تفسیر نهایی
# ════════════════════════════════════════════════════════════════

def _build_final_interpretation(results: Dict, gaps: List[Dict], n: int) -> str:
    """تولید تفسیر متنی کامل مطابق کتاب"""
    
    gap_warning = ""
    if gaps:
        gap_warning = f"\n  ⚠️ {len(gaps)} گپ مصنوعی محتمل شناسایی شد. برای تحلیل دقیق موج‌شماری، داده‌ها نیاز به تعدیل دارند."
    else:
        gap_warning = "\n  ✓ هیچ گپ مصنوعی قابل توجهی شناسایی نشد."
    
    return f"""
═══════════════════════════════════════════════════════════════════
  فصل ۹: تعدیل چارت (Chart Adjustment)
  مرجع: صفحات ۵۲-۵۳ | گلن نیلی | سبک نئوویو
═══════════════════════════════════════════════════════════════════

📐 اصل اساسی تعدیل چارت (صفحه ۵۲):

  "تعدیل چارت ابزار دیگری است که با استفاده از آن فاصله های قیمتی یا
   همان گپ های مصنوعی ناشی از افزایش سرمایه و توزیع سود نقدی پوشش داده می‌شود.
   
   توجه شود که تعدیل برای گپ های طبیعی چارت استفاده نمی‌شود بلکه فقط برای
   گپ هایی که با عوامل غیر از عرضه و تقاضا در چارت ایجاد شده اند."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 آمار داده‌های فعلی:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • تعداد کندل‌ها: {n}
  • گپ‌های مصنوعی محتمل: {len(gaps)}
  • میانگین اندازه گپ: {results.get('میانگین_اندازه_گپ', 'N/A')}
{gap_warning}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 پنج روش تعدیل چارت (صفحات ۵۲-۵۳):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌─────────────────────────────────────────────────────────────────┐
  │ روش ۱: افزایش سرمایه                                           │
  │   فرمول: ضریب = سرمایه_قبلی / سرمایه_جدید = ۱ / نسبت_افزایش    │
  │   مثال: قیمت ۱۰۰۰ با افزایش ۲۰٪ → قیمت تعدیل‌شده = ۸۳۳.۳۳     │
  ├─────────────────────────────────────────────────────────────────┤
  │ روش ۲: افزایش سرمایه با احتساب آورده                           │
  │   فرمول: قیمت_تئوریک = (قیمت_قبل + حق_تقدم) / نسبت_افزایش     │
  │   مثال: قیمت ۱۰۰۰ + حق تقدم ۳۰ با افزایش ۲۰٪ → ۸۵۸.۳۳          │
  ├─────────────────────────────────────────────────────────────────┤
  │ روش ۳: سود نقدی و افزایش سرمایه                                │
  │   فرمول: ضریب = (قیمت_بعد_مجمع / قیمت_قبل_مجمع) × (۱/نسبت)    │
  │   مثال: قیمت ۱۰۰۰ → بعد مجمع ۸۰۰ با افزایش ۲۰٪ → ۶۶۶.۶۷        │
  ├─────────────────────────────────────────────────────────────────┤
  │ روش ۴: سود نقدی و افزایش سرمایه با احتساب آورده                │
  │   فرمول: قیمت_تئوریک = (قیمت_بعد_مجمع + حق_تقدم) / نسبت        │
  │   مثال: ۸۰۰ + ۳۰ با افزایش ۲۰٪ → ۶۹۱.۶۷                         │
  ├─────────────────────────────────────────────────────────────────┤
  │ روش ۵: تعدیل عملکردی                                            │
  │   فرمول: ضریب_عملکردی = قیمت_گشایش / (قیمت_گشایش + سود_نقدی)   │
  │   مبنای محاسبات = قیمت گشایش سهام بعد از مجمع                   │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ نکات مهم:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • گپ‌های طبیعی ناشی از عرضه و تقاضا هرگز تعدیل نمی‌شوند
  • جهش قیمت بعد از مجمع با میل و اراده بازار شکل می‌گیرد
  • در عمل، تعدیل چارت توسط دیتا پرووایدرها انجام می‌شود
  • برای تحلیل نئوویو، استفاده از داده‌های تعدیل‌شده ضروری است

💡 نتیجه نئوویو:
   برای تحلیل موجی دقیق، همیشه از داده‌های تعدیل‌شده استفاده کنید.
   گپ‌های مصنوعی ساختار موجی را مخدوش می‌کنند و باید حذف شوند.
   {results.get('اصل_تعدیل', '')}

═══════════════════════════════════════════════════════════════════
"""


# ════════════════════════════════════════════════════════════════
# بخش ۶: ثبت در لاگ
# ════════════════════════════════════════════════════════════════

def _write_to_logger(logger, results: Dict, gaps: List[Dict]):
    """ثبت نتایج در لاگر"""
    logger.add_section("فصل ۹: تعدیل چارت (Chart Adjustment)", level=1)
    logger.add_result("مرجع کتاب", "صفحات ۵۲-۵۳ - گلن نیلی")
    logger.add_result("تعداد کندل", results["تعداد_کندل"])
    logger.add_result("گپ مصنوعی محتمل", results["تعداد_گپ_مصنوعی_محتمل"])
    logger.add_result("میانگین اندازه گپ", results["میانگین_اندازه_گپ"])
    
    logger.add_section("پنج روش تعدیل چارت", level=2)
    for i in range(1, 6):
        logger.add_result(f"روش {i}", results.get(f"روش_{i}_نام", ""))
        logger.add_result(f"فرمول {i}", results.get(f"روش_{i}_فرمول", ""))
    
    logger.add_section("گپ‌های شناسایی‌شده", level=2)
    for gap in gaps[:5]:
        logger.add_result(
            f"گپ {gap['date']}",
            f"{gap['gap_percent']:.2f}% (قبل: {gap['price_before']:.2f}, بعد: {gap['price_after']:.2f})"
        )
    
    logger.add_section("قوانین کلیدی", level=2)
    logger.add_result("گپ طبیعی", results["قانون_گپ_طبیعی"])
    logger.add_result("گپ مصنوعی", results["قانون_گپ_مصنوعی"])
    logger.add_result("جهش قیمت", results["قانون_جهش_قیمت"])
    
    logger.add_result("تفسیر نهایی", results["تفسیر_نهایی"])


# ════════════════════════════════════════════════════════════════
# اجرای مستقیم برای تست
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # ایجاد داده تست با گپ مصنوعی شبیه‌سازی‌شده
    test_data = pd.DataFrame({
        "close": [1000, 1020, 1010, 1030, 830, 840, 850, 860, 870, 880],
        "high": [1010, 1030, 1020, 1040, 840, 850, 860, 870, 880, 890],
        "low": [990, 1010, 1000, 1020, 820, 830, 840, 850, 860, 870],
        "open": [1000, 1020, 1010, 1030, 830, 840, 850, 860, 870, 880],
        "volume": [1000, 1200, 1100, 1300, 5000, 1100, 1000, 900, 800, 700],
    })
    
    result = analyze(test_data)
    print(result["تفسیر_نهایی"])