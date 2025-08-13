diff --git a/config.py b/config.py
--- a/config.py
+++ b/config.py
@@ -0,0 +1,104 @@
+#!/usr/bin/env python3
+"""
+SECURE CONFIGURATION FOR CASH HUNTERS BOT NETWORK
+Environment variables and secure settings management
+"""
+
+import os
+from typing import Dict, Any
+from dotenv import load_dotenv
+
+# Load environment variables
+load_dotenv()
+
+class BotConfig:
+    """Secure configuration management for bot network"""
+    
+    def __init__(self):
+        self.validate_environment()
+    
+    # Bot Tokens (NEVER hardcode these!)
+    MASTER_BOT_TOKEN = os.getenv('MASTER_BOT_TOKEN')
+    PUBLIC_BOT_TOKEN = os.getenv('PUBLIC_BOT_TOKEN')
+    
+    # Admin Settings
+    ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))
+    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', '')
+    
+    # Commission Settings
+    MASTER_COMMISSION_RATE = float(os.getenv('MASTER_COMMISSION_RATE', '0.15'))  # 15%
+    PUBLIC_COMMISSION_RATE = float(os.getenv('PUBLIC_COMMISSION_RATE', '0.12'))  # 12%
+    REFERRAL_BONUS = float(os.getenv('REFERRAL_BONUS', '5.00'))
+    
+    # Database Settings
+    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///cash_hunters.db')
+    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
+    
+    # API Keys (External Services)
+    API_KEYS = {
+        'rakuten': os.getenv('RAKUTEN_API_KEY'),
+        'amazon': os.getenv('AMAZON_API_KEY'),
+        'coingecko': os.getenv('COINGECKO_API_KEY'),
+        'etherscan': os.getenv('ETHERSCAN_API_KEY'),
+        'binance': os.getenv('BINANCE_API_KEY'),
+        'coinbase': os.getenv('COINBASE_API_KEY'),
+    }
+    
+    # Security Settings
+    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '20'))
+    MAX_USERS_PER_BOT = int(os.getenv('MAX_USERS_PER_BOT', '10000'))
+    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '3600'))  # 1 hour
+    
+    # File Paths
+    SHARED_DATA_FILE = os.getenv('SHARED_DATA_FILE', 'bot_network_data.json')
+    LOG_FILE = os.getenv('LOG_FILE', 'cash_hunters.log')
+    BACKUP_DIR = os.getenv('BACKUP_DIR', './backups')
+    
+    # Webhook Settings (for production)
+    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
+    WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '8443'))
+    
+    # Premium Plans
+    PREMIUM_PLANS = {
+        'flash': {'price': 19.00, 'features': ['auto_claims', 'alerts', '2x_speed']},
+        'turbo': {'price': 39.00, 'features': ['premium_apis', '5x_speed', 'priority']},
+        'elite': {'price': 79.00, 'features': ['exclusive_ops', '10x_speed', 'manager']}
+    }
+    
+    def validate_environment(self):
+        """Validate required environment variables"""
+        required_vars = [
+            'MASTER_BOT_TOKEN',
+            'PUBLIC_BOT_TOKEN', 
+            'ADMIN_ID'
+        ]
+        
+        missing_vars = []
+        for var in required_vars:
+            if not os.getenv(var):
+                missing_vars.append(var)
+        
+        if missing_vars:
+            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
+    
+    @classmethod
+    def get_api_key(cls, service: str) -> str:
+        """Safely get API key for service"""
+        return cls.API_KEYS.get(service.lower(), '')
+    
+    @classmethod
+    def is_admin(cls, user_id: int) -> bool:
+        """Check if user is admin"""
+        return user_id == cls.ADMIN_ID
+    
+    @classmethod
+    def get_commission_rate(cls, bot_type: str) -> float:
+        """Get commission rate for bot type"""
+        if bot_type == 'master':
+            return cls.MASTER_COMMISSION_RATE
+        elif bot_type == 'public':
+            return cls.PUBLIC_COMMISSION_RATE
+        return 0.0
+
+# Global config instance
+config = BotConfig()
