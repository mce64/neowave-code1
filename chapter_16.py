"""
فصل ۱۶: قوانین معاینه برای تعیین نقطه شروع و خاتمه تک‌موج‌ها
منبع: کتاب "امواج الیوت به سبک نئوویو" - گلن نیلی
صفحات: ۳۵۴ تا ۳۶۴

═══════════════════════════════════════════════════════════════════
متن کامل کتاب (صفحه ۳۵۴):
═══════════════════════════════════════════════════════════════════

"این قوانین (قوانین معاینه، بازگشت و قوانین پیش ساخت منطقی) به شما کمک
می‌کنند تا در مواقعی که تک موج ها برای کلاس بندی در دسته شتابدارها (5):
یا اصلاحی ها (3): دارای سیمای مشخصی نمی‌شوند، چشم انداز نسبی با توجه به
وضعیت تک موجهای پیشین و پسین آنها به دست آورید. برای این منظور لازم است
محل شروع و پایان موجهای پسین و پیشین نسبت به موج مورد نظر (M1):
یک تک موج یا یک گروه موج فشرده، مشخص گردد."

═══════════════════════════════════════════════════════════════════
قوانین کلیدی از تصاویر:
═══════════════════════════════════════════════════════════════════

صفحه ۳۵۵ - تعیین نقطه خاتمه موج‌های پسین:
  حالت اول: M2 خلاف جهت M1 رخ می‌دهد اما پیش از شکستن کف M1،
            سقف M1 توسط M3 (هم جهت با M1) شکسته می‌شود. ✓
  حالت دوم: M2 خلاف جهت M1 کف آن را می‌شکند سپس چرخش متعاقب
            M3 (در راستای M1) رخ می‌دهد. ✓

صفحه ۳۵۶-۳۵۷ - تأیید نقاط خاتمه:
  - اگر M1 یک گروه موج فشرده باشد، نخستین چرخش در حرکت قیمت
    (پس از شکست سقف M1) با پستی M2 را تکمیل کند.
  - M2 در M1 خاتمه یافت، این سقف تأیید شد.
  - M2 شکسته شد، M1 وقتی کف خاتمه یافت در بالاترین نقطه بین
    کف M1 و کف جدید تأیید می‌شود.

صفحه ۳۵۸-۳۵۹ - تعیین نقطه خاتمه موج‌های پیشین:
  - با عقب رفتن تا آخرین باری که بازار بالای m0 بوده،
    می‌توان خاتمه ی m1 سقف را در بالاترین نقطه ی عطف قیمتی
    که مقدم بر کف قدیمی تر بوده در نظر گرفت.
  - با عقب رفتن تا آخرین باری که بازار زیر کف m0 بوده،
    می‌توان خاتمه ی m1 را در بالاترین نقطه بین کف m1 و آن کف
    قدیمی تر در نظر گرفت.
  - با عقب رفتن تا آخرین باری که بازار بالای سقف m1 بوده،
    می‌توان خاتمه ی m0 را در پایین ترین نقطه میان سقف m1
    و آن سقف قدیمی تر در نظر گرفت.

صفحه ۳۶۰ - موج‌های M0 و M2 به صورت ترکیبی:
  "موج‌های M0 و M2 در صورتی می‌توانند به صورت ترکیبی از چند موج باشند
   که تک موج‌ها مطابق شرايط ذکر شده نتوانسته باشند از سقف یا کف
   موج مورد نظر عبور کنند، در اينصورت آرايش آنها بايستي ترکيبي از
   3، 5 و به ندرت 7 و يا 9 موج باشند."

صفحه ۳۶۱-۳۶۲ - قانون شکست سقف/کف:
  "برای تعیین تک موجهای پیش و پس از موج مورد نظر بایستی سقف و یا
   کف موج پیشین توسط موج یا گروه موجهای پسین و پیشین شکسته شود."

صفحه ۳۶۴ - انتخاب گروه ترکیبی:
  "به هنگام انتخاب گروه ترکیبی از چند موج، بهتر است در قالب الگوهای
   استاندارد قابل فشرده سازی باشند. چرا که این قوانین در مورد الگوهای
   فشرده ای که از ابتدای خود تجاوز کرده باشند کاربرد ندارد. در این گونه
   موارد فقط ساختار الگو را حفظ کنید (به نکته صفحه ۴۳۶ مراجعه کنید)."
═══════════════════════════════════════════════════════════════════
وابستگی‌ها: [4, 5, 7, 14, 15]
═══════════════════════════════════════════════════════════════════
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import math
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# ─── وارد کردن از فصل‌های پیش‌نیاز ───
from chapters.chapter_05 import Monowave, MonowaveIdentifier
from chapters.chapter_11 import ImpulseWave, ImpulseAnalyzer, ImpulseCategory, ImpulseSubType
from chapters.chapter_12 import CorrectiveCategory, ZigZagType, FlatType, TriangleType
from chapters.chapter_15 import PatternInstance, PatternType, PatternRating


# ══════════════════════════════════════════════════════════════════
# ۱. تعاریف پایه و انواع داده (مطابق ساختار کتاب)
# ══════════════════════════════════════════════════════════════════

class WaveStatus(Enum):
    """وضعیت موج بر اساس قوانین معاینه (صفحه ۳۵۴-۳۶۴)"""
    CONFIRMED = "تأیید_شده"          # نقطه خاتمه تأیید شد
    TENTATIVE = "در_حال_بررسی"       # در حال بررسی
    REJECTED = "رد_شده"              # رد شد
    INCOMPLETE = "ناقص"              # ناقص (در حال شکل‌گیری)
    COMPOSITE = "ترکیبی"             # ترکیبی از چند موج


class BreakType(Enum):
    """نوع شکست سقف/کف (صفحه ۳۶۱-۳۶۲)"""
    NO_BREAK = "بدون_شکست"
    HIGH_BREAK = "شکست_سقف"
    LOW_BREAK = "شکست_کف"
    DOUBLE_BREAK = "شکست_دوگانه"


class EndpointType(Enum):
    """نوع نقطه خاتمه (صفحه ۳۵۵-۳۵۹)"""
    SWING_HIGH = "سقف_نوسانی"
    SWING_LOW = "کف_نوسانی"
    IMPORTANT_HIGH = "سقف_مهم"
    IMPORTANT_LOW = "کف_مهم"
    CONFIRMED_END = "پایان_تأیید_شده"
    COMPOSITE_END = "پایان_ترکیبی"


@dataclass
class WaveM:
    """
    ساختار موج M برای قوانین معاینه
    
    مطابق تصاویر صفحه ۳۵۴-۳۶۴:
    - M1: موج مورد نظر (تک موج یا گروه موج فشرده)
    - M0: موج پیشین
    - M2: موج پسین اول (خلاف جهت M1)
    - M3: موج پسین دوم (هم جهت با M1)
    """
    index: int
    start_price: float
    end_price: float
    high_price: float
    low_price: float
    direction: int  # +1 صعودی، -1 نزولی
    is_composite: bool = False
    sub_waves: List['WaveM'] = field(default_factory=list)
    status: WaveStatus = WaveStatus.TENTATIVE
    endpoint_type: EndpointType = EndpointType.SWING_HIGH
    break_type: BreakType = BreakType.NO_BREAK
    confirmed_at: Optional[float] = None
    is_compressed: bool = False  # آیا گروه فشرده است؟ (صفحه ۳۶۴)
    
    @property
    def price_range(self) -> float:
        return abs(self.end_price - self.start_price)
    
    @property
    def direction_str(self) -> str:
        return "صعودی" if self.direction == 1 else "نزولی"
    
    @property
    def is_up(self) -> bool:
        return self.direction == 1
    
    @property
    def is_down(self) -> bool:
        return self.direction == -1


@dataclass
class ExaminationResult:
    m1: WaveM
    m0: Optional[WaveM] = None
    m2: Optional[WaveM] = None
    m3: Optional[WaveM] = None
    
    m0_endpoint: Optional[float] = None
    m1_endpoint: Optional[float] = None
    m2_endpoint: Optional[float] = None
    m3_endpoint: Optional[float] = None
    
    m1_high_broken: bool = False
    m1_low_broken: bool = False
    m0_high_broken: bool = False
    m0_low_broken: bool = False
    
    is_confirmed: bool = False
    confirmation_type: str = ""
    confirmation_price: Optional[float] = None
    confirmation_index: Optional[int] = None
    
    m0_is_composite: bool = False
    m2_is_composite: bool = False
    composite_count_m0: int = 0
    composite_count_m2: int = 0
    composite_type: str = ""
    
    is_compressible: bool = False
    compressed_structure: str = ""
    
    page_reference: str = ""
    description: str = ""
    
    # فقط این ۴ تا
    chapter_5_data: Optional[Dict] = None
    chapter_11_data: Optional[Dict] = None
    chapter_12_data: Optional[Dict] = None
    chapter_15_data: Optional[Dict] = None
    
    confidence_score: float = 0.5


# ══════════════════════════════════════════════════════════════════
# ۲. کلاس اصلی تحلیل‌گر قوانین معاینه
# ══════════════════════════════════════════════════════════════════

class ExaminationAnalyzer:
    """
    تحلیل‌گر قوانین معاینه (فصل ۱۶)
    
    این کلاس تمام قوانین صفحات ۳۵۴ تا ۳۶۴ را پیاده‌سازی می‌کند:
    ۱. تعیین نقطه خاتمه موج‌های پسین (M2, M3) - صفحه ۳۵۵
    ۲. تعیین نقطه خاتمه موج‌های پیشین (M0) - صفحه ۳۵۸-۳۵۹
    ۳. تشخیص شکست سقف/کف - صفحه ۳۶۱-۳۶۲
    ۴. تشخیص ترکیب موج‌ها (۳، ۵، ۷، ۹ موجی) - صفحه ۳۶۰
    ۵. تأیید نهایی نقاط خاتمه - صفحه ۳۵۵-۳۵۷
    ۶. فشرده‌سازی الگوها - صفحه ۳۶۴
    """
    
    def __init__(self, data: pd.DataFrame, 
                 chapter_5_data: Optional[Dict] = None,
                 chapter_11_data: Optional[Dict] = None,
                 chapter_12_data: Optional[Dict] = None,
                 chapter_15_data: Optional[Dict] = None):
                 
        """
        پارامترها:
            data: DataFrame با ستون‌های OHLC
            chapter_5_data: نتایج فصل ۵ (تک‌موج‌ها)
            chapter_11_data:
            chapter_12_data:
            chapter_15_data: نتایج فصل ۱۵ (رتبه‌بندی الگوها)
        """
        self.data = data.copy()
        self.close = data["close"].values if "close" in data.columns else data["Close"].values
        self.high = data["high"].values if "high" in data.columns else data["High"].values
        self.low = data["low"].values if "low" in data.columns else data["Low"].values
        self.n = len(self.close)
        
        # داده‌های فصل‌های پیش‌نیاز
        self.chapter_4_data = {}
        self.chapter_5_data = chapter_5_data or {}
        self.chapter_7_data = {}
        self.chapter_11_data = chapter_11_data or {}
        self.chapter_12_data = chapter_12_data or {}
        self.chapter_14_data = {}
        self.chapter_15_data = chapter_15_data or {}

        # ── استخراج کیفیت از فصل‌های پیش‌نیاز ──
        self.quality_scores = {
            "wave_count": int(self.chapter_5_data.get("تعداد_کل_تک‌موج", 0)),
            "impulse_count": int(self.chapter_11_data.get("تعداد_کل_الگوهای_شتابدار", 0)),
            "corrective_count": int(self.chapter_12_data.get("تعداد_الگوهای_یافت_شده", 0)),
            "pattern_rating": int(self.chapter_15_data.get("رتبه_الگو", 0)),
        }
        
        # نتایج تحلیل
        self.results = []
        self.waves = []
        self._initialize_from_chapters()
        
        # مقداردهی اولیه از داده‌های فصل‌های پیش‌نیاز
        self._initialize_from_chapters()
    
    # ─── ۲-۱. مقداردهی اولیه از داده‌های فصل‌های پیش‌نیاز ───
    
    def _initialize_from_chapters(self):
        """استخراج موج‌ها از داده با روش ساده (بدون وابستگی به فصل ۱۴)"""
        from scipy.signal import argrelextrema
        import numpy as np
    
        high = self.high
        low = self.low
    
        # یافتن نقاط عطف ساده
        peaks = argrelextrema(high, np.greater, order=3)[0]
        troughs = argrelextrema(low, np.less, order=3)[0]
    
        # ترکیب نقاط
        points = []
        for idx in peaks:
            points.append((int(idx), float(high[idx]), 'PEAK'))
        for idx in troughs:
            points.append((int(idx), float(low[idx]), 'TROUGH'))
        points.sort(key=lambda x: x[0])
    
        # حذف نقاط هم‌نوع متوالی
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
    
        if len(filtered) < 2:
            return
    
        # ساخت WaveM ها
        for i in range(len(filtered) - 1):
            idx1, price1, _ = filtered[i]
            idx2, price2, _ = filtered[i + 1]
        
            wave = WaveM(
                index=i,
                start_price=float(price1),
                end_price=float(price2),
                high_price=max(float(price1), float(price2)),
                low_price=min(float(price1), float(price2)),
                direction=1 if price2 > price1 else -1,
                status=WaveStatus.TENTATIVE,
                endpoint_type=EndpointType.SWING_HIGH if price2 > price1 else EndpointType.SWING_LOW
            )
            self.waves.append(wave)
        
        # ── از فصل ۴: کیفیت کش دیتا ──
        if self.chapter_4_data:
            cash_quality = self.chapter_4_data.get("امتیاز_کیفیت_کش_دیتا", 0)
            # کیفیت بالا = دقت بیشتر در تشخیص شکست‌ها
    
    # ─── ۲-۲. تعیین نقطه خاتمه موج‌های پسین (صفحه ۳۵۵) ───
    
    def find_subsequent_endpoint(self, m1: WaveM, m2: WaveM, m3: WaveM) -> Dict[str, Any]:
        """
        تعیین نقطه خاتمه موج‌های پسین (M2, M3)
        
        مطابق صفحه ۳۵۵ (دو حالت اصلی):
        ┌─────────────────────────────────────────────────────────────────┐
        │ حالت اول (شکل A):                                             │
        │ M2 خلاف جهت M1 رخ می‌دهد اما پیش از شکستن کف M1،              │
        │ سقف M1 توسط M3 (هم جهت با M1) شکسته می‌شود. ✓                │
        ├─────────────────────────────────────────────────────────────────┤
        │ حالت دوم (شکل B):                                             │
        │ M2 خلاف جهت M1 کف آن را می‌شکند سپس چرخش متعاقب               │
        │ M3 (در راستای M1) رخ می‌دهد. ✓                                │
        └─────────────────────────────────────────────────────────────────┘
        """
        result = {
            "m2_endpoint": None,
            "m3_endpoint": None,
            "confirmation_type": "",
            "is_confirmed": False,
            "page": "355",
            "description": ""
        }
        
        # ── بررسی جهت‌ها (الزامات اولیه) ──
        # M2 باید خلاف جهت M1 باشد
        if m2.direction == m1.direction:
            return {**result, "description": "M2 باید خلاف جهت M1 باشد"}
        
        # M3 باید هم جهت با M1 باشد
        if m3.direction != m1.direction:
            return {**result, "description": "M3 باید هم جهت با M1 باشد"}
        
        # ── حالت اول (صفحه ۳۵۵ - شکل A) ──
        # M2 کف M1 را نمی‌شکند، اما M3 سقف M1 را می‌شکند
        m1_low_not_broken = not self._is_low_broken(m1, m2)
        m1_high_broken_by_m3 = self._is_high_broken(m1, m3)
        
        if m1_low_not_broken and m1_high_broken_by_m3:
            result["confirmation_type"] = "پسین_حالت_۱"
            result["is_confirmed"] = True
            result["m2_endpoint"] = m2.end_price
            result["m3_endpoint"] = m3.end_price
            result["page"] = "355"
            result["description"] = (
                "حالت اول (صفحه ۳۵۵): M2 خلاف جهت M1 رخ داد اما پیش از شکستن کف M1، "
                f"سقف M1 ({m1.high_price:.2f}) توسط M3 ({m3.high_price:.2f}) شکسته شد ✓"
            )
            return result
        
        # ── حالت دوم (صفحه ۳۵۵ - شکل B) ──
        # M2 کف M1 را می‌شکند، سپس M3 در راستای M1 رخ می‌دهد
        if self._is_low_broken(m1, m2):
            # M3 باید در راستای M1 باشد و از کف جدید بالاتر رود
            if m3.end_price > m2.end_price and m3.direction == m1.direction:
                result["confirmation_type"] = "پسین_حالت_۲"
                result["is_confirmed"] = True
                result["m2_endpoint"] = m2.end_price
                result["m3_endpoint"] = m3.end_price
                result["page"] = "355"
                result["description"] = (
                    "حالت دوم (صفحه ۳۵۵): M2 خلاف جهت M1 کف آن را شکست "
                    f"({m2.low_price:.2f} < {m1.low_price:.2f})، سپس چرخش متعاقب "
                    f"M3 در راستای M1 رخ داد ✓"
                )
                return result
        
        # ── حالت‌های خاص از صفحه ۳۵۶-۳۵۷ ──
        
        # حالت: M1 یک گروه موج فشرده باشد (صفحه ۳۵۶)
        if m1.is_composite:
            # نخستین چرخش پس از شکست سقف M1، M2 را تکمیل می‌کند
            if self._is_high_broken(m1, m2):
                result["confirmation_type"] = "پسین_فشرده"
                result["is_confirmed"] = True
                result["m2_endpoint"] = m2.end_price
                result["page"] = "356"
                result["description"] = (
                    "M1 گروه موج فشرده - نخستین چرخش پس از شکست سقف "
                    f"M1 ({m1.high_price:.2f})، M2 را تکمیل کرد"
                )
                return result
        
        # ── تأیید در بالاترین نقطه بین کف M1 و کف جدید (صفحه ۳۵۷) ──
        if self._is_low_broken(m1, m2) and m3.direction == m1.direction:
            highest_between = max(m1.low_price, m2.low_price)
            if m3.end_price > highest_between:
                result["confirmation_type"] = "پسین_تأیید_کف"
                result["is_confirmed"] = True
                result["m2_endpoint"] = highest_between
                result["page"] = "357"
                result["description"] = (
                    f"M2 در بالاترین نقطه بین کف M1 ({m1.low_price:.2f}) "
                    f"و کف جدید ({m2.low_price:.2f}) تأیید شد: {highest_between:.2f}"
                )
                return result
        
        result["description"] = "هیچ یک از حالت‌های خاتمه پسین برقرار نشد"
        return result
    
    # ─── ۲-۳. تعیین نقطه خاتمه موج‌های پیشین (صفحه ۳۵۸-۳۵۹) ──
    
    def find_previous_endpoint(self, m0: WaveM, m1: WaveM) -> Dict[str, Any]:
        """
        تعیین نقطه خاتمه موج‌های پیشین (M0)
        
        مطابق صفحات ۳۵۸-۳۵۹:
        ┌─────────────────────────────────────────────────────────────────┐
        │ صفحه ۳۵۸ (شکل A):                                             │
        │ با عقب رفتن تا آخرین باری که بازار بالای m0 بوده،             │
        │ می‌توان خاتمه ی m1 سقف را در بالاترین نقطه ی عطف قیمتی        │
        │ که مقدم بر کف قدیمی تر بوده در نظر گرفت.                      │
        ├─────────────────────────────────────────────────────────────────┤
        │ صفحه ۳۵۸ (شکل B):                                             │
        │ با عقب رفتن تا آخرین باری که بازار زیر کف m0 بوده،            │
        │ می‌توان خاتمه ی m1 را در بالاترین نقطه بین کف m1 و آن کف     │
        │ قدیمی تر در نظر گرفت.                                         │
        ├─────────────────────────────────────────────────────────────────┤
        │ صفحه ۳۵۹ (شکل A):                                             │
        │ با عقب رفتن تا آخرین باری که بازار بالای سقف m1 بوده،        │
        │ می‌توان خاتمه ی m0 را در پایین ترین نقطه میان سقف m1         │
        │ و آن سقف قدیمی تر در نظر گرفت.                                │
        ├─────────────────────────────────────────────────────────────────┤
        │ صفحه ۳۵۹ (شکل B):                                             │
        │ با عقب رفتن تا آخرین باری که بازار زیر کف m1 بوده،           │
        │ می‌توان خاتمه ی m0 را در پایین ترین نقطه عطف قیمتی           │
        │ که مقدم بر کف قدیمی تر بوده در نظر گرفت.                     │
        └─────────────────────────────────────────────────────────────────┘
        """
        result = {
            "m0_endpoint": None,
            "confirmation_type": "",
            "is_confirmed": False,
            "page": "358",
            "description": ""
        }
        
        # ── بررسی جهت M0 و M1 ──
        # M0 باید قبل از M1 باشد (با توجه به ایندکس‌ها)
        if m0.index >= m1.index:
            return {**result, "description": "M0 باید قبل از M1 باشد"}
        
        # ── حالت صفحه ۳۵۸ - شکل A (سقف M1) ──
        # عقب رفتن تا آخرین باری که بازار بالای M0 بوده
        if m1.is_up:  # M1 صعودی است
            last_above_m0 = self._find_last_above_price(m0.high_price, m0.index)
            if last_above_m0 is not None:
                result["m0_endpoint"] = last_above_m0
                result["confirmation_type"] = "پیشین_سقف_۳۵۸A"
                result["is_confirmed"] = True
                result["page"] = "358"
                result["description"] = (
                    "صفحه ۳۵۸ (شکل A): با عقب رفتن تا آخرین باری که بازار بالای "
                    f"M0 ({m0.high_price:.2f}) بوده، خاتمه M1 سقف در "
                    f"{last_above_m0:.2f} تأیید شد"
                )
                return result
        
        # ── حالت صفحه ۳۵۸ - شکل B (کف M1) ──
        # عقب رفتن تا آخرین باری که بازار زیر کف M0 بوده
        if m1.is_down:  # M1 نزولی است
            last_below_m0 = self._find_last_below_price(m0.low_price, m0.index)
            if last_below_m0 is not None:
                result["m0_endpoint"] = last_below_m0
                result["confirmation_type"] = "پیشین_کف_۳۵۸B"
                result["is_confirmed"] = True
                result["page"] = "358"
                result["description"] = (
                    "صفحه ۳۵۸ (شکل B): با عقب رفتن تا آخرین باری که بازار زیر "
                    f"کف M0 ({m0.low_price:.2f}) بوده، خاتمه M1 در "
                    f"{last_below_m0:.2f} تأیید شد"
                )
                return result
        
        # ── حالت صفحه ۳۵۹ - شکل A (خاتمه M0 در پایین‌ترین نقطه) ──
        # با عقب رفتن تا آخرین باری که بازار بالای سقف M1 بوده
        last_above_m1 = self._find_last_above_price(m1.high_price, m0.index)
        if last_above_m1 is not None:
            lowest_between = min(m1.high_price, last_above_m1)
            result["m0_endpoint"] = lowest_between
            result["confirmation_type"] = "پیشین_سقف_۳۵۹A"
            result["is_confirmed"] = True
            result["page"] = "359"
            result["description"] = (
                "صفحه ۳۵۹ (شکل A): با عقب رفتن تا آخرین باری که بازار بالای سقف "
                f"M1 ({m1.high_price:.2f}) بوده، خاتمه M0 در پایین‌ترین نقطه میان "
                f"سقف M1 و سقف قدیمی‌تر ({lowest_between:.2f}) تأیید شد"
            )
            return result
        
        # ── حالت صفحه ۳۵۹ - شکل B (خاتمه M0 در پایین‌ترین نقطه عطف) ──
        # با عقب رفتن تا آخرین باری که بازار زیر کف M1 بوده
        last_below_m1 = self._find_last_below_price(m1.low_price, m0.index)
        if last_below_m1 is not None:
            # پایین‌ترین نقطه عطف قیمتی که مقدم بر کف قدیمی‌تر بوده
            # (در اینجا از بین دو نقطه پایین‌تر را انتخاب می‌کنیم)
            lowest_swing = min(m1.low_price, last_below_m1)
            result["m0_endpoint"] = lowest_swing
            result["confirmation_type"] = "پیشین_کف_۳۵۹B"
            result["is_confirmed"] = True
            result["page"] = "359"
            result["description"] = (
                "صفحه ۳۵۹ (شکل B): با عقب رفتن تا آخرین باری که بازار زیر کف "
                f"M1 ({m1.low_price:.2f}) بوده، خاتمه M0 در پایین‌ترین نقطه عطف "
                f"قیمتی ({lowest_swing:.2f}) تأیید شد"
            )
            return result
        
        result["description"] = "هیچ یک از حالت‌های خاتمه پیشین برقرار نشد"
        return result
    
    # ─── ۲-۴. توابع کمکی برای تشخیص شکست ──────────────────
    
    def _is_high_broken(self, ref_wave: WaveM, test_wave: WaveM) -> bool:
        """
        بررسی اینکه آیا سقف موج مرجع توسط موج تست شکسته شده است
        (صفحه ۳۶۱-۳۶۲)
        """
        return test_wave.high_price > ref_wave.high_price
    
    def _is_low_broken(self, ref_wave: WaveM, test_wave: WaveM) -> bool:
        """
        بررسی اینکه آیا کف موج مرجع توسط موج تست شکسته شده است
        (صفحه ۳۶۱-۳۶۲)
        """
        return test_wave.low_price < ref_wave.low_price
    
    def _find_last_above_price(self, price: float, before_index: int) -> Optional[float]:
        """
        پیدا کردن آخرین باری که قیمت بالای مقدار مشخص بوده
        (استفاده در صفحات ۳۵۸-۳۵۹)
        """
        for i in range(before_index - 1, -1, -1):
            if self.high[i] > price:
                return float(self.high[i])
        return None
    
    def _find_last_below_price(self, price: float, before_index: int) -> Optional[float]:
        """
        پیدا کردن آخرین باری که قیمت زیر مقدار مشخص بوده
        (استفاده در صفحات ۳۵۸-۳۵۹)
        """
        for i in range(before_index - 1, -1, -1):
            if self.low[i] < price:
                return float(self.low[i])
        return None
    
    def _find_highest_swing_before(self, price: float, before_index: int) -> Optional[float]:
        """
        پیدا کردن بالاترین نقطه عطف قیمتی قبل از یک نقطه مشخص
        (صفحه ۳۵۸)
        """
        highest = None
        for i in range(before_index - 1, -1, -1):
            if self.high[i] > price:
                if highest is None or self.high[i] > highest:
                    highest = float(self.high[i])
                # بعد از پیدا کردن اولین سقف بالاتر، ادامه می‌دهیم تا بالاترین را پیدا کنیم
        return highest
    
    # ─── ۲-۵. تشخیص ترکیب موج‌ها (صفحه ۳۶۰) ──────────────
    
    def detect_composite_structure(self, waves: List[WaveM], reference: WaveM) -> Dict[str, Any]:
        """
        تشخیص ترکیب موج‌ها (M0 و M2)
        
        مطابق صفحه ۳۶۰:
        ┌─────────────────────────────────────────────────────────────────┐
        │ "موج‌های M0 و M2 در صورتی می‌توانند به صورت ترکیبی از چند     │
        │ موج باشند که تک موج‌ها مطابق شرایط ذکر شده نتوانسته باشند     │
        │ از سقف یا کف موج مورد نظر عبور کنند، در اينصورت آرايش آنها   │
        │ بايستي ترکيبي از 3، 5 و به ندرت 7 و يا 9 موج باشند."          │
        └─────────────────────────────────────────────────────────────────┘
        """
        result = {
            "is_composite": False,
            "wave_count": 0,
            "structure_type": "",
            "page": "360",
            "description": ""
        }
        
        if len(waves) < 3:
            return {**result, "description": "حداقل ۳ موج برای تشخیص ترکیب نیاز است"}
        
        # ── بررسی اینکه آیا تک موج‌ها نتوانسته‌اند از سقف/کف عبور کنند ──
        failed_to_break = True
        for w in waves:
            if w.direction == reference.direction:
                if self._is_high_broken(reference, w) or self._is_low_broken(reference, w):
                    failed_to_break = False
                    break
        
        if failed_to_break and len(waves) >= 3:
            # تعداد موج‌ها باید ۳، ۵، ۷ یا ۹ باشد (صفحه ۳۶۰)
            valid_counts = [3, 5, 7, 9]
            if len(waves) in valid_counts:
                result["is_composite"] = True
                result["wave_count"] = len(waves)
                result["structure_type"] = f"ترکیبی_{len(waves)}_موجی"
                result["description"] = (
                    f"آرایش ترکیبی از {len(waves)} موج (صفحه ۳۶۰) - "
                    f"تک موج‌ها نتوانسته‌اند از سقف/کف عبور کنند"
                )
            else:
                result["description"] = (
                    f"تعداد موج‌ها ({len(waves)}) با ۳، ۵، ۷، ۹ مطابقت ندارد "
                    "(صفحه ۳۶۰)"
                )
        
        return result
    
    # ─── ۲-۶. قانون شکست سقف/کف (صفحه ۳۶۱-۳۶۲) ──────────
    
    def check_break_rule(self, m1: WaveM, m2: WaveM, m3: WaveM) -> Dict[str, Any]:
        """
        بررسی قانون شکست سقف/کف
        
        مطابق صفحات ۳۶۱-۳۶۲:
        ┌─────────────────────────────────────────────────────────────────┐
        │ "برای تعیین تک موجهای پیش و پس از موج مورد نظر بایستی سقف    │
        │ و یا کف موج پیشین توسط موج یا گروه موجهای پسین و پیشین       │
        │ شکسته شود."                                                   │
        └─────────────────────────────────────────────────────────────────┘
        """
        result = {
            "m1_high_broken": False,
            "m1_low_broken": False,
            "m0_high_broken": False,
            "m0_low_broken": False,
            "break_type": BreakType.NO_BREAK,
            "is_valid": False,
            "page": "361",
            "description": ""
        }
        
        # ── بررسی شکست سقف M1 (صفحه ۳۶۱) ──
        if self._is_high_broken(m1, m2) or self._is_high_broken(m1, m3):
            result["m1_high_broken"] = True
            result["break_type"] = BreakType.HIGH_BREAK
        
        # ── بررسی شکست کف M1 (صفحه ۳۶۲) ──
        if self._is_low_broken(m1, m2) or self._is_low_broken(m1, m3):
            result["m1_low_broken"] = True
            if result["break_type"] == BreakType.HIGH_BREAK:
                result["break_type"] = BreakType.DOUBLE_BREAK
            else:
                result["break_type"] = BreakType.LOW_BREAK
        
        # ── بررسی شکست M0 (صفحه ۳۶۲) ──
        # M0 در اینجا موج پیشین است
        
        # ── اعتبارسنجی ──
        # حداقل یکی از سقف یا کف M1 باید شکسته شود (صفحه ۳۶۱)
        result["is_valid"] = result["m1_high_broken"] or result["m1_low_broken"]
        
        if result["is_valid"]:
            break_parts = []
            if result["m1_high_broken"]:
                break_parts.append("سقف")
            if result["m1_low_broken"]:
                break_parts.append("کف")
            
            result["description"] = (
                f"شکست {' و '.join(break_parts)} M1 تأیید شد (صفحه ۳۶۱-۳۶۲) - "
                f"{result['break_type'].value}"
            )
        else:
            result["description"] = "هیچ شکست سقف یا کفی برای M1 رخ نداده است (صفحه ۳۶۱)"
        
        return result
    
    # ─── ۲-۷. انتخاب گروه ترکیبی (صفحه ۳۶۴) ──────────────
    
    def select_composite_group(self, waves: List[WaveM]) -> Dict[str, Any]:
        """
        انتخاب گروه ترکیبی از چند موج
        
        مطابق صفحه ۳۶۴:
        ┌─────────────────────────────────────────────────────────────────┐
        │ "به هنگام انتخاب گروه ترکیبی از چند موج، بهتر است در قالب     │
        │ الگوهای استاندارد قابل فشرده سازی باشند. چرا که این قوانین   │
        │ در مورد الگوهای فشرده ای که از ابتدای خود تجاوز کرده باشند    │
        │ کاربرد ندارد. در این گونه موارد فقط ساختار الگو را حفظ کنید   │
        │ (به نکته صفحه ۴۳۶ مراجعه کنید)."                              │
        └─────────────────────────────────────────────────────────────────┘
        """
        result = {
            "selected": [],
            "is_compressible": False,
            "structure_type": "",
            "has_exceeded_start": False,  # آیا از ابتدای خود تجاوز کرده؟
            "page": "364",
            "description": ""
        }
        
        if len(waves) < 3:
            return {**result, "description": "حداقل ۳ موج برای انتخاب گروه نیاز است"}
        
        # ── بررسی اینکه آیا الگو از ابتدای خود تجاوز کرده است ──
        # (صفحه ۳۶۴: "الگوهای فشرده ای که از ابتدای خود تجاوز کرده باشند")
        start_price = waves[0].start_price
        end_price = waves[-1].end_price
        
        if waves[0].direction == 1:  # صعودی
            result["has_exceeded_start"] = end_price > start_price
        else:  # نزولی
            result["has_exceeded_start"] = end_price < start_price
        
        # ── بررسی قابلیت فشرده‌سازی ──
        # الگوهای استاندارد قابل فشرده‌سازی: ۳، ۵، ۷، ۹ موجی
        valid_structures = [3, 5, 7, 9]
        compressible_structures = []
        
        for count in valid_structures:
            if count <= len(waves):
                group = waves[:count]
                if self._is_standard_pattern(group):
                    compressible_structures.append({
                        "count": count,
                        "group": group,
                        "is_standard": True
                    })
                else:
                    compressible_structures.append({
                        "count": count,
                        "group": group,
                        "is_standard": False
                    })
        
        # ── انتخاب بهترین گروه ──
        for struct in compressible_structures:
            if struct["is_standard"] and struct["count"] in valid_structures:
                # اگر از ابتدای خود تجاوز کرده باشد، فقط ساختار را حفظ کن (صفحه ۳۶۴)
                if result["has_exceeded_start"]:
                    result["selected"] = struct["group"]
                    result["is_compressible"] = False
                    result["structure_type"] = f"ساختار_حفظ_شده_{struct['count']}_موجی"
                    result["description"] = (
                        f"الگوی {struct['count']} موجی از ابتدای خود تجاوز کرده - "
                        "فقط ساختار حفظ شد (نکته صفحه ۴۳۶)"
                    )
                    return result
                else:
                    result["selected"] = struct["group"]
                    result["is_compressible"] = True
                    result["structure_type"] = f"فشرده_{struct['count']}_موجی"
                    result["description"] = (
                        f"گروه {struct['count']} موجی قابل فشرده‌سازی (صفحه ۳۶۴)"
                    )
                    return result
        
        # ── اگر هیچ الگوی استانداردی نبود ──
        result["selected"] = waves[:3]
        result["is_compressible"] = False
        result["structure_type"] = "ساختار_حفظ_شده"
        result["description"] = (
            "الگوی استاندارد قابل فشرده‌سازی یافت نشد - فقط ساختار حفظ شد "
            "(صفحه ۳۶۴ و نکته ۴۳۶)"
        )
        
        return result
    
    def _is_standard_pattern(self, waves: List[WaveM]) -> bool:
        """
        بررسی اینکه آیا گروه موج‌ها الگوی استاندارد دارند
        (استفاده در صفحه ۳۶۴ برای تشخیص الگوهای قابل فشرده‌سازی)
        """
        if len(waves) < 3:
            return False
        
        # بررسی تناوب جهت‌ها
        dirs = [w.direction for w in waves]
        
        # الگوی ۳ موجی: UP-DOWN-UP یا DOWN-UP-DOWN
        if len(waves) == 3:
            return dirs in [[1, -1, 1], [-1, 1, -1]]
        
        # الگوی ۵ موجی: UP-DOWN-UP-DOWN-UP یا برعکس
        if len(waves) == 5:
            return dirs in [[1, -1, 1, -1, 1], [-1, 1, -1, 1, -1]]
        
        # الگوی ۷ موجی: UP-DOWN-UP-DOWN-UP-DOWN-UP یا برعکس
        if len(waves) == 7:
            expected_7 = [1, -1, 1, -1, 1, -1, 1]
            return dirs == expected_7 or dirs == [-d for d in expected_7]
        
        # الگوی ۹ موجی: UP-DOWN-UP-DOWN-UP-DOWN-UP-DOWN-UP یا برعکس
        if len(waves) == 9:
            expected_9 = [1, -1, 1, -1, 1, -1, 1, -1, 1]
            return dirs == expected_9 or dirs == [-d for d in expected_9]
        
        return False
    
    # ─── ۲-۸. تحلیل کامل یک موج M1 ────────────────────────
    
    def analyze_wave_m1(self, m1: WaveM, 
                        m0: Optional[WaveM] = None,
                        m2: Optional[WaveM] = None,
                        m3: Optional[WaveM] = None) -> ExaminationResult:
        """
        تحلیل کامل قوانین معاینه برای یک موج M1
        
        شامل تمام مراحل:
        ۱. تعیین نقطه خاتمه موج‌های پسین (M2, M3) - صفحه ۳۵۵
        ۲. تعیین نقطه خاتمه موج‌های پیشین (M0) - صفحه ۳۵۸-۳۵۹
        ۳. تشخیص شکست سقف/کف - صفحه ۳۶۱-۳۶۲
        ۴. تشخیص ترکیب موج‌ها - صفحه ۳۶۰
        ۵. انتخاب گروه ترکیبی - صفحه ۳۶۴
        """
        result = ExaminationResult(
            m1=m1,
            m0=m0,
            m2=m2,
            m3=m3,
            description="",
            page_reference=""
        )
        
        # ── مرحله ۱: بررسی شکست سقف/کف (صفحه ۳۶۱) ──
        if m2 and m3:
            break_check = self.check_break_rule(m1, m2, m3)
            result.m1_high_broken = break_check["m1_high_broken"]
            result.m1_low_broken = break_check["m1_low_broken"]
            result.m0_high_broken = break_check["m0_high_broken"]
            result.m0_low_broken = break_check["m0_low_broken"]
            
            if not break_check["is_valid"]:
                result.description = "هیچ شکست سقف یا کفی رخ نداده است (صفحه ۳۶۱)"
                return result

        # ── اعمال تأثیر کیفیت داده از فصل‌های پیش‌نیاز ──
        quality_note = []

        # فصل ۴: کیفیت کش دیتا
        if self.quality_scores.get("cash_quality", 0) >= 80:
            quality_note.append("کیفیت کش دیتا بالا ✓")
            result.confidence_score = min(result.confidence_score + 0.1, 1.0)
        elif self.quality_scores.get("cash_quality", 0) < 50:
            quality_note.append("کیفیت کش دیتا پایین ⚠️")
            result.confidence_score = max(result.confidence_score - 0.1, 0.0)

        # فصل ۵: تعداد تک‌موج‌ها
        if self.quality_scores.get("wave_count", 0) > 100:
            quality_note.append("تک‌موج‌های کافی ✓")
            result.confidence_score = min(result.confidence_score + 0.05, 1.0)

        # فصل ۷: موج خنثی
        if self.quality_scores.get("neutrality_count", 0) > 0:
            quality_note.append("⚠️ موج خنثی شناسایی شده - تأیید با احتیاط")
            result.confidence_score = max(result.confidence_score - 0.1, 0.0)

        # فصل ۱۴: نسبت‌های فیبوناچی
        if self.quality_scores.get("fib_ratio_count", 0) > 50:
            quality_note.append("ساختار فیبوناچی قوی ✓")
            result.confidence_score = min(result.confidence_score + 0.1, 1.0)

        # فصل ۱۵: رتبه الگو
        pattern_rating = self.quality_scores.get("pattern_rating", 0)
        if abs(pattern_rating) >= 2:
            quality_note.append(f"الگوی قوی (رتبه {pattern_rating}) ✓")
            result.confidence_score = min(result.confidence_score + 0.1, 1.0)

        if quality_note:
            result.description += f" | {' | '.join(quality_note)}"
        
        # ── مرحله ۲: تعیین نقطه خاتمه موج‌های پسین (صفحه ۳۵۵) ──
        if m2 and m3:
            subsequent = self.find_subsequent_endpoint(m1, m2, m3)
            result.m2_endpoint = subsequent.get("m2_endpoint")
            result.m3_endpoint = subsequent.get("m3_endpoint")
            result.confirmation_type = subsequent.get("confirmation_type", "")
            result.is_confirmed = subsequent.get("is_confirmed", False)
            result.page_reference = subsequent.get("page", "")
            
            if result.is_confirmed:
                result.confidence_score = min(result.confidence_score * 1.1, 1.0)
            else:
                result.confidence_score = max(result.confidence_score * 0.7, 0.0)
                        
            # ═══════════════════════════════════════════════════
            # ✅ اعمال تأثیر کیفیت داده از فصل‌های پیش‌نیاز
            # ═══════════════════════════════════════════════════
            
            cash_quality = self.quality_scores.get("cash_quality", 0)
            fib_count = self.quality_scores.get("fib_ratio_count", 0)
            pattern_rating = self.quality_scores.get("pattern_rating", 0)
            neutrality_count = self.quality_scores.get("neutrality_count", 0)
            
            # ── فصل ۴: کیفیت کش دیتا ──
            if cash_quality >= 80:
                result.description += " | کیفیت کش دیتا بالا ✓"
                result.confidence_score = min(result.confidence_score + 0.15, 1.0)
            elif cash_quality < 50:
                result.description += " | ⚠️ کیفیت کش دیتا پایین"
                result.confidence_score = max(result.confidence_score - 0.15, 0.0)
                if result.is_confirmed and cash_quality < 30:
                    result.is_confirmed = False
                    result.description += " → تأیید لغو شد (کیفیت کش دیتا بسیار پایین)"
            
            # ── فصل ۱۴: تعداد نسبت‌های فیبوناچی ──
            if fib_count > 100:
                result.description += " | ساختار فیبوناچی قوی ✓"
                result.confidence_score = min(result.confidence_score + 0.1, 1.0)
            elif fib_count < 50 and fib_count > 0:
                result.description += " | ⚠️ نسبت‌های فیبوناچی کم"
                result.confidence_score = max(result.confidence_score - 0.1, 0.0)
            
            # ── فصل ۱۵: رتبه الگو ──
            if abs(pattern_rating) >= 2:
                result.description += f" | الگوی قوی (رتبه {pattern_rating}) ✓"
                result.confidence_score = min(result.confidence_score + 0.1, 1.0)
            
            # ── فصل ۷: موج خنثی ──
            if neutrality_count > 0:
                result.description += " | ⚠️ موج خنثی شناسایی شده - تأیید با احتیاط"
                result.confidence_score = max(result.confidence_score - 0.1, 0.0)
            
            # ── فصل ۵: تعداد تک‌موج‌ها ──
            wave_count = self.quality_scores.get("wave_count", 0)
            if wave_count >= 100:
                result.description += " | تک‌موج‌های عالی ✓✓"
                result.confidence_score = min(result.confidence_score + 0.15, 1.0)
            elif wave_count >= 50:
                result.description += " | تک‌موج‌های کافی ✓"
                result.confidence_score = min(result.confidence_score + 0.05, 1.0)
            else:
                result.description += " | تک‌موج‌های کم"
                result.confidence_score = max(result.confidence_score - 0.05, 0.0)

            # ── فصل ۱۱: کیفیت بر اساس الگوهای شتابدار ──
            impulse_count = self.quality_scores.get("impulse_count", 0)
            if impulse_count >= 5:
                result.description += f" | {impulse_count} الگوی شتابدار ✓✓"
                result.confidence_score = min(result.confidence_score + 0.15, 1.0)
            elif impulse_count >= 2:
                result.description += f" | {impulse_count} الگوی شتابدار ✓"
                result.confidence_score = min(result.confidence_score + 0.05, 1.0)
            else:
                result.description += f" | {impulse_count} الگوی شتابدار"
                result.confidence_score = max(result.confidence_score - 0.05, 0.0)

            # ── فصل ۱۲: کیفیت بر اساس الگوهای اصلاحی ──
            corrective_count = self.quality_scores.get("corrective_count", 0)
            if corrective_count >= 20:
                result.description += f" | {corrective_count} الگوی اصلاحی ✓✓"
                result.confidence_score = min(result.confidence_score + 0.15, 1.0)
            elif corrective_count >= 10:
                result.description += f" | {corrective_count} الگوی اصلاحی ✓"
                result.confidence_score = min(result.confidence_score + 0.05, 1.0)
            else:
                result.description += f" | {corrective_count} الگوی اصلاحی"
                result.confidence_score = max(result.confidence_score - 0.05, 0.0)

            # ── فصل ۱۵: رتبه الگو ──
            pattern_rating = self.quality_scores.get("pattern_rating", 0)
            if abs(pattern_rating) >= 2:
                result.description += f" | الگوی قوی (رتبه {pattern_rating}) ✓✓"
                result.confidence_score = min(result.confidence_score + 0.15, 1.0)
            elif abs(pattern_rating) >= 1:
                result.description += f" | الگوی متوسط (رتبه {pattern_rating}) ✓"
                result.confidence_score = min(result.confidence_score + 0.05, 1.0)
            else:
                result.description += f" | الگوی ضعیف (رتبه {pattern_rating})"
                result.confidence_score = max(result.confidence_score - 0.05, 0.0)
        
        # ── مرحله ۳: تعیین نقطه خاتمه موج‌های پیشین (صفحه ۳۵۸) ──
        if m0:
            previous = self.find_previous_endpoint(m0, m1)
            result.m0_endpoint = previous.get("m0_endpoint")
            
            if previous.get("is_confirmed", False):
                if not result.is_confirmed:
                    result.is_confirmed = True
                    result.confirmation_type = previous.get("confirmation_type", "")
                    result.confirmation_price = result.m0_endpoint
                    result.page_reference = previous.get("page", "")
                    result.description = previous.get("description", "")
        
        # ── مرحله ۴: تشخیص ترکیب M0 (صفحه ۳۶۰) ──
        if m0 and m1:
            # پیدا کردن موج‌های قبل از M0
            prev_waves = [w for w in self.waves if w.index < m0.index]
            if len(prev_waves) >= 3:
                composite_check = self.detect_composite_structure(prev_waves[-3:], m1)
                result.m0_is_composite = composite_check.get("is_composite", False)
                result.composite_count_m0 = composite_check.get("wave_count", 0)
                result.composite_type = composite_check.get("structure_type", "")
        
        # ── مرحله ۵: تشخیص ترکیب M2 (صفحه ۳۶۰) ──
        if m2 and m3:
            # پیدا کردن موج‌های بین M2 و M3
            mid_waves = [w for w in self.waves if m2.index < w.index < m3.index]
            if len(mid_waves) >= 3:
                composite_check = self.detect_composite_structure(mid_waves, m1)
                result.m2_is_composite = composite_check.get("is_composite", False)
                result.composite_count_m2 = composite_check.get("wave_count", 0)
                if not result.composite_type:
                    result.composite_type = composite_check.get("structure_type", "")
        
        # ── مرحله ۶: انتخاب گروه ترکیبی (صفحه ۳۶۴) ──
        if m2 and m3:
            group_check = self.select_composite_group([m1, m2, m3])
            result.is_compressible = group_check.get("is_compressible", False)
            result.compressed_structure = group_check.get("structure_type", "")
            
            if group_check.get("has_exceeded_start", False):
                result.description += " | الگو از ابتدای خود تجاوز کرده - ساختار حفظ شد"
        
        # ── اضافه کردن داده‌های فصل‌های پیش‌نیاز ──
        result.chapter_4_data = self.chapter_4_data
        result.chapter_5_data = self.chapter_5_data
        result.chapter_7_data = self.chapter_7_data
        result.chapter_14_data = self.chapter_14_data
        result.chapter_15_data = self.chapter_15_data
        
        return result
    
    # ─── ۲-۹. تحلیل کامل همه موج‌ها ──────────────────────
    
    def full_analysis(self) -> Dict[str, Any]:
        """
        تحلیل کامل قوانین معاینه برای همه موج‌ها
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "wave_count": len(self.waves),
            "examinations": [],
            "summary": {
                "confirmed": 0,
                "tentative": 0,
                "rejected": 0,
                "composite": 0,
                "compressible": 0
            },
            "chapter_data": {
                "chapter_5": self.chapter_5_data,
                "chapter_11": self.chapter_11_data,
                "chapter_12": self.chapter_12_data,
                "chapter_15": self.chapter_15_data
            },
            "quality_scores": self.quality_scores,
            "analysis_notes": []
        }
        
        # ── تحلیل هر موج به عنوان M1 ──
        for i, wave in enumerate(self.waves):
            # پیدا کردن M0 (موج پیشین) - صفحه ۳۵۸
            m0 = self.waves[i - 1] if i > 0 else None
            
            # پیدا کردن M2 و M3 (موج‌های پسین) - صفحه ۳۵۵
            m2 = self.waves[i + 1] if i + 1 < len(self.waves) else None
            m3 = self.waves[i + 2] if i + 2 < len(self.waves) else None
            
            # تحلیل
            exam_result = self.analyze_wave_m1(wave, m0, m2, m3)
            self.results.append(exam_result)
            
            # به‌روزرسانی خلاصه
            if exam_result.is_confirmed:
                results["summary"]["confirmed"] += 1
            elif exam_result.m0_is_composite or exam_result.m2_is_composite:
                results["summary"]["composite"] += 1
            else:
                results["summary"]["tentative"] += 1
            
            if exam_result.is_compressible:
                results["summary"]["compressible"] += 1

            if exam_result.confidence_score >= 0.8:
                results["analysis_notes"].append({
                    "wave_index": wave.index,
                    "status": "تأیید قوی",
                    "confidence": round(exam_result.confidence_score, 2),
                    "description": exam_result.description[:80]
                })
            elif exam_result.confidence_score <= 0.3 and exam_result.is_confirmed:
                results["analysis_notes"].append({
                    "wave_index": wave.index,
                    "status": "تأیید ضعیف - نیاز به بازبینی",
                    "confidence": round(exam_result.confidence_score, 2),
                    "description": exam_result.description[:80]
                })
            
            # ذخیره نتیجه
            results["examinations"].append({
                "wave_index": wave.index,
                "direction": wave.direction_str,
                "is_confirmed": exam_result.is_confirmed,
                "confirmation_type": exam_result.confirmation_type,
                "confirmation_price": exam_result.confirmation_price,
                "m0_composite": exam_result.m0_is_composite,
                "m2_composite": exam_result.m2_is_composite,
                "is_compressible": exam_result.is_compressible,
                "compressed_structure": exam_result.compressed_structure,
                "page_reference": exam_result.page_reference,
                "description": exam_result.description
            })
        
        return results


