diff --git a/CashHuntingbot_improved.py b/CashHuntingbot_improved.py
--- a/CashHuntingbot_improved.py
+++ b/CashHuntingbot_improved.py
@@ -0,0 +1,654 @@
+#!/usr/bin/env python3
+"""
+CASH HUNTERS - MASTER BOT (IMPROVED VERSION)
+"Command and conquer the crypto world"
+👑💰 MASTER CONTROL + PERSONAL EARNINGS 💰👑
+"""
+
+import asyncio
+import random
+import json
+import os
+import logging
+from datetime import datetime, timedelta
+from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
+from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
+from config import config
+
+# Setup logging
+logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
+logger = logging.getLogger(__name__)
+
+# MASTER DATA
+master_data = {
+    'personal_earnings': 0.0,
+    'network_commissions': 0.0,
+    'subscription_revenue': 0.0,
+    'active_bots': 0,
+    'total_users': 0,
+    'api_connections': {},
+    'daily_stats': []
+}
+
+network_bots = {}  # Track all bots in your network
+commission_queue = []  # Pending commissions
+
+class MasterCashEngine:
+    def __init__(self):
+        self.name = "Master Cash Engine"
+        self.commission_rate = config.MASTER_COMMISSION_RATE
+        self.subscription_plans = config.PREMIUM_PLANS
+    
+    def calculate_personal_earnings(self):
+        """Calculate your direct earnings"""
+        # Simulate personal crypto activities
+        airdrops = random.uniform(100, 500)
+        faucets = random.uniform(10, 50)
+        cashback = random.uniform(25, 150)
+        api_profits = random.uniform(50, 200)
+        
+        return {
+            'airdrops': airdrops,
+            'faucets': faucets,
+            'cashback': cashback,
+            'api_profits': api_profits,
+            'total': airdrops + faucets + cashback + api_profits
+        }
+    
+    def calculate_network_commissions(self):
+        """Calculate commissions from your bot network"""
+        bot_earnings = random.uniform(200, 800)  # From viral bot
+        sub_network = random.uniform(100, 400)   # From sub-bots
+        referral_bonuses = random.uniform(50, 200)
+        
+        your_commission = (bot_earnings + sub_network) * self.commission_rate
+        
+        return {
+            'bot_earnings': bot_earnings,
+            'sub_network': sub_network,
+            'referral_bonuses': referral_bonuses,
+            'your_commission': your_commission,
+            'total': your_commission + referral_bonuses
+        }
+    
+    def get_subscription_revenue(self):
+        """Calculate subscription income"""
+        subscribers = random.randint(10, 50)
+        plans = list(self.subscription_plans.keys())
+        avg_plan = random.choice(plans)
+        monthly_revenue = subscribers * self.subscription_plans[avg_plan]['price']
+        
+        return {
+            'subscribers': subscribers,
+            'avg_plan': avg_plan,
+            'monthly_revenue': monthly_revenue
+        }
+    
+    def get_api_status(self):
+        """Check API connections status"""
+        apis = {}
+        for service in config.API_KEYS.keys():
+            api_key = config.get_api_key(service)
+            apis[service] = bool(api_key and api_key != 'your_' + service + '_api_key')
+        
+        return apis
+
+# Initialize master engine
+cash_engine = MasterCashEngine()
+
+async def admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    user_id = update.effective_user.id
+    
+    # Check if user is admin
+    if not config.is_admin(user_id):
+        await update.message.reply_text("🚫 **ACCESS DENIED** - This is a private bot.", parse_mode='Markdown')
+        return
+    
+    # Calculate current earnings
+    personal = cash_engine.calculate_personal_earnings()
+    network = cash_engine.calculate_network_commissions()
+    subscriptions = cash_engine.get_subscription_revenue()
+    
+    # Update master data
+    master_data['personal_earnings'] += personal['total']
+    master_data['network_commissions'] += network['total']
+    master_data['subscription_revenue'] += subscriptions['monthly_revenue']
+    
+    total_income = personal['total'] + network['total'] + subscriptions['monthly_revenue']
+    
+    msg = f"""👑 **MASTER CONTROL DASHBOARD** 👑
+
+💰 **TODAY'S EARNINGS:**
+🎯 Personal: ${personal['total']:.2f}
+🌐 Network: ${network['total']:.2f}
+💳 Subscriptions: ${subscriptions['monthly_revenue']:.2f}
+💎 **TOTAL TODAY: ${total_income:.2f}**
+
+📊 **EMPIRE STATUS:**
+🤖 Active Bots: {master_data['active_bots']}
+👥 Total Users: {master_data['total_users']}
+📈 Growth Rate: +{random.randint(5,15)}% daily
+
+💵 **LIFETIME TOTALS:**
+💰 Personal: ${master_data['personal_earnings']:.2f}
+🏦 Network: ${master_data['network_commissions']:.2f}
+💳 Subscriptions: ${master_data['subscription_revenue']:.2f}
+
+⏰ **Last Update:** {datetime.now().strftime('%H:%M:%S')}"""
+
+    # Main navigation keyboard
+    kb = [
+        [
+            InlineKeyboardButton("💰 Personal", callback_data='personal'),
+            InlineKeyboardButton("🌐 Network", callback_data='network')
+        ],
+        [
+            InlineKeyboardButton("🔧 APIs", callback_data='apis'),
+            InlineKeyboardButton("💸 Payouts", callback_data='payouts')
+        ],
+        [
+            InlineKeyboardButton("📊 Analytics", callback_data='analytics'),
+            InlineKeyboardButton("⚙️ Settings", callback_data='settings')
+        ],
+        [
+            InlineKeyboardButton("📖 API Setup Guide", callback_data='api_guide'),
+            InlineKeyboardButton("🆘 Help", callback_data='help')
+        ]
+    ]
+    
+    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def personal_earnings(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    earnings = cash_engine.calculate_personal_earnings()
+    
+    msg = f"""💰 **YOUR PERSONAL CASH MACHINE** 💰
+
+**TODAY'S DIRECT EARNINGS:**
+🪂 Airdrops: ${earnings['airdrops']:.2f}
+💧 Faucets: ${earnings['faucets']:.2f}
+💳 Cashback: ${earnings['cashback']:.2f}
+🔌 API Profits: ${earnings['api_profits']:.2f}
+
+💎 **TOTAL PERSONAL: ${earnings['total']:.2f}**
+
+**ACTIVE SOURCES:**
+✅ LayerZero airdrop: $200 pending
+✅ Rakuten cashback: 5% active
+✅ Bitcoin faucets: 12 active
+✅ Amazon affiliates: $150/week avg
+
+**OPTIMIZATION TIPS:**
+• Set up 5 more wallets (+$50/week)
+• Add 3 more affiliate programs (+$100/week)
+• Automate faucet claims (+$20/week)
+
+**NEXT ACTIONS:**
+• Check airdrop deadlines
+• Claim daily faucets
+• Review cashback opportunities"""
+
+    kb = [
+        [
+            InlineKeyboardButton("🪂 Manage Airdrops", callback_data='manage_airdrops'),
+            InlineKeyboardButton("💳 Cashback Setup", callback_data='cashback_setup')
+        ],
+        [
+            InlineKeyboardButton("🤖 Automation", callback_data='automation'),
+            InlineKeyboardButton("📊 Detailed Stats", callback_data='personal_stats')
+        ],
+        [
+            InlineKeyboardButton("🔄 Refresh Data", callback_data='personal'),
+            InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
+        ]
+    ]
+    
+    if hasattr(update, 'callback_query') and update.callback_query:
+        await update.callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+    else:
+        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def network_overview(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    network = cash_engine.calculate_network_commissions()
+    
+    # Simulate network stats
+    bots_created = random.randint(15, 50)
+    active_users = random.randint(100, 500)
+    daily_growth = random.randint(5, 25)
+    
+    msg = f"""🌐 **YOUR BOT NETWORK EMPIRE** 🌐
+
+**NETWORK EARNINGS:**
+🤖 Bot Commissions: ${network['your_commission']:.2f}
+👥 Referral Bonuses: ${network['referral_bonuses']:.2f}
+🎯 **TOTAL NETWORK: ${network['total']:.2f}**
+
+**EMPIRE STATS:**
+🤖 Bots Created: {bots_created}
+👥 Active Users: {active_users}
+📈 Daily Growth: +{daily_growth} users
+💰 Avg. Commission/User: ${network['total']/active_users:.2f}
+
+**TOP PERFORMING BOTS:**
+🥇 AirdropHunter_v2: {random.randint(50,150)} users, ${random.randint(20,80)}/day
+🥈 CashMachine_Pro: {random.randint(30,100)} users, ${random.randint(15,50)}/day
+🥉 CryptoFarmer_AI: {random.randint(20,80)} users, ${random.randint(10,40)}/day
+
+**COMMISSION BREAKDOWN:**
+• Direct bot earnings: {config.MASTER_COMMISSION_RATE*100:.0f}%
+• Sub-network: 5%
+• Referral bonuses: ${config.REFERRAL_BONUS}/each
+• Premium subscriptions: $19-79/month"""
+
+    kb = [
+        [
+            InlineKeyboardButton("📊 Detailed Stats", callback_data='detailed_stats'),
+            InlineKeyboardButton("🚀 Growth Tools", callback_data='growth_tools')
+        ],
+        [
+            InlineKeyboardButton("💎 Premium Features", callback_data='premium_features'),
+            InlineKeyboardButton("🤖 Create New Bot", callback_data='create_new_bot')
+        ],
+        [
+            InlineKeyboardButton("🔄 Refresh Network", callback_data='network'),
+            InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
+        ]
+    ]
+    
+    if hasattr(update, 'callback_query') and update.callback_query:
+        await update.callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+    else:
+        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def api_management(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    api_status = cash_engine.get_api_status()
+    
+    # Count connected APIs
+    connected_count = sum(1 for status in api_status.values() if status)
+    total_count = len(api_status)
+    
+    msg = f"""🔧 **API MANAGEMENT CENTER** 🔧
+
+**CONNECTION STATUS ({connected_count}/{total_count}):**"""
+    
+    # Add status for each API
+    for api_name, is_connected in api_status.items():
+        status_emoji = '🟢' if is_connected else '🔴'
+        status_text = 'Connected' if is_connected else 'Not configured'
+        msg += f"\n{status_emoji} {api_name.title()}: {status_text}"
+    
+    msg += f"""
+
+**API EARNINGS TODAY:**
+💳 Rakuten: $45.20 (142 transactions)
+🛒 Amazon: $67.80 (23 sales)
+💧 Faucets: $12.40 (Auto-claims)
+🪂 Airdrops: $89.60 (Monitoring)
+
+**API PERFORMANCE:**
+📊 Uptime: 99.2%
+⚡ Response Time: 145ms avg
+💰 Revenue/API Call: $0.23
+🔄 Daily Requests: 15,847
+
+**QUICK SETUP:**
+Missing APIs? Use our setup guide to get started in minutes!"""
+
+    kb = [
+        [
+            InlineKeyboardButton("📖 API Setup Guide", callback_data='api_guide'),
+            InlineKeyboardButton("🧪 Test All APIs", callback_data='test_apis')
+        ],
+        [
+            InlineKeyboardButton("🔑 Add New API", callback_data='add_api'),
+            InlineKeyboardButton("📈 API Analytics", callback_data='api_analytics')
+        ],
+        [
+            InlineKeyboardButton("⚙️ API Settings", callback_data='api_settings'),
+            InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
+        ]
+    ]
+    
+    if hasattr(update, 'callback_query') and update.callback_query:
+        await update.callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+    else:
+        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def api_setup_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    """Show API setup guide with direct links"""
+    
+    msg = f"""📖 **API SETUP GUIDE** 📖
+
+**QUICK START APIS (FREE):**
+🪙 CoinGecko - Crypto prices
+🔍 Etherscan - Blockchain data
+🔶 Binance - Trading data
+
+**EARNING APIS (PAID):**
+💳 Rakuten - Cashback ($50-500/month)
+🛒 Amazon - Affiliates ($100-1000/month)
+
+**SETUP DIFFICULTY:**
+🟢 Easy: CoinGecko, Etherscan, Binance
+🟡 Medium: Rakuten, Amazon, Coinbase
+🔴 Advanced: Custom faucet APIs
+
+**ESTIMATED SETUP TIME:**
+• Free APIs: 5-10 minutes each
+• Earning APIs: 30-60 minutes each
+• Full setup: 2-4 hours total
+
+**EARNING POTENTIAL:**
+💰 Monthly: $150-1500+
+🚀 Scaling: Unlimited with more users
+
+**NEXT STEPS:**
+1. Start with free APIs for testing
+2. Add earning APIs once working
+3. Scale with more bot users
+4. Monitor and optimize regularly"""
+
+    kb = [
+        [
+            InlineKeyboardButton("🤖 Telegram Bot Setup", callback_data='telegram_setup'),
+            InlineKeyboardButton("💳 Rakuten Setup", callback_data='rakuten_setup')
+        ],
+        [
+            InlineKeyboardButton("🛒 Amazon Setup", callback_data='amazon_setup'),
+            InlineKeyboardButton("🪙 Crypto APIs", callback_data='crypto_setup')
+        ],
+        [
+            InlineKeyboardButton("📋 Full Guide (External)", url='https://github.com/05Z3r0C0d3/Cash-Hunters/blob/main/API_SETUP_GUIDE.md'),
+        ],
+        [
+            InlineKeyboardButton("🔄 Back to APIs", callback_data='apis'),
+            InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
+        ]
+    ]
+    
+    if hasattr(update, 'callback_query') and update.callback_query:
+        await update.callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+    else:
+        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def telegram_setup_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    """Detailed Telegram bot setup"""
+    
+    msg = f"""🤖 **TELEGRAM BOT SETUP** 🤖
+
+**STEP 1: Create Master Bot**
+1. Message @BotFather
+2. Send `/newbot`
+3. Name: `YourName Cash Master`
+4. Username: `yournamemaster_bot`
+5. Copy token → MASTER_BOT_TOKEN
+
+**STEP 2: Create Public Bot**  
+1. Send `/newbot` again
+2. Name: `YourName Flash Cash`
+3. Username: `yournameflash_bot`
+4. Copy token → PUBLIC_BOT_TOKEN
+
+**STEP 3: Get Your User ID**
+1. Message @userinfobot
+2. Copy your User ID
+3. Use as ADMIN_ID in .env
+
+**STEP 4: Bot Settings**
+```
+/setdescription - Set bot description
+/setabouttext - Set about text  
+/setuserpic - Upload bot avatar
+/setcommands - Set bot commands
+```
+
+**STEP 5: Test Connection**
+Send `/start` to both bots to verify they work.
+
+**⚠️ SECURITY:**
+• Never share bot tokens
+• Use environment variables
+• Enable 2FA on Telegram"""
+
+    kb = [
+        [
+            InlineKeyboardButton("📱 Open @BotFather", url='https://t.me/BotFather'),
+            InlineKeyboardButton("🆔 Get User ID", url='https://t.me/userinfobot')
+        ],
+        [
+            InlineKeyboardButton("🔄 Back to Guide", callback_data='api_guide'),
+            InlineKeyboardButton("➡️ Next: Rakuten", callback_data='rakuten_setup')
+        ]
+    ]
+    
+    await update.callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def rakuten_setup_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    """Detailed Rakuten setup"""
+    
+    msg = f"""💳 **RAKUTEN ADVERTISING SETUP** 💳
+
+**💰 EARNING POTENTIAL: $50-500/month**
+
+**STEP 1: Publisher Application**
+1. Visit advertising.rakuten.com
+2. Click "Join Now" → "Publisher"
+3. Fill application form:
+   • Website: Your Telegram channel
+   • Traffic: Social Media/Telegram
+   • Monthly visitors: 1000+
+
+**STEP 2: Get Approved (1-7 days)**
+• Create active Telegram channel first
+• Post crypto/cashback content
+• Show engagement (likes, comments)
+
+**STEP 3: API Access**
+1. Login to dashboard
+2. Tools → API section
+3. Request API access
+4. Get API credentials
+
+**STEP 4: Integration**
+• Add API key to .env file
+• Test with sample requests
+• Monitor earnings in dashboard
+
+**💡 PRO TIPS:**
+• Start with free tier
+• Focus on cashback offers
+• Promote to your bot users
+• Scale with more channels"""
+
+    kb = [
+        [
+            InlineKeyboardButton("🔗 Join Rakuten", url='https://advertising.rakuten.com/'),
+            InlineKeyboardButton("📊 View Dashboard", url='https://advertising.rakuten.com/publishers/dashboard')
+        ],
+        [
+            InlineKeyboardButton("⬅️ Back: Telegram", callback_data='telegram_setup'),
+            InlineKeyboardButton("➡️ Next: Amazon", callback_data='amazon_setup')
+        ]
+    ]
+    
+    await update.callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def payout_center(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    available = master_data['personal_earnings'] + master_data['network_commissions']
+    pending = random.uniform(100, 500)
+    
+    msg = f"""💸 **MASTER PAYOUT CENTER** 💸
+
+💰 **AVAILABLE FOR WITHDRAWAL:**
+💎 Total Available: ${available:.2f}
+⏳ Pending: ${pending:.2f}
+🏦 Last Payout: ${random.randint(200,800)} (Aug 10)
+
+**WITHDRAWAL METHODS:**
+💳 PayPal: Instant (2% fee)
+🏦 Bank Transfer: 1-2 days (Free)
+₿ Crypto Wallet: 5 mins ($3 fee)
+🎁 Gift Cards: Instant (Free)
+
+**PAYOUT SCHEDULE:**
+📅 Weekly: Every Friday 5PM
+💰 Minimum: $50.00
+⚡ Express: Available 24/7 (+$5 fee)
+
+**THIS WEEK'S EARNINGS:**
+Mon: $127.45 | Tue: $89.20 | Wed: $156.80
+Thu: $203.15 | Fri: $178.90 | Sat: $145.60
+Sun: $98.30
+
+💎 **WEEKLY TOTAL: $999.40**
+
+**RECENT PAYOUTS:**
+Aug 10: $756.20 → PayPal ✅
+Aug 3: $623.80 → Bank ✅  
+Jul 27: $891.45 → Crypto ✅"""
+
+    kb = [
+        [
+            InlineKeyboardButton("💸 Withdraw Now", callback_data='withdraw_now'),
+            InlineKeyboardButton("⚙️ Payout Settings", callback_data='payout_settings')
+        ],
+        [
+            InlineKeyboardButton("📊 Tax Reports", callback_data='tax_reports'),
+            InlineKeyboardButton("📈 Earnings History", callback_data='earnings_history')
+        ],
+        [
+            InlineKeyboardButton("🔄 Refresh Balance", callback_data='payouts'),
+            InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
+        ]
+    ]
+    
+    if hasattr(update, 'callback_query') and update.callback_query:
+        await update.callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+    else:
+        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    query = update.callback_query
+    await query.answer()
+    
+    user_id = query.from_user.id
+    
+    # Check admin access for all callbacks
+    if not config.is_admin(user_id):
+        await query.edit_message_text("🚫 **ACCESS DENIED** - This is a private bot.", parse_mode='Markdown')
+        return
+    
+    # Main navigation
+    if query.data == 'main_menu':
+        await admin_start(query, context)
+    elif query.data == 'personal':
+        await personal_earnings(query, context)
+    elif query.data == 'network':
+        await network_overview(query, context)
+    elif query.data == 'apis':
+        await api_management(query, context)
+    elif query.data == 'payouts':
+        await payout_center(query, context)
+    
+    # API Guide navigation
+    elif query.data == 'api_guide':
+        await api_setup_guide(query, context)
+    elif query.data == 'telegram_setup':
+        await telegram_setup_guide(query, context)
+    elif query.data == 'rakuten_setup':
+        await rakuten_setup_guide(query, context)
+    
+    # Withdrawal simulation
+    elif query.data == 'withdraw_now':
+        amount = random.uniform(200, 800)
+        
+        success_msg = f"""✅ **WITHDRAWAL PROCESSED!**
+
+💰 **Amount:** ${amount:.2f}
+📧 **Method:** PayPal
+⏰ **Processing:** 1-2 hours
+📄 **Transaction ID:** TXN{random.randint(100000,999999)}
+
+💡 **What's next:**
+• Check PayPal for incoming payment
+• Continue earning with active bots
+• Weekly payout scheduled for Friday
+
+🎯 **Keep building your empire!**
+Your network is generating ${random.randint(50,150)}/day"""
+        
+        kb = [
+            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')],
+            [InlineKeyboardButton("📊 View Earnings", callback_data='personal')]
+        ]
+        
+        await query.edit_message_text(success_msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+    
+    # Help section
+    elif query.data == 'help':
+        help_msg = f"""🆘 **CASH HUNTERS HELP CENTER** 🆘
+
+**QUICK COMMANDS:**
+/start - Main dashboard
+/personal - Personal earnings
+/network - Network overview
+/apis - API management
+/payouts - Withdrawal center
+
+**GETTING STARTED:**
+1. Set up your APIs using the guide
+2. Configure your .env file
+3. Launch your public bot
+4. Share and grow your network
+
+**SUPPORT CHANNELS:**
+📧 Email: support@cashhunters.com
+💬 Telegram: @cashhunters_support
+📚 Docs: github.com/05Z3r0C0d3/Cash-Hunters
+
+**TROUBLESHOOTING:**
+• Bot not responding → Check tokens
+• APIs failing → Verify keys
+• No earnings → Check connections
+• Commission issues → Restart bots"""
+
+        kb = [
+            [InlineKeyboardButton("📖 Full Documentation", url='https://github.com/05Z3r0C0d3/Cash-Hunters')],
+            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
+        ]
+        
+        await query.edit_message_text(help_msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+def main():
+    print("👑 CASH HUNTERS - MASTER BOT (IMPROVED) starting...")
+    print("💰 Your personal cash machine + empire control!")
+    
+    # Validate configuration
+    try:
+        if not config.MASTER_BOT_TOKEN:
+            raise ValueError("MASTER_BOT_TOKEN not configured")
+        if not config.ADMIN_ID:
+            raise ValueError("ADMIN_ID not configured")
+    except Exception as e:
+        print(f"❌ Configuration error: {e}")
+        print("💡 Please check your .env file and API_SETUP_GUIDE.md")
+        return
+    
+    app = Application.builder().token(config.MASTER_BOT_TOKEN).build()
+    
+    # Admin commands
+    app.add_handler(CommandHandler("start", admin_start))
+    app.add_handler(CommandHandler("personal", personal_earnings))
+    app.add_handler(CommandHandler("network", network_overview))
+    app.add_handler(CommandHandler("apis", api_management))
+    app.add_handler(CommandHandler("payouts", payout_center))
+    app.add_handler(CallbackQueryHandler(button_handler))
+    
+    print("🔥 MASTER BOT IS LIVE!")
+    print("👑 Your empire control center activated!")
+    print(f"💰 Ready to generate serious money!")
+    print(f"🔧 Admin ID: {config.ADMIN_ID}")
+    
+    app.run_polling()
+
+if __name__ == '__main__':
+    main()
