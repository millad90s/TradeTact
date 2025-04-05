import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from technical_analysis import TechnicalAnalysis
import ccxt

# Initialize Binance exchange
exchange = ccxt.binance()

# Fetch historical candlestick data
symbol = 'BTC/USDT'  # Update with your desired trading pair
timeframe = '1h'  # Update with your desired timeframe
limit = 200  # Number of candlesticks to fetch

# Fetch data
ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

# Convert to DataFrame
data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Convert the 'timestamp' column to datetime and set it as the index
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
data.set_index('timestamp', inplace=True)

# Slice the DataFrame to get the last 200 rows
# data = data.tail(00)

# Fetch 30-minute data
symbol_30m = 'BTC/USDT'  # Update with your desired trading pair
timeframe_30m = '30m'  # 30-minute timeframe
limit_30m = 150  # Number of candlesticks to fetch

# Fetch data for 30-minute timeframe
ohlcv_30m = exchange.fetch_ohlcv(symbol_30m, timeframe=timeframe_30m, limit=limit_30m)

# Convert to DataFrame
data_30m = pd.DataFrame(ohlcv_30m, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Convert the 'timestamp' column to datetime and set it as the index
data_30m['timestamp'] = pd.to_datetime(data_30m['timestamp'], unit='ms')
data_30m.set_index('timestamp', inplace=True)

# Perform technical analysis
st.set_page_config(layout="wide")
st.title('Technical Analysis Dashboard')

# Initialize the TechnicalAnalysis class
st.sidebar.header('Technical Indicators')
ta = TechnicalAnalysis(data)

# Calculate indicators
ma_window = st.sidebar.slider('Moving Average Window', 5, 50, 20, key='ma_window')
data['MA'] = ta.moving_average(window=ma_window)
data['RSI'] = ta.rsi()
data['MACD'], data['Signal'] = ta.macd()

# Add a slider for Support and Resistance window size
sr_window = st.sidebar.slider('Support and Resistance Window', 5, 10, 7, key='sr_window')

# Calculate strong support and resistance levels
strong_support, strong_resistance = ta.calculate_strong_support_resistance(order=sr_window, touch_threshold=3, merge_threshold=0.01)

# Calculate Bollinger Bands
bb_window = st.sidebar.slider('Bollinger Bands Window', 5, 50, 20, key='bb_window')
ma, upper_band, lower_band = ta.bollinger_bands(window=bb_window)

# Add a checkbox to toggle Bollinger Bands
show_bb = st.sidebar.checkbox('Show Bollinger Bands')

# Add a checkbox to toggle Moving Average
show_ma = st.sidebar.checkbox('Show Moving Average')

# Add a checkbox to toggle Support and Resistance, enabled by default
show_sr = st.sidebar.checkbox('Show Support and Resistance', value=True)

# Remove duplicate checkboxes and add unique keys

# Bullish Patterns
st.sidebar.subheader('Bullish Patterns')
show_three_white_soldiers = st.sidebar.checkbox('Show Three White Soldiers', key='three_white_soldiers')
show_bullish_harami = st.sidebar.checkbox('Show Bullish Harami', key='bullish_harami')
show_harami_cross = st.sidebar.checkbox('Show Harami Cross', key='harami_cross')
show_morning_star = st.sidebar.checkbox('Show Morning Star Pattern', key='morning_star')
show_rising_three_methods = st.sidebar.checkbox('Show Rising Three Methods Pattern', key='rising_three_methods')

# Bearish Patterns
st.sidebar.subheader('Bearish Patterns')
show_engulfing = st.sidebar.checkbox('Show Engulfing Patterns', key='engulfing')
show_hanging_man = st.sidebar.checkbox('Show Hanging Man Pattern', key='hanging_man')
show_shooting_star = st.sidebar.checkbox('Show Shooting Star Pattern', key='shooting_star')
show_evening_star = st.sidebar.checkbox('Show Evening Star Pattern', key='evening_star')
show_three_black_crows = st.sidebar.checkbox('Show Three Black Crows Pattern', key='three_black_crows')
show_dark_cloud_cover = st.sidebar.checkbox('Show Dark Cloud Cover Pattern', key='dark_cloud_cover')
show_bearish_harami = st.sidebar.checkbox('Show Bearish Harami Pattern', key='bearish_harami')

# Neutral Patterns
st.sidebar.subheader('Neutral Patterns')
show_doji_star = st.sidebar.checkbox('Show Doji Star Pattern', key='doji_star')
show_long_legged_doji = st.sidebar.checkbox('Show Long-Legged Doji Pattern', key='long_legged_doji')
show_dragonfly_doji = st.sidebar.checkbox('Show Dragonfly Doji Pattern', key='dragonfly_doji')
show_gravestone_doji = st.sidebar.checkbox('Show Gravestone Doji Pattern', key='gravestone_doji')

# Add a checkbox for Hammer pattern
show_hammer = st.sidebar.checkbox('Show Hammer Pattern', key='hammer')

# Plot the candlestick chart
fig_candlestick = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                name='Candlestick')])

