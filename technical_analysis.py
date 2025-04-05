import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

class TechnicalAnalysis:
    def __init__(self, data):
        self.data = data

    def moving_average(self, window):
        """Calculate the moving average with the specified window size."""
        return self.data['close'].rolling(window=window).mean()

    def rsi(self, window=14):
        """Calculate the Relative Strength Index (RSI)."""
        delta = self.data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def macd(self, short_window=12, long_window=26, signal_window=9):
        """Calculate the MACD and Signal Line."""
        short_ema = self.data['close'].ewm(span=short_window, adjust=False).mean()
        long_ema = self.data['close'].ewm(span=long_window, adjust=False).mean()
        macd = short_ema - long_ema
        signal = macd.ewm(span=signal_window, adjust=False).mean()
        return macd, signal

    def detect_engulfing_patterns(self):
        """Detect bullish and bearish engulfing patterns."""
        patterns = []
        for i in range(1, len(self.data)):
            prev_open = self.data['open'].iloc[i - 1]
            prev_close = self.data['close'].iloc[i - 1]
            curr_open = self.data['open'].iloc[i]
            curr_close = self.data['close'].iloc[i]

            # Bullish Engulfing
            if prev_close < prev_open and curr_close > curr_open and curr_close > prev_open and curr_open < prev_close:
                patterns.append((self.data.index[i], 'Bullish'))

            # Bearish Engulfing
            elif prev_close > prev_open and curr_close < curr_open and curr_close < prev_open and curr_open > prev_close:
                patterns.append((self.data.index[i], 'Bearish'))

        return patterns

    def calculate_support_resistance(self, order=5, df=None):
        """Calculate support and resistance levels using local minima and maxima."""
        if df is None:
            df = self.data
        df['Support'] = df['close'][argrelextrema(df['close'].values, np.less_equal, order=order)[0]]
        df['Resistance'] = df['close'][argrelextrema(df['close'].values, np.greater_equal, order=order)[0]]
        return df['Support'], df['Resistance']

    def bollinger_bands(self, window=20, num_std=2):
        rolling_mean = self.data['close'].rolling(window=window).mean()
        rolling_std = self.data['close'].rolling(window=window).std()
        upper_band = rolling_mean + (rolling_std * num_std)
        lower_band = rolling_mean - (rolling_std * num_std)
        return rolling_mean, upper_band, lower_band

    def detect_three_white_soldiers(self):
        patterns = []
        for i in range(2, len(self.data)):
            if (self.data['close'][i] > self.data['open'][i] and
                self.data['close'][i-1] > self.data['open'][i-1] and
                self.data['close'][i-2] > self.data['open'][i-2] and
                self.data['close'][i] > self.data['close'][i-1] > self.data['close'][i-2] and
                self.data['open'][i] < self.data['close'][i-1] and
                self.data['open'][i-1] < self.data['close'][i-2]):
                patterns.append((self.data.index[i], 'Three White Soldiers'))
        return patterns

    def calculate_strong_support_resistance(self, order=5, touch_threshold=3, merge_threshold=0.01):
        support, resistance = self.calculate_support_resistance(order=order)
        
        # Count touches
        support_touches = self.count_touches(support, self.data['close'])
        resistance_touches = self.count_touches(resistance, self.data['close'])
        
        # Filter strong levels
        strong_support = [level for level, count in support_touches.items() if count >= touch_threshold]
        strong_resistance = [level for level, count in resistance_touches.items() if count >= touch_threshold]
        
        # Merge nearby levels
        def merge_levels(levels):
            levels.sort()
            merged = []
            current = levels[0]
            for level in levels[1:]:
                if abs(level - current) / current <= merge_threshold:
                    current = (current + level) / 2
                else:
                    merged.append(current)
                    current = level
            merged.append(current)
            return merged
        
        strong_support = merge_levels(strong_support)
        strong_resistance = merge_levels(strong_resistance)
        
        return strong_support, strong_resistance

    def count_touches(self, levels, prices):
        touch_counts = {}
        for level in levels:
            touch_counts[level] = ((prices >= level * 0.99) & (prices <= level * 1.01)).sum()
        return touch_counts

    def detect_bullish_harami(self):
        """Detect Bullish Harami patterns."""
        patterns = []
        for i in range(1, len(self.data)):
            prev_open = self.data['open'].iloc[i - 1]
            prev_close = self.data['close'].iloc[i - 1]
            curr_open = self.data['open'].iloc[i]
            curr_close = self.data['close'].iloc[i]

            # Bullish Harami: Previous candle is bearish, current candle is bullish and within the previous candle's body
            if prev_close < prev_open and curr_close > curr_open and curr_open > prev_close and curr_close < prev_open:
                patterns.append((self.data.index[i], 'Bullish Harami'))

        return patterns

    def detect_bearish_harami(self):
        """Detect Bearish Harami patterns."""
        patterns = []
        for i in range(1, len(self.data)):
            prev_open = self.data['open'].iloc[i - 1]
            prev_close = self.data['close'].iloc[i - 1]
            curr_open = self.data['open'].iloc[i]
            curr_close = self.data['close'].iloc[i]

            # Bearish Harami: Previous candle is bullish, current candle is bearish and within the previous candle's body
            if prev_close > prev_open and curr_close < curr_open and curr_open < prev_close and curr_close > prev_open:
                patterns.append((self.data.index[i], 'Bearish Harami'))

        return patterns

    def detect_harami_cross(self):
        """Detect Harami Cross patterns."""
        patterns = []
        for i in range(1, len(self.data)):
            prev_open = self.data['open'].iloc[i - 1]
            prev_close = self.data['close'].iloc[i - 1]
            curr_open = self.data['open'].iloc[i]
            curr_close = self.data['close'].iloc[i]
            curr_high = self.data['high'].iloc[i]
            curr_low = self.data['low'].iloc[i]

            # Check if the current candle is a Doji
            is_doji = abs(curr_open - curr_close) <= (curr_high - curr_low) * 0.1

            # Bullish Harami Cross: Previous candle is bearish, current candle is a Doji within the previous candle's body
            if prev_close < prev_open and is_doji and curr_high < prev_open and curr_low > prev_close:
                patterns.append((self.data.index[i], 'Bullish Harami Cross'))

            # Bearish Harami Cross: Previous candle is bullish, current candle is a Doji within the previous candle's body
            elif prev_close > prev_open and is_doji and curr_high < prev_close and curr_low > prev_open:
                patterns.append((self.data.index[i], 'Bearish Harami Cross'))

        return patterns

    def detect_hammer(self):
        """Detect Hammer patterns."""
        patterns = []
        for i in range(len(self.data)):
            open_price = self.data['open'].iloc[i]
            close_price = self.data['close'].iloc[i]
            high_price = self.data['high'].iloc[i]
            low_price = self.data['low'].iloc[i]

            # Calculate the body and shadows
            body = abs(close_price - open_price)
            lower_shadow = open_price - low_price if close_price > open_price else close_price - low_price
            upper_shadow = high_price - close_price if close_price > open_price else high_price - open_price

            # Hammer pattern conditions
            if lower_shadow >= 2 * body and upper_shadow <= 0.1 * body:
                patterns.append((self.data.index[i], 'Hammer'))

        return patterns

    def detect_piercing(self):
        """Detect Piercing patterns."""
        patterns = []
        for i in range(1, len(self.data)):
            prev_open = self.data['open'].iloc[i - 1]
            prev_close = self.data['close'].iloc[i - 1]
            curr_open = self.data['open'].iloc[i]
            curr_close = self.data['close'].iloc[i]

            # Piercing pattern conditions
            if prev_close < prev_open and curr_open < prev_close and curr_close > prev_open and curr_close > (prev_open + prev_close) / 2:
                patterns.append((self.data.index[i], 'Piercing'))

        return patterns

    def detect_morning_star(self):
        """Detect Morning Star patterns."""
        patterns = []
        for i in range(2, len(self.data)):
            first_open = self.data['open'].iloc[i - 2]
            first_close = self.data['close'].iloc[i - 2]
            second_open = self.data['open'].iloc[i - 1]
            second_close = self.data['close'].iloc[i - 1]
            third_open = self.data['open'].iloc[i]
            third_close = self.data['close'].iloc[i]

            # Morning Star pattern conditions
            if (first_close < first_open and  # First candle is bearish
                second_close < second_open and  # Second candle is bearish or a doji
                third_close > third_open and  # Third candle is bullish
                third_close > (first_open + first_close) / 2 and  # Third closes well into the first candle
                second_open < first_close and  # Second candle gaps down
                third_open > second_close):  # Third candle gaps up
                patterns.append((self.data.index[i], 'Morning Star'))

        return patterns

    def detect_hanging_man(self):
        """Detect Hanging Man patterns."""
        patterns = []
        for i in range(len(self.data)):
            open_price = self.data['open'].iloc[i]
            close_price = self.data['close'].iloc[i]
            high_price = self.data['high'].iloc[i]
            low_price = self.data['low'].iloc[i]

            # Calculate the body and shadows
            body = abs(close_price - open_price)
            lower_shadow = open_price - low_price if close_price > open_price else close_price - low_price
            upper_shadow = high_price - close_price if close_price > open_price else high_price - open_price

            # Hanging Man pattern conditions
            if lower_shadow >= 2 * body and upper_shadow <= 0.1 * body:
                # Ensure it occurs at the top of an uptrend
                if i > 0 and self.data['close'].iloc[i - 1] < open_price:
                    patterns.append((self.data.index[i], 'Hanging Man'))

        return patterns

    def detect_shooting_star(self):
        """Detect Shooting Star patterns."""
        patterns = []
        for i in range(len(self.data)):
            open_price = self.data['open'].iloc[i]
            close_price = self.data['close'].iloc[i]
            high_price = self.data['high'].iloc[i]
            low_price = self.data['low'].iloc[i]

            # Calculate the body and shadows
            body = abs(close_price - open_price)
            upper_shadow = high_price - max(open_price, close_price)
            lower_shadow = min(open_price, close_price) - low_price

            # Shooting Star pattern conditions
            if upper_shadow >= 2 * body and lower_shadow <= 0.1 * body:
                # Ensure it occurs at the top of an uptrend
                if i > 0 and self.data['close'].iloc[i - 1] < open_price:
                    patterns.append((self.data.index[i], 'Shooting Star'))

        return patterns

    def detect_evening_star(self):
        """Detect Evening Star patterns."""
        patterns = []
        for i in range(2, len(self.data)):
            first_open = self.data['open'].iloc[i - 2]
            first_close = self.data['close'].iloc[i - 2]
            second_open = self.data['open'].iloc[i - 1]
            second_close = self.data['close'].iloc[i - 1]
            third_open = self.data['open'].iloc[i]
            third_close = self.data['close'].iloc[i]

            # Evening Star pattern conditions
            if (first_close > first_open and  # First candle is bullish
                second_close > second_open and  # Second candle is bullish or a doji
                third_close < third_open and  # Third candle is bearish
                third_close < (first_open + first_close) / 2 and  # Third closes well into the first candle
                second_open > first_close and  # Second candle gaps up
                third_open < second_close):  # Third candle gaps down
                patterns.append((self.data.index[i], 'Evening Star'))

        return patterns

    def detect_three_black_crows(self):
        """Detect Three Black Crows patterns."""
        patterns = []
        for i in range(2, len(self.data)):
            if (self.data['close'][i] < self.data['open'][i] and
                self.data['close'][i-1] < self.data['open'][i-1] and
                self.data['close'][i-2] < self.data['open'][i-2] and
                self.data['close'][i] < self.data['close'][i-1] < self.data['close'][i-2] and
                self.data['open'][i] > self.data['close'][i-1] and
                self.data['open'][i-1] > self.data['close'][i-2]):
                patterns.append((self.data.index[i], 'Three Black Crows'))
        return patterns

    def detect_dark_cloud_cover(self):
        """Detect Dark Cloud Cover patterns."""
        patterns = []
        for i in range(1, len(self.data)):
            prev_open = self.data['open'].iloc[i - 1]
            prev_close = self.data['close'].iloc[i - 1]
            curr_open = self.data['open'].iloc[i]
            curr_close = self.data['close'].iloc[i]

            # Dark Cloud Cover pattern conditions
            if (prev_close > prev_open and  # First candle is bullish
                curr_open > prev_close and  # Second candle opens above the first candle's close
                curr_close < prev_close and  # Second candle closes below the first candle's close
                curr_close < (prev_open + prev_close) / 2):  # Second candle closes below the midpoint of the first candle
                patterns.append((self.data.index[i], 'Dark Cloud Cover'))

        return patterns

    def detect_doji_star(self):
        """Detect Doji Star patterns."""
        patterns = []
        for i in range(1, len(self.data)):
            open_price = self.data['open'].iloc[i]
            close_price = self.data['close'].iloc[i]
            prev_close = self.data['close'].iloc[i - 1]

            # Doji Star pattern conditions
            if abs(open_price - close_price) <= 0.1 * (self.data['high'].iloc[i] - self.data['low'].iloc[i]) and \
               abs(prev_close - open_price) > 0.5 * (self.data['high'].iloc[i - 1] - self.data['low'].iloc[i - 1]):
                patterns.append((self.data.index[i], 'Doji Star'))

        return patterns

    def detect_long_legged_doji(self):
        """Detect Long-Legged Doji patterns."""
        patterns = []
        for i in range(len(self.data)):
            open_price = self.data['open'].iloc[i]
            close_price = self.data['close'].iloc[i]
            high_price = self.data['high'].iloc[i]
            low_price = self.data['low'].iloc[i]

            # Long-Legged Doji pattern conditions
            if abs(open_price - close_price) <= 0.1 * (high_price - low_price) and \
               (high_price - low_price) > 2 * abs(open_price - close_price):
                patterns.append((self.data.index[i], 'Long-Legged Doji'))

        return patterns

    def detect_dragonfly_doji(self):
        """Detect Dragonfly Doji patterns."""
        patterns = []
        for i in range(len(self.data)):
            open_price = self.data['open'].iloc[i]
            close_price = self.data['close'].iloc[i]
            high_price = self.data['high'].iloc[i]
            low_price = self.data['low'].iloc[i]

            # Dragonfly Doji pattern conditions
            if abs(open_price - close_price) <= 0.1 * (high_price - low_price) and \
               (high_price - max(open_price, close_price)) <= 0.1 * (high_price - low_price) and \
               (min(open_price, close_price) - low_price) > 2 * abs(open_price - close_price):
                patterns.append((self.data.index[i], 'Dragonfly Doji'))

        return patterns

    def detect_gravestone_doji(self):
        """Detect Gravestone Doji patterns."""
        patterns = []
        for i in range(len(self.data)):
            open_price = self.data['open'].iloc[i]
            close_price = self.data['close'].iloc[i]
            high_price = self.data['high'].iloc[i]
            low_price = self.data['low'].iloc[i]

            # Gravestone Doji pattern conditions
            if abs(open_price - close_price) <= 0.1 * (high_price - low_price) and \
               (min(open_price, close_price) - low_price) <= 0.1 * (high_price - low_price) and \
               (high_price - max(open_price, close_price)) > 2 * abs(open_price - close_price):
                patterns.append((self.data.index[i], 'Gravestone Doji'))

        return patterns

    def detect_spinning_top(self):
        """Detect Spinning Top patterns."""
        patterns = []
        for i in range(len(self.data)):
            open_price = self.data['open'].iloc[i]
            close_price = self.data['close'].iloc[i]
            high_price = self.data['high'].iloc[i]
            low_price = self.data['low'].iloc[i]

            # Calculate the body and shadows
            body = abs(close_price - open_price)
            lower_shadow = open_price - low_price if close_price > open_price else close_price - low_price
            upper_shadow = high_price - close_price if close_price > open_price else high_price - open_price

            # Spinning Top pattern conditions
            if body <= 0.1 * (high_price - low_price) and lower_shadow > body and upper_shadow > body:
                patterns.append((self.data.index[i], 'Spinning Top'))

        return patterns

    def detect_falling_three_methods(self):
        """Detect Falling Three Methods patterns."""
        patterns = []
        for i in range(4, len(self.data)):
            first_open = self.data['open'].iloc[i - 4]
            first_close = self.data['close'].iloc[i - 4]
            last_open = self.data['open'].iloc[i]
            last_close = self.data['close'].iloc[i]

            # Check if the first and last candles are bearish
            if first_close < first_open and last_close < last_open:
                # Check if the last candle closes below the first candle's close
                if last_close < first_close:
                    # Check the middle three candles
                    middle_candles = True
                    for j in range(i - 3, i):
                        mid_open = self.data['open'].iloc[j]
                        mid_close = self.data['close'].iloc[j]
                        # Middle candles should be within the range of the first candle
                        if not (first_close < mid_open < first_open and first_close < mid_close < first_open):
                            middle_candles = False
                            break
                    if middle_candles:
                        patterns.append((self.data.index[i], 'Falling Three Methods'))

        return patterns

    def detect_rising_three_methods(self):
        """Detect Rising Three Methods patterns."""
        patterns = []
        for i in range(4, len(self.data)):
            first_open = self.data['open'].iloc[i - 4]
            first_close = self.data['close'].iloc[i - 4]
            last_open = self.data['open'].iloc[i]
            last_close = self.data['close'].iloc[i]

            # Check if the first and last candles are bullish
            if first_close > first_open and last_close > last_open:
                # Check if the last candle closes above the first candle's close
                if last_close > first_close:
                    # Check the middle three candles
                    middle_candles = True
                    for j in range(i - 3, i):
                        mid_open = self.data['open'].iloc[j]
                        mid_close = self.data['close'].iloc[j]
                        # Middle candles should be within the range of the first candle
                        if not (first_open < mid_open < first_close and first_open < mid_close < first_close):
                            middle_candles = False
                            break
                    if middle_candles:
                        patterns.append((self.data.index[i], 'Rising Three Methods'))

        return patterns 