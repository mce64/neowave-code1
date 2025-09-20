"""ویجت‌های نمودار پیشرفته"""

import pyqtgraph as pg
import numpy as np
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CandlestickChart(pg.PlotWidget):
    """نمودار کندل استیک پیشرفته"""
    
    def __init__(self):
        super().__init__()
        
        # تنظیمات نمودار
        self.setBackground('#1a1a1a')
        self.showGrid(x=True, y=True, alpha=0.3)
        self.setLabel('left', 'قیمت', units='$')
        self.setLabel('bottom', 'زمان')
        
        # آیتم‌های نمودار
        self.candlesticks = []
        self.pivot_points = []
        self.fibonacci_levels = []
        self.trend_lines = []
        self.channels = []
        self.wave_labels = []
        
        # رنگ‌ها
        self.colors = {
            'bullish': '#4CAF50',
            'bearish': '#f44336',
            'pivot_high': '#FF9800',
            'pivot_low': '#2196F3',
            'fibonacci': '#9C27B0',
            'support': '#4CAF50',
            'resistance': '#f44336',
            'channel': '#607D8B'
        }
        
    def update_data(self, data: pd.DataFrame):
        """بروزرسانی داده‌های نمودار"""
        self.clear()
        self.candlesticks = []
        
        if data is None or len(data) == 0:
            return
            
        for i, (idx, row) in enumerate(data.iterrows()):
            self.draw_candlestick(i, row)
            
        # تنظیم محدوده نمایش
        self.setXRange(0, len(data))
        y_min = data['low'].min() * 0.995
        y_max = data['high'].max() * 1.005
        self.setYRange(y_min, y_max)
        
    def draw_candlestick(self, x, row):
        """رسم یک کندل"""
        try:
            open_price = float(row['open'])
            high_price = float(row['high'])
            low_price = float(row['low'])
            close_price = float(row['close'])
            
            # تعیین رنگ
            if close_price >= open_price:
                color = self.colors['bullish']
            else:
                color = self.colors['bearish']
                
            # رسم سایه (wick)
            wick = pg.PlotDataItem(
                [x, x], [low_price, high_price],
                pen=pg.mkPen(color, width=1)
            )
            self.addItem(wick)
            
            # رسم بدنه (body)
            body_height = abs(close_price - open_price)
            body_y = min(open_price, close_price)
            
            if body_height > 0:
                body = pg.BarGraphItem(
                    x=[x], height=[body_height], y=[body_y],
                    width=0.6, brush=color, pen=pg.mkPen(color)
                )
                self.addItem(body)
            else:
                # خط افقی برای doji
                doji_line = pg.PlotDataItem(
                    [x-0.3, x+0.3], [close_price, close_price],
                    pen=pg.mkPen(color, width=2)
                )
                self.addItem(doji_line)
                
        except (ValueError, TypeError, KeyError) as e:
            print(f"خطا در رسم کندل {x}: {e}")
    
    def add_pivot_points(self, pivots):
        """اضافه کردن نقاط پیووت"""
        self.clear_pivot_points()
        
        for pivot in pivots:
            try:
                if hasattr(pivot, 'index') and hasattr(pivot, 'value') and hasattr(pivot, 'type'):
                    x = pivot.index
                    y = pivot.value
                    pivot_type = pivot.type
                elif isinstance(pivot, (list, tuple)) and len(pivot) >= 3:
                    x, y, pivot_type = pivot[0], pivot[1], pivot[2]
                else:
                    continue
                
                # تعیین رنگ بر اساس نوع پیووت
                if 'high' in str(pivot_type).lower() or 'peak' in str(pivot_type).lower():
                    color = self.colors['pivot_high']
                    symbol = 'v'  # مثلث رو به پایین
                else:
                    color = self.colors['pivot_low']
                    symbol = '^'  # مثلث رو به بالا
                
                # رسم نقطه پیووت
                scatter = pg.ScatterPlotItem(
                    [x], [y], 
                    size=12, 
                    brush=color,
                    symbol=symbol,
                    pen=pg.mkPen('white', width=1)
                )
                self.addItem(scatter)
                self.pivot_points.append(scatter)
                
                # اضافه کردن برچسب
                text = pg.TextItem(
                    f'P{len(self.pivot_points)}',
                    color=color,
                    anchor=(0.5, 0.5)
                )
                text.setPos(x, y)
                self.addItem(text)
                self.pivot_points.append(text)
                
            except Exception as e:
                print(f"خطا در رسم پیووت: {e}")
    
    def add_fibonacci_levels(self, high_price, low_price, levels=None):
        """اضافه کردن سطوح فیبوناچی"""
        self.clear_fibonacci_levels()
        
        if levels is None:
            levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
        
        price_range = high_price - low_price
        view_range = self.getViewBox().viewRange()[0]
        x_start = max(0, view_range[0])
        x_end = view_range[1]
        
        for level in levels:
            price = low_price + (price_range * level)
            
            # رسم خط افقی
            line = pg.PlotDataItem(
                [x_start, x_end], [price, price],
                pen=pg.mkPen(self.colors['fibonacci'], width=1, style=Qt.DashLine)
            )
            self.addItem(line)
            self.fibonacci_levels.append(line)
            
            # اضافه کردن برچسب
            text = pg.TextItem(
                f'Fib {level:.1%}: ${price:.2f}',
                color=self.colors['fibonacci'],
                anchor=(0, 0.5)
            )
            text.setPos(x_end - (x_end - x_start) * 0.1, price)
            self.addItem(text)
            self.fibonacci_levels.append(text)
    
    def add_support_resistance(self, support_level, resistance_level):
        """اضافه کردن خطوط حمایت و مقاومت"""
        view_range = self.getViewBox().viewRange()[0]
        x_start = max(0, view_range[0])
        x_end = view_range[1]
        
        # خط حمایت
        support_line = pg.PlotDataItem(
            [x_start, x_end], [support_level, support_level],
            pen=pg.mkPen(self.colors['support'], width=2)
        )
        self.addItem(support_line)
        
        # خط مقاومت
        resistance_line = pg.PlotDataItem(
            [x_start, x_end], [resistance_level, resistance_level],
            pen=pg.mkPen(self.colors['resistance'], width=2)
        )
        self.addItem(resistance_line)
        
        # برچسب‌ها
        support_text = pg.TextItem(
            f'Support: ${support_level:.2f}',
            color=self.colors['support'],
            anchor=(0, 0.5)
        )
        support_text.setPos(x_end - (x_end - x_start) * 0.15, support_level)
        self.addItem(support_text)
        
        resistance_text = pg.TextItem(
            f'Resistance: ${resistance_level:.2f}',
            color=self.colors['resistance'],
            anchor=(0, 0.5)
        )
        resistance_text.setPos(x_end - (x_end - x_start) * 0.15, resistance_level)
        self.addItem(resistance_text)
    
    def add_trend_line(self, x1, y1, x2, y2, color=None, label=None):
        """اضافه کردن خط روند"""
        if color is None:
            color = '#FFC107'
            
        line = pg.PlotDataItem(
            [x1, x2], [y1, y2],
            pen=pg.mkPen(color, width=2)
        )
        self.addItem(line)
        self.trend_lines.append(line)
        
        if label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            text = pg.TextItem(label, color=color, anchor=(0.5, 0.5))
            text.setPos(mid_x, mid_y)
            self.addItem(text)
            self.trend_lines.append(text)
    
    def add_channel(self, upper_points, lower_points):
        """اضافه کردن کانال قیمتی"""
        if len(upper_points) < 2 or len(lower_points) < 2:
            return
            
        # خط بالایی کانال
        upper_x = [p[0] for p in upper_points]
        upper_y = [p[1] for p in upper_points]
        upper_line = pg.PlotDataItem(
            upper_x, upper_y,
            pen=pg.mkPen(self.colors['channel'], width=2, style=Qt.DashLine)
        )
        self.addItem(upper_line)
        self.channels.append(upper_line)
        
        # خط پایینی کانال
        lower_x = [p[0] for p in lower_points]
        lower_y = [p[1] for p in lower_points]
        lower_line = pg.PlotDataItem(
            lower_x, lower_y,
            pen=pg.mkPen(self.colors['channel'], width=2, style=Qt.DashLine)
        )
        self.addItem(lower_line)
        self.channels.append(lower_line)
        
        # پر کردن فضای بین خطوط
        if len(upper_points) == len(lower_points):
            x_coords = upper_x + lower_x[::-1]
            y_coords = upper_y + lower_y[::-1]
            
            fill = pg.FillBetweenItem(
                pg.PlotDataItem(upper_x, upper_y),
                pg.PlotDataItem(lower_x, lower_y),
                brush=pg.mkBrush(color=self.colors['channel'], alpha=30)
            )
            self.addItem(fill)
            self.channels.append(fill)
    
    def add_wave_count(self, wave_points, wave_labels):
        """اضافه کردن شماره‌گذاری امواج"""
        self.clear_wave_labels()
        
        for i, (point, label) in enumerate(zip(wave_points, wave_labels)):
            if len(point) >= 2:
                x, y = point[0], point[1]
                
                # رسم نقطه موج
                scatter = pg.ScatterPlotItem(
                    [x], [y], 
                    size=15, 
                    brush='yellow',
                    pen=pg.mkPen('black', width=2)
                )
                self.addItem(scatter)
                self.wave_labels.append(scatter)
                
                # اضافه کردن برچسب موج
                text = pg.TextItem(
                    str(label),
                    color='black',
                    anchor=(0.5, 0.5)
                )
                text.setPos(x, y)
                self.addItem(text)
                self.wave_labels.append(text)
    
    def clear_pivot_points(self):
        """پاک کردن نقاط پیووت"""
        for item in self.pivot_points:
            self.removeItem(item)
        self.pivot_points.clear()
    
    def clear_fibonacci_levels(self):
        """پاک کردن سطوح فیبوناچی"""
        for item in self.fibonacci_levels:
            self.removeItem(item)
        self.fibonacci_levels.clear()
    
    def clear_trend_lines(self):
        """پاک کردن خطوط روند"""
        for item in self.trend_lines:
            self.removeItem(item)
        self.trend_lines.clear()
    
    def clear_channels(self):
        """پاک کردن کانال‌ها"""
        for item in self.channels:
            self.removeItem(item)
        self.channels.clear()
    
    def clear_wave_labels(self):
        """پاک کردن برچسب‌های امواج"""
        for item in self.wave_labels:
            self.removeItem(item)
        self.wave_labels.clear()
    
    def clear_all_analysis(self):
        """پاک کردن تمام تحلیل‌ها"""
        self.clear_pivot_points()
        self.clear_fibonacci_levels()
        self.clear_trend_lines()
        self.clear_channels()
        self.clear_wave_labels()

