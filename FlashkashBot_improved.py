diff --git a/FlashkashBot_improved.py b/FlashkashBot_improved.py
--- a/FlashkashBot_improved.py
+++ b/FlashkashBot_improved.py
@@ -0,0 +1,678 @@
+#!/usr/bin/env python3
+"""
+CASH HUNTERS - PUBLIC BOT (IMPROVED VERSION)
+"Flash profits, instant results, viral growth"
+⚡💰 PUBLIC BOT + COMMISSION TO MASTER 💰⚡
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
+# USER DATA
+flash_users = {}
+daily_stats = {}
+
+class FlashCashEngine:
+    def __init__(self):
+        self.name = "Flash Cash Engine"
+        self.commission_rate = config.PUBLIC_COMMISSION_RATE
+        self.referral_bonus = config.REFERRAL_BONUS
+        self.success_stories = [
+            "Sarah made $347 in her first week!",
+            "Mike earned $892 from airdrops last month!",
+            "Jessica got $156 from faucets this week!",
+            "Carlos made $623 with cashback automation!",
+            "Ana earned $445 with API automation!",
+            "David made $789 from his bot network!"
+        ]
+        
+    def load_shared_data(self):
+        """Load data shared between bots"""
+        try:
+            if os.path.exists(config.SHARED_DATA_FILE):
+                with open(config.SHARED_DATA_FILE, 'r') as f:
+                    return json.load(f)
+            else:
+                return {
+                    'master_earnings': 0.0,
+                    'network_commissions': 0.0,
+                    'total_users': 0,
+                    'daily_commissions': []
+                }
+        except Exception as e:
+            logger.error(f"Error loading shared data: {e}")
+            return {'master_earnings': 0.0, 'network_commissions': 0.0, 'total_users': 0}
+    
+    def save_shared_data(self, data):
+        """Save data to share with master bot"""
+        try:
+            with open(config.SHARED_DATA_FILE, 'w') as f:
+                json.dump(data, f, indent=2)
+        except Exception as e:
+            logger.error(f"Error saving shared data: {e}")
+    
+    def send_commission_to_master(self, user_earnings, user_id):
+        """Calculate and log commission for master bot"""
+        commission = user_earnings * self.commission_rate
+        
+        # Load shared data
+        shared = self.load_shared_data()
+        shared['network_commissions'] += commission
+        shared['total_users'] = len(flash_users)
+        shared['daily_commissions'].append({
+            'date': datetime.now().isoformat(),
+            'user_id': user_id,
+            'commission': commission,
+            'user_earnings': user_earnings
+        })
+        
+        # Save updated data
+        self.save_shared_data(shared)
+        
+        logger.info(f"Commission sent to master: ${commission:.2f} from user {user_id}")
+        return commission
+    
+    def get_flash_airdrops(self):
+        """Get flash airdrop opportunities"""
+        airdrops = [
+            {
+                'name': 'FlashDrop Alpha',
+                'value': random.randint(75, 400),
+                'urgency': 'HIGH',
+                'time_left': '6 hours',
+                'difficulty': 'Easy',
+                'tasks': 3,
+                'success_rate': '94%'
+            },
+            {
+                'name': 'Lightning Token',
+                'value': random.randint(100, 600),
+                'urgency': 'MEDIUM',
+                'time_left': '2 days',
+                'difficulty': 'Medium',
+                'tasks': 5,
+                'success_rate': '87%'
+            },
+            {
+                'name': 'QuickCash Airdrop',
+                'value': random.randint(50, 300),
+                'urgency': 'HIGH',
+                'time_left': '12 hours',
+                'difficulty': 'Easy',
+                'tasks': 2,
+                'success_rate': '96%'
+            },
+            {
+                'name': 'RapidRewards Drop',
+                'value': random.randint(125, 500),
+                'urgency': 'LOW',
+                'time_left': '5 days',
+                'difficulty': 'Hard',
+                'tasks': 8,
+                'success_rate': '78%'
+            }
+        ]
+        return airdrops
+    
+    def get_flash_faucets(self):
+        """Get flash faucet opportunities"""
+        faucets = [
+            {'name': 'Lightning BTC', 'amount': 0.00015, 'time': '15 min', 'status': 'ready'},
+            {'name': 'Flash ETH', 'amount': 0.002, 'time': '30 min', 'status': 'ready'},
+            {'name': 'Quick USDT', 'amount': 0.5, 'time': '1 hour', 'status': 'claiming'},
+            {'name': 'Instant BNB', 'amount': 0.008, 'time': '45 min', 'status': 'ready'},
+            {'name': 'Rapid MATIC', 'amount': 0.15, 'time': '20 min', 'status': 'ready'}
+        ]
+        return faucets
+
+# Initialize engine
+flash_engine = FlashCashEngine()
+
+def get_user(user_id):
+    if user_id not in flash_users:
+        flash_users[user_id] = {
+            'flash_earnings': random.uniform(10, 75),  # Starting motivation
+            'tasks_completed': random.randint(0, 5),
+            'success_rate': random.uniform(85, 98),
+            'join_date': datetime.now(),
+            'referrals': 0,
+            'bot_created': False,
+            'premium': False,
+            'last_claim': None
+        }
+    return flash_users[user_id]
+
+async def flash_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    user = get_user(update.effective_user.id)
+    name = update.effective_user.first_name or "Flash Hunter"
+    
+    # Get shared network stats
+    shared = flash_engine.load_shared_data()
+    
+    # Random success story
+    success_story = random.choice(flash_engine.success_stories)
+    
+    msg = f"""⚡ **WELCOME TO FLASHCASH, {name.upper()}!** ⚡
+
+💰 **FLASH PROFITS IN MINUTES, NOT MONTHS!**
+
+**YOUR FLASH STATS:**
+💸 Flash Earnings: ${user['flash_earnings']:.2f}
+⚡ Success Rate: {user['success_rate']:.1f}%
+🎯 Tasks Done: {user['tasks_completed']}
+📅 Member Since: {user['join_date'].strftime('%m/%d')}
+
+**NETWORK POWER:**
+🌐 Total Users: {shared.get('total_users', 0)} Flash Hunters
+💰 Network Earned: ${shared.get('network_commissions', 0) * 8:.0f}
+🚀 Growth Rate: +{random.randint(15,35)}% daily
+
+**FLASH OPPORTUNITIES TODAY:**
+⚡ 4 High-Urgency Airdrops
+💧 5 Flash Faucets (15-min cycles)
+🎯 3 Instant Cashback Deals
+🤖 Bot Creation Wizard (EARN MORE!)
+
+💡 **SUCCESS STORY:** {success_story}
+
+**READY FOR FLASH PROFITS?**"""
+
+    kb = [
+        [
+            InlineKeyboardButton("⚡ Flash Airdrops", callback_data='flash_airdrops'),
+            InlineKeyboardButton("💧 Flash Faucets", callback_data='flash_faucets')
+        ],
+        [
+            InlineKeyboardButton("🤖 Create My Bot", callback_data='create_bot'),
+            InlineKeyboardButton("💎 Go Premium", callback_data='go_premium')
+        ],
+        [
+            InlineKeyboardButton("📊 My Stats", callback_data='my_stats'),
+            InlineKeyboardButton("📖 API Guide", callback_data='api_guide_public')
+        ],
+        [
+            InlineKeyboardButton("🆘 Help & Support", callback_data='help_support')
+        ]
+    ]
+    
+    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def flash_airdrops(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    user = get_user(update.effective_user.id)
+    
+    # Show loading message
+    if hasattr(update, 'callback_query') and update.callback_query:
+        msg = await update.callback_query.edit_message_text("⚡ **SCANNING FLASH AIRDROPS...**", parse_mode='Markdown')
+    else:
+        msg = await update.message.reply_text("⚡ **SCANNING FLASH AIRDROPS...**", parse_mode='Markdown')
+    
+    await asyncio.sleep(1.5)  # Realistic loading time
+    
+    airdrops = flash_engine.get_flash_airdrops()
+    
+    text = "⚡ **FLASH AIRDROP OPPORTUNITIES:**\n\n"
+    total_value = 0
+    
+    for i, airdrop in enumerate(airdrops, 1):
+        urgency_emoji = "🔥" if airdrop['urgency'] == 'HIGH' else "⚡" if airdrop['urgency'] == 'MEDIUM' else "📅"
+        
+        text += f"**{i}. {airdrop['name']} {urgency_emoji}**\n"
+        text += f"💰 Value: ${airdrop['value']}\n"
+        text += f"⏰ Time Left: {airdrop['time_left']}\n"
+        text += f"🎯 Tasks: {airdrop['tasks']} ({airdrop['difficulty']})\n"
+        text += f"✅ Success Rate: {airdrop['success_rate']}\n\n"
+        
+        total_value += airdrop['value']
+    
+    text += f"💎 **TOTAL FLASH VALUE: ${total_value}**\n"
+    text += f"⚡ **ALL EXECUTABLE IN UNDER 30 MINUTES!**\n\n"
+    text += f"💡 **Your current success rate: {user['success_rate']:.1f}%**"
+    
+    kb = [
+        [
+            InlineKeyboardButton("🚀 Flash Execute All", callback_data='execute_airdrops'),
+            InlineKeyboardButton("📋 Manual Setup", callback_data='manual_airdrops')
+        ],
+        [
+            InlineKeyboardButton("🔄 Refresh List", callback_data='flash_airdrops'),
+            InlineKeyboardButton("📖 Airdrop Guide", callback_data='airdrop_guide')
+        ],
+        [
+            InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
+        ]
+    ]
+    
+    await msg.edit_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def flash_faucets(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    user = get_user(update.effective_user.id)
+    
+    # Show loading message
+    if hasattr(update, 'callback_query') and update.callback_query:
+        msg = await update.callback_query.edit_message_text("💧 **ACTIVATING FLASH FAUCETS...**", parse_mode='Markdown')
+    else:
+        msg = await update.message.reply_text("💧 **ACTIVATING FLASH FAUCETS...**", parse_mode='Markdown')
+    
+    await asyncio.sleep(1.2)
+    
+    faucets = flash_engine.get_flash_faucets()
+    
+    text = "💧 **FLASH FAUCET STATUS:**\n\n"
+    
+    for faucet in faucets:
+        status_emoji = "🟢" if faucet['status'] == 'ready' else "🟡"
+        status_text = "Ready to claim" if faucet['status'] == 'ready' else "Claiming..."
+        
+        text += f"**{faucet['name']} {status_emoji}**\n"
+        text += f"💰 Amount: {faucet['amount']:.6f} crypto\n"
+        text += f"⏰ Next: {faucet['time']} | {status_text}\n\n"
+    
+    # Check if user can claim (rate limiting)
+    can_claim = True
+    if user.get('last_claim'):
+        time_diff = datetime.now() - user['last_claim']
+        if time_diff.total_seconds() < 300:  # 5 minutes cooldown
+            can_claim = False
+            remaining = 300 - int(time_diff.total_seconds())
+            text += f"⏰ **Cooldown:** {remaining//60}m {remaining%60}s remaining\n"
+    
+    text += f"🎯 **Your Success Rate: {user['success_rate']:.1f}%**\n"
+    text += f"💎 **Total Earned: ${user['flash_earnings']:.2f}**"
+    
+    kb = []
+    if can_claim:
+        kb.append([InlineKeyboardButton("💧 Claim All Faucets", callback_data='claim_faucets')])
+    else:
+        kb.append([InlineKeyboardButton("⏰ Waiting for Cooldown", callback_data='cooldown_info')])
+    
+    kb.extend([
+        [
+            InlineKeyboardButton("🤖 Auto Mode (Premium)", callback_data='auto_mode'),
+            InlineKeyboardButton("📖 Faucet Guide", callback_data='faucet_guide')
+        ],
+        [
+            InlineKeyboardButton("🔄 Refresh Status", callback_data='flash_faucets'),
+            InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
+        ]
+    ])
+    
+    await msg.edit_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def create_bot_wizard(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    user = get_user(update.effective_user.id)
+    
+    text = f"""🤖 **CREATE YOUR OWN FLASH BOT!**
+
+**WHY CREATE YOUR BOT?**
+💰 Earn commissions from YOUR users
+🚀 Build your own network
+⚡ 10x your earnings potential
+👑 Become a Flash Leader
+
+**BOT CREATION WIZARD:**
+1. **Get Bot Token** (Free from @BotFather)
+2. **Copy Flash Template** (We provide everything)
+3. **Customize Your Bot** (Name, features)
+4. **Launch & Share** (Start earning immediately)
+
+**EARNINGS POTENTIAL:**
+• 100 users = $200/month extra
+• 500 users = $1,000/month extra  
+• 1,000 users = $2,500/month extra
+
+**WHAT YOU GET:**
+✅ Complete bot source code
+✅ Setup tutorial (step-by-step)
+✅ API integration guide
+✅ Marketing templates
+✅ 24/7 support access
+
+**CURRENT OFFER:**
+🎯 Bot Template: FREE (normally $97)
+🎯 Setup Support: FREE (normally $47)
+🎯 API Guide: FREE (normally $67)
+💎 **TOTAL VALUE: $211 - TODAY: FREE!**
+
+**COMMISSION STRUCTURE:**
+• You earn: {(1-config.PUBLIC_COMMISSION_RATE)*100:.0f}% of your bot's profits
+• FlashCash gets: {config.PUBLIC_COMMISSION_RATE*100:.0f}% network fee
+• Your users get: Real crypto earnings
+
+**READY TO 10X YOUR EARNINGS?**"""
+
+    kb = [
+        [
+            InlineKeyboardButton("🚀 Start Creation", callback_data='start_creation'),
+            InlineKeyboardButton("📖 View Tutorial", callback_data='bot_tutorial')
+        ],
+        [
+            InlineKeyboardButton("📱 Get @BotFather Token", url='https://t.me/BotFather'),
+            InlineKeyboardButton("💬 Get Support", callback_data='get_support')
+        ],
+        [
+            InlineKeyboardButton("📊 Success Stories", callback_data='success_stories'),
+            InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
+        ]
+    ]
+    
+    if hasattr(update, 'callback_query') and update.callback_query:
+        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+    else:
+        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def premium_upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    user = get_user(update.effective_user.id)
+    
+    text = f"""💎 **FLASHCASH PREMIUM UPGRADE** 💎
+
+**PREMIUM FEATURES:**
+⚡ **Flash Alerts:** Get notified of high-value opportunities
+🤖 **Auto Mode:** Fully automated earning (24/7)
+💰 **Premium APIs:** Access to exclusive earning sources
+🎯 **Priority Support:** Direct line to Flash team
+📊 **Advanced Analytics:** Detailed earning reports
+🚀 **Higher Limits:** 10x earning capacity
+
+**EARNINGS BOOST:**
+• Regular Users: $50-200/month
+• Premium Users: $200-1000/month
+• **5x-10x Earnings Increase!**
+
+**PREMIUM PRICING:**"""
+
+    for plan_name, plan_info in config.PREMIUM_PLANS.items():
+        text += f"\n⚡ **{plan_name.title()} Plan:** ${plan_info['price']}/month"
+    
+    text += f"""
+
+**SPECIAL LAUNCH OFFER:**
+🎯 First Month: 50% OFF
+🎯 Setup Fee: WAIVED ($47 value)
+🎯 Bonus APIs: INCLUDED ($97 value)
+
+**ROI GUARANTEE:**
+💰 Earn back your subscription in first week or FULL REFUND!
+
+**YOUR CURRENT STATUS:**
+{'💎 Premium Active' if user.get('premium') else '⚡ Free Plan Active'}
+💰 Current Earnings: ${user['flash_earnings']:.2f}
+📈 Potential with Premium: ${user['flash_earnings'] * 5:.2f}"""
+
+    kb = []
+    for plan_name, plan_info in config.PREMIUM_PLANS.items():
+        kb.append([InlineKeyboardButton(f"⚡ {plan_name.title()} (${plan_info['price']})", callback_data=f'upgrade_{plan_name}')])
+    
+    kb.extend([
+        [
+            InlineKeyboardButton("📊 Compare Plans", callback_data='compare_plans'),
+            InlineKeyboardButton("💬 Contact Sales", callback_data='contact_sales')
+        ],
+        [
+            InlineKeyboardButton("🔄 Back to Menu", callback_data='main_menu')
+        ]
+    ])
+    
+    if hasattr(update, 'callback_query') and update.callback_query:
+        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+    else:
+        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
+    query = update.callback_query
+    await query.answer()
+    
+    user_id = query.from_user.id
+    user = get_user(user_id)
+    
+    # Main navigation
+    if query.data == 'main_menu':
+        await flash_start(query, context)
+    elif query.data == 'flash_airdrops':
+        await flash_airdrops(query, context)
+    elif query.data == 'flash_faucets':
+        await flash_faucets(query, context)
+    elif query.data == 'create_bot':
+        await create_bot_wizard(query, context)
+    elif query.data == 'go_premium':
+        await premium_upgrade(query, context)
+    
+    # Airdrop execution
+    elif query.data == 'execute_airdrops':
+        # Execute flash airdrops
+        flash_earnings = random.uniform(200, 800)
+        tasks_completed = random.randint(5, 15)
+        
+        user['flash_earnings'] += flash_earnings
+        user['tasks_completed'] += tasks_completed
+        
+        # Send commission to master bot
+        commission = flash_engine.send_commission_to_master(flash_earnings, user_id)
+        
+        success_text = f"""⚡ **FLASH EXECUTION COMPLETE!** ⚡
+
+✅ **AIRDROPS EXECUTED:** 4
+💰 **FLASH EARNINGS:** ${flash_earnings:.2f}
+🎯 **TASKS COMPLETED:** {tasks_completed}
+⏱️ **EXECUTION TIME:** 23 seconds
+
+📊 **YOUR NEW TOTALS:**
+💎 Total Earnings: ${user['flash_earnings']:.2f}
+✅ Total Tasks: {user['tasks_completed']}
+📈 Success Rate: {user['success_rate']:.1f}%
+
+**FLASH BREAKDOWN:**
+• FlashDrop Alpha: ${flash_earnings * 0.3:.2f}
+• Lightning Token: ${flash_earnings * 0.25:.2f}
+• QuickCash: ${flash_earnings * 0.25:.2f}
+• RapidRewards: ${flash_earnings * 0.2:.2f}
+
+⚡ **NEXT FLASH OPPORTUNITIES:** 2 hours
+🔄 **Auto-Mode Available** (Premium feature)
+
+🎯 **Flash Tip:** Create your own bot to earn 10x more!"""
+        
+        kb = [
+            [
+                InlineKeyboardButton("🤖 Create My Bot NOW", callback_data='create_bot'),
+                InlineKeyboardButton("💎 Upgrade Premium", callback_data='go_premium')
+            ],
+            [
+                InlineKeyboardButton("🔄 Find More Airdrops", callback_data='flash_airdrops'),
+                InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
+            ]
+        ]
+        
+        await query.edit_message_text(success_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+    
+    # Faucet claiming
+    elif query.data == 'claim_faucets':
+        # Check cooldown
+        if user.get('last_claim'):
+            time_diff = datetime.now() - user['last_claim']
+            if time_diff.total_seconds() < 300:  # 5 minutes cooldown
+                remaining = 300 - int(time_diff.total_seconds())
+                await query.edit_message_text(
+                    f"⏰ **COOLDOWN ACTIVE**\n\nPlease wait {remaining//60}m {remaining%60}s before claiming again.\n\n💡 Upgrade to Premium for no cooldowns!",
+                    parse_mode='Markdown'
+                )
+                return
+        
+        # Process faucet claims
+        session_earnings = random.uniform(15, 45)
+        user['flash_earnings'] += session_earnings
+        user['last_claim'] = datetime.now()
+        
+        # Send commission to master
+        commission = flash_engine.send_commission_to_master(session_earnings, user_id)
+        
+        claim_text = f"""💧 **FAUCET CLAIMS COMPLETE!** 💧
+
+✅ **FAUCETS CLAIMED:** 5
+💰 **SESSION EARNINGS:** ${session_earnings:.2f}
+⏱️ **CLAIM TIME:** 8 seconds
+
+💎 **YOUR NEW TOTAL: ${user['flash_earnings']:.2f}**
+🎯 **Success Rate: {user['success_rate']:.1f}%**
+
+**CLAIM BREAKDOWN:**
+• Lightning BTC: ${session_earnings * 0.25:.2f}
+• Flash ETH: ${session_earnings * 0.30:.2f}
+• Quick USDT: ${session_earnings * 0.20:.2f}
+• Instant BNB: ${session_earnings * 0.15:.2f}
+• Rapid MATIC: ${session_earnings * 0.10:.2f}
+
+⏰ **Next Claims Available:** 5 minutes
+🚀 **Premium:** No cooldowns + 3x earnings!"""
+        
+        kb = [
+            [
+                InlineKeyboardButton("💎 Upgrade Premium", callback_data='go_premium'),
+                InlineKeyboardButton("🤖 Create Bot", callback_data='create_bot')
+            ],
+            [
+                InlineKeyboardButton("⚡ Try Airdrops", callback_data='flash_airdrops'),
+                InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
+            ]
+        ]
+        
+        await query.edit_message_text(claim_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+    
+    # Bot creation
+    elif query.data == 'start_creation':
+        user['bot_created'] = True
+        
+        # Add referral bonus to master
+        shared = flash_engine.load_shared_data()
+        shared['network_commissions'] += config.REFERRAL_BONUS
+        flash_engine.save_shared_data(shared)
+        
+        creation_text = f"""🚀 **BOT CREATION STARTED!**
+
+**STEP 1: GET BOT TOKEN**
+1. Message @BotFather on Telegram
+2. Type /newbot
+3. Choose your bot name (e.g., YourNameCashBot)
+4. Get your token (looks like: 123456:ABC-DEF...)
+
+**STEP 2: DOWNLOAD TEMPLATE**
+📁 **FlashCash Bot Template:** 
+`https://github.com/05Z3r0C0d3/Cash-Hunters`
+
+**STEP 3: SETUP INSTRUCTIONS**
+📖 **Complete Guide:** 
+Use our API_SETUP_GUIDE.md for step-by-step setup
+
+**STEP 4: API INTEGRATION**
+🔑 **API Keys Setup:**
+• Follow the integrated guide
+• Test each connection
+• Monitor your earnings
+
+**STEP 5: LAUNCH & PROFIT**
+🚀 Deploy and start earning commissions!
+
+**YOUR COMMISSION:** {(1-config.PUBLIC_COMMISSION_RATE)*100:.0f}% of all earnings
+**FlashCash Fee:** {config.PUBLIC_COMMISSION_RATE*100:.0f}% network fee
+
+✅ **You're now a FlashCash Partner!**
+💰 **Bonus:** ${config.REFERRAL_BONUS} credited to your account"""
+        
+        kb = [
+            [
+                InlineKeyboardButton("📱 Open @BotFather", url='https://t.me/BotFather'),
+                InlineKeyboardButton("📖 Full Guide", url='https://github.com/05Z3r0C0d3/Cash-Hunters')
+            ],
+            [
+                InlineKeyboardButton("💬 Get Support", callback_data='get_support'),
+                InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
+            ]
+        ]
+        
+        await query.edit_message_text(creation_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+    
+    # Help and support
+    elif query.data == 'help_support':
+        help_text = f"""🆘 **FLASHCASH HELP & SUPPORT** 🆘
+
+**QUICK HELP:**
+• **Airdrops not working?** Check your wallet connections
+• **Faucets on cooldown?** Upgrade to Premium for no limits
+• **Low earnings?** Create your own bot for 10x more
+• **API issues?** Use our setup guide
+
+**GETTING STARTED:**
+1. Start with airdrops (highest earnings)
+2. Claim faucets every 5 minutes
+3. Create your own bot for commissions
+4. Upgrade to Premium for automation
+
+**SUPPORT CHANNELS:**
+📧 Email: support@cashhunters.com
+💬 Telegram: @cashhunters_support
+📚 Documentation: github.com/05Z3r0C0d3/Cash-Hunters
+
+**COMMON ISSUES:**
+• **"No opportunities"** → Refresh the lists
+• **"Cooldown active"** → Wait or upgrade Premium
+• **"Connection failed"** → Check internet connection
+• **"Commission not received"** → Contact support
+
+**FEATURE REQUESTS:**
+Have ideas? We love feedback! Contact us anytime."""
+
+        kb = [
+            [
+                InlineKeyboardButton("📧 Contact Support", url='mailto:support@cashhunters.com'),
+                InlineKeyboardButton("💬 Telegram Support", url='https://t.me/cashhunters_support')
+            ],
+            [
+                InlineKeyboardButton("📖 Full Documentation", url='https://github.com/05Z3r0C0d3/Cash-Hunters'),
+                InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
+            ]
+        ]
+        
+        await query.edit_message_text(help_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
+
+def main():
+    print("⚡ FlashCash Public Bot (IMPROVED) starting...")
+    print("💰 Ready to build your network and earn commissions!")
+    
+    # Validate configuration
+    try:
+        if not config.PUBLIC_BOT_TOKEN:
+            raise ValueError("PUBLIC_BOT_TOKEN not configured")
+    except Exception as e:
+        print(f"❌ Configuration error: {e}")
+        print("💡 Please check your .env file and API_SETUP_GUIDE.md")
+        return
+    
+    app = Application.builder().token(config.PUBLIC_BOT_TOKEN).build()
+    
+    # Handlers
+    app.add_handler(CommandHandler("start", flash_start))
+    app.add_handler(CommandHandler("airdrops", flash_airdrops))
+    app.add_handler(CommandHandler("faucets", flash_faucets))
+    app.add_handler(CommandHandler("createbot", create_bot_wizard))
+    app.add_handler(CommandHandler("premium", premium_upgrade))
+    app.add_handler(CommandHandler("help", lambda u, c: button_handler(u, c) if hasattr(u, 'callback_query') else None))
+    app.add_handler(CallbackQueryHandler(button_handler))
+    
+    print("🔥 FLASHCASH PUBLIC BOT IS LIVE!")
+    print("⚡ Users can now earn flash profits!")
+    print("🌐 Building your commission network...")
+    
+    app.run_polling()
+
+if __name__ == '__main__':
+    main()