# Add moving average to the candlestick chart
if show_ma:
    ma_window = st.sidebar.slider('Moving Average Window', 5, 50, 20, key='ma_window_chart')
    moving_average = ta.moving_average(window=ma_window)
    fig_candlestick.add_trace(go.Scatter(x=data.index, y=moving_average, mode='lines', name='Moving Average', line=dict(color='orange')))

# Function to count touches
def count_touches(levels, prices):
    touch_counts = {}
    for level in levels:
        touch_counts[level] = ((prices >= level * 0.99) & (prices <= level * 1.01)).sum()
    return touch_counts

# Count touches for support and resistance levels
support_touches = count_touches(strong_support, data['close'])
resistance_touches = count_touches(strong_resistance, data['close'])

# Select the strongest levels (e.g., top 3)
strongest_support = sorted(support_touches, key=support_touches.get, reverse=True)[:3]
strongest_resistance = sorted(resistance_touches, key=resistance_touches.get, reverse=True)[:3]

# Plot the strongest support and resistance zones if the checkbox is checked
if show_sr:
    for level in strong_support:
        fig_candlestick.add_shape(type='line', x0=data.index.min(), x1=data.index.max(), y0=level, y1=level,
                                  line=dict(color='blue', dash='dash'), name='Support')
        # Add annotation for support level
        fig_candlestick.add_annotation(x=data.index.min(), y=level,
                                       text=f'Support: {level:.2f}',
                                       showarrow=False,
                                       yshift=10,
                                       bgcolor='blue',
                                       opacity=0.7)

    for level in strong_resistance:
        fig_candlestick.add_shape(type='line', x0=data.index.min(), x1=data.index.max(), y0=level, y1=level,
                                  line=dict(color='red', dash='dash'), name='Resistance')
        # Add annotation for resistance level
        fig_candlestick.add_annotation(x=data.index.min(), y=level,
                                       text=f'Resistance: {level:.2f}',
                                       showarrow=False,
                                       yshift=-10,
                                       bgcolor='red',
                                       opacity=0.7)

# Annotate the candlestick chart with Engulfing patterns if the checkbox is checked
if show_engulfing:
    engulfing_patterns = ta.detect_engulfing_patterns()
    for pattern in engulfing_patterns:
        x, pattern_type = pattern
        color = 'green' if pattern_type == 'Bullish' else 'red'
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor=color,
                                       opacity=0.7)

# Annotate the candlestick chart with Three White Soldiers pattern if the checkbox is checked
if show_three_white_soldiers:
    three_white_soldiers = ta.detect_three_white_soldiers()
    for pattern in three_white_soldiers:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='blue',
                                       opacity=0.7)

# Annotate the candlestick chart with Bullish Harami pattern if the checkbox is checked
if show_bullish_harami:
    bullish_harami = ta.detect_bullish_harami()
    for pattern in bullish_harami:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='purple',
                                       opacity=0.7)

# Annotate the candlestick chart with Harami Cross pattern if the checkbox is checked
if show_harami_cross:
    harami_cross_patterns = ta.detect_harami_cross()
    for pattern in harami_cross_patterns:
        x, pattern_type = pattern
        color = 'orange' if 'Bullish' in pattern_type else 'darkorange'
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor=color,
                                       opacity=0.7)

# Annotate the candlestick chart with Hammer pattern if the checkbox is checked
if show_hammer:
    hammer_patterns = ta.detect_hammer()
    for pattern in hammer_patterns:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='yellow',
                                       opacity=0.7)

