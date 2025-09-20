"""
Advanced Money Management & Risk Control System
سیستم پیشرفته مدیریت سرمایه و کنترل ریسک - نسخه حرفه‌ای
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union, Any
import json
import sqlite3
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import warnings
import logging
from scipy import stats, optimize
from scipy.stats import norm, t, skew, kurtosis
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
import math
from collections import defaultdict, deque
import talib

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskModelType(Enum):
    """انواع مدل‌های ریسک"""
    PARAMETRIC_VAR = "پارامتریک VAR"
    HISTORICAL_VAR = "تاریخی VAR"
    MONTE_CARLO_VAR = "مونت کارلو VAR"
    CVAR = "CVaR"
    EXPECTED_SHORTFALL = "انتظار کمبود"
    EXTREME_VALUE_THEORY = "نظریه مقادیر حدی"
    COPULA_GARCH = "کوپولا-گارچ"
    REGIME_SWITCHING = "تغییر رژیم"

class PositionSizeMethod(Enum):
    """روش‌های تعیین حجم معامله"""
    FIXED_RISK = "ریسک ثابت"
    KELLY_CRITERION = "معیار کلی"
    VOLATILITY_ADJUSTED = "تنظیم شده بر اساس نوسان"
    CORRELATION_ADJUSTED = "تنظیم شده بر اساس همبستگی"
    MACHINE_LEARNING = "یادگیری ماشین"
    DYNAMIC_RISK_PARITY = "برابری ریسک پویا"
    MAXIMUM_DIVERSIFICATION = "حداکثر تنوع"
    MINIMUM_VARIANCE = "حداقل واریانس"
    BLACK_LITTERMAN = "بلک-لیترمن"

class MarketRegime(Enum):
    """رژیم‌های بازار"""
    BULL_TRENDING = "روند صعودی"
    BEAR_TRENDING = "روند نزولی"
    HIGH_VOLATILITY = "نوسان بالا"
    LOW_VOLATILITY = "نوسان پایین"
    SIDEWAYS = "خنثی"
    CRISIS = "بحران"
    RECOVERY = "بهبود"
    UNKNOWN = "نامشخص"

class PortfolioOptimization(Enum):
    """روش‌های بهینه‌سازی پرتفوی"""
    MEAN_VARIANCE = "میانگین-واریانس"
    BLACK_LITTERMAN = "بلک-لیترمن"
    RISK_PARITY = "برابری ریسک"
    HIERARCHICAL_RISK_PARITY = "برابری ریسک سلسله‌مراتبی"
    MEAN_REVERSION = "بازگشت به میانگین"
    MOMENTUM = "ممنتوم"
    MULTI_FACTOR = "چند عاملی"

@dataclass
class RiskMetrics:
    """متریک‌های ریسک پیشرفته"""
    var_95: float = 0.0
    var_99: float = 0.0
    cvar_95: float = 0.0
    cvar_99: float = 0.0
    expected_shortfall: float = 0.0
    maximum_drawdown: float = 0.0
    calmar_ratio: float = 0.0
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0
    omega_ratio: float = 0.0
    tail_ratio: float = 0.0
    skewness: float = 0.0
    excess_kurtosis: float = 0.0
    volatility: float = 0.0
    tracking_error: float = 0.0
    information_ratio: float = 0.0
    treynor_ratio: float = 0.0
    jensen_alpha: float = 0.0
    beta: float = 0.0
    correlation_portfolio: float = 0.0
    diversification_ratio: float = 0.0
    concentration_index: float = 0.0

@dataclass
class Position:
    """کلاس پوزیشن پیشرفته"""
    position_id: str
    symbol: str
    signal_source: str  # NEOWave, Elliott, etc.
    wave_type: str
    wave_degree: int
    entry_price: float
    quantity: float
    position_type: str  # LONG/SHORT
    entry_time: datetime
    stop_loss: float
    take_profits: List[float]
    confidence_score: float
    risk_score: float
    correlation_risk: float
    liquidity_score: float
    market_regime: MarketRegime
    
    # متغیرهای محاسبه شده
    current_price: float = 0.0
    unrealized_pnl: float = 0.0
    unrealized_pnl_percent: float = 0.0
    realized_pnl: float = 0.0
    realized_pnl_percent: float = 0.0
    exit_time: Optional[datetime] = None
    exit_price: Optional[float] = None
    exit_reason: str = ""
    duration_hours: float = 0.0
    
    # ریسک و عملکرد
    max_risk: float = 0.0
    current_risk: float = 0.0
    risk_reward_ratio: float = 0.0
    win_probability: float = 0.0
    position_score: float = 0.0
    
    # داده‌های اضافی
    metadata: Dict = field(default_factory=dict)
    price_history: List[Tuple[datetime, float]] = field(default_factory=list)
    risk_history: List[Tuple[datetime, float]] = field(default_factory=list)
    
    def update_current_data(self, current_price: float, timestamp: datetime = None):
        """بروزرسانی داده‌های جاری"""
        if timestamp is None:
            timestamp = datetime.now()
            
        self.current_price = current_price
        self.price_history.append((timestamp, current_price))
        
        # محاسبه PnL
        if self.position_type == "LONG":
            self.unrealized_pnl = (current_price - self.entry_price) * self.quantity
        else:
            self.unrealized_pnl = (self.entry_price - current_price) * self.quantity
            
        position_value = self.entry_price * self.quantity
        self.unrealized_pnl_percent = (self.unrealized_pnl / position_value) * 100
        
        # محاسبه ریسک فعلی
        if self.position_type == "LONG":
            risk_distance = abs(current_price - self.stop_loss) / current_price
        else:
            risk_distance = abs(self.stop_loss - current_price) / current_price
            
        self.current_risk = risk_distance * position_value
        self.risk_history.append((timestamp, self.current_risk))
        
        # محاسبه مدت زمان
        self.duration_hours = (timestamp - self.entry_time).total_seconds() / 3600

@dataclass
class PortfolioState:
    """وضعیت پرتفوی"""
    total_capital: float
    available_capital: float
    invested_capital: float
    total_pnl: float
    daily_pnl: float
    unrealized_pnl: float
    realized_pnl: float
    exposure_percent: float
    leverage: float
    positions_count: int
    risk_metrics: RiskMetrics
    last_update: datetime

class MarketRegimeDetector:
    """تشخیص رژیم بازار"""
    
    def __init__(self, lookback_period: int = 252):
        self.lookback_period = lookback_period
        self.regime_history = deque(maxlen=1000)
        
    def detect_regime(self, price_data: pd.Series, volume_data: pd.Series = None) -> MarketRegime:
        """تشخیص رژیم فعلی بازار"""
        if len(price_data) < 50:
            return MarketRegime.UNKNOWN
            
        # محاسبه شاخص‌های تکنیکال
        returns = price_data.pct_change().dropna()
        volatility = returns.rolling(20).std() * np.sqrt(252)
        
        # روند
        sma_short = price_data.rolling(20).mean()
        sma_long = price_data.rolling(50).mean()
        trend_strength = ((sma_short.iloc[-1] - sma_long.iloc[-1]) / sma_long.iloc[-1]) * 100
        
        # نوسان
        current_vol = volatility.iloc[-1] if not volatility.empty else 0
        vol_percentile = self._calculate_percentile(volatility, current_vol)
        
        # تشخیص رژیم
        if abs(trend_strength) > 5:
            if trend_strength > 0:
                if vol_percentile > 75:
                    regime = MarketRegime.HIGH_VOLATILITY
                else:
                    regime = MarketRegime.BULL_TRENDING
            else:
                if vol_percentile > 75:
                    regime = MarketRegime.CRISIS
                else:
                    regime = MarketRegime.BEAR_TRENDING
        else:
            if vol_percentile > 75:
                regime = MarketRegime.HIGH_VOLATILITY
            elif vol_percentile < 25:
                regime = MarketRegime.LOW_VOLATILITY
            else:
                regime = MarketRegime.SIDEWAYS
                
        self.regime_history.append((datetime.now(), regime))
        return regime
        
    def _calculate_percentile(self, data: pd.Series, value: float) -> float:
        """محاسبه صدک"""
        if len(data) == 0:
            return 50
        return (data < value).sum() / len(data) * 100

class AdvancedRiskCalculator:
    """محاسبه‌گر ریسک پیشرفته"""
    
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
        self.alpha = 1 - confidence_level
        
    def calculate_parametric_var(self, returns: pd.Series, holding_period: int = 1) -> float:
        """محاسبه VAR پارامتریک"""
        if len(returns) < 30:
            return 0.0
            
        mean_return = returns.mean()
        std_return = returns.std()
        
        # فرض توزیع نرمال
        z_score = norm.ppf(self.alpha)
        var = -(mean_return + z_score * std_return) * np.sqrt(holding_period)
        
        return var
        
    def calculate_historical_var(self, returns: pd.Series, holding_period: int = 1) -> float:
        """محاسبه VAR تاریخی"""
        if len(returns) < 30:
            return 0.0
            
        # مرتب‌سازی بازده‌ها
        sorted_returns = returns.sort_values()
        index = int(self.alpha * len(sorted_returns))
        
        if index == 0:
            index = 1
            
        var = -sorted_returns.iloc[index - 1] * np.sqrt(holding_period)
        return var
        
    def calculate_cvar(self, returns: pd.Series, holding_period: int = 1) -> float:
        """محاسبه Conditional VAR"""
        if len(returns) < 30:
            return 0.0
            
        var = self.calculate_historical_var(returns, holding_period)
        
        # میانگین ضررهای بیش از VAR
        tail_losses = returns[returns <= -var]
        
        if len(tail_losses) == 0:
            return var
            
        cvar = -tail_losses.mean() * np.sqrt(holding_period)
        return cvar
        
    def calculate_monte_carlo_var(self, returns: pd.Series, simulations: int = 10000, 
                                holding_period: int = 1) -> float:
        """محاسبه VAR با شبیه‌سازی مونت کارلو"""
        if len(returns) < 30:
            return 0.0
            
        mean_return = returns.mean()
        std_return = returns.std()
        
        # شبیه‌سازی
        np.random.seed(42)
        simulated_returns = np.random.normal(mean_return, std_return, simulations)
        
        # محاسبه VAR
        var_index = int(self.alpha * simulations)
        simulated_returns_sorted = np.sort(simulated_returns)
        
        var = -simulated_returns_sorted[var_index] * np.sqrt(holding_period)
        return var
        
    def calculate_expected_shortfall(self, returns: pd.Series, holding_period: int = 1) -> float:
        """محاسبه Expected Shortfall"""
        return self.calculate_cvar(returns, holding_period)
        
    def calculate_maximum_drawdown(self, cumulative_returns: pd.Series) -> float:
        """محاسبه حداکثر افت"""
        if len(cumulative_returns) < 2:
            return 0.0
            
        # محاسبه peaks
        cummax = cumulative_returns.cummax()
        drawdown = (cumulative_returns - cummax) / cummax
        
        return abs(drawdown.min())
        
    def calculate_portfolio_var(self, positions: List[Position], 
                              correlation_matrix: pd.DataFrame) -> float:
        """محاسبه VAR پرتفوی با در نظر گیری همبستگی"""
        if not positions:
            return 0.0
            
        # محاسبه ماتریس کوواریانس
        weights = []
        symbols = []
        
        for pos in positions:
            weights.append(pos.quantity * pos.current_price)
            symbols.append(pos.symbol)
            
        if len(weights) == 0:
            return 0.0
            
        weights = np.array(weights)
        total_value = weights.sum()
        
        if total_value == 0:
            return 0.0
            
        weights = weights / total_value
        
        # VAR فردی
        individual_vars = [pos.current_risk for pos in positions]
        
        if len(individual_vars) != len(weights):
            return sum(individual_vars)
            
        # VAR پرتفوی
        portfolio_var = 0.0
        
        for i in range(len(weights)):
            for j in range(len(weights)):
                if i < len(symbols) and j < len(symbols):
                    symbol_i = symbols[i]
                    symbol_j = symbols[j]
                    
                    correlation = 1.0
                    if (symbol_i in correlation_matrix.index and 
                        symbol_j in correlation_matrix.columns):
                        correlation = correlation_matrix.loc[symbol_i, symbol_j]
                    
                    portfolio_var += (weights[i] * weights[j] * 
                                    individual_vars[i] * individual_vars[j] * correlation)
                    
        return np.sqrt(portfolio_var) if portfolio_var > 0 else 0.0

class MLPositionSizer:
    """تعیین حجم معامله با یادگیری ماشین"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_columns = []
        
    def prepare_features(self, market_data: pd.DataFrame, position_data: Dict) -> np.ndarray:
        """آماده‌سازی ویژگی‌ها برای مدل"""
        features = []
        
        # ویژگی‌های بازار
        if len(market_data) >= 20:
            close_prices = market_data['close']
            volumes = market_data['volume']
            
            # شاخص‌های تکنیکال
            rsi = talib.RSI(close_prices.values, timeperiod=14)
            macd, _, _ = talib.MACD(close_prices.values)
            bb_upper, bb_middle, bb_lower = talib.BBANDS(close_prices.values)
            atr = talib.ATR(market_data['high'].values, 
                           market_data['low'].values, 
                           close_prices.values)
            
            # ویژگی‌های آماری
            returns = close_prices.pct_change()
            volatility = returns.rolling(20).std()
            
            features.extend([
                rsi[-1] if not np.isnan(rsi[-1]) else 50,
                macd[-1] if not np.isnan(macd[-1]) else 0,
                (close_prices.iloc[-1] - bb_middle[-1]) / bb_middle[-1] if not np.isnan(bb_middle[-1]) else 0,
                atr[-1] / close_prices.iloc[-1] if not np.isnan(atr[-1]) else 0.01,
                volatility.iloc[-1] if not np.isnan(volatility.iloc[-1]) else 0.01,
                returns.iloc[-20:].mean() if len(returns) >= 20 else 0,
                volumes.iloc[-1] / volumes.iloc[-20:].mean() if len(volumes) >= 20 else 1
            ])
        else:
            features.extend([50, 0, 0, 0.01, 0.01, 0, 1])
            
        # ویژگی‌های سیگنال
        features.extend([
            position_data.get('confidence_score', 0.5),
            position_data.get('risk_reward_ratio', 1.0),
            position_data.get('wave_degree', 0),
            1 if position_data.get('position_type') == 'LONG' else 0,
            position_data.get('stop_loss_distance', 0.02),
            len(position_data.get('take_profits', []))
        ])
        
        # ویژگی‌های پرتفوی
        features.extend([
            position_data.get('portfolio_exposure', 0),
            position_data.get('correlation_risk', 0),
            position_data.get('current_positions_count', 0),
            position_data.get('recent_performance', 0)
        ])
        
        self.feature_columns = [
            'rsi', 'macd', 'bb_position', 'atr_ratio', 'volatility',
            'mean_return', 'volume_ratio', 'confidence', 'risk_reward',
            'wave_degree', 'is_long', 'stop_distance', 'tp_count',
            'portfolio_exposure', 'correlation_risk', 'positions_count', 'performance'
        ]
        
        return np.array(features).reshape(1, -1)
        
    def train_model(self, training_data: pd.DataFrame):
        """آموزش مدل"""
        if len(training_data) < 100:
            logger.warning("داده‌های آموزشی کافی نیست")
            return
            
        # آماده‌سازی داده‌ها
        X = training_data[self.feature_columns]
        y = training_data['optimal_position_size']
        
        # تمیزکاری داده‌ها
        X = X.fillna(X.mean())
        y = y.fillna(y.mean())
        
        # تقسیم داده‌ها
        tscv = TimeSeriesSplit(n_splits=5)
        
        # آموزش مدل
        self.model = GradientBoostingRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            random_state=42
        )
        
        # اعتبارسنجی متقابل
        scores = []
        for train_idx, val_idx in tscv.split(X):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            # نرمال‌سازی
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_val_scaled = self.scaler.transform(X_val)
            
            # آموزش
            self.model.fit(X_train_scaled, y_train)
            
            # پیش‌بینی
            y_pred = self.model.predict(X_val_scaled)
            score = r2_score(y_val, y_pred)
            scores.append(score)
            
        self.is_trained = True
        logger.info(f"مدل آموزش داده شد. میانگین R²: {np.mean(scores):.3f}")
        
        # ذخیره مدل
        joblib.dump(self.model, 'ml_position_sizer.pkl')
        joblib.dump(self.scaler, 'ml_scaler.pkl')
        
    def predict_position_size(self, features: np.ndarray, base_size: float) -> float:
        """پیش‌بینی حجم بهینه معامله"""
        if not self.is_trained or self.model is None:
            return base_size
            
        try:
            # نرمال‌سازی
            features_scaled = self.scaler.transform(features)
            
            # پیش‌بینی
            multiplier = self.model.predict(features_scaled)[0]
            
            # محدودیت‌ها
            multiplier = max(0.1, min(3.0, multiplier))
            
            return base_size * multiplier
            
        except Exception as e:
            logger.error(f"خطا در پیش‌بینی حجم: {e}")
            return base_size
            
    def load_model(self):
        """بارگذاری مدل ذخیره شده"""
        try:
            self.model = joblib.load('ml_position_sizer.pkl')
            self.scaler = joblib.load('ml_scaler.pkl')
            self.is_trained = True
            logger.info("مدل با موفقیت بارگذاری شد")
        except:
            logger.warning("مدل ذخیره شده یافت نشد")