class WaveCountChart(pg.PlotWidget):
    """نمودار موج شماری"""
    
    def __init__(self):
        super().__init__()
        self.setBackground('#1a1a1a')
        self.showGrid(x=True, y=True, alpha=0.3)
        self.setLabel('left', 'قیمت', units='$')
        self.setLabel('bottom', 'زمان')
        
        self.wave_lines = []
        self.wave_labels = []
        
    def update_wave_analysis(self, data, waves):
        """بروزرسانی تحلیل موجی"""
        self.clear()
        self.wave_lines.clear()
        self.wave_labels.clear()
        
        if data is None or len(data) == 0:
            return
        
        # رسم قیمت اصلی
        prices = data['close'].values
        x_data = list(range(len(prices)))
        price_line = pg.PlotDataItem(
            x_data, prices,
            pen=pg.mkPen('white', width=1)
        )
        self.addItem(price_line)
        
        # رسم امواج
        if waves:
            self.draw_waves(waves)
    
    def draw_waves(self, waves):
        """رسم امواج"""
        colors = ['red', 'green', 'blue', 'yellow', 'magenta']
        
        for i, wave in enumerate(waves[:5]):  # حداکثر 5 موج
            color = colors[i % len(colors)]
            
            # استخراج نقاط موج
            if hasattr(wave, 'waves') and wave.waves:
                points = []
                for sub_wave in wave.waves:
                    if hasattr(sub_wave, 'start_index') and hasattr(sub_wave, 'start_price'):
                        points.append((sub_wave.start_index, sub_wave.start_price))
                    if hasattr(sub_wave, 'end_index') and hasattr(sub_wave, 'end_price'):
                        points.append((sub_wave.end_index, sub_wave.end_price))
                
                if len(points) >= 2:
                    x_coords = [p[0] for p in points]
                    y_coords = [p[1] for p in points]
                    
                    wave_line = pg.PlotDataItem(
                        x_coords, y_coords,
                        pen=pg.mkPen(color, width=3)
                    )
                    self.addItem(wave_line)
                    self.wave_lines.append(wave_line)
                    
                    # اضافه کردن برچسب
                    mid_x = sum(x_coords) / len(x_coords)
                    mid_y = sum(y_coords) / len(y_coords)
                    
                    wave_type = getattr(wave, 'wave_type', f'Wave {i+1}')
                    if hasattr(wave_type, 'value'):
                        wave_type = wave_type.value
                    
                    text = pg.TextItem(
                        str(wave_type),
                        color=color,
                        anchor=(0.5, 0.5)
                    )
                    text.setPos(mid_x, mid_y)
                    self.addItem(text)
                    self.wave_labels.append(text)