# Annotate the candlestick chart with Morning Star pattern if the checkbox is checked
if show_morning_star:
    morning_star_patterns = ta.detect_morning_star()
    for pattern in morning_star_patterns:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='lightgreen',
                                       opacity=0.7)

# Annotate the candlestick chart with Hanging Man pattern if the checkbox is checked
if show_hanging_man:
    hanging_man_patterns = ta.detect_hanging_man()
    for pattern in hanging_man_patterns:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='pink',
                                       opacity=0.7)

# Annotate the candlestick chart with Shooting Star pattern if the checkbox is checked
if show_shooting_star:
    shooting_star_patterns = ta.detect_shooting_star()
    for pattern in shooting_star_patterns:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='red',
                                       opacity=0.7)

# Annotate the candlestick chart with Evening Star pattern if the checkbox is checked
if show_evening_star:
    evening_star_patterns = ta.detect_evening_star()
    for pattern in evening_star_patterns:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='darkred',
                                       opacity=0.7)

# Annotate the candlestick chart with Three Black Crows pattern if the checkbox is checked
if show_three_black_crows:
    three_black_crows_patterns = ta.detect_three_black_crows()
    for pattern in three_black_crows_patterns:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='black',
                                       opacity=0.7)

# Annotate the candlestick chart with Dark Cloud Cover pattern if the checkbox is checked
if show_dark_cloud_cover:
    dark_cloud_cover_patterns = ta.detect_dark_cloud_cover()
    for pattern in dark_cloud_cover_patterns:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='darkblue',
                                       opacity=0.7)

# Annotate the candlestick chart with Bearish Harami pattern if the checkbox is checked
if show_bearish_harami:
    bearish_harami_patterns = ta.detect_bearish_harami()
    for pattern in bearish_harami_patterns:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='brown',
                                       opacity=0.7)

# Annotate the candlestick chart with Doji Star pattern if the checkbox is checked
if show_doji_star:
    doji_star_patterns = ta.detect_doji_star()
    for pattern in doji_star_patterns:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='gray',
                                       opacity=0.7)

# Annotate the candlestick chart with Long-Legged Doji pattern if the checkbox is checked
if show_long_legged_doji:
    long_legged_doji_patterns = ta.detect_long_legged_doji()
    for pattern in long_legged_doji_patterns:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='lightgray',
                                       opacity=0.7)

# Annotate the candlestick chart with Dragonfly Doji pattern if the checkbox is checked
if show_dragonfly_doji:
    dragonfly_doji_patterns = ta.detect_dragonfly_doji()
    for pattern in dragonfly_doji_patterns:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='green',
                                       opacity=0.7)

# Annotate the candlestick chart with Gravestone Doji pattern if the checkbox is checked
if show_gravestone_doji:
    gravestone_doji_patterns = ta.detect_gravestone_doji()
    for pattern in gravestone_doji_patterns:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='red',
                                       opacity=0.7)

# Annotate the candlestick chart with Rising Three Methods pattern if the checkbox is checked
if show_rising_three_methods:
    rising_three_methods = ta.detect_rising_three_methods()
    for pattern in rising_three_methods:
        x, pattern_type = pattern
        fig_candlestick.add_annotation(x=x, y=data.loc[x, 'high'],
                                       text=pattern_type,
                                       showarrow=True,
                                       arrowhead=1,
                                       ax=0,
                                       ay=-40,
                                       bgcolor='purple',
                                       opacity=0.7)

# Plot Bollinger Bands if the checkbox is checked
if show_bb:
    fig_candlestick.add_trace(go.Scatter(x=data.index, y=upper_band, mode='lines', name='Upper Band', line=dict(color='cyan', dash='dash')))
    fig_candlestick.add_trace(go.Scatter(x=data.index, y=lower_band, mode='lines', name='Lower Band', line=dict(color='cyan', dash='dash')))
    fig_candlestick.add_trace(go.Scatter(x=data.index, y=ma, mode='lines', name='Middle Band', line=dict(color='cyan', dash='dot')))

# Get the current price
current_price = data['close'].iloc[-1]

