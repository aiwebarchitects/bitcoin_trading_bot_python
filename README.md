# Free Bitcoin Trading Bot python for Hyperliquid API

A real-time monitoring and trading panel for Bitcoin (BTC) using the RSI 1MIN Double Confirm strategy on Hyperliquid, now with integrated backtesting!

![Free Hyperliquid Trading Bot](free_hyperliquid_trading_bot.png)

## 🎁 Get Started with Bonus

**Sign up using our referral link to get a 4% fee discount bonus:**
👉 [Join Hyperliquid with BONUS500](https://app.hyperliquid.xyz/join/BONUS500)

After signing up, get your API keys from: [Hyperliquid API Settings](https://app.hyperliquid.xyz/API)

## Screenshots

The bot features a clean, four-tab interface for monitoring, controlling, and backtesting your trading operations:

### Main Dashboard
![Main Dashboard](screenshots/Main.png)
*Real-time account overview with balance, current position, and RSI indicator*

### Bot Control Panel
![Bot Control](screenshots/Bot.png)
*Start/stop the bot, view activity logs, and monitor current trading signals*

### Trade History
![Trade History](screenshots/History.png)
*Track your last 20 Bitcoin trades with detailed information*

### Backtest Analysis
![Backtest](screenshots/Backtest.png)
*Test your strategy with historical data and view comprehensive performance metrics*

## Version 0.2 - Backtest Integration Release

**What's New in v0.2:**
- ✨ **Integrated Backtesting**: Test your strategy directly from the panel
- 🤖 **Self-Optimizing System**: Automatically runs backtests every 24 hours to find best parameters
- 📊 **4-Tab Interface**: Added dedicated BACKTEST tab
- 🧹 **Cleaner Codebase**: Removed unused algorithms (MACD, SMA, Support Volume, Vol24)
- 📁 **Better Organization**: Backtesting files moved to `helpers/` folder
- 🎯 **Focused Strategy**: Optimized for RSI 1MIN Double Confirm only
- 🔄 **Dynamic Parameters**: Bot automatically uses best-performing parameters from backtest results

## Overview

This bot implements a SHORT-based trading strategy using RSI (Relative Strength Index) with a double confirmation mechanism:
- **SHORT Signal**: RSI tops above 65, then dips below 50 while price breaks support
- **COVER Signal**: RSI reaches oversold levels (< 20)
- **Risk Management**: Automatic take profit (1.5%) and stop loss (-0.7%)

## Features

- 🎯 **Real-time Monitoring**: Live account balance, positions, and RSI tracking
- 🤖 **Automated Trading**: Set-and-forget bot with configurable parameters
- 🔄 **Self-Optimizing**: Automatically backtests every 24 hours and uses best parameters
- 📊 **4-Tab Interface**: Main dashboard, bot control, trade history, and backtesting
- 🔬 **Integrated Backtesting**: Test strategy performance with historical data
- 🏆 **Performance-Based**: Bot uses parameters from best-performing backtest results
- 🔒 **Risk Management**: Built-in take profit and stop loss protection
- 🌐 **Testnet Support**: Test strategies safely before going live

## Installation

### Prerequisites

- Python 3.8 or higher
- Linux/Mac (for curses terminal UI)
- Hyperliquid account with API access

### Setup

1. Clone the repository:
```bash
git clone https://github.com/aiwebarchitects/hyperliquid_free_trading_bot.git
cd hyperliquid_free_trading_bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API credentials:
Open `executer/config.json` and replace the placeholder values with your Hyperliquid API credentials:
```json
{
  "account_address": "your_wallet_address",
  "secret_key": "your_private_key"
}
```

**For Mainnet:**
Get your API credentials from [Hyperliquid API Settings](https://app.hyperliquid.xyz/API)

**For Testnet:**
- First, claim 1000 USDC test funds: [Testnet Faucet](https://app.hyperliquid-testnet.xyz/drip)
- Then create your testnet API key: [Testnet API Settings](https://app.hyperliquid-testnet.xyz/API)
- Remember to set `BOT_USE_TESTNET = True` in `settings.py`

4. Configure bot settings:
Edit `settings.py` to customize:
- `BOT_USE_TESTNET`: Set to `True` for testnet, `False` for mainnet
- `BOT_POSITION_VALUE_USD`: Position size per trade
- `BOT_MAX_TOTAL_POSITION_USD`: Maximum total position value
- `BOT_BUY_COOLDOWN_MINUTES`: Cooldown between trades

## Usage

### Start the Panel

```bash
python3 bitcoin_panel.py
```

### Keyboard Controls

- **TAB** or **←/→**: Switch between tabs (Main, Bot, History, Backtest)
- **S**: Start the automated trading bot
- **X**: Stop the automated trading bot
- **B**: Run backtest (when on BACKTEST tab)
- **R**: Refresh data manually
- **Q**: Quit the application

### Tabs

1. **MAIN**: Account overview, current position, and RSI indicator
2. **BOT**: Bot control, activity logs, and current signals
3. **HISTORY**: Last 20 Bitcoin trades
4. **BACKTEST**: Strategy backtesting with performance metrics

## Backtesting & Self-Optimization

### Automatic Optimization System

The bot features an **intelligent self-optimization system** that automatically improves its performance:

1. **On Startup**: Checks if backtest results are older than 24 hours
2. **Auto-Backtest**: If needed, runs comprehensive parameter optimization
3. **Parameter Testing**: Tests 1000+ combinations of RSI settings, take profit, and stop loss
4. **Best Selection**: Automatically selects parameters with highest win rate
5. **Live Trading**: Bot uses these optimized parameters for actual trading

**Result**: Your bot is always trading with the most recently optimized parameters based on real market data!

### Manual Backtesting

You can also run backtests manually from the panel:

1. Navigate to the **BACKTEST** tab
2. Review current settings (RSI period, thresholds, take profit, stop loss)
3. Press **B** to run backtest
4. View results including:
   - Win rate and total profit
   - Profit factor and max drawdown
   - Average profit per trade
   - Recent trades with entry/exit details

### Backtest Features

- **Real Market Data**: Fetches 1-minute Bitcoin data from Binance
- **Comprehensive Testing**: Tests up to 1000 candles (approximately 16 hours)
- **Parameter Optimization**: Tests multiple combinations to find best settings
- **Detailed Results**: Trade-by-trade breakdown with entry/exit analysis
- **Performance Metrics**: Win rate, profit factor, max drawdown, and more
- **24-Hour Cache**: Results cached for 24 hours to avoid unnecessary re-testing
- **Automatic Updates**: Bot parameters automatically update from backtest results

### How Parameters Are Selected

The optimization system tests these parameter ranges:
- **RSI Period**: 7, 10, 14
- **Oversold Threshold**: 10, 15, 20, 25, 30
- **Overbought Threshold**: 60, 65, 70, 75, 80, 85
- **Take Profit**: 1.0%, 1.5%, 2.0%, 2.5%, 3.0%
- **Stop Loss**: -0.5%, -0.7%, -1.0%, -1.5%, -2.0%

The system ranks all combinations by:
1. **Primary**: Win rate (higher is better)
2. **Secondary**: Total profit (higher is better)

The top-performing combination is automatically loaded into `settings.py` and used by the bot.

## Trading Strategy

### RSI 1MIN Double Confirm (SHORT-based)

The bot uses a sophisticated double confirmation mechanism:

1. **Setup Phase**: RSI must first "top" by either:
   - Reaching overbought (> 65), OR
   - Making a local peak above 60

2. **SHORT Signal** (all conditions must be met):
   - RSI has topped (from step 1)
   - RSI crosses below 50
   - Price breaks below support level (lowest low in last 10 candles)

3. **COVER Signal**:
   - RSI crosses into oversold territory (< 20)

4. **Risk Management** (checked every cycle):
   - Take Profit: Close at +1.5% profit
   - Stop Loss: Close at -0.7% loss

### Dynamic Parameters (Auto-Optimized)

The bot **automatically loads optimized parameters** from backtest results:

**How It Works:**
1. System runs backtest optimization (every 24 hours or on first run)
2. Best parameters saved to `backtest_results/results.json`
3. `settings.py` automatically loads these optimized values
4. Bot uses these parameters for live trading

**Current Default Fallbacks** (used only if backtest fails):
- RSI Period: 10
- Oversold Threshold: 20
- Overbought Threshold: 65
- Take Profit: 1.5%
- Stop Loss: -0.7%

**To see your current optimized parameters:**
- Check `backtest_results/results.json` for the latest optimization results
- Or view them in the BACKTEST tab of the panel
- Parameters are displayed on startup in the console

**Note**: The bot will use the best-performing parameters from the most recent backtest, not the fallback defaults!

## Configuration

### settings.py

The `settings.py` file **automatically loads optimized parameters** from backtest results:

```python
# Network Configuration
BOT_USE_TESTNET = False  # Set to True for testnet

# Trading Configuration
BOT_POSITION_VALUE_USD = 100.0  # Position size per trade
BOT_MAX_TOTAL_POSITION_USD = 500.0  # Maximum total position
BOT_BUY_COOLDOWN_MINUTES = 5  # Cooldown between trades

# RSI Parameters (AUTO-LOADED from backtest_results/results.json)
# These values are automatically optimized every 24 hours
BOT_RSI_PERIOD = _optimized_params.get('rsi_period', 10)
BOT_RSI_OVERSOLD = _optimized_params.get('oversold', 20)
BOT_RSI_OVERBOUGHT = _optimized_params.get('overbought', 65)

# Risk Management (AUTO-LOADED from backtest_results/results.json)
BOT_TAKE_PROFIT = _optimized_params.get('take_profit', 0.015)
BOT_STOP_LOSS = _optimized_params.get('stop_loss', -0.007)
```

**Important**: The values shown above are fallback defaults. The actual values used by the bot come from `backtest_results/results.json` and are automatically optimized based on recent market performance.

### Manual Parameter Override

If you want to use specific parameters instead of auto-optimized ones:

1. Edit `settings.py`
2. Replace the `_optimized_params.get()` calls with hardcoded values
3. Example:
```python
BOT_RSI_PERIOD = 14  # Use 14 instead of auto-optimized value
```

**Note**: This is not recommended as it disables the self-optimization feature.

## Safety Features

- ✅ Testnet mode for safe testing
- ✅ Position size limits
- ✅ Trade cooldown periods
- ✅ Automatic stop loss
- ✅ Manual bot control (start/stop anytime)
- ✅ Backtesting before live trading

## File Structure

```
hyperliquid_free_trading_bot_0.2/
├── bitcoin_panel.py                 # Main application
├── settings.py                      # Bot configuration
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── system_files.txt                 # System documentation
├── changelog_v_0.2.md              # Version changelog
├── free_hyperliquid_trading_bot.png # Bot screenshot
├── algos/                           # Trading algorithms
│   ├── __init__.py
│   ├── base_algorithm.py
│   ├── rsi_algorithm.py
│   └── rsi_1min_double_confirm_algorithm.py
├── helpers/                         # Helper modules
│   ├── backtest_helper.py          # Panel backtester
│   ├── backtest_manager.py         # Auto-optimization system
│   └── start_backtesting.py        # Standalone backtester
├── backtest_results/                # Optimization results
│   └── results.json                # Best parameters (auto-generated)
├── executer/                        # Exchange utilities
│   ├── example_utils.py
│   └── config.json                 # API credentials
└── screenshots/                     # UI screenshots
    ├── Main.png
    ├── Bot.png
    └── History.png
```

## Troubleshooting

### Terminal Size Error
If you see "Terminal too small!", resize your terminal to at least 60x20 characters.

### Connection Issues
- Verify your API credentials in `executer/config.json`
- Check if you're using the correct network (testnet vs mainnet)
- Ensure you have internet connectivity

### No RSI Data
- The bot fetches data from Binance API for RSI calculation
- Check your internet connection
- Wait a few seconds for initial data load

### Backtest Errors
- Ensure you have internet connectivity (fetches data from Binance)
- Check that pandas and requests are properly installed
- Try running backtest again if it times out

## Changelog

### Version 0.2 (Current)
- Added integrated backtesting system with auto-optimization
- Self-optimizing: Automatically runs backtests every 24 hours
- Bot uses best-performing parameters from backtest results
- New BACKTEST tab in panel interface
- Parameter optimization tests 1000+ combinations
- Results cached for 24 hours to improve performance
- Moved backtesting files to `helpers/` folder
- Removed unused algorithms (MACD, SMA, Support Volume, Vol24)
- Cleaner, more focused codebase
- Updated documentation with optimization details

### Version 0.1
- Initial release
- 3-tab interface (Main, Bot, History)
- RSI 1MIN Double Confirm strategy
- Manual bot start/stop
- Basic monitoring features

## Disclaimer

⚠️ **IMPORTANT**: This bot is for educational purposes only. Trading cryptocurrencies involves substantial risk of loss. Always:
- Test thoroughly on testnet first
- Use backtesting to validate strategy
- Start with small position sizes
- Never invest more than you can afford to lose
- Monitor the bot regularly
- Understand the strategy before using it

## License

This project is provided as-is without any warranty. Use at your own risk.

## Support

For issues or questions, please check the system_files.txt for technical details or review the code documentation.

## Contributing

This is an open-source project. Feel free to fork, modify, and improve!