class RatioChart(pg.PlotWidget):
    """نمودار نسبت‌های فیبوناچی"""
    
    def __init__(self):
        super().__init__()
        self.setBackground('#1a1a1a')
        self.showGrid(x=True, y=True, alpha=0.3)
        self.setLabel('left', 'نسبت فیبوناچی')
        self.setLabel('bottom', 'زمان')
        
        self.ratio_lines = []
        
    def update_ratio_analysis(self, ratios_data):
        """بروزرسانی تحلیل نسبت‌ها"""
        self.clear()
        self.ratio_lines.clear()
        
        if not ratios_data:
            return
        
        # نسبت‌های فیبوناچی استاندارد
        fib_levels = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618]
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown']
        
        # رسم خطوط مرجع
        for i, level in enumerate(fib_levels):
            color = colors[i % len(colors)]
            line = pg.InfiniteLine(
                pos=level,
                angle=0,
                pen=pg.mkPen(color, width=1, style=Qt.DashLine),
                label=f'Fib {level}'
            )
            self.addItem(line)
            self.ratio_lines.append(line)
        
        # رسم نسبت‌های محاسبه شده
        if isinstance(ratios_data, dict):
            x_data = []
            y_data = []
            
            for i, (name, ratio_result) in enumerate(ratios_data.items()):
                if hasattr(ratio_result, 'target_ratio'):
                    x_data.append(i)
                    y_data.append(ratio_result.target_ratio)
            
            if x_data and y_data:
                scatter = pg.ScatterPlotItem(
                    x_data, y_data,
                    size=10,
                    brush='white',
                    pen=pg.mkPen('black', width=1)
                )
                self.addItem(scatter)

