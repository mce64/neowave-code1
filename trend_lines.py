"""خطوط روند پیشرفته"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional
from collections import deque

class TrendLineAnalyzer:
    """تحلیلگر خطوط روند نئوویو"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.trend_lines = []
        self.break_points = []
        
    def draw_0_2_trendline(self, waves: List[Dict]) -> Dict:
        """رسم خط روند 0-2 (مهم‌ترین خط در نئوویو)"""
        if len(waves) < 3:
            return None
            
        # نقطه شروع موج 1 و انتهای موج 2
        point_0 = waves[0]['start']
        point_2 = waves[1]['end']
        
        trendline = {
            'type': '0-2',
            'points': [point_0, point_2],
            'slope': (point_2[1] - point_0[1]) / (point_2[0] - point_0[0]),
            'significance': 'Critical',
            'rules': {
                'wave3_must_break': True,  # موج 3 باید این خط را بشکند
                'wave4_interaction': 'موج 4 ممکن است به این خط برسد',
                'post_pattern': 'شکست این خط تایید پایان الگو است'
            }
        }
        
        # بررسی شکست توسط موج 3
        if len(waves) >= 3:
            wave3_end = waves[2]['end']
            trendline['wave3_break'] = self._check_trendline_break(
                trendline, wave3_end
            )
            
        self.trend_lines.append(trendline)
        return trendline
        
    def draw_2_4_trendline(self, waves: List[Dict]) -> Dict:
        """رسم خط روند 2-4"""
        if len(waves) < 5:
            return None
            
        point_2 = waves[1]['end']
        point_4 = waves[3]['end']
        
        trendline = {
            'type': '2-4',
            'points': [point_2, point_4],
            'slope': (point_4[1] - point_2[1]) / (point_4[0] - point_2[0]),
            'significance': 'Important',
            'rules': {
                'wave5_target': 'موج 5 ممکن است به موازی این خط برسد',
                'channel_base': 'پایه کانال‌بندی الگو',
                'pattern_validation': 'عدم شکست = الگو معتبر'
            }
        }
        
        # محاسبه خط موازی از موج 3
        if len(waves) >= 3:
            wave3_end = waves[2]['end']
            trendline['parallel_from_3'] = {
                'slope': trendline['slope'],
                'intercept': wave3_end[1] - trendline['slope'] * wave3_end[0]
            }
            
        self.trend_lines.append(trendline)
        return trendline
        
    def draw_b_d_trendline(self, triangle_waves: List[Dict]) -> Dict:
        """رسم خط روند B-D برای مثلث‌ها"""
        if len(triangle_waves) < 4:
            return None
            
        point_b = triangle_waves[1]['end']
        point_d = triangle_waves[3]['end']
        
        trendline = {
            'type': 'B-D',
            'points': [point_b, point_d],
            'slope': (point_d[1] - point_b[1]) / (point_d[0] - point_b[0]),
            'significance': 'Triangle validation',
            'rules': {
                'e_wave_target': 'موج E معمولاً این خط را لمس می‌کند',
                'apex_calculation': 'برای محاسبه Apex استفاده می‌شود',
                'breakout_signal': 'شکست = خروج از مثلث'
            }
        }
        
        self.trend_lines.append(trendline)
        return trendline
        
    def find_touch_points(self, trendline: Dict, tolerance: float = 0.02) -> List[int]:
        """یافتن نقاط تماس با خط روند"""
        touches = []
        
        for i, row in self.data.iterrows():
            # محاسبه قیمت خط روند در این نقطه
            trendline_price = trendline['slope'] * i + \
                            (trendline['points'][0][1] - 
                             trendline['slope'] * trendline['points'][0][0])
                             
            # بررسی تماس
            if abs(row['high'] - trendline_price) / trendline_price < tolerance or \
               abs(row['low'] - trendline_price) / trendline_price < tolerance:
                touches.append(i)
                
        return touches
        
    def _check_trendline_break(self, trendline: Dict, 
                               point: Tuple, 
                               confirmation_percent: float = 0.03) -> bool:
        """بررسی شکست خط روند"""
        # محاسبه قیمت خط روند در نقطه مورد نظر
        trendline_price = trendline['slope'] * point[0] + \
                         (trendline['points'][0][1] - 
                          trendline['slope'] * trendline['points'][0][0])
                          
        # بررسی شکست با تایید
        if trendline['slope'] > 0:  # خط صعودی
            return point[1] > trendline_price * (1 + confirmation_percent)
        else:  # خط نزولی
            return point[1] < trendline_price * (1 - confirmation_percent)
            
    def calculate_thrust_measurement(self, triangle_trendlines: List[Dict]) -> Dict:
        """محاسبه Thrust (حرکت پس از شکست مثلث)"""
        if len(triangle_trendlines) < 2:
            return None
            
        # عریض‌ترین بخش مثلث
        max_width = 0
        for tl in triangle_trendlines:
            width = abs(tl['points'][0][1] - tl['points'][1][1])
            if width > max_width:
                max_width = width
                
        return {
            'conservative_target': max_width * 0.618,
            'normal_target': max_width * 1.000,
            'extended_target': max_width * 1.618,
            'measurement_base': max_width
        }
