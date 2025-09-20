"""الگوهای مثلثی پیشرفته"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional
from enum import Enum

class TriangleType(Enum):
    """انواع مثلث"""
    CONTRACTING = "انقباضی"
    EXPANDING = "انبساطی"
    NEUTRAL = "خنثی"
    RUNNING = "جاری"
    BARRIER = "سدی"

class TriangleVariation(Enum):
    """تنوعات مثلث"""
    LIMITING = "محدود"
    NON_LIMITING = "نامحدود"
    HORIZONTAL = "افقی"
    IRREGULAR = "نامنظم"
    RUNNING = "جاری"
    COUNTER = "کانتر"
    REVERSE_ALTERNATION = "تناوب معکوس"

class TriangleAnalyzer:
    """تحلیلگر الگوهای مثلثی"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.triangles = []
        
    def identify_triangle(self, pivots: List[Tuple]) -> Optional[Dict]:
        """شناسایی الگوی مثلث"""
        if len(pivots) < 6:  # حداقل 6 نقطه برای مثلث
            return None
            
        triangle_type = self._determine_triangle_type(pivots)
        variation = self._determine_variation(pivots, triangle_type)
        
        triangle = {
            'type': triangle_type,
            'variation': variation,
            'pivots': pivots,
            'trend_lines': self._calculate_trend_lines(pivots),
            'apex': self._calculate_apex(pivots),
            'breakout_targets': self._calculate_breakout_targets(pivots),
            'is_valid': self._validate_triangle(pivots, triangle_type)
        }
        
        if triangle['is_valid']:
            self.triangles.append(triangle)
            return triangle
            
        return None
        
    def _determine_triangle_type(self, pivots: List[Tuple]) -> TriangleType:
        """تعیین نوع مثلث"""
        # محاسبه دامنه موج‌ها
        ranges = []
        for i in range(len(pivots) - 1):
            ranges.append(abs(pivots[i+1][1] - pivots[i][1]))
            
        # بررسی روند دامنه‌ها
        if all(ranges[i] > ranges[i+1] for i in range(len(ranges)-1)):
            return TriangleType.CONTRACTING
        elif all(ranges[i] < ranges[i+1] for i in range(len(ranges)-1)):
            return TriangleType.EXPANDING
        else:
            # بررسی نسبت اول و آخر
            if ranges[0] > ranges[-1]:
                return TriangleType.CONTRACTING
            elif ranges[0] < ranges[-1]:
                return TriangleType.EXPANDING
            else:
                return TriangleType.NEUTRAL
                
    def _determine_variation(self, pivots: List[Tuple], 
                           triangle_type: TriangleType) -> TriangleVariation:
        """تعیین تنوع مثلث"""
        # محاسبه موقعیت نسبی قله‌ها و دره‌ها
        highs = [p[1] for p in pivots if p[2] == 'HIGH']
        lows = [p[1] for p in pivots if p[2] == 'LOW']
        
        # بررسی افقی بودن
        high_range = max(highs) - min(highs)
        low_range = max(lows) - min(lows)
        
        if high_range < low_range * 0.1:  # یک خط تقریباً افقی
            return TriangleVariation.HORIZONTAL
            
        # بررسی نامنظم بودن
        if triangle_type == TriangleType.CONTRACTING:
            if highs[0] < highs[1]:  # B بالاتر از شروع
                return TriangleVariation.IRREGULAR
                
        # بررسی Running
        if pivots[-1][1] > pivots[0][1] * 1.1:  # انتها بالاتر از شروع
            return TriangleVariation.RUNNING
            
        return TriangleVariation.LIMITING
        
    def _calculate_trend_lines(self, pivots: List[Tuple]) -> Dict:
        """محاسبه خطوط روند مثلث"""
        highs = [(p[0], p[1]) for p in pivots if p[2] == 'HIGH']
        lows = [(p[0], p[1]) for p in pivots if p[2] == 'LOW']
        
        # خط روند بالایی
        upper_slope, upper_intercept = np.polyfit(
            [h[0] for h in highs],
            [h[1] for h in highs],
            1
        )
        
        # خط روند پایینی
        lower_slope, lower_intercept = np.polyfit(
            [l[0] for l in lows],
            [l[1] for l in lows],
            1
        )
        
        return {
            'upper': {
                'slope': upper_slope,
                'intercept': upper_intercept,
                'points': highs
            },
            'lower': {
                'slope': lower_slope,
                'intercept': lower_intercept,
                'points': lows
            }
        }
        
    def _calculate_apex(self, pivots: List[Tuple]) -> Dict:
        """محاسبه نقطه همگرایی (Apex) مثلث"""
        trend_lines = self._calculate_trend_lines(pivots)
        
        # حل معادله دو خط برای یافتن نقطه تقاطع
        upper = trend_lines['upper']
        lower = trend_lines['lower']
        
        # اگر خطوط موازی باشند
        if abs(upper['slope'] - lower['slope']) < 0.0001:
            return None
            
        # نقطه تقاطع
        x_apex = (lower['intercept'] - upper['intercept']) / \
                 (upper['slope'] - lower['slope'])
        y_apex = upper['slope'] * x_apex + upper['intercept']
        
        return {
            'x': x_apex,
            'y': y_apex,
            'distance_from_start': x_apex - pivots[0][0]
        }
        
    def _calculate_breakout_targets(self, pivots: List[Tuple]) -> Dict:
        """محاسبه اهداف شکست مثلث"""
        # اندازه‌گیری بزرگترین موج
        max_range = 0
        for i in range(len(pivots) - 1):
            range_val = abs(pivots[i+1][1] - pivots[i][1])
            if range_val > max_range:
                max_range = range_val
                
        # اهداف بر اساس اندازه مثلث
        targets = {
            'conservative': max_range * 0.618,
            'normal': max_range * 1.0,
            'aggressive': max_range * 1.618
        }
        
        return targets
        
    def _validate_triangle(self, pivots: List[Tuple], 
                         triangle_type: TriangleType) -> bool:
        """اعتبارسنجی مثلث"""
        # حداقل 5 موج (A-B-C-D-E)
        if len(pivots) < 6:
            return False
            
        # بررسی تناوب
        for i in range(len(pivots) - 1):
            if pivots[i][2] == pivots[i+1][2]:
                return False
                
        # در مثلث انقباضی، هر موج باید از موج قبلی کوتاه‌تر باشد
        if triangle_type == TriangleType.CONTRACTING:
            ranges = []
            for i in range(0, len(pivots) - 1, 2):
                if i + 2 < len(pivots):
                    ranges.append(abs(pivots[i+2][1] - pivots[i][1]))
                    
            for i in range(len(ranges) - 1):
                if ranges[i] <= ranges[i+1]:
                    return False
                    
        return True
        
    def calculate_post_pattern_confirmation(self, triangle: Dict, 
                                           current_price: float) -> Dict:
        """محاسبه تایید پسا الگوی مثلث"""
        apex = triangle['apex']
        targets = triangle['breakout_targets']
        
        # تعیین جهت شکست
        last_pivot = triangle['pivots'][-1]
        breakout_direction = 'up' if current_price > last_pivot[1] else 'down'
        
        # محاسبه میزان حرکت
        move_size = abs(current_price - last_pivot[1])
        
        confirmation = {
            'breakout_direction': breakout_direction,
            'move_size': move_size,
            'target_reached': {
                'conservative': move_size >= targets['conservative'],
                'normal': move_size >= targets['normal'],
                'aggressive': move_size >= targets['aggressive']
            },
            'time_from_apex': None  # محاسبه فاصله زمانی از apex
        }
        
        return confirmation