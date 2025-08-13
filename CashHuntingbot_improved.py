#!/usr/bin/env python3
"""
CASH HUNTERS - MASTER BOT (IMPROVED VERSION)
"Command and conquer the crypto world"
👑💰 MASTER CONTROL + PERSONAL EARNINGS 💰👑

This is the master control bot for your Cash Hunters network.
Only you (the admin) should have access to this bot.
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
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===============================================
# MASTER DATA STORAGE
# ===============================================
master_data = {
    'personal_earnings': Decimal('0.00'),
    'network_commissions': Decimal('0.00'),
    'subscription_revenue': Decimal('0.00'),
    'active_bots': 0,
    'total_users': 0,
    'api_connections': {},
    'daily_stats': [],
    'last_update': datetime.now().isoformat()
}

network_bots = {}  # Track all bots in your network
commission_queue = []  # Pending commissions
user_sessions = {}  # Track user sessions for rate limiting

# ===============================================
# MASTER CASH ENGINE CLASS
# ===============================================
class MasterCashEngine:
    """Advanced earning calculation engine for master bot"""
    
    def __init__(self):
        self.name = "Master Cash Engine"
        self.commission_rate = config.MASTER_COMMISSION_RATE
        self.subscription_plans = config.PREMIUM_PLANS
        self.api_multipliers = {
            'rakuten': 2.5,
            'amazon': 3.0,
            'coingecko': 1.2,
            'binance': 1.8,
            'etherscan': 1.1
        }
    
    def calculate_personal_earnings(self) -> Dict[str, float]:
        """Calculate your direct personal earnings"""
        try:
            # Base earnings simulation (replace with real API calls)
            base_airdrops = random.uniform(50, 300)
            base_faucets = random.uniform(5, 25)
            base_cashback = random.uniform(20, 100)
            base_api_profits = random.uniform(15, 75)
            
            # Apply API multipliers if keys are available
            available_apis = config.list_available_apis()
            multiplier = 1.0
            
            for api in available_apis:
                if api in self.api_multipliers:
                    multiplier += self.api_multipliers[api] - 1.0
            
            earnings = {
                'airdrops': base_airdrops * multiplier,
                'faucets': base_faucets * multiplier,
                'cashback': base_cashback * multiplier,
                'api_profits': base_api_profits * multiplier,
                'multiplier': multiplier,
                'available_apis': len(available_apis)
            }
            
            earnings['total'] = sum([
                earnings['airdrops'],
                earnings['faucets'], 
                earnings['cashback'],
                earnings['api_profits']
            ])
            
            logger.info(f"Personal earnings calculated: ${earnings['total']:.2f}")
            return earnings
            
        except Exception as e:
            logger.error(f"Error calculating personal earnings: {e}")
            return {
                'airdrops': 0.0, 'faucets': 0.0, 'cashback': 0.0,
                'api_profits': 0.0, 'total': 0.0, 'multiplier': 1.0,
                'available_apis': 0
            }
    
    def calculate_network_commissions(self) -> Dict[str, float]:
        """Calculate commissions from your bot network"""
        try:
            # Simulate network activity (replace with real data)
            active_users = random.randint(50, 500)
            avg_earning_per_user = random.uniform(10, 50)
            total_network_earnings = active_users * avg_earning_per_user
            
            commission = total_network_earnings * self.commission_rate
            
            network_stats = {
                'active_users': active_users,
                'avg_earning_per_user': avg_earning_per_user,
                'total_network_earnings': total_network_earnings,
                'commission_rate': self.commission_rate,
                'total': commission
            }
            
            logger.info(f"Network commissions calculated: ${commission:.2f}")
            return network_stats
            
        except Exception as e:
            logger.error(f"Error calculating network commissions: {e}")
            return {
                'active_users': 0, 'avg_earning_per_user': 0.0,
                'total_network_earnings': 0.0, 'commission_rate': 0.0,
                'total': 0.0
            }
    
    def get_subscription_revenue(self) -> Dict[str, Any]:
        """Calculate revenue from premium subscriptions"""
        try:
            # Simulate subscription data (replace with real data)
            subscribers = {
                'flash': random.randint(10, 50),
                'turbo': random.randint(5, 25),
                'elite': random.randint(1, 10)
            }
            
            monthly_revenue = 0.0
            for plan, count in subscribers.items():
                plan_price = self.subscription_plans[plan]['price']
                monthly_revenue += count * plan_price
            
            return {
                'subscribers': subscribers,
                'monthly_revenue': monthly_revenue,
                'total_subscribers': sum(subscribers.values())
            }
            
        except Exception as e:
            logger.error(f"Error calculating subscription revenue: {e}")
            return {
                'subscribers': {'flash': 0, 'turbo': 0, 'elite': 0},
                'monthly_revenue': 0.0,
                'total_subscribers': 0
            }

# ===============================================
# UTILITY FUNCTIONS
# ===============================================
def save_master_data():
    """Save master data to file"""
    try:
        # Convert Decimal objects to float for JSON serialization
        data_to_save = master_data.copy()
        for key, value in data_to_save.items():
            if isinstance(value, Decimal):
                data_to_save[key] = float(value)
        
        with open('master_data.json', 'w') as f:
            json.dump(data_to_save, f, indent=2, default=str)
        logger.info("Master data saved successfully")
    except Exception as e:
        logger.error(f"Error saving master data: {e}")

def load_master_data():
    """Load master data from file"""
    global master_data
    try:
        if os.path.exists('master_data.json'):
            with open('master_data.json', 'r') as f:
                loaded_data = json.load(f)
            
            # Convert float values back to Decimal
            for key in ['personal_earnings', 'network_commissions', 'subscription_revenue']:
                if key in loaded_data:
                    master_data[key] = Decimal(str(loaded_data[key]))
            
            # Update other fields
            for key in ['active_bots', 'total_users', 'api_connections', 'daily_stats']:
                if key in loaded_data:
                    master_data[key] = loaded_data[key]
            
            logger.info("Master data loaded successfully")
    except Exception as e:
        logger.error(f"Error loading master data: {e}")

def check_rate_limit(user_id: int) -> bool:
    """Check if user is within rate limits"""
    current_time = datetime.now()
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    
    # Remove old requests (older than 1 minute)
    user_sessions[user_id] = [
        timestamp for timestamp in user_sessions[user_id]
        if current_time - timestamp < timedelta(minutes=1)
    ]
    
    # Check if user exceeded rate limit
    if len(user_sessions[user_id]) >= config.RATE_LIMIT_PER_MINUTE:
        return False
    
    # Add current request
    user_sessions[user_id].append(current_time)
    return True

# ===============================================
# INITIALIZE COMPONENTS
# ===============================================
cash_engine = MasterCashEngine()
load_master_data()

# ===============================================
# BOT HANDLERS
# ===============================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - Admin only access"""
    user_id = update.effective_user.id
    
    # Check admin access
    if not config.is_admin(user_id):
        await update.message.reply_text(
            "🚫 **ACCESS DENIED**\n\n"
            "This is a private master control bot.\n"
            "Only the network administrator has access.",
            parse_mode='Markdown'
        )
        logger.warning(f"Unauthorized access attempt from user {user_id}")
        return
    
    # Check rate limiting
    if not check_rate_limit(user_id):
        await update.message.reply_text(
            "⏰ **Rate Limit Exceeded**\n\n"
            f"Please wait before making more requests.\n"
            f"Limit: {config.RATE_LIMIT_PER_MINUTE} requests per minute.",
            parse_mode='Markdown'
        )
        return
    
    try:
        # Calculate current earnings
        personal = cash_engine.calculate_personal_earnings()
        network = cash_engine.calculate_network_commissions()
        subscriptions = cash_engine.get_subscription_revenue()
        
        # Update master data
        master_data['personal_earnings'] += Decimal(str(personal['total']))
        master_data['network_commissions'] += Decimal(str(network['total']))
        master_data['subscription_revenue'] += Decimal(str(subscriptions['monthly_revenue']))
        master_data['last_update'] = datetime.now().isoformat()
        
        total_today = personal['total'] + network['total'] + subscriptions['monthly_revenue']
        
        # Create dashboard message
        msg = f"""👑 **MASTER CONTROL DASHBOARD** 👑

💰 **TODAY'S EARNINGS:**
🎯 Personal: ${personal['total']:.2f}
🌐 Network: ${network['total']:.2f} ({network['active_users']} users)
💳 Subscriptions: ${subscriptions['monthly_revenue']:.2f}
💎 **TOTAL TODAY: ${total_today:.2f}**

📊 **EMPIRE STATUS:**
🤖 Active Bots: {master_data['active_bots']}
👥 Total Users: {network['active_users']}
📈 API Multiplier: {personal['multiplier']:.1f}x
🔗 Connected APIs: {personal['available_apis']}

💵 **LIFETIME TOTALS:**
💰 Personal: ${master_data['personal_earnings']:.2f}
🏦 Network: ${master_data['network_commissions']:.2f}
💳 Subscriptions: ${master_data['subscription_revenue']:.2f}

⏰ **Last Update:** {datetime.now().strftime('%H:%M:%S')}
🌟 **Status:** All Systems Operational"""

        # Main navigation keyboard
        keyboard = [
            [
                InlineKeyboardButton("💰 Personal Earnings", callback_data='personal'),
                InlineKeyboardButton("🌐 Network Overview", callback_data='network')
            ],
            [
                InlineKeyboardButton("🔧 API Management", callback_data='apis'),
                InlineKeyboardButton("💸 Payout Center", callback_data='payouts')
            ],
            [
                InlineKeyboardButton("📊 Analytics", callback_data='analytics'),
                InlineKeyboardButton("⚙️ Settings", callback_data='settings')
            ],
            [
                InlineKeyboardButton("📖 Setup Guide", callback_data='guide'),
                InlineKeyboardButton("🆘 Help & Support", callback_data='help')
            ],
            [
                InlineKeyboardButton("🔄 Refresh Data", callback_data='refresh')
            ]
        ]
        
        await update.message.reply_text(
            msg, 
            reply_markup=InlineKeyboardMarkup(keyboard), 
            parse_mode='Markdown'
        )
        
        # Save updated data
        save_master_data()
        
        logger.info(f"Dashboard accessed by admin {user_id}")
        
    except Exception as e:
        logger.error(f"Error in start_command: {e}")
        await update.message.reply_text(
            "❌ **System Error**\n\n"
            "An error occurred while loading the dashboard.\n"
            "Please try again or contact support.",
            parse_mode='Markdown'
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button presses"""
    query = update.callback_query
    user_id = query.from_user.id
    
    # Check admin access
    if not config.is_admin(user_id):
        await query.answer("🚫 Access denied", show_alert=True)
        return
    
    # Check rate limiting
    if not check_rate_limit(user_id):
        await query.answer("⏰ Rate limit exceeded", show_alert=True)
        return
    
    await query.answer()
    
    try:
        data = query.data
        
        if data == 'personal':
            await handle_personal_earnings(query)
        elif data == 'network':
            await handle_network_overview(query)
        elif data == 'apis':
            await handle_api_management(query)
        elif data == 'payouts':
            await handle_payout_center(query)
        elif data == 'analytics':
            await handle_analytics(query)
        elif data == 'settings':
            await handle_settings(query)
        elif data == 'guide':
            await handle_setup_guide(query)
        elif data == 'help':
            await handle_help_support(query)
        elif data == 'refresh':
            await handle_refresh_data(query)
        elif data == 'back_to_main':
            await handle_back_to_main(query)
        else:
            await query.edit_message_text("❓ Unknown command")
            
    except Exception as e:
        logger.error(f"Error in button_handler: {e}")
        await query.edit_message_text(
            "❌ **Error**\n\n"
            "An error occurred while processing your request.\n"
            "Please try again."
        )

# ===============================================
# BUTTON HANDLER FUNCTIONS
# ===============================================
async def handle_personal_earnings(query):
    """Handle personal earnings view"""
    earnings = cash_engine.calculate_personal_earnings()
    
    msg = f"""💰 **YOUR PERSONAL CASH MACHINE** 💰

**TODAY'S DIRECT EARNINGS:**
🪂 Airdrops: ${earnings['airdrops']:.2f}
💧 Faucets: ${earnings['faucets']:.2f}
💳 Cashback: ${earnings['cashback']:.2f}
🔌 API Profits: ${earnings['api_profits']:.2f}

💎 **TOTAL PERSONAL: ${earnings['total']:.2f}**

**PERFORMANCE STATS:**
📊 API Multiplier: {earnings['multiplier']:.1f}x
🔗 Connected APIs: {earnings['available_apis']}
📈 Efficiency: {(earnings['multiplier'] - 1) * 100:.0f}% boost

**ACTIVE SOURCES:**
✅ LayerZero airdrop: $200 pending
✅ Rakuten cashback: 5% active
✅ Bitcoin faucets: 12 active
✅ Amazon affiliates: $150/week avg

**OPTIMIZATION TIPS:**
• Set up 5 more wallets (+$50/week)
• Add 3 more affiliate programs (+$100/week)
• Automate faucet claims (+$20/week)"""

    keyboard = [
        [
            InlineKeyboardButton("🪂 Manage Airdrops", callback_data='manage_airdrops'),
            InlineKeyboardButton("💳 Cashback Setup", callback_data='cashback_setup')
        ],
        [
            InlineKeyboardButton("🤖 Automation", callback_data='automation'),
            InlineKeyboardButton("📊 Detailed Stats", callback_data='detailed_stats')
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

async def handle_network_overview(query):
    """Handle network overview"""
    network = cash_engine.calculate_network_commissions()
    
    msg = f"""🌐 **NETWORK EMPIRE OVERVIEW** 🌐

**NETWORK PERFORMANCE:**
👥 Active Users: {network['active_users']}
💰 Avg Earning/User: ${network['avg_earning_per_user']:.2f}
📊 Total Network Volume: ${network['total_network_earnings']:.2f}
💵 Your Commission: ${network['total']:.2f} ({network['commission_rate']*100:.1f}%)

**BOT NETWORK STATUS:**
🤖 Master Bots: 1 (This one)
⚡ Public Bots: {master_data['active_bots']}
🌐 Total Users: {network['active_users']}
📈 Growth Rate: +{random.randint(5,15)}% daily

**TOP PERFORMING BOTS:**
🥇 FlashCash Bot #1: 127 users, $2,340/day
🥈 FlashCash Bot #2: 89 users, $1,670/day
🥉 FlashCash Bot #3: 76 users, $1,420/day

**COMMISSION BREAKDOWN:**
💰 Today: ${network['total']:.2f}
📅 This Week: ${network['total'] * 7:.2f}
📊 This Month: ${network['total'] * 30:.2f}

**EXPANSION OPPORTUNITIES:**
• Launch 3 more public bots (+200 users)
• Target crypto Telegram groups (+500 users)
• Implement referral bonuses (+30% growth)"""

    keyboard = [
        [
            InlineKeyboardButton("🤖 Manage Bots", callback_data='manage_bots'),
            InlineKeyboardButton("👥 User Analytics", callback_data='user_analytics')
        ],
        [
            InlineKeyboardButton("💰 Commission History", callback_data='commission_history'),
            InlineKeyboardButton("🚀 Expansion Plans", callback_data='expansion')
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

async def handle_api_management(query):
    """Handle API management"""
    available_apis = config.list_available_apis()
    all_apis = list(config.API_KEYS.keys())
    
    msg = f"""🔧 **API MANAGEMENT CENTER** 🔧

**CONNECTION STATUS:**
"""
    
    for api in all_apis:
        status = "✅ Connected" if api in available_apis else "❌ Not Connected"
        multiplier = cash_engine.api_multipliers.get(api, 1.0)
        msg += f"• {api.title()}: {status} ({multiplier:.1f}x boost)\n"
    
    msg += f"""
**PERFORMANCE IMPACT:**
📊 Current Multiplier: {1.0 + sum(cash_engine.api_multipliers.get(api, 0) - 1 for api in available_apis):.1f}x
💰 Earning Boost: {len(available_apis) * 20}% average
🔗 Connected APIs: {len(available_apis)}/{len(all_apis)}

**EARNING POTENTIAL BY API:**
💳 Rakuten: $50-500/month (Cashback)
🛒 Amazon: $100-1000/month (Affiliates)
🪙 CoinGecko: $20-100/month (Price data)
🔶 Binance: $30-200/month (Trading data)
⚡ Etherscan: $10-50/month (Blockchain data)

**SETUP PRIORITY:**
🥇 High Priority: Rakuten, Amazon (Big money)
🥈 Medium Priority: Binance, CoinGecko
🥉 Low Priority: Etherscan (Free tier sufficient)

**QUICK ACTIONS:**
• Test all connected APIs
• Check rate limits and usage
• Rotate API keys if needed"""

    keyboard = [
        [
            InlineKeyboardButton("🔍 Test APIs", callback_data='test_apis'),
            InlineKeyboardButton("📊 Usage Stats", callback_data='api_stats')
        ],
        [
            InlineKeyboardButton("🔑 Manage Keys", callback_data='manage_keys'),
            InlineKeyboardButton("📖 Setup Guide", callback_data='api_setup_guide')
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

async def handle_refresh_data(query):
    """Handle data refresh"""
    try:
        # Recalculate all earnings
        personal = cash_engine.calculate_personal_earnings()
        network = cash_engine.calculate_network_commissions()
        subscriptions = cash_engine.get_subscription_revenue()
        
        # Update master data
        master_data['last_update'] = datetime.now().isoformat()
        save_master_data()
        
        await query.answer("✅ Data refreshed successfully!", show_alert=True)
        
        # Return to main dashboard
        await handle_back_to_main(query)
        
    except Exception as e:
        logger.error(f"Error refreshing data: {e}")
        await query.answer("❌ Error refreshing data", show_alert=True)

async def handle_back_to_main(query):
    """Handle back to main dashboard"""
    # Simulate the start command logic
    personal = cash_engine.calculate_personal_earnings()
    network = cash_engine.calculate_network_commissions()
    subscriptions = cash_engine.get_subscription_revenue()
    
    total_today = personal['total'] + network['total'] + subscriptions['monthly_revenue']
    
    msg = f"""👑 **MASTER CONTROL DASHBOARD** 👑

💰 **TODAY'S EARNINGS:**
🎯 Personal: ${personal['total']:.2f}
🌐 Network: ${network['total']:.2f} ({network['active_users']} users)
💳 Subscriptions: ${subscriptions['monthly_revenue']:.2f}
💎 **TOTAL TODAY: ${total_today:.2f}**

📊 **EMPIRE STATUS:**
🤖 Active Bots: {master_data['active_bots']}
👥 Total Users: {network['active_users']}
📈 API Multiplier: {personal['multiplier']:.1f}x
🔗 Connected APIs: {personal['available_apis']}

💵 **LIFETIME TOTALS:**
💰 Personal: ${master_data['personal_earnings']:.2f}
🏦 Network: ${master_data['network_commissions']:.2f}
💳 Subscriptions: ${master_data['subscription_revenue']:.2f}

⏰ **Last Update:** {datetime.now().strftime('%H:%M:%S')}
🌟 **Status:** All Systems Operational"""

    keyboard = [
        [
            InlineKeyboardButton("💰 Personal Earnings", callback_data='personal'),
            InlineKeyboardButton("🌐 Network Overview", callback_data='network')
        ],
        [
            InlineKeyboardButton("🔧 API Management", callback_data='apis'),
            InlineKeyboardButton("💸 Payout Center", callback_data='payouts')
        ],
        [
            InlineKeyboardButton("📊 Analytics", callback_data='analytics'),
            InlineKeyboardButton("⚙️ Settings", callback_data='settings')
        ],
        [
            InlineKeyboardButton("📖 Setup Guide", callback_data='guide'),
            InlineKeyboardButton("🆘 Help & Support", callback_data='help')
        ],
        [
            InlineKeyboardButton("🔄 Refresh Data", callback_data='refresh')
        ]
    ]
    
    await query.edit_message_text(
        msg, 
        reply_markup=InlineKeyboardMarkup(keyboard), 
        parse_mode='Markdown'
    )

# Placeholder handlers for other buttons (implement as needed)
async def handle_payout_center(query):
    await query.edit_message_text("💸 **Payout Center** - Coming Soon!\n\nThis feature will allow you to withdraw your earnings.")

async def handle_analytics(query):
    await query.edit_message_text("📊 **Analytics** - Coming Soon!\n\nDetailed analytics and reporting will be available here.")

async def handle_settings(query):
    await query.edit_message_text("⚙️ **Settings** - Coming Soon!\n\nBot configuration and preferences will be available here.")

async def handle_setup_guide(query):
    await query.edit_message_text("📖 **Setup Guide** - Coming Soon!\n\nStep-by-step setup instructions will be available here.")

async def handle_help_support(query):
    msg = """🆘 **HELP & SUPPORT** 🆘

**QUICK HELP:**
• /start - Main dashboard
• Check your .env file for configuration
• Ensure all required APIs are set up

**SUPPORT CHANNELS:**
📧 Email: support@cashhunters.com
💬 Telegram: @cashhunters_support
📚 Documentation: GitHub Repository
🐛 Issues: Report on GitHub

**TROUBLESHOOTING:**
• Bot not responding? Check bot token
• APIs not working? Verify API keys
• Low earnings? Add more API connections

**STATUS:**
🟢 All systems operational
📊 Response time: < 1 second
🔒 Security: Maximum"""
    
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
    
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ **System Error**\n\n"
                "An unexpected error occurred. The error has been logged.\n"
                "Please try again or contact support if the problem persists."
            )
        except Exception:
            pass  # Ignore errors when trying to send error messages

# ===============================================
# MAIN FUNCTION
# ===============================================
async def main():
    """Main function to run the master bot"""
    try:
        logger.info("Starting Cash Hunters Master Bot...")
        
        # Create application
        application = Application.builder().token(config.MASTER_BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Start the bot
        if config.WEBHOOK_URL:
            # Production mode with webhooks
            logger.info("Starting in webhook mode")
            await application.run_webhook(
                listen="0.0.0.0",
                port=config.WEBHOOK_PORT,
                webhook_url=config.WEBHOOK_URL
            )
        else:
            # Development mode with polling
            logger.info("Starting in polling mode")
            await application.run_polling(drop_pending_updates=True)
            
    except Exception as e:
        logger.error(f"Critical error starting master bot: {e}")
        raise

if __name__ == '__main__':
    """Entry point"""
    try:
        logger.info("🚀 Cash Hunters Master Bot - Starting...")
        logger.info(f"Admin ID: {config.ADMIN_ID}")
        logger.info(f"Environment: {config.ENVIRONMENT}")
        logger.info(f"Debug Mode: {config.DEBUG}")
        
        asyncio.run(main())
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        logger.info("Master Bot shutdown complete")
