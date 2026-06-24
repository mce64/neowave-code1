"""
╔══════════════════════════════════════════════════════════════════╗
║         هسته اصلی نئوویو - استادی در امواج الیوت              ║
║                    گلن نیلی | NeoWave                           ║
║         معماری: Single-file + Dynamic Chapter Loader            ║
║         با پشتیبانی از وابستگی بین فصل‌ها                      ║
╚══════════════════════════════════════════════════════════════════╝

ساختار:
- هسته اصلی (این فایل): UI + ChapterManager + ChartAnalyzer
- پوشه chapters/: یک فایل chapter_XX.py برای هر فصل
- هر فصل یک تابع analyze(data, logger, context) دارد
- context: نتایج تحلیل فصل‌های قبلی برای استفاده در تحلیل
- پشتیبانی از وابستگی بین فصل‌ها
- گزارش خطای کامل
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import importlib
import importlib.util
import sys
import os
from pathlib import Path
import json
import traceback
import inspect
import hashlib
from typing import Dict, Any, Optional, List, Set, Callable
from dataclasses import dataclass, field
import logging
import time


# ══════════════════════════════════════════════════════════════════
# تنظیمات صفحه
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="NeoWave | نئوویو - گلن نیلی",
    page_icon="〜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── تنظیمات لاگینگ ───
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('neowave_debug.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NeoWave")


# ══════════════════════════════════════════════════════════════════
# استایل CSS
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;900&display=swap');

:root {
    --bg-deep:    #070b14;
    --bg-card:    #0d1422;
    --bg-panel:   #111827;
    --accent-r:   #f97316;
    --accent-b:   #38bdf8;
    --accent-g:   #4ade80;
    --accent-y:   #facc15;
    --accent-p:   #a78bfa;
    --text-main:  #e2e8f0;
    --text-muted: #64748b;
    --border:     #1e293b;
    --border-hot: #f97316;
}

* { font-family: 'Vazirmatn', sans-serif !important; }
body, .stApp { background: var(--bg-deep) !important; color: var(--text-main); }

/* ── هدر اصلی */
.nw-header {
    background: linear-gradient(135deg, #070b14 0%, #0d1f3c 50%, #070b14 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.nw-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(56,189,248,0.06) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 50%, rgba(249,115,22,0.06) 0%, transparent 60%);
    pointer-events: none;
}
.nw-header h1 { color: var(--accent-r); font-size: 2rem; margin: 0; letter-spacing: -0.5px; }
.nw-header h3 { color: var(--accent-b); font-size: 1rem; margin: 6px 0 0 0; font-weight: 400; }
.nw-header p  { color: var(--text-muted); font-size: 0.8rem; margin: 8px 0 0 0; }

/* ── کارت‌ها */
.nw-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin: 12px 0;
}
.nw-card h4 { color: var(--accent-r); margin: 0 0 14px 0; font-size: 0.95rem; letter-spacing: 0.3px; }

/* ── متریک */
.nw-metric {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 12px;
    text-align: center;
}
.nw-metric .val { font-size: 1.5rem; font-weight: 700; color: var(--accent-b); line-height: 1; }
.nw-metric .lbl { font-size: 0.72rem; color: var(--text-muted); margin-top: 5px; }
.nw-metric.up   .val { color: var(--accent-g); }
.nw-metric.down .val { color: #f87171; }
.nw-metric.warn .val { color: var(--accent-y); }

/* ── بج وضعیت */
.nw-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}
.nw-badge.green  { background: rgba(74,222,128,0.15); color: var(--accent-g); border: 1px solid rgba(74,222,128,0.3); }
.nw-badge.red    { background: rgba(248,113,113,0.15); color: #f87171;        border: 1px solid rgba(248,113,113,0.3); }
.nw-badge.blue   { background: rgba(56,189,248,0.15); color: var(--accent-b); border: 1px solid rgba(56,189,248,0.3); }
.nw-badge.orange { background: rgba(249,115,22,0.15); color: var(--accent-r); border: 1px solid rgba(249,115,22,0.3); }
.nw-badge.purple { background: rgba(167,139,250,0.15);color: var(--accent-p); border: 1px solid rgba(167,139,250,0.3); }
.nw-badge.gray   { background: rgba(100,116,139,0.15); color: var(--text-muted); border: 1px solid rgba(100,116,139,0.3); }

/* ── فصل‌ها */
.nw-chapter-row {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 12px; border-radius: 8px;
    border: 1px solid var(--border);
    margin: 4px 0;
    background: var(--bg-panel);
    transition: border-color 0.2s;
}
.nw-chapter-row:hover { border-color: var(--accent-r); }
.nw-chapter-num  { color: var(--accent-r); font-weight: 700; font-size: 0.8rem; min-width: 28px; }
.nw-chapter-name { color: var(--text-main); font-size: 0.8rem; flex: 1; }
.nw-chapter-ok   { color: var(--accent-g); font-size: 0.75rem; }

/* ── خط جداساز */
.nw-divider {
    border: none; border-top: 1px solid var(--border);
    margin: 16px 0;
}

/* ── لیست نتایج */
.nw-result-item {
    display: flex; justify-content: space-between; align-items: center;
    padding: 7px 12px; border-radius: 6px;
    border-bottom: 1px solid var(--border);
}
.nw-result-item:last-child { border-bottom: none; }
.nw-result-key   { color: var(--text-muted); font-size: 0.8rem; }
.nw-result-val   { color: var(--accent-b);   font-size: 0.82rem; font-weight: 600; }

/* ── دکمه‌ها */
.stButton > button {
    background: linear-gradient(135deg, #f97316, #ea580c) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-weight: 600 !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(249,115,22,0.35) !important;
}

/* ── سایدبار */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}

/* ── تب‌ها */
.stTabs [data-baseweb="tab"] {
    color: var(--text-muted) !important;
    font-size: 0.85rem !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent-r) !important;
    border-bottom-color: var(--accent-r) !important;
}

/* ── اسکرول‌بار */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: var(--border-hot); border-radius: 4px; }

/* ── progress */
.nw-progress-wrap { background: var(--border); border-radius: 4px; height: 5px; margin: 8px 0; }
.nw-progress-fill { background: var(--accent-r); border-radius: 4px; height: 5px; transition: width 0.3s; }

/* ── خطاها */
.nw-error {
    background: rgba(248,113,113,0.1);
    border: 1px solid rgba(248,113,113,0.3);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #f87171;
}
.nw-error .title { font-weight: 700; }
.nw-error .detail { font-size: 0.85rem; margin-top: 4px; opacity: 0.8; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# لیست کامل ۳۶ فصل با وابستگی‌ها
# ══════════════════════════════════════════════════════════════════
CHAPTERS_LIST = [
    (1,  "پایه و اساس الیوت کلاسیک و نئوویو", []),
    (2,  "ساختار فراکتال", []),
    (3,  "ساختار دوره کامل امواج", [2]),
    (4,  "کش دیتا", []),
    (5,  "شناسایی تک‌موج‌ها", [2, 3, 4, 9]),
    (6,  "قانون تناسب", [2, 5]),
    (7,  "قانون خنثایی", [4, 5]),
    (8,  "نمودار لگاریتمی یا حسابی", [2, 5]),
    (9,  "تعدیل چارت", [4, 8]),
    (10, "دسته‌بندی امواج و الگوهای الیوتی", [2, 3, 5]),
    (11, "دسته‌بندی امواج شتابدار", [2, 3, 5, 10]),
    (12, "دسته‌بندی امواج اصلاحی", [2, 3, 5, 10, 11]),
    (13, "صفات و مشخصات موج‌ها", [2, 3, 5, 10, 11, 12]),
    (14, "تحلیل نسبت‌ها", [2, 5, 6, 11, 12]),
    (15, "میزان بازگشت بازار پس از الگوهای اصلاحی", [3, 12, 14]),
    (16, "قوانین معاینه", [15, 12, 11, 5]),
    (17, "قوانین بازگشت", [2, 3, 11, 12, 15]),
    (18, "قوانین پیش‌ساخت منطقی", [2, 3, 5, 11, 12, 16]),
    (19, "قوانین تفسیر وضعیت", [2, 5, 11, 12, 17, 18]),
    (20, "قانون تشابه و تعادل", [2, 5, 11, 12, 14]),
    (21, "مثال عملی برچسب‌گذاری", [10, 11, 12, 13, 14]),
    (22, "فشرده‌سازی و تجمیع الگوها", [2, 3, 10, 11, 12]),
    (23, "قانون نقاط تماس با خط روند", [2, 5, 11, 12]),
    (24, "قانون زمان", [2, 5, 11, 12]),
    (25, "قانون تناوب", [2, 5, 11, 12]),
    (26, "درجه‌بندی پیچیدگی موج‌ها", [2, 3, 10, 11, 12]),
    (27, "انواع موج از نظر سطح پیچیدگی", [2, 3, 10, 11, 12, 26]),
    (28, "ساختار بساموج‌ها", [2, 3, 5, 10, 26]),
    (29, "ساختار فراموج‌ها", [2, 3, 5, 10, 26, 28]),
    (30, "ساختار ابرموج‌ها", [2, 3, 5, 10, 26, 28, 29]),
    (31, "قانون استثناء", [2, 3, 5, 11, 12, 13]),
    (32, "امواج مفقود", [2, 3, 5, 11, 12, 31]),
    (33, "نکات کلیدی در موج‌شماری صحیح", [10, 11, 12, 13, 14, 16, 17]),
    (34, "استراتژی معامله با امواج", [10, 11, 12, 13, 14, 15, 16, 17]),
    (35, "پرسش و پاسخ با گلن نیلی", [10, 11, 12, 13, 14, 15, 16, 17, 33]),
    (36, "موارد ابهام‌دار که باید بررسی شوند", [10, 11, 12, 13, 14, 15, 16, 17, 33]),
]

CHAPTERS_DICT = {num: {"title": title, "deps": deps} for num, title, deps in CHAPTERS_LIST}
CHAPTER_TITLES = {num: title for num, title, _ in CHAPTERS_LIST}
CHAPTER_DEPS = {num: deps for num, _, deps in CHAPTERS_LIST}


# ══════════════════════════════════════════════════════════════════
# الگوی پیش‌فرض برای فصل‌های هنوز پیاده‌سازی نشده
# ══════════════════════════════════════════════════════════════════
DEFAULT_CHAPTER_TEMPLATE = '''"""
فصل {num}: {title}
منبع: کتاب "استادی در امواج الیوت" - گلن نیلی

