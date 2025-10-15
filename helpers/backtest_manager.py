"""
Backtest Manager - Handles automatic backtesting and parameter optimization
Runs on system initialization and caches results for 24 hours
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import requests

from algos import RSI1MinDoubleConfirmAlgorithm, BacktestEngine


class BacktestManager:
    """Manages automatic backtesting and result caching"""
    
    def __init__(self, results_file: str = "results.json"):
        self.results_file = results_file
        self.results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backtest_results")
        self.results_path = os.path.join(self.results_dir, results_file)
        
        # Ensure results directory exists
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Parameter ranges for optimization
        self.param_ranges = {
            'rsi_period': [7, 10, 14],
            'oversold': [10, 15, 20, 25, 30],
            'overbought': [60, 65, 70, 75, 80, 85],
            'take_profit': [0.01, 0.015, 0.02, 0.025, 0.030],
            'stop_loss': [-0.005, -0.007, -0.01, -0.015, -0.020]
        }
    
    def needs_backtest(self) -> bool:
        """Check if backtest needs to be run (results older than 24 hours or missing)"""
        if not os.path.exists(self.results_path):
            return True
        
        try:
            with open(self.results_path, 'r') as f:
                data = json.load(f)
            
            last_run = data.get('last_run')
            if not last_run:
                return True
            
            last_run_time = datetime.fromisoformat(last_run)
            time_diff = datetime.now() - last_run_time
            
            # Run if older than 24 hours
            return time_diff > timedelta(hours=24)
            
        except Exception:
            return True
    
    def fetch_binance_data(self, symbol: str = "BTCUSDT", days: int = 1) -> Optional[pd.DataFrame]:
        """Fetch historical data from Binance (max 1000 1-minute candles = ~16 hours)"""
        try:
            url = "https://api.binance.com/api/v3/klines"
            
            # Binance limit is 1000 candles max
            limit = 1000
            
            params = {
                "symbol": symbol,
                "interval": "1m",
                "limit": limit
            }
            
            response = requests.get(url, params=params, timeout=30)
            if response.status_code != 200:
                return None
            
            data = response.json()
            if not data:
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['price'] = df['close'].astype(float)
            df['volume'] = df['volume'].astype(float)
            df['low'] = df['low'].astype(float)
            df['high'] = df['high'].astype(float)
            
            df = df[['timestamp', 'price', 'volume', 'low', 'high']]
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def run_single_backtest(self, df: pd.DataFrame, params: Dict) -> Optional[Dict]:
        """Run a single backtest with given parameters"""
        try:
            # Create algorithm instance
            algorithm = RSI1MinDoubleConfirmAlgorithm(
                period=params['rsi_period'],
                oversold_threshold=params['oversold'],
                overbought_threshold=params['overbought']
            )
            
            # Create backtest engine
            engine = BacktestEngine(
                algorithm=algorithm,
                take_profit=params['take_profit'],
                stop_loss=params['stop_loss'],
                commission=0.0005  # 0.05% commission
            )
            
            # Run backtest
            trades_df, metrics = engine.backtest(df)
            
            # Return combined result
            return {
                'parameters': params,
                'metrics': metrics,
                'total_trades': metrics['total_trades'],
                'win_rate': metrics['win_rate'],
                'total_profit': metrics['total_profit'],
                'profit_factor': metrics['profit_factor'],
                'max_drawdown': metrics['max_drawdown'],
                'avg_profit': metrics['avg_profit']
            }
            
        except Exception as e:
            print(f"Error in backtest: {e}")
            return None
    
    def optimize_parameters(self, df: pd.DataFrame, max_results: int = 10) -> List[Dict]:
        """
        Test multiple parameter combinations and return best results
        
        Args:
            df: Historical price data
            max_results: Maximum number of best results to keep
        
        Returns:
            List of best backtest results sorted by win rate
        """
        print("Starting parameter optimization...")
        print(f"Testing {len(self.param_ranges['rsi_period']) * len(self.param_ranges['oversold']) * len(self.param_ranges['overbought']) * len(self.param_ranges['take_profit']) * len(self.param_ranges['stop_loss'])} combinations...")
        
        results = []
        total_combinations = 0
        tested_combinations = 0
        
        # Generate all parameter combinations
        for rsi_period in self.param_ranges['rsi_period']:
            for oversold in self.param_ranges['oversold']:
                for overbought in self.param_ranges['overbought']:
                    for take_profit in self.param_ranges['take_profit']:
                        for stop_loss in self.param_ranges['stop_loss']:
                            total_combinations += 1
                            
                            # Skip invalid combinations
                            if oversold >= overbought:
                                continue
                            
                            params = {
                                'rsi_period': rsi_period,
                                'oversold': oversold,
                                'overbought': overbought,
                                'take_profit': take_profit,
                                'stop_loss': stop_loss
                            }
                            
                            tested_combinations += 1
                            
                            # Show progress every 50 combinations with cleaner output
                            if tested_combinations % 50 == 0:
                                progress_pct = (tested_combinations / total_combinations) * 100
                                print(f"\rTesting combinations: {tested_combinations}/{total_combinations} ({progress_pct:.1f}%)", end='', flush=True)
                            
                            result = self.run_single_backtest(df, params)
                            if result and result['total_trades'] >= 5:  # Minimum 5 trades
                                results.append(result)
        
        print(f"\n\nTested {tested_combinations} valid combinations")
        print(f"Found {len(results)} results with at least 5 trades")
        
        # Sort by win rate (primary) and total profit (secondary)
        results.sort(key=lambda x: (x['win_rate'], x['total_profit']), reverse=True)
        
        # Keep only top results
        return results[:max_results]
    
    def save_results(self, results: List[Dict]):
        """Save backtest results to JSON file"""
        try:
            # Convert numpy types to native Python types
            def convert_to_native(obj):
                """Recursively convert numpy types to native Python types"""
                import numpy as np
                
                if isinstance(obj, (np.integer, np.int64, np.int32)):
                    return int(obj)
                elif isinstance(obj, (np.floating, np.float64, np.float32)):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {key: convert_to_native(value) for key, value in obj.items()}
                elif isinstance(obj, list):
                    return [convert_to_native(item) for item in obj]
                elif hasattr(obj, 'item'):  # numpy scalar
                    return obj.item()
                return obj
            
            # Convert all results
            clean_results = convert_to_native(results)
            
            data = {
                'last_run': datetime.now().isoformat(),
                'data_points': int(len(results[0]['metrics'])) if results else 0,
                'best_strategies': clean_results
            }
            
            with open(self.results_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"Results saved to {self.results_path}")
            
        except Exception as e:
            print(f"Error saving results: {e}")
            import traceback
            traceback.print_exc()
    
    def load_results(self) -> Optional[Dict]:
        """Load cached backtest results"""
        try:
            if not os.path.exists(self.results_path):
                return None
            
            with open(self.results_path, 'r') as f:
                data = json.load(f)
            
            return data
            
        except Exception as e:
            print(f"Error loading results: {e}")
            return None
    
    def get_best_parameters(self) -> Optional[Dict]:
        """Get the best parameters from cached results"""
        data = self.load_results()
        if not data or not data.get('best_strategies'):
            return None
        
        # Return the best strategy (first in list)
        best = data['best_strategies'][0]
        return best['parameters']
    
    def run_optimization(self, days: int = 1, max_results: int = 10) -> bool:
        """
        Run full optimization process
        
        Args:
            days: Not used (kept for compatibility) - always fetches max 1000 candles
            max_results: Maximum number of best results to keep
        
        Returns:
            True if successful, False otherwise
        """
        print("="*60)
        print("BACKTEST OPTIMIZATION STARTING")
        print("="*60)
        
        # Fetch data
        print(f"Fetching historical data (max 1000 1-minute candles)...")
        df = self.fetch_binance_data()
        if df is None:
            print("Failed to fetch data")
            return False
        
        print(f"Loaded {len(df)} candles from {df.index[0]} to {df.index[-1]}")
        
        # Run optimization
        results = self.optimize_parameters(df, max_results=max_results)
        
        if not results:
            print("No valid results found")
            return False
        
        # Display best result
        best = results[0]
        print("\n" + "="*60)
        print("BEST STRATEGY FOUND")
        print("="*60)
        print(f"Win Rate:      {best['win_rate']:.2f}%")
        print(f"Total Profit:  {best['total_profit']:.2f}%")
        print(f"Total Trades:  {best['total_trades']}")
        print(f"Profit Factor: {best['profit_factor']:.2f}")
        print(f"Max Drawdown:  {best['max_drawdown']:.2f}%")
        print(f"Avg Profit:    {best['avg_profit']:.2f}%")
        print("\nParameters:")
        for key, value in best['parameters'].items():
            print(f"  {key}: {value}")
        
        # Save results
        self.save_results(results)
        
        print("\n" + "="*60)
        print(f"Saved top {len(results)} strategies to {self.results_path}")
        print("="*60)
        
        return True
    
    def initialize(self, force: bool = False) -> Dict:
        """
        Initialize backtest system - run optimization if needed
        
        Args:
            force: Force re-run even if results are fresh
        
        Returns:
            Best parameters to use
        """
        if force or self.needs_backtest():
            print("Running backtest optimization (results older than 24 hours or missing)...")
            success = self.run_optimization(max_results=10)
            
            if not success:
                print("Optimization failed, using default parameters")
                return self._get_default_parameters()
        else:
            print("Using cached backtest results (less than 24 hours old)")
        
        # Load and return best parameters
        params = self.get_best_parameters()
        if params:
            print(f"\nLoaded best parameters: {params}")
            return params
        else:
            print("No cached results found, using defaults")
            return self._get_default_parameters()
    
    def _get_default_parameters(self) -> Dict:
        """Get default parameters as fallback"""
        return {
            'rsi_period': 10,
            'oversold': 20,
            'overbought': 65,
            'take_profit': 0.015,
            'stop_loss': -0.007
        }


def main():
    """Test the backtest manager"""
    manager = BacktestManager()
    params = manager.initialize(force=True)
    print(f"\nFinal parameters to use: {params}")


if __name__ == "__main__":
    main()
