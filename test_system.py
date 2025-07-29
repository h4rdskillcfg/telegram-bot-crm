#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестовый скрипт для проверки работы Telegram Bot CRM системы
"""

import sys
import os

def test_imports():
    """Тестирование импортов"""
    print("🔍 Тестирование импортов...")
    
    try:
        from config import BOT_TOKEN, ADMIN_ID, DATABASE_PATH
        print("✅ config.py - OK")
    except Exception as e:
        print(f"❌ config.py - Ошибка: {e}")
        return False
    
    try:
        from database import Database
        print("✅ database.py - OK")
    except Exception as e:
        print(f"❌ database.py - Ошибка: {e}")
        return False
    
    try:
        from bot import TelegramBot
        print("✅ bot.py - OK")
    except Exception as e:
        print(f"❌ bot.py - Ошибка: {e}")
        return False
    
    try:
        from web_interface import app
        print("✅ web_interface.py - OK")
    except Exception as e:
        print(f"❌ web_interface.py - Ошибка: {e}")
        return False
    
    return True

def test_database():
    """Тестирование базы данных"""
    print("\n🗄️ Тестирование базы данных...")
    
    try:
        from database import Database
        db = Database()
        print("✅ База данных инициализирована")
        
        # Тест добавления пользователя
        db.add_user(123456789, "test_user", "Test", "User")
        print("✅ Добавление пользователя - OK")
        
        # Тест получения статистики
        stats = db.get_statistics()
        print(f"✅ Статистика получена: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка базы данных: {e}")
        return False

def test_config():
    """Тестирование конфигурации"""
    print("\n⚙️ Тестирование конфигурации...")
    
    try:
        from config import BOT_TOKEN, ADMIN_ID, DATABASE_PATH
        
        print(f"✅ Токен бота: {BOT_TOKEN[:20]}...")
        print(f"✅ ID администратора: {ADMIN_ID}")
        print(f"✅ Путь к БД: {DATABASE_PATH}")
        
        if BOT_TOKEN and BOT_TOKEN != "YOUR_BOT_TOKEN":
            print("✅ Токен бота настроен")
        else:
            print("⚠️ Токен бота не настроен")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False

def test_files():
    """Тестирование наличия файлов"""
    print("\n📁 Проверка файлов...")
    
    required_files = [
        'config.py',
        'database.py',
        'bot.py',
        'web_interface.py',
        'main.py',
        'requirements.txt',
        'README.md'
    ]
    
    required_templates = [
        'templates/base.html',
        'templates/index.html',
        'templates/users.html',
        'templates/active_users.html',
        'templates/broadcast.html'
    ]
    
    all_files = required_files + required_templates
    
    for file_path in all_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - отсутствует")
            return False
    
    return True

def main():
    """Главная функция тестирования"""
    print("🧪 Тестирование Telegram Bot CRM системы")
    print("=" * 50)
    
    tests = [
        test_files,
        test_config,
        test_imports,
        test_database
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Ошибка в тесте {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Результаты тестирования: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Система готова к запуску.")
        print("\n🚀 Для запуска выполните:")
        print("   python main.py")
        print("\n🌐 Веб-интерфейс будет доступен по адресу:")
        print("   http://localhost:5000")
        print("\n🤖 Бот будет работать в Telegram")
        return True
    else:
        print("❌ Некоторые тесты не пройдены. Проверьте настройки.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 