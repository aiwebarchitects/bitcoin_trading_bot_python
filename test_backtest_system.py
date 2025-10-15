#!/usr/bin/env python3
"""
Test script to verify the backtest optimization system
"""

from helpers.backtest_manager import BacktestManager

def main():
    print("Testing Backtest Optimization System")
    print("="*60)
    
    # Create manager
    manager = BacktestManager()
    
    # Run optimization (force=True to test even if results exist)
    print("\nRunning optimization test...")
    params = manager.initialize(force=True)
    
    print("\n" + "="*60)
    print("OPTIMIZATION TEST COMPLETE")
    print("="*60)
    print(f"\nBest parameters found: {params}")
    
    # Verify results file was created
    import os
    if os.path.exists(manager.results_path):
        print(f"\n✅ Results file created: {manager.results_path}")
        
        # Load and display results
        data = manager.load_results()
        if data and data.get('best_strategies'):
            print(f"\n✅ Found {len(data['best_strategies'])} optimized strategies")
            print("\nTop 3 strategies by win rate:")
            for i, strategy in enumerate(data['best_strategies'][:3], 1):
                print(f"\n{i}. Win Rate: {strategy['win_rate']:.2f}% | "
                      f"Profit: {strategy['total_profit']:.2f}% | "
                      f"Trades: {strategy['total_trades']}")
                print(f"   Parameters: {strategy['parameters']}")
    else:
        print(f"\n❌ Results file not found: {manager.results_path}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
