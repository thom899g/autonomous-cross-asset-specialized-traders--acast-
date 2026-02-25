"""
ACAST Configuration and Constants
Centralized configuration management for the ACAST ecosystem
"""
import os
from dataclasses import dataclass
from typing import Dict, Any, Optional
from enum import Enum
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AssetClass(Enum):
    """Supported asset classes for ACAST specialization"""
    EQUITY = "equity"
    CRYPTO = "crypto"
    FOREX = "forex"
    COMMODITY = "commodity"
    FIXED_INCOME = "fixed_income"

class TradingMode(Enum):
    """Trading operation modes"""
    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"

@dataclass
class ACASTConfig:
    """Main configuration container for ACAST nodes"""
    
    # Node Identity
    node_id: str
    asset_class: AssetClass
    trading_mode: TradingMode = TradingMode.PAPER
    
    # Trading Parameters
    initial_capital: float = 10000.0
    max_position_size: float = 0.1  # 10% of capital
    stop_loss_pct: float = 0.02  # 2% stop loss
    take_profit_pct: float = 0.05  # 5% take profit
    
    # RL Training Parameters
    learning_rate: float = 0.001
    discount_factor: float = 0.99
    exploration_rate: float = 0.1
    training_episodes: int = 1000
    
    # Quantum-Inspired Parameters
    quantum_temperature: float = 1.0  # For simulated annealing
    quantum_entanglement: bool = False  # Enable correlation effects
    
    # Firestore Configuration
    firestore_project: str = os.getenv("FIRESTORE_PROJECT", "acast-ecosystem")
    firestore_collection: str = "acast_nodes"
    
    # Logging Configuration
    log_level: str = logging.INFO
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Risk Management
    max_drawdown: float = 0.15  # 15% maximum drawdown
    daily_loss_limit: float = 0.03  # 3% daily loss limit
    correlation_threshold: float = 0.7  # For cross-asset analysis
    
    @classmethod
    def from_env(cls, node_id: str, asset_class: AssetClass) -> 'ACASTConfig':
        """Create configuration from environment variables"""
        return cls(
            node_id=node_id,
            asset_class=asset_class,
            trading_mode=TradingMode(os.getenv("TRADING_MODE", "paper")),
            initial_capital=float(os.getenv("INITIAL_CAPITAL", "10000")),
            max_position_size=float(os.getenv("MAX_POSITION_SIZE", "0.1")),
            firestore_project=os.getenv("FIRESTORE_PROJECT", "acast-ecosystem"),
            log_level=os.getenv("LOG_LEVEL", "INFO")
        )

def setup_logging(config: ACASTConfig) -> logging.Logger:
    """Configure and return logger for ACAST node"""
    logger = logging.getLogger(f"ACAST_{config.node_id}")
    logger.setLevel(config.log_level)
    
    # Create handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(config.log_level)
    
    # Create formatter
    formatter = logging.Formatter(config.log_format)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    
    # Prevent duplicate handlers
    logger.propagate = False
    
    return logger