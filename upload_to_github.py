#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для автоматической загрузки проекта на GitHub
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Выполнение команды с выводом"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - успешно")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} - ошибка:")
            print(result.stderr)
            return False
        return True
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return False

def check_git_installed():
    """Проверка установки Git"""
    return run_command("git --version", "Проверка Git")

def init_git_repository():
    """Инициализация Git репозитория"""
    commands = [
        ("git init", "Инициализация Git репозитория"),
        ("git add .", "Добавление файлов в индекс"),
        ("git commit -m \"Initial commit: Telegram Bot CRM System\"", "Создание первого коммита")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def setup_remote_repository():
    """Настройка удаленного репозитория"""
    print("\n🌐 Настройка удаленного репозитория")
    print("=" * 50)
    
    # Запрос информации о репозитории
    username = input("Введите ваше имя пользователя GitHub: ")
    repo_name = input("Введите название репозитория (по умолчанию: telegram-bot-crm): ") or "telegram-bot-crm"
    
    remote_url = f"https://github.com/{username}/{repo_name}.git"
    
    print(f"\n📋 Информация о репозитории:")
    print(f"   Пользователь: {username}")
    print(f"   Репозиторий: {repo_name}")
    print(f"   URL: {remote_url}")
    
    confirm = input("\nПродолжить? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Операция отменена")
        return False
    
    # Добавление удаленного репозитория
    commands = [
        (f"git remote add origin {remote_url}", "Добавление удаленного репозитория"),
        ("git branch -M main", "Переименование ветки в main"),
        ("git push -u origin main", "Отправка кода на GitHub")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print(f"\n🎉 Проект успешно загружен на GitHub!")
    print(f"📱 Ссылка на репозиторий: https://github.com/{username}/{repo_name}")
    return True

def create_github_repository_instructions():
    """Инструкции по созданию репозитория на GitHub"""
    print("\n📋 Инструкции по созданию репозитория на GitHub:")
    print("=" * 50)
    print("1. Перейдите на https://github.com")
    print("2. Нажмите 'New repository'")
    print("3. Заполните форму:")
    print("   - Repository name: telegram-bot-crm")
    print("   - Description: Мини CRM система для Telegram бота")
    print("   - Public или Private (на ваш выбор)")
    print("   - ✅ Add a README file")
    print("   - ✅ Add .gitignore (Python)")
    print("   - ✅ Choose a license (MIT)")
    print("4. Нажмите 'Create repository'")
    print("5. Вернитесь сюда и продолжите")

def main():
    """Главная функция"""
    print("🚀 Автоматическая загрузка проекта на GitHub")
    print("=" * 50)
    
    # Проверка Git
    if not check_git_installed():
        print("❌ Git не установлен. Установите Git и попробуйте снова.")
        return False
    
    # Проверка наличия .gitignore
    if not os.path.exists('.gitignore'):
        print("❌ Файл .gitignore не найден. Создайте его перед загрузкой.")
        return False
    
    # Проверка конфиденциальных файлов
    sensitive_files = ['.env', 'bot_database.db', 'config_local.py']
    for file in sensitive_files:
        if os.path.exists(file):
            print(f"⚠️  Внимание: файл {file} будет исключен из загрузки (.gitignore)")
    
    # Создание репозитория
    print("\n📋 Создание репозитория на GitHub")
    print("=" * 50)
    create_github_repository_instructions()
    
    input("\nНажмите Enter после создания репозитория на GitHub...")
    
    # Инициализация Git
    if not init_git_repository():
        print("❌ Ошибка инициализации Git репозитория")
        return False
    
    # Настройка удаленного репозитория
    if not setup_remote_repository():
        print("❌ Ошибка настройки удаленного репозитория")
        return False
    
    print("\n🎉 Загрузка завершена успешно!")
    print("\n📝 Следующие шаги:")
    print("1. Проверьте репозиторий на GitHub")
    print("2. Настройте GitHub Secrets для безопасности")
    print("3. Создайте Issues для отслеживания задач")
    print("4. Добавьте описание проекта")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 