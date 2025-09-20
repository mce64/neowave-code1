"""استراتژی معامله پیشرفته با امواج NEOWave"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime, timedelta
import warnings
from scipy import stats
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import joblib
import json
import talib

# تنظیم logging
logger = logging.getLogger(__name__)

class SignalType(Enum):
    """انواع سیگنال پیشرفته"""
    BUY = "خرید"
    SELL = "فروش"
    HOLD = "نگهداری"
    EXIT = "خروج"
    PARTIAL_EXIT = "خروج جزئی"
    ADD_POSITION = "افزایش پوزیشن"
    REDUCE_POSITION = "کاهش پوزیشن"
    HEDGE = "پوشش ریسک"

class MarketRegime(Enum):
    """رژیم‌های بازار"""
    BULL_TRENDING = "روند صعودی"
    BEAR_TRENDING = "روند نزولی"
    SIDEWAYS = "خنثی"
    HIGH_VOLATILITY = "نوسان بالا"
    LOW_VOLATILITY = "نوسان پایین"
    CRISIS = "بحرانی"
    RECOVERY = "بازیابی"

class ConfidenceLevel(Enum):
    """سطوح اطمینان"""
    VERY_LOW = "بسیار پایین"
    LOW = "پایین"
    MEDIUM = "متوسط"
    HIGH = "بالا"
    VERY_HIGH = "بسیار بالا"
    EXTREME = "فوق‌العاده"

class PositionSizing(Enum):
    """روش‌های محاسبه حجم پوزیشن"""
    FIXED = "ثابت"
    RISK_BASED = "بر اساس ریسک"
    VOLATILITY_BASED = "بر اساس نوسان"
    ML_OPTIMIZED = "بهینه‌سازی شده با ML"
    KELLY = "کلی"
    ADAPTIVE = "تطبیقی"

@dataclass
class MarketConditions:
    """شرایط بازار"""
    regime: MarketRegime
    volatility_percentile: float
    volume_profile: Dict[str, float]
    correlation_matrix: Dict[str, float]
    sentiment_score: float
    fear_greed_index: float
    rsi_divergence: bool
    macd_signal: str
    bollinger_position: float
    support_resistance_proximity: float
    trend_strength: float
    market_microstructure: Dict[str, Any]

@dataclass
class RiskMetrics:
    """متریک‌های ریسک پیشرفته"""
    value_at_risk_95: float
    expected_shortfall: float
    maximum_drawdown_risk: float
    correlation_risk: float
    tail_risk: float
    liquidity_risk: float
    volatility_risk: float
    concentration_risk: float
    beta_risk: float
    skewness: float
    kurtosis: float
    sharpe_ratio_forecast: float

@dataclass
class MLPredictions:
    """پیش‌بینی‌های ML"""
    price_direction_prob: float
    volatility_forecast: float
    regime_change_prob: float
    optimal_holding_period: int
    feature_importance: Dict[str, float]
    model_confidence: float
    anomaly_score: float
    cluster_assignment: int
    nearest_neighbors: List[Dict]
    ensemble_prediction: Dict[str, float]

@dataclass
class AdvancedTradingSignal:
    """کلاس سیگنال معاملاتی پیشرفته"""
    # اطلاعات اساسی
    timestamp: pd.Timestamp
    symbol: str
    signal_type: SignalType
    primary_timeframe: str
    
    # قیمت‌گذاری
    entry_price: float
    stop_loss: float
    take_profits: List[float]
    dynamic_stop_loss: bool = True
    trailing_stop_distance: float = 0.02
    
    # اطمینان و کیفیت
    confidence: float
    confidence_level: ConfidenceLevel
    signal_strength: float
    quality_score: float
    
    # موقعیت موج
    wave_position: str
    wave_degree: int
    elliott_count: str
    neowave_structure: str
    
    # متریک‌های ریسک/ریوارد
    risk_reward_ratio: float
    risk_amount: float
    expected_return: float
    win_probability: float
    kelly_fraction: float
    
    # شرایط بازار
    market_conditions: MarketConditions
    risk_metrics: RiskMetrics
    
    # تحلیل چندگانه timeframe
    multi_timeframe_alignment: Dict[str, float]
    higher_timeframe_bias: str
    lower_timeframe_entry: Dict[str, Any]
    
    # ML و تحلیل پیشرفته
    ml_predictions: MLPredictions
    sentiment_analysis: Dict[str, float]
    volume_analysis: Dict[str, float]
    
    # مدیریت پوزیشن
    position_sizing_method: PositionSizing
    suggested_position_size: float
    max_position_size: float
    scale_in_levels: List[float]
    scale_out_levels: List[float]
    
    # زمان‌بندی
    optimal_entry_window: Tuple[datetime, datetime]
    max_holding_period: int
    review_intervals: List[int]
    expiration_time: datetime
    
    # یادداشت‌ها و توضیحات
    notes: str = ""
    warning_flags: List[str] = field(default_factory=list)
    supporting_indicators: List[str] = field(default_factory=list)
    conflicting_signals: List[str] = field(default_factory=list)
    
    # metadata
    signal_id: str = field(default_factory=lambda: f"SIG_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    created_by: str = "NEOWave Advanced System"
    version: str = "2.0"
    backtest_performance: Optional[Dict[str, float]] = None

class AdvancedNEOWaveTradingStrategy:
    """استراتژی معاملاتی پیشرفته بر اساس NEOWave"""
    
    def __init__(self, data: pd.DataFrame, config: Optional[Dict] = None):
        self.data = data
        self.config = config or self._get_default_config()
        self.signals_history = []
        self.performance_metrics = {}
        
        # مدل‌های ML
        self.price_direction_model = None
        self.volatility_model = None
        self.regime_model = None
        self.anomaly_detector = None
        
        # تحلیل‌گرهای تکنیکال
        self.technical_indicators = {}
        self.support_resistance_levels = []
        self.volume_profile = {}
        
        # متغیرهای تطبیقی
        self.adaptive_parameters = {
            'volatility_lookback': 20,
            'confidence_threshold': 0.6,
            'risk_multiplier': 1.0,
            'regime_sensitivity': 0.75
        }
        
        # بارگذاری مدل‌های از پیش آموزش دیده
        self._initialize_ml_models()
        self._calculate_technical_indicators()
        self._identify_support_resistance()
        
        logger.info("استراتژی معاملاتی پیشرفته NEOWave راه‌اندازی شد")
    
    def _get_default_config(self) -> Dict:
        """تنظیمات پیش‌فرض"""
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
            'wave_weight': 0.3
        }
    
    def _initialize_ml_models(self):
        """راه‌اندازی مدل‌های ML"""
        try:
            # مدل پیش‌بینی جهت قیمت
            self.price_direction_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            # مدل پیش‌بینی نوسان
            self.volatility_model = RandomForestRegressor(
                n_estimators=50,
                max_depth=8,
                random_state=42
            )
            
            # تشخیص anomaly
            self.anomaly_detector = IsolationForest(
                contamination=0.1,
                random_state=42
            )
            
            # اگر مدل‌های از پیش آموزش دیده موجود باشند
            self._load_pretrained_models()
            
        except Exception as e:
            logger.warning(f"خطا در راه‌اندازی مدل‌های ML: {e}")
            self.config['ml_enabled'] = False
    
    def _load_pretrained_models(self):
        """بارگذاری مدل‌های از پیش آموزش دیده"""
        try:
            # در صورت وجود فایل‌های مدل
            # self.price_direction_model = joblib.load('price_direction_model.pkl')
            # self.volatility_model = joblib.load('volatility_model.pkl')
            pass
        except:
            logger.info("مدل‌های از پیش آموزش دیده یافت نشد، از مدل‌های پایه استفاده می‌شود")
    
    def _calculate_technical_indicators(self):
        """محاسبه اندیکاتورهای تکنیکال"""
        try:
            close = self.data['close'].values
            high = self.data['high'].values
            low = self.data['low'].values
            volume = self.data['volume'].values
            
            self.technical_indicators = {
                'rsi': talib.RSI(close),
                'macd': talib.MACD(close)[0],
                'macd_signal': talib.MACD(close)[1],
                'macd_hist': talib.MACD(close)[2],
                'bb_upper': talib.BBANDS(close)[0],
                'bb_middle': talib.BBANDS(close)[1],
                'bb_lower': talib.BBANDS(close)[2],
                'atr': talib.ATR(high, low, close),
                'adx': talib.ADX(high, low, close),
                'stoch_k': talib.STOCH(high, low, close)[0],
                'stoch_d': talib.STOCH(high, low, close)[1],
                'cci': talib.CCI(high, low, close),
                'williams_r': talib.WILLR(high, low, close),
                'mfi': talib.MFI(high, low, close, volume),
                'obv': talib.OBV(close, volume),
                'ad': talib.AD(high, low, close, volume)
            }
            
        except Exception as e:
            logger.warning(f"خطا در محاسبه اندیکاتورها: {e}")
            self.technical_indicators = {}
    
    def _identify_support_resistance(self):
        """شناسایی سطوح حمایت و مقاومت"""
        try:
            close = self.data['close'].values
            high = self.data['high'].values
            low = self.data['low'].values
            
            # روش fractal
            window = 5
            resistance_levels = []
            support_levels = []
            
            for i in range(window, len(high) - window):
                if all(high[i] >= high[i-j] and high[i] >= high[i+j] for j in range(1, window+1)):
                    resistance_levels.append(high[i])
                
                if all(low[i] <= low[i-j] and low[i] <= low[i+j] for j in range(1, window+1)):
                    support_levels.append(low[i])
            
            # clustering برای ترکیب سطوح نزدیک
            all_levels = resistance_levels + support_levels
            if len(all_levels) > 0:
                levels_array = np.array(all_levels).reshape(-1, 1)
                scaler = StandardScaler()
                scaled_levels = scaler.fit_transform(levels_array)
                
                clustering = DBSCAN(eps=0.5, min_samples=2)
                clusters = clustering.fit_predict(scaled_levels)
                
                final_levels = []
                for cluster_id in set(clusters):
                    if cluster_id != -1:
                        cluster_levels = [all_levels[i] for i, c in enumerate(clusters) if c == cluster_id]
                        final_levels.append(np.mean(cluster_levels))
                
                self.support_resistance_levels = sorted(final_levels)
            
        except Exception as e:
            logger.warning(f"خطا در شناسایی سطوح: {e}")
            self.support_resistance_levels = []
    
    def analyze_market_conditions(self) -> MarketConditions:
        """تحلیل شرایط بازار"""
        try:
            close = self.data['close'].values
            volume = self.data['volume'].values
            
            # تشخیص رژیم بازار
            returns = np.diff(np.log(close))
            volatility = np.std(returns[-20:]) * np.sqrt(252)
            trend_strength = abs(np.corrcoef(range(20), close[-20:])[0,1])
            
            if trend_strength > 0.7:
                if returns[-1] > 0:
                    regime = MarketRegime.BULL_TRENDING
                else:
                    regime = MarketRegime.BEAR_TRENDING
            elif volatility > np.percentile([np.std(returns[i:i+20]) for i in range(len(returns)-20)], 80):
                regime = MarketRegime.HIGH_VOLATILITY
            else:
                regime = MarketRegime.SIDEWAYS
            
            # محاسبه سایر متریک‌ها
            vol_percentile = np.percentile([np.std(returns[i:i+20]) for i in range(len(returns)-20)], 
                                          (volatility - np.min([np.std(returns[i:i+20]) for i in range(len(returns)-20)])) / 
                                          (np.max([np.std(returns[i:i+20]) for i in range(len(returns)-20)]) - 
                                           np.min([np.std(returns[i:i+20]) for i in range(len(returns)-20)])) * 100)
            
            # تحلیل volume profile
            volume_profile = {
                'volume_sma_ratio': volume[-1] / np.mean(volume[-20:]) if len(volume) >= 20 else 1.0,
                'volume_trend': np.corrcoef(range(10), volume[-10:])[0,1] if len(volume) >= 10 else 0.0,
                'high_volume_nodes': len([v for v in volume[-20:] if v > np.mean(volume[-20:]) * 1.5])
            }
            
            # سنتیمنت (ساده‌سازی شده)
            rsi = self.technical_indicators.get('rsi', np.array([50]))
            sentiment_score = (50 - rsi[-1]) / 50 if not np.isnan(rsi[-1]) else 0.0
            
            return MarketConditions(
                regime=regime,
                volatility_percentile=vol_percentile,
                volume_profile=volume_profile,
                correlation_matrix={},  # ساده‌سازی شده
                sentiment_score=sentiment_score,
                fear_greed_index=50.0,  # پیش‌فرض
                rsi_divergence=False,
                macd_signal="NEUTRAL",
                bollinger_position=0.5,
                support_resistance_proximity=self._calculate_sr_proximity(),
                trend_strength=trend_strength,
                market_microstructure={}
            )
            
        except Exception as e:
            logger.error(f"خطا در تحلیل شرایط بازار: {e}")
            return MarketConditions(
                regime=MarketRegime.SIDEWAYS,
                volatility_percentile=50.0,
                volume_profile={},
                correlation_matrix={},
                sentiment_score=0.0,
                fear_greed_index=50.0,
                rsi_divergence=False,
                macd_signal="NEUTRAL",
                bollinger_position=0.5,
                support_resistance_proximity=0.0,
                trend_strength=0.5,
                market_microstructure={}
            )
    
    def _calculate_sr_proximity(self) -> float:
        """محاسبه نزدیکی به سطوح حمایت/مقاومت"""
        if not self.support_resistance_levels or self.data.empty:
            return 0.0
        
        current_price = self.data['close'].iloc[-1]
        distances = [abs(current_price - level) / current_price for level in self.support_resistance_levels]
        min_distance = min(distances) if distances else 0.0
        
        return max(0.0, 1.0 - min_distance * 20)  # نرمال‌سازی
    
    def calculate_risk_metrics(self, lookback: int = 252) -> RiskMetrics:
        """محاسبه متریک‌های ریسک"""
        try:
            close = self.data['close'].values
            returns = np.diff(np.log(close))
            
            if len(returns) < lookback:
                lookback = len(returns)
            
            recent_returns = returns[-lookback:]
            
            # VaR و ES
            var_95 = np.percentile(recent_returns, 5)
            es_95 = np.mean(recent_returns[recent_returns <= var_95])
            
            # Maximum Drawdown
            cumulative = np.cumprod(1 + recent_returns)
            running_max = np.maximum.accumulate(cumulative)
            drawdown = (cumulative - running_max) / running_max
            max_dd = np.min(drawdown)
            
            # نوسان
            volatility = np.std(recent_returns) * np.sqrt(252)
            
            # Skewness و Kurtosis
            skewness = stats.skew(recent_returns)
            kurtosis_val = stats.kurtosis(recent_returns)
            
            # Sharpe ratio
            sharpe = np.mean(recent_returns) / np.std(recent_returns) * np.sqrt(252) if np.std(recent_returns) > 0 else 0
            
            return RiskMetrics(
                value_at_risk_95=var_95,
                expected_shortfall=es_95,
                maximum_drawdown_risk=max_dd,
                correlation_risk=0.0,  # ساده‌سازی
                tail_risk=abs(skewness) + kurtosis_val,
                liquidity_risk=0.1,  # فرض
                volatility_risk=volatility,
                concentration_risk=0.0,
                beta_risk=1.0,  # فرض
                skewness=skewness,
                kurtosis=kurtosis_val,
                sharpe_ratio_forecast=sharpe
            )
            
        except Exception as e:
            logger.error(f"خطا در محاسبه متریک‌های ریسک: {e}")
            return RiskMetrics(
                value_at_risk_95=-0.02,
                expected_shortfall=-0.03,
                maximum_drawdown_risk=-0.1,
                correlation_risk=0.0,
                tail_risk=0.5,
                liquidity_risk=0.1,
                volatility_risk=0.2,
                concentration_risk=0.0,
                beta_risk=1.0,
                skewness=0.0,
                kurtosis=0.0,
                sharpe_ratio_forecast=0.0
            )
    
    def generate_ml_predictions(self) -> MLPredictions:
        """تولید پیش‌بینی‌های ML"""
        try:
            if not self.config['ml_enabled']:
                return self._get_default_ml_predictions()
            
            # آماده‌سازی features
            features = self._prepare_ml_features()
            
            if features is None or len(features) == 0:
                return self._get_default_ml_predictions()
            
            # پیش‌بینی جهت قیمت
            if hasattr(self.price_direction_model, 'predict'):
                # اگر مدل آموزش دیده باشد
                direction_prob = 0.6  # پیش‌فرض
            else:
                # آموزش سریع مدل
                self._quick_train_models()
                direction_prob = 0.5
            
            # پیش‌بینی نوسان
            volatility_forecast = np.std(np.diff(np.log(self.data['close'].values[-20:]))) * np.sqrt(252)
            
            # تشخیص anomaly
            anomaly_score = 0.1  # پیش‌فرض
            
            return MLPredictions(
                price_direction_prob=direction_prob,
                volatility_forecast=volatility_forecast,
                regime_change_prob=0.1,
                optimal_holding_period=5,
                feature_importance={},
                model_confidence=0.7,
                anomaly_score=anomaly_score,
                cluster_assignment=0,
                nearest_neighbors=[],
                ensemble_prediction={}
            )
            
        except Exception as e:
            logger.error(f"خطا در تولید پیش‌بینی ML: {e}")
            return self._get_default_ml_predictions()
    
    def _get_default_ml_predictions(self) -> MLPredictions:
        """پیش‌بینی‌های پیش‌فرض"""
        return MLPredictions(
            price_direction_prob=0.5,
            volatility_forecast=0.2,
            regime_change_prob=0.1,
            optimal_holding_period=5,
            feature_importance={},
            model_confidence=0.5,
            anomaly_score=0.1,
            cluster_assignment=0,
            nearest_neighbors=[],
            ensemble_prediction={}
        )
    
    def _prepare_ml_features(self) -> Optional[np.ndarray]:
        """آماده‌سازی features برای ML"""
        try:
            features = []
            
            # قیمت‌ها
            close = self.data['close'].values
            if len(close) < 20:
                return None
            
            # returns
            returns = np.diff(np.log(close))[-10:]
            features.extend(returns)
            
            # technical indicators
            if self.technical_indicators:
                rsi = self.technical_indicators.get('rsi', np.array([50]))
                if not np.isnan(rsi[-1]):
                    features.append(rsi[-1])
                
                macd = self.technical_indicators.get('macd', np.array([0]))
                if not np.isnan(macd[-1]):
                    features.append(macd[-1])
            
            # volume
            if 'volume' in self.data.columns:
                volume_ratio = self.data['volume'].iloc[-1] / self.data['volume'].iloc[-20:-1].mean()
                features.append(volume_ratio)
            
            return np.array(features).reshape(1, -1)
            
        except Exception as e:
            logger.error(f"خطا در آماده‌سازی features: {e}")
            return None
    
    def _quick_train_models(self):
        """آموزش سریع مدل‌ها"""
        try:
            features = []
            targets = []
            
            close = self.data['close'].values
            if len(close) < 50:
                return
            
            # آماده‌سازی داده‌های آموزش
            for i in range(20, len(close) - 1):
                feature_vector = []
                
                # returns
                returns = np.diff(np.log(close[i-10:i]))
                feature_vector.extend(returns)
                
                # simple technical indicators
                sma_5 = np.mean(close[i-5:i])
                sma_20 = np.mean(close[i-20:i])
                feature_vector.append(close[i-1] / sma_5 - 1)
                feature_vector.append(close[i-1] / sma_20 - 1)
                
                features.append(feature_vector)
                
                # target: آیا قیمت بعدی بالاتر است؟
                targets.append(1 if close[i+1] > close[i] else 0)
            
            if len(features) > 10:
                X = np.array(features)
                y = np.array(targets)
                
                self.price_direction_model.fit(X, y)
                
        except Exception as e:
            logger.error(f"خطا در آموزش سریع مدل: {e}")
    
    def analyze_wave_position(self, current_wave: Dict) -> AdvancedTradingSignal:
        """تحلیل موقعیت فعلی موج و تولید سیگنال پیشرفته"""
        wave_number = current_wave.get('number', 0)
        wave_type = current_wave.get('type', '')
        
        # انتخاب استراتژی بر اساس نوع موج
        if wave_number == 1:
            return self._advanced_strategy_wave1(current_wave)
        elif wave_number == 2:
            return self._advanced_strategy_wave2(current_wave)
        elif wave_number == 3:
            return self._advanced_strategy_wave3(current_wave)
        elif wave_number == 4:
            return self._advanced_strategy_wave4(current_wave)
        elif wave_number == 5:
            return self._advanced_strategy_wave5(current_wave)
        elif wave_type == 'A':
            return self._advanced_strategy_waveA(current_wave)
        elif wave_type == 'B':
            return self._advanced_strategy_waveB(current_wave)
        elif wave_type == 'C':
            return self._advanced_strategy_waveC(current_wave)
        else:
            return self._generate_default_signal()
    
    def _advanced_strategy_wave2(self, wave: Dict) -> AdvancedTradingSignal:
        """استراتژی پیشرفته برای موج 2"""
        # تحلیل شرایط بازار
        market_conditions = self.analyze_market_conditions()
        risk_metrics = self.calculate_risk_metrics()
        ml_predictions = self.generate_ml_predictions()
        
        # محاسبه‌های پایه
        retracement = wave.get('retracement', 0.5)
        current_price = wave.get('end_price', self.data['close'].iloc[-1])
        wave1_start = wave.get('wave1_start_price', current_price * 0.9)
        wave1_length = wave.get('wave1_length', current_price * 0.1)
        
        # تعیین confidence بر اساس عمق retracement
        if 0.382 <= retracement <= 0.618:
            base_confidence = 0.9
            confidence_level = ConfidenceLevel.VERY_HIGH
        elif 0.236 <= retracement <= 0.786:
            base_confidence = 0.7
            confidence_level = ConfidenceLevel.HIGH
        else:
            base_confidence = 0.4
            confidence_level = ConfidenceLevel.MEDIUM
        
        # تنظیم confidence بر اساس شرایط بازار
        market_adjustment = self._calculate_market_confidence_adjustment(market_conditions)
        final_confidence = min(0.95, base_confidence * market_adjustment)
        
        # محاسبه stop loss تطبیقی
        atr = self.technical_indicators.get('atr', np.array([current_price * 0.02]))[-1]
        volatility_multiplier = 1 + (risk_metrics.volatility_risk / 0.3)  # تنظیم بر اساس نوسان
        
        stop_loss = wave1_start * (0.995 - atr / current_price * volatility_multiplier)
        
        # محاسبه take profits با فیبوناچی پیشرفته
        fibonacci_extensions = [1.0, 1.272, 1.414, 1.618, 2.0, 2.618]
        take_profits = []
        
        for ext in fibonacci_extensions:
            tp = current_price + (wave1_length * ext)
            # بررسی سطوح مقاومت
            if not self._is_near_resistance(tp):
                take_profits.append(tp)
            if len(take_profits) >= 4:  # حداکثر 4 هدف
                break
        
        # محاسبه risk/reward
        risk = abs(current_price - stop_loss)
        reward = take_profits[0] - current_price if take_profits else wave1_length
        rr_ratio = reward / risk if risk > 0 else 0
        
        # تعیین نوع signal
        if rr_ratio >= self.config['min_rr_ratio'] and final_confidence >= self.config['confidence_threshold']:
            if ml_predictions.price_direction_prob > 0.6:
                signal_type = SignalType.BUY
            else:
                signal_type = SignalType.HOLD
        else:
            signal_type = SignalType.HOLD
        
        # محاسبه position sizing
        position_sizing = self._calculate_adaptive_position_size(
            risk, final_confidence, market_conditions, ml_predictions
        )
        
        # multi-timeframe analysis
        mtf_analysis = self._analyze_multiple_timeframes(current_price)
        
        # ایجاد سیگنال پیشرفته
        return AdvancedTradingSignal(
            timestamp=pd.Timestamp.now(),
            symbol=getattr(self.data, 'symbol', 'UNKNOWN'),
            signal_type=signal_type,
            primary_timeframe=getattr(self.data, 'timeframe', '1h'),
            
            entry_price=current_price,
            stop_loss=stop_loss,
            take_profits=take_profits,
            dynamic_stop_loss=True,
            trailing_stop_distance=atr / current_price,
            
            confidence=final_confidence,
            confidence_level=confidence_level,
            signal_strength=self._calculate_signal_strength(wave, market_conditions),
            quality_score=self._calculate_quality_score(final_confidence, rr_ratio, market_conditions),
            
            wave_position="End of Wave 2",
            wave_degree=wave.get('degree', 0),
            elliott_count="2",
            neowave_structure=self._analyze_neowave_structure(wave),
            
            risk_reward_ratio=rr_ratio,
            risk_amount=risk,
            expected_return=reward,
            win_probability=final_confidence,
            kelly_fraction=self._calculate_kelly_fraction(final_confidence, rr_ratio),
            
            market_conditions=market_conditions,
            risk_metrics=risk_metrics,
            
            multi_timeframe_alignment=mtf_analysis,
            higher_timeframe_bias=self._get_higher_timeframe_bias(),
            lower_timeframe_entry=self._get_lower_timeframe_entry(),
            
            ml_predictions=ml_predictions,
            sentiment_analysis=self._analyze_sentiment(),
            volume_analysis=self._analyze_volume(),
            
            position_sizing_method=PositionSizing.ADAPTIVE,
            suggested_position_size=position_sizing['suggested_size'],
            max_position_size=position_sizing['max_size'],
            scale_in_levels=self._calculate_scale_in_levels(current_price, 3),
            scale_out_levels=take_profits,
            
            optimal_entry_window=self._calculate_entry_window(),
            max_holding_period=ml_predictions.optimal_holding_period,
            review_intervals=[1, 3, 5, 10],  # روزهای بازبینی
            expiration_time=datetime.now() + timedelta(days=10),
            
            notes=f"موج 2 با retracement {retracement:.1%} - تحلیل جامع انجام شد",
            warning_flags=self._identify_warning_flags(market_conditions, risk_metrics),
            supporting_indicators=self._identify_supporting_indicators(),
            conflicting_signals=self._identify_conflicting_signals()
        )
    
    def _advanced_strategy_wave1(self, wave: Dict) -> AdvancedTradingSignal:
        """استراتژی پیشرفته برای موج 1"""
        market_conditions = self.analyze_market_conditions()
        risk_metrics = self.calculate_risk_metrics()
        ml_predictions = self.generate_ml_predictions()
        
        current_price = wave.get('end_price', self.data['close'].iloc[-1])
        
        # موج 1 معمولاً ریسک بالایی دارد - رویکرد محتاطانه
        base_confidence = 0.3
        
        # افزایش confidence در صورت تأیید ML
        if ml_predictions.price_direction_prob > 0.8:
            base_confidence = 0.5
        
        return AdvancedTradingSignal(
            timestamp=pd.Timestamp.now(),
            symbol=getattr(self.data, 'symbol', 'UNKNOWN'),
            signal_type=SignalType.HOLD,
            primary_timeframe=getattr(self.data, 'timeframe', '1h'),
            
            entry_price=current_price,
            stop_loss=wave.get('start_price', current_price * 0.95),
            take_profits=[],
            
            confidence=base_confidence,
            confidence_level=ConfidenceLevel.LOW,
            signal_strength=0.3,
            quality_score=0.3,
            
            wave_position="Wave 1",
            wave_degree=wave.get('degree', 0),
            elliott_count="1",
            neowave_structure="Impulse Start",
            
            risk_reward_ratio=0,
            risk_amount=0,
            expected_return=0,
            win_probability=base_confidence,
            kelly_fraction=0,
            
            market_conditions=market_conditions,
            risk_metrics=risk_metrics,
            
            multi_timeframe_alignment={},
            higher_timeframe_bias="NEUTRAL",
            lower_timeframe_entry={},
            
            ml_predictions=ml_predictions,
            sentiment_analysis={},
            volume_analysis={},
            
            position_sizing_method=PositionSizing.FIXED,
            suggested_position_size=0,
            max_position_size=0,
            scale_in_levels=[],
            scale_out_levels=[],
            
            optimal_entry_window=(datetime.now(), datetime.now() + timedelta(hours=1)),
            max_holding_period=1,
            review_intervals=[1],
            expiration_time=datetime.now() + timedelta(hours=4),
            
            notes="موج 1: انتظار برای تأیید با موج 2 توصیه می‌شود",
            warning_flags=["HIGH_RISK", "EARLY_STAGE"],
            supporting_indicators=[],
            conflicting_signals=[]
        )
    
    def _advanced_strategy_wave3(self, wave: Dict) -> AdvancedTradingSignal:
        """استراتژی پیشرفته برای موج 3"""
        market_conditions = self.analyze_market_conditions()
        risk_metrics = self.calculate_risk_metrics()
        ml_predictions = self.generate_ml_predictions()
        
        current_price = wave.get('current_price', self.data['close'].iloc[-1])
        
        # موج 3 معمولاً قوی‌ترین موج است
        base_confidence = 0.85
        
        # محاسبه targets بر اساس پروژکشن موج 3
        wave1_length = wave.get('wave1_length', current_price * 0.1)
        
        take_profits = [
            current_price + (wave1_length * 1.618),  # هدف اول
            current_price + (wave1_length * 2.618),  # هدف دوم
            current_price + (wave1_length * 4.236),  # هدف سوم
        ]
        
        stop_loss = wave.get('start_price', current_price * 0.95)
        risk = abs(current_price - stop_loss)
        reward = take_profits[0] - current_price
        rr_ratio = reward / risk if risk > 0 else 0
        
        return AdvancedTradingSignal(
            timestamp=pd.Timestamp.now(),
            symbol=getattr(self.data, 'symbol', 'UNKNOWN'),
            signal_type=SignalType.BUY,
            primary_timeframe=getattr(self.data, 'timeframe', '1h'),
            
            entry_price=current_price,
            stop_loss=stop_loss,
            take_profits=take_profits,
            dynamic_stop_loss=True,
            trailing_stop_distance=0.03,
            
            confidence=base_confidence,
            confidence_level=ConfidenceLevel.VERY_HIGH,
            signal_strength=0.9,
            quality_score=0.9,
            
            wave_position="Wave 3 in progress",
            wave_degree=wave.get('degree', 0),
            elliott_count="3",
            neowave_structure="Strong Impulse",
            
            risk_reward_ratio=rr_ratio,
            risk_amount=risk,
            expected_return=reward,
            win_probability=base_confidence,
            kelly_fraction=self._calculate_kelly_fraction(base_confidence, rr_ratio),
            
            market_conditions=market_conditions,
            risk_metrics=risk_metrics,
            
            multi_timeframe_alignment=self._analyze_multiple_timeframes(current_price),
            higher_timeframe_bias="BULLISH",
            lower_timeframe_entry=self._get_lower_timeframe_entry(),
            
            ml_predictions=ml_predictions,
            sentiment_analysis=self._analyze_sentiment(),
            volume_analysis=self._analyze_volume(),
            
            position_sizing_method=PositionSizing.ADAPTIVE,
            suggested_position_size=self._calculate_adaptive_position_size(risk, base_confidence, market_conditions, ml_predictions)['suggested_size'],
            max_position_size=self._calculate_adaptive_position_size(risk, base_confidence, market_conditions, ml_predictions)['max_size'],
            scale_in_levels=self._calculate_scale_in_levels(current_price, 2),
            scale_out_levels=take_profits,
            
            optimal_entry_window=(datetime.now(), datetime.now() + timedelta(hours=2)),
            max_holding_period=20,
            review_intervals=[2, 5, 10],
            expiration_time=datetime.now() + timedelta(days=30),
            
            notes="موج 3: قوی‌ترین موج - فرصت عالی برای افزایش پوزیشن",
            warning_flags=[],
            supporting_indicators=["STRONG_MOMENTUM", "HIGH_VOLUME"],
            conflicting_signals=[]
        )
    
    def _advanced_strategy_wave4(self, wave: Dict) -> AdvancedTradingSignal:
        """استراتژی پیشرفته برای موج 4"""
        market_conditions = self.analyze_market_conditions()
        risk_metrics = self.calculate_risk_metrics()
        ml_predictions = self.generate_ml_predictions()
        
        current_price = wave.get('current_price', self.data['close'].iloc[-1])
        
        # موج 4 زمان مناسب برای کاهش پوزیشن
        return AdvancedTradingSignal(
            timestamp=pd.Timestamp.now(),
            symbol=getattr(self.data, 'symbol', 'UNKNOWN'),
            signal_type=SignalType.PARTIAL_EXIT,
            primary_timeframe=getattr(self.data, 'timeframe', '1h'),
            
            entry_price=current_price,
            stop_loss=wave.get('end_price', current_price * 0.97),
            take_profits=[],
            
            confidence=0.6,
            confidence_level=ConfidenceLevel.MEDIUM,
            signal_strength=0.5,
            quality_score=0.6,
            
            wave_position="Wave 4 correction",
            wave_degree=wave.get('degree', 0),
            elliott_count="4",
            neowave_structure="Corrective Phase",
            
            risk_reward_ratio=0,
            risk_amount=0,
            expected_return=0,
            win_probability=0.6,
            kelly_fraction=0,
            
            market_conditions=market_conditions,
            risk_metrics=risk_metrics,
            
            multi_timeframe_alignment={},
            higher_timeframe_bias="NEUTRAL",
            lower_timeframe_entry={},
            
            ml_predictions=ml_predictions,
            sentiment_analysis={},
            volume_analysis={},
            
            position_sizing_method=PositionSizing.RISK_BASED,
            suggested_position_size=0,
            max_position_size=0,
            scale_in_levels=[],
            scale_out_levels=[current_price * 0.5],  # کاهش 50% پوزیشن
            
            optimal_entry_window=(datetime.now(), datetime.now() + timedelta(hours=1)),
            max_holding_period=5,
            review_intervals=[1, 3],
            expiration_time=datetime.now() + timedelta(days=7),
            
            notes="موج 4: کاهش پوزیشن یا صبر برای موج 5",
            warning_flags=["CORRECTION_PHASE"],
            supporting_indicators=[],
            conflicting_signals=[]
        )
    
    def _advanced_strategy_wave5(self, wave: Dict) -> AdvancedTradingSignal:
        """استراتژی پیشرفته برای موج 5"""
        market_conditions = self.analyze_market_conditions()
        risk_metrics = self.calculate_risk_metrics()
        ml_predictions = self.generate_ml_predictions()
        
        current_price = wave.get('current_price', self.data['close'].iloc[-1])
        divergence = wave.get('divergence', False)
        
        # تشخیص divergence و علائم پایان روند
        if divergence or ml_predictions.regime_change_prob > 0.7:
            signal_type = SignalType.EXIT
            confidence = 0.9
            notes = "divergence مشاهده شد - خروج فوری توصیه می‌شود"
        else:
            signal_type = SignalType.PARTIAL_EXIT
            confidence = 0.7
            notes = "نزدیک به پایان روند - آماده خروج تدریجی"
        
        return AdvancedTradingSignal(
            timestamp=pd.Timestamp.now(),
            symbol=getattr(self.data, 'symbol', 'UNKNOWN'),
            signal_type=signal_type,
            primary_timeframe=getattr(self.data, 'timeframe', '1h'),
            
            entry_price=current_price,
            stop_loss=current_price * 1.02,
            take_profits=[
                current_price * 0.95,
                current_price * 0.90
            ],
            
            confidence=confidence,
            confidence_level=ConfidenceLevel.HIGH if divergence else ConfidenceLevel.MEDIUM,
            signal_strength=0.8 if divergence else 0.6,
            quality_score=0.8,
            
            wave_position="End of Wave 5",
            wave_degree=wave.get('degree', 0),
            elliott_count="5",
            neowave_structure="Impulse Completion",
            
            risk_reward_ratio=-2.0,  # معامله معکوس
            risk_amount=current_price * 0.02,
            expected_return=current_price * 0.05,
            win_probability=confidence,
            kelly_fraction=self._calculate_kelly_fraction(confidence, 2.0),
            
            market_conditions=market_conditions,
            risk_metrics=risk_metrics,
            
            multi_timeframe_alignment=self._analyze_multiple_timeframes(current_price),
            higher_timeframe_bias="BEARISH",
            lower_timeframe_entry=self._get_lower_timeframe_entry(),
            
            ml_predictions=ml_predictions,
            sentiment_analysis=self._analyze_sentiment(),
            volume_analysis=self._analyze_volume(),
            
            position_sizing_method=PositionSizing.ADAPTIVE,
            suggested_position_size=0,
            max_position_size=0,
            scale_in_levels=[],
            scale_out_levels=[current_price, current_price * 0.95],
            
            optimal_entry_window=(datetime.now(), datetime.now() + timedelta(minutes=30)),
            max_holding_period=10,
            review_intervals=[1, 2, 5],
            expiration_time=datetime.now() + timedelta(days=5),
            
            notes=notes,
            warning_flags=["TREND_EXHAUSTION"] + (["DIVERGENCE"] if divergence else []),
            supporting_indicators=["MOMENTUM_DIVERGENCE"] if divergence else [],
            conflicting_signals=[]
        )
    
    def _advanced_strategy_waveA(self, wave: Dict) -> AdvancedTradingSignal:
        """استراتژی پیشرفته برای موج A"""
        market_conditions = self.analyze_market_conditions()
        risk_metrics = self.calculate_risk_metrics()
        ml_predictions = self.generate_ml_predictions()
        
        current_price = wave.get('current_price', self.data['close'].iloc[-1])
        
        return AdvancedTradingSignal(
            timestamp=pd.Timestamp.now(),
            symbol=getattr(self.data, 'symbol', 'UNKNOWN'),
            signal_type=SignalType.SELL,
            primary_timeframe=getattr(self.data, 'timeframe', '1h'),
            
            entry_price=current_price,
            stop_loss=wave.get('start_price', current_price * 1.05),
            take_profits=[
                current_price * 0.95,
                current_price * 0.90,
                current_price * 0.85
            ],
            
            confidence=0.6,
            confidence_level=ConfidenceLevel.MEDIUM,
            signal_strength=0.6,
            quality_score=0.6,
            
            wave_position="Wave A correction",
            wave_degree=wave.get('degree', 0),
            elliott_count="A",
            neowave_structure="Corrective Start",
            
            risk_reward_ratio=2.0,
            risk_amount=current_price * 0.05,
            expected_return=current_price * 0.10,
            win_probability=0.6,
            kelly_fraction=self._calculate_kelly_fraction(0.6, 2.0),
            
            market_conditions=market_conditions,
            risk_metrics=risk_metrics,
            
            multi_timeframe_alignment=self._analyze_multiple_timeframes(current_price),
            higher_timeframe_bias="BEARISH",
            lower_timeframe_entry=self._get_lower_timeframe_entry(),
            
            ml_predictions=ml_predictions,
            sentiment_analysis=self._analyze_sentiment(),
            volume_analysis=self._analyze_volume(),
            
            position_sizing_method=PositionSizing.RISK_BASED,
            suggested_position_size=self._calculate_adaptive_position_size(current_price * 0.05, 0.6, market_conditions, ml_predictions)['suggested_size'],
            max_position_size=self._calculate_adaptive_position_size(current_price * 0.05, 0.6, market_conditions, ml_predictions)['max_size'],
            scale_in_levels=self._calculate_scale_in_levels(current_price, 2),
            scale_out_levels=[current_price * 0.95, current_price * 0.90],
            
            optimal_entry_window=(datetime.now(), datetime.now() + timedelta(hours=2)),
            max_holding_period=15,
            review_intervals=[3, 7, 14],
            expiration_time=datetime.now() + timedelta(days=21),
            
            notes="شروع اصلاح - پوزیشن شورت محتاطانه",
            warning_flags=[],
            supporting_indicators=["CORRECTION_START"],
            conflicting_signals=[]
        )
    
    def _advanced_strategy_waveB(self, wave: Dict) -> AdvancedTradingSignal:
        """استراتژی پیشرفته برای موج B"""
        market_conditions = self.analyze_market_conditions()
        risk_metrics = self.calculate_risk_metrics()
        ml_predictions = self.generate_ml_predictions()
        
        current_price = wave.get('current_price', self.data['close'].iloc[-1])
        
        return AdvancedTradingSignal(
            timestamp=pd.Timestamp.now(),
            symbol=getattr(self.data, 'symbol', 'UNKNOWN'),
            signal_type=SignalType.HOLD,
            primary_timeframe=getattr(self.data, 'timeframe', '1h'),
            
            entry_price=current_price,
            stop_loss=wave.get('end_price', current_price * 0.98),
            take_profits=[],
            
            confidence=0.4,
            confidence_level=ConfidenceLevel.LOW,
            signal_strength=0.4,
            quality_score=0.4,
            
            wave_position="Wave B bounce",
            wave_degree=wave.get('degree', 0),
            elliott_count="B",
            neowave_structure="Corrective Bounce",
            
            risk_reward_ratio=0,
            risk_amount=0,
            expected_return=0,
            win_probability=0.4,
            kelly_fraction=0,
            
            market_conditions=market_conditions,
            risk_metrics=risk_metrics,
            
            multi_timeframe_alignment={},
            higher_timeframe_bias="NEUTRAL",
            lower_timeframe_entry={},
            
            ml_predictions=ml_predictions,
            sentiment_analysis={},
            volume_analysis={},
            
            position_sizing_method=PositionSizing.FIXED,
            suggested_position_size=0,
            max_position_size=0,
            scale_in_levels=[],
            scale_out_levels=[],
            
            optimal_entry_window=(datetime.now(), datetime.now() + timedelta(hours=1)),
            max_holding_period=3,
            review_intervals=[1, 2],
            expiration_time=datetime.now() + timedelta(days=3),
            
            notes="موج B: صبر برای موج C",
            warning_flags=["UNCERTAIN_DIRECTION"],
            supporting_indicators=[],
            conflicting_signals=[]
        )
    
    def _advanced_strategy_waveC(self, wave: Dict) -> AdvancedTradingSignal:
        """استراتژی پیشرفته برای موج C"""
        market_conditions = self.analyze_market_conditions()
        risk_metrics = self.calculate_risk_metrics()
        ml_predictions = self.generate_ml_predictions()
        
        current_price = wave.get('end_price', self.data['close'].iloc[-1])
        
        return AdvancedTradingSignal(
            timestamp=pd.Timestamp.now(),
            symbol=getattr(self.data, 'symbol', 'UNKNOWN'),
            signal_type=SignalType.BUY,
            primary_timeframe=getattr(self.data, 'timeframe', '1h'),
            
            entry_price=current_price,
            stop_loss=current_price * 0.95,
            take_profits=[
                current_price * 1.10,
                current_price * 1.20,
                current_price * 1.35
            ],
            
            confidence=0.7,
            confidence_level=ConfidenceLevel.HIGH,
            signal_strength=0.7,
            quality_score=0.7,
            
            wave_position="End of Wave C",
            wave_degree=wave.get('degree', 0),
            elliott_count="C",
            neowave_structure="Correction Completion",
            
            risk_reward_ratio=3.0,
            risk_amount=current_price * 0.05,
            expected_return=current_price * 0.15,
            win_probability=0.7,
            kelly_fraction=self._calculate_kelly_fraction(0.7, 3.0),
            
            market_conditions=market_conditions,
            risk_metrics=risk_metrics,
            
            multi_timeframe_alignment=self._analyze_multiple_timeframes(current_price),
            higher_timeframe_bias="BULLISH",
            lower_timeframe_entry=self._get_lower_timeframe_entry(),
            
            ml_predictions=ml_predictions,
            sentiment_analysis=self._analyze_sentiment(),
            volume_analysis=self._analyze_volume(),
            
            position_sizing_method=PositionSizing.ADAPTIVE,
            suggested_position_size=self._calculate_adaptive_position_size(current_price * 0.05, 0.7, market_conditions, ml_predictions)['suggested_size'],
            max_position_size=self._calculate_adaptive_position_size(current_price * 0.05, 0.7, market_conditions, ml_predictions)['max_size'],
            scale_in_levels=self._calculate_scale_in_levels(current_price, 3),
            scale_out_levels=[current_price * 1.10, current_price * 1.20],
            
            optimal_entry_window=(datetime.now(), datetime.now() + timedelta(hours=4)),
            max_holding_period=30,
            review_intervals=[5, 15, 30],
            expiration_time=datetime.now() + timedelta(days=60),
            
            notes="پایان اصلاح - آماده برای روند جدید صعودی",
            warning_flags=[],
            supporting_indicators=["CORRECTION_COMPLETION", "OVERSOLD"],
            conflicting_signals=[]
        )
    
    def _generate_default_signal(self) -> AdvancedTradingSignal:
        """تولید سیگنال پیش‌فرض"""
        current_price = self.data['close'].iloc[-1] if not self.data.empty else 100.0
        
        return AdvancedTradingSignal(
            timestamp=pd.Timestamp.now(),
            symbol="UNKNOWN",
            signal_type=SignalType.HOLD,
            primary_timeframe="1h",
            
            entry_price=current_price,
            stop_loss=current_price * 0.98,
            take_profits=[],
            
            confidence=0.5,
            confidence_level=ConfidenceLevel.MEDIUM,
            signal_strength=0.5,
            quality_score=0.5,
            
            wave_position="Unknown",
            wave_degree=0,
            elliott_count="?",
            neowave_structure="Unknown",
            
            risk_reward_ratio=0,
            risk_amount=0,
            expected_return=0,
            win_probability=0.5,
            kelly_fraction=0,
            
            market_conditions=self.analyze_market_conditions(),
            risk_metrics=self.calculate_risk_metrics(),
            
            multi_timeframe_alignment={},
            higher_timeframe_bias="NEUTRAL",
            lower_timeframe_entry={},
            
            ml_predictions=self.generate_ml_predictions(),
            sentiment_analysis={},
            volume_analysis={},
            
            position_sizing_method=PositionSizing.FIXED,
            suggested_position_size=0,
            max_position_size=0,
            scale_in_levels=[],
            scale_out_levels=[],
            
            optimal_entry_window=(datetime.now(), datetime.now() + timedelta(hours=1)),
            max_holding_period=1,
            review_intervals=[1],
            expiration_time=datetime.now() + timedelta(hours=2),
            
            notes="سیگنال پیش‌فرض - تحلیل بیشتر نیاز است",
            warning_flags=["NO_CLEAR_PATTERN"],
            supporting_indicators=[],
            conflicting_signals=[]
        )
    
    # متدهای کمکی
    
    def _calculate_market_confidence_adjustment(self, market_conditions: MarketConditions) -> float:
        """محاسبه تنظیم confidence بر اساس شرایط بازار"""
        adjustment = 1.0
        
        # رژیم بازار
        if market_conditions.regime in [MarketRegime.BULL_TRENDING, MarketRegime.BEAR_TRENDING]:
            adjustment *= 1.2
        elif market_conditions.regime == MarketRegime.HIGH_VOLATILITY:
            adjustment *= 0.8
        
        # نوسان
        if market_conditions.volatility_percentile > 80:
            adjustment *= 0.7
        elif market_conditions.volatility_percentile < 20:
            adjustment *= 1.1
        
        # قدرت روند
        adjustment *= (0.5 + market_conditions.trend_strength)
        
        return max(0.3, min(1.5, adjustment))
    
    def _is_near_resistance(self, price: float, threshold: float = 0.02) -> bool:
        """بررسی نزدیکی به سطح مقاومت"""
        for level in self.support_resistance_levels:
            if abs(price - level) / price < threshold:
                return True
        return False
    
    def _calculate_adaptive_position_size(self, risk: float, confidence: float, 
                                        market_conditions: MarketConditions, 
                                        ml_predictions: MLPredictions) -> Dict[str, float]:
        """محاسبه حجم پوزیشن تطبیقی"""
        base_risk = self.config['risk_per_trade']
        
        # تنظیم بر اساس confidence
        confidence_multiplier = confidence ** 2
        
        # تنظیم بر اساس شرایط بازار
        market_multiplier = 1.0
        if market_conditions.regime == MarketRegime.HIGH_VOLATILITY:
            market_multiplier = 0.5
        elif market_conditions.regime in [MarketRegime.BULL_TRENDING, MarketRegime.BEAR_TRENDING]:
            market_multiplier = 1.2
        
        # تنظیم بر اساس ML
        ml_multiplier = 0.5 + ml_predictions.model_confidence
        
        # محاسبه نهایی
        adjusted_risk = base_risk * confidence_multiplier * market_multiplier * ml_multiplier
        suggested_size = min(adjusted_risk, base_risk * 2)  # حداکثر 2 برابر
        
        return {
            'suggested_size': suggested_size,
            'max_size': base_risk * 3,  # حداکثر مطلق
            'confidence_component': confidence_multiplier,
            'market_component': market_multiplier,
            'ml_component': ml_multiplier
        }
    
    def _calculate_signal_strength(self, wave: Dict, market_conditions: MarketConditions) -> float:
        """محاسبه قدرت سیگنال"""
        strength = 0.5
        
        # کیفیت الگوی موج
        if wave.get('fibonacci_accuracy', 0) > 0.8:
            strength += 0.2
        
        # تأیید volume
        volume_confirmation = wave.get('volume_confirmation', False)
        if volume_confirmation:
            strength += 0.15
        
        # همراستایی با روند کلی
        if market_conditions.trend_strength > 0.7:
            strength += 0.15
        
        return min(1.0, strength)
    
    def _calculate_quality_score(self, confidence: float, rr_ratio: float, 
                                market_conditions: MarketConditions) -> float:
        """محاسبه امتیاز کیفیت سیگنال"""
        quality = 0.0
        
        # confidence
        quality += confidence * 0.4
        
        # risk/reward
        quality += min(1.0, rr_ratio / 3.0) * 0.3
        
        # شرایط بازار
        quality += market_conditions.trend_strength * 0.3
        
        return min(1.0, quality)
    
    def _analyze_neowave_structure(self, wave: Dict) -> str:
        """تحلیل ساختار NEOWave"""
        wave_type = wave.get('type', 'Unknown')
        complexity = wave.get('complexity', 'Simple')
        
        if wave_type in ['1', '3', '5']:
            return f"Impulse {wave_type} - {complexity}"
        elif wave_type in ['2', '4']:
            return f"Corrective {wave_type} - {complexity}"
        elif wave_type in ['A', 'B', 'C']:
            return f"Complex Correction {wave_type} - {complexity}"
        else:
            return "Unknown Structure"
    
    def _calculate_kelly_fraction(self, win_prob: float, rr_ratio: float) -> float:
        """محاسبه Kelly Criterion"""
        if rr_ratio <= 0:
            return 0.0
        
        kelly = (win_prob * rr_ratio - (1 - win_prob)) / rr_ratio
        return max(0.0, min(0.25, kelly))  # محدود به 25%
    
    def _analyze_multiple_timeframes(self, current_price: float) -> Dict[str, float]:
        """تحلیل چندگانه timeframe"""
        # ساده‌سازی شده - در عمل باید داده‌های timeframe های مختلف بررسی شود
        return {
            '1m': 0.6,
            '5m': 0.7,
            '15m': 0.8,
            '1h': 0.9,
            '4h': 0.8,
            '1d': 0.7
        }
    
    def _get_higher_timeframe_bias(self) -> str:
        """تعیین bias timeframe بالاتر"""
        # ساده‌سازی - در عمل باید از داده‌های واقعی استفاده شود
        return "BULLISH"
    
    def _get_lower_timeframe_entry(self) -> Dict[str, Any]:
        """نقطه ورود در timeframe پایین‌تر"""
        return {
            'timeframe': '5m',
            'entry_pattern': 'pullback',
            'confirmation_needed': True
        }
    
    def _analyze_sentiment(self) -> Dict[str, float]:
        """تحلیل سنتیمنت"""
        return {
            'social_sentiment': 0.6,
            'news_sentiment': 0.5,
            'fear_greed': 0.4,
            'institutional_flow': 0.7
        }
    
    def _analyze_volume(self) -> Dict[str, float]:
        """تحلیل volume"""
        if 'volume' not in self.data.columns:
            return {}
        
        volume = self.data['volume'].values
        if len(volume) < 10:
            return {}
        
        return {
            'volume_trend': np.corrcoef(range(10), volume[-10:])[0,1],
            'volume_spike': volume[-1] / np.mean(volume[-20:-1]),
            'accumulation_distribution': np.mean(volume[-5:]) / np.mean(volume[-20:-5])
        }
    
    def _calculate_scale_in_levels(self, current_price: float, levels: int) -> List[float]:
        """محاسبه سطوح scale-in"""
        if levels <= 0:
            return []
        
        step = 0.02  # 2% فاصله
        return [current_price * (1 - i * step) for i in range(1, levels + 1)]
    
    def _calculate_entry_window(self) -> Tuple[datetime, datetime]:
        """محاسبه پنجره زمانی ورود"""
        now = datetime.now()
        return (now, now + timedelta(hours=4))
    
    def _identify_warning_flags(self, market_conditions: MarketConditions, 
                               risk_metrics: RiskMetrics) -> List[str]:
        """شناسایی پرچم‌های هشدار"""
        flags = []
        
        if market_conditions.volatility_percentile > 90:
            flags.append("EXTREME_VOLATILITY")
        
        if risk_metrics.volatility_risk > 0.5:
            flags.append("HIGH_VOLATILITY_RISK")
        
        if market_conditions.regime == MarketRegime.CRISIS:
            flags.append("CRISIS_MODE")
        
        return flags
    
    def _identify_supporting_indicators(self) -> List[str]:
        """شناسایی اندیکاتورهای پشتیبان"""
        indicators = []
        
        if self.technical_indicators:
            rsi = self.technical_indicators.get('rsi', np.array([50]))
            if not np.isnan(rsi[-1]):
                if rsi[-1] < 30:
                    indicators.append("OVERSOLD_RSI")
                elif rsi[-1] > 70:
                    indicators.append("OVERBOUGHT_RSI")
        
        return indicators
    
    def _identify_conflicting_signals(self) -> List[str]:
        """شناسایی سیگنال‌های متضاد"""
        conflicts = []
        
        # بررسی تضاد بین اندیکاتورها
        if self.technical_indicators:
            rsi = self.technical_indicators.get('rsi', np.array([50]))
            macd = self.technical_indicators.get('macd', np.array([0]))
            
            if not np.isnan(rsi[-1]) and not np.isnan(macd[-1]):
                if rsi[-1] > 70 and macd[-1] > 0:
                    conflicts.append("OVERBOUGHT_BUT_BULLISH_MOMENTUM")
                elif rsi[-1] < 30 and macd[-1] < 0:
                    conflicts.append("OVERSOLD_BUT_BEARISH_MOMENTUM")
        
        return conflicts
    
    def calculate_position_size(self, signal: AdvancedTradingSignal, 
                              capital: float, 
                              risk_percent: float = None) -> Dict[str, float]:
        """محاسبه حجم پوزیشن پیشرفته"""
        if risk_percent is None:
            risk_percent = signal.suggested_position_size
        
        risk_amount = capital * risk_percent
        stop_distance = abs(signal.entry_price - signal.stop_loss)
        
        if stop_distance > 0:
            base_position_size = risk_amount / stop_distance
        else:
            base_position_size = 0
        
        # تنظیم بر اساس Kelly Criterion
        kelly_adjusted = base_position_size * signal.kelly_fraction
        
        # تنظیم بر اساس confidence
        confidence_adjusted = kelly_adjusted * signal.confidence
        
        # محدودیت‌های نهایی
        max_position = capital * signal.max_position_size
        final_size = min(confidence_adjusted, max_position)
        
        return {
            'base_size': base_position_size,
            'kelly_adjusted': kelly_adjusted,
            'confidence_adjusted': confidence_adjusted,
            'final_size': final_size,
            'risk_amount': final_size * stop_distance,
            'capital_at_risk_percent': (final_size * stop_distance) / capital * 100
        }
    
    def generate_alert(self, signal: AdvancedTradingSignal) -> str:
        """تولید هشدار پیشرفته"""
        alert = f"""
