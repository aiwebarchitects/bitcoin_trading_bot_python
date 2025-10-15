"""
Settings configuration for the Bitcoin trading bot
Automatically loads optimized parameters from backtest results
"""

import json
import os
from typing import Dict

# =============================================================================
# PARAMETER LOADING FROM BACKTEST RESULTS
# =============================================================================

def load_optimized_parameters() -> Dict:
    """Load optimized parameters from backtest results.json"""
    results_path = os.path.join(os.path.dirname(__file__), "backtest_results", "results.json")
    
    # Default parameters (fallback)
    defaults = {
        'rsi_period': 10,
        'oversold': 20,
        'overbought': 65,
        'take_profit': 0.015,
        'stop_loss': -0.007
    }
    
    try:
        if os.path.exists(results_path):
            with open(results_path, 'r') as f:
                data = json.load(f)
            
            best_strategies = data.get('best_strategies', [])
            if best_strategies:
                # Get best strategy (highest win rate)
                best = best_strategies[0]
                params = best.get('parameters', {})
                
                print(f"Loaded optimized parameters from backtest results:")
                print(f"  Win Rate: {best.get('win_rate', 0):.2f}%")
                print(f"  Total Profit: {best.get('total_profit', 0):.2f}%")
                print(f"  Parameters: {params}")
                
                return params
    except Exception as e:
        print(f"Error loading optimized parameters: {e}")
    
    print("Using default parameters")
    return defaults

# Load optimized parameters
_optimized_params = load_optimized_parameters()

# =============================================================================
# LIVE TRADING BOT SETTINGS
# =============================================================================

# Network configuration
BOT_USE_TESTNET = False  # True for testnet, False for mainnet (REAL MONEY!)

# Trading configuration
BOT_POSITION_VALUE_USD = 20.0  # USD value per position
BOT_MAX_TOTAL_POSITION_USD = 100.0  # Maximum total position value in USD
BOT_CYCLE_INTERVAL = 60  # Seconds between trading cycles

# Cooldown configuration
BOT_BUY_COOLDOWN_MINUTES = 5  # Minutes to wait after each buy before buying again

# RSI trading parameters (loaded from backtest optimization)
BOT_RSI_PERIOD = _optimized_params.get('rsi_period', 10)
BOT_RSI_OVERSOLD = _optimized_params.get('oversold', 20)
BOT_RSI_OVERBOUGHT = _optimized_params.get('overbought', 65)

# Risk management (loaded from backtest optimization)
BOT_TAKE_PROFIT = _optimized_params.get('take_profit', 0.015)
BOT_STOP_LOSS = _optimized_params.get('stop_loss', -0.007)

# Sell conditions
BOT_SELL_ENTIRE_POSITION = True  # True = sell entire position, False = sell one position at a time
