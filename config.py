# ================= فایل config.py =================

import json
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class APIConfig:
    """تنظیمات API صرافی"""
    api_key: str = ""
    secret_key: str = ""
    exchange: str = "lbank"
    testnet: bool = False

@dataclass
class AnalysisConfig:
    """تنظیمات تحلیل"""
    timeframe: str = "1h"
    symbol: str = "BTC/USDT"
    lookback_periods: int = 500
    auto_refresh: bool = True
    refresh_interval: int = 60  # ثانیه

class Config:
    """مدیریت تنظیمات برنامه"""
    
    CONFIG_FILE = "config.json"
    
    def __init__(self):
        self.api = APIConfig()
        self.analysis = AnalysisConfig()
        self.load_config()
        
    def load_config(self):
        """بارگذاری تنظیمات از فایل"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    
                # API Config
                if 'api' in data:
                    self.api.api_key = data['api'].get('api_key', '')
                    self.api.secret_key = data['api'].get('secret_key', '')
                    self.api.exchange = data['api'].get('exchange', 'lbank')
                    self.api.testnet = data['api'].get('testnet', False)
                    
                # Analysis Config
                if 'analysis' in data:
                    self.analysis.timeframe = data['analysis'].get('timeframe', '1h')
                    self.analysis.symbol = data['analysis'].get('symbol', 'BTC/USDT')
                    self.analysis.lookback_periods = data['analysis'].get('lookback_periods', 500)
                    self.analysis.auto_refresh = data['analysis'].get('auto_refresh', True)
                    self.analysis.refresh_interval = data['analysis'].get('refresh_interval', 60)
                    
            except Exception as e:
                print(f"خطا در بارگذاری تنظیمات: {e}")
                
    def save_config(self):
        """ذخیره تنظیمات در فایل"""
        data = {
            'api': {
                'api_key': self.api.api_key,
                'secret_key': self.api.secret_key,
                'exchange': self.api.exchange,
                'testnet': self.api.testnet
            },
            'analysis': {
                'timeframe': self.analysis.timeframe,
                'symbol': self.analysis.symbol,
                'lookback_periods': self.analysis.lookback_periods,
                'auto_refresh': self.analysis.auto_refresh,
                'refresh_interval': self.analysis.refresh_interval
            }
        }
        
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"خطا در ذخیره تنظیمات: {e}")