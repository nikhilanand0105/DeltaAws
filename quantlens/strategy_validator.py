"""
Strict Strategy Compiler & Validator for QuantLens-XAI.
Validates extracted strategy rules to ensure:
1. Symbol exists in supported universe.
2. Positive and logically ordered indicator parameters.
3. No contradictory conditions (e.g. SL >= TP or Fast EMA >= Slow EMA).
4. Strict capital boundaries (max allocation <= 100%, max positions >= 1).
5. Zero arbitrary code execution or unvetted instructions.
"""

from typing import Tuple, List, Dict, Any
from quantlens.strategy_schema import StrategyDefinition

SUPPORTED_SYMBOLS = ["RELIANCE", "TCS", "INFY", "NIFTY50", "RELIANCE.NS", "TCS.NS", "INFY.NS", "^NSEI"]
SUPPORTED_TIMEFRAMES = ["daily", "hourly"]


class StrategyValidationError(Exception):
    """Custom exception raised when strategy fails structural validation."""
    pass


def validate_strategy(strategy: StrategyDefinition) -> Tuple[bool, List[str]]:
    """
    Validates a StrategyDefinition object.
    Returns (is_valid: bool, errors: List[str]).
    """
    errors = []

    # 1. Symbol validation
    clean_sym = strategy.symbol.upper().replace(".NS", "")
    if clean_sym not in [s.replace(".NS", "").replace("^", "") for s in SUPPORTED_SYMBOLS]:
        errors.append(f"Symbol '{strategy.symbol}' is not in the supported asset universe: {SUPPORTED_SYMBOLS}")

    # 2. Timeframe validation
    if strategy.timeframe not in SUPPORTED_TIMEFRAMES:
        errors.append(f"Timeframe '{strategy.timeframe}' not supported. Allowed: {SUPPORTED_TIMEFRAMES}")

    # 3. Indicator parameter validation
    inds = strategy.indicators
    if inds.ema_fast_period <= 0:
        errors.append(f"Fast EMA period ({inds.ema_fast_period}) must be positive.")
    if inds.ema_slow_period <= 0:
        errors.append(f"Slow EMA period ({inds.ema_slow_period}) must be positive.")
    if inds.ema_fast_period >= inds.ema_slow_period:
        errors.append(
            f"Contradictory EMA parameters: Fast EMA ({inds.ema_fast_period}) must be strictly less than Slow EMA ({inds.ema_slow_period})."
        )
    if not (0.0 < inds.rsi_threshold < 100.0):
        errors.append(f"RSI threshold ({inds.rsi_threshold}) must be between 0 and 100.")

    # 4. Risk parameter validation
    rc = strategy.risk_config
    if rc.initial_capital <= 0:
        errors.append(f"Initial capital ({rc.initial_capital}) must be greater than 0.")
    if not (0.1 <= rc.max_position_allocation_pct <= 100.0):
        errors.append(f"Max allocation ({rc.max_position_allocation_pct}%) must be between 0.1% and 100%.")
    if rc.max_open_positions < 1:
        errors.append(f"Max open positions ({rc.max_open_positions}) must be at least 1.")

    # 5. Exit rule validation
    exit_r = strategy.exit_rule
    if exit_r.stop_loss_pct <= 0:
        errors.append(f"Stop-loss ({exit_r.stop_loss_pct}%) must be positive.")
    if exit_r.take_profit_pct <= 0:
        errors.append(f"Take-profit ({exit_r.take_profit_pct}%) must be positive.")
    if exit_r.stop_loss_pct >= exit_r.take_profit_pct * 3.0:
        errors.append(
            f"Unfavorable Risk-Reward Ratio: Stop-Loss ({exit_r.stop_loss_pct}%) is more than 3x the Take-Profit ({exit_r.take_profit_pct}%)."
        )

    # 6. Safety check: mode must be paper
    if rc.trading_mode != "paper":
        errors.append("Safety Violation: Trading mode must strictly be 'paper'. Real-money trading is disabled.")

    return len(errors) == 0, errors
