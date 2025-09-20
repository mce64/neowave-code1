import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import asyncio
import threading

class DataFetcher:
    """دریافت داده از صرافی LBank"""
    
    def __init__(self, api_key: str = "", secret_key: str = ""):
        self.api_key = api_key
        self.secret_key = secret_key
        self.exchange = None
        self.initialize_exchange()
        
    def initialize_exchange(self):
        """راه‌اندازی اتصال به صرافی"""
        try:
            self.exchange = ccxt.lbank({
                'apiKey': self.api_key,
                'secret': self.secret_key,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                }
            })
            
            # بررسی اتصال
            self.exchange.load_markets()
            print("✅ اتصال به صرافی LBank برقرار شد")
            
        except Exception as e:
            print(f"❌ خطا در اتصال به صرافی: {e}")
            
    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', 
                    limit: int = 500) -> pd.DataFrame:
        """دریافت داده‌های OHLCV"""
        try:
            if not self.exchange:
                self.initialize_exchange()
                
            # دریافت داده‌ها
            ohlcv = self.exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                limit=limit
            )
            
            # تبدیل به DataFrame
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            
            # تبدیل timestamp به datetime
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('datetime', inplace=True)
            
            # محاسبه فیلدهای اضافی
            df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
            df['hl2'] = (df['high'] + df['low']) / 2
            df['hlc3'] = (df['high'] + df['low'] + df['close']) / 3
            df['ohlc4'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
            
            return df
            
        except Exception as e:
            print(f"خطا در دریافت داده: {e}")
            return pd.DataFrame()
            
    def fetch_ticker(self, symbol: str) -> Dict:
        """دریافت اطلاعات لحظه‌ای"""
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as e:
            print(f"خطا در دریافت ticker: {e}")
            return {}
            
    def fetch_order_book(self, symbol: str, limit: int = 20) -> Dict:
        """دریافت دفتر سفارشات"""
        try:
            return self.exchange.fetch_order_book(symbol, limit)
        except Exception as e:
            print(f"خطا در دریافت order book: {e}")
            return {}
            
    def get_available_symbols(self) -> List[str]:
        """دریافت لیست جفت ارزهای موجود"""
        try:
            if not self.exchange:
                self.initialize_exchange()
            markets = self.exchange.load_markets()
            return list(markets.keys())
        except Exception as e:
            print(f"خطا در دریافت symbols: {e}")
            return []