# Add a horizontal line for the current price
fig_candlestick.add_shape(type='line', x0=data.index.min(), x1=data.index.max(), y0=current_price, y1=current_price,
                          line=dict(color='green', dash='dot'), name='Current Price')

# Add annotation for the current price
fig_candlestick.add_annotation(x=data.index.max(), y=current_price,
                               text=f'Current Price: {current_price:.2f}',
                               showarrow=False,
                               xshift=10,
                               bgcolor='green',
                               opacity=0.7)

# Update layout for better visualization
fig_candlestick.update_layout(title='1-Hour Candlestick Chart with Indicators',
                               xaxis_title='Time',
                               yaxis_title='Price',
                               xaxis_rangeslider_visible=False,
                               height=700)  # Set the height of the chart

# Display the candlestick chart
st.plotly_chart(fig_candlestick, use_container_width=True)

# Initialize the TechnicalAnalysis class for 30-minute data
ta_30m = TechnicalAnalysis(data_30m)

# Calculate indicators for 30-minute data
ma_30m = ta_30m.moving_average(window=ma_window)
ma_30m, upper_band_30m, lower_band_30m = ta_30m.bollinger_bands(window=bb_window)
support_30m, resistance_30m = ta_30m.calculate_support_resistance(order=sr_window)

# Calculate strong support and resistance levels for 30-minute data
strong_support_30m, strong_resistance_30m = ta_30m.calculate_strong_support_resistance(order=sr_window, touch_threshold=3, merge_threshold=0.01)

# Plot the 30-minute candlestick chart
fig_candlestick_30m = go.Figure(data=[go.Candlestick(x=data_30m.index,
                open=data_30m['open'],
                high=data_30m['high'],
                low=data_30m['low'],
                close=data_30m['close'],
                name='Candlestick 30m')])

# Plot moving average on the 30-minute candlestick chart if the checkbox is checked
if show_ma:
    fig_candlestick_30m.add_trace(go.Scatter(x=data_30m.index, y=ma_30m, mode='lines', name='Moving Average', line=dict(color='orange')))

# Plot Bollinger Bands on the 30-minute candlestick chart if the checkbox is checked
if show_bb:
    fig_candlestick_30m.add_trace(go.Scatter(x=data_30m.index, y=upper_band_30m, mode='lines', name='Upper Band', line=dict(color='cyan', dash='dash')))
    fig_candlestick_30m.add_trace(go.Scatter(x=data_30m.index, y=lower_band_30m, mode='lines', name='Lower Band', line=dict(color='cyan', dash='dash')))
    fig_candlestick_30m.add_trace(go.Scatter(x=data_30m.index, y=ma_30m, mode='lines', name='Middle Band', line=dict(color='cyan', dash='dot')))

