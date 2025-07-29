@echo off
echo 🚀 Быстрая загрузка проекта на GitHub
echo ==========================================

echo.
echo 📋 Проверка Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git не установлен. Установите Git с https://git-scm.com/
    pause
    exit /b 1
)

echo ✅ Git установлен

echo.
echo 📋 Инициализация Git репозитория...
git init
git add .
git commit -m "Initial commit: Telegram Bot CRM System"

echo.
echo 🌐 Настройка удаленного репозитория...
set /p username="Введите ваше имя пользователя GitHub: "
set /p repo_name="Введите название репозитория (по умолчанию: telegram-bot-crm): "

if "%repo_name%"=="" set repo_name=telegram-bot-crm

echo.
echo 📋 Информация о репозитории:
echo    Пользователь: %username%
echo    Репозиторий: %repo_name%
echo    URL: https://github.com/%username%/%repo_name%

echo.
set /p confirm="Продолжить? (y/n): "
if /i not "%confirm%"=="y" (
    echo ❌ Операция отменена
    pause
    exit /b 1
)

echo.
echo 🔄 Добавление удаленного репозитория...
git remote add origin https://github.com/%username%/%repo_name%.git
git branch -M main
git push -u origin main

echo.
echo 🎉 Проект успешно загружен на GitHub!
echo 📱 Ссылка на репозиторий: https://github.com/%username%/%repo_name%
echo.
echo 📝 Следующие шаги:
echo 1. Проверьте репозиторий на GitHub
echo 2. Настройте GitHub Secrets для безопасности
echo 3. Создайте Issues для отслеживания задач
echo 4. Добавьте описание проекта

pause 