class AdvancedMoneyManager:
    """مدیریت سرمایه پیشرفته"""
    
    def __init__(self, initial_capital: float, config: Dict = None):
        """مقداردهی اولیه"""
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.config = config or self._get_default_config()
        
        # تنظیمات ریسک
        self.max_risk_per_trade = self.config.get('max_risk_per_trade', 0.02)
        self.max_portfolio_risk = self.config.get('max_portfolio_risk', 0.06)
        self.max_correlation_exposure = self.config.get('max_correlation_exposure', 0.4)
        self.max_positions = self.config.get('max_positions', 5)
        self.max_leverage = self.config.get('max_leverage', 1.0)
        
        # مولفه‌های سیستم
        self.positions: List[Position] = []
        self.closed_positions: List[Position] = []
        self.risk_calculator = AdvancedRiskCalculator()
        self.regime_detector = MarketRegimeDetector()
        self.ml_sizer = MLPositionSizer()
        self.ml_sizer.load_model()
        
        # داده‌های عملکرد
        self.equity_curve = [initial_capital]
        self.daily_returns = []
        self.performance_history = deque(maxlen=1000)
        self.risk_metrics_history = deque(maxlen=100)
        
        # پایگاه داده
        self.db_connection = self._initialize_database()
        
        # تنظیمات real-time
        self.last_update = datetime.now()
        self.update_frequency = timedelta(minutes=1)
        
        # کش برای بهبود عملکرد
        self.correlation_cache = {}
        self.volatility_cache = {}
        self.cache_expiry = timedelta(hours=1)
        
        logger.info(f"💰 سیستم مدیریت سرمایه پیشرفته راه‌اندازی شد - سرمایه اولیه: ${initial_capital:,.2f}")
        
    def _get_default_config(self) -> Dict:
        """تنظیمات پیش‌فرض"""
        return {
            'max_risk_per_trade': 0.02,           # 2% ریسک برای هر معامله
            'max_portfolio_risk': 0.06,           # 6% ریسک کل پرتفوی
            'max_correlation_exposure': 0.4,      # 40% حداکثر در دارایی‌های همبسته
            'max_positions': 5,                   # حداکثر 5 پوزیشن همزمان
            'max_leverage': 1.0,                  # بدون اهرم
            'rebalance_threshold': 0.05,          # 5% انحراف برای rebalance
            'emergency_stop_loss': 0.15,          # 15% stop loss اضطراری
            'volatility_lookback': 20,            # 20 روز برای محاسبه نوسان
            'correlation_lookback': 50,           # 50 روز برای همبستگی
            'position_size_method': PositionSizeMethod.VOLATILITY_ADJUSTED,
            'risk_model': RiskModelType.HISTORICAL_VAR,
            'optimization_method': PortfolioOptimization.RISK_PARITY,
            'regime_sensitivity': 0.7,            # حساسیت تشخیص رژیم
            'ml_enabled': True,                   # فعالسازی ML
            'stress_test_enabled': True,          # فعالسازی stress test
            'real_time_monitoring': True          # مانیتورینگ real-time
        }
        
    def _initialize_database(self) -> sqlite3.Connection:
        """راه‌اندازی پایگاه داده"""
        try:
            conn = sqlite3.connect('portfolio_management.db', check_same_thread=False)
            
            # جدول پوزیشن‌ها
            conn.execute('''
                CREATE TABLE IF NOT EXISTS positions (
                    position_id TEXT PRIMARY KEY,
                    symbol TEXT,
                    signal_source TEXT,
                    wave_type TEXT,
                    wave_degree INTEGER,
                    entry_price REAL,
                    quantity REAL,
                    position_type TEXT,
                    entry_time TEXT,
                    exit_time TEXT,
                    exit_price REAL,
                    realized_pnl REAL,
                    risk_score REAL,
                    confidence_score REAL,
                    metadata TEXT
                )
            ''')
            
            # جدول متریک‌های ریسک
            conn.execute('''
                CREATE TABLE IF NOT EXISTS risk_metrics (
                    timestamp TEXT,
                    portfolio_value REAL,
                    var_95 REAL,
                    var_99 REAL,
                    max_drawdown REAL,
                    sharpe_ratio REAL,
                    positions_count INTEGER,
                    exposure_percent REAL
                )
            ''')
            
            # جدول عملکرد روزانه
            conn.execute('''
                CREATE TABLE IF NOT EXISTS daily_performance (
                    date TEXT PRIMARY KEY,
                    portfolio_value REAL,
                    daily_return REAL,
                    volatility REAL,
                    trades_count INTEGER,
                    win_rate REAL
                )
            ''')
            
            conn.commit()
            return conn
            
        except Exception as e:
            logger.error(f"خطا در راه‌اندازی پایگاه داده: {e}")
            return None
            
    def calculate_optimal_position_size(self, signal_data: Dict, 
                                      market_data: pd.DataFrame) -> Dict:
        """محاسبه حجم بهینه معامله"""
        try:
            entry_price = signal_data.get('entry_price', 0)
            stop_loss = signal_data.get('stop_loss', 0)
            confidence = signal_data.get('confidence_score', 0.5)
            
            if entry_price <= 0 or stop_loss <= 0:
                return {'size': 0, 'risk': 0, 'method': 'INVALID_PRICES'}
                
            # محاسبه ریسک پایه
            price_risk = abs(entry_price - stop_loss) / entry_price
            max_loss_per_share = abs(entry_price - stop_loss)
            
            # روش‌های مختلف محاسبه حجم
            method = self.config.get('position_size_method', PositionSizeMethod.VOLATILITY_ADJUSTED)
            
            if method == PositionSizeMethod.FIXED_RISK:
                size = self._calculate_fixed_risk_size(max_loss_per_share, confidence)
                
            elif method == PositionSizeMethod.KELLY_CRITERION:
                size = self._calculate_kelly_size(signal_data, market_data)
                
            elif method == PositionSizeMethod.VOLATILITY_ADJUSTED:
                size = self._calculate_volatility_adjusted_size(
                    signal_data, market_data, max_loss_per_share
                )
                
            elif method == PositionSizeMethod.CORRELATION_ADJUSTED:
                size = self._calculate_correlation_adjusted_size(
                    signal_data, market_data, max_loss_per_share
                )
                
            elif method == PositionSizeMethod.MACHINE_LEARNING:
                size = self._calculate_ml_size(signal_data, market_data, max_loss_per_share)
                
            else:
                size = self._calculate_fixed_risk_size(max_loss_per_share, confidence)
                
            # اعمال محدودیت‌ها
            size = self._apply_position_limits(size, entry_price, signal_data)
            
            # محاسبه ریسک نهایی
            total_risk = size * max_loss_per_share
            risk_percent = (total_risk / self.current_capital) * 100
            
            return {
                'size': round(size, 8),
                'risk_amount': total_risk,
                'risk_percent': risk_percent,
                'method': method.value,
                'price_risk': price_risk,
                'confidence_adjusted': confidence,
                'capital_utilization': (size * entry_price / self.current_capital) * 100
            }
            
        except Exception as e:
            logger.error(f"خطا در محاسبه حجم معامله: {e}")
            return {'size': 0, 'risk': 0, 'method': 'ERROR'}
            
    def _calculate_fixed_risk_size(self, max_loss_per_share: float, confidence: float) -> float:
        """محاسبه حجم با ریسک ثابت"""
        risk_capital = self.current_capital * self.max_risk_per_trade * confidence
        size = risk_capital / max_loss_per_share if max_loss_per_share > 0 else 0
        return size
        
    def _calculate_kelly_size(self, signal_data: Dict, market_data: pd.DataFrame) -> float:
        """محاسبه حجم با معیار کلی"""
        try:
            # آمار تاریخی سیگنال‌ها
            win_rate = self._get_signal_win_rate(signal_data.get('signal_source', ''))
            avg_win = self._get_average_win(signal_data.get('signal_source', ''))
            avg_loss = self._get_average_loss(signal_data.get('signal_source', ''))
            
            if avg_loss <= 0:
                return self._calculate_fixed_risk_size(
                    abs(signal_data.get('entry_price', 0) - signal_data.get('stop_loss', 0)),
                    signal_data.get('confidence_score', 0.5)
                )
                
            # فرمول کلی
            win_loss_ratio = avg_win / avg_loss
            kelly_fraction = (win_rate * win_loss_ratio - (1 - win_rate)) / win_loss_ratio
            
            # اعمال فاکتور محافظه‌کارانه
            kelly_fraction = max(0, min(0.25, kelly_fraction * 0.5))
            
            # محاسبه حجم
            risk_capital = self.current_capital * kelly_fraction
            max_loss = abs(signal_data.get('entry_price', 0) - signal_data.get('stop_loss', 0))
            
            size = risk_capital / max_loss if max_loss > 0 else 0
            return size
            
        except Exception as e:
            logger.error(f"خطا در محاسبه کلی: {e}")
            return 0
            
    def _calculate_volatility_adjusted_size(self, signal_data: Dict, 
                                          market_data: pd.DataFrame, 
                                          max_loss_per_share: float) -> float:
        """محاسبه حجم تنظیم شده بر اساس نوسان"""
        try:
            symbol = signal_data.get('symbol', '')
            
            # محاسبه نوسان
            if len(market_data) >= 20:
                returns = market_data['close'].pct_change().dropna()
                volatility = returns.std() * np.sqrt(252)  # نوسان سالانه
            else:
                volatility = 0.3  # نوسان پیش‌فرض
                
            # تنظیم ریسک بر اساس نوسان
            vol_factor = max(0.5, min(2.0, 0.3 / volatility))
            adjusted_risk = self.max_risk_per_trade * vol_factor
            
            # محاسبه حجم
            risk_capital = self.current_capital * adjusted_risk * signal_data.get('confidence_score', 0.5)
            size = risk_capital / max_loss_per_share if max_loss_per_share > 0 else 0
            
            return size
            
        except Exception as e:
            logger.error(f"خطا در محاسبه حجم تنظیم شده نوسان: {e}")
            return 0
            
    def _calculate_correlation_adjusted_size(self, signal_data: Dict,
                                           market_data: pd.DataFrame,
                                           max_loss_per_share: float) -> float:
        """محاسبه حجم تنظیم شده بر اساس همبستگی"""
        try:
            symbol = signal_data.get('symbol', '')
            
            # محاسبه همبستگی با پوزیشن‌های موجود
            correlation_risk = self._calculate_portfolio_correlation_risk(symbol, market_data)
            
            # تنظیم ریسک بر اساس همبستگی
            correlation_factor = max(0.3, 1.0 - correlation_risk)
            adjusted_risk = self.max_risk_per_trade * correlation_factor
            
            # محاسبه حجم
            risk_capital = self.current_capital * adjusted_risk * signal_data.get('confidence_score', 0.5)
            size = risk_capital / max_loss_per_share if max_loss_per_share > 0 else 0
            
            return size
            
        except Exception as e:
            logger.error(f"خطا در محاسبه حجم تنظیم شده همبستگی: {e}")
            return 0
            
    def _calculate_ml_size(self, signal_data: Dict, 
                          market_data: pd.DataFrame,
                          max_loss_per_share: float) -> float:
        """محاسبه حجم با یادگیری ماشین"""
        try:
            # محاسبه حجم پایه
            base_size = self._calculate_volatility_adjusted_size(
                signal_data, market_data, max_loss_per_share
            )
            
            if not self.ml_sizer.is_trained:
                return base_size
                
            # آماده‌سازی ویژگی‌ها
            features = self.ml_sizer.prepare_features(market_data, signal_data)
            
            # پیش‌بینی حجم بهینه
            optimal_size = self.ml_sizer.predict_position_size(features, base_size)
            
            return optimal_size
            
        except Exception as e:
            logger.error(f"خطا در محاسبه حجم ML: {e}")
            return self._calculate_volatility_adjusted_size(
                signal_data, market_data, max_loss_per_share
            )
            
    def _apply_position_limits(self, size: float, entry_price: float, 
                              signal_data: Dict) -> float:
        """اعمال محدودیت‌های پوزیشن"""
        if size <= 0 or entry_price <= 0:
            return 0
            
        # محدودیت سرمایه
        position_value = size * entry_price
        max_position_value = self.current_capital * 0.3  # حداکثر 30% سرمایه
        
        if position_value > max_position_value:
            size = max_position_value / entry_price
            
        # محدودیت حداقل
        min_position_value = 100  # حداقل 100 دلار
        if position_value < min_position_value:
            size = min_position_value / entry_price
            
        # محدودیت تعداد پوزیشن‌ها
        if len(self.positions) >= self.max_positions:
            size = 0
            
        # محدودیت ریسک کل پرتفوی
        current_portfolio_risk = self._calculate_portfolio_risk()
        new_position_risk = size * abs(entry_price - signal_data.get('stop_loss', entry_price))
        new_portfolio_risk = (current_portfolio_risk + new_position_risk) / self.current_capital
        
        if new_portfolio_risk > self.max_portfolio_risk:
            allowed_risk = self.max_portfolio_risk * self.current_capital - current_portfolio_risk
            if allowed_risk > 0:
                max_loss = abs(entry_price - signal_data.get('stop_loss', entry_price))
                size = allowed_risk / max_loss if max_loss > 0 else 0
            else:
                size = 0
                
        return max(0, size)
        
    def add_position(self, signal_data: Dict, market_data: pd.DataFrame) -> Optional[Position]:
        """اضافه کردن پوزیشن جدید"""
        try:
            # محاسبه حجم بهینه
            size_result = self.calculate_optimal_position_size(signal_data, market_data)
            
            if size_result['size'] <= 0:
                logger.warning(f"حجم معامله صفر: {signal_data.get('symbol', 'Unknown')}")
                return None
                
            # تشخیص رژیم بازار
            regime = self.regime_detector.detect_regime(market_data['close'])
            
            # ایجاد پوزیشن
            position = Position(
                position_id=self._generate_position_id(),
                symbol=signal_data.get('symbol', ''),
                signal_source=signal_data.get('signal_source', ''),
                wave_type=signal_data.get('wave_type', ''),
                wave_degree=signal_data.get('wave_degree', 0),
                entry_price=signal_data.get('entry_price', 0),
                quantity=size_result['size'],
                position_type=signal_data.get('position_type', 'LONG'),
                entry_time=datetime.now(),
                stop_loss=signal_data.get('stop_loss', 0),
                take_profits=signal_data.get('take_profits', []),
                confidence_score=signal_data.get('confidence_score', 0.5),
                risk_score=size_result['risk_percent'],
                correlation_risk=self._calculate_portfolio_correlation_risk(
                    signal_data.get('symbol', ''), market_data
                ),
                liquidity_score=self._calculate_liquidity_score(market_data),
                market_regime=regime
            )
            
            # محاسبه متادیتا
            position.metadata = {
                'size_method': size_result['method'],
                'capital_utilization': size_result['capital_utilization'],
                'portfolio_positions_before': len(self.positions),
                'market_volatility': market_data['close'].pct_change().std() if len(market_data) > 1 else 0,
                'entry_signals': signal_data
            }
            
            # بروزرسانی داده‌های جاری
            position.update_current_data(position.entry_price, position.entry_time)
            
            # اضافه کردن به پرتفوی
            self.positions.append(position)
            
            # ثبت در پایگاه داده
            self._save_position_to_db(position)
            
            # بروزرسانی سرمایه
            self._update_portfolio_state()
            
            logger.info(f"✅ پوزیشن جدید: {position.symbol} - حجم: {position.quantity:.6f} - ریسک: {position.risk_score:.2f}%")
            
            return position
            
        except Exception as e:
            logger.error(f"خطا در اضافه کردن پوزیشن: {e}")
            return None
            
    def close_position(self, position_id: str, exit_price: float, 
                      reason: str = "Manual") -> Optional[Position]:
        """بستن پوزیشن"""
        try:
            # پیدا کردن پوزیشن
            position = None
            position_index = -1
            
            for i, pos in enumerate(self.positions):
                if pos.position_id == position_id:
                    position = pos
                    position_index = i
                    break
                    
            if position is None:
                logger.warning(f"پوزیشن پیدا نشد: {position_id}")
                return None
                
            # بروزرسانی داده‌های خروج
            position.exit_price = exit_price
            position.exit_time = datetime.now()
            position.exit_reason = reason
            
            # محاسبه PnL نهایی
            if position.position_type == "LONG":
                position.realized_pnl = (exit_price - position.entry_price) * position.quantity
            else:
                position.realized_pnl = (position.entry_price - exit_price) * position.quantity
                
            position_value = position.entry_price * position.quantity
            position.realized_pnl_percent = (position.realized_pnl / position_value) * 100
            
            # انتقال به پوزیشن‌های بسته
            self.closed_positions.append(position)
            self.positions.pop(position_index)
            
            # بروزرسانی سرمایه
            self.current_capital += position.realized_pnl
            self.equity_curve.append(self.current_capital)
            
            # ثبت عملکرد
            self._record_trade_performance(position)
            
            # بروزرسانی پایگاه داده
            self._update_position_in_db(position)
            
            # بروزرسانی وضعیت پرتفوی
            self._update_portfolio_state()
            
            pnl_emoji = "💚" if position.realized_pnl > 0 else "💔"
            logger.info(f"{pnl_emoji} پوزیشن بسته شد: {position.symbol} - PnL: ${position.realized_pnl:,.2f} ({position.realized_pnl_percent:.2f}%)")
            
            return position
            
        except Exception as e:
            logger.error(f"خطا در بستن پوزیشن: {e}")
            return None
            
    def update_positions(self, market_data: Dict[str, pd.DataFrame]):
        """بروزرسانی تمام پوزیشن‌ها"""
        try:
            current_time = datetime.now()
            
            for position in self.positions:
                symbol_data = market_data.get(position.symbol)
                
                if symbol_data is not None and not symbol_data.empty:
                    current_price = symbol_data['close'].iloc[-1]
                    position.update_current_data(current_price, current_time)
                    
                    # بررسی stop loss و take profit
                    self._check_exit_conditions(position, current_price)
                    
            # بروزرسانی وضعیت کلی
            self._update_portfolio_state()
            
            # بروزرسانی کش
            self._update_cache(market_data)
            
        except Exception as e:
            logger.error(f"خطا در بروزرسانی پوزیشن‌ها: {e}")
            
    def _check_exit_conditions(self, position: Position, current_price: float):
        """بررسی شرایط خروج"""
        try:
            # Stop Loss
            if position.position_type == "LONG":
                if current_price <= position.stop_loss:
                    self.close_position(position.position_id, current_price, "Stop Loss")
                    return
                    
                # Take Profit
                for i, tp in enumerate(position.take_profits):
                    if current_price >= tp:
                        # بستن بخشی از پوزیشن
                        partial_quantity = position.quantity / len(position.take_profits)
                        self._partial_close_position(position, tp, partial_quantity, f"Take Profit {i+1}")
                        position.take_profits.remove(tp)
                        break
                        
            else:  # SHORT
                if current_price >= position.stop_loss:
                    self.close_position(position.position_id, current_price, "Stop Loss")
                    return
                    
                # Take Profit
                for i, tp in enumerate(position.take_profits):
                    if current_price <= tp:
                        partial_quantity = position.quantity / len(position.take_profits)
                        self._partial_close_position(position, tp, partial_quantity, f"Take Profit {i+1}")
                        position.take_profits.remove(tp)
                        break
                        
            # شرایط خروج زمانی
            duration_hours = (datetime.now() - position.entry_time).total_seconds() / 3600
            
            # خروج اضطراری برای معاملات طولانی مدت
            if duration_hours > 168:  # بیش از یک هفته
                if position.unrealized_pnl_percent < -5:  # ضرر بیش از 5%
                    self.close_position(position.position_id, current_price, "Emergency Time Exit")
                    
        except Exception as e:
            logger.error(f"خطا در بررسی شرایط خروج: {e}")
            
    def calculate_advanced_metrics(self) -> RiskMetrics:
        """محاسبه متریک‌های پیشرفته ریسک"""
        try:
            if len(self.closed_positions) < 10:
                return RiskMetrics()
                
            # آماده‌سازی داده‌ها
            returns = pd.Series([pos.realized_pnl_percent / 100 for pos in self.closed_positions])
            equity_series = pd.Series(self.equity_curve)
            
            # محاسبه متریک‌ها
            metrics = RiskMetrics()
            
            # VAR و CVaR
            metrics.var_95 = self.risk_calculator.calculate_historical_var(returns, 1) * 100
            metrics.var_99 = self.risk_calculator.calculate_historical_var(
                returns, 1
            ) * 100 if len(returns) > 0 else 0
            
            metrics.cvar_95 = self.risk_calculator.calculate_cvar(returns, 1) * 100
            metrics.cvar_99 = self.risk_calculator.calculate_cvar(returns, 1) * 100
            
            metrics.expected_shortfall = metrics.cvar_95
            
            # حداکثر افت
            metrics.maximum_drawdown = self.risk_calculator.calculate_maximum_drawdown(equity_series) * 100
            
            # نسبت‌های عملکرد
            if len(returns) > 1:
                mean_return = returns.mean()
                std_return = returns.std()
                
                if std_return > 0:
                    metrics.sharpe_ratio = (mean_return / std_return) * np.sqrt(252)
                    
                # Sortino
                negative_returns = returns[returns < 0]
                if len(negative_returns) > 0:
                    downside_std = negative_returns.std()
                    if downside_std > 0:
                        metrics.sortino_ratio = (mean_return / downside_std) * np.sqrt(252)
                        
                # Calmar
                if metrics.maximum_drawdown > 0:
                    annual_return = mean_return * 252
                    metrics.calmar_ratio = annual_return / (metrics.maximum_drawdown / 100)
                    
                # آمار توزیع
                metrics.skewness = skew(returns.values)
                metrics.excess_kurtosis = kurtosis(returns.values)
                
                # نوسان
                metrics.volatility = std_return * np.sqrt(252) * 100
                
            # متریک‌های پرتفوی
            if self.positions:
                total_exposure = sum(pos.quantity * pos.current_price for pos in self.positions)
                metrics.concentration_index = self._calculate_concentration_index()
                metrics.diversification_ratio = self._calculate_diversification_ratio()
                
            return metrics
            
        except Exception as e:
            logger.error(f"خطا در محاسبه متریک‌ها: {e}")
            return RiskMetrics()
            
    def generate_performance_report(self) -> Dict:
        """تولید گزارش عملکرد جامع"""
        try:
            current_metrics = self.calculate_advanced_metrics()
            
            # آمار کلی
            total_trades = len(self.closed_positions)
            winning_trades = len([p for p in self.closed_positions if p.realized_pnl > 0])
            losing_trades = total_trades - winning_trades
            
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            # PnL
            total_pnl = sum(pos.realized_pnl for pos in self.closed_positions)
            total_wins = sum(pos.realized_pnl for pos in self.closed_positions if pos.realized_pnl > 0)
            total_losses = abs(sum(pos.realized_pnl for pos in self.closed_positions if pos.realized_pnl < 0))
            
            profit_factor = (total_wins / total_losses) if total_losses > 0 else float('inf')
            
            # ROI
            roi = ((self.current_capital - self.initial_capital) / self.initial_capital) * 100
            
            # آمار معاملات
            if self.closed_positions:
                avg_win = np.mean([p.realized_pnl for p in self.closed_positions if p.realized_pnl > 0]) if winning_trades > 0 else 0
                avg_loss = np.mean([abs(p.realized_pnl) for p in self.closed_positions if p.realized_pnl < 0]) if losing_trades > 0 else 0
                avg_trade_duration = np.mean([p.duration_hours for p in self.closed_positions])
                
                # بهترین و بدترین معامله
                best_trade = max(self.closed_positions, key=lambda x: x.realized_pnl)
                worst_trade = min(self.closed_positions, key=lambda x: x.realized_pnl)
            else:
                avg_win = avg_loss = avg_trade_duration = 0
                best_trade = worst_trade = None
                
            # وضعیت فعلی
            current_exposure = sum(pos.quantity * pos.current_price for pos in self.positions)
            exposure_percent = (current_exposure / self.current_capital * 100) if self.current_capital > 0 else 0
            
            unrealized_pnl = sum(pos.unrealized_pnl for pos in self.positions)
            
            report = {
                'portfolio_summary': {
                    'initial_capital': self.initial_capital,
                    'current_capital': self.current_capital,
                    'total_pnl': total_pnl,
                    'unrealized_pnl': unrealized_pnl,
                    'roi_percent': roi,
                    'current_positions': len(self.positions),
                    'exposure_percent': exposure_percent
                },
                'trading_statistics': {
                    'total_trades': total_trades,
                    'winning_trades': winning_trades,
                    'losing_trades': losing_trades,
                    'win_rate_percent': win_rate,
                    'profit_factor': profit_factor,
                    'average_win': avg_win,
                    'average_loss': avg_loss,
                    'average_duration_hours': avg_trade_duration
                },
                'risk_metrics': {
                    'var_95_percent': current_metrics.var_95,
                    'var_99_percent': current_metrics.var_99,
                    'max_drawdown_percent': current_metrics.maximum_drawdown,
                    'sharpe_ratio': current_metrics.sharpe_ratio,
                    'sortino_ratio': current_metrics.sortino_ratio,
                    'calmar_ratio': current_metrics.calmar_ratio,
                    'volatility_percent': current_metrics.volatility,
                    'skewness': current_metrics.skewness,
                    'kurtosis': current_metrics.excess_kurtosis
                },
                'best_worst_trades': {
                    'best_trade': {
                        'symbol': best_trade.symbol if best_trade else '',
                        'pnl': best_trade.realized_pnl if best_trade else 0,
                        'pnl_percent': best_trade.realized_pnl_percent if best_trade else 0,
                        'duration': best_trade.duration_hours if best_trade else 0
                    },
                    'worst_trade': {
                        'symbol': worst_trade.symbol if worst_trade else '',
                        'pnl': worst_trade.realized_pnl if worst_trade else 0,
                        'pnl_percent': worst_trade.realized_pnl_percent if worst_trade else 0,
                        'duration': worst_trade.duration_hours if worst_trade else 0
                    }
                },
                'monthly_performance': self._calculate_monthly_performance(),
                'symbol_performance': self._calculate_symbol_performance(),
                'signal_source_performance': self._calculate_signal_performance()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"خطا در تولید گزارش: {e}")
            return {}
            
    def stress_test_portfolio(self, scenarios: List[Dict]) -> Dict:
        """تست استرس پرتفوی"""
        try:
            stress_results = {}
            
            for scenario in scenarios:
                scenario_name = scenario.get('name', 'Unknown')
                price_changes = scenario.get('price_changes', {})
                
                # شبیه‌سازی تغییرات قیمت
                scenario_pnl = 0
                
                for position in self.positions:
                    symbol = position.symbol
                    price_change = price_changes.get(symbol, 0)
                    
                    new_price = position.current_price * (1 + price_change)
                    
                    if position.position_type == "LONG":
                        scenario_pnl += (new_price - position.entry_price) * position.quantity
                    else:
                        scenario_pnl += (position.entry_price - new_price) * position.quantity
                        
                # محاسبه اثر بر سرمایه
                new_capital = self.current_capital + scenario_pnl
                capital_change_percent = ((new_capital - self.current_capital) / self.current_capital) * 100
                
                stress_results[scenario_name] = {
                    'scenario_pnl': scenario_pnl,
                    'new_capital': new_capital,
                    'capital_change_percent': capital_change_percent,
                    'survival': new_capital > self.initial_capital * 0.5  # آیا بیش از 50% سرمایه باقی می‌ماند
                }
                
            return stress_results
            
        except Exception as e:
            logger.error(f"خطا در تست استرس: {e}")
            return {}
            
    def optimize_portfolio(self, method: PortfolioOptimization = None) -> Dict:
        """بهینه‌سازی پرتفوی"""
        try:
            if not self.positions:
                return {'status': 'no_positions', 'recommendations': []}
                
            method = method or self.config.get('optimization_method', PortfolioOptimization.RISK_PARITY)
            
            recommendations = []
            
            if method == PortfolioOptimization.RISK_PARITY:
                recommendations = self._risk_parity_optimization()
            elif method == PortfolioOptimization.MEAN_VARIANCE:
                recommendations = self._mean_variance_optimization()
            elif method == PortfolioOptimization.HIERARCHICAL_RISK_PARITY:
                recommendations = self._hierarchical_risk_parity()
                
            return {
                'status': 'success',
                'method': method.value,
                'recommendations': recommendations,
                'expected_improvement': self._calculate_improvement_potential(recommendations)
            }
            
        except Exception as e:
            logger.error(f"خطا در بهینه‌سازی: {e}")
            return {'status': 'error', 'message': str(e)}
            
    # متدهای کمکی
    def _generate_position_id(self) -> str:
        """تولید شناسه منحصر به فرد پوزیشن"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"POS_{timestamp}_{len(self.positions):03d}"
        
    def _calculate_portfolio_risk(self) -> float:
        """محاسبه ریسک کل پرتفوی"""
        return sum(pos.current_risk for pos in self.positions)
        
    def _calculate_portfolio_correlation_risk(self, new_symbol: str, 
                                            market_data: pd.DataFrame) -> float:
        """محاسبه ریسک همبستگی پرتفوی"""
        if not self.positions:
            return 0.0
            
        try:
            # محاسبه همبستگی با پوزیشن‌های موجود
            correlations = []
            
            for position in self.positions:
                # شبیه‌سازی همبستگی (در عمل باید از داده‌های واقعی استفاده شود)
                if position.symbol == new_symbol:
                    correlations.append(1.0)
                elif position.symbol[:3] == new_symbol[:3]:  # ارزهای مشابه
                    correlations.append(0.7)
                else:
                    correlations.append(0.3)
                    
            return np.mean(correlations) if correlations else 0.0
            
        except Exception:
            return 0.5  # همبستگی متوسط
            
    def _calculate_liquidity_score(self, market_data: pd.DataFrame) -> float:
        """محاسبه امتیاز نقدینگی"""
        try:
            if len(market_data) < 20:
                return 0.5
                
            # محاسبه بر اساس حجم معاملات
            avg_volume = market_data['volume'].rolling(20).mean().iloc[-1]
            current_volume = market_data['volume'].iloc[-1]
            
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
            
            # تبدیل به امتیاز 0-1
            liquidity_score = min(1.0, max(0.1, volume_ratio / 2))
            
            return liquidity_score
            
        except Exception:
            return 0.5
            
    def _get_signal_win_rate(self, signal_source: str) -> float:
        """دریافت نرخ برد سیگنال"""
        if not signal_source:
            return 0.6  # پیش‌فرض
            
        source_trades = [p for p in self.closed_positions if p.signal_source == signal_source]
        
        if len(source_trades) < 10:
            return 0.6
            
        wins = len([p for p in source_trades if p.realized_pnl > 0])
        return wins / len(source_trades)
        
    def _get_average_win(self, signal_source: str) -> float:
        """دریافت میانگین برد"""
        source_trades = [p for p in self.closed_positions 
                        if p.signal_source == signal_source and p.realized_pnl > 0]
        
        if not source_trades:
            return 1.0
            
        return np.mean([abs(p.realized_pnl) for p in source_trades])
        
    def _get_average_loss(self, signal_source: str) -> float:
        """دریافت میانگین ضرر"""
        source_trades = [p for p in self.closed_positions 
                        if p.signal_source == signal_source and p.realized_pnl < 0]
        
        if not source_trades:
            return 1.0
            
        return np.mean([abs(p.realized_pnl) for p in source_trades])
        
    def _update_portfolio_state(self):
        """بروزرسانی وضعیت پرتفوی"""
        try:
            # محاسبه مقادیر فعلی
            total_exposure = sum(pos.quantity * pos.current_price for pos in self.positions)
            unrealized_pnl = sum(pos.unrealized_pnl for pos in self.positions)
            
            # ثبت متریک‌ها
            metrics = self.calculate_advanced_metrics()
            
            # ذخیره در تاریخچه
            portfolio_state = PortfolioState(
                total_capital=self.current_capital + unrealized_pnl,
                available_capital=self.current_capital - total_exposure,
                invested_capital=total_exposure,
                total_pnl=self.current_capital - self.initial_capital + unrealized_pnl,
                daily_pnl=self._calculate_daily_pnl(),
                unrealized_pnl=unrealized_pnl,
                realized_pnl=self.current_capital - self.initial_capital,
                exposure_percent=(total_exposure / self.current_capital * 100) if self.current_capital > 0 else 0,
                leverage=total_exposure / self.current_capital if self.current_capital > 0 else 0,
                positions_count=len(self.positions),
                risk_metrics=metrics,
                last_update=datetime.now()
            )
            
            # ثبت در پایگاه داده
            self._save_risk_metrics_to_db(portfolio_state)
            
        except Exception as e:
            logger.error(f"خطا در بروزرسانی وضعیت پرتفوی: {e}")
            
    def _save_position_to_db(self, position: Position):
        """ذخیره پوزیشن در پایگاه داده"""
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO positions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    position.position_id,
                    position.symbol,
                    position.signal_source,
                    position.wave_type,
                    position.wave_degree,
                    position.entry_price,
                    position.quantity,
                    position.position_type,
                    position.entry_time.isoformat(),
                    position.exit_time.isoformat() if position.exit_time else None,
                    position.exit_price,
                    position.realized_pnl,
                    position.risk_score,
                    position.confidence_score,
                    json.dumps(position.metadata)
                ))
                self.db_connection.commit()
            except Exception as e:
                logger.error(f"خطا در ذخیره پوزیشن: {e}")
                
    def _update_position_in_db(self, position: Position):
        """بروزرسانی پوزیشن در پایگاه داده"""
        self._save_position_to_db(position)
        
    def _save_risk_metrics_to_db(self, portfolio_state: PortfolioState):
        """ذخیره متریک‌های ریسک"""
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute('''
                    INSERT INTO risk_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    portfolio_state.last_update.isoformat(),
                    portfolio_state.total_capital,
                    portfolio_state.risk_metrics.var_95,
                    portfolio_state.risk_metrics.var_99,
                    portfolio_state.risk_metrics.maximum_drawdown,
                    portfolio_state.risk_metrics.sharpe_ratio,
                    portfolio_state.positions_count,
                    portfolio_state.exposure_percent
                ))
                self.db_connection.commit()
            except Exception as e:
                logger.error(f"خطا در ذخیره متریک‌ها: {e}")
                
    # متدهای کمکی اضافی
    def _calculate_concentration_index(self) -> float:
        """محاسبه شاخص تمرکز"""
        if not self.positions:
            return 0.0
            
        total_value = sum(pos.quantity * pos.current_price for pos in self.positions)
        if total_value == 0:
            return 0.0
            
        weights = [(pos.quantity * pos.current_price / total_value) ** 2 for pos in self.positions]
        return sum(weights)
        
    def _calculate_diversification_ratio(self) -> float:
        """محاسبه نسبت تنوع"""
        if len(self.positions) <= 1:
            return 1.0
            
        # شبیه‌سازی ساده
        return min(2.0, np.sqrt(len(self.positions)))
        
    def _calculate_daily_pnl(self) -> float:
        """محاسبه PnL روزانه"""
        if len(self.equity_curve) < 2:
            return 0.0
        return self.equity_curve[-1] - self.equity_curve[-2]
        
    def _calculate_monthly_performance(self) -> Dict:
        """محاسبه عملکرد ماهانه"""
        monthly_data = {}
        
        for position in self.closed_positions:
            if position.exit_time:
                month_key = position.exit_time.strftime("%Y-%m")
                
                if month_key not in monthly_data:
                    monthly_data[month_key] = {'pnl': 0, 'trades': 0, 'wins': 0}
                    
                monthly_data[month_key]['pnl'] += position.realized_pnl
                monthly_data[month_key]['trades'] += 1
                
                if position.realized_pnl > 0:
                    monthly_data[month_key]['wins'] += 1
                    
        # محاسبه نرخ برد ماهانه
        for month in monthly_data:
            trades = monthly_data[month]['trades']
            monthly_data[month]['win_rate'] = (monthly_data[month]['wins'] / trades * 100) if trades > 0 else 0
            
        return monthly_data
        
    def _calculate_symbol_performance(self) -> Dict:
        """محاسبه عملکرد بر اساس نماد"""
        symbol_data = {}
        
        for position in self.closed_positions:
            symbol = position.symbol
            
            if symbol not in symbol_data:
                symbol_data[symbol] = {'pnl': 0, 'trades': 0, 'wins': 0}
                
            symbol_data[symbol]['pnl'] += position.realized_pnl
            symbol_data[symbol]['trades'] += 1
            
            if position.realized_pnl > 0:
                symbol_data[symbol]['wins'] += 1
                
        # محاسبه نرخ برد برای هر نماد
        for symbol in symbol_data:
            trades = symbol_data[symbol]['trades']
            symbol_data[symbol]['win_rate'] = (symbol_data[symbol]['wins'] / trades * 100) if trades > 0 else 0
            
        return symbol_data
        
    def _calculate_signal_performance(self) -> Dict:
        """محاسبه عملکرد بر اساس منبع سیگنال"""
        signal_data = {}
        
        for position in self.closed_positions:
            source = position.signal_source
            
            if source not in signal_data:
                signal_data[source] = {'pnl': 0, 'trades': 0, 'wins': 0}
                
            signal_data[source]['pnl'] += position.realized_pnl
            signal_data[source]['trades'] += 1
            
            if position.realized_pnl > 0:
                signal_data[source]['wins'] += 1
                
        # محاسبه نرخ برد برای هر منبع
        for source in signal_data:
            trades = signal_data[source]['trades']
            signal_data[source]['win_rate'] = (signal_data[source]['wins'] / trades * 100) if trades > 0 else 0
            
        return signal_data
        
    def _partial_close_position(self, position: Position, exit_price: float, 
                               quantity: float, reason: str):
        """بستن جزئی پوزیشن"""
        # کاهش حجم پوزیشن اصلی
        position.quantity -= quantity
        
        # محاسبه PnL جزئی
        if position.position_type == "LONG":
            partial_pnl = (exit_price - position.entry_price) * quantity
        else:
            partial_pnl = (position.entry_price - exit_price) * quantity
            
        # بروزرسانی سرمایه
        self.current_capital += partial_pnl
        
        logger.info(f"💰 بستن جزئی: {position.symbol} - مقدار: {quantity:.6f} - PnL: ${partial_pnl:,.2f}")
        
    def _risk_parity_optimization(self) -> List[Dict]:
        """بهینه‌سازی برابری ریسک"""
        recommendations = []
        
        total_risk = sum(pos.current_risk for pos in self.positions)
        target_risk_per_position = total_risk / len(self.positions)
        
        for position in self.positions:
            risk_deviation = (position.current_risk - target_risk_per_position) / target_risk_per_position
            
            if abs(risk_deviation) > 0.2:  # انحراف بیش از 20%
                action = "REDUCE" if risk_deviation > 0 else "INCREASE"
                recommendations.append({
                    'position_id': position.position_id,
                    'symbol': position.symbol,
                    'action': action,
                    'current_risk': position.current_risk,
                    'target_risk': target_risk_per_position,
                    'deviation_percent': risk_deviation * 100
                })
                
        return recommendations
        
    def _mean_variance_optimization(self) -> List[Dict]:
        """بهینه‌سازی میانگین-واریانس"""
        # پیاده‌سازی ساده
        recommendations = []
        
        if len(self.closed_positions) < 20:
            return recommendations
            
        # محاسبه بازده مورد انتظار برای هر نماد
        symbol_returns = {}
        for position in self.closed_positions:
            symbol = position.symbol
            if symbol not in symbol_returns:
                symbol_returns[symbol] = []
            symbol_returns[symbol].append(position.realized_pnl_percent / 100)
            
        # توصیه بر اساس بازده مورد انتظار
        for position in self.positions:
            symbol = position.symbol
            if symbol in symbol_returns and len(symbol_returns[symbol]) >= 5:
                expected_return = np.mean(symbol_returns[symbol])
                
                if expected_return > 0.05:  # بازده مثبت بیش از 5%
                    recommendations.append({
                        'position_id': position.position_id,
                        'symbol': symbol,
                        'action': 'INCREASE',
                        'expected_return': expected_return * 100,
                        'confidence': min(0.8, len(symbol_returns[symbol]) / 20)
                    })
                elif expected_return < -0.02:  # بازده منفی بیش از 2%
                    recommendations.append({
                        'position_id': position.position_id,
                        'symbol': symbol,
                        'action': 'REDUCE',
                        'expected_return': expected_return * 100,
                        'confidence': min(0.8, len(symbol_returns[symbol]) / 20)
                    })
                    
        return recommendations
        
    def _hierarchical_risk_parity(self) -> List[Dict]:
        """بهینه‌سازی برابری ریسک سلسله‌مراتبی"""
        # پیاده‌سازی ساده
        return self._risk_parity_optimization()
        
    def _calculate_improvement_potential(self, recommendations: List[Dict]) -> float:
        """محاسبه پتانسیل بهبود"""
        if not recommendations:
            return 0.0
            
        # تخمین بهبود بر اساس تعداد توصیه‌ها
        improvement = min(0.15, len(recommendations) * 0.03)  # حداکثر 15% بهبود
        return improvement * 100
        
    def _update_cache(self, market_data: Dict[str, pd.DataFrame]):
        """بروزرسانی کش"""
        current_time = datetime.now()
        
        # پاک کردن کش منقضی شده
        if hasattr(self, 'cache_last_update'):
            if current_time - self.cache_last_update > self.cache_expiry:
                self.correlation_cache.clear()
                self.volatility_cache.clear()
                
        self.cache_last_update = current_time
        
    def _record_trade_performance(self, position: Position):
        """ثبت عملکرد معامله"""
        performance_record = {
            'timestamp': datetime.now().isoformat(),
            'position_id': position.position_id,
            'symbol': position.symbol,
            'signal_source': position.signal_source,
            'wave_type': position.wave_type,
            'pnl': position.realized_pnl,
            'pnl_percent': position.realized_pnl_percent,
            'duration_hours': position.duration_hours,
            'confidence_score': position.confidence_score,
            'risk_score': position.risk_score
        }
        
        self.performance_history.append(performance_record)
        
        # ثبت در فایل JSON
        try:
            with open('trade_performance.json', 'a', encoding='utf-8') as f:
                json.dump(performance_record, f, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            logger.error(f"خطا در ثبت عملکرد: {e}")
            
    def export_data(self, format: str = 'json') -> str:
        """صادرات داده‌ها"""
        try:
            data = {
                'portfolio_summary': {
                    'initial_capital': self.initial_capital,
                    'current_capital': self.current_capital,
                    'total_pnl': self.current_capital - self.initial_capital,
                    'roi_percent': ((self.current_capital - self.initial_capital) / self.initial_capital) * 100
                },
                'positions': [
                    {
                        'position_id': pos.position_id,
                        'symbol': pos.symbol,
                        'quantity': pos.quantity,
                        'entry_price': pos.entry_price,
                        'current_price': pos.current_price,
                        'unrealized_pnl': pos.unrealized_pnl,
                        'unrealized_pnl_percent': pos.unrealized_pnl_percent
                    }
                    for pos in self.positions
                ],
                'closed_positions': [
                    {
                        'position_id': pos.position_id,
                        'symbol': pos.symbol,
                        'realized_pnl': pos.realized_pnl,
                        'realized_pnl_percent': pos.realized_pnl_percent,
                        'entry_time': pos.entry_time.isoformat(),
                        'exit_time': pos.exit_time.isoformat() if pos.exit_time else None,
                        'duration_hours': pos.duration_hours
                    }
                    for pos in self.closed_positions
                ],
                'performance_metrics': self.calculate_advanced_metrics().__dict__
            }
            
            filename = f"portfolio_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            
            if format == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            elif format == 'csv':
                # صادرات CSV برای معاملات بسته
                df = pd.DataFrame([
                    {
                        'Position ID': pos.position_id,
                        'Symbol': pos.symbol,
                        'Entry Price': pos.entry_price,
                        'Exit Price': pos.exit_price,
                        'Quantity': pos.quantity,
                        'PnL': pos.realized_pnl,
                        'PnL %': pos.realized_pnl_percent,
                        'Duration (hours)': pos.duration_hours,
                        'Entry Time': pos.entry_time,
                        'Exit Time': pos.exit_time
                    }
                    for pos in self.closed_positions
                ])
                df.to_csv(filename, index=False)
                
            logger.info(f"📁 داده‌ها در فایل {filename} صادر شد")
            return filename
            
        except Exception as e:
            logger.error(f"خطا در صادرات داده‌ها: {e}")
            return ""
            
    def get_real_time_status(self) -> Dict:
        """دریافت وضعیت real-time"""
        try:
            total_exposure = sum(pos.quantity * pos.current_price for pos in self.positions)
            unrealized_pnl = sum(pos.unrealized_pnl for pos in self.positions)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'capital': {
                    'total': self.current_capital + unrealized_pnl,
                    'available': self.current_capital - total_exposure,
                    'invested': total_exposure,
                    'unrealized_pnl': unrealized_pnl
                },
                'positions': {
                    'count': len(self.positions),
                    'total_value': total_exposure,
                    'exposure_percent': (total_exposure / self.current_capital * 100) if self.current_capital > 0 else 0
                },
                'risk': {
                    'portfolio_risk': self._calculate_portfolio_risk(),
                    'max_risk_reached': len(self.positions) >= self.max_positions,
                    'emergency_stop_triggered': False  # پیاده‌سازی شرایط اضطراری
                },
                'performance': {
                    'daily_pnl': self._calculate_daily_pnl(),
                    'total_roi': ((self.current_capital - self.initial_capital) / self.initial_capital) * 100,
                    'trades_today': len([p for p in self.closed_positions 
                                       if p.exit_time and p.exit_time.date() == datetime.now().date()])
                }
            }
            
        except Exception as e:
            logger.error(f"خطا در دریافت وضعیت real-time: {e}")
            return {}

    def __del__(self):
        """تمیزکاری هنگام حذف شئ"""
        try:
            if hasattr(self, 'db_connection') and self.db_connection:
                self.db_connection.close()
        except:
            pass