TODO_UPGRADE: این فصل آماده‌ی پیاده‌سازی عمیق است.
              محتوای analyze را با منطق واقعی نئوویو جایگزین کنید.
وابستگی‌ها: {deps}
"""


def analyze(data, logger=None, context=None):
    """
    تحلیل فصل {num} - {title}

    پارامترها:
        data   : DataFrame با ستون‌های open, high, low, close, volume
        logger : آبجکت ResultsLogger برای ذخیره نتایج (اختیاری)
        context: دیکشنری نتایج تحلیل فصل‌های قبلی (وابستگی‌ها)

    خروجی:
        دیکشنری نتایج - همه key ها باید string باشند
    """
    import numpy as np

    close = data["close"].values if "close" in data.columns else data["Close"].values
    high  = data["high"].values  if "high"  in data.columns else data["High"].values
    low   = data["low"].values   if "low"   in data.columns else data["Low"].values
    n = len(close)

    results = {{
        "عنوان"   : "{title}",
        "وضعیت"   : "TODO_UPGRADE - پیاده‌سازی اولیه",
        "تعداد_داده": n,
        "آخرین_قیمت": round(float(close[-1]), 4) if n > 0 else 0,
        "بالاترین" : round(float(np.max(high)), 4) if n > 0 else 0,
        "پایین‌ترین": round(float(np.min(low)), 4)  if n > 0 else 0,
    }}

    # استفاده از context در صورت وجود
    if context:
        # اینجا می‌توانید از نتایج فصل‌های وابسته استفاده کنید
        pass

    if logger:
        logger.add_section(f"فصل {num}: {title}", level=1)
        for k, v in results.items():
            logger.add_result(k, str(v))

    return results
'''


# ══════════════════════════════════════════════════════════════════
# مدیریت لاگ
# ══════════════════════════════════════════════════════════════════
class ResultsLogger:
    """مدیریت ذخیره نتایج تحلیل در فایل متنی"""

    def __init__(self):
        self.sections: list[str] = []
        self.results: Dict[str, Any] = {}
        self.filename = f"neowave_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self._indent_level = 0

    def add_section(self, title: str, level: int = 1):
        if level == 1:
            sep = "═" * 70
        elif level == 2:
            sep = "─" * 50
        else:
            sep = "·" * 30
        self.sections.append(f"\n{sep}\n  {title}\n{sep}\n")

    def add_result(self, key: str, value, formula: str = ""):
        self.sections.append(f"   • {key}: {value}")
        if formula:
            self.sections.append(f"     ↳ {formula}")

    def add_wave(self, wave_name: str, details: dict):
        self.sections.append(f"\n   〜 {wave_name}:")
        for k, v in details.items():
            if isinstance(v, (dict, list)):
                self.sections.append(f"      {k}: {json.dumps(v, ensure_ascii=False, default=str)}")
            else:
                self.sections.append(f"      {k}: {v}")

    def add_error(self, chapter_num: int, error: str, trace: str = ""):
        self.sections.append(f"\n   ❌ خطا در فصل {chapter_num}:")
        self.sections.append(f"      {error}")
        if trace:
            self.sections.append(f"      جزئیات:\n{trace}")

    def save(self) -> str:
        header = (
            "═" * 80 + "\n"
            "   تحلیل نئوویو | گلن نیلی | NeoWave\n"
            f"   تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "═" * 80 + "\n"
        )
        footer = "\n" + "═" * 80 + "\n   پایان گزارش\n" + "═" * 80
        
        clean = []
        for line in self.sections:
            s = line.strip()
            if not s:
                continue
            if "تحلیل نئوویو" in s and "فصل" not in s:
                continue
            if s.startswith("تاریخ:") and len(s) < 30:
                continue
            if all(c in "═━─ " for c in s) and len(s) > 10:
                continue
            clean.append(line)
        
        content = header + "\n".join(clean) + footer
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(content)
        return self.filename


# ══════════════════════════════════════════════════════════════════
# مدیریت ماژول‌های فصل‌ها با پشتیبانی از وابستگی
# ══════════════════════════════════════════════════════════════════
@dataclass
class ChapterInfo:
    """اطلاعات یک فصل"""
    num: int
    title: str
    deps: List[int]
    module: Optional[object] = None
    is_loaded: bool = False
    is_upgraded: bool = False
    load_error: Optional[str] = None
    result: Optional[Dict] = None
    execution_time: float = 0.0
    hash: str = ""


class ChapterManager:
    """
    مدیریت بارگذاری و اجرای فصل‌ها با پشتیبانی از وابستگی
    
    ویژگی‌ها:
    - بارگذاری پویا از پوشه chapters/
    - شناسایی وابستگی‌ها بین فصل‌ها
    - ترتیب‌دهی توپولوژیک برای اجرا
    - کش کردن نتایج برای استفاده مجدد
    - گزارش خطای دقیق
    - سازگاری با امضای توابع مختلف (1، 2 یا 3 پارامتری)
    """

    CHAPTERS_DIR = "chapters"

    def __init__(self):
        self.chapters: Dict[int, ChapterInfo] = {}
        self._context: Dict[int, Dict] = {}
        self._load_errors: Dict[int, str] = {}
        self._cache: Dict[str, Dict] = {}
        
        self._ensure_directories()
        self._ensure_default_files()
        self._load_all()

    def _ensure_directories(self):
        """ایجاد پوشه‌های مورد نیاز"""
        Path(self.CHAPTERS_DIR).mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        Path("reports").mkdir(exist_ok=True)
        Path("cache").mkdir(exist_ok=True)

    def _ensure_default_files(self):
        """ایجاد فایل‌های پیش‌فرض برای فصل‌ها"""
        for num, title, deps in CHAPTERS_LIST:
            path = Path(self.CHAPTERS_DIR) / f"chapter_{num:02d}.py"
            if not path.exists():
                with open(path, "w", encoding="utf-8") as f:
                    f.write(DEFAULT_CHAPTER_TEMPLATE.format(
                        num=num, 
                        title=title, 
                        deps=", ".join(str(d) for d in deps)
                    ))

    def _load_all(self):
        """بارگذاری همه ماژول‌ها"""
        self.chapters = {}
        
        for num, title, deps in CHAPTERS_LIST:
            info = ChapterInfo(num=num, title=title, deps=deps)
            path = Path(self.CHAPTERS_DIR) / f"chapter_{num:02d}.py"
            
            if path.exists():
                try:
                    with open(path, "rb") as f:
                        content = f.read()
                        info.hash = hashlib.md5(content).hexdigest()
                    
                    spec = importlib.util.spec_from_file_location(
                        f"chapter_{num:02d}", str(path.resolve())
                    )
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    
                    info.module = mod
                    info.is_loaded = True
                    info.is_upgraded = "TODO_UPGRADE" not in content.decode('utf-8')
                    
                except Exception as e:
                    info.is_loaded = False
                    info.load_error = str(e)
                    self._load_errors[num] = str(e)
                    logger.error(f"خطا در بارگذاری فصل {num}: {e}")
            
            self.chapters[num] = info

    def reload(self):
        """بارگذاری مجدد همه ماژول‌ها"""
        self._load_all()
        self._cache.clear()
        self._context.clear()

    def get_dependencies(self, num: int) -> List[int]:
        return self.chapters.get(num, ChapterInfo(num, "", [])).deps

    def get_topological_order(self, selected: List[int]) -> List[int]:
        graph = {num: set(self.get_dependencies(num)) for num in selected}
        in_degree = {num: len(deps) for num, deps in graph.items()}
        queue = [num for num in selected if in_degree[num] == 0]
        result = []
        
        while queue:
            num = queue.pop(0)
            result.append(num)
            for other in selected:
                if num in graph[other]:
                    in_degree[other] -= 1
                    if in_degree[other] == 0:
                        queue.append(other)
        
        if len(result) != len(selected):
            remaining = set(selected) - set(result)
            for num in remaining:
                result.append(num)
                logger.warning(f"دور در وابستگی‌های فصل {num} - شکسته شد")
        
        return result

    def is_loaded(self, num: int) -> bool:
        return num in self.chapters and self.chapters[num].is_loaded

    def is_upgraded(self, num: int) -> bool:
        return num in self.chapters and self.chapters[num].is_upgraded

    def run(self, num: int, data: pd.DataFrame, 
            logger_obj: Optional[ResultsLogger] = None,
            context: Optional[Dict] = None) -> Dict:
        """
        اجرای یک فصل با سازگاری با هر دو امضای تابع
        """
        info = self.chapters.get(num)
        if not info or not info.is_loaded:
            return {
                "خطا": f"فصل {num} بارگذاری نشد",
                "وضعیت": "error",
                "دلیل": info.load_error if info else "فصل وجود ندارد"
            }
    
        mod = info.module
        if not hasattr(mod, "analyze"):
            return {
                "خطا": f"تابع analyze در فصل {num} وجود ندارد",
                "وضعیت": "error"
            }
    
        try:
            # بررسی امضای تابع analyze
            import inspect
            sig = inspect.signature(mod.analyze)
            params = list(sig.parameters.keys())
        
            # تشخیص تعداد پارامترهای مورد نیاز
            has_context = 'context' in params
            has_logger = 'logger' in params or 'logger_obj' in params
        
            # اجرا با پارامترهای مناسب
            if has_context and has_logger:
                # تابع با ۳ پارامتر: analyze(data, logger, context)
                result = mod.analyze(data, logger_obj, context) or {}
            elif has_logger:
                # تابع با ۲ پارامتر: analyze(data, logger)
                result = mod.analyze(data, logger_obj) or {}
            else:
                # تابع با ۱ پارامتر: analyze(data)
                result = mod.analyze(data) or {}
        
            # اگر تابع context را نپذیرفته اما context ارسال شده،
            # آن را به صورت دستی به result اضافه نمی‌کنیم (چون تابع از آن استفاده نکرده)
        
            # ذخیره در context برای استفاده بعدی
            self._context[num] = result
        
            return result
        
        except TypeError as e:
            # خطای نوع پارامتر - تلاش مجدد با امضای ساده‌تر
            if "takes" in str(e) and "positional" in str(e):
                try:
                    # تلاش با ۲ پارامتر
                    result = mod.analyze(data, logger_obj) or {}
                    self._context[num] = result
                    return result
                except Exception as e2:
                    try:
                        # تلاش با ۱ پارامتر
                        result = mod.analyze(data) or {}
                        self._context[num] = result
                        return result
                    except Exception as e3:
                        error_trace = traceback.format_exc()
                        if logger_obj:
                            logger_obj.add_error(num, str(e3), error_trace)
                        return {
                            "خطا": str(e3),
                            "traceback": error_trace,
                            "وضعیت": "runtime_error"
                        }
            else:
                error_trace = traceback.format_exc()
                if logger_obj:
                    logger_obj.add_error(num, str(e), error_trace)
                return {
                    "خطا": str(e),
                    "traceback": error_trace,
                    "وضعیت": "runtime_error"
                }
            
        except Exception as e:
            error_trace = traceback.format_exc()
            if logger_obj:
                logger_obj.add_error(num, str(e), error_trace)
        
            return {
                "خطا": str(e),
                "traceback": error_trace,
                "وضعیت": "runtime_error"
            }

    def run_selected(self, data: pd.DataFrame, 
                     selected: List[int],
                     logger_obj: Optional[ResultsLogger] = None,
                     progress_cb: Optional[Callable] = None) -> Dict[int, Dict]:
        """
        اجرای فصل‌های انتخاب‌شده با ترتیب وابستگی
        """
        if not selected:
            selected = [n for n, _, _ in CHAPTERS_LIST]
    
        order = self.get_topological_order(selected)
    
        results = {}
        context = {}
    
        for i, num in enumerate(order):
            if progress_cb:
                progress_cb(i + 1, len(order), num)
        
            # جمع‌آوری context از وابستگی‌ها
            deps = self.get_dependencies(num)
            chapter_context = {}
            for dep in deps:
                if dep in self._context:
                    chapter_context[f"chapter_{dep}"] = self._context[dep]
        
            # اجرای فصل
            start_time = time.time()
            result = self.run(num, data, logger_obj, chapter_context)
            elapsed = time.time() - start_time
        
            if num in self.chapters:
                self.chapters[num].result = result
                self.chapters[num].execution_time = elapsed
        
            results[num] = result
        
            if "خطا" not in result:
                self._context[num] = result
                context[f"chapter_{num}"] = result
        
            if logger_obj:
                status = "✅" if "خطا" not in result else "❌"
                logger_obj.add_section(f"{status} فصل {num}: {self.chapters[num].title}", level=2)
                logger_obj.add_result("زمان اجرا", f"{elapsed:.3f} ثانیه")
            
                if "خطا" in result:
                    logger_obj.add_error(num, result.get("خطا", ""), result.get("traceback", ""))
    
        return results

    def get_context(self, num: int) -> Dict:
        return self._context.get(num, {})

    def get_all_context(self) -> Dict[int, Dict]:
        return self._context.copy()

# ══════════════════════════════════════════════════════════════════
# تحلیل‌گر نمودار (ChartAnalyzer)
# ══════════════════════════════════════════════════════════════════
class ChartAnalyzer:
    """
    تحلیل‌های پایه روی داده قیمتی

    این کلاس داده را آماده می‌کند و اطلاعات پایه‌ای
    (مونوویو، نسبت‌های فیبو، حمایت/مقاومت، اندیکاتور)
    را برای نمایش در UI فراهم می‌کند.

    تمام محاسبات موجی عمیق‌تر توسط ماژول‌های فصل انجام می‌شود.
    """

    FIBS = [0.0, 0.236, 0.382, 0.5, 0.618, 0.764, 1.0, 1.272, 1.618, 2.618]

    def __init__(self, data: pd.DataFrame):
        self.data  = data.copy()
        self.close  = self._safe_arr("close",  "Close")
        self.open_  = self._safe_arr("open",   "Open")
        self.high   = self._safe_arr("high",   "High")
        self.low    = self._safe_arr("low",    "Low")
        self.volume = self._safe_arr("volume", "Volume", default=None)
        self.n = len(self.close)

    def _safe_arr(self, col_lower: str, col_upper: str, default=None):
        """استخراج ایمن ستون به عنوان آرایه float64"""
        if col_lower in self.data.columns:
            return self.data[col_lower].astype(float).values
        elif col_upper in self.data.columns:
            return self.data[col_upper].astype(float).values
        return default

    def find_monowaves(self, threshold_pct: float = 0.5) -> list[dict]:
        """شناسایی مونوویوها بر اساس آستانه درصدی تغییر قیمت"""
        from scipy.signal import argrelextrema
        
        high = self.high
        low = self.low
        
        # یافتن نقاط عطف
        peaks = argrelextrema(high, np.greater, order=3)[0]
        troughs = argrelextrema(low, np.less, order=3)[0]
        
        # ترکیب و مرتب‌سازی
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
            return []
        
        # ساخت مونوویوها
        waves = []
        for i in range(len(filtered) - 1):
            idx1, price1, _ = filtered[i]
            idx2, price2, _ = filtered[i + 1]
            
            waves.append({
                "dir": "UP" if price2 > price1 else "DOWN",
                "start": int(idx1),
                "end": int(idx2),
                "start_price": float(price1),
                "end_price": float(price2),
                "price_range": abs(float(price2) - float(price1)),
                "pct": round(abs((price2 - price1) / price1 * 100), 3) if price1 != 0 else 0,
                "bars": int(idx2 - idx1),
            })
        
        return waves

    def find_pivots(self, window: int = 3) -> tuple[list, list]:
        """یافتن سقف‌ها و کف‌های قیمتی"""
        highs, lows = [], []
        for i in range(window, self.n - window):
            local_h = self.high[i - window: i + window + 1]
            local_l = self.low[i - window:  i + window + 1]
            if float(self.high[i]) == float(np.max(local_h)):
                highs.append((i, float(self.high[i])))
            if float(self.low[i]) == float(np.min(local_l)):
                lows.append((i, float(self.low[i])))
        return highs, lows

    def detect_trend(self) -> dict:
        """تشخیص روند با MA20 و MA50"""
        if self.n < 20:
            ma20 = float(np.mean(self.close))
            ma50 = float(np.mean(self.close))
        else:
            ma20 = float(np.mean(self.close[-20:]))
            ma50 = float(np.mean(self.close[-50:])) if self.n >= 50 else float(np.mean(self.close))

        if ma20 > ma50 * 1.001:
            trend = "صعودی"
        elif ma20 < ma50 * 0.999:
            trend = "نزولی"
        else:
            trend = "خنثی"

        return {"trend": trend, "ma20": ma20, "ma50": ma50}

    def calc_rsi(self, period: int = 14) -> float | None:
        if self.n <= period:
            return None
        delta = np.diff(self.close)
        gain  = np.where(delta > 0, delta, 0.0)
        loss  = np.where(delta < 0, -delta, 0.0)
        ag = float(np.mean(gain[-period:]))
        al = float(np.mean(loss[-period:]))
        if al == 0:
            return 100.0
        return round(100 - 100 / (1 + ag / al), 2)

    def calc_macd(self) -> dict | None:
        if self.n < 26:
            return None
        series = pd.Series(self.close)
        ema12  = series.ewm(span=12, adjust=False).mean()
        ema26  = series.ewm(span=26, adjust=False).mean()
        macd   = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        return {
            "macd"      : round(float(macd.iloc[-1]),   4),
            "signal"    : round(float(signal.iloc[-1]), 4),
            "histogram" : round(float((macd - signal).iloc[-1]), 4),
        }

    def calc_fib_levels(self, last_n: int = 100) -> dict:
        """سطوح فیبوناچی بر اساس آخرین N کندل"""
        subset_h = self.high[-last_n:] if self.n > last_n else self.high
        subset_l = self.low[-last_n:]  if self.n > last_n else self.low
        h = float(np.max(subset_h))
        l = float(np.min(subset_l))
        diff = h - l
        return {str(r): round(l + diff * r, 4) for r in self.FIBS}

    def calc_sr_levels(self, window: int = 3) -> dict:
        highs, lows = self.find_pivots(window)
        res = sorted([h[1] for h in highs[-8:]], reverse=True) if highs else []
        sup = sorted([l[1] for l in lows[-8:]])                if lows  else []
        return {
            "resistance"        : res[:4],
            "support"           : sup[:4],
            "nearest_resistance": res[0] if res else None,
            "nearest_support"   : sup[0] if sup else None,
        }

    def monowave_stats(self, threshold_pct: float = 0.5) -> dict:
        waves = self.find_monowaves(threshold_pct)
        up   = [w for w in waves if w["dir"] == "UP"]
        down = [w for w in waves if w["dir"] == "DOWN"]

        avg_up_pct   = round(float(np.mean([w["pct"] for w in up])),   3) if up   else 0
        avg_down_pct = round(float(np.mean([w["pct"] for w in down])), 3) if down else 0
        avg_bars     = round(float(np.mean([w["bars"] for w in waves])), 1) if waves else 0

        rule_violations = []
        for i in range(len(waves) - 4):
            seg = waves[i: i + 5]
            dirs = [w["dir"] for w in seg]
            if dirs == ["UP","DOWN","UP","DOWN","UP"] or dirs == ["DOWN","UP","DOWN","UP","DOWN"]:
                w1, w2, w3, w4, w5 = seg
                if dirs[0] == "UP" and w2["end_price"] <= w1["start_price"]:
                    rule_violations.append(f"نقض Q1 در موج {i+1}")
                motive = [w1["price_range"], w3["price_range"], w5["price_range"]]
                if w3["price_range"] == min(motive):
                    rule_violations.append(f"نقض Q2 در موج {i+1}")
                if dirs[0] == "UP" and w4["end_price"] < w1["end_price"]:
                    rule_violations.append(f"نقض Q3 در موج {i+1}")

        return {
            "waves"          : waves,
            "total"          : len(waves),
            "up_count"       : len(up),
            "down_count"     : len(down),
            "avg_up_pct"     : avg_up_pct,
            "avg_down_pct"   : avg_down_pct,
            "avg_bars"       : avg_bars,
            "rule_violations": rule_violations,
        }

    def detect_wave_patterns(self, threshold_pct: float = 0.5) -> dict:
        waves = self.find_monowaves(threshold_pct)
        motive_idx     = []
        corrective_idx = []

        for i in range(len(waves) - 4):
            seg = waves[i: i + 5]
            dirs = [w["dir"] for w in seg]
            base = dirs[0]
            alt  = "DOWN" if base == "UP" else "UP"
            if dirs == [base, alt, base, alt, base]:
                motive_idx.append(i)

        for i in range(len(waves) - 2):
            seg = waves[i: i + 3]
            if seg[0]["dir"] != seg[1]["dir"] and seg[0]["dir"] == seg[2]["dir"]:
                corrective_idx.append(i)

        return {
            "motive_patterns"    : motive_idx,
            "corrective_patterns": corrective_idx,
            "motive_count"       : len(motive_idx),
            "corrective_count"   : len(corrective_idx),
        }

    def full_analysis(self, threshold_pct: float = 0.5) -> dict:
        trend_d  = self.detect_trend()
        rsi      = self.calc_rsi()
        macd_d   = self.calc_macd()
        fib      = self.calc_fib_levels()
        sr       = self.calc_sr_levels()
        mw_stats = self.monowave_stats(threshold_pct)
        patterns = self.detect_wave_patterns(threshold_pct)

        return {
            "تعداد_کندل"        : self.n,
            "بالاترین_قیمت"     : round(float(np.max(self.high)), 4),
            "پایین‌ترین_قیمت"   : round(float(np.min(self.low)),  4),
            "قیمت_فعلی"         : round(float(self.close[-1]),     4),
            "روند"              : trend_d["trend"],
            "MA20"              : round(trend_d["ma20"], 4),
            "MA50"              : round(trend_d["ma50"], 4),
            "RSI"               : rsi,
            "MACD"              : macd_d,
            "فیبوناچی"          : fib,
            "حمایت_مقاومت"      : sr,
            "مونوویو"           : mw_stats,
            "الگوها"            : patterns,
        }


# ══════════════════════════════════════════════════════════════════
# ساخت نمودار کندلی پیشرفته
# ══════════════════════════════════════════════════════════════════
def build_chart(df: pd.DataFrame, analysis: dict,
                show_waves: bool = True,
                show_fib: bool = False,
                show_sr: bool = True,
                threshold_pct: float = 0.5) -> go.Figure:
    """نمودار کندلی با لایه‌های اختیاری"""
    has_macd = analysis.get("MACD") is not None
    rows = 3 if has_macd else 2
    row_h = [0.55, 0.22, 0.23] if has_macd else [0.65, 0.35]

    fig = make_subplots(
        rows=rows, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=row_h,
    )

    # کندل‌ها
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["open"], high=df["high"],
        low=df["low"],   close=df["close"],
        name="قیمت",
        increasing_line_color="#4ade80",
        decreasing_line_color="#f87171",
        increasing_fillcolor="#4ade80",
        decreasing_fillcolor="#f87171",
    ), row=1, col=1)

    # میانگین متحرک
    if len(df) >= 20:
        ma20 = df["close"].rolling(20).mean()
        fig.add_trace(go.Scatter(
            x=df.index, y=ma20, name="MA20",
            line=dict(color="#f97316", width=1.2, dash="dot"),
        ), row=1, col=1)
    if len(df) >= 50:
        ma50 = df["close"].rolling(50).mean()
        fig.add_trace(go.Scatter(
            x=df.index, y=ma50, name="MA50",
            line=dict(color="#38bdf8", width=1.2, dash="dot"),
        ), row=1, col=1)

    # امواج مونوویو
    if show_waves:
        mw_stats = analysis.get("مونوویو", {})
        waves = mw_stats.get("waves", [])
        x_vals, y_vals = [], []
        for w in waves:
            si = min(int(w["start"]), len(df) - 1)
            ei = min(int(w["end"]),   len(df) - 1)
            x_vals.extend([df.index[si], df.index[ei], None])
            y_vals.extend([w["start_price"], w["end_price"], None])

        if x_vals:
            fig.add_trace(go.Scatter(
                x=x_vals, y=y_vals,
                mode="lines",
                line=dict(color="rgba(167,139,250,0.7)", width=1.5),
                name="مونوویو",
            ), row=1, col=1)

    # فیبوناچی
    if show_fib:
        fibs = analysis.get("فیبوناچی", {})
        key_fibs = ["0.382", "0.5", "0.618"]
        colors_f  = ["#fbbf24", "#f97316", "#ef4444"]
        for fk, fc in zip(key_fibs, colors_f):
            val = fibs.get(fk)
            if val:
                fig.add_hline(
                    y=val, line_dash="dot",
                    line=dict(color=fc, width=1),
                    annotation_text=f"Fib {fk}",
                    annotation_font=dict(color=fc, size=10),
                    row=1, col=1
                )

    # حمایت و مقاومت
    if show_sr:
        sr = analysis.get("حمایت_مقاومت", {})
        for rv in sr.get("resistance", [])[:2]:
            fig.add_hline(
                y=rv, line_dash="dash",
                line=dict(color="rgba(248,113,113,0.5)", width=1),
                row=1, col=1
            )
        for sv in sr.get("support", [])[:2]:
            fig.add_hline(
                y=sv, line_dash="dash",
                line=dict(color="rgba(74,222,128,0.5)", width=1),
                row=1, col=1
            )

    # RSI
    if len(df) > 14:
        delta = df["close"].diff()
        gain  = delta.where(delta > 0, 0.0)
        loss  = -delta.where(delta < 0, 0.0)
        ag    = gain.rolling(14).mean()
        al    = loss.rolling(14).mean()
        rsi   = 100 - (100 / (1 + ag / al))

        fig.add_trace(go.Scatter(
            x=df.index, y=rsi, name="RSI",
            line=dict(color="#a78bfa", width=1.4),
        ), row=2, col=1)
        fig.add_hline(y=70, line_dash="dot", line_color="rgba(248,113,113,0.5)", row=2, col=1)
        fig.add_hline(y=30, line_dash="dot", line_color="rgba(74,222,128,0.5)",  row=2, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color="rgba(100,116,139,0.4)", row=2, col=1)

    # MACD
    if has_macd and rows == 3:
        series = df["close"]
        ema12  = series.ewm(span=12, adjust=False).mean()
        ema26  = series.ewm(span=26, adjust=False).mean()
        macd   = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        hist   = macd - signal

        colors_h = ["#4ade80" if v >= 0 else "#f87171" for v in hist]
        fig.add_trace(go.Bar(x=df.index, y=hist, name="MACD Hist", marker_color=colors_h), row=3, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=macd,   name="MACD",   line=dict(color="#38bdf8", width=1.2)), row=3, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=signal, name="Signal", line=dict(color="#f97316", width=1.2)), row=3, col=1)

    fig.update_layout(
        height=700,
        template="plotly_dark",
        paper_bgcolor="#070b14",
        plot_bgcolor="#070b14",
        font=dict(family="Vazirmatn", color="#94a3b8", size=11),
        showlegend=True,
        legend=dict(
            bgcolor="rgba(13,20,34,0.8)",
            bordercolor="#1e293b",
            borderwidth=1,
            font=dict(size=10),
        ),
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=30, b=10),
    )
    fig.update_yaxes(gridcolor="#1e293b", zerolinecolor="#1e293b")
    fig.update_xaxes(gridcolor="#1e293b")

    return fig


# ══════════════════════════════════════════════════════════════════
# بارگذاری فایل داده
# ══════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_data(file_bytes: bytes, filename: str) -> pd.DataFrame:
    """بارگذاری و استانداردسازی فایل CSV / Excel"""
    import io
    
    # بارگذاری فایل
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_bytes))
        else:
            df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
    except Exception as e:
        raise ValueError(f"خطا در خواندن فایل: {e}")
    
    if df.empty:
        raise ValueError("فایل خالی است")
    
    # نرمال‌سازی نام ستون‌ها
    df.columns = [str(col).strip().lower() for col in df.columns]
    
    # تشخیص ستون‌ها
    close_col = None
    for col in df.columns:
        if col in ["close", "بسته", "close price", "adj close", "adj_close", "قیمت بسته"]:
            close_col = col
            break
    
    if close_col is None:
        raise ValueError("ستون قیمت بسته شدن (Close) یافت نشد")
    
    open_col = None
    high_col = None
    low_col = None
    volume_col = None
    date_col = None
    
    for col in df.columns:
        if col in ["open", "باز", "open price", "قیمت باز"]:
            open_col = col
        elif col in ["high", "بالاترین", "high price", "بیشترین"]:
            high_col = col
        elif col in ["low", "پایین‌ترین", "low price", "کمترین"]:
            low_col = col
        elif col in ["volume", "حجم", "vol"]:
            volume_col = col
        elif col in ["date", "time", "datetime", "تاریخ"]:
            date_col = col
    
    # ساخت دیتافریم نهایی
    result = pd.DataFrame()
    result["close"] = pd.to_numeric(df[close_col], errors="coerce")
    
    if open_col:
        result["open"] = pd.to_numeric(df[open_col], errors="coerce")
    else:
        result["open"] = result["close"].copy()
    
    if high_col:
        result["high"] = pd.to_numeric(df[high_col], errors="coerce")
    else:
        result["high"] = result["close"].copy()
    
    if low_col:
        result["low"] = pd.to_numeric(df[low_col], errors="coerce")
    else:
        result["low"] = result["close"].copy()
    
    if volume_col:
        result["volume"] = pd.to_numeric(df[volume_col], errors="coerce").fillna(0)
    else:
        result["volume"] = 0
    
    result = result.dropna(subset=["close"])
    result["open"] = result["open"].fillna(result["close"])
    result["high"] = result["high"].fillna(result["close"])
    result["low"] = result["low"].fillna(result["close"])
    
    # تنظیم ایندکس
    if date_col:
        try:
            result["date"] = pd.to_datetime(df[date_col], errors="coerce")
            result = result.dropna(subset=["date"])
            result = result.set_index("date")
            result = result.sort_index()
        except Exception:
            result = result.reset_index(drop=True)
    else:
        result = result.reset_index(drop=True)
    
    for col in ["open", "high", "low", "close"]:
        result[col] = result[col].astype(float)
    result["volume"] = result["volume"].astype(float)
    
    return result


# ══════════════════════════════════════════════════════════════════
# رابط کاربری اصلی
# ══════════════════════════════════════════════════════════════════
def main():
    # هدر
    st.markdown("""
    <div class="nw-header">
        <h1>〜 استادی در امواج الیوت</h1>
        <h3>سبک نئوویو · گلن نیلی · پوشش کامل ۳۶ فصل</h3>
        <p>هسته اصلی | ماژول‌های فصل از پوشه chapters/ بارگذاری می‌شوند</p>
        <p style="color: #38bdf8; font-size: 0.85rem;">✅ پشتیبانی از وابستگی بین فصل‌ها · گزارش خطای کامل</p>
    </div>
    """, unsafe_allow_html=True)

    # سایدبار
    with st.sidebar:
        st.markdown("### 📁 داده ورودی")
        uploaded = st.file_uploader(
            "فایل Excel یا CSV",
            type=["csv", "xlsx", "xls"],
            help="ستون‌های مورد نیاز: Date, Open, High, Low, Close"
        )
        st.markdown('<hr class="nw-divider">', unsafe_allow_html=True)

        if uploaded:
            st.markdown("### ⚙️ تنظیمات")

            tf_map = {"روزانه (D)": "D", "هفتگی (W)": "W", "ماهانه (M)": "ME"}
            sel_tf = st.selectbox("تایم‌فریم", list(tf_map.keys()))

            lookback = st.slider("تعداد کندل آخر", 50, 5000, 500, 50)
            sensitivity = st.slider(
                "حساسیت مونوویو (%)", 0.1, 3.0, 0.5, 0.1,
                help="مقدار کمتر = موج‌های کوچک‌تر تشخیص داده می‌شود"
            )

            st.markdown('<hr class="nw-divider">', unsafe_allow_html=True)
            st.markdown("### 📚 فصل‌ها")

            # نمایش وضعیت فصل‌ها
            chapter_mgr = ChapterManager()
            
            # آمار ارتقا
            upgraded_count = sum(1 for info in chapter_mgr.chapters.values() if info.is_upgraded)
            loaded_count = sum(1 for info in chapter_mgr.chapters.values() if info.is_loaded)
            error_count = len(chapter_mgr._load_errors)

            st.markdown(f"""
            <div style="display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap;">
              <span class="nw-badge green">✓ ارتقا: {upgraded_count}</span>
              <span class="nw-badge orange">⏳ TODO: {36 - upgraded_count}</span>
              <span class="nw-badge blue">📦 بارگذاری: {loaded_count}</span>
              {f'<span class="nw-badge red">❌ خطا: {error_count}</span>' if error_count > 0 else ''}
            </div>
            """, unsafe_allow_html=True)

            # نمایش خطاهای بارگذاری
            if error_count > 0:
                with st.expander(f"⚠️ خطاهای بارگذاری ({error_count})", expanded=False):
                    for num, err in chapter_mgr._load_errors.items():
                        st.markdown(f"""
                        <div class="nw-error">
                            <div class="title">❌ فصل {num:02d}: {CHAPTER_TITLES.get(num, '')}</div>
                            <div class="detail">{err}</div>
                        </div>
                        """, unsafe_allow_html=True)

            sel_chapters = st.multiselect(
                "فصل‌های هدف",
                options=[n for n, _, _ in CHAPTERS_LIST],
                default=[n for n, _, _ in CHAPTERS_LIST if n <= 14],  # پیش‌فرض فصل‌های ارتقا یافته
                format_func=lambda x: f"{x:02d} · {CHAPTER_TITLES.get(x, '')} {'⭐' if chapter_mgr.is_upgraded(x) else '📄'}"
            )

            # نمایش وابستگی‌های فصل انتخاب‌شده
            if sel_chapters:
                with st.expander("📊 وابستگی‌های فصل‌ها", expanded=False):
                    for num in sel_chapters:
                        deps = chapter_mgr.get_dependencies(num)
                        deps_str = ", ".join(f"{d:02d}" for d in deps) if deps else "بدون وابستگی"
                        st.markdown(f"• فصل {num:02d} ← {deps_str}")

            st.markdown('<hr class="nw-divider">', unsafe_allow_html=True)

            if st.button("🔄 بارگذاری مجدد ماژول‌ها", use_container_width=True):
                with st.spinner("در حال بارگذاری مجدد..."):
                    chapter_mgr.reload()
                    st.cache_data.clear()
                    st.rerun()

    # صفحه بدون فایل
    if not uploaded:
        _render_welcome()
        return

    # بارگذاری داده
    try:
        raw_bytes = uploaded.read()
        df_full = load_data(raw_bytes, uploaded.name)
    except Exception as e:
        st.error(f"❌ خطا در بارگذاری فایل: {e}")
        return

    # ریسمپل
    tf_code = tf_map[sel_tf]
    if tf_code in ["W", "ME"] and isinstance(df_full.index, pd.DatetimeIndex):
        agg = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
        df_full = df_full.resample(tf_code).agg(agg).dropna()

    df = df_full.tail(lookback).copy()

    st.success(f"✅ {len(df):,} کندل بارگذاری شد · {sel_tf} · {uploaded.name}")

    # تحلیل‌گر نمودار
    analyzer = ChartAnalyzer(df)
    analysis = analyzer.full_analysis(sensitivity)

    # تب‌های اصلی
    tab_overview, tab_chart, tab_chapters, tab_report, tab_settings = st.tabs([
        "📊 نمای کلی",
        "📈 نمودار",
        "📚 تحلیل فصل‌ها",
        "📋 گزارش کامل",
        "⚙️ تنظیمات",
    ])

    # تب ۱: نمای کلی
    with tab_overview:
        _render_overview(df, analysis, sensitivity)

    # تب ۲: نمودار
    with tab_chart:
        _render_chart(df, analysis, sensitivity)

    # تب ۳: تحلیل فصل‌ها (با پشتیبانی از وابستگی)
    with tab_chapters:
        _render_chapters_with_deps(df, analysis, sel_chapters if sel_chapters else [n for n, _, _ in CHAPTERS_LIST])

    # تب ۴: گزارش کامل
    with tab_report:
        _render_report(df, sel_chapters if sel_chapters else [n for n, _, _ in CHAPTERS_LIST])

    # تب ۵: تنظیمات
    with tab_settings:
        _render_settings()


# ══════════════════════════════════════════════════════════════════
# رندر نمای کلی
# ══════════════════════════════════════════════════════════════════
def _render_overview(df: pd.DataFrame, analysis: dict, sensitivity: float):
    c1, c2, c3, c4, c5 = st.columns(5)
    curr = analysis["قیمت_فعلی"]
    prev = float(df["close"].iloc[-2]) if len(df) > 1 else curr
    chg  = round((curr - prev) / prev * 100, 2) if prev != 0 else 0

    mw   = analysis["مونوویو"]
    rsi  = analysis.get("RSI")
    trend = analysis["روند"]

    with c1:
        cls = "up" if chg >= 0 else "down"
        arrow = "▲" if chg >= 0 else "▼"
        st.markdown(f"""<div class="nw-metric {cls}">
            <div class="val">{curr:,.2f}</div>
            <div class="lbl">💰 قیمت فعلی {arrow}{abs(chg)}%</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        t_cls = "up" if trend == "صعودی" else ("down" if trend == "نزولی" else "")
        t_ico = "📈" if trend == "صعودی" else ("📉" if trend == "نزولی" else "🔄")
        st.markdown(f"""<div class="nw-metric {t_cls}">
            <div class="val">{trend}</div>
            <div class="lbl">{t_ico} روند کلی</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""<div class="nw-metric">
            <div class="val">{mw['total']}</div>
            <div class="lbl">〜 مونوویو (حساسیت {sensitivity}%)</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        rsi_cls = "warn" if rsi and 40 <= rsi <= 60 else ("down" if rsi and rsi > 70 else ("up" if rsi and rsi < 30 else ""))
        st.markdown(f"""<div class="nw-metric {rsi_cls}">
            <div class="val">{rsi if rsi else 'N/A'}</div>
            <div class="lbl">📊 RSI(14)</div>
        </div>""", unsafe_allow_html=True)

    with c5:
        pats = analysis.get("الگوها", {})
        st.markdown(f"""<div class="nw-metric">
            <div class="val">{pats.get('motive_count', 0)} / {pats.get('corrective_count', 0)}</div>
            <div class="lbl">⚡ شتابدار / 🔄 اصلاحی</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="nw-divider">', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="nw-card"><h4>〜 آمار مونوویو</h4>', unsafe_allow_html=True)
        items = [
            ("صعودی", mw["up_count"]),
            ("نزولی", mw["down_count"]),
            ("میانگین % صعود", f"{mw['avg_up_pct']}%"),
            ("میانگین % نزول", f"{mw['avg_down_pct']}%"),
            ("میانگین طول (کندل)", mw["avg_bars"]),
        ]
        for k, v in items:
            st.markdown(f"""<div class="nw-result-item">
                <span class="nw-result-key">{k}</span>
                <span class="nw-result-val">{v}</span>
            </div>""", unsafe_allow_html=True)

        violations = mw.get("rule_violations", [])
        if violations:
            st.markdown(f'<span class="nw-badge red">⚠ {len(violations)} نقض قانون</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="nw-badge green">✓ بدون نقض قانون</span>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="nw-card"><h4>📐 نسبت‌های فیبوناچی (آخرین ۱۰۰ کندل)</h4>', unsafe_allow_html=True)
        fib = analysis.get("فیبوناچی", {})
        key_fib = ["0.0", "0.236", "0.382", "0.5", "0.618", "0.764", "1.0", "1.618"]
        for fk in key_fib:
            val = fib.get(fk, "─")
            badge = "orange" if fk in ["0.618", "1.618"] else "blue"
            st.markdown(f"""<div class="nw-result-item">
                <span class="nw-result-key"><span class="nw-badge {badge}">{fk}</span></span>
                <span class="nw-result-val">{val}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col_c, col_d = st.columns(2)
    sr = analysis.get("حمایت_مقاومت", {})

    with col_c:
        st.markdown('<div class="nw-card"><h4>🔴 سطوح مقاومت</h4>', unsafe_allow_html=True)
        for rv in sr.get("resistance", [])[:4]:
            st.markdown(f"""<div class="nw-result-item">
                <span class="nw-result-key">مقاومت</span>
                <span class="nw-result-val" style="color:#f87171">{rv:,.4f}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_d:
        st.markdown('<div class="nw-card"><h4>🟢 سطوح حمایت</h4>', unsafe_allow_html=True)
        for sv in sr.get("support", [])[:4]:
            st.markdown(f"""<div class="nw-result-item">
                <span class="nw-result-key">حمایت</span>
                <span class="nw-result-val" style="color:#4ade80">{sv:,.4f}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# رندر نمودار
# ══════════════════════════════════════════════════════════════════
def _render_chart(df: pd.DataFrame, analysis: dict, sensitivity: float):
    st.markdown('<div class="nw-card"><h4>📈 نمودار کندلی پیشرفته</h4>', unsafe_allow_html=True)

    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        show_waves = st.toggle("〜 امواج مونوویو", value=True)
    with cc2:
        show_fib = st.toggle("📐 سطوح فیبوناچی", value=False)
    with cc3:
        show_sr = st.toggle("⚡ حمایت/مقاومت", value=True)

    fig = build_chart(df, analysis, show_waves, show_fib, show_sr, sensitivity)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("〜 جدول مونوویوهای اخیر"):
        waves = analysis["مونوویو"]["waves"][-30:]
        if waves:
            wave_df = pd.DataFrame([{
                "#"            : i + 1,
                "جهت"          : w["dir"],
                "شروع"         : round(w["start_price"], 4),
                "پایان"        : round(w["end_price"],   4),
                "دامنه"        : round(w["price_range"],  4),
                "%"            : f"{w['pct']}%",
                "کندل"         : w["bars"],
            } for i, w in enumerate(waves)])
            st.dataframe(wave_df, use_container_width=True, height=300)


# ══════════════════════════════════════════════════════════════════
# رندر تحلیل فصل‌ها با پشتیبانی از وابستگی
# ══════════════════════════════════════════════════════════════════
def _render_chapters_with_deps(df: pd.DataFrame, analysis: dict, sel_chapters: list[int]):
    chapter_mgr = ChapterManager()

    # انتخاب تک فصل
    st.markdown('<div class="nw-card"><h4>📚 تحلیل تک فصل با وابستگی‌ها</h4>', unsafe_allow_html=True)

    ch_col1, ch_col2, ch_col3 = st.columns([2, 1, 1])
    with ch_col1:
        chosen = st.selectbox(
            "انتخاب فصل",
            options=[n for n, _, _ in CHAPTERS_LIST],
            format_func=lambda x: f"فصل {x:02d} · {CHAPTER_TITLES.get(x, '')} {'⭐' if chapter_mgr.is_upgraded(x) else '📄'}"
        )
    with ch_col2:
        info = chapter_mgr.chapters.get(chosen)
        status = "✅ ارتقا یافته" if info and info.is_upgraded else "⏳ پیش‌فرض"
        st.markdown(f"<br><span class='nw-badge {'green' if info and info.is_upgraded else 'orange'}'>{status}</span>", unsafe_allow_html=True)
    with ch_col3:
        deps = chapter_mgr.get_dependencies(chosen)
        deps_str = ", ".join(f"{d:02d}" for d in deps) if deps else "بدون"
        st.markdown(f"<br><span class='nw-badge blue'>⬅ {deps_str}</span>", unsafe_allow_html=True)

    if st.button(f"▶ اجرای فصل {chosen:02d} با وابستگی‌ها", use_container_width=True):
        with st.spinner(f"در حال اجرای فصل {chosen} و وابستگی‌های آن..."):
            logger_obj = ResultsLogger()
            
            # اجرای وابستگی‌ها
            deps = chapter_mgr.get_dependencies(chosen)
            dep_results = {}
            for dep in deps:
                if chapter_mgr.is_loaded(dep):
                    dep_result = chapter_mgr.run(dep, df, logger_obj, None)
                    if "خطا" not in dep_result:
                        dep_results[f"chapter_{dep}"] = dep_result
                        logger_obj.add_section(f"✅ وابستگی فصل {dep} اجرا شد", level=2)
            
            # اجرای فصل اصلی
            result = chapter_mgr.run(chosen, df, logger_obj, dep_results)

        if "خطا" in result:
            st.error(f"❌ {result['خطا']}")
            if "traceback" in result:
                with st.expander("جزئیات خطا"):
                    st.code(result["traceback"])
        else:
            st.markdown(f"**نتایج فصل {chosen:02d} · {CHAPTER_TITLES.get(chosen, '')}**")
            
            # نمایش وابستگی‌های استفاده‌شده
            if dep_results:
                st.markdown("**📊 داده‌های استفاده‌شده از وابستگی‌ها:**")
                for dep_num in deps:
                    if dep_num in dep_results:
                        dep_res = dep_results[f"chapter_{dep_num}"]
                        st.markdown(f"• فصل {dep_num:02d}: {dep_res.get('وضعیت', 'نامشخص')}")
            
            st.markdown("**📋 نتایج تحلیل:**")
            for k, v in result.items():
                if k not in ["تفسیر_نهایی", "error", "traceback"]:
                    if isinstance(v, (dict, list)):
                        st.markdown(f"""<div class="nw-result-item">
                            <span class="nw-result-key">{k}</span>
                            <span class="nw-result-val">{json.dumps(v, ensure_ascii=False, default=str)[:100]}...</span>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div class="nw-result-item">
                            <span class="nw-result-key">{k}</span>
                            <span class="nw-result-val">{v}</span>
                        </div>""", unsafe_allow_html=True)
            
            if "تفسیر_نهایی" in result:
                with st.expander("📖 تفسیر کامل", expanded=True):
                    st.text(result["تفسیر_نهایی"])

    st.markdown("</div>", unsafe_allow_html=True)

    # وضعیت همه فصل‌ها
    st.markdown('<hr class="nw-divider">', unsafe_allow_html=True)
    st.markdown("#### وضعیت همه فصل‌ها با وابستگی‌ها")

    cols = st.columns(4)
    for idx, (num, title, deps) in enumerate(CHAPTERS_LIST):
        info = chapter_mgr.chapters.get(num)
        is_up = info and info.is_upgraded
        is_loaded = info and info.is_loaded
        selected = num in sel_chapters
        deps_str = ", ".join(str(d) for d in deps) if deps else "بدون"
        
        with cols[idx % 4]:
            badge = "🟢" if is_up else "🟡" if is_loaded else "🔴"
            dim = "" if selected else "opacity:0.5;"
            st.markdown(f"""<div class="nw-chapter-row" style="{dim}">
                <span class="nw-chapter-num">{num:02d}</span>
                <span class="nw-chapter-name" style="font-size:0.7rem;">{title[:15]}...</span>
                <span class="nw-chapter-ok" style="font-size:0.65rem;">{badge}</span>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# رندر گزارش کامل
# ══════════════════════════════════════════════════════════════════
def _render_report(df: pd.DataFrame, sel_chapters: list[int]):
    st.markdown('<div class="nw-card"><h4>📋 گزارش کامل با وابستگی‌ها</h4>', unsafe_allow_html=True)
    st.info(f"فصل‌های انتخاب‌شده: {len(sel_chapters)} از ۳۶")

    chapter_mgr = ChapterManager()

    # نمایش ترتیب اجرا
    order = chapter_mgr.get_topological_order(sel_chapters)
    st.markdown("**🔄 ترتیب اجرای فصل‌ها (بر اساس وابستگی):**")
    st.markdown(" → ".join(f"{num:02d}" for num in order))

    if st.button("🚀 اجرای تحلیل کامل", use_container_width=True):
        logger_obj = ResultsLogger()
        
        progress = st.progress(0)
        status_txt = st.empty()
        error_log = []
        
        def on_progress(done, total, num):
            progress.progress(done / total)
            status_txt.markdown(
                f"<small>فصل {num:02d} · {CHAPTER_TITLES.get(num, '')} ({done}/{total})</small>",
                unsafe_allow_html=True
            )

        all_results = chapter_mgr.run_selected(df, sel_chapters, logger_obj, on_progress)

        progress.empty()
        status_txt.empty()

        # خلاصه
        ok = sum(1 for r in all_results.values() if "خطا" not in r)
        fail = len(all_results) - ok
        st.markdown(f"""
        <div style="display:flex;gap:10px;margin:10px 0;">
          <span class="nw-badge green">✓ موفق: {ok}</span>
          <span class="nw-badge red">✗ خطا: {fail}</span>
        </div>""", unsafe_allow_html=True)

        # نمایش خطاها
        if fail > 0:
            with st.expander(f"❌ خطاها ({fail})", expanded=True):
                for num, result in all_results.items():
                    if "خطا" in result:
                        st.markdown(f"""
                        <div class="nw-error">
                            <div class="title">❌ فصل {num:02d}: {CHAPTER_TITLES.get(num, '')}</div>
                            <div class="detail">{result['خطا']}</div>
                        </div>
                        """, unsafe_allow_html=True)

        # ذخیره و دانلود
        report_path = logger_obj.save()
        with open(report_path, "rb") as f:
            st.download_button(
                "📥 دانلود گزارش TXT",
                data=f,
                file_name=report_path,
                mime="text/plain",
                use_container_width=True,
            )

        # پیش‌نمایش
        with open(report_path, "r", encoding="utf-8") as f:
            preview = f.read()
        with st.expander("👁 پیش‌نمایش گزارش", expanded=False):
            st.text(preview[:5000] + ("…" if len(preview) > 5000 else ""))

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# رندر تنظیمات
# ══════════════════════════════════════════════════════════════════
def _render_settings():
    st.markdown('<div class="nw-card"><h4>⚙️ راهنمای سیستم وابستگی‌ها</h4>', unsafe_allow_html=True)

    st.markdown("""
    **ساختار interface هر فصل:**
    - فایل: `chapters/chapter_XX.py`
    - تابع: `analyze(data, logger, context)` → `dict`
    - `data`: DataFrame با ستون‌های `open, high, low, close, volume`
    - `logger`: آبجکت `ResultsLogger` (اختیاری)
    - `context`: دیکشنری نتایج فصل‌های قبلی (بر اساس وابستگی‌ها)

    **سیستم وابستگی:**
    - هر فصل می‌تواند به نتایج فصل‌های دیگر وابسته باشد
    - وابستگی‌ها در `CHAPTERS_LIST` تعریف می‌شوند
    - ترتیب اجرا به صورت توپولوژیک انجام می‌شود
    - نتایج هر فصل در `context` برای استفاده در دسترس است
    """)

    st.markdown("**مثال استفاده از context در یک فصل:**")
    st.code('''
def analyze(data, logger=None, context=None):
    # دریافت نتایج فصل‌های وابسته
    if context and "chapter_2" in context:
        fractal_data = context["chapter_2"]
        waves = fractal_data.get("تعداد_تک‌موج", 0)
    
    # تحلیل با استفاده از داده‌های وابسته
    # ...
    return results
    ''', language="python")

    st.markdown('<hr class="nw-divider">', unsafe_allow_html=True)
    st.markdown("**وضعیت فعلی ماژول‌ها:**")

    chapter_mgr = ChapterManager()
    rows = []
    for num, title, deps in CHAPTERS_LIST:
        info = chapter_mgr.chapters.get(num)
        rows.append({
            "فصل": f"{num:02d}",
            "عنوان": title[:30] + "..." if len(title) > 30 else title,
            "وضعیت": "✅ ارتقا" if info and info.is_upgraded else "⏳ پیش‌فرض" if info and info.is_loaded else "❌ خطا",
            "بارگذاری": "✓" if info and info.is_loaded else "✗",
            "وابستگی": ", ".join(f"{d:02d}" for d in deps) if deps else "بدون",
            "زمان": f"{info.execution_time:.2f}s" if info and info.execution_time > 0 else "─",
        })
    
    st.dataframe(pd.DataFrame(rows), use_container_width=True, height=400)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# صفحه خوشامدگویی
# ══════════════════════════════════════════════════════════════════
def _render_welcome():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="nw-card">
            <h4>📁 فرمت فایل ورودی</h4>
            <div class="nw-result-item"><span class="nw-result-key">Date</span><span class="nw-result-val">تاریخ (میلادی)</span></div>
            <div class="nw-result-item"><span class="nw-result-key">Open</span><span class="nw-result-val">قیمت باز شدن</span></div>
            <div class="nw-result-item"><span class="nw-result-key">High</span><span class="nw-result-val">بالاترین قیمت</span></div>
            <div class="nw-result-item"><span class="nw-result-key">Low</span><span class="nw-result-val">پایین‌ترین قیمت</span></div>
            <div class="nw-result-item"><span class="nw-result-key">Close</span><span class="nw-result-val">قیمت بسته شدن ✱ اجباری</span></div>
            <div class="nw-result-item"><span class="nw-result-key">Volume</span><span class="nw-result-val">حجم (اختیاری)</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="nw-card">
            <h4>🚀 قابلیت‌های هسته</h4>
            <div class="nw-result-item"><span class="nw-result-key">ساختار فراکتال</span><span class="nw-badge green">✓ آماده</span></div>
            <div class="nw-result-item"><span class="nw-result-key">۳ قانون نقض‌ناپذیر</span><span class="nw-badge green">✓ آماده</span></div>
            <div class="nw-result-item"><span class="nw-result-key">نسبت‌های فیبوناچی</span><span class="nw-badge green">✓ آماده</span></div>
            <div class="nw-result-item"><span class="nw-result-key">حمایت/مقاومت</span><span class="nw-badge green">✓ آماده</span></div>
            <div class="nw-result-item"><span class="nw-result-key">RSI + MACD</span><span class="nw-badge green">✓ آماده</span></div>
            <div class="nw-result-item"><span class="nw-result-key">وابستگی بین فصل‌ها</span><span class="nw-badge green">✓ فعال</span></div>
            <div class="nw-result-item"><span class="nw-result-key">گزارش خطای کامل</span><span class="nw-badge green">✓ فعال</span></div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()