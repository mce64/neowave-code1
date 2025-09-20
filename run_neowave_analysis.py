# ================= run_neowave_analysis.py =================
"""
🌊 سیستم جامع تحلیل NEOWave به روش گلن نیلی
نسخه کامل و حرفه‌ای با مدیریت سرمایه پیشرفته

برای اجرا:
python run_neowave_analysis.py
"""

import sys
import os
import asyncio
from datetime import datetime
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication
import logging
from typing import Dict, List, Optional, Any

# تنظیم مسیرها
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all modules
from config import Config
from core.data_fetcher import DataFetcher
from modules.elliott_basics import ElliottBasics
from modules.fractal_structure import FractalStructure
from modules.impulse_waves import ImpulseWaveAnalyzer
from modules.corrective_waves import CorrectiveWaveAnalyzer
from modules.triangle_pattern import TriangleAnalyzer
from modules.diametric_pattern import DiametricAnalyzer
from modules.symmetric_pattern import AdvancedSymmetricAnalyzer
from modules.ratio_analysis import RatioAnalyzer, ValidationLevel
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from scipy import stats, optimize
from scipy.spatial.distance import euclidean
from modules.channeling import ChannelAnalyzer
from modules.trend_lines import TrendLineAnalyzer
from modules.time_analysis import AdvancedTimeAnalyzer  # تغییر داده شده از TimeAnalyzer به AdvancedTimeAnalyzer
from modules.complexity import ComplexityAnalyzer
from modules.trading_strategy import AdvancedNEOWaveTradingStrategy, AdvancedTradingSignal, SignalType, MarketRegime, ConfidenceLevel
from modules.money_management import AdvancedMoneyManager, PositionSizeMethod, RiskModelType, PortfolioOptimization
from ui.main_window import MainWindow

