#!/usr/bin/env python3
"""
CASH HUNTERS - PUBLIC BOT (CENTRALIZED VERSION)
"Flash profits, instant results, all earnings to master"
⚡💰 USERS EARN + MASTER GETS COMMISSION 💰⚡

This is the public bot that users interact with.
All earnings are tracked and commissions go to master bot owner.
Users CANNOT create their own bots - they only use this shared bot.
"""

import asyncio
import json
import logging
import os
import random
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from decimal import Decimal

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler, 
    ContextTypes,
    MessageHandler,
    filters
)

from config import config

# ===============================================
# LOGGING SETUP
# ===============================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('public_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===============================================
# USER DATA STORAGE
# ===============================================
flash_users = {}  # Track all users and their earnings
daily_stats = {}  # Daily statistics
user_sessions = {}  # Rate limiting
commission_queue = []  # Commission payments to master

# ===============================================
# CENTRALIZED CASH ENGINE
# ===============================================
class CentralizedCashEngine:
    """Centralized earning system - all money flows to master"""
    
    def __init__(self):
        self.name = "Centralized Flash Cash Engine"
        self.master_commission_rate = 0.15  # 15% to master (you)
        self.user_earning_rate = 0.85  # 85% to user
        self.success_stories = [
            "Sarah earned $347 in her first week! 🎉",
            "Mike made $892 from airdrops last month! 💰",
            "Jessica got $156 from faucets this week! 🚀",
            "Carlos earned $623 with cashback! 💳",
            "Ana made $445 with our system! ⚡",
            "David earned $789 this month! 👑"
        ]
        self.load_user_data()
    
    def load_user_data(self):
        """Load user data from file"""
        global flash_users
        try:
            if os.path.exists('flash_users.json'):
                with open('flash_users.json', 'r') as f:
                    flash_users = json.load(f)
                logger.info(f"Loaded {len(flash_users)} users")
        except Exception as e:
            logger.error(f"Error loading user data: {e}")
    
    def save_user_data(self):
        """Save user data to file"""
        try:
            # Convert Decimal objects for JSON serialization
            users_to_save = {}
            for user_id, data in flash_users.items():
                users_to_save[user_id] = {}
                for key, value in data.items():
                    if isinstance(value, Decimal):
                        users_to_save[user_id][key] = float(value)
                    else:
                        users_to_save[user_id][key] = value
            
            with open('flash_users.json', 'w') as f:
                json.dump(users_to_save, f, indent=2, default=str)
            logger.info("User data saved successfully")
        except Exception as e:
            logger.error(f"Error saving user data: {e}")
    
    def register_user(self, user_id: int, username: str = "") -> Dict[str, Any]:
        """Register new user in the system"""
        if str(user_id) not in flash_users:
            flash_users[str(user_id)] = {
                'username': username,
                'total_earnings': Decimal('0.00'),
                'commissions_paid': Decimal('0.00'),
                'join_date': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'premium_plan': None,
                'referrals': 0,
                'sessions_completed': 0,
                'level': 1
            }
            self.save_user_data()
            logger.info(f"New user registered: {user_id}")
        
        return flash_users[str(user_id)]
    
    def calculate_flash_earnings(self, user_id: int) -> Dict[str, float]:
        """Calculate earnings for flash activities"""
        try:
            user_data = flash_users.get(str(user_id), {})
            level = user_data.get('level', 1)
            premium_multiplier = 2.0 if user_data.get('premium_plan') else 1.0
            
            # Base earnings (these would be real in production)
            base_airdrop = random.uniform(50, 200) * level
            base_faucet = random.uniform(10, 40) * level
            base_cashback = random.uniform(15, 60) * level
            base_bonus = random.uniform(5, 25) * level
            
            # Apply premium multiplier
            earnings = {
                'flash_airdrops': base_airdrop * premium_multiplier,
                'flash_faucets': base_faucet * premium_multiplier,
                'cashback_rewards': base_cashback * premium_multiplier,
                'bonus_activities': base_bonus * premium_multiplier,
                'level': level,
                'premium_multiplier': premium_multiplier
            }
            
            earnings['total'] = sum([
                earnings['flash_airdrops'],
                earnings['flash_faucets'],
                earnings['cashback_rewards'],
                earnings['bonus_activities']
            ])
            
            return earnings
            
        except Exception as e:
            logger.error(f"Error calculating earnings for user {user_id}: {e}")
            return {
                'flash_airdrops': 0.0, 'flash_faucets': 0.0,
                'cashback_rewards': 0.0, 'bonus_activities': 0.0,
                'total': 0.0, 'level': 1, 'premium_multiplier': 1.0
            }
    
    def process_earnings(self, user_id: int, earnings: float) -> Dict[str, float]:
        """Process user earnings and calculate commission to master"""
        try:
            user_earnings = earnings * self.user_earning_rate
            master_commission = earnings * self.master_commission_rate
            
            # Update user data
            user_data = flash_users.get(str(user_id), {})
            user_data['total_earnings'] = Decimal(str(user_data.get('total_earnings', 0))) + Decimal(str(user_earnings))
            user_data['commissions_paid'] = Decimal(str(user_data.get('commissions_paid', 0))) + Decimal(str(master_commission))
            user_data['last_activity'] = datetime.now().isoformat()
            user_data['sessions_completed'] = user_data.get('sessions_completed', 0) + 1
            
            # Level up system
            total_earnings = float(user_data['total_earnings'])
            new_level = min(10, max(1, int(total_earnings / 100) + 1))
            user_data['level'] = new_level
            
            flash_users[str(user_id)] = user_data
            
            # Send commission to master
            self.send_commission_to_master(master_commission, user_id, user_earnings)
            
            # Save data
            self.save_user_data()
            
            return {
                'user_earnings': user_earnings,
                'master_commission': master_commission,
                'total_user_earnings': float(user_data['total_earnings']),
                'new_level': new_level
            }
            
        except Exception as e:
            logger.error(f"Error processing earnings for user {user_id}: {e}")
            return {
                'user_earnings': 0.0, 'master_commission': 0.0,
                'total_user_earnings': 0.0, 'new_level': 1
            }
    
    def send_commission_to_master(self, commission: float, user_id: int, user_earnings: float):
        """Send commission data to master bot"""
        try:
            # Load or create shared data file
            shared_data = self.load_shared_data()
            
            # Add commission record
            commission_record = {
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'commission': commission,
                'user_earnings': user_earnings,
                'commission_rate': self.master_commission_rate
            }
            
            # Update totals
            shared_data['total_commissions'] = shared_data.get('total_commissions', 0.0) + commission
            shared_data['total_users'] = len(flash_users)
            shared_data['last_update'] = datetime.now().isoformat()
            
            # Add to commission queue
            if 'commission_queue' not in shared_data:
                shared_data['commission_queue'] = []
            shared_data['commission_queue'].append(commission_record)
            
            # Keep only last 1000 records
            shared_data['commission_queue'] = shared_data['commission_queue'][-1000:]
            
            # Save to shared file
            self.save_shared_data(shared_data)
            
            logger.info(f"Commission ${commission:.2f} sent to master from user {user_id}")
            
        except Exception as e:
            logger.error(f"Error sending commission to master: {e}")
    
    def load_shared_data(self) -> Dict[str, Any]:
        """Load shared data file"""
        try:
            if os.path.exists(config.SHARED_DATA_FILE):
                with open(config.SHARED_DATA_FILE, 'r') as f:
                    return json.load(f)
            else:
                return {
                    'total_commissions': 0.0,
                    'total_users': 0,
                    'commission_queue': [],
                    'last_update': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error loading shared data: {e}")
            return {
                'total_commissions': 0.0,
                'total_users': 0,
                'commission_queue': [],
                'last_update': datetime.now().isoformat()
            }
    
    def save_shared_data(self, data: Dict[str, Any]):
        """Save shared data file"""
        try:
            with open(config.SHARED_DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving shared data: {e}")

# ===============================================
# RATE LIMITING
# ===============================================
def check_rate_limit(user_id: int) -> bool:
    """Check if user is within rate limits"""
    current_time = datetime.now()
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    
    # Remove old requests
    user_sessions[user_id] = [
        timestamp for timestamp in user_sessions[user_id]
        if current_time - timestamp < timedelta(minutes=1)
    ]
    
    # Check limit
    if len(user_sessions[user_id]) >= config.RATE_LIMIT_PER_MINUTE:
        return False
    
    # Add current request
    user_sessions[user_id].append(current_time)
    return True

# ===============================================
# INITIALIZE ENGINE
# ===============================================
cash_engine = CentralizedCashEngine()

# ===============================================
# BOT HANDLERS
# ===============================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - Welcome new users"""
    user_id = update.effective_user.id
    username = update.effective_user.username or ""
    
    # Rate limiting
    if not check_rate_limit(user_id):
        await update.message.reply_text(
            "⏰ **Slow down!**\n\n"
            f"Please wait before making more requests.\n"
            f"Limit: {config.RATE_LIMIT_PER_MINUTE} per minute.",
            parse_mode='Markdown'
        )
        return
    
    try:
        # Register user
        user_data = cash_engine.register_user(user_id, username)
        
        # Get random success story
        success_story = random.choice(cash_engine.success_stories)
        
        welcome_msg = f"""⚡ **WELCOME TO CASH HUNTERS!** ⚡

🚀 **The #1 Crypto Earning Bot Network**

💰 **WHAT YOU CAN EARN:**
🪂 Flash Airdrops: $50-400 per session
💧 Flash Faucets: $10-80 per session  
💳 Cashback Rewards: $15-120 per session
🎁 Bonus Activities: $5-50 per session

📊 **YOUR STATUS:**
👤 Level: {user_data.get('level', 1)}
💎 Total Earned: ${float(user_data.get('total_earnings', 0)):.2f}
🏆 Sessions: {user_data.get('sessions_completed', 0)}

🌟 **SUCCESS STORY:**
{success_story}

💡 **HOW IT WORKS:**
• Click buttons to start earning activities
• Complete simple tasks (5-10 minutes)
• Get paid instantly to your account
• Level up for higher earnings!

⚠️ **IMPORTANT:** This is a SHARED bot. Everyone uses the same bot to earn money. You earn 85% of all activities, and 15% goes to network maintenance.

🎯 **Ready to start earning?**"""

        keyboard = [
            [
                InlineKeyboardButton("⚡ Start Flash Earning", callback_data='flash_earn'),
                InlineKeyboardButton("📊 My Stats", callback_data='my_stats')
            ],
            [
                InlineKeyboardButton("🪂 Flash Airdrops", callback_data='flash_airdrops'),
                InlineKeyboardButton("💧 Flash Faucets", callback_data='flash_faucets')
            ],
            [
                InlineKeyboardButton("💎 Premium Plans", callback_data='premium'),
                InlineKeyboardButton("🆘 Help & Support", callback_data='help')
            ],
            [
                InlineKeyboardButton("📢 Share & Earn More", callback_data='share_bot')
            ]
        ]
        
        await update.message.reply_text(
            welcome_msg,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        
        logger.info(f"User {user_id} started the bot")
        
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text(
            "❌ **System Error**\n\n"
            "Sorry, there was an error. Please try again.",
            parse_mode='Markdown'
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button presses"""
    query = update.callback_query
    user_id = query.from_user.id
    
    # Rate limiting
    if not check_rate_limit(user_id):
        await query.answer("⏰ Rate limit exceeded", show_alert=True)
        return
    
    await query.answer()
    
    try:
        data = query.data
        
        if data == 'flash_earn':
            await handle_flash_earning(query)
        elif data == 'my_stats':
            await handle_user_stats(query)
        elif data == 'flash_airdrops':
            await handle_flash_airdrops(query)
        elif data == 'flash_faucets':
            await handle_flash_faucets(query)
        elif data == 'premium':
            await handle_premium_plans(query)
        elif data == 'help':
            await handle_help_support(query)
        elif data == 'share_bot':
            await handle_share_bot(query)
        elif data == 'back_to_main':
            await handle_back_to_main(query)
        elif data.startswith('earn_'):
            await handle_earning_activity(query, data)
        else:
            await query.edit_message_text("❓ Unknown command")
            
    except Exception as e:
        logger.error(f"Error in button_handler: {e}")
        await query.edit_message_text(
            "❌ **Error**\n\n"
            "An error occurred. Please try again."
        )

# ===============================================
# BUTTON HANDLER FUNCTIONS
# ===============================================
async def handle_flash_earning(query):
    """Handle main flash earning activities"""
    user_id = query.from_user.id
    user_data = flash_users.get(str(user_id), {})
    level = user_data.get('level', 1)
    premium = user_data.get('premium_plan') is not None
    
    msg = f"""⚡ **FLASH EARNING CENTER** ⚡

👤 **Your Level:** {level} {'👑' if premium else ''}
💰 **Earning Multiplier:** {2.0 if premium else 1.0}x

🎯 **AVAILABLE ACTIVITIES:**

🪂 **Flash Airdrops** - ${50 * level}-${200 * level}
• High-value crypto airdrops
• 5-15 minutes to complete
• Success rate: 92%

💧 **Flash Faucets** - ${10 * level}-${80 * level}  
• Multiple crypto faucets
• 2-8 minutes each
• Auto-claim available

💳 **Cashback Rewards** - ${15 * level}-${120 * level}
• Shopping cashback opportunities
• Instant rewards
• Premium partnerships

🎁 **Bonus Activities** - ${5 * level}-${50 * level}
• Social media tasks
• Quick surveys
• Referral bonuses

💡 **Pro Tip:** Complete multiple activities for maximum earnings!"""

    keyboard = [
        [
            InlineKeyboardButton("🪂 Start Airdrops", callback_data='earn_airdrops'),
            InlineKeyboardButton("💧 Start Faucets", callback_data='earn_faucets')
        ],
        [
            InlineKeyboardButton("💳 Start Cashback", callback_data='earn_cashback'),
            InlineKeyboardButton("🎁 Start Bonus", callback_data='earn_bonus')
        ],
        [
            InlineKeyboardButton("⚡ EARN ALL (Premium)", callback_data='earn_all'),
        ],
        [
            InlineKeyboardButton("🔙 Back to Main", callback_data='back_to_main')
        ]
    ]
    
    await query.edit_message_text(
        msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_earning_activity(query, activity_type):
    """Handle specific earning activities"""
    user_id = query.from_user.id
    
    # Calculate earnings for this session
    earnings = cash_engine.calculate_flash_earnings(user_id)
    
    # Process the earnings (user gets 85%, master gets 15%)
    result = cash_engine.process_earnings(user_id, earnings['total'])
    
    activity_names = {
        'earn_airdrops': 'Flash Airdrops',
        'earn_faucets': 'Flash Faucets', 
        'earn_cashback': 'Cashback Rewards',
        'earn_bonus': 'Bonus Activities',
        'earn_all': 'ALL ACTIVITIES'
    }
    
    activity_name = activity_names.get(activity_type, 'Activity')
    
    success_msg = f"""✅ **{activity_name.upper()} COMPLETED!** ✅

💰 **YOUR EARNINGS:**
🎯 This Session: ${result['user_earnings']:.2f}
💎 Total Earnings: ${result['total_user_earnings']:.2f}
📈 New Level: {result['new_level']}

📊 **SESSION BREAKDOWN:**
🪂 Airdrops: ${earnings['flash_airdrops']:.2f}
💧 Faucets: ${earnings['flash_faucets']:.2f}
💳 Cashback: ${earnings['cashback_rewards']:.2f}
🎁 Bonuses: ${earnings['bonus_activities']:.2f}

🏆 **LEVEL UP REWARDS:**
{'🎉 Level increased! Higher earnings unlocked!' if result['new_level'] > earnings['level'] else '💪 Keep earning to level up!'}

💡 **What's Next:**
• Try other earning activities
• Share the bot for referral bonuses
• Upgrade to Premium for 2x earnings"""

    keyboard = [
        [
            InlineKeyboardButton("🔄 Earn Again", callback_data='flash_earn'),
            InlineKeyboardButton("📊 View Stats", callback_data='my_stats')
        ],
        [
            InlineKeyboardButton("💎 Upgrade Premium", callback_data='premium'),
            InlineKeyboardButton("📢 Share Bot", callback_data='share_bot')
        ],
        [
            InlineKeyboardButton("🏠 Main Menu", callback_data='back_to_main')
        ]
    ]
    
    await query.edit_message_text(
        success_msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_user_stats(query):
    """Handle user statistics display"""
    user_id = query.from_user.id
    user_data = flash_users.get(str(user_id), {})
    
    if not user_data:
        await query.edit_message_text("❌ User data not found. Please use /start first.")
        return
    
    join_date = datetime.fromisoformat(user_data.get('join_date', datetime.now().isoformat()))
    days_active = (datetime.now() - join_date).days + 1
    
    avg_daily = float(user_data.get('total_earnings', 0)) / days_active if days_active > 0 else 0
    
    msg = f"""📊 **YOUR CASH HUNTERS STATS** 📊

👤 **Profile:**
🆔 User ID: {user_id}
📅 Member Since: {join_date.strftime('%B %d, %Y')}
⏱️ Days Active: {days_active}

💰 **Earnings:**
💎 Total Earned: ${float(user_data.get('total_earnings', 0)):.2f}
📈 Daily Average: ${avg_daily:.2f}
🏆 Level: {user_data.get('level', 1)}/10
🎯 Sessions: {user_data.get('sessions_completed', 0)}

💳 **Network Stats:**
💰 Commissions Paid: ${float(user_data.get('commissions_paid', 0)):.2f}
📊 Your Share: 85% | Network: 15%
👥 Referrals: {user_data.get('referrals', 0)}

🎖️ **Achievements:**
{'🥇 Top Earner' if float(user_data.get('total_earnings', 0)) > 500 else '🥈 Rising Star' if float(user_data.get('total_earnings', 0)) > 100 else '🥉 Getting Started'}
{'👑 Premium Member' if user_data.get('premium_plan') else '💎 Free Member'}
{'🔥 Active User' if user_data.get('sessions_completed', 0) > 10 else '🌱 New User'}

📈 **Next Milestones:**
• Level {user_data.get('level', 1) + 1}: ${(user_data.get('level', 1) + 1) * 100} total earnings
• Premium: 2x earnings multiplier
• Referrals: $5 bonus per friend"""

    keyboard = [
        [
            InlineKeyboardButton("⚡ Start Earning", callback_data='flash_earn'),
            InlineKeyboardButton("💎 Go Premium", callback_data='premium')
        ],
        [
            InlineKeyboardButton("📢 Refer Friends", callback_data='share_bot'),
            InlineKeyboardButton("🏠 Main Menu", callback_data='back_to_main')
        ]
    ]
    
    await query.edit_message_text(
        msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_premium_plans(query):
    """Handle premium plans display"""
    plans = config.PREMIUM_PLANS
    
    msg = f"""💎 **PREMIUM PLANS** 💎

🚀 **Unlock 2x Earnings + Exclusive Features!**

💡 **FLASH PLAN** - ${plans['flash']['price']}/month
✅ 2x Earnings Multiplier
✅ Priority Support
✅ Auto-Claim Features
✅ Advanced Analytics

⚡ **TURBO PLAN** - ${plans['turbo']['price']}/month  
✅ All Flash Plan features
✅ 5x Earnings Multiplier
✅ Premium API Access
✅ VIP Airdrops
✅ Personal Manager

👑 **ELITE PLAN** - ${plans['elite']['price']}/month
✅ All Turbo Plan features  
✅ 10x Earnings Multiplier
✅ Exclusive Opportunities
✅ White-glove Service
✅ Custom Strategies

💰 **EARNINGS COMPARISON:**
Free: $50-200/session
Flash: $100-400/session (2x)
Turbo: $250-1000/session (5x)
Elite: $500-2000/session (10x)

🎯 **ROI Calculator:**
Flash Plan pays for itself with just 1 session!
Elite Plan can earn $15,000+/month!

⚠️ **Limited Time:** 50% off first month!"""

    keyboard = [
        [
            InlineKeyboardButton("💡 Get Flash ($19)", callback_data='buy_flash'),
            InlineKeyboardButton("⚡ Get Turbo ($39)", callback_data='buy_turbo')
        ],
        [
            InlineKeyboardButton("👑 Get Elite ($79)", callback_data='buy_elite')
        ],
        [
            InlineKeyboardButton("💳 Payment Methods", callback_data='payment_methods'),
            InlineKeyboardButton("🔙 Back", callback_data='back_to_main')
        ]
    ]
    
    await query.edit_message_text(
        msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_share_bot(query):
    """Handle bot sharing for referrals"""
    user_id = query.from_user.id
    bot_username = context.bot.username if hasattr(context, 'bot') else "YourCashHuntersBot"
    
    share_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    msg = f"""📢 **SHARE & EARN MORE!** 📢

💰 **REFERRAL PROGRAM:**
🎁 Earn $5 for each friend who joins
🚀 Your friends get $5 welcome bonus too
📈 Unlimited referrals = Unlimited bonuses

🔗 **Your Referral Link:**
`{share_link}`

📱 **Share Message (Copy & Paste):**
```
💰 I'm earning $200+ daily with Cash Hunters!

⚡ Flash Airdrops, Faucets & Cashback
🎁 Get $5 welcome bonus
🚀 Start earning in 5 minutes

Join here: {share_link}
```

📊 **Your Referral Stats:**
👥 Total Referrals: {flash_users.get(str(user_id), {}).get('referrals', 0)}
💰 Referral Earnings: ${flash_users.get(str(user_id), {}).get('referrals', 0) * 5:.2f}

🎯 **Best Places to Share:**
• Telegram crypto groups
• Discord communities  
• Social media (Twitter, Facebook)
• Friends & family
• Crypto forums"""

    keyboard = [
        [
            InlineKeyboardButton("📋 Copy Link", callback_data=f'copy_link_{user_id}'),
            InlineKeyboardButton("📱 Share on Telegram", url=f"https://t.me/share/url?url={share_link}")
        ],
        [
            InlineKeyboardButton("📊 Referral Stats", callback_data='referral_stats'),
            InlineKeyboardButton("🔙 Back", callback_data='back_to_main')
        ]
    ]
    
    await query.edit_message_text(
        msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_back_to_main(query):
    """Handle back to main menu"""
    user_id = query.from_user.id
    user_data = flash_users.get(str(user_id), {})
    
    success_story = random.choice(cash_engine.success_stories)
    
    msg = f"""⚡ **CASH HUNTERS DASHBOARD** ⚡

👤 **Your Status:**
💎 Level: {user_data.get('level', 1)}
💰 Total Earned: ${float(user_data.get('total_earnings', 0)):.2f}
🏆 Sessions: {user_data.get('sessions_completed', 0)}

🌟 **Today's Success:**
{success_story}

🎯 **Quick Actions:**
Ready to earn more money?"""

    keyboard = [
        [
            InlineKeyboardButton("⚡ Start Flash Earning", callback_data='flash_earn'),
            InlineKeyboardButton("📊 My Stats", callback_data='my_stats')
        ],
        [
            InlineKeyboardButton("🪂 Flash Airdrops", callback_data='flash_airdrops'),
            InlineKeyboardButton("💧 Flash Faucets", callback_data='flash_faucets')
        ],
        [
            InlineKeyboardButton("💎 Premium Plans", callback_data='premium'),
            InlineKeyboardButton("🆘 Help & Support", callback_data='help')
        ],
        [
            InlineKeyboardButton("📢 Share & Earn More", callback_data='share_bot')
        ]
    ]
    
    await query.edit_message_text(
        msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# Placeholder handlers
async def handle_flash_airdrops(query):
    await query.edit_message_text("🪂 **Flash Airdrops** - Coming Soon!\n\nSpecialized airdrop hunting features will be available here.")

async def handle_flash_faucets(query):
    await query.edit_message_text("💧 **Flash Faucets** - Coming Soon!\n\nAutomated faucet claiming features will be available here.")

async def handle_help_support(query):
    msg = """🆘 **HELP & SUPPORT** 🆘

❓ **Frequently Asked Questions:**

**How do I earn money?**
Click "Start Flash Earning" and complete activities. You'll earn 85% of all generated revenue.

**Is this a shared bot?**
Yes! Everyone uses the same bot. This ensures maximum efficiency and earnings for all users.

**How do I get paid?**
Earnings are tracked in your account. Contact support for withdrawal methods.

**What about commissions?**
15% of earnings go to network maintenance and development. You keep 85%.

📞 **Contact Support:**
📧 Email: support@cashhunters.com
💬 Telegram: @cashhunters_support
🌐 Website: cashhunters.com

⏰ **Response Time:** Usually within 24 hours
🔒 **Security:** All data is encrypted and secure"""
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Main", callback_data='back_to_main')]]
    
    await query.edit_message_text(
        msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# ===============================================
# ERROR HANDLER
# ===============================================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Exception while handling an update: {context.error}")

# ===============================================
# MAIN FUNCTION
# ===============================================
async def main():
    """Main function to run the public bot"""
    try:
        logger.info("Starting Cash Hunters Public Bot...")
        
        # Create application
        application = Application.builder().token(config.PUBLIC_BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Start the bot
        if config.WEBHOOK_URL:
            # Production mode
            logger.info("Starting in webhook mode")
            await application.run_webhook(
                listen="0.0.0.0",
                port=config.WEBHOOK_PORT + 1,  # Different port from master
                webhook_url=config.WEBHOOK_URL + "/public"
            )
        else:
            # Development mode
            logger.info("Starting in polling mode")
            await application.run_polling(drop_pending_updates=True)
            
    except Exception as e:
        logger.error(f"Critical error starting public bot: {e}")
        raise

if __name__ == '__main__':
    """Entry point"""
    try:
        logger.info("🚀 Cash Hunters Public Bot - Starting...")
        logger.info("⚡ Centralized earning system active")
        logger.info("💰 All commissions flow to master bot")
        
        asyncio.run(main())
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        logger.info("Public Bot shutdown complete")