# Plot the strongest support and resistance levels on the 30-minute chart if the checkbox is checked
if show_sr:
    for level in strong_support_30m:
        fig_candlestick_30m.add_shape(type='line', x0=data_30m.index.min(), x1=data_30m.index.max(), y0=level, y1=level,
                                      line=dict(color='blue', dash='dash'), name='Support')
        # Add annotation for support level
        fig_candlestick_30m.add_annotation(x=data_30m.index.min(), y=level,
                                           text=f'Support: {level:.2f}',
                                           showarrow=False,
                                           yshift=10,
                                           bgcolor='blue',
                                           opacity=0.7)

    for level in strong_resistance_30m:
        fig_candlestick_30m.add_shape(type='line', x0=data_30m.index.min(), x1=data_30m.index.max(), y0=level, y1=level,
                                      line=dict(color='red', dash='dash'), name='Resistance')
        # Add annotation for resistance level
        fig_candlestick_30m.add_annotation(x=data_30m.index.min(), y=level,
                                           text=f'Resistance: {level:.2f}',
                                           showarrow=False,
                                           yshift=-10,
                                           bgcolor='red',
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Engulfing patterns if the checkbox is checked
if show_engulfing:
    engulfing_patterns_30m = ta_30m.detect_engulfing_patterns()
    for pattern in engulfing_patterns_30m:
        x, pattern_type = pattern
        color = 'green' if pattern_type == 'Bullish' else 'red'
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor=color,
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Three White Soldiers pattern if the checkbox is checked
if show_three_white_soldiers:
    three_white_soldiers_30m = ta_30m.detect_three_white_soldiers()
    for pattern in three_white_soldiers_30m:
        x, pattern_type = pattern
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor='blue',
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Bullish Harami pattern if the checkbox is checked
if show_bullish_harami:
    bullish_harami_30m = ta_30m.detect_bullish_harami()
    for pattern in bullish_harami_30m:
        x, pattern_type = pattern
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor='purple',
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Harami Cross pattern if the checkbox is checked
if show_harami_cross:
    harami_cross_patterns_30m = ta_30m.detect_harami_cross()
    for pattern in harami_cross_patterns_30m:
        x, pattern_type = pattern
        color = 'orange' if 'Bullish' in pattern_type else 'darkorange'
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor=color,
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Morning Star pattern if the checkbox is checked
if show_morning_star:
    morning_star_patterns_30m = ta_30m.detect_morning_star()
    for pattern in morning_star_patterns_30m:
        x, pattern_type = pattern
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor='lightgreen',
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Shooting Star pattern if the checkbox is checked
if show_shooting_star:
    shooting_star_patterns_30m = ta_30m.detect_shooting_star()
    for pattern in shooting_star_patterns_30m:
        x, pattern_type = pattern
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor='red',
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Evening Star pattern if the checkbox is checked
if show_evening_star:
    evening_star_patterns_30m = ta_30m.detect_evening_star()
    for pattern in evening_star_patterns_30m:
        x, pattern_type = pattern
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor='darkred',
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Three Black Crows pattern if the checkbox is checked
if show_three_black_crows:
    three_black_crows_patterns_30m = ta_30m.detect_three_black_crows()
    for pattern in three_black_crows_patterns_30m:
        x, pattern_type = pattern
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor='black',
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Dark Cloud Cover pattern if the checkbox is checked
if show_dark_cloud_cover:
    dark_cloud_cover_patterns_30m = ta_30m.detect_dark_cloud_cover()
    for pattern in dark_cloud_cover_patterns_30m:
        x, pattern_type = pattern
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor='darkblue',
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Bearish Harami pattern if the checkbox is checked
if show_bearish_harami:
    bearish_harami_patterns_30m = ta_30m.detect_bearish_harami()
    for pattern in bearish_harami_patterns_30m:
        x, pattern_type = pattern
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor='brown',
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Doji Star pattern if the checkbox is checked
if show_doji_star:
    doji_star_patterns_30m = ta_30m.detect_doji_star()
    for pattern in doji_star_patterns_30m:
        x, pattern_type = pattern
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor='gray',
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Long-Legged Doji pattern if the checkbox is checked
if show_long_legged_doji:
    long_legged_doji_patterns_30m = ta_30m.detect_long_legged_doji()
    for pattern in long_legged_doji_patterns_30m:
        x, pattern_type = pattern
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor='lightgray',
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Dragonfly Doji pattern if the checkbox is checked
if show_dragonfly_doji:
    dragonfly_doji_patterns_30m = ta_30m.detect_dragonfly_doji()
    for pattern in dragonfly_doji_patterns_30m:
        x, pattern_type = pattern
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor='green',
                                           opacity=0.7)

# Annotate the 30-minute candlestick chart with Gravestone Doji pattern if the checkbox is checked
if show_gravestone_doji:
    gravestone_doji_patterns_30m = ta_30m.detect_gravestone_doji()
    for pattern in gravestone_doji_patterns_30m:
        x, pattern_type = pattern
        fig_candlestick_30m.add_annotation(x=x, y=data_30m.loc[x, 'high'],
                                           text=pattern_type,
                                           showarrow=True,
                                           arrowhead=1,
                                           ax=0,
                                           ay=-40,
                                           bgcolor='red',
                                           opacity=0.7)

# Update layout for better visualization
fig_candlestick_30m.update_layout(title='30-Minute Candlestick Chart',
                                  xaxis_title='Time',
                                  yaxis_title='Price',
                                  xaxis_rangeslider_visible=False,
                                  height=800)  # Set the height of the chart

# Display the 30-minute candlestick chart
st.plotly_chart(fig_candlestick_30m, use_container_width=True)

# Display the data
# st.subheader('Data Table')
# st.write(data.head()) 

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