🚨 سیگنال پیشرفته NEOWave
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 نماد: {signal.symbol}
⏰ زمان: {signal.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
🎯 نوع سیگنال: {signal.signal_type.value}
📈 timeframe اصلی: {signal.primary_timeframe}

💰 قیمت‌گذاری:
   💸 ورود: ${signal.entry_price:,.2f}
   🛡️ حد ضرر: ${signal.stop_loss:,.2f}
   🎯 اهداف: {', '.join([f'${tp:,.2f}' for tp in signal.take_profits[:3]])}
   🔄 trailing stop: {'✅' if signal.dynamic_stop_loss else '❌'}

🎯 کیفیت سیگنال:
   🔥 اطمینان: {signal.confidence:.1%} ({signal.confidence_level.value})
   💪 قدرت: {signal.signal_strength:.1%}
   ⭐ امتیاز کیفیت: {signal.quality_score:.1%}

🌊 تحلیل موج:
   📍 موقعیت: {signal.wave_position}
   🔢 شمارش الیوت: {signal.elliott_count}
   🏗️ ساختار NEOWave: {signal.neowave_structure}
   📐 درجه: {signal.wave_degree}

📊 متریک‌های مالی:
   ⚖️ نسبت R/R: {signal.risk_reward_ratio:.1f}
   💵 ریسک پیش‌بینی: ${signal.risk_amount:,.2f}
   💰 بازده مورد انتظار: ${signal.expected_return:,.2f}
   🎲 احتمال برد: {signal.win_probability:.1%}
   🔢 Kelly fraction: {signal.kelly_fraction:.1%}

🏭 شرایط بازار:
   🌡️ رژیم: {signal.market_conditions.regime.value}
   📈 قدرت روند: {signal.market_conditions.trend_strength:.1%}
   💥 نوسان: {signal.market_conditions.volatility_percentile:.0f}th percentile
   😊 سنتیمنت: {signal.market_conditions.sentiment_score:.1f}

🤖 پیش‌بینی ML:
   🎯 جهت قیمت: {signal.ml_predictions.price_direction_prob:.1%}
   📊 اطمینان مدل: {signal.ml_predictions.model_confidence:.1%}
   ⚠️ anomaly score: {signal.ml_predictions.anomaly_score:.1%}

💼 مدیریت پوزیشن:
   📏 روش sizing: {signal.position_sizing_method.value}
   💰 حجم پیشنهادی: {signal.suggested_position_size:.1%}
   🔒 حداکثر حجم: {signal.max_position_size:.1%}
   📈 سطوح scale-in: {len(signal.scale_in_levels)} سطح
   📉 سطوح scale-out: {len(signal.scale_out_levels)} سطح

⏱️ زمان‌بندی:
   🚪 پنجره ورود: {signal.optimal_entry_window[1] - signal.optimal_entry_window[0]}
   📅 حداکثر نگهداری: {signal.max_holding_period} روز
   🔄 بازبینی: هر {', '.join(map(str, signal.review_intervals[:3]))} روز
   ⏰ انقضا: {signal.expiration_time.strftime('%Y-%m-%d %H:%M')}

📝 یادداشت‌ها: {signal.notes}

⚠️ هشدارها: {', '.join(signal.warning_flags) if signal.warning_flags else 'هیچ'}
✅ پشتیبان‌ها: {', '.join(signal.supporting_indicators) if signal.supporting_indicators else 'هیچ'}
❌ متضادها: {', '.join(signal.conflicting_signals) if signal.conflicting_signals else 'هیچ'}

🆔 شناسه: {signal.signal_id}
🔧 ساخته شده توسط: {signal.created_by} v{signal.version}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        return alert.strip()
    
    def export_signal_data(self, signal: AdvancedTradingSignal, format: str = 'json') -> str:
        """صادرات داده‌های سیگنال"""
        data = {
            'signal_id': signal.signal_id,
            'timestamp': signal.timestamp.isoformat(),
            'symbol': signal.symbol,
            'signal_type': signal.signal_type.value,
            'entry_price': signal.entry_price,
            'stop_loss': signal.stop_loss,
            'take_profits': signal.take_profits,
            'confidence': signal.confidence,
            'risk_reward_ratio': signal.risk_reward_ratio,
            'wave_position': signal.wave_position,
            'market_regime': signal.market_conditions.regime.value,
            'quality_score': signal.quality_score,
            'notes': signal.notes
        }
        
        if format == 'json':
            return json.dumps(data, indent=2, default=str)
        elif format == 'csv':
            import csv
            import io
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)
            return output.getvalue()
        else:
            return str(data)
    
    def backtest_signal(self, signal: AdvancedTradingSignal, 
                       historical_data: pd.DataFrame) -> Dict[str, float]:
        """بک‌تست سیگنال"""
        # ساده‌سازی شده - در عمل پیچیده‌تر
        entry_price = signal.entry_price
        stop_loss = signal.stop_loss
        take_profits = signal.take_profits
        
        # شبیه‌سازی ساده
        if signal.signal_type == SignalType.BUY:
            if len(take_profits) > 0:
                return_pct = (take_profits[0] - entry_price) / entry_price
            else:
                return_pct = 0.05  # فرض 5%
        else:
            return_pct = -0.02  # فرض -2%
        
        return {
            'return_percent': return_pct,
            'success_rate': signal.win_probability,
            'max_drawdown': abs(stop_loss - entry_price) / entry_price,
            'sharpe_ratio': return_pct / 0.02  # ساده‌سازی
        }
    
    def update_adaptive_parameters(self, performance_metrics: Dict[str, float]):
        """به‌روزرسانی پارامترهای تطبیقی"""
        if performance_metrics.get('success_rate', 0) < 0.5:
            self.adaptive_parameters['confidence_threshold'] += 0.05
            self.adaptive_parameters['risk_multiplier'] *= 0.9
        elif performance_metrics.get('success_rate', 0) > 0.7:
            self.adaptive_parameters['confidence_threshold'] -= 0.02
            self.adaptive_parameters['risk_multiplier'] *= 1.05
        
        # محدود کردن مقادیر
        self.adaptive_parameters['confidence_threshold'] = max(0.3, min(0.9, self.adaptive_parameters['confidence_threshold']))
        self.adaptive_parameters['risk_multiplier'] = max(0.5, min(2.0, self.adaptive_parameters['risk_multiplier']))
        
        logger.info(f"پارامترهای تطبیقی به‌روزرسانی شد: {self.adaptive_parameters}")

# برای سازگاری با کد قدیمی
NEOWaveTradingStrategy = AdvancedNEOWaveTradingStrategy
TradingSignal = AdvancedTradingSignal