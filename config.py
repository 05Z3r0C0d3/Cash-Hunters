#!/usr/bin/env python3
"""
SECURE CONFIGURATION FOR CASH HUNTERS BOT NETWORK
Environment variables and secure settings management
"""

import os
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Setup logging for config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class BotConfig:
    """Secure configuration management for bot network"""
    
    def __init__(self):
        """Initialize configuration and validate environment"""
        self.validate_environment()
        logger.info("Configuration loaded successfully")
    
    # ===============================================
    # BOT TOKENS (CRITICAL - NEVER HARDCODE!)
    # ===============================================
    @property
    def MASTER_BOT_TOKEN(self) -> str:
        """Get master bot token with validation"""
        token = os.getenv('MASTER_BOT_TOKEN')
        if not token:
            raise ValueError("MASTER_BOT_TOKEN is required but not set")
        return token
    
    @property
    def PUBLIC_BOT_TOKEN(self) -> str:
        """Get public bot token with validation"""
        token = os.getenv('PUBLIC_BOT_TOKEN')
        if not token:
            raise ValueError("PUBLIC_BOT_TOKEN is required but not set")
        return token
    
    # ===============================================
    # ADMIN SETTINGS
    # ===============================================
    @property
    def ADMIN_ID(self) -> int:
        """Get admin ID with validation"""
        admin_id = os.getenv('ADMIN_ID')
        if not admin_id:
            raise ValueError("ADMIN_ID is required but not set")
        try:
            return int(admin_id)
        except ValueError:
            raise ValueError("ADMIN_ID must be a valid integer")
    
    @property
    def ADMIN_USERNAME(self) -> str:
        """Get admin username"""
        return os.getenv('ADMIN_USERNAME', '')
    
    # ===============================================
    # COMMISSION SETTINGS
    # ===============================================
    @property
    def MASTER_COMMISSION_RATE(self) -> float:
        """Get master commission rate with validation"""
        rate = float(os.getenv('MASTER_COMMISSION_RATE', '0.15'))
        if not 0.0 <= rate <= 1.0:
            raise ValueError("MASTER_COMMISSION_RATE must be between 0.0 and 1.0")
        return rate
    
    @property
    def PUBLIC_COMMISSION_RATE(self) -> float:
        """Get public commission rate with validation"""
        rate = float(os.getenv('PUBLIC_COMMISSION_RATE', '0.12'))
        if not 0.0 <= rate <= 1.0:
            raise ValueError("PUBLIC_COMMISSION_RATE must be between 0.0 and 1.0")
        return rate
    
    @property
    def REFERRAL_BONUS(self) -> float:
        """Get referral bonus amount"""
        return float(os.getenv('REFERRAL_BONUS', '5.00'))
    
    # ===============================================
    # DATABASE SETTINGS
    # ===============================================
    @property
    def DATABASE_URL(self) -> str:
        """Get database URL"""
        return os.getenv('DATABASE_URL', 'sqlite:///cash_hunters.db')
    
    @property
    def REDIS_URL(self) -> str:
        """Get Redis URL"""
        return os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # ===============================================
    # API KEYS (EXTERNAL SERVICES)
    # ===============================================
    @property
    def API_KEYS(self) -> Dict[str, Optional[str]]:
        """Get all API keys"""
        return {
            'rakuten': os.getenv('RAKUTEN_API_KEY'),
            'amazon': os.getenv('AMAZON_API_KEY'),
            'coingecko': os.getenv('COINGECKO_API_KEY'),
            'etherscan': os.getenv('ETHERSCAN_API_KEY'),
            'binance': os.getenv('BINANCE_API_KEY'),
            'binance_secret': os.getenv('BINANCE_SECRET_KEY'),
            'coinbase': os.getenv('COINBASE_API_KEY'),
        }
    
    # ===============================================
    # SECURITY SETTINGS
    # ===============================================
    @property
    def RATE_LIMIT_PER_MINUTE(self) -> int:
        """Get rate limit per minute"""
        limit = int(os.getenv('RATE_LIMIT_PER_MINUTE', '20'))
        if limit <= 0:
            raise ValueError("RATE_LIMIT_PER_MINUTE must be positive")
        return limit
    
    @property
    def MAX_USERS_PER_BOT(self) -> int:
        """Get maximum users per bot"""
        max_users = int(os.getenv('MAX_USERS_PER_BOT', '10000'))
        if max_users <= 0:
            raise ValueError("MAX_USERS_PER_BOT must be positive")
        return max_users
    
    @property
    def SESSION_TIMEOUT(self) -> int:
        """Get session timeout in seconds"""
        timeout = int(os.getenv('SESSION_TIMEOUT', '3600'))
        if timeout <= 0:
            raise ValueError("SESSION_TIMEOUT must be positive")
        return timeout
    
    # ===============================================
    # FILE PATHS
    # ===============================================
    @property
    def SHARED_DATA_FILE(self) -> str:
        """Get shared data file path"""
        return os.getenv('SHARED_DATA_FILE', 'bot_network_data.json')
    
    @property
    def LOG_FILE(self) -> str:
        """Get log file path"""
        return os.getenv('LOG_FILE', 'cash_hunters.log')
    
    @property
    def BACKUP_DIR(self) -> str:
        """Get backup directory path"""
        backup_dir = os.getenv('BACKUP_DIR', './backups')
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        return backup_dir
    
    # ===============================================
    # WEBHOOK SETTINGS (PRODUCTION)
    # ===============================================
    @property
    def WEBHOOK_URL(self) -> Optional[str]:
        """Get webhook URL for production"""
        return os.getenv('WEBHOOK_URL')
    
    @property
    def WEBHOOK_PORT(self) -> int:
        """Get webhook port"""
        return int(os.getenv('WEBHOOK_PORT', '8443'))
    
    # ===============================================
    # DEVELOPMENT SETTINGS
    # ===============================================
    @property
    def DEBUG(self) -> bool:
        """Get debug mode status"""
        return os.getenv('DEBUG', 'False').lower() == 'true'
    
    @property
    def ENVIRONMENT(self) -> str:
        """Get environment (development/production)"""
        return os.getenv('ENVIRONMENT', 'development')
    
    # ===============================================
    # PREMIUM PLANS CONFIGURATION
    # ===============================================
    @property
    def PREMIUM_PLANS(self) -> Dict[str, Dict[str, Any]]:
        """Get premium plans configuration"""
        return {
            'flash': {
                'price': 19.00,
                'features': ['auto_claims', 'alerts', '2x_speed'],
                'description': 'Flash Plan - 2x Speed & Auto Claims'
            },
            'turbo': {
                'price': 39.00,
                'features': ['premium_apis', '5x_speed', 'priority'],
                'description': 'Turbo Plan - 5x Speed & Premium APIs'
            },
            'elite': {
                'price': 79.00,
                'features': ['exclusive_ops', '10x_speed', 'manager'],
                'description': 'Elite Plan - 10x Speed & Personal Manager'
            }
        }
    
    # ===============================================
    # VALIDATION METHODS
    # ===============================================
    def validate_environment(self) -> None:
        """Validate required environment variables"""
        required_vars = [
            'MASTER_BOT_TOKEN',
            'PUBLIC_BOT_TOKEN', 
            'ADMIN_ID'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Validate token formats
        self._validate_bot_tokens()
        
        logger.info("Environment validation passed")
    
    def _validate_bot_tokens(self) -> None:
        """Validate bot token formats"""
        master_token = os.getenv('MASTER_BOT_TOKEN')
        public_token = os.getenv('PUBLIC_BOT_TOKEN')
        
        if master_token and not self._is_valid_token_format(master_token):
            raise ValueError("MASTER_BOT_TOKEN has invalid format")
        
        if public_token and not self._is_valid_token_format(public_token):
            raise ValueError("PUBLIC_BOT_TOKEN has invalid format")
    
    def _is_valid_token_format(self, token: str) -> bool:
        """Check if token has valid Telegram bot token format"""
        if not token:
            return False
        
        # Basic format: numbers:letters_and_numbers
        parts = token.split(':')
        if len(parts) != 2:
            return False
        
        bot_id, auth_token = parts
        return bot_id.isdigit() and len(auth_token) >= 35
    
    # ===============================================
    # UTILITY METHODS
    # ===============================================
    def get_api_key(self, service: str) -> Optional[str]:
        """Safely get API key for service"""
        api_key = self.API_KEYS.get(service.lower())
        if api_key:
            logger.info(f"API key found for service: {service}")
        else:
            logger.warning(f"No API key configured for service: {service}")
        return api_key
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        return user_id == self.ADMIN_ID
    
    def get_commission_rate(self, bot_type: str) -> float:
        """Get commission rate for bot type"""
        if bot_type == 'master':
            return self.MASTER_COMMISSION_RATE
        elif bot_type == 'public':
            return self.PUBLIC_COMMISSION_RATE
        else:
            logger.warning(f"Unknown bot type: {bot_type}")
            return 0.0
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == 'production'
    
    def get_plan_info(self, plan_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific premium plan"""
        return self.PREMIUM_PLANS.get(plan_name.lower())
    
    def list_available_apis(self) -> list:
        """List all APIs that have keys configured"""
        return [service for service, key in self.API_KEYS.items() if key]

# ===============================================
# GLOBAL CONFIG INSTANCE
# ===============================================
try:
    config = BotConfig()
    logger.info("Cash Hunters configuration initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize configuration: {e}")
    raise

# ===============================================
# CONFIGURATION SUMMARY
# ===============================================
def print_config_summary():
    """Print configuration summary (without sensitive data)"""
    print("\n" + "="*50)
    print("🚀 CASH HUNTERS BOT NETWORK CONFIG")
    print("="*50)
    print(f"Environment: {config.ENVIRONMENT}")
    print(f"Debug Mode: {config.DEBUG}")
    print(f"Admin ID: {config.ADMIN_ID}")
    print(f"Master Commission: {config.MASTER_COMMISSION_RATE*100}%")
    print(f"Public Commission: {config.PUBLIC_COMMISSION_RATE*100}%")
    print(f"Rate Limit: {config.RATE_LIMIT_PER_MINUTE}/min")
    print(f"Max Users: {config.MAX_USERS_PER_BOT}")
    print(f"Available APIs: {', '.join(config.list_available_apis())}")
    print(f"Premium Plans: {', '.join(config.PREMIUM_PLANS.keys())}")
    print("="*50)

if __name__ == "__main__":
    print_config_summary()
