import threading
import time
from bot import TelegramBot
from web_interface import app
from config import WEB_HOST, WEB_PORT, WEB_DEBUG

def run_bot():
    """Запуск Telegram бота в отдельном потоке"""
    print("🤖 Запуск Telegram бота...")
    bot = TelegramBot()
    bot.run()

def run_web():
    """Запуск веб-интерфейса в отдельном потоке"""
    print("🌐 Запуск веб-интерфейса...")
    app.run(host=WEB_HOST, port=WEB_PORT, debug=WEB_DEBUG)

def main():
    """Главная функция запуска системы"""
    print("🚀 Запуск Telegram Bot CRM системы...")
    print("=" * 50)
    
    # Запуск бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Небольшая задержка для инициализации бота
    time.sleep(2)
    
    # Запуск веб-интерфейса в основном потоке
    run_web()

if __name__ == "__main__":
    main() 