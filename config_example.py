import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
# Замените на свой токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Замените на свой Telegram ID
ADMIN_ID = int(os.getenv("ADMIN_ID", "YOUR_ADMIN_ID_HERE"))

# Database Configuration
DATABASE_PATH = "bot_database.db"

# Web Interface Configuration
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
WEB_DEBUG = True 