# تنظیم لاگینگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('neowave_analysis.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NEOWaveSystem:
    """سیستم اصلی تحلیل NEOWave با مدیریت سرمایه پیشرفته"""
    
    def __init__(self, initial_capital: float = 10000):
        """راه‌اندازی سیستم"""
        logger.info("🚀 شروع راه‌اندازی سیستم NEOWave...")
        
        self.config = Config()
        self.initial_capital = initial_capital
        self.data_fetcher = None
        self.current_data = None
        self.analysis_results = {}
        self.market_data_cache = {}
        
        # ماژول‌های تحلیل
        self.elliott_analyzer = None
        self.fractal_analyzer = None
        self.impulse_analyzer = None
        self.corrective_analyzer = None
        self.triangle_analyzer = None
        self.diametric_analyzer = None
        self.symmetric_analyzer = None
        self.ratio_analyzer = None
        self.channel_analyzer = None
        self.trendline_analyzer = None
        self.time_analyzer = None
        self.complexity_analyzer = None
        self.trading_strategy = None
        
        # سیستم مدیریت سرمایه پیشرفته
        self.money_manager = AdvancedMoneyManager(
            initial_capital=initial_capital,
            config=self._get_money_management_config()
        )
        
        # تنظیمات معاملاتی
        self.auto_trading_enabled = False
        self.risk_management_active = True
        self.real_time_monitoring = True
        
        # ذخیره تاریخچه سیگنال‌ها
        self.signals_history = []
        self.performance_tracking = {
            'total_signals': 0,
            'successful_signals': 0,
            'failed_signals': 0,
            'average_confidence': 0.0,
            'best_signal': None,
            'worst_signal': None
        }
        
        logger.info("✅ سیستم با موفقیت راه‌اندازی شد")
        logger.info(f"💰 سرمایه اولیه: ${initial_capital:,.2f}")
        
    def _get_money_management_config(self) -> Dict:
        """تنظیمات مدیریت سرمایه"""
        return {
            'max_risk_per_trade': 0.015,                # 1.5% ریسک برای هر معامله
            'max_portfolio_risk': 0.05,                 # 5% ریسک کل پرتفویو
            'max_correlation_exposure': 0.3,            # 30% حداکثر در دارایی‌های همبسته
            'max_positions': 4,                         # حداکثر 4 پوزیشن همزمان
            'max_leverage': 1.0,                        # بدون اهرم
            'rebalance_threshold': 0.05,                # 5% انحراف برای rebalance
            'emergency_stop_loss': 0.12,                # 12% stop loss اضطراری
            'volatility_lookback': 20,                  # 20 روز برای محاسبه نوسان
            'correlation_lookback': 50,                 # 50 روز برای همبستگی
            'position_size_method': PositionSizeMethod.MACHINE_LEARNING,
            'risk_model': RiskModelType.HISTORICAL_VAR,
            'optimization_method': PortfolioOptimization.RISK_PARITY,
            'regime_sensitivity': 0.75,                 # حساسیت تشخیص رژیم
            'ml_enabled': True,                         # فعال‌سازی ML
            'stress_test_enabled': True,                # فعال‌سازی stress test
            'real_time_monitoring': True                # مانیتورینگ real-time
        }
    
    def _get_symmetric_analyzer_config(self) -> Dict:
        """تنظیمات تحلیلگر پیشرفته سیمتریک"""
        return {
            'min_pattern_length': 150,
            'max_pattern_length': 1000,
            'symmetry_tolerance': 0.03,           # تحمل 3% برای تقارن
            'confidence_threshold': 0.75,        # حد آستانه اعتماد 75%
            'ml_enabled': True,                  # فعال‌سازی machine learning
            'statistical_analysis': True,        # تحلیل آماری پیشرفته
            'geometric_analysis': True,          # تحلیل هندسی
            'multi_timeframe': False,            # تحلیل چندگانه timeframe
            'advanced_validation': True,         # اعتبارسنجی پیشرفته
            'harmonic_analysis': True,           # تحلیل هارمونیک
            'fractal_integration': True,         # ادغام با تحلیل فرکتال
            'fibonacci_validation': True,        # اعتبارسنجی فیبوناچی
            'volume_analysis': True,             # تحلیل حجم
            'momentum_analysis': True,           # تحلیل مومنتوم
            'projection_accuracy': 'high',      # دقت بالا در پروژکشن‌ها
            'risk_assessment': True,             # ارزیابی ریسک
            'market_context': True               # تحلیل محیط بازار
        }
    
    def _get_advanced_trading_strategy_config(self) -> Dict:
        """تنظیمات استراتژی معاملاتی پیشرفته"""
        return {
            'risk_per_trade': 0.02,
            'max_positions': 3,
            'min_rr_ratio': 2.0,
            'confidence_threshold': 0.6,
            'ml_enabled': True,
            'multi_timeframe': True,
            'adaptive_sizing': True,
            'dynamic_stops': True,
            'regime_filtering': True,
            'correlation_filtering': True,
            'volume_confirmation': True,
            'sentiment_weight': 0.3,
            'technical_weight': 0.4,
            'wave_weight': 0.3,
            'advanced_risk_management': True,
            'kelly_criterion': True,
            'position_scaling': True,
            'market_microstructure': True,
            'regime_adaptation': True,
            'volatility_targeting': True
        }
        
    def initialize_exchange_connection(self, api_key: str = "", secret_key: str = ""):
        """اتصال به صرافی"""
        try:
            logger.info("🔗 در حال اتصال به صرافی LBank...")
            self.data_fetcher = DataFetcher(api_key, secret_key)
            logger.info("✅ اتصال به صرافی برقرار شد")
            return True
        except Exception as e:
            logger.error(f"❌ خطا در اتصال: {e}")
            return False
            
    def fetch_market_data(self, symbol: str = "BTC/USDT", 
                         timeframe: str = "1h", 
                         limit: int = 500):
        """دریافت داده‌های بازار"""
        try:
            logger.info(f"📊 دریافت داده‌های {symbol} در تایم‌فریم {timeframe}...")
            
            if not self.data_fetcher:
                self.data_fetcher = DataFetcher()
                
            self.current_data = self.data_fetcher.fetch_ohlcv(symbol, timeframe, limit)
            
            if self.current_data.empty:
                logger.warning("⚠️ داده‌ای دریافت نشد")
                return None
                
            # اضافه کردن metadata برای استراتژی پیشرفته
            self.current_data.symbol = symbol
            self.current_data.timeframe = timeframe
                
            # ذخیره در کش
            self.market_data_cache[symbol] = self.current_data
                
            logger.info(f"✅ {len(self.current_data)} کندل دریافت شد")
            
            # راه‌اندازی تحلیلگرها با داده جدید
            self._initialize_analyzers()
            
            return self.current_data
            
        except Exception as e:
            logger.error(f"❌ خطا در دریافت داده: {e}")
            return None
            
    def fetch_multiple_symbols(self, symbols: List[str], timeframe: str = "1h", limit: int = 500):
        """دریافت داده‌های چندین نماد"""
        try:
            logger.info(f"📊 دریافت داده‌های {len(symbols)} نماد...")
            
            for symbol in symbols:
                try:
                    data = self.fetch_market_data(symbol, timeframe, limit)
                    if data is not None:
                        self.market_data_cache[symbol] = data
                        logger.info(f"✓ {symbol}: {len(data)} کندل")
                except Exception as e:
                    logger.warning(f"⚠️ خطا در دریافت {symbol}: {e}")
                    
            logger.info(f"✅ داده‌های {len(self.market_data_cache)} نماد آماده")
            return self.market_data_cache
            
        except Exception as e:
            logger.error(f"❌ خطا در دریافت چندین نماد: {e}")
            return {}
            
    def _initialize_analyzers(self):
        """راه‌اندازی ماژول‌های تحلیل"""
        if self.current_data is None:
            return
            
        logger.info("🔧 راه‌اندازی ماژول‌های تحلیل...")
        
        self.elliott_analyzer = ElliottBasics(self.current_data)
        self.fractal_analyzer = FractalStructure(self.current_data)
        self.impulse_analyzer = ImpulseWaveAnalyzer(self.current_data)
        self.corrective_analyzer = CorrectiveWaveAnalyzer(self.current_data)
        self.triangle_analyzer = TriangleAnalyzer(self.current_data)
        self.diametric_analyzer = DiametricAnalyzer(self.current_data)
        self.symmetric_analyzer = AdvancedSymmetricAnalyzer(
            self.current_data, 
            config=self._get_symmetric_analyzer_config()
        )
        self.channel_analyzer = ChannelAnalyzer(self.current_data)
        self.trendline_analyzer = TrendLineAnalyzer(self.current_data)
        
        # تغییر داده شده: استفاده از AdvancedTimeAnalyzer
        self.time_analyzer = AdvancedTimeAnalyzer(self.current_data)
        
        self.complexity_analyzer = ComplexityAnalyzer(self.current_data)
        
        # راه‌اندازی استراتژی معاملاتی پیشرفته
        self.trading_strategy = AdvancedNEOWaveTradingStrategy(
            self.current_data,
            config=self._get_advanced_trading_strategy_config()
        )
        
        # راه‌اندازی تحلیلگر نسبت‌های پیشرفته
        self.ratio_analyzer = None
        
        logger.info("✅ ماژول‌های تحلیل آماده")
        
    def run_complete_analysis(self):
        """اجرای تحلیل کامل NEOWave"""
        if self.current_data is None:
            logger.error("❌ ابتدا داده‌ها را دریافت کنید")
            return None
            
        logger.info("🌊 شروع تحلیل کامل NEOWave...")
        results = {}
        
        try:
           
            # 1. شناسایی پیوت‌ها
            logger.info("🔍 شناسایی نقاط پیوت...")
            pivots = self.elliott_analyzer.identify_pivots(
                window=5, 
                min_strength=0.3, 
                use_fractal=True, 
                volume_confirmation=True
            )
            
            # دریافت pivot های تفصیلی برای تحلیل بهتر
            detailed_pivots = self.elliott_analyzer.pivot_points
            
            # آمار تفصیلی pivot ها
            pivot_types_count = {}
            strong_pivots = 0
            confirmed_pivots = 0
            
            for pivot in detailed_pivots:
                pivot_type = pivot.pivot_type.value
                pivot_types_count[pivot_type] = pivot_types_count.get(pivot_type, 0) + 1
                
                if pivot.strength >= 0.7:
                    strong_pivots += 1
                if pivot.confirmation:
                    confirmed_pivots += 1
            
            results['pivots'] = {
                'count': len(pivots),
                'strong_pivots': strong_pivots,
                'confirmed_pivots': confirmed_pivots,
                'pivot_types': pivot_types_count,
                'points': pivots[:20],  # نمایش 20 پیوت اول
                'statistics': {
                    'average_strength': np.mean([p.strength for p in detailed_pivots]) if detailed_pivots else 0,
                    'volume_confirmed_ratio': confirmed_pivots / len(detailed_pivots) if detailed_pivots else 0
                }
            }
            logger.info(f"✓ {len(pivots)} پیوت شناسایی شد ({strong_pivots} قوی, {confirmed_pivots} تایید شده)")
            
            
            # 2. تحلیل فرکتال
            logger.info("🔷 تحلیل ساختار فرکتال...")
            fractal_data = self.fractal_analyzer.identify_fractals(period=5)
            fractal_dimension = self.fractal_analyzer.calculate_fractal_dimension(
                self.current_data['close'].values
            )
            
            # تحلیل پیشرفته جدید
            logger.info("🔷 تحلیل پیشرفته ساختار فرکتال...")
            fractal_analysis = self.fractal_analyzer.perform_complete_analysis()
            
            results['fractal'] = {
                'dimension': fractal_dimension,
                'bullish_fractals': fractal_data['bullish_fractal'].sum(),
                'bearish_fractals': fractal_data['bearish_fractal'].sum(),
                # داده‌های پیشرفته جدید
                'advanced': {
                    'total_fractals': len(fractal_analysis.fractal_points),
                    'clusters': len(fractal_analysis.clusters),
                    'market_regime': fractal_analysis.market_regime,
                    'trend_strength': fractal_analysis.trend_strength,
                    'chaos_level': fractal_analysis.chaos_level,
                    'predictability': fractal_analysis.predictability_score,
                    'dimensions': fractal_analysis.dimension_profile,
                    'top_fractals': [
                        {
                            'index': f.index,
                            'price': f.price,
                            'type': f.type.value,
                            'strength': f.strength.value,
                            'confidence': f.confidence,
                            'reversal_prob': f.reversal_probability,
                            'targets': f.target_prices[:3] if f.target_prices else [],
                            'invalidation': f.invalidation_level
                        }
                        for f in fractal_analysis.fractal_points[:10]  # 10 فرکتال مهم
                    ],
                    'clusters': [
                        {
                            'center_price': c.center_price,
                            'density': c.density,
                            'significance': c.significance,
                            'type': c.cluster_type,
                            'breakout_probability': c.breakout_probability
                        }
                        for c in fractal_analysis.clusters[:5]  # 5 خوشه مهم
                    ]
                }
            }
            logger.info(f"✓ بعد فرکتال: {fractal_dimension:.3f}")
            logger.info(f"✓ رژیم بازار: {fractal_analysis.market_regime}")
            logger.info(f"✓ {len(fractal_analysis.fractal_points)} فرکتال پیشرفته شناسایی شد")
            logger.info(f"✓ سطح آشوب: {fractal_analysis.chaos_level:.2%}")
            
            
            # 3. شناسایی امواج شتابدار
            # 3. شناسایی امواج شتابدار
            logger.info("⚡ شناسایی امواج شتابدار...")
            impulse_waves = self.impulse_analyzer.identify_impulse_patterns(pivots)
            
            # استفاده از قابلیت‌های پیشرفته
            logger.info("⚡ تحلیل پیشرفته امواج شتابدار...")
            advanced_impulses = self.impulse_analyzer.identify_impulse_patterns_advanced(
                pivots, degree=0, min_confidence=0.6
            )
            
            # ترکیب نتایج
            all_impulses = impulse_waves + advanced_impulses
            
            # حذف تکراری‌ها
            unique_impulses = self.impulse_analyzer._remove_duplicate_impulses(all_impulses)
            
            # تولید خلاصه
            impulse_summary = self.impulse_analyzer.get_impulse_summary()
            
            results['impulse_waves'] = {
                'count': len(impulse_waves),
                'waves': impulse_waves[:5],  # نمایش 5 موج اول
                'advanced': {
                    'total_count': impulse_summary.get('total_count', 0),
                    'valid_count': impulse_summary.get('valid_count', 0),
                    'high_confidence_count': impulse_summary.get('high_confidence_count', 0),
                    'wave_types': impulse_summary.get('wave_types', {}),
                    'average_confidence': impulse_summary.get('average_confidence', 0.0),
                    'best_waves': []
                }
            }
            
            # بهترین امواج (با جزئیات کامل)
            best_waves = sorted(unique_impulses, key=lambda x: x.confidence_score, reverse=True)[:5]
            for wave in best_waves:
                wave_info = {
                    'id': wave.wave_id,
                    'type': wave.wave_type.value,
                    'confidence': wave.confidence_score,
                    'confidence_level': wave.confidence_level,
                    'start_price': wave.start_price,
                    'end_price': wave.end_price,
                    'duration': wave.end_index - wave.start_index,
                    'direction': wave.direction,
                    'is_valid': wave.is_valid,
                    'validation_errors': len(wave.validation_errors),
                    'validation_warnings': len(wave.validation_warnings),
                    'degree': wave.degree
                }
                
                # اضافه کردن متریک‌های پیشرفته
                if wave.metrics:
                    wave_info['advanced_metrics'] = {
                        'fibonacci_accuracy': f"{wave.metrics.fibonacci_accuracy:.2%}",
                        'channeling_quality': f"{wave.metrics.channeling_quality:.2%}",
                        'volume_confirmation': f"{wave.metrics.volume_confirmation:.2%}",
                        'momentum_confirmation': f"{wave.metrics.momentum_confirmation:.2%}",
                        'structural_integrity': f"{wave.metrics.structural_integrity:.2%}",
                        'fractal_dimension': f"{wave.metrics.fractal_dimension:.3f}",
                        'hurst_exponent': f"{wave.metrics.hurst_exponent:.3f}",
                        'predictive_power': f"{wave.metrics.predictive_power:.2%}",
                        'alternation_score': f"{wave.metrics.alternation_score:.2%}",
                        'complexity_index': f"{wave.metrics.complexity_index:.2%}",
                        'market_context_score': f"{wave.metrics.market_context_score:.2%}"
                    }
                    
                    # امتیاز کلی
                    overall_score = wave.metrics.calculate_overall_score()
                    wave_info['overall_quality_score'] = f"{overall_score:.2%}"
                
                # اضافه کردن پروژکشن‌ها
                if wave.projections:
                    wave_info['projections'] = {
                        'price_targets': wave.projections.get('wave5_targets', {}),
                        'time_targets': wave.projections.get('time_targets', {}),
                        'invalidation_level': wave.projections.get('invalidation_level', 0)
                    }
                
                # پیش‌بینی موج بعدی
                if wave.next_wave_prediction:
                    wave_info['next_wave_prediction'] = {
                        'type': wave.next_wave_prediction.get('type', 'unknown'),
                        'direction': wave.next_wave_prediction.get('direction', 'unknown'),
                        'confidence': f"{wave.next_wave_prediction.get('confidence', 0):.1%}",
                        'expected_retracement': wave.next_wave_prediction.get('expected_retracement', 'N/A'),
                        'target_range': wave.next_wave_prediction.get('target_range', [])
                    }
                
                results['impulse_waves']['advanced']['best_waves'].append(wave_info)
            
            logger.info(f"✓ {len(impulse_waves)} موج شتابدار کلاسیک شناسایی شد")
            logger.info(f"✓ {len(unique_impulses)} موج شتابدار پیشرفته شناسایی شد")
            logger.info(f"✓ {impulse_summary.get('valid_count', 0)} موج معتبر")
            logger.info(f"✓ {impulse_summary.get('high_confidence_count', 0)} موج با اطمینان بالا")
            logger.info(f"✓ میانگین اطمینان: {impulse_summary.get('average_confidence', 0):.1%}")
            
            # بهترین امواج (5 موج با بالاترین اطمینان)
            best_waves = sorted(advanced_impulses, key=lambda x: x.confidence_score, reverse=True)[:5]
            for wave in best_waves:
                wave_info = {
                    'id': wave.wave_id,
                    'type': wave.wave_type.value,
                    'confidence': wave.confidence_score,
                    'start_price': wave.start_price,
                    'end_price': wave.end_price,
                    'duration': wave.end_index - wave.start_index,
                    'is_valid': wave.is_valid,
                    'errors': len(wave.validation_errors),
                    'warnings': len(wave.validation_warnings)
                }
                
                # اضافه کردن متریک‌ها
                if wave.metrics:
                    wave_info['metrics'] = {
                        'fibonacci_accuracy': wave.metrics.fibonacci_accuracy,
                        'channeling_quality': wave.metrics.channeling_quality,
                        'predictive_power': wave.metrics.predictive_power,
                        'fractal_dimension': wave.metrics.fractal_dimension,
                        'hurst_exponent': wave.metrics.hurst_exponent
                    }
                
                # اضافه کردن پروژکشن‌ها
                if wave.projections:
                    wave_info['targets'] = wave.projections.get('wave5_targets', {})
                    
                # اضافه کردن پیش‌بینی موج بعدی
                if wave.next_wave_prediction:
                    wave_info['next_wave'] = {
                        'type': wave.next_wave_prediction.get('type'),
                        'direction': wave.next_wave_prediction.get('direction'),
                        'confidence': wave.next_wave_prediction.get('confidence')
                    }
                    
                results['impulse_waves']['advanced']['best_waves'].append(wave_info)
                
            logger.info(f"✓ {len(impulse_waves)} موج شتابدار کلاسیک شناسایی شد")
            logger.info(f"✓ {len(advanced_impulses)} موج شتابدار پیشرفته شناسایی شد")
            logger.info(f"✓ {results['impulse_waves']['advanced']['valid_count']} موج معتبر")
            logger.info(f"✓ {results['impulse_waves']['advanced']['high_confidence_count']} موج با اطمینان بالا")
            
            
            # 4. شناسایی امواج اصلاحی
            logger.info("🔄 شناسایی امواج اصلاحی...")
            corrective_waves = self.corrective_analyzer.identify_corrective_patterns(pivots, wave_degree=0, min_confidence=0.7)
            
            # تبدیل به فرمت ساده برای نمایش
            corrective_summary = []
            for wave in corrective_waves[:5]:  # نمایش 5 موج اول
                wave_info = {
                    'id': wave.wave_id,
                    'type': wave.wave_type.value,
                    'subtype': wave.subtype.value,
                    'confidence': wave.confidence_score,
                    'start_price': wave.start_price,
                    'end_price': wave.end_price,
                    'duration': wave.end_index - wave.start_index,
                    'target': wave.next_wave_target,
                    'invalidation': wave.invalidation_level,
                    'fibonacci_accuracy': wave.metrics.fibonacci_accuracy,
                    'structural_integrity': wave.metrics.structural_integrity
                }
                corrective_summary.append(wave_info)
            
            results['corrective_waves'] = {
                'count': len(corrective_waves),
                'valid_count': sum(1 for w in corrective_waves if w.is_valid),
                'waves': corrective_summary,
                'patterns_distribution': {
                    wave_type.value: sum(1 for w in corrective_waves if w.wave_type == wave_type)
                    for wave_type in set(w.wave_type for w in corrective_waves)
                }
            }
            logger.info(f"✓ {len(corrective_waves)} موج اصلاحی شناسایی شد ({sum(1 for w in corrective_waves if w.is_valid)} معتبر)")
            
            # 5. شناسایی مثلث‌ها
            logger.info("🔺 شناسایی الگوهای مثلثی...")
            triangle = self.triangle_analyzer.identify_triangle(pivots)
            if triangle:
                results['triangle'] = triangle
                logger.info(f"✓ مثلث {triangle['type'].value} شناسایی شد")
            else:
                results['triangle'] = None
                logger.info("✓ مثلثی شناسایی نشد")
                
            # 6. شناسایی دیامتریک
            logger.info("💎 شناسایی الگوهای دیامتریک...")
            diametric_pattern = self.diametric_analyzer.identify_diametric(pivots, wave_degree=0, strict_validation=True)
            
            if diametric_pattern and diametric_pattern.is_valid:
                diametric_info = {
                    'id': diametric_pattern.pattern_id,
                    'type': diametric_pattern.pattern_type.value,
                    'subtype': diametric_pattern.subtype.value,
                    'confidence': diametric_pattern.confidence_score,
                    'duration': diametric_pattern.duration,
                    'start_price': diametric_pattern.start_price,
                    'end_price': diametric_pattern.end_price,
                    'target': diametric_pattern.post_pattern_target,
                    'invalidation': diametric_pattern.invalidation_level,
                    'reversal_probability': diametric_pattern.reversal_probability,
                    'geometry': {
                        'geometric_balance': diametric_pattern.geometry.geometric_balance,
                        'radial_symmetry': diametric_pattern.geometry.radial_symmetry,
                        'bilateral_symmetry': diametric_pattern.geometry.bilateral_symmetry,
                        'aspect_ratio': diametric_pattern.geometry.aspect_ratio
                    },
                    'waves_count': len(diametric_pattern.waves),
                    'validation_details': diametric_pattern.validation_details
                }
                results['diametric'] = diametric_info
                logger.info(f"✓ دیامتریک {diametric_pattern.pattern_type.value} شناسایی شد - اعتماد: {diametric_pattern.confidence_score:.2f}")
            else:
                results['diametric'] = None
                logger.info("✓ دیامتریکی شناسایی نشد")

            # 7. شناسایی الگوهای سیمتریک پیشرفته
            logger.info("🔄 شناسایی الگوهای سیمتریک پیشرفته...")
            try:
                # شناسایی الگوی سیمتریک پیشرفته
                symmetric_pattern = self.symmetric_analyzer.identify_advanced_symmetric(
                    pivots, 
                    degree=0, 
                    strict_validation=True
                )
                
                if symmetric_pattern and symmetric_pattern.is_valid:
                    # تبدیل به فرمت گزارش
                    symmetric_info = {
                        'pattern_id': symmetric_pattern.pattern_id,
                        'pattern_type': symmetric_pattern.pattern_type.value,
                        'symmetry_type': symmetric_pattern.symmetry_type.value,
                        'symmetry_quality': symmetric_pattern.symmetry_quality.value,
                        'overall_confidence': symmetric_pattern.overall_confidence,
                        'pattern_completion': symmetric_pattern.pattern_completion,
                        'validation_score': symmetric_pattern.validation_score,
                        'statistical_significance': symmetric_pattern.statistical_significance,
                        'strength_rating': symmetric_pattern.strength_rating,
                        'trade_recommendation': symmetric_pattern.trade_recommendation,
                        
                        # متریک‌های تقارن
                        'symmetry_metrics': {
                            'spatial_symmetry': symmetric_pattern.symmetry_metrics.spatial_symmetry,
                            'temporal_symmetry': symmetric_pattern.symmetry_metrics.temporal_symmetry,
                            'amplitude_symmetry': symmetric_pattern.symmetry_metrics.amplitude_symmetry,
                            'frequency_symmetry': symmetric_pattern.symmetry_metrics.frequency_symmetry,
                            'phase_symmetry': symmetric_pattern.symmetry_metrics.phase_symmetry,
                            'harmonic_symmetry': symmetric_pattern.symmetry_metrics.harmonic_symmetry,
                            'fractal_symmetry': symmetric_pattern.symmetry_metrics.fractal_symmetry,
                            'statistical_symmetry': symmetric_pattern.symmetry_metrics.statistical_symmetry,
                            'information_entropy': symmetric_pattern.symmetry_metrics.information_entropy,
                            'lyapunov_exponent': symmetric_pattern.symmetry_metrics.lyapunov_exponent,
                            'correlation_dimension': symmetric_pattern.symmetry_metrics.correlation_dimension
                        },
                        
                        # تحلیل هندسی
                        'geometric_analysis': {
                            'center_point': symmetric_pattern.geometric_analysis.center_point,
                            'symmetry_axis': symmetric_pattern.geometric_analysis.symmetry_axis,
                            'reflection_accuracy': symmetric_pattern.geometric_analysis.reflection_accuracy,
                            'rotation_angle': symmetric_pattern.geometric_analysis.rotation_angle,
                            'scaling_factor': symmetric_pattern.geometric_analysis.scaling_factor,
                            'geometric_balance': symmetric_pattern.geometric_analysis.geometric_balance,
                            'aspect_ratio': symmetric_pattern.geometric_analysis.aspect_ratio,
                            'golden_ratio_alignment': symmetric_pattern.geometric_analysis.golden_ratio_alignment
                        },
                        
                        # پروژکشن‌ها و اهداف
                        'projections': {
                            'post_pattern_targets': symmetric_pattern.projections.post_pattern_targets,
                            'time_projections': symmetric_pattern.projections.time_projections,
                            'support_resistance_levels': symmetric_pattern.projections.support_resistance_levels[:10],  # محدود کردن
                            'invalidation_levels': symmetric_pattern.projections.invalidation_levels,
                            'confidence_intervals': symmetric_pattern.projections.confidence_intervals,
                            'probability_distribution': symmetric_pattern.projections.probability_distribution
                        },
                        
                        # محیط بازار
                        'market_context': symmetric_pattern.market_context,
                        
                        # ویژگی‌های ML
                        'ml_features': {
                            'ml_confidence': symmetric_pattern.ml_confidence,
                            'anomaly_score': symmetric_pattern.anomaly_score,
                            'features_count': len(symmetric_pattern.ml_features) if symmetric_pattern.ml_features is not None else 0
                        },
                        
                        # ارزیابی ریسک
                        'risk_assessment': symmetric_pattern.risk_assessment,
                        
                        # جزئیات امواج
                        'waves_analysis': {
                            'total_waves': len(symmetric_pattern.waves),
                            'center_wave_strength': symmetric_pattern.waves[4].length / np.mean([w.length for w in symmetric_pattern.waves]),
                            'average_wave_length': np.mean([w.length for w in symmetric_pattern.waves]),
                            'average_wave_duration': np.mean([w.duration for w in symmetric_pattern.waves]),
                            'direction_pattern': [w.direction for w in symmetric_pattern.waves],
                            'fractal_dimensions': [w.fractal_dimension for w in symmetric_pattern.waves],
                            'hurst_exponents': [w.hurst_exponent for w in symmetric_pattern.waves],
                            'complexity_scores': [w.shape_complexity for w in symmetric_pattern.waves]
                        },
                        
                        # اعتبارسنجی تفصیلی
                        'validation_details': symmetric_pattern.validation_details
                    }
                    
                    results['advanced_symmetric'] = symmetric_info
                    
                    logger.info(f"✓ الگوی سیمتریک پیشرفته شناسایی شد:")
                    logger.info(f"  - شناسه: {symmetric_pattern.pattern_id}")
                    logger.info(f"  - نوع: {symmetric_pattern.pattern_type.value}")
                    logger.info(f"  - نوع تقارن: {symmetric_pattern.symmetry_type.value}")
                    logger.info(f"  - کیفیت: {symmetric_pattern.symmetry_quality.value}")
                    logger.info(f"  - اعتماد کلی: {symmetric_pattern.overall_confidence:.2%}")
                    logger.info(f"  - تکمیل الگو: {symmetric_pattern.pattern_completion:.2%}")
                    logger.info(f"  - قدرت الگو: {symmetric_pattern.strength_rating}")
                    logger.info(f"  - توصیه معاملاتی: {symmetric_pattern.trade_recommendation}")
                    logger.info(f"  - سطح ریسک: {symmetric_pattern.risk_assessment.get('risk_level', 'نامشخص')}")
                    logger.info(f"  - معنی‌داری آماری: {symmetric_pattern.statistical_significance:.2%}")
                    
                    # نمایش متریک‌های کلیدی تقارن
                    sym_metrics = symmetric_pattern.symmetry_metrics
                    logger.info(f"  - تقارن فضایی: {sym_metrics.spatial_symmetry:.2%}")
                    logger.info(f"  - تقارن زمانی: {sym_metrics.temporal_symmetry:.2%}")
                    logger.info(f"  - تقارن دامنه: {sym_metrics.amplitude_symmetry:.2%}")
                    logger.info(f"  - تقارن هارمونیک: {sym_metrics.harmonic_symmetry:.2%}")
                    
                    # نمایش اهداف قیمتی
                    targets = symmetric_pattern.projections.post_pattern_targets
                    logger.info(f"  - اهداف قیمتی:")
                    for target_name, target_price in targets.items():
                        logger.info(f"    * {target_name}: ${target_price:,.2f}")
                    
                else:
                    results['advanced_symmetric'] = None
                    logger.info("✓ الگوی سیمتریک پیشرفته‌ای شناسایی نشد")
                    
                # دریافت خلاصه کلی الگوهای سیمتریک
                symmetric_summary = self.symmetric_analyzer.get_pattern_summary()
                results['symmetric_summary'] = symmetric_summary
                
                if symmetric_summary['total_patterns'] > 0:
                    logger.info(f"📊 خلاصه الگوهای سیمتریک:")
                    logger.info(f"  - تعداد کل الگوها: {symmetric_summary['total_patterns']}")
                    logger.info(f"  - میانگین اعتماد: {symmetric_summary['average_confidence']:.2%}")
                    logger.info(f"  - توزیع انواع: {symmetric_summary['pattern_types']}")
                    logger.info(f"  - توزیع کیفیت: {symmetric_summary['quality_distribution']}")
                    
            except Exception as e:
                logger.error(f"❌ خطا در تحلیل سیمتریک پیشرفته: {e}")
                results['advanced_symmetric'] = None
                results['symmetric_summary'] = {'total_patterns': 0, 'patterns': []}

            # 8. تحلیل نسبت‌های پیشرفته
            if impulse_waves:
                logger.info("🔢 تحلیل پیشرفته نسبت‌های فیبوناچی...")
                
                # آماده‌سازی داده‌های امواج برای RatioAnalyzer
                sample_waves = []
                for wave in impulse_waves[0].waves:
                    wave_dict = {
                        'length': getattr(wave, 'length', abs(getattr(wave, 'end_price', 0) - getattr(wave, 'start_price', 0))),
                        'duration': getattr(wave, 'duration', getattr(wave, 'end_index', 0) - getattr(wave, 'start_index', 0)),
                        'price': getattr(wave, 'end_price', 0),
                        'sub_waves_count': len(getattr(wave, 'sub_waves', [])),
                        'volume_profile': getattr(wave, 'volume_profile', {}),
                        'momentum': getattr(wave, 'momentum', {}),
                        'shape_quality': getattr(wave, 'shape_quality', 0.7)
                    }
                    sample_waves.append(wave_dict)
                
                # ایجاد RatioAnalyzer با تنظیمات پیشرفته
                self.ratio_analyzer = RatioAnalyzer(
                    waves=sample_waves,
                    validation_level=ValidationLevel.MODERATE,
                    enable_ml=True,
                    enable_statistics=True,
                    enable_geometry=True
                )
                
                # تحلیل نسبت‌های داخلی پیشرفته
                advanced_ratios = self.ratio_analyzer.calculate_advanced_internal_ratios()
                
                # اعتبارسنجی امواج ممتد
                extended_wave_validations = {}
                for i in range(len(impulse_waves[0].waves)):
                    validation = self.ratio_analyzer.calculate_extended_wave_validation(
                        wave_number=i+1, 
                        strict_validation=True
                    )
                    extended_wave_validations[f'wave_{i+1}'] = validation
                
                # تحلیل جامع روابط فیبوناچی
                comprehensive_fibonacci = {}
                waves = impulse_waves[0].waves
                for i in range(len(waves)-1):
                    wave1 = waves[i]
                    wave2 = waves[i+1]
                    
                    length1 = getattr(wave1, 'length', abs(getattr(wave1, 'end_price', 0) - getattr(wave1, 'start_price', 0)))
                    length2 = getattr(wave2, 'length', abs(getattr(wave2, 'end_price', 0) - getattr(wave2, 'start_price', 0)))
                    
                    if length1 > 0:
                        comprehensive_analysis = self.ratio_analyzer.calculate_comprehensive_fibonacci_relationship(
                            wave1_length=length1,
                            wave2_length=length2,
                            tolerance=0.05,
                            include_harmonics=True
                        )
                        comprehensive_fibonacci[f'wave_{i+1}_to_wave_{i+2}'] = comprehensive_analysis
                
                results['advanced_ratios'] = {
                    'internal_ratios': advanced_ratios,
                    'extended_wave_validations': extended_wave_validations,
                    'comprehensive_fibonacci': comprehensive_fibonacci,
                    'summary': {
                        'total_ratios_analyzed': len(advanced_ratios.get('classic_ratios', {})),
                        'valid_extensions': sum(1 for v in extended_wave_validations.values() if v.get('is_extended', False)),
                        'high_confidence_ratios': sum(1 for r in advanced_ratios.get('classic_ratios', {}).values() 
                                                    if hasattr(r, 'confidence_score') and r.confidence_score > 0.8),
                        'ml_predictions_available': advanced_ratios.get('ml_predictions', {}).get('ml_enabled', False),
                        'statistical_analysis_completed': bool(advanced_ratios.get('statistical_analysis')),
                        'geometric_analysis_completed': bool(advanced_ratios.get('geometric_analysis'))
                    }
                }
                
                logger.info(f"✓ {results['advanced_ratios']['summary']['total_ratios_analyzed']} نسبت تحلیل شد")
                logger.info(f"✓ {results['advanced_ratios']['summary']['valid_extensions']} موج ممتد شناسایی شد")
                logger.info(f"✓ {results['advanced_ratios']['summary']['high_confidence_ratios']} نسبت با اطمینان بالا")
                
            # 9. تحلیل پیچیدگی
            if impulse_waves:
                logger.info("🧩 تحلیل پیچیدگی ساختاری...")
                # تبدیل wave به فرمت dictionary
                first_wave = impulse_waves[0].waves[0]
                wave_dict = {
                    'label': getattr(first_wave, 'label', 'Wave-1'),
                    'start_index': getattr(first_wave, 'start_index', 0),
                    'end_index': getattr(first_wave, 'end_index', 0), 
                    'start_price': getattr(first_wave, 'start_price', 0),
                    'end_price': getattr(first_wave, 'end_price', 0),
                    'sub_waves': getattr(first_wave, 'sub_waves', [])
                }
                
                complexity_result = self.complexity_analyzer.analyze_wave_complexity(wave_dict)
                results['complexity'] = {
                    'level': complexity_result.complexity_level.name,
                    'structure_type': complexity_result.structure_type.value,
                    'confidence': complexity_result.complexity_confidence,
                    'metrics': {
                        'fractal_dimension': complexity_result.metrics.fractal_dimension,
                        'time_complexity': complexity_result.metrics.time_complexity,
                        'price_complexity': complexity_result.metrics.price_complexity,
                        'structural_complexity': complexity_result.metrics.structural_complexity
                    },
                    'recommendations': complexity_result.recommendations
                }
                logger.info(f"✓ سطح پیچیدگی: {complexity_result.complexity_level.name}")
                
            # 10. کانال‌بندی
            if impulse_waves:
                logger.info("📊 ایجاد کانال‌های قیمتی...")
                elliott_channel = self.channel_analyzer.create_elliott_channel(
                    impulse_waves[0].waves
                )
                results['channel'] = elliott_channel
                logger.info("✓ کانال الیوت ایجاد شد")
                
            # 11. خطوط روند
            if impulse_waves and len(impulse_waves[0].waves) >= 3:
                logger.info("📈 رسم خطوط روند...")
                trendline_0_2 = self.trendline_analyzer.draw_0_2_trendline(
                    impulse_waves[0].waves
                )
                
                # ایجاد کانال موازی از pivots
                pivot_points = [(p.index, p.value, 'HIGH' if p.type == 'peak' else 'LOW') 
                               for p in pivots[:10]]
                parallel_channel = self.channel_analyzer.create_parallel_channel(pivot_points)
                
                results['trendlines'] = {
                    '0-2': trendline_0_2
                }
                results['parallel_channel'] = parallel_channel
                logger.info("✓ خطوط روند و کانال‌های موازی رسم شد")
                
            # 12. تحلیل زمانی پیشرفته
            if impulse_waves:
                logger.info("⏰ تحلیل روابط زمانی پیشرفته...")
                
                # تبدیل امواج به فرمت مناسب برای AdvancedTimeAnalyzer
                waves_for_analysis = []
                for wave in impulse_waves[0].waves:
                    wave_dict = {
                        'start': [getattr(wave, 'start_index', 0), getattr(wave, 'start_price', 0)],
                        'end': [getattr(wave, 'end_index', 0), getattr(wave, 'end_price', 0)],
                        'duration': getattr(wave, 'duration', getattr(wave, 'end_index', 0) - getattr(wave, 'start_index', 0))
                    }
                    waves_for_analysis.append(wave_dict)
                
                # اجرای تحلیل زمانی پیشرفته
                time_analysis_result = self.time_analyzer.analyze_advanced_time_relationships(
                    waves_for_analysis, degree=0
                )
                
                if time_analysis_result:
                    results['advanced_time_analysis'] = {
                        'analysis_id': time_analysis_result.analysis_id,
                        'timeframe': time_analysis_result.timeframe.value,
                        'analysis_quality': time_analysis_result.analysis_quality,
                        'reliability_score': time_analysis_result.reliability_score,
                        'time_metrics': {
                            'duration': time_analysis_result.time_metrics.duration,
                            'velocity': time_analysis_result.time_metrics.velocity,
                            'acceleration': time_analysis_result.time_metrics.acceleration,
                            'momentum_persistence': time_analysis_result.time_metrics.momentum_persistence,
                            'volatility_clustering': time_analysis_result.time_metrics.volatility_clustering,
                            'hurst_exponent': time_analysis_result.time_metrics.hurst_exponent,
                            'fractal_dimension': time_analysis_result.time_metrics.fractal_dimension,
                            'entropy': time_analysis_result.time_metrics.entropy,
                            'lyapunov_exponent': time_analysis_result.time_metrics.lyapunov_exponent,
                            'correlation_length': time_analysis_result.time_metrics.correlation_length
                        },
                        'cycles': [
                            {
                                'type': cycle.cycle_type.value,
                                'period': cycle.period,
                                'amplitude': cycle.amplitude,
                                'phase': cycle.phase,
                                'confidence': cycle.confidence,
                                'strength': cycle.strength,
                                'next_peak': cycle.next_peak,
                                'next_trough': cycle.next_trough,
                                'statistical_significance': cycle.statistical_significance
                            }
                            for cycle in time_analysis_result.cycles[:10]  # 10 چرخه برتر
                        ],
                        'dominant_cycle': {
                            'type': time_analysis_result.dominant_cycle.cycle_type.value,
                            'period': time_analysis_result.dominant_cycle.period,
                            'strength': time_analysis_result.dominant_cycle.strength,
                            'confidence': time_analysis_result.dominant_cycle.confidence
                        } if time_analysis_result.dominant_cycle else None,
                        'time_projections': [
                            {
                                'target_time': proj.target_time,
                                'type': proj.projection_type.value,
                                'confidence_level': proj.confidence_level.value,
                                'confidence_score': proj.confidence_score,
                                'supporting_factors': proj.supporting_factors,
                                'invalidation_time': proj.invalidation_time,
                                'probability_distribution': proj.probability_distribution
                            }
                            for proj in time_analysis_result.time_projections[:5]  # 5 پروژکشن برتر
                        ],
                        'critical_time_zones': [
                            {
                                'center_time': zone.center_time,
                                'time_range': zone.time_range,
                                'strength': zone.strength,
                                'significance': zone.significance,
                                'probability': zone.probability,
                                'cluster_type': zone.cluster_type
                            }
                            for zone in time_analysis_result.critical_time_zones[:5]  # 5 منطقه بحرانی برتر
                        ],
                        'seasonal_patterns': [
                            {
                                'name': pattern.pattern_name,
                                'period_days': pattern.period_days,
                                'strength': pattern.strength,
                                'phase_offset': pattern.phase_offset
                            }
                            for pattern in time_analysis_result.seasonal_patterns
                        ],
                        'time_alternations': [
                            {
                                'wave_pair': alt.wave_pair,
                                'time_ratio': alt.time_ratio,
                                'alternation_type': alt.alternation_type,
                                'alternation_strength': alt.alternation_strength,
                                'fibonacci_alignment': alt.fibonacci_alignment,
                                'statistical_significance': alt.statistical_significance,
                                'expected_range': alt.expected_range
                            }
                            for alt in time_analysis_result.time_alternations
                        ],
                        'ml_predictions': time_analysis_result.ml_predictions,
                        'summary': time_analysis_result.summary
                    }
                    
                    logger.info("✓ تحلیل زمانی پیشرفته انجام شد:")
                    logger.info(f"  - کیفیت تحلیل: {time_analysis_result.analysis_quality:.2%}")
                    logger.info(f"  - قابلیت اطمینان: {time_analysis_result.reliability_score:.2%}")
                    logger.info(f"  - تعداد چرخه‌ها: {len(time_analysis_result.cycles)}")
                    logger.info(f"  - پروژکشن‌های زمانی: {len(time_analysis_result.time_projections)}")
                    logger.info(f"  - مناطق بحرانی: {len(time_analysis_result.critical_time_zones)}")
                    
                    if time_analysis_result.dominant_cycle:
                        logger.info(f"  - چرخه غالب: {time_analysis_result.dominant_cycle.cycle_type.value} "
                                  f"با دوره {time_analysis_result.dominant_cycle.period:.1f}")
                else:
                    results['advanced_time_analysis'] = None
                    logger.info("✓ تحلیل زمانی پیشرفته انجام نشد")
                
            # 13. سیگنال‌های معاملاتی پیشرفته و مدیریت سرمایه
            logger.info("💰 تولید سیگنال‌های معاملاتی پیشرفته...")
            if impulse_waves and len(impulse_waves[0].waves) >= 2:
                current_wave = impulse_waves[0].waves[-1]
                
                # تبدیل current_wave به فرمت مناسب برای استراتژی پیشرفته
                wave_data = {
                    'number': getattr(current_wave, 'wave_number', len(impulse_waves[0].waves)),
                    'type': getattr(current_wave, 'wave_type', ''),
                    'end_price': getattr(current_wave, 'end_price', self.current_data['close'].iloc[-1]),
                    'start_price': getattr(current_wave, 'start_price', self.current_data['close'].iloc[-10]),
                    'current_price': self.current_data['close'].iloc[-1],
                    'retracement': getattr(current_wave, 'retracement', 0.5),
                    'wave1_start_price': getattr(current_wave, 'wave1_start_price', self.current_data['close'].iloc[-20]),
                    'wave1_length': getattr(current_wave, 'wave1_length', abs(self.current_data['close'].iloc[-10] - self.current_data['close'].iloc[-20])),
                    'projected_length': getattr(current_wave, 'projected_length', abs(self.current_data['close'].iloc[-5] - self.current_data['close'].iloc[-10])),
                    'divergence': getattr(current_wave, 'divergence', False),
                    'volume_confirmation': getattr(current_wave, 'volume_confirmation', True),
                    'degree': getattr(current_wave, 'degree', 0),
                    'complexity': getattr(current_wave, 'complexity', 'Simple')
                }
                
                # تولید سیگنال پیشرفته
                advanced_signal = self.trading_strategy.analyze_wave_position(wave_data)
                
                if advanced_signal:
                    # ادغام با مدیریت سرمایه پیشرفته
                    enhanced_signal = self._enhance_advanced_signal_with_money_management(advanced_signal)
                    results['advanced_trading_signal'] = enhanced_signal
                    
                    # محاسبه حجم پوزیشن پیشرفته
                    position_sizing = self.trading_strategy.calculate_position_size(
                        enhanced_signal, 
                        self.money_manager.current_capital
                    )
                    results['position_sizing'] = position_sizing
                    
                    # تولید توصیه‌های مدیریت سرمایه
                    if self.auto_trading_enabled:
                        position_result = self._execute_advanced_signal(enhanced_signal)
                        results['position_execution'] = position_result
                    
                    # ذخیره در تاریخچه
                    self.signals_history.append({
                        'timestamp': enhanced_signal.timestamp,
                        'signal': enhanced_signal,
                        'market_conditions': enhanced_signal.market_conditions,
                        'performance': None  # خواهد شد پر شود بعداً
                    })
                    
                    # به‌روزرسانی آمار عملکرد
                    self._update_performance_tracking(enhanced_signal)
                    
                    alert = self.trading_strategy.generate_alert(enhanced_signal)
                    logger.info(alert)
                else:
                    logger.info("⚠️ سیگنال معاملاتی تولید نشد")
                    
            # 14. گزارش مدیریت سرمایه پیشرفته
            logger.info("📊 آماده‌سازی گزارش مدیریت سرمایه پیشرفته...")
            portfolio_report = self.money_manager.generate_performance_report()
            results['portfolio_management'] = portfolio_report
            
            # اضافه کردن متریک‌های خاص NEOWave
            results['portfolio_management']['neowave_metrics'] = {
                'signals_generated': len(self.signals_history),
                'average_signal_confidence': self.performance_tracking['average_confidence'],
                'success_rate': self.performance_tracking['successful_signals'] / max(1, self.performance_tracking['total_signals']),
                'current_wave_analysis': wave_data if 'wave_data' in locals() else None,
                'market_regime': advanced_signal.market_conditions.regime.value if 'advanced_signal' in locals() and advanced_signal else 'UNKNOWN'
            }
            
            # 15. تست استرس
            if self.money_manager.config.get('stress_test_enabled', False):
                logger.info("🧪 اجرای تست استرس...")
                stress_scenarios = self._get_stress_test_scenarios()
                stress_results = self.money_manager.stress_test_portfolio(stress_scenarios)
                results['stress_test'] = stress_results
                
            # 16. بهینه‌سازی پرتفویو
            optimization_results = self.money_manager.optimize_portfolio()
            results['portfolio_optimization'] = optimization_results
            
            # 17. تحلیل ریسک جامع
            comprehensive_risk = self._analyze_comprehensive_risk(results)
            results['comprehensive_risk'] = comprehensive_risk
            
            # 18. پیش‌بینی‌های ML
            if self.config.get('ml_enabled', True):
                ml_predictions = self._generate_ml_predictions(results)
                results['ml_predictions'] = ml_predictions
            
            self.analysis_results = results
            logger.info("✅ تحلیل کامل NEOWave با موفقیت انجام شد!")
            
            # خلاصه نهایی
            logger.info(f"📈 خلاصه نتایج:")
            logger.info(f"  - پیوت‌ها: {results['pivots']['count']}")
            logger.info(f"  - امواج شتابدار: {results['impulse_waves']['count']}")
            logger.info(f"  - امواج اصلاحی: {results['corrective_waves']['count']}")
            logger.info(f"  - الگوهای خاص: {len([k for k, v in results.items() if k in ['triangle', 'diametric', 'advanced_symmetric'] and v])}")
            logger.info(f"  - سیگنال‌های تولید شده: {len(self.signals_history)}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ خطا در تحلیل: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def _enhance_advanced_signal_with_money_management(self, signal: AdvancedTradingSignal) -> AdvancedTradingSignal:
        """تقویت سیگنال پیشرفته با مدیریت سرمایه"""
        try:
            # آماده‌سازی داده‌های سیگنال برای مدیریت سرمایه
            signal_data = {
                'symbol': signal.symbol,
                'signal_source': 'NEOWave Advanced',
                'wave_type': signal.wave_position,
                'wave_degree': signal.wave_degree,
                'entry_price': signal.entry_price,
                'stop_loss': signal.stop_loss,
                'take_profits': signal.take_profits,
                'confidence_score': signal.confidence,
                'position_type': signal.signal_type.value,
                'risk_reward_ratio': signal.risk_reward_ratio,
                'market_regime': signal.market_conditions.regime.value,
                'volatility_forecast': signal.ml_predictions.volatility_forecast,
                'anomaly_score': signal.ml_predictions.anomaly_score
            }
            
            # محاسبه حجم بهینه با سیستم پیشرفته
            position_size_result = self.money_manager.calculate_optimal_position_size(
                signal_data, self.current_data
            )
            
            # به‌روزرسانی سیگنال با اطلاعات مدیریت سرمایه
            signal.suggested_position_size = position_size_result['size']
            signal.max_position_size = position_size_result.get('max_size', position_size_result['size'] * 2)
            signal.risk_amount = position_size_result['risk_amount']
            
            # اضافه کردن metadata مدیریت سرمایه
            if not hasattr(signal, 'money_management'):
                signal.money_management = {}
            
            signal.money_management.update({
                'optimal_size': position_size_result['size'],
                'risk_amount': position_size_result['risk_amount'],
                'risk_percent': position_size_result['risk_percent'],
                'sizing_method': position_size_result['method'],
                'capital_utilization': position_size_result.get('capital_utilization', 0),
                'portfolio_impact': self._calculate_portfolio_impact(position_size_result),
                'mm_recommendation': self._get_money_management_recommendation(position_size_result),
                'regime_adjustment': self._get_regime_adjustment(signal.market_conditions),
                'correlation_check': self._check_correlation_limits(signal.symbol),
                'stress_test_impact': self._estimate_stress_impact(signal)
            })
            
            return signal
            
        except Exception as e:
            logger.error(f"خطا در تقویت سیگنال پیشرفته: {e}")
            return signal
    
    def _execute_advanced_signal(self, signal: AdvancedTradingSignal) -> Dict:
        """اجرای سیگنال پیشرفته"""
        try:
            if not self.auto_trading_enabled:
                return {'status': 'auto_trading_disabled'}
                
            # بررسی محدودیت‌های ریسک پیشرفته
            risk_check = self.money_manager.check_risk_limits()
            
            if not risk_check['can_trade']:
                return {
                    'status': 'rejected',
                    'reason': 'Risk limits exceeded',
                    'details': risk_check
                }
            
            # بررسی اضافی برای سیگنال‌های پیشرفته
            if signal.confidence < self.config.get('min_signal_confidence', 0.6):
                return {
                    'status': 'rejected',
                    'reason': 'Signal confidence too low',
                    'confidence': signal.confidence
                }
            
            if signal.risk_reward_ratio < self.config.get('min_rr_ratio', 2.0):
                return {
                    'status': 'rejected',
                    'reason': 'Risk/Reward ratio insufficient',
                    'rr_ratio': signal.risk_reward_ratio
                }
            
            # اجرای پوزیشن با اطلاعات پیشرفته
            position_data = {
                'signal_id': signal.signal_id,
                'symbol': signal.symbol,
                'signal_type': signal.signal_type.value,
                'entry_price': signal.entry_price,
                'stop_loss': signal.stop_loss,
                'take_profits': signal.take_profits,
                'quantity': signal.suggested_position_size,
                'wave_analysis': {
                    'wave_position': signal.wave_position,
                    'elliott_count': signal.elliott_count,
                    'neowave_structure': signal.neowave_structure
                },
                'risk_metrics': {
                    'confidence': signal.confidence,
                    'risk_reward_ratio': signal.risk_reward_ratio,
                    'market_regime': signal.market_conditions.regime.value,
                    'volatility_forecast': signal.ml_predictions.volatility_forecast
                }
            }
            
            position = self.money_manager.add_position(position_data, self.current_data)
            
            if position:
                return {
                    'status': 'executed',
                    'position_id': position.position_id,
                    'signal_id': signal.signal_id,
                    'symbol': position.symbol,
                    'quantity': position.quantity,
                    'entry_price': position.entry_price,
                    'risk_amount': position.current_risk,
                    'expected_return': signal.expected_return,
                    'wave_analysis': position_data['wave_analysis'],
                    'execution_time': datetime.now().isoformat()
                }
            else:
                return {'status': 'failed', 'reason': 'Position creation failed'}
                
        except Exception as e:
            logger.error(f"خطا در اجرای سیگنال پیشرفته: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _update_performance_tracking(self, signal: AdvancedTradingSignal):
        """به‌روزرسانی آمار عملکرد"""
        self.performance_tracking['total_signals'] += 1
        
        # محاسبه میانگین اطمینان
        total_confidence = (self.performance_tracking['average_confidence'] * 
                          (self.performance_tracking['total_signals'] - 1) + signal.confidence)
        self.performance_tracking['average_confidence'] = total_confidence / self.performance_tracking['total_signals']
        
        # ذخیره بهترین و بدترین سیگنال
        if (not self.performance_tracking['best_signal'] or 
            signal.confidence > self.performance_tracking['best_signal'].confidence):
            self.performance_tracking['best_signal'] = signal
            
        if (not self.performance_tracking['worst_signal'] or 
            signal.confidence < self.performance_tracking['worst_signal'].confidence):
            self.performance_tracking['worst_signal'] = signal
    
    def _analyze_comprehensive_risk(self, results: Dict) -> Dict:
        """تحلیل ریسک جامع"""
        risk_analysis = {
            'overall_risk_score': 0.5,
            'risk_factors': [],
            'risk_mitigation': [],
            'recommendations': []
        }
        
        try:
            # ریسک بر اساس نوسان
            if 'advanced_trading_signal' in results:
                signal = results['advanced_trading_signal']
                volatility_risk = signal.ml_predictions.volatility_forecast
                
                if volatility_risk > 0.3:
                    risk_analysis['risk_factors'].append(f"نوسان بالا: {volatility_risk:.1%}")
                    risk_analysis['overall_risk_score'] += 0.2
                
                # ریسک رژیم بازار
                if signal.market_conditions.regime == MarketRegime.CRISIS:
                    risk_analysis['risk_factors'].append("رژیم بحرانی بازار")
                    risk_analysis['overall_risk_score'] += 0.3
                elif signal.market_conditions.regime == MarketRegime.HIGH_VOLATILITY:
                    risk_analysis['risk_factors'].append("نوسان بالای بازار")
                    risk_analysis['overall_risk_score'] += 0.15
                
                # ریسک اطمینان سیگنال
                if signal.confidence < 0.7:
                    risk_analysis['risk_factors'].append(f"اطمینان پایین سیگنال: {signal.confidence:.1%}")
                    risk_analysis['overall_risk_score'] += 0.1
            
            # توصیه‌های کاهش ریسک
            if risk_analysis['overall_risk_score'] > 0.7:
                risk_analysis['risk_mitigation'].extend([
                    "کاهش حجم پوزیشن",
                    "تنظیم stop loss نزدیک‌تر",
                    "نظارت مداوم بر بازار"
                ])
            
            risk_analysis['overall_risk_score'] = min(1.0, risk_analysis['overall_risk_score'])
            
        except Exception as e:
            logger.error(f"خطا در تحلیل ریسک جامع: {e}")
        
        return risk_analysis
    
    def _generate_ml_predictions(self, results: Dict) -> Dict:
        """تولید پیش‌بینی‌های ML"""
        predictions = {
            'price_direction': {'up': 0.5, 'down': 0.5},
            'volatility_forecast': 0.2,
            'regime_change_probability': 0.1,
            'confidence': 0.5
        }
        
        try:
            if 'advanced_trading_signal' in results:
                signal = results['advanced_trading_signal']
                ml_preds = signal.ml_predictions
                
                predictions.update({
                    'price_direction': {
                        'up': ml_preds.price_direction_prob,
                        'down': 1 - ml_preds.price_direction_prob
                    },
                    'volatility_forecast': ml_preds.volatility_forecast,
                    'regime_change_probability': ml_preds.regime_change_prob,
                    'confidence': ml_preds.model_confidence,
                    'anomaly_score': ml_preds.anomaly_score,
                    'optimal_holding_period': ml_preds.optimal_holding_period
                })
                
        except Exception as e:
            logger.error(f"خطا در تولید پیش‌بینی ML: {e}")
        
        return predictions
            
    def _calculate_portfolio_impact(self, position_size_result: Dict) -> Dict:
        """محاسبه تأثیر بر پرتفویو"""
        current_status = self.money_manager.get_real_time_status()
        
        return {
            'current_positions': current_status['positions']['count'],
            'current_exposure': current_status['positions']['exposure_percent'],
            'new_exposure': position_size_result.get('capital_utilization', 0),
            'total_exposure_after': current_status['positions']['exposure_percent'] + position_size_result.get('capital_utilization', 0),
            'risk_increase': position_size_result.get('risk_percent', 0),
            'diversification_impact': self._calculate_diversification_impact(position_size_result)
        }
    
    def _calculate_diversification_impact(self, position_size_result: Dict) -> float:
        """محاسبه تأثیر بر تنوع‌بخشی"""
        # ساده‌سازی - در عمل پیچیده‌تر
        current_positions = len(self.money_manager.positions)
        max_positions = self.money_manager.config.get('max_positions', 5)
        
        diversification_score = current_positions / max_positions
        return min(1.0, diversification_score)
        
    def _get_money_management_recommendation(self, position_size_result: Dict) -> str:
        """دریافت توصیه مدیریت سرمایه"""
        size = position_size_result.get('size', 0)
        risk_percent = position_size_result.get('risk_percent', 0)
        
        if size == 0:
            return "⛔ عدم ورود - ریسک بالا یا محدودیت‌های پرتفویو"
        elif risk_percent < 1:
            return "🟢 ورود محافظه‌کارانه - ریسک کم"
        elif risk_percent < 2:
            return "🟡 ورود متعادل - ریسک متوسط"
        else:
            return "🔴 ورود پرریسک - مراقبت لازم"
    
    def _get_regime_adjustment(self, market_conditions) -> Dict:
        """تنظیم بر اساس رژیم بازار"""
        adjustments = {
            'position_size_multiplier': 1.0,
            'stop_loss_adjustment': 1.0,
            'take_profit_adjustment': 1.0,
            'holding_period_adjustment': 1.0
        }
        
        if market_conditions.regime == MarketRegime.HIGH_VOLATILITY:
            adjustments.update({
                'position_size_multiplier': 0.7,
                'stop_loss_adjustment': 0.8,
                'holding_period_adjustment': 0.6
            })
        elif market_conditions.regime == MarketRegime.CRISIS:
            adjustments.update({
                'position_size_multiplier': 0.5,
                'stop_loss_adjustment': 0.7,
                'holding_period_adjustment': 0.4
            })
        elif market_conditions.regime in [MarketRegime.BULL_TRENDING, MarketRegime.BEAR_TRENDING]:
            adjustments.update({
                'position_size_multiplier': 1.2,
                'take_profit_adjustment': 1.3,
                'holding_period_adjustment': 1.5
            })
        
        return adjustments
    
    def _check_correlation_limits(self, symbol: str) -> Dict:
        """بررسی محدودیت‌های همبستگی"""
        return {
            'correlation_ok': True,
            'max_correlation': 0.3,
            'current_correlation': 0.1,
            'correlated_positions': []
        }
    
    def _estimate_stress_impact(self, signal: AdvancedTradingSignal) -> Dict:
        """تخمین تأثیر stress test"""
        return {
            'worst_case_loss': signal.risk_amount * 2,
            'expected_loss': signal.risk_amount,
            'probability_of_loss': 1 - signal.win_probability,
            'recovery_time_estimate': 30  # روز
        }
            
    def _get_stress_test_scenarios(self) -> List[Dict]:
        """سناریوهای تست استرس"""
        return [
            {
                'name': 'Market Crash',
                'price_changes': {
                    'BTC/USDT': -0.30,
                    'ETH/USDT': -0.35,
                    'default': -0.25
                }
            },
            {
                'name': 'Flash Crash',
                'price_changes': {
                    'BTC/USDT': -0.15,
                    'ETH/USDT': -0.20,
                    'default': -0.12
                }
            },
            {
                'name': 'Volatility Spike',
                'price_changes': {
                    'BTC/USDT': 0.20,
                    'ETH/USDT': -0.18,
                    'default': 0.10
                }
            },
            {
                'name': 'Regime Change',
                'price_changes': {
                    'BTC/USDT': -0.08,
                    'ETH/USDT': -0.10,
                    'default': -0.05
                }
            }
        ]
        
    def update_real_time_data(self, symbol: str = None):
        """برونزرسانی داده‌های real-time"""
        try:
            if symbol:
                symbols = [symbol]
            else:
                symbols = list(self.market_data_cache.keys())
                
            if not symbols:
                symbols = ['BTC/USDT']  # پیش‌فرض
                
            # برونزرسانی داده‌های بازار
            updated_data = self.fetch_multiple_symbols(symbols, limit=100)
            
            # برونزرسانی پوزیشن‌ها
            self.money_manager.update_positions(updated_data)
            
            # برونزرسانی تحلیل‌ها
            if self.current_data is not None:
                self._initialize_analyzers()
                
            # به‌روزرسانی پارامترهای تطبیقی استراتژی
            if hasattr(self.trading_strategy, 'update_adaptive_parameters'):
                current_performance = {
                    'success_rate': self.performance_tracking['successful_signals'] / max(1, self.performance_tracking['total_signals']),
                    'average_confidence': self.performance_tracking['average_confidence']
                }
                self.trading_strategy.update_adaptive_parameters(current_performance)
                
            logger.info("✅ داده‌های real-time برونزرسانی شد")
            
        except Exception as e:
            logger.error(f"خطا در برونزرسانی real-time: {e}")
            
    def enable_auto_trading(self, enabled: bool = True):
        """فعال/غیرفعال کردن معاملات خودکار"""
        self.auto_trading_enabled = enabled
        status = "فعال" if enabled else "غیرفعال"
        logger.info(f"🤖 معاملات خودکار: {status}")
        
    def get_portfolio_status(self) -> Dict:
        """دریافت وضعیت کامل پرتفویو"""
        try:
            real_time_status = self.money_manager.get_real_time_status()
            performance_report = self.money_manager.generate_performance_report()
            
            # اضافه کردن آمار NEOWave
            neowave_stats = {
                'signals_generated': len(self.signals_history),
                'average_signal_confidence': self.performance_tracking['average_confidence'],
                'success_rate': self.performance_tracking['successful_signals'] / max(1, self.performance_tracking['total_signals']),
                'total_signals': self.performance_tracking['total_signals'],
                'successful_signals': self.performance_tracking['successful_signals'],
                'failed_signals': self.performance_tracking['failed_signals'],
                'best_signal_confidence': self.performance_tracking['best_signal'].confidence if self.performance_tracking['best_signal'] else 0,
                'worst_signal_confidence': self.performance_tracking['worst_signal'].confidence if self.performance_tracking['worst_signal'] else 0
            }
            
            return {
                'real_time_status': real_time_status,
                'performance_summary': performance_report,
                'risk_metrics': self.money_manager.calculate_advanced_metrics().__dict__,
                'neowave_statistics': neowave_stats,
                'open_positions': [
                    {
                        'id': pos.position_id,
                        'symbol': pos.symbol,
                        'type': pos.position_type,
                        'size': pos.quantity,
                        'entry_price': pos.entry_price,
                        'current_price': pos.current_price,
                        'pnl': pos.unrealized_pnl,
                        'pnl_percent': pos.unrealized_pnl_percent,
                        'wave_analysis': getattr(pos, 'wave_analysis', {}),
                        'signal_id': getattr(pos, 'signal_id', '')
                    }
                    for pos in self.money_manager.positions
                ],
                'auto_trading': self.auto_trading_enabled,
                'last_update': datetime.now().isoformat(),
                'system_health': self._check_system_health()
            }
            
        except Exception as e:
            logger.error(f"خطا در دریافت وضعیت: {e}")
            return {}
    
    def _check_system_health(self) -> Dict:
        """بررسی سلامت سیستم"""
        health = {
            'overall_status': 'healthy',
            'components': {},
            'warnings': [],
            'errors': []
        }
        
        try:
            # بررسی اتصال داده
            if self.current_data is None or self.current_data.empty:
                health['components']['data_connection'] = 'error'
                health['errors'].append('No market data available')
            else:
                health['components']['data_connection'] = 'healthy'
            
            # بررسی تحلیلگرها
            analyzers = ['elliott_analyzer', 'trading_strategy', 'money_manager']
            for analyzer in analyzers:
                if hasattr(self, analyzer) and getattr(self, analyzer) is not None:
                    health['components'][analyzer] = 'healthy'
                else:
                    health['components'][analyzer] = 'error'
                    health['errors'].append(f'{analyzer} not initialized')
            
            # بررسی کارایی
            if len(self.signals_history) > 0:
                recent_signals = [s for s in self.signals_history if 
                                (datetime.now() - s['timestamp']).days < 7]
                if len(recent_signals) == 0:
                    health['warnings'].append('No recent signals generated')
            
            # تعیین وضعیت کلی
            if health['errors']:
                health['overall_status'] = 'error'
            elif health['warnings']:
                health['overall_status'] = 'warning'
                
        except Exception as e:
            health['overall_status'] = 'error'
            health['errors'].append(f'Health check failed: {str(e)}')
        
        return health
            
    def close_position(self, position_id: str, reason: str = "Manual") -> Dict:
        """بستن پوزیشن"""
        try:
            # پیدا کردن پوزیشن
            position = None
            for pos in self.money_manager.positions:
                if pos.position_id == position_id:
                    position = pos
                    break
                    
            if not position:
                return {'status': 'error', 'message': 'Position not found'}
                
            # برونزرسانی قیمت فعلی
            symbol_data = self.market_data_cache.get(position.symbol)
            if symbol_data is not None and not symbol_data.empty:
                current_price = symbol_data['close'].iloc[-1]
            else:
                current_price = position.current_price
                
            # بستن پوزیشن
            closed_position = self.money_manager.close_position(position_id, current_price, reason)
            
            if closed_position:
                # به‌روزرسانی آمار عملکرد
                if closed_position.realized_pnl > 0:
                    self.performance_tracking['successful_signals'] += 1
                else:
                    self.performance_tracking['failed_signals'] += 1
                
                return {
                    'status': 'success',
                    'position_id': closed_position.position_id,
                    'symbol': closed_position.symbol,
                    'pnl': closed_position.realized_pnl,
                    'pnl_percent': closed_position.realized_pnl_percent,
                    'exit_price': closed_position.exit_price,
                    'holding_period': closed_position.holding_period_hours,
                    'close_reason': reason
                }
            else:
                return {'status': 'error', 'message': 'Failed to close position'}
                
        except Exception as e:
            logger.error(f"خطا در بستن پوزیشن: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_signal_history(self, limit: int = 50) -> List[Dict]:
        """دریافت تاریخچه سیگنال‌ها"""
        try:
            recent_signals = self.signals_history[-limit:] if limit else self.signals_history
            
            signal_summary = []
            for entry in recent_signals:
                signal = entry['signal']
                summary = {
                    'timestamp': entry['timestamp'].isoformat(),
                    'signal_id': signal.signal_id,
                    'symbol': signal.symbol,
                    'signal_type': signal.signal_type.value,
                    'confidence': signal.confidence,
                    'confidence_level': signal.confidence_level.value,
                    'entry_price': signal.entry_price,
                    'risk_reward_ratio': signal.risk_reward_ratio,
                    'wave_position': signal.wave_position,
                    'market_regime': signal.market_conditions.regime.value,
                    'performance': entry.get('performance')
                }
                signal_summary.append(summary)
            
            return signal_summary
            
        except Exception as e:
            logger.error(f"خطا در دریافت تاریخچه سیگنال‌ها: {e}")
            return []
    
    def export_analysis_results(self, format: str = 'json') -> str:
        """صادرات نتایج تحلیل"""
        try:
            if not self.analysis_results:
                return "هیچ نتیجه تحلیلی برای صادرات وجود ندارد"
            
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'analysis_results': self.analysis_results,
                'signals_history': self.get_signal_history(),
                'portfolio_status': self.get_portfolio_status(),
                'system_config': {
                    'initial_capital': self.initial_capital,
                    'auto_trading_enabled': self.auto_trading_enabled,
                    'money_management_config': self.money_manager.config
                }
            }
            
            if format == 'json':
                import json
                return json.dumps(export_data, indent=2, default=str)
            elif format == 'csv':
                # برای CSV، فقط خلاصه‌ای از اطلاعات
                import csv
                import io
                output = io.StringIO()
                
                # صادرات سیگنال‌ها
                if self.signals_history:
                    writer = csv.writer(output)
                    writer.writerow(['Timestamp', 'Symbol', 'Signal_Type', 'Confidence', 'Entry_Price', 'Wave_Position'])
                    
                    for entry in self.signals_history:
                        signal = entry['signal']
                        writer.writerow([
                            entry['timestamp'],
                            signal.symbol,
                            signal.signal_type.value,
                            signal.confidence,
                            signal.entry_price,
                            signal.wave_position
                        ])
                
                return output.getvalue()
            else:
                return str(export_data)
                
        except Exception as e:
            logger.error(f"خطا در صادرات: {e}")
            return f"خطا در صادرات: {str(e)}"
            
    def generate_report(self, results: Dict = None):
        """تولید گزارش تحلیل جامع"""
        if results is None:
            results = self.analysis_results
            
        if not results:
            logger.warning("⚠️ نتایجی برای گزارش وجود ندارد")
            return None
            
        logger.info("📝 تولید گزارش تحلیل...")
        
        # گزارش تحلیل NEOWave
        neowave_report = self._generate_neowave_report(results)
        
        # گزارش مدیریت سرمایه
        portfolio_report = self._generate_portfolio_report()
        
        # گزارش سیگنال‌های پیشرفته
        signals_report = self._generate_signals_report()
        
        # ترکیب گزارش‌ها
        complete_report = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║         🌊📊 گزارش جامع NEOWave & مدیریت سرمایه پیشرفته                  ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ 📅 تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                    ║
║ 💻 نسخه: NEOWave Advanced System v2.0                                     ║
╚═══════════════════════════════════════════════════════════════════════════════╝

{neowave_report}

{portfolio_report}

{signals_report}

╔═══════════════════════════════════════════════════════════════════════════════╗
║                    🎯 خلاصه توصیه‌ها و راهکارهای عملی                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝

{self._generate_advanced_recommendations_summary(results)}

╔═══════════════════════════════════════════════════════════════════════════════╗
║                          📊 آمار عملکرد سیستم                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝

{self._generate_system_performance_summary()}

╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        
        # ذخیره گزارش
        filename = f"complete_neowave_advanced_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(complete_report)
            
        logger.info(f"✅ گزارش کامل در فایل {filename} ذخیره شد")
        print(complete_report)
        
        return complete_report
    
    def _generate_neowave_report(self, results: Dict) -> str:
        """تولید گزارش تحلیل NEOWave"""
        report = f"""
🔍 نقاط پیوت:
   - تعداد: {results.get('pivots', {}).get('count', 0)}
   
🔷 تحلیل فرکتال:
   - بعد فرکتال: {results.get('fractal', {}).get('dimension', 0):.3f}
   - فرکتال‌های صعودی: {results.get('fractal', {}).get('bullish_fractals', 0)}
   - فرکتال‌های نزولی: {results.get('fractal', {}).get('bearish_fractals', 0)}
   
🔷 تحلیل پیشرفته فرکتال:
   - تعداد کل فرکتال‌های شناسایی شده: {results.get('fractal', {}).get('advanced', {}).get('total_fractals', 0)}
   - رژیم بازار: {results.get('fractal', {}).get('advanced', {}).get('market_regime', 'نامشخص')}
   - قدرت روند: {results.get('fractal', {}).get('advanced', {}).get('trend_strength', 0):.2%}
   - سطح آشوب: {results.get('fractal', {}).get('advanced', {}).get('chaos_level', 0):.2%}
   - قابلیت پیش‌بینی: {results.get('fractal', {}).get('advanced', {}).get('predictability', 0):.2%}
   
⚡ امواج شتابدار:
   - تعداد: {results.get('impulse_waves', {}).get('count', 0)}
   
⚡ امواج شتابدار پیشرفته:
   - تعداد کل: {results.get('impulse_waves', {}).get('advanced', {}).get('total_count', 0)}
   - امواج معتبر: {results.get('impulse_waves', {}).get('advanced', {}).get('valid_count', 0)}
   - اطمینان بالا: {results.get('impulse_waves', {}).get('advanced', {}).get('high_confidence_count', 0)}
   - میانگین اطمینان: {results.get('impulse_waves', {}).get('advanced', {}).get('average_confidence', 0):.1%}
"""

        # نمایش بهترین امواج شتابدار
        best_waves = results.get('impulse_waves', {}).get('advanced', {}).get('best_waves', [])
        if best_waves:
            report += """
   
⚡ امواج شتابدار کلیدی:"""
            for i, wave in enumerate(best_waves[:3], 1):
                report += f"""
   {i}. {wave['type']} ({wave.get('confidence_level', 'نامشخص')})
      - شناسه: {wave['id']}
      - اطمینان: {wave['confidence']*100:.0f}%
      - جهت: {wave.get('direction', 'نامشخص')}
      - قیمت شروع: ${wave['start_price']:,.2f}
      - قیمت پایان: ${wave['end_price']:,.2f}
      - مدت زمان: {wave['duration']} کندل
      - وضعیت: {'✅ معتبر' if wave['is_valid'] else '⚠️ نامعتبر'}
      - خطاها: {wave['validation_errors']}
      - هشدارها: {wave['validation_warnings']}"""
                
                # نمایش متریک‌های پیشرفته
                if 'advanced_metrics' in wave:
                    metrics = wave['advanced_metrics']
                    report += f"""
      
      📊 متریک‌های پیشرفته:
      - دقت فیبوناچی: {metrics['fibonacci_accuracy']}
      - کیفیت کانال‌بندی: {metrics['channeling_quality']}
      - تأیید حجم: {metrics['volume_confirmation']}
      - تأیید مومنتوم: {metrics['momentum_confirmation']}
      - یکپارچگی ساختاری: {metrics['structural_integrity']}
      - بعد فرکتال: {metrics['fractal_dimension']}
      - نمای هرست: {metrics['hurst_exponent']}
      - قدرت پیش‌بینی: {metrics['predictive_power']}
      - امتیاز کلی کیفیت: {metrics.get('overall_quality_score', 'N/A')}"""
                
                # نمایش پروژکشن‌ها
                if 'projections' in wave and wave['projections']:
                    projections = wave['projections']
                    if 'price_targets' in projections:
                        targets = projections['price_targets']
                        report += f"""
      
      🎯 اهداف قیمتی:"""
                        for ratio, price in targets.items():
                            report += f"""
      - {ratio}: ${price:,.2f}"""
                    
                    if 'invalidation_level' in projections:
                        report += f"""
      - سطح باطل‌سازی: ${projections['invalidation_level']:,.2f}"""
                
                # نمایش پیش‌بینی موج بعدی
                if 'next_wave_prediction' in wave and wave['next_wave_prediction']:
                    next_wave = wave['next_wave_prediction']
                    report += f"""
      
      🔮 پیش‌بینی موج بعدی:
      - نوع: {next_wave['type']}
      - جهت: {next_wave['direction']}
      - اطمینان: {next_wave['confidence']}
      - اصلاح مورد انتظار: {next_wave['expected_retracement']}"""

        # آمار انواع امواج
        wave_types = results.get('impulse_waves', {}).get('advanced', {}).get('wave_types', {})
        if wave_types:
            report += """
   
📈 توزیع انواع امواج:"""
            for wave_type, count in wave_types.items():
                report += f"""
   - {wave_type}: {count} موج"""

        report += f"""
   
🔺 الگوهای خاص:
   - مثلث: {'شناسایی شد' if results.get('triangle') else 'شناسایی نشد'}
   - دیامتریک: {'شناسایی شد' if results.get('diametric') else 'شناسایی نشد'}
"""

        # اضافه کردن بخش سیمتریک پیشرفته
        if results.get('advanced_symmetric'):
            symmetric = results['advanced_symmetric']
            report += f"""

🔄 الگوی سیمتریک پیشرفته:
   - شناسه الگو: {symmetric['pattern_id']}
   - نوع الگو: {symmetric['pattern_type']}
   - نوع تقارن: {symmetric['symmetry_type']}
   - کیفیت تقارن: {symmetric['symmetry_quality']}
   - اعتماد کلی: {symmetric['overall_confidence']:.2%}
   - تکمیل الگو: {symmetric['pattern_completion']:.2%}
   - امتیاز اعتبارسنجی: {symmetric['validation_score']:.2%}
   - معنی‌داری آماری: {symmetric['statistical_significance']:.2%}
   - قدرت الگو: {symmetric['strength_rating']}
   - توصیه معاملاتی: {symmetric['trade_recommendation']}
   - سطح ریسک: {symmetric['risk_assessment'].get('risk_level', 'نامشخص')}
   
🔍 متریک‌های تقارن پیشرفته:
   - تقارن فضایی: {symmetric['symmetry_metrics']['spatial_symmetry']:.2%}
   - تقارن زمانی: {symmetric['symmetry_metrics']['temporal_symmetry']:.2%}
   - تقارن دامنه: {symmetric['symmetry_metrics']['amplitude_symmetry']:.2%}
   - تقارن فرکانس: {symmetric['symmetry_metrics']['frequency_symmetry']:.2%}
   - تقارن فاز: {symmetric['symmetry_metrics']['phase_symmetry']:.2%}
   - تقارن هارمونیک: {symmetric['symmetry_metrics']['harmonic_symmetry']:.2%}
   - تقارن فرکتالی: {symmetric['symmetry_metrics']['fractal_symmetry']:.2%}
   - تقارن آماری: {symmetric['symmetry_metrics']['statistical_symmetry']:.2%}
   - آنتروپی اطلاعات: {symmetric['symmetry_metrics']['information_entropy']:.3f}
   - نمای لیاپانوف: {symmetric['symmetry_metrics']['lyapunov_exponent']:.3f}
   - بعد همبستگی: {symmetric['symmetry_metrics']['correlation_dimension']:.3f}
   
🔍 تحلیل هندسی:
   - نقطه مرکز: ({symmetric['geometric_analysis']['center_point'][0]:.1f}, {symmetric['geometric_analysis']['center_point'][1]:.2f})
   - محور تقارن: {symmetric['geometric_analysis']['symmetry_axis']:.2f}
   - دقت انعکاس: {symmetric['geometric_analysis']['reflection_accuracy']:.2%}
   - زاویه چرخش: {symmetric['geometric_analysis']['rotation_angle']:.2f}°
   - فاکتور مقیاس: {symmetric['geometric_analysis']['scaling_factor']:.3f}
   - تعادل هندسی: {symmetric['geometric_analysis']['geometric_balance']:.2%}
   - نسبت ابعاد: {symmetric['geometric_analysis']['aspect_ratio']:.3f}
   - تراز نسبت طلایی: {symmetric['geometric_analysis']['golden_ratio_alignment']:.2%}
   
🎯 اهداف و پروژکشن‌ها:"""
            
            # نمایش اهداف قیمتی
            targets = symmetric['projections']['post_pattern_targets']
            for target_name, target_price in targets.items():
                report += f"""
   - {target_name}: ${target_price:,.2f}"""
            
            # نمایش پروژکشن‌های زمانی
            time_proj = symmetric['projections']['time_projections']
            report += f"""
   
⏰ پروژکشن‌های زمانی:"""
            for time_name, duration in time_proj.items():
                report += f"""
   - {time_name}: {duration} کندل"""
            
            # نمایش سطوح مهم
            invalidation = symmetric['projections']['invalidation_levels']
            report += f"""
   
⚠️ سطوح باطل‌سازی:"""
            for level_name, level_price in invalidation.items():
                report += f"""
   - {level_name}: ${level_price:,.2f}"""
            
            # نمایش توزیع احتمال
            prob_dist = symmetric['projections']['probability_distribution']
            report += f"""
   
📊 توزیع احتمال:"""
            for scenario, probability in prob_dist.items():
                report += f"""
   - {scenario}: {probability:.1%}"""
            
            # تحلیل محیط بازار
            market_ctx = symmetric['market_context']
            report += f"""
   
🌍 محیط بازار:
   - جهت روند: {market_ctx.get('trend_direction', 'نامشخص')}
   - قدرت روند: {market_ctx.get('trend_strength', 0):.2f}%
   - سطح نوسانات: {market_ctx.get('volatility_level', 0):.2f}%
   - موقعیت الگو: {market_ctx.get('pattern_position', 'نامشخص')}
   - احساسات بازار: {market_ctx.get('market_sentiment', 'نامشخص')}
   
🤖 تحلیل Machine Learning:
   - اعتماد ML: {symmetric['ml_features']['ml_confidence']:.2%}
   - امتیاز ناهنجاری: {symmetric['ml_features']['anomaly_score']:.2%}
   - تعداد ویژگی‌ها: {symmetric['ml_features']['features_count']}
   
📈 تحلیل امواج:
   - تعداد کل امواج: {symmetric['waves_analysis']['total_waves']}
   - قدرت موج مرکزی: {symmetric['waves_analysis']['center_wave_strength']:.2f}x
   - میانگین طول امواج: {symmetric['waves_analysis']['average_wave_length']:.2f}
   - میانگین مدت امواج: {symmetric['waves_analysis']['average_wave_duration']} کندل
   - الگوی جهت: {' → '.join(symmetric['waves_analysis']['direction_pattern'])}
   
⚖️ ارزیابی ریسک:
   - ریسک نوسانات: {symmetric['risk_assessment'].get('volatility_risk', 0):.2%}
   - ریسک زمانی: {symmetric['risk_assessment'].get('time_risk', 0):.2%}
   - ریسک ساختاری: {symmetric['risk_assessment'].get('structural_risk', 0):.2%}
   - ریسک کلی: {symmetric['risk_assessment'].get('overall_risk', 0):.2%}"""

        else:
            report += f"""

🔄 الگوی سیمتریک: شناسایی نشد"""

        # نمایش خلاصه کلی
        symmetric_summary = results.get('symmetric_summary', {})
        if symmetric_summary.get('total_patterns', 0) > 0:
            report += f"""
   
📋 خلاصه کلی الگوهای سیمتریک:
   - تعداد کل الگوها: {symmetric_summary['total_patterns']}
   - میانگین اعتماد: {symmetric_summary['average_confidence']:.2%}
   
   انواع الگوها:"""
            for pattern_type, count in symmetric_summary.get('pattern_types', {}).items():
                report += f"""
   - {pattern_type}: {count} الگو"""
            
            report += f"""
   
   توزیع کیفیت:"""
            for quality, count in symmetric_summary.get('quality_distribution', {}).items():
                report += f"""
   - {quality}: {count} الگو"""

        # تحلیل نسبت‌های پیشرفته
        if results.get('advanced_ratios'):
            adv_ratios = results['advanced_ratios']
            summary = adv_ratios.get('summary', {})
            
            report += f"""

🔢 تحلیل نسبت‌های پیشرفته:
   - تعداد نسبت‌های تحلیل شده: {summary.get('total_ratios_analyzed', 0)}
   - امواج ممتد شناسایی شده: {summary.get('valid_extensions', 0)}
   - نسبت‌های با اطمینان بالا: {summary.get('high_confidence_ratios', 0)}
   - تحلیل آماری: {'✅ انجام شده' if summary.get('statistical_analysis_completed') else '❌ انجام نشده'}
   - تحلیل هندسی: {'✅ انجام شده' if summary.get('geometric_analysis_completed') else '❌ انجام نشده'}
   - پیش‌بینی ML: {'✅ فعال' if summary.get('ml_predictions_available') else '❌ غیرفعال'}"""

            # نمایش جزئیات امواج ممتد
            extended_validations = adv_ratios.get('extended_wave_validations', {})
            valid_extensions = [k for k, v in extended_validations.items() if v.get('is_extended', False)]
            
            if valid_extensions:
                report += """
   
🚀 امواج ممتد شناسایی شده:"""
                for wave_key in valid_extensions[:3]:  # نمایش 3 موج اول
                    validation = extended_validations[wave_key]
                    report += f"""
   • {wave_key}:
     - نسبت امتداد: {validation.get('extension_ratio', 0):.3f}
     - اطمینان: {validation.get('confidence_score', 0):.2%}
     - دقت فیبوناچی: {validation.get('fibonacci_accuracy', 0):.2%}
     - انطباق NEOWave: {'✅' if validation.get('neowave_compliance', False) else '❌'}"""

            # نمایش بهترین نسبت‌های فیبوناچی
            internal_ratios = adv_ratios.get('internal_ratios', {})
            classic_ratios = internal_ratios.get('classic_ratios', {})
            
            if classic_ratios:
                high_confidence_ratios = [
                    (name, ratio) for name, ratio in classic_ratios.items()
                    if hasattr(ratio, 'confidence_score') and ratio.confidence_score > 0.7
                ]
                
                if high_confidence_ratios:
                    report += """
   
🎯 نسبت‌های فیبوناچی برتر:"""
                    for name, ratio in high_confidence_ratios[:5]:  # 5 نسبت برتر
                        report += f"""
   • {name}:
     - نسبت: {ratio.target_ratio:.3f} ≈ {ratio.closest_fibonacci.value:.3f}
     - انحراف: {ratio.deviation_percent:.2f}%
     - اطمینان: {ratio.confidence_score:.2%}
     - معناداری آماری: {ratio.statistical_significance:.2%}"""

        # اضافه کردن تحلیل زمانی پیشرفته
        if results.get('advanced_time_analysis'):
            time_analysis = results['advanced_time_analysis']
            report += f"""

⏰ تحلیل زمانی پیشرفته:
   - شناسه تحلیل: {time_analysis['analysis_id']}
   - تایم‌فریم: {time_analysis['timeframe']}
   - کیفیت تحلیل: {time_analysis['analysis_quality']:.2%}
   - قابلیت اطمینان: {time_analysis['reliability_score']:.2%}
   
📊 متریک‌های زمانی:
   - مدت کل: {time_analysis['time_metrics']['duration']:.1f}
   - سرعت متوسط: {time_analysis['time_metrics']['velocity']:.3f}
   - شتاب: {time_analysis['time_metrics']['acceleration']:.3f}
   - پایداری مومنتوم: {time_analysis['time_metrics']['momentum_persistence']:.2%}
   - خوشه‌بندی نوسانات: {time_analysis['time_metrics']['volatility_clustering']:.2%}
   - نمای هرست: {time_analysis['time_metrics']['hurst_exponent']:.3f}
   - بعد فرکتال: {time_analysis['time_metrics']['fractal_dimension']:.3f}
   - آنتروپی: {time_analysis['time_metrics']['entropy']:.3f}
   - طول همبستگی: {time_analysis['time_metrics']['correlation_length']:.1f}
   
🔄 تحلیل چرخه‌ها:
   - تعداد چرخه‌های شناسایی شده: {len(time_analysis['cycles'])}"""
            
            if time_analysis.get('dominant_cycle'):
                dominant = time_analysis['dominant_cycle']
                report += f"""
   - چرخه غالب: {dominant['type']} (دوره: {dominant['period']:.1f}, قدرت: {dominant['strength']:.2%})"""
            
            # نمایش بهترین چرخه‌ها
            top_cycles = time_analysis['cycles'][:3]
            if top_cycles:
                report += """
   
   چرخه‌های کلیدی:"""
                for i, cycle in enumerate(top_cycles, 1):
                    report += f"""
   {i}. {cycle['type']} - دوره: {cycle['period']:.1f}, قدرت: {cycle['strength']:.2%}"""
            
            # پروژکشن‌های زمانی
            if time_analysis['time_projections']:
                report += f"""
   
🎯 پروژکشن‌های زمانی:
   - تعداد پروژکشن‌ها: {len(time_analysis['time_projections'])}"""
                
                for i, proj in enumerate(time_analysis['time_projections'][:3], 1):
                    report += f"""
   {i}. {proj['type']} - زمان هدف: {proj['target_time']:.1f} ({proj['confidence_level']})"""
            
            # مناطق بحرانی
            if time_analysis['critical_time_zones']:
                report += f"""
   
⚠️ مناطق زمانی بحرانی:
   - تعداد مناطق: {len(time_analysis['critical_time_zones'])}"""
                
                for i, zone in enumerate(time_analysis['critical_time_zones'][:3], 1):
                    report += f"""
   {i}. مرکز: {zone['center_time']:.1f}, قدرت: {zone['strength']}, احتمال: {zone['probability']:.1%}"""
        
        return report
        
    def _generate_portfolio_report(self) -> str:
        """تولید گزارش مدیریت سرمایه"""
        try:
            status = self.money_manager.get_real_time_status()
            performance = self.money_manager.generate_performance_report()
            metrics = self.money_manager.calculate_advanced_metrics()
            
            report = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                   💼 گزارش مدیریت سرمایه پیشرفته                          ║
╚═══════════════════════════════════════════════════════════════════════════════╝

💰 وضعیت سرمایه:
   - سرمایه اولیه: ${self.money_manager.initial_capital:,.2f}
   - سرمایه فعلی: ${status['capital']['total']:,.2f}
   - سرمایه در دسترس: ${status['capital']['available']:,.2f}
   - سرمایه سرمایه‌گذاری شده: ${status['capital']['invested']:,.2f}
   - PnL تحقق نیافته: ${status['capital']['unrealized_pnl']:,.2f}

📊 آمار معاملات:
   - تعداد کل معاملات: {performance['trading_statistics']['total_trades']}
   - معاملات برنده: {performance['trading_statistics']['wins']}
   - معاملات بازنده: {performance['trading_statistics']['losses']}
   - نرخ برد: {performance['trading_statistics']['win_rate_percent']:.1f}%
   - فاکتور سود: {performance['trading_statistics']['profit_factor']:.2f}
   - ROI: {performance['portfolio_summary']['roi_percent']:.2f}%

⚠️ متریک‌های ریسک:
   - VAR 95%: {metrics.var_95:.2f}%
   - حداکثر افت: {metrics.maximum_drawdown:.2f}%
   - نسبت شارپ: {metrics.sharpe_ratio:.3f}
   - نسبت سورتینو: {metrics.sortino_ratio:.3f}
   - نوسان: {metrics.volatility:.2f}%

🎯 پوزیشن‌های فعلی:
   - تعداد پوزیشن‌ها: {status['positions']['count']}
   - درصد exposure: {status['positions']['exposure_percent']:.1f}%
   - ارزش کل: ${status['positions']['total_value']:,.2f}
"""

            # نمایش پوزیشن‌های فعلی
            if self.money_manager.positions:
                report += """
   
📋 جزئیات پوزیشن‌های فعلی:"""
                for i, pos in enumerate(self.money_manager.positions[:5], 1):
                    pnl_emoji = "💚" if pos.unrealized_pnl > 0 else "💔"
                    wave_info = getattr(pos, 'wave_analysis', {})
                    signal_id = getattr(pos, 'signal_id', 'N/A')
                    
                    report += f"""
   {i}. {pos.symbol} ({pos.position_type})
      - حجم: {pos.quantity:.6f}
      - قیمت ورود: ${pos.entry_price:,.2f}
      - قیمت فعلی: ${pos.current_price:,.2f}
      - PnL: {pnl_emoji} ${pos.unrealized_pnl:,.2f} ({pos.unrealized_pnl_percent:.2f}%)
      - مدت زمان: {pos.duration_hours:.1f} ساعت
      - شناسه سیگنال: {signal_id}
      - تحلیل موج: {wave_info.get('wave_position', 'نامشخص')}"""

            return report
            
        except Exception as e:
            logger.error(f"خطا در تولید گزارش پرتفویو: {e}")
            return "خطا در تولید گزارش مدیریت سرمایه"
    
    def _generate_signals_report(self) -> str:
        """تولید گزارش سیگنال‌های پیشرفته"""
        if not self.signals_history:
            return """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    📡 گزارش سیگنال‌های معاملاتی                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

⚠️ هیچ سیگنالی تولید نشده است.
"""
        
        recent_signals = self.signals_history[-5:]  # 5 سیگنال اخیر
        
        report = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    📡 گزارش سیگنال‌های معاملاتی پیشرفته                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝

📊 آمار کلی سیگنال‌ها:
   - تعداد کل سیگنال‌ها: {self.performance_tracking['total_signals']}
   - سیگنال‌های موفق: {self.performance_tracking['successful_signals']}
   - سیگنال‌های ناموفق: {self.performance_tracking['failed_signals']}
   - نرخ موفقیت: {self.performance_tracking['successful_signals'] / max(1, self.performance_tracking['total_signals']):.1%}
   - میانگین اطمینان: {self.performance_tracking['average_confidence']:.1%}

🔥 آخرین سیگنال‌های تولید شده:"""
        
        for i, entry in enumerate(recent_signals, 1):
            signal = entry['signal']
            market_conditions = entry['market_conditions']
            
            report += f"""

{i}. سیگنال {signal.signal_id}:
   ⏰ زمان: {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
   📊 نماد: {signal.symbol}
   🎯 نوع: {signal.signal_type.value}
   💪 اطمینان: {signal.confidence:.1%} ({signal.confidence_level.value})
   💰 قیمت ورود: ${signal.entry_price:,.2f}
   🛡️ حد ضرر: ${signal.stop_loss:,.2f}
   🎯 اهداف: {', '.join([f'${tp:,.2f}' for tp in signal.take_profits[:3]])}
   ⚖️ نسبت R/R: {signal.risk_reward_ratio:.1f}
   🌊 موقعیت موج: {signal.wave_position}
   🏭 رژیم بازار: {market_conditions.regime.value}
   🤖 پیش‌بینی ML: {signal.ml_predictions.price_direction_prob:.1%}
   📏 حجم پیشنهادی: {signal.suggested_position_size:.1%}"""
        
        # بهترین و بدترین سیگنال
        if self.performance_tracking['best_signal']:
            best = self.performance_tracking['best_signal']
            report += f"""

🏆 بهترین سیگنال:
   - شناسه: {best.signal_id}
   - اطمینان: {best.confidence:.1%}
   - نوع: {best.signal_type.value}
   - موقعیت موج: {best.wave_position}"""
        
        if self.performance_tracking['worst_signal']:
            worst = self.performance_tracking['worst_signal']
            report += f"""

📉 ضعیف‌ترین سیگنال:
   - شناسه: {worst.signal_id}
   - اطمینان: {worst.confidence:.1%}
   - نوع: {worst.signal_type.value}
   - موقعیت موج: {worst.wave_position}"""
        
        return report
    
    def _generate_advanced_recommendations_summary(self, results: Dict) -> str:
        """تولید خلاصه توصیه‌های پیشرفته"""
        recommendations = []
        
        # توصیه‌های تحلیلی
        if results.get('advanced_trading_signal'):
            signal = results['advanced_trading_signal']
            mm_rec = signal.money_management.get('mm_recommendation', 'بررسی سیگنال معاملاتی')
            recommendations.append(f"📈 {mm_rec}")
            
            # توصیه‌های بر اساس اطمینان
            if signal.confidence > 0.8:
                recommendations.append("⭐ سیگنال با اطمینان بالا - اجرای سریع توصیه می‌شود")
            elif signal.confidence < 0.5:
                recommendations.append("⚠️ سیگنال با اطمینان پایین - انتظار برای تأیید")
            
            # توصیه‌های ریسک/ریوارد
            if signal.risk_reward_ratio >= 3:
                recommendations.append("💎 نسبت ریسک/ریوارد عالی - فرصت مناسب")
            elif signal.risk_reward_ratio < 2:
                recommendations.append("🔶 نسبت ریسک/ریوارد نامناسب - بازنگری شرایط")
        
        # توصیه‌های سیمتریک
        symmetric_pattern = results.get('advanced_symmetric')
        if symmetric_pattern:
            trade_rec = symmetric_pattern['trade_recommendation']
            confidence = symmetric_pattern['overall_confidence']
            risk_level = symmetric_pattern['risk_assessment'].get('risk_level', 'UNKNOWN')
            
            if trade_rec != 'NO_TRADE':
                emoji = "📈" if 'BUY' in trade_rec else "📉" if 'SELL' in trade_rec else "↔️"
                recommendations.append(f"{emoji} {trade_rec} - اعتماد: {confidence:.1%} - ریسک: {risk_level}")
            
            if confidence > 0.8:
                recommendations.append("⭐ الگوی سیمتریک با اعتماد بالا شناسایی شد")
            elif confidence > 0.6:
                recommendations.append("🔍 الگوی سیمتریک با اعتماد متوسط - بررسی بیشتر لازم")
        
        # توصیه‌های مدیریت ریسک
        status = self.money_manager.get_real_time_status()
        if status['positions']['exposure_percent'] > 70:
            recommendations.append("⚠️ درصد exposure بالا - کاهش پوزیشن‌ها توصیه می‌شود")
        elif status['positions']['exposure_percent'] < 20:
            recommendations.append("🟢 فرصت برای افزایش exposure موجود است")
        
        # توصیه‌های رژیم بازار
        if results.get('advanced_trading_signal'):
            regime = results['advanced_trading_signal'].market_conditions.regime
            if regime == MarketRegime.HIGH_VOLATILITY:
                recommendations.append("🌊 رژیم نوسان بالا - کاهش حجم پوزیشن‌ها")
            elif regime == MarketRegime.CRISIS:
                recommendations.append("🚨 رژیم بحرانی - حفظ نقدینگی و صبر")
            elif regime in [MarketRegime.BULL_TRENDING, MarketRegime.BEAR_TRENDING]:
                recommendations.append("📊 رژیم روندی - فرصت مناسب برای پیروی از روند")
        
        # توصیه‌های زمانی
        if results.get('advanced_time_analysis'):
            time_analysis = results['advanced_time_analysis']
            if time_analysis['reliability_score'] > 0.8:
                recommendations.append("⏰ تحلیل زمانی قابل اعتماد - رعایت پروژکشن‌های زمانی")
            if len(time_analysis['critical_time_zones']) > 0:
                recommendations.append("🎯 مناطق زمانی بحرانی شناسایی شد - آمادگی برای تغییرات")
        
        # توصیه‌های بهینه‌سازی
        optimization = results.get('portfolio_optimization', {})
        if optimization.get('recommendations'):
            recommendations.append("🔄 بهینه‌سازی پرتفویو پیشنهاد می‌شود")
        
        # توصیه‌های stress test
        stress_test = results.get('stress_test', {})
        if stress_test:
            failed_scenarios = [name for name, result in stress_test.items() 
                              if not result.get('survival', True)]
            if failed_scenarios:
                recommendations.append(f"🚨 خطر در سناریوهای: {', '.join(failed_scenarios)}")
        
        # توصیه‌های ML
        if results.get('ml_predictions'):
            ml_preds = results['ml_predictions']
            if ml_preds['confidence'] > 0.8:
                direction = "صعودی" if ml_preds['price_direction']['up'] > 0.6 else "نزولی"
                recommendations.append(f"🤖 پیش‌بینی ML با اطمینان بالا: جهت {direction}")
        
        if not recommendations:
            recommendations.append("✅ وضعیت پرتفویو مطلوب است - ادامه نظارت")
            
        return "\n".join(f"• {rec}" for rec in recommendations)
    
    def _generate_system_performance_summary(self) -> str:
        """تولید خلاصه عملکرد سیستم"""
        uptime = datetime.now() - datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        system_health = self._check_system_health()
        
        return f"""
🖥️ وضعیت سیستم:
   - حالت کلی: {system_health['overall_status'].upper()}
   - مدت فعالیت جلسه: {uptime}
   - معاملات خودکار: {'✅ فعال' if self.auto_trading_enabled else '❌ غیرفعال'}
   - نظارت real-time: {'✅ فعال' if self.real_time_monitoring else '❌ غیرفعال'}

📊 آمار تولید سیگنال:
   - کل سیگنال‌ها: {len(self.signals_history)}
   - میانگین اطمینان: {self.performance_tracking['average_confidence']:.1%}
   - نرخ موفقیت: {self.performance_tracking['successful_signals'] / max(1, self.performance_tracking['total_signals']):.1%}

🔧 وضعیت ماژول‌ها:"""
        
        for component, status in system_health['components'].items():
            emoji = "✅" if status == 'healthy' else "❌"
            component_name = component.replace('_', ' ').title()
            return f"""
   - {component_name}: {emoji} {status.upper()}"""
        
        if system_health['warnings']:
            return f"""

⚠️ هشدارها: {', '.join(system_health['warnings'])}"""
        
        if system_health['errors']:
            return f"""

❌ خطاها: {', '.join(system_health['errors'])}"""
        
        return f"""

💡 توصیه‌های سیستم:
   • برای عملکرد بهتر، داده‌ها را مرتب به‌روزرسانی کنید
   • تنظیمات ریسک را بر اساس شرایط بازار تطبیق دهید
   • از گزارش‌های دوره‌ای برای بهبود استراتژی استفاده کنید"""
        
    def run_gui(self):
        """اجرای رابط کاربری گرافیکی"""
        logger.info("🖥️ راه‌اندازی رابط کاربری...")
        
        app = QApplication(sys.argv)
        
        # تنظیمات ظاهری
        app.setStyle('Fusion')
        app.setApplicationName("NEOWave Analyzer Advanced Pro")
        app.setOrganizationName("Professional Trading Systems")
        
        # ایجاد و نمایش پنجره اصلی
        window = MainWindow(self.config)
        
        # اتصال سیستم مدیریت سرمایه به رابط کاربری
        if hasattr(window, 'set_money_manager'):
            window.set_money_manager(self.money_manager)
        
        # اتصال استراتژی پیشرفته
        if hasattr(window, 'set_trading_strategy'):
            window.set_trading_strategy(self.trading_strategy)
            
        window.show()
        
        logger.info("✅ رابط کاربری آماده است")
        
        sys.exit(app.exec_())
        
    def export_portfolio_data(self, format: str = 'json') -> str:
        """صادرات داده‌های پرتفویو"""
        return self.money_manager.export_data(format)
    
    def export_advanced_ratio_analysis(self, format: str = 'json') -> str:
        """صادرات تحلیل پیشرفته نسبت‌ها"""
        if not self.ratio_analyzer:
            return "تحلیلگر نسبت راه‌اندازی نشده"
        
        try:
            # دریافت نتایج تحلیل پیشرفته
            advanced_results = self.ratio_analyzer.calculate_advanced_internal_ratios()
            
            # صادرات با فرمت درخواستی
            exported_data = self.ratio_analyzer.export_analysis_results(advanced_results, format)
            
            # ذخیره در فایل
            filename = f"advanced_ratio_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(exported_data)
            
            logger.info(f"✅ تحلیل نسبت‌های پیشرفته در {filename} صادر شد")
            return exported_data
            
        except Exception as e:
            logger.error(f"خطا در صادرات تحلیل نسبت‌ها: {e}")
            return ""

    def get_ratio_analysis_summary(self) -> Dict[str, Any]:
        """دریافت خلاصه تحلیل نسبت‌ها"""
        if not self.ratio_analyzer:
            return {}
        
        try:
            results = self.ratio_analyzer.calculate_advanced_internal_ratios()
            
            return {
                'total_ratios': len(results.get('classic_ratios', {})),
                'high_confidence_count': sum(
                    1 for r in results.get('classic_ratios', {}).values()
                    if hasattr(r, 'confidence_score') and r.confidence_score > 0.8
                ),
                'ml_enabled': results.get('ml_predictions', {}).get('ml_enabled', False),
                'statistical_completed': bool(results.get('statistical_analysis')),
                'geometric_completed': bool(results.get('geometric_analysis')),
                'last_analysis': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"خطا در دریافت خلاصه: {e}")
            return {}
    
    def set_impulse_validation_level(self, level: str = "MEDIUM"):
        """تنظیم سطح دقت اعتبارسنجی امواج شتابدار"""
        level_mapping = {
            'HIGH': 'HIGH',
            'MEDIUM': 'MEDIUM', 
            'LOW': 'LOW'
        }
        
        if level.upper() in level_mapping and hasattr(self.impulse_analyzer, 'validation_level'):
            # این ویژگی در آینده قابل گسترش است
            logger.info(f"سطح اعتبارسنجی امواج شتابدار: {level}")
        else:
            logger.warning(f"سطح نامعتبر: {level}. از 'HIGH', 'MEDIUM', یا 'LOW' استفاده کنید")

    def get_detailed_impulse_analysis(self) -> Dict:
        """دریافت تحلیل تفصیلی امواج شتابدار"""
        if hasattr(self.impulse_analyzer, 'get_impulse_summary'):
            return self.impulse_analyzer.get_impulse_summary()
        return {}

    def get_advanced_time_analysis_summary(self) -> Dict[str, Any]:
        """دریافت خلاصه تحلیل زمانی پیشرفته"""
        try:
            if hasattr(self.time_analyzer, 'get_analysis_summary'):
                return self.time_analyzer.get_analysis_summary()
            else:
                return {}
        except Exception as e:
            logger.error(f"خطا در دریافت خلاصه تحلیل زمانی: {e}")
            return {}

    def export_advanced_time_analysis(self, format: str = 'json') -> str:
        """صادرات تحلیل زمانی پیشرفته"""
        try:
            if hasattr(self.time_analyzer, 'export_analysis_results'):
                exported_data = self.time_analyzer.export_analysis_results(format)
                
                # ذخیره در فایل
                filename = f"advanced_time_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(exported_data)
                
                logger.info(f"✅ تحلیل زمانی پیشرفته در {filename} صادر شد")
                return exported_data
            else:
                logger.warning("Time analyzer does not support export functionality")
                return ""
        except Exception as e:
            logger.error(f"خطا در صادرات تحلیل زمانی: {e}")
            return ""

    def export_symmetric_analysis(self, format: str = 'json') -> str:
        """صادرات تحلیل سیمتریک پیشرفته"""
        try:
            if hasattr(self.symmetric_analyzer, 'export_analysis_results'):
                return self.symmetric_analyzer.export_analysis_results(format)
            else:
                logger.warning("Symmetric analyzer does not support export functionality")
                return ""
        except Exception as e:
            logger.error(f"خطا در صادرات تحلیل سیمتریک: {e}")
            return ""

    def get_symmetric_analysis_summary(self) -> Dict[str, Any]:
        """دریافت خلاصه تحلیل سیمتریک"""
        try:
            if hasattr(self.symmetric_analyzer, 'get_pattern_summary'):
                return self.symmetric_analyzer.get_pattern_summary()
            else:
                return {}
        except Exception as e:
            logger.error(f"خطا در دریافت خلاصه سیمتریک: {e}")
            return {}

    def update_symmetric_config(self, new_config: Dict):
        """بروزرسانی تنظیمات تحلیلگر سیمتریک"""
        try:
            if hasattr(self.symmetric_analyzer, 'config'):
                self.symmetric_analyzer.config.update(new_config)
                logger.info(f"تنظیمات تحلیلگر سیمتریک بروزرسانی شد: {new_config}")
            else:
                logger.warning("Symmetric analyzer config update not supported")
        except Exception as e:
            logger.error(f"خطا در بروزرسانی تنظیمات: {e}")
    
    def get_trading_strategy_performance(self) -> Dict[str, Any]:
        """دریافت عملکرد استراتژی معاملاتی"""
        try:
            if hasattr(self.trading_strategy, 'performance_metrics'):
                return self.trading_strategy.performance_metrics
            else:
                return {
                    'signals_generated': len(self.signals_history),
                    'average_confidence': self.performance_tracking['average_confidence'],
                    'success_rate': self.performance_tracking['successful_signals'] / max(1, self.performance_tracking['total_signals']),
                    'best_signal_confidence': self.performance_tracking['best_signal'].confidence if self.performance_tracking['best_signal'] else 0,
                    'worst_signal_confidence': self.performance_tracking['worst_signal'].confidence if self.performance_tracking['worst_signal'] else 0
                }
        except Exception as e:
            logger.error(f"خطا در دریافت عملکرد استراتژی: {e}")
            return {}
    
    def update_trading_strategy_config(self, new_config: Dict):
        """بروزرسانی تنظیمات استراتژی معاملاتی"""
        try:
            if hasattr(self.trading_strategy, 'config'):
                self.trading_strategy.config.update(new_config)
                logger.info(f"تنظیمات استراتژی معاملاتی بروزرسانی شد: {new_config}")
            else:
                logger.warning("Trading strategy config update not supported")
        except Exception as e:
            logger.error(f"خطا در بروزرسانی تنظیمات استراتژی: {e}")
    
    def backup_system_state(self) -> str:
        """پشتیبان‌گیری از وضعیت سیستم"""
        try:
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'system_config': {
                    'initial_capital': self.initial_capital,
                    'auto_trading_enabled': self.auto_trading_enabled,
                    'risk_management_active': self.risk_management_active
                },
                'money_manager_config': self.money_manager.config,
                'trading_strategy_config': self.trading_strategy.config if self.trading_strategy else {},
                'signals_history': self.get_signal_history(),
                'performance_tracking': self.performance_tracking,
                'market_data_cache_keys': list(self.market_data_cache.keys()),
                'analysis_results_summary': {
                    'last_analysis_time': self.analysis_results.get('timestamp', 'never'),
                    'components_analyzed': list(self.analysis_results.keys()) if self.analysis_results else []
                }
            }
            
            import json
            backup_json = json.dumps(backup_data, indent=2, default=str)
            
            filename = f"neowave_system_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(backup_json)
            
            logger.info(f"✅ پشتیبان‌گیری سیستم در {filename} ذخیره شد")
            return backup_json
            
        except Exception as e:
            logger.error(f"خطا در پشتیبان‌گیری: {e}")
            return ""
    
    def restore_system_state(self, backup_file: str) -> bool:
        """بازیابی وضعیت سیستم از پشتیبان"""
        try:
            import json
            
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # بازیابی تنظیمات اصلی
            self.initial_capital = backup_data['system_config']['initial_capital']
            self.auto_trading_enabled = backup_data['system_config']['auto_trading_enabled']
            self.risk_management_active = backup_data['system_config']['risk_management_active']
            
            # بازیابی آمار عملکرد
            self.performance_tracking = backup_data['performance_tracking']
            
            # بازیابی تنظیمات مدیریت سرمایه
            self.money_manager.config.update(backup_data['money_manager_config'])
            
            logger.info(f"✅ وضعیت سیستم از {backup_file} بازیابی شد")
            return True
            
        except Exception as e:
            logger.error(f"خطا در بازیابی: {e}")
            return False

# ================= نمونه استفاده =================

def example_console_analysis():
    """نمونه تحلیل در حالت کنسول"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════════════════╗
    ║   🌊 سیستم تحلیل NEOWave - نسخه کنسول پیشرفته                           ║
    ╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # ایجاد سیستم با سرمایه اولیه
    system = NEOWaveSystem(initial_capital=10000)
    
    # اتصال به صرافی (بدون API برای تست)
    system.initialize_exchange_connection()
    
    # دریافت داده‌ها
    print("\n📊 در حال دریافت داده‌های BTC/USDT...")
    data = system.fetch_market_data(
        symbol="BTC/USDT",
        timeframe="1h",
        limit=500
    )
    
    if data is not None:
        print(f"✅ {len(data)} کندل دریافت شد")
        
        # اجرای تحلیل کامل
        print("\n🔍 در حال تحلیل...")
        results = system.run_complete_analysis()
        
        if results:
            # نمایش و ذخیره گزارش
            system.generate_report(results)
            
            # صادرات تحلیل سیمتریک
            print("\n🔄 صادرات تحلیل سیمتریک...")
            symmetric_export = system.export_symmetric_analysis('json')
            if symmetric_export:
                with open(f"symmetric_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w', encoding='utf-8') as f:
                    f.write(symmetric_export)
                print("✅ تحلیل سیمتریک صادر شد")

            # نمایش خلاصه سیمتریک
            symmetric_summary = system.get_symmetric_analysis_summary()
            if symmetric_summary.get('total_patterns', 0) > 0:
                print(f"\n🔄 خلاصه الگوهای سیمتریک:")
                print(f"   تعداد کل: {symmetric_summary['total_patterns']}")
                print(f"   میانگین اعتماد: {symmetric_summary['average_confidence']:.1%}")
            
            # صادرات تحلیل زمانی پیشرفته
            print("\n⏰ صادرات تحلیل زمانی پیشرفته...")
            time_export = system.export_advanced_time_analysis('json')
            if time_export:
                print("✅ تحلیل زمانی پیشرفته صادر شد")
            
            # نمایش وضعیت پرتفویو
            portfolio_status = system.get_portfolio_status()
            print(f"\n💼 وضعیت پرتفویو:")
            print(f"💰 سرمایه کل: ${portfolio_status['real_time_status']['capital']['total']:,.2f}")
            print(f"📊 تعداد پوزیشن‌ها: {portfolio_status['real_time_status']['positions']['count']}")
            print(f"📡 سیگنال‌های تولید شده: {portfolio_status['neowave_statistics']['signals_generated']}")
            
            # پشتیبان‌گیری از سیستم
            print("\n💾 پشتیبان‌گیری از سیستم...")
            backup_data = system.backup_system_state()
            if backup_data:
                print("✅ پشتیبان‌گیری انجام شد")
            
            print("\n✨ تحلیل کامل شد!")
        else:
            print("\n❌ خطا در تحلیل")
    else:
        print("\n❌ خطا در دریافت داده‌ها")

def example_gui_analysis():
    """نمونه اجرای رابط کاربری گرافیکی"""
    system = NEOWaveSystem(initial_capital=10000)
    system.run_gui()

def example_auto_trading():
    """نمونه معاملات خودکار"""
    print("🤖 راه‌اندازی سیستم معاملات خودکار پیشرفته...")
    
    system = NEOWaveSystem(initial_capital=10000)
    system.enable_auto_trading(True)
    
    # دریافت داده‌ها
    system.fetch_market_data("BTC/USDT")
    
    # اجرای تحلیل و معاملات خودکار
    results = system.run_complete_analysis()
    
    if results and results.get('position_execution'):
        execution = results['position_execution']
        print(f"✅ پوزیشن اجرا شد: {execution}")
    
    # بروزرسانی real-time
    import time
    for i in range(10):
        time.sleep(30)  # هر 30 ثانیه
        system.update_real_time_data()
        print(f"🔄 بروزرسانی {i+1}/10 انجام شد")

# ================= اجرای اصلی =================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='سیستم تحلیل NEOWave به روش گلن نیلی - نسخه پیشرفته v2.0'
    )
    parser.add_argument(
        '--mode', 
        choices=['console', 'gui', 'auto'], 
        default='gui',
        help='حالت اجرا: console، gui یا auto (پیش‌فرض: gui)'
    )
    parser.add_argument(
        '--symbol',
        default='BTC/USDT',
        help='نماد مورد تحلیل (پیش‌فرض: BTC/USDT)'
    )
    parser.add_argument(
        '--timeframe',
        default='1h',
        help='تایم‌فریم (پیش‌فرض: 1h)'
    )
    parser.add_argument(
        '--capital',
        type=float,
        default=10000,
        help='سرمایه اولیه (پیش‌فرض: 10000)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'console':
        example_console_analysis()
    elif args.mode == 'auto':
        example_auto_trading()
    else:
        example_gui_analysis()

# ================= README.md =================
"""
# 🌊💰 سیستم جامع تحلیل NEOWave و مدیریت سرمایه - نسخه 2.0

## ✨ ویژگی‌های جدید نسخه پیشرفته

### 🤖 مدیریت سرمایه پیشرفته:
- **محاسبه حجم بهینه با ML**: استفاده از یادگیری ماشین
- **مدل‌های ریسک پیشرفته**: VAR، CVaR، Monte Carlo
- **تشخیص رژیم بازار**: انطباق با شرایط مختلف بازار
- **بهینه‌سازی پرتفویو**: Risk Parity، Mean-Variance
- **تست استرس**: شبیه‌سازی سناریوهای مختلف
- **مانیتورینگ Real-time**: پایش لحظه‌ای ریسک

### 🔄 الگوهای سیمتریک پیشرفته:
- **تحلیل 11 نوع متریک تقارن**: فضایی، زمانی، دامنه، فرکانس، فاز، هارمونیک، فرکتالی، آماری، آنتروپی، لیاپانوف، همبستگی
- **تحلیل هندسی 8 بعدی**: نقطه مرکز، محور تقارن، دقت انعکاس، زاویه چرخش، فاکتور مقیاس، تعادل هندسی، نسبت ابعاد، تراز طلایی
- **پروژکشن‌های پیشرفته**: اهداف قیمتی چندگانه، زمان‌بندی دقیق، سطوح باطل‌سازی، توزیع احتمال
- **ادغام ML**: 50+ ویژگی، تشخیص ناهنجاری، طبقه‌بندی الگو
- **ارزیابی ریسک جامع**: ریسک نوسانات، زمانی، ساختاری، کلی

### ⏰ تحلیل زمانی پیشرفته:
- **متریک‌های زمانی کامل**: سرعت، شتاب، پایداری مومنتوم، خوشه‌بندی نوسانات، نمای هرست، بعد فرکتال، آنتروپی، نمای لیاپانوف، طول همبستگی
- **تحلیل چرخه‌های پیچیده**: فیبوناچی، هارمونیک، فوریه، موسمی با اعتبارسنجی آماری
- **پروژکشن‌های زمانی دقیق**: خطی، نمایی، فیبوناچی، هارمونیک، ML
- **شناسایی مناطق بحرانی**: خوشه‌بندی زمان‌های هدف با تحلیل احتمال
- **تناوب‌های پیشرفته**: تحلیل کامل روابط زمانی امواج

### 📊 قابلیت‌های تحلیلی:
- **ادغام کامل**: سیگنال‌های NEOWave + مدیریت سرمایه
- **معاملات خودکار**: اجرای خودکار سیگنال‌ها
- **گزارش‌گیری پیشرفته**: آنالیز جامع عملکرد
- **پایگاه داده**: ذخیره تاریخچه معاملات و متریک‌ها

## 🚀 نصب و راه‌اندازی

```bash
# نصب پکیج‌های اضافی
pip install scikit-learn joblib talib

# اجرای نسخه پیشرفته
python run_neowave_analysis.py --mode console --capital 10000
```

## 💻 نحوه استفاده

### حالت کنسول پیشرفته:
```bash
python run_neowave_analysis.py --mode console --capital 10000
```

### معاملات خودکار:
```bash
python run_neowave_analysis.py --mode auto --capital 50000
```

### رابط گرافیکی:
```bash
python run_neowave_analysis.py --mode gui --capital 10000
```

## 🎯 مزایای نسخه پیشرفته

1. **دقت بالاتر**: محاسبه حجم با ML
2. **ریسک کنترل شده**: مدل‌های ریسک پیشرفته
3. **سودآوری بهتر**: بهینه‌سازی پرتفویو
4. **اتوماسیون**: معاملات خودکار ایمن
5. **شفافیت**: گزارش‌گیری دقیق

## ⚠️ نکات مهم

- برای معاملات واقعی، کلیدهای API معتبر وارد کنید
- ابتدا با سرمایه کم تست کنید
- همیشه از stop loss استفاده کنید
- عملکرد گذشته ضامن عملکرد آینده نیست

---
🔥 **ساخته شده برای معامله‌گران حرفه‌ای**
"""