class VolumeChart(pg.PlotWidget):
    """نمودار حجم"""
    
    def __init__(self):
        super().__init__()
        self.setBackground('#1a1a1a')
        self.showGrid(x=True, y=True, alpha=0.3)
        self.setLabel('left', 'حجم')
        self.setLabel('bottom', 'زمان')
        
        self.volume_bars = []
        
    def update_volume_data(self, data):
        """بروزرسانی داده‌های حجم"""
        self.clear()
        self.volume_bars.clear()
        
        if data is None or len(data) == 0 or 'volume' not in data.columns:
            return
        
        volumes = data['volume'].values
        x_data = list(range(len(volumes)))
        
        # تعیین رنگ بر اساس تغییرات قیمت
        colors = []
        for i in range(len(data)):
            if i == 0:
                colors.append('#888888')
            else:
                if data['close'].iloc[i] >= data['close'].iloc[i-1]:
                    colors.append('#4CAF50')  # سبز برای صعود
                else:
                    colors.append('#f44336')  # قرمز برای نزول
        
        # رسم نمودار میله‌ای حجم
        volume_bars = pg.BarGraphItem(
            x=x_data,
            height=volumes,
            width=0.8,
            brushes=colors
        )
        self.addItem(volume_bars)
        self.volume_bars.append(volume_bars)
        
        # اضافه کردن خط میانگین متحرک حجم
        if len(volumes) > 20:
            ma_volume = pd.Series(volumes).rolling(window=20).mean().values
            ma_line = pg.PlotDataItem(
                x_data, ma_volume,
                pen=pg.mkPen('yellow', width=2)
            )
            self.addItem(ma_line)
            self.volume_bars.append(ma_line)
    
    def add_volume_profile(self, data, levels=20):
        """اضافه کردن پروفایل حجم"""
        if data is None or len(data) == 0:
            return
        
        # محاسبه محدوده قیمت
        price_min = data['low'].min()
        price_max = data['high'].max()
        price_step = (price_max - price_min) / levels
        
        # محاسبه حجم در هر سطح قیمتی
        volume_profile = {}
        
        for i, row in data.iterrows():
            # تعیین سطح قیمتی برای این کندل
            avg_price = (row['high'] + row['low'] + row['close']) / 3
            level = int((avg_price - price_min) / price_step)
            level = min(level, levels - 1)  # محدود کردن به محدوده
            
            level_price = price_min + (level * price_step)
            
            if level_price not in volume_profile:
                volume_profile[level_price] = 0
            volume_profile[level_price] += row['volume']
        
        # رسم پروفایل حجم به صورت نمودار افقی
        if volume_profile:
            prices = list(volume_profile.keys())
            volumes = list(volume_profile.values())
            max_volume = max(volumes)
            
            # نرمال‌سازی حجم‌ها برای نمایش
            normalized_volumes = [v / max_volume * 50 for v in volumes]  # حداکثر 50 واحد عرض
            
            for price, volume in zip(prices, normalized_volumes):
                bar = pg.BarGraphItem(
                    x=[len(data) + 10],  # کنار نمودار اصلی
                    y=[price],
                    height=[price_step * 0.8],
                    width=[volume],
                    brush=pg.mkBrush(100, 150, 200, 100)
                )
                self.addItem(bar)