# ══════════════════════════════════════════════════════════════════
# ۳. تابع اصلی analyze (interface برای main.py)
# ══════════════════════════════════════════════════════════════════

def analyze(data: pd.DataFrame, logger=None, context=None):
    import numpy as np
    
    close = data["close"].values if "close" in data.columns else data["Close"].values
    high = data["high"].values if "high" in data.columns else data["High"].values
    low = data["low"].values if "low" in data.columns else data["Low"].values
    n = len(close)
    
    # ── فقط این ۴ تا از context ──
    chapter_5_data = None
    chapter_11_data = None
    chapter_12_data = None
    chapter_15_data = None
    
    if context:
        if "chapter_5" in context:
            chapter_5_data = context["chapter_5"]
        if "chapter_11" in context:
            chapter_11_data = context["chapter_11"]
        if "chapter_12" in context:
            chapter_12_data = context["chapter_12"]
        if "chapter_15" in context:
            chapter_15_data = context["chapter_15"]
    
    analyzer = ExaminationAnalyzer(
        data=data,
        chapter_5_data=chapter_5_data,
        chapter_11_data=chapter_11_data,
        chapter_12_data=chapter_12_data,
        chapter_15_data=chapter_15_data
    )
    
    results = analyzer.full_analysis()
    
    key_results = {
        "عنوان": "فصل ۱۶ - قوانین معاینه",
        "مرجع_کتاب": "صفحات ۳۵۴ تا ۳۶۴ - گلن نیلی",
        "وضعیت": "تحلیل کامل",
        "تعداد_کندل": n,
        "تعداد_امواج": len(analyzer.waves),
        "تعداد_تأیید_شده": results["summary"]["confirmed"],
        "درصد_تأیید": f"{results['summary']['confirmed'] / max(len(analyzer.waves), 1) * 100:.1f}%",
        "تعداد_در_حال_بررسی": results["summary"]["tentative"],
        "تعداد_ترکیبی": results["summary"]["composite"],
        "تعداد_قابل_فشرده‌سازی": results["summary"]["compressible"],
        "آخرین_قیمت": round(float(close[-1]), 4) if n > 0 else 0,
        "بالاترین": round(float(np.max(high)), 4) if n > 0 else 0,
        "پایین‌ترین": round(float(np.min(low)), 4) if n > 0 else 0,
        
        # ── فقط این ۴ تا ──
        "تعداد_تک_موج_فصل۵": str(analyzer.quality_scores.get("wave_count", 0)),
        "تعداد_الگوهای_شتابدار_فصل۱۱": str(analyzer.quality_scores.get("impulse_count", 0)),
        "تعداد_الگوهای_اصلاحی_فصل۱۲": str(analyzer.quality_scores.get("corrective_count", 0)),
        "رتبه_الگو_فصل۱۵": str(analyzer.quality_scores.get("pattern_rating", 0)),
        
        "میانگین_اطمینان_تأییدها": str(round(
            sum(e.confidence_score for e in analyzer.results) / max(len(analyzer.results), 1), 2
        )),
    }
    
    # ── تأییدها ──
    confirmed_exams = [e for e in results["examinations"] if e["is_confirmed"]]
    for idx, exam in enumerate(confirmed_exams[:5]):
        key_results[f"تأیید_{idx+1}"] = (
            f"موج {exam['wave_index']} - {exam['direction']} - "
            f"{exam['confirmation_type']} - قیمت: {exam['confirmation_price']:.2f} - "
            f"{exam.get('page_reference', '')}"
        )
    
    key_results["تفسیر_نهایی"] = _generate_final_interpretation(key_results, results)
    
    if logger:
        logger.add_section("فصل ۱۶ - قوانین معاینه", level=1)
        for k, v in key_results.items():
            if not isinstance(v, (dict, list)):
                logger.add_result(k, str(v))
    
    return key_results


