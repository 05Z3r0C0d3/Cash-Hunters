diff --git a/API_SETUP_GUIDE.md b/API_SETUP_GUIDE.md
--- a/API_SETUP_GUIDE.md
+++ b/API_SETUP_GUIDE.md
@@ -0,0 +1,394 @@
+# 🔑 **CASH HUNTERS - API SETUP GUIDE**
+
+*Complete step-by-step guide to set up all APIs needed for your bot network*
+
+---
+
+## 📋 **TABLE OF CONTENTS**
+
+1. [Telegram Bot API](#telegram-bot-api)
+2. [Rakuten Advertising API](#rakuten-advertising-api)
+3. [Amazon Associates API](#amazon-associates-api)
+4. [CoinGecko API](#coingecko-api)
+5. [Etherscan API](#etherscan-api)
+6. [Binance API](#binance-api)
+7. [Coinbase API](#coinbase-api)
+8. [Additional APIs](#additional-apis)
+9. [Testing Your APIs](#testing-your-apis)
+
+---
+
+## 🤖 **TELEGRAM BOT API**
+
+### **Step 1: Create Your Bots**
+
+1. **Open Telegram** and search for `@BotFather`
+2. **Start a chat** with BotFather
+3. **Create Master Bot:**
+   ```
+   /newbot
+   Choose name: YourName Cash Master
+   Choose username: yournamemaster_bot
+   ```
+4. **Create Public Bot:**
+   ```
+   /newbot
+   Choose name: YourName Flash Cash
+   Choose username: yournameflash_bot
+   ```
+
+### **Step 2: Get Your Tokens**
+
+- BotFather will give you tokens like: `123456789:ABCDEF...`
+- **MASTER_BOT_TOKEN**: For your personal bot
+- **PUBLIC_BOT_TOKEN**: For the public bot
+
+### **Step 3: Get Your User ID**
+
+1. **Message `@userinfobot`** on Telegram
+2. **Copy your User ID** (numbers only)
+3. **Use this as ADMIN_ID** in your .env file
+
+---
+
+## 💳 **RAKUTEN ADVERTISING API**
+
+*Earn commissions from cashback and affiliate marketing*
+
+### **Step 1: Sign Up**
+
+1. **Visit:** https://advertising.rakuten.com/
+2. **Click "Join Now"** → "Publisher"
+3. **Fill application:**
+   - Website: Your bot's channel/group
+   - Traffic: Social Media/Telegram
+   - Monthly visitors: 1000+
+
+### **Step 2: Get Approved**
+
+- **Approval time:** 1-7 days
+- **Requirements:** Active social media presence
+- **Tip:** Create a Telegram channel first
+
+### **Step 3: Get API Access**
+
+1. **Login to dashboard**
+2. **Go to:** Tools → API
+3. **Request API access**
+4. **Get your API key**
+
+### **Step 4: Integration**
+
+```python
+# Example Rakuten API call
+import requests
+
+def get_rakuten_deals(api_key):
+    url = "https://api.rakutenadvertising.com/coupon/1.0/coupons"
+    headers = {"Authorization": f"Bearer {api_key}"}
+    response = requests.get(url, headers=headers)
+    return response.json()
+```
+
+**💰 Earning Potential:** $50-500/month
+
+---
+
+## 🛒 **AMAZON ASSOCIATES API**
+
+*Earn commissions from Amazon product recommendations*
+
+### **Step 1: Join Amazon Associates**
+
+1. **Visit:** https://affiliate-program.amazon.com/
+2. **Sign up** with your details
+3. **Website/App info:**
+   - Type: Social Media
+   - Platform: Telegram Bot
+   - Description: Crypto cashback bot
+
+### **Step 2: Product Advertising API**
+
+1. **Go to:** https://advertising.amazon.com/API/docs
+2. **Sign up for Product Advertising API**
+3. **Create an application**
+4. **Get your credentials:**
+   - Access Key ID
+   - Secret Access Key
+   - Associate Tag
+
+### **Step 3: Implementation**
+
+```python
+# Amazon API example
+from paapi5_python_sdk.api.default_api import DefaultApi
+from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
+
+def search_amazon_products(keyword):
+    search_items_request = SearchItemsRequest(
+        partner_tag="your-associate-tag",
+        partner_type="Associates",
+        marketplace="www.amazon.com",
+        keywords=keyword,
+        search_index="All"
+    )
+    response = default_api.search_items(search_items_request)
+    return response
+```
+
+**💰 Earning Potential:** $100-1000/month
+
+---
+
+## 🪙 **COINGECKO API**
+
+*Real-time crypto prices and market data*
+
+### **Step 1: Sign Up (Free)**
+
+1. **Visit:** https://www.coingecko.com/en/api
+2. **Click "Get Free API Key"**
+3. **Sign up** with email
+4. **Verify email** and login
+
+### **Step 2: Get API Key**
+
+1. **Go to Dashboard**
+2. **Copy your API key**
+3. **Free tier:** 10,000 calls/month
+
+### **Step 3: Usage**
+
+```python
+# CoinGecko API example
+import requests
+
+def get_crypto_prices(api_key):
+    url = "https://api.coingecko.com/api/v3/simple/price"
+    params = {
+        "ids": "bitcoin,ethereum,binancecoin",
+        "vs_currencies": "usd",
+        "x_cg_demo_api_key": api_key
+    }
+    response = requests.get(url, params=params)
+    return response.json()
+```
+
+**💰 Value:** Real-time price data for your users
+
+---
+
+## 🔍 **ETHERSCAN API**
+
+*Ethereum blockchain data and transaction info*
+
+### **Step 1: Get Free API Key**
+
+1. **Visit:** https://etherscan.io/apis
+2. **Sign up** for free account
+3. **Go to API-KEYs** section
+4. **Create new API key**
+
+### **Step 2: Usage**
+
+```python
+# Etherscan API example
+import requests
+
+def get_eth_balance(address, api_key):
+    url = "https://api.etherscan.io/api"
+    params = {
+        "module": "account",
+        "action": "balance",
+        "address": address,
+        "tag": "latest",
+        "apikey": api_key
+    }
+    response = requests.get(url, params=params)
+    return response.json()
+```
+
+**💰 Value:** Track airdrop eligibility and transactions
+
+---
+
+## 🔶 **BINANCE API**
+
+*Crypto trading and price data*
+
+### **Step 1: Create Binance Account**
+
+1. **Visit:** https://www.binance.com/
+2. **Sign up** and verify account
+3. **Enable 2FA** for security
+
+### **Step 2: Create API Key**
+
+1. **Go to:** Account → API Management
+2. **Create API Key**
+3. **Set permissions:** Read only (for safety)
+4. **Save API Key and Secret**
+
+### **Step 3: Usage**
+
+```python
+# Binance API example
+import requests
+
+def get_binance_prices():
+    url = "https://api.binance.com/api/v3/ticker/price"
+    response = requests.get(url)
+    return response.json()
+```
+
+**💰 Value:** Real-time crypto prices and trading data
+
+---
+
+## 🟦 **COINBASE API**
+
+*Crypto prices and wallet integration*
+
+### **Step 1: Coinbase Developer Account**
+
+1. **Visit:** https://developers.coinbase.com/
+2. **Sign up** with your Coinbase account
+3. **Create new application**
+
+### **Step 2: Get API Credentials**
+
+1. **Go to:** My Applications
+2. **Create API Key**
+3. **Choose permissions:** Read only
+4. **Save API Key and Secret**
+
+### **Step 3: Implementation**
+
+```python
+# Coinbase API example
+import requests
+
+def get_coinbase_prices(api_key):
+    url = "https://api.coinbase.com/v2/exchange-rates"
+    headers = {"Authorization": f"Bearer {api_key}"}
+    response = requests.get(url, headers=headers)
+    return response.json()
+```
+
+---
+
+## 🌟 **ADDITIONAL APIS**
+
+### **Faucet APIs**
+
+1. **FreeBitco.in API**
+   - URL: https://freebitco.in/api/
+   - Usage: Auto-claim faucets
+
+2. **Moon Bitcoin API**
+   - URL: https://moonbitcoin.cash/faucet
+   - Usage: Automated claims
+
+### **Airdrop Monitoring**
+
+1. **AirdropAlert API**
+   - URL: https://airdropalert.com/
+   - Usage: New airdrop notifications
+
+2. **CoinMarketCap API**
+   - URL: https://coinmarketcap.com/api/
+   - Usage: Crypto data and airdrops
+
+---
+
+## 🧪 **TESTING YOUR APIS**
+
+### **Test Script**
+
+```python
+#!/usr/bin/env python3
+"""
+API Testing Script for Cash Hunters
+"""
+
+import requests
+from config import config
+
+def test_all_apis():
+    results = {}
+    
+    # Test CoinGecko
+    try:
+        response = requests.get(
+            "https://api.coingecko.com/api/v3/ping",
+            headers={"x_cg_demo_api_key": config.get_api_key('coingecko')}
+        )
+        results['coingecko'] = response.status_code == 200
+    except:
+        results['coingecko'] = False
+    
+    # Test Etherscan
+    try:
+        response = requests.get(
+            f"https://api.etherscan.io/api?module=stats&action=ethsupply&apikey={config.get_api_key('etherscan')}"
+        )
+        results['etherscan'] = response.status_code == 200
+    except:
+        results['etherscan'] = False
+    
+    # Test Binance
+    try:
+        response = requests.get("https://api.binance.com/api/v3/ping")
+        results['binance'] = response.status_code == 200
+    except:
+        results['binance'] = False
+    
+    return results
+
+if __name__ == "__main__":
+    print("🧪 Testing APIs...")
+    results = test_all_apis()
+    
+    for api, status in results.items():
+        status_emoji = "✅" if status else "❌"
+        print(f"{status_emoji} {api.upper()}: {'Connected' if status else 'Failed'}")
+```
+
+---
+
+## 📈 **EXPECTED EARNINGS**
+
+| API Source | Monthly Potential | Setup Difficulty |
+|------------|------------------|------------------|
+| Rakuten | $50-500 | Medium |
+| Amazon | $100-1000 | Medium |
+| CoinGecko | Free (Data) | Easy |
+| Etherscan | Free (Data) | Easy |
+| Binance | Free (Data) | Easy |
+| Coinbase | Free (Data) | Easy |
+| **TOTAL** | **$150-1500+** | - |
+
+---
+
+## 🚨 **IMPORTANT NOTES**
+
+1. **Keep API keys secure** - Never share or commit to git
+2. **Respect rate limits** - Don't spam API calls
+3. **Read terms of service** - Follow each platform's rules
+4. **Start with free tiers** - Upgrade as you earn
+5. **Monitor usage** - Track API call limits
+
+---
+
+## 🆘 **SUPPORT**
+
+If you need help with API setup:
+
+1. **Check documentation** for each service
+2. **Join Telegram support** groups
+3. **Contact API support** directly
+4. **Search Stack Overflow** for solutions
+
+---
+
+**💡 Pro Tip:** Start with the free APIs (CoinGecko, Etherscan) to test your bot, then add the earning APIs (Rakuten, Amazon) once everything works!
