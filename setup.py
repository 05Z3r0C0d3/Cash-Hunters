diff --git a/setup.py b/setup.py
--- a/setup.py
+++ b/setup.py
@@ -0,0 +1,164 @@
+#!/usr/bin/env python3
+"""
+CASH HUNTERS - AUTOMATED SETUP SCRIPT
+Automates installation and configuration of the bot network
+"""
+
+import os
+import sys
+import subprocess
+import shutil
+from pathlib import Path
+
+def print_banner():
+    """Print setup banner"""
+    print("""
+    ╔══════════════════════════════════════════════════════════════╗
+    ║                    💰 CASH HUNTERS SETUP 💰                 ║
+    ║              Automated Bot Network Installation              ║
+    ║                                                              ║
+    ║  🤖 Master Bot + Public Bot                                  ║
+    ║  🔧 Secure Configuration                                     ║
+    ║  📖 Complete API Guide                                       ║
+    ║  🚀 Ready to Deploy                                          ║
+    ╚══════════════════════════════════════════════════════════════╝
+    """)
+
+def check_python_version():
+    """Check if Python version is compatible"""
+    if sys.version_info < (3, 8):
+        print("❌ Error: Python 3.8 or higher is required")
+        print(f"   Current version: {sys.version}")
+        sys.exit(1)
+    print(f"✅ Python version: {sys.version.split()[0]}")
+
+def install_requirements():
+    """Install required Python packages"""
+    print("\n📦 Installing required packages...")
+    try:
+        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
+        print("✅ All packages installed successfully")
+    except subprocess.CalledProcessError:
+        print("❌ Error installing packages. Please install manually:")
+        print("   pip install -r requirements.txt")
+        sys.exit(1)
+
+def setup_environment():
+    """Set up environment configuration"""
+    print("\n🔧 Setting up environment configuration...")
+    
+    if not os.path.exists('.env'):
+        if os.path.exists('.env.template'):
+            shutil.copy('.env.template', '.env')
+            print("✅ Created .env file from template")
+            print("⚠️  IMPORTANT: Edit .env file with your bot tokens and API keys!")
+        else:
+            print("❌ Error: .env.template not found")
+            return False
+    else:
+        print("ℹ️  .env file already exists")
+    
+    return True
+
+def create_directories():
+    """Create necessary directories"""
+    print("\n📁 Creating directories...")
+    
+    directories = ['logs', 'data', 'backups']
+    for directory in directories:
+        Path(directory).mkdir(exist_ok=True)
+        print(f"✅ Created directory: {directory}")
+
+def validate_files():
+    """Validate that all required files exist"""
+    print("\n📋 Validating files...")
+    
+    required_files = [
+        'config.py',
+        'CashHuntingbot_improved.py',
+        'FlashkashBot_improved.py',
+        'API_SETUP_GUIDE.md',
+        'requirements.txt',
+        '.env.template'
+    ]
+    
+    missing_files = []
+    for file in required_files:
+        if os.path.exists(file):
+            print(f"✅ {file}")
+        else:
+            print(f"❌ {file} - MISSING")
+            missing_files.append(file)
+    
+    if missing_files:
+        print(f"\n❌ Missing files: {', '.join(missing_files)}")
+        return False
+    
+    print("\n✅ All required files present")
+    return True
+
+def show_next_steps():
+    """Show what to do next"""
+    print("""
+    ╔══════════════════════════════════════════════════════════════╗
+    ║                        🎉 SETUP COMPLETE! 🎉                ║
+    ╚══════════════════════════════════════════════════════════════╝
+    
+    📋 NEXT STEPS:
+    
+    1. 🔧 CONFIGURE YOUR BOTS:
+       • Edit .env file with your bot tokens
+       • Get tokens from @BotFather on Telegram
+       • Add your Telegram User ID
+    
+    2. 📖 SET UP APIs (OPTIONAL BUT RECOMMENDED):
+       • Read API_SETUP_GUIDE.md
+       • Start with free APIs (CoinGecko, Etherscan)
+       • Add earning APIs (Rakuten, Amazon)
+    
+    3. 🚀 LAUNCH YOUR BOTS:
+       • Master Bot: python CashHuntingbot_improved.py
+       • Public Bot: python FlashkashBot_improved.py
+    
+    4. 💰 START EARNING:
+       • Share your public bot
+       • Watch commissions roll in
+       • Scale your network
+    
+    ⚠️  IMPORTANT REMINDERS:
+    • Never share your bot tokens
+    • Keep .env file secure
+    • Read the API guide carefully
+    • Test with small amounts first
+    
+    📧 SUPPORT:
+    • GitHub: https://github.com/05Z3r0C0d3/Cash-Hunters
+    • Email: support@cashhunters.com
+    • Telegram: @cashhunters_support
+    
+    🎯 READY TO BUILD YOUR CRYPTO EMPIRE? LET'S GO! 🚀
+    """)
+
+def main():
+    """Main setup function"""
+    print_banner()
+    
+    print("🔍 Checking system requirements...")
+    check_python_version()
+    
+    if not validate_files():
+        print("\n❌ Setup failed: Missing required files")
+        sys.exit(1)
+    
+    install_requirements()
+    
+    if not setup_environment():
+        print("\n❌ Setup failed: Environment configuration error")
+        sys.exit(1)
+    
+    create_directories()
+    
+    show_next_steps()
+
+if __name__ == "__main__":
+    main()