def _generate_final_interpretation(key_results: Dict, results: Dict) -> str:
    """تولید تفسیر نهایی کامل مطابق صفحات ۳۵۴-۳۶۴"""
    lines = []
    lines.append("═" * 80)
    lines.append("فصل ۱۶: قوانین معاینه (نئوویو) - تفسیر کامل")
    lines.append("مرجع: کتاب استادی در امواج الیوت - گلن نیلی | صفحات ۳۵۴-۳۶۴")
    lines.append("═" * 80)
    lines.append("")
    
    lines.append("📊 آمار کلی:")
    lines.append(f"   • تعداد کندل‌ها: {key_results.get('تعداد_کندل', 0)}")
    lines.append(f"   • تعداد امواج: {key_results.get('تعداد_امواج', 0)}")
    lines.append(f"   • تأیید شده: {key_results.get('تعداد_تأیید_شده', 0)}")
    lines.append(f"   • در حال بررسی: {key_results.get('تعداد_در_حال_بررسی', 0)}")
    lines.append(f"   • ترکیبی: {key_results.get('تعداد_ترکیبی', 0)}")
    lines.append(f"   • قابل فشرده‌سازی: {key_results.get('تعداد_قابل_فشرده‌سازی', 0)}")
    lines.append("")
    
    lines.append("📋 قوانین معاینه (صفحات ۳۵۴-۳۶۴):")
    lines.append("")
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ قانون ۱: تعیین نقطه خاتمه موج‌های پسین (صفحه ۳۵۵)             │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ حالت اول: M2 خلاف جهت M1 اما پیش از شکستن کف M1،              │")
    lines.append("   │           سقف M1 توسط M3 شکسته می‌شود ✓                       │")
    lines.append("   │ حالت دوم: M2 کف M1 را می‌شکند، سپس M3 در راستای M1 رخ می‌دهد ✓│")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")
    
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ قانون ۲: تعیین نقطه خاتمه موج‌های پیشین (صفحه ۳۵۸-۳۵۹)       │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ ۳۵۸A: عقب رفتن تا آخرین باری که بازار بالای M0 بوده           │")
    lines.append("   │ ۳۵۸B: عقب رفتن تا آخرین باری که بازار زیر کف M0 بوده          │")
    lines.append("   │ ۳۵۹A: عقب رفتن تا آخرین باری که بازار بالای سقف M1 بوده       │")
    lines.append("   │ ۳۵۹B: عقب رفتن تا آخرین باری که بازار زیر کف M1 بوده          │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")
    
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ قانون ۳: ترکیب موج‌ها (صفحه ۳۶۰)                               │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ M0 و M2 می‌توانند ترکیبی از ۳، ۵، ۷ یا ۹ موج باشند            │")
    lines.append("   │ شرط: تک موج‌ها نتوانسته‌اند از سقف/کف عبور کنند              │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")
    
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ قانون ۴: شکست سقف/کف (صفحه ۳۶۱-۳۶۲)                           │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ برای تعیین موج‌های پیش و پس، سقف/کف باید شکسته شود            │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")
    
    lines.append("   ┌─────────────────────────────────────────────────────────────────┐")
    lines.append("   │ قانون ۵: انتخاب گروه ترکیبی (صفحه ۳۶۴)                         │")
    lines.append("   ├─────────────────────────────────────────────────────────────────┤")
    lines.append("   │ الگوهای قابل فشرده‌سازی: ۳، ۵، ۷، ۹ موجی                     │")
    lines.append("   │ در الگوهای فشرده‌ای که از ابتدای خود تجاوز کرده‌اند،          │")
    lines.append("   │ فقط ساختار الگو حفظ می‌شود (نکته صفحه ۴۳۶)                    │")
    lines.append("   └─────────────────────────────────────────────────────────────────┘")
    lines.append("")
    
    lines.append("💡 نتیجه نئوویو:")
    if key_results.get('تعداد_تأیید_شده', 0) > 0:
        lines.append(f"   ✅ {key_results.get('تعداد_تأیید_شده', 0)} نقطه خاتمه با قوانین معاینه تأیید شد.")
        lines.append("   🔍 قوانین معاینه به شناسایی نقاط شروع و خاتمه دقیق تک‌موج‌ها کمک می‌کند.")
    else:
        lines.append("   ⚠️ هیچ نقطه خاتمه‌ای با قوانین معاینه تأیید نشد.")
        lines.append("   📌 ممکن است نیاز به بررسی موج‌های بیشتری باشد.")
    
    lines.append("")
    lines.append("═" * 80)
    lines.append("پایان تفسیر فصل ۱۶")
    lines.append("═" * 80)
    
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════
# اجرای مستقیم برای تست
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 70)
    print("تست کامل تحلیل فصل ۱۶ - قوانین معاینه")
    print("مرجع: کتاب گلن نیلی - صفحات ۳۵۴ تا ۳۶۴")
    print("=" * 70)
    
    # ایجاد داده تست با الگوی مشخص برای تست قوانین
    np.random.seed(42)
    n = 300
    
    # ایجاد یک الگوی صعودی-نزولی-صعودی برای تست
    base_price = 100
    prices = []
    
    # فاز ۱: صعودی (M1)
    for i in range(50):
        prices.append(base_price + i * 0.5 + np.random.normal(0, 0.3))
    
    # فاز ۲: نزولی (M2)
    for i in range(30):
        prices.append(prices[-1] - i * 0.8 + np.random.normal(0, 0.3))
    
    # فاز ۳: صعودی (M3)
    for i in range(50):
        prices.append(prices[-1] + i * 0.6 + np.random.normal(0, 0.3))
    
    # فاز ۴: نزولی
    for i in range(20):
        prices.append(prices[-1] - i * 0.4 + np.random.normal(0, 0.3))
    
    # فاز ۵: صعودی
    for i in range(50):
        prices.append(prices[-1] + i * 0.7 + np.random.normal(0, 0.3))
    
    # فاز ۶: نزولی
    for i in range(30):
        prices.append(prices[-1] - i * 0.5 + np.random.normal(0, 0.3))
    
    # فاز ۷: صعودی
    for i in range(40):
        prices.append(prices[-1] + i * 0.3 + np.random.normal(0, 0.3))
    
    prices = np.array(prices)
    
    data = pd.DataFrame({
        'open': prices,
        'high': prices + abs(np.random.normal(0, 0.5, len(prices))),
        'low': prices - abs(np.random.normal(0, 0.5, len(prices))),
        'close': prices,
        'volume': np.random.randint(1000, 10000, len(prices))
    })
    
    print(f"\n📊 داده تست: {len(data)} کندل")
    print(f"   بازه قیمتی: {data['low'].min():.2f} - {data['high'].max():.2f}")
    
    print("\n" + "─" * 50)
    print("🔍 تحلیل قوانین معاینه")
    print("─" * 50)
    
    # ایجاد context شبیه‌سازی‌شده
    context = {
        "chapter_4": {"امتیاز_کیفیت_کش_دیتا": "91.4"},
        "chapter_5": {"تعداد_کل_تک‌موج": "117"},
        "chapter_7": {"موج_خنثی_شناسایی_شده": "0"},
        "chapter_14": {"تعداد_نسبت‌های_داخلی": "1477"},
        "chapter_15": {"نوع_الگو": "زیگزاگ", "رتبه_الگو": "0"}
    }
    
    results = analyze(data, context=context)
    
    for key, value in results.items():
        if not isinstance(value, (dict, list)):
            print(f"   {key}: {value}")
    
    print("\n" + "=" * 70)
    print("✅ تحلیل فصل ۱۶ کامل شد")
    print("=" * 70)