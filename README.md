# TradeTact

**TradeTact** is a sophisticated Python application designed for traders and analysts who seek a tactical approach to market analysis. Leveraging advanced technical analysis techniques, TradeTact provides insights into market trends and patterns, helping users make informed trading decisions.

## Features

- **Technical Indicators**: Calculate key indicators such as Moving Averages, RSI, and MACD to understand market momentum and trends.
- **Pattern Detection**: Identify crucial candlestick patterns like Bullish/Bearish Engulfing, Harami, Hammer, and more to anticipate market movements.
- **Support and Resistance Levels**: Determine strong support and resistance levels using local minima and maxima, enhancing your trading strategy.
- **Bollinger Bands**: Analyze market volatility and potential price movements with Bollinger Bands.
- **Comprehensive Analysis**: Integrate multiple indicators and patterns for a holistic view of the market.

## Application Preview

![TradeTact Dashboard](Screenshot%202025-04-08%20at%2000.22.29.png)

## Configuration

The application can be configured through the `config.yaml` file:

### Trading Settings
```yaml
trading:
  symbol: "BTC/USDT"  # Trading pair
  timeframes:         # Available timeframes
    - "1h"
    - "30m"
    - "15m"
    - "5m"
```

### Technical Analysis Settings
```yaml
technical_analysis:
  support_resistance:
    order: 5          # Order for support/resistance calculation
    touch_threshold: 3 # Minimum touches for a level
    merge_threshold: 0.01 # Threshold for merging nearby levels
  
  bollinger_bands:
    window: 20        # Moving average window
    num_std: 2        # Number of standard deviations
  
  supply_demand:
    consolidation_candles: 5    # Number of candles for consolidation
    impulse_threshold: 0.02     # Price movement threshold
    min_zone_width: 0.01        # Minimum width for a zone
```

### Chart Settings
```yaml
chart:
  candlestick:
    height_1h: 700    # Height for 1-hour chart
    height_30m: 800   # Height for 30-minute chart
    height_15m: 800   # Height for 15-minute chart
    height_5m: 800    # Height for 5-minute chart
  
  annotations:
    opacity: 0.7      # Opacity for annotations
    font_size: 12     # Font size for annotations
  
  colors:
    bullish: "green"  # Color for bullish elements
    bearish: "red"    # Color for bearish elements
    neutral: "blue"   # Color for neutral elements
    moving_average: "orange"  # Color for moving average
    bollinger_bands: "cyan"   # Color for Bollinger Bands
    current_price: "green"    # Color for current price
```

### UI Controls
```yaml
ui_controls:
  indicators:
    show_moving_average: true      # Show/hide moving average
    show_bollinger_bands: false    # Show/hide Bollinger Bands
    show_support_resistance: true  # Show/hide support/resistance
    show_supply_demand: true       # Show/hide supply/demand zones
  
  bullish_patterns:
    show_three_white_soldiers: false  # Show/hide Three White Soldiers
    show_bullish_harami: false        # Show/hide Bullish Harami
    show_harami_cross: false          # Show/hide Harami Cross
    show_morning_star: false          # Show/hide Morning Star
    show_rising_three_methods: false  # Show/hide Rising Three Methods
  
  bearish_patterns:
    show_engulfing: false         # Show/hide Engulfing patterns
    show_hanging_man: false       # Show/hide Hanging Man
    show_shooting_star: false     # Show/hide Shooting Star
    show_evening_star: false      # Show/hide Evening Star
    show_three_black_crows: false # Show/hide Three Black Crows
    show_dark_cloud_cover: false  # Show/hide Dark Cloud Cover
    show_bearish_harami: false    # Show/hide Bearish Harami
  
  neutral_patterns:
    show_doji_star: false         # Show/hide Doji Star
    show_long_legged_doji: false  # Show/hide Long-Legged Doji
    show_dragonfly_doji: false    # Show/hide Dragonfly Doji
    show_gravestone_doji: false   # Show/hide Gravestone Doji
    show_hammer: false            # Show/hide Hammer pattern
```

## Getting Started

1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/yourusername/TradeTact.git
   cd TradeTact
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run streamlit_app.py
   ```

## Running with Docker

To run the application using Docker, follow these steps:

1. **Build the Docker Image**:
   ```bash
   docker build -t tradetact .
   ```

2. **Run the Docker Container**:
   ```bash
   docker run -p 8501:8501 tradetact
   ```

This will start the application, and you can access it by navigating to `http://localhost:8501` in your web browser.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for any bugs or feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 