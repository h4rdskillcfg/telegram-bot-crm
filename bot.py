import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN, ADMIN_ID
from database import Database
import asyncio

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.db = Database()
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        # Основные команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("broadcast", self.broadcast_command))
        
        # Обработка callback запросов (кнопки)
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Обработка текстовых сообщений
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        user = update.effective_user
        user_id = user.id
        
        # Добавляем пользователя в базу данных
        self.db.add_user(
            user_id=user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Создаем главное меню
        keyboard = [
            [KeyboardButton("🎮 Запустить игру")],
            [KeyboardButton("👤 Профиль")],
            [KeyboardButton("📢 Канал")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
        
        welcome_text = f"""
🎉 Добро пожаловать, {user.first_name}!

Выберите действие из меню ниже:
        """
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        
        # Логируем активность
        self.db.update_user_activity(user_id)
        self.db.log_message(user_id, "/start")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        help_text = """
🤖 Доступные команды:

/start - Главное меню
/help - Справка
/profile - Ваш профиль
/game - Запустить игру
/channel - Наш канал

Для администратора:
/stats - Статистика бота
/broadcast - Массовая рассылка
        """
        
        await update.message.reply_text(help_text)
        self.db.update_user_activity(update.effective_user.id)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать статистику (только для администратора)"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ У вас нет доступа к этой команде.")
            return
        
        stats = self.db.get_statistics()
        
        stats_text = f"""
📊 Статистика бота:

👥 Общее количество пользователей: {stats['total_users']}
✅ Активных за неделю: {stats['active_users']}
🆕 Новых за сегодня: {stats['new_users_today']}
🆕 Новых за неделю: {stats['new_users_week']}
        """
        
        await update.message.reply_text(stats_text)
    
    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Массовая рассылка (только для администратора)"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ У вас нет доступа к этой команде.")
            return
        
        # Проверяем, есть ли текст сообщения
        if not context.args:
            await update.message.reply_text(
                "📢 Использование: /broadcast <текст сообщения>\n\n"
                "Пример: /broadcast Привет всем! Новое обновление бота."
            )
            return
        
        message_text = " ".join(context.args)
        users = self.db.get_users_for_broadcast()
        
        if not users:
            await update.message.reply_text("❌ Нет активных пользователей для рассылки.")
            return
        
        # Отправляем сообщение всем пользователям
        success_count = 0
        failed_count = 0
        
        for user_id in users:
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"📢 Массовая рассылка:\n\n{message_text}"
                )
                success_count += 1
                await asyncio.sleep(0.1)  # Небольшая задержка между отправками
            except Exception as e:
                failed_count += 1
                logger.error(f"Failed to send message to {user_id}: {e}")
        
        await update.message.reply_text(
            f"✅ Рассылка завершена!\n\n"
            f"✅ Успешно отправлено: {success_count}\n"
            f"❌ Ошибок: {failed_count}"
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нажатий на inline кнопки"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        self.db.update_user_activity(user_id)
        
        if query.data == "profile":
            await self.show_profile(query, context)
        elif query.data == "game":
            await self.start_game(query, context)
        elif query.data == "channel":
            await self.show_channel(query, context)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        user = update.effective_user
        message_text = update.message.text
        user_id = user.id
        
        # Обновляем активность пользователя
        self.db.update_user_activity(user_id)
        self.db.log_message(user_id, message_text)
        
        if message_text == "👤 Профиль":
            await self.show_profile_text(update, context)
        elif message_text == "🎮 Запустить игру":
            await self.start_game_text(update, context)
        elif message_text == "📢 Канал":
            await self.show_channel_text(update, context)
        else:
            await update.message.reply_text(
                "Выберите действие из меню или используйте команду /help для справки."
            )
    
    async def show_profile_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать профиль пользователя (текстовое меню)"""
        user = update.effective_user
        user_data = self.db.get_user(user.id)
        
        if user_data:
            join_date = user_data[4]  # join_date
            profile_text = f"""
👤 Профиль пользователя:

🆔 ID: {user.id}
👤 Имя: {user.first_name}
📛 Фамилия: {user.last_name or 'Не указана'}
🔗 Username: @{user.username or 'Не указан'}
📅 Дата регистрации: {join_date}
            """
        else:
            profile_text = "❌ Ошибка получения данных профиля."
        
        await update.message.reply_text(profile_text)
    
    async def show_profile(self, query, context):
        """Показать профиль пользователя (inline кнопки)"""
        user = query.from_user
        user_data = self.db.get_user(user.id)
        
        if user_data:
            join_date = user_data[4]
            profile_text = f"""
👤 Профиль пользователя:

🆔 ID: {user.id}
👤 Имя: {user.first_name}
📛 Фамилия: {user.last_name or 'Не указана'}
🔗 Username: @{user.username or 'Не указан'}
📅 Дата регистрации: {join_date}
            """
        else:
            profile_text = "❌ Ошибка получения данных профиля."
        
        await query.edit_message_text(profile_text)
    
    async def start_game_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Запустить игру (текстовое меню)"""
        game_text = """
🎮 Игра запущена!

🎯 Правила игры:
- Угадайте число от 1 до 100
- У вас есть 10 попыток
- После каждой попытки бот подскажет, больше или меньше загаданное число

🎲 Начнем игру!
        """
        
        await update.message.reply_text(game_text)
    
    async def start_game(self, query, context):
        """Запустить игру (inline кнопки)"""
        game_text = """
🎮 Игра запущена!

🎯 Правила игры:
- Угадайте число от 1 до 100
- У вас есть 10 попыток
- После каждой попытки бот подскажет, больше или меньше загаданное число

🎲 Начнем игру!
        """
        
        await query.edit_message_text(game_text)
    
    async def show_channel_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать информацию о канале (текстовое меню)"""
        channel_text = """
📢 Наш канал:

🔗 Подписывайтесь на наш канал для получения последних новостей и обновлений!

📱 Telegram канал: @your_channel_name
🌐 Веб-сайт: https://your-website.com

📧 Поддержка: @support_username
        """
        
        await update.message.reply_text(channel_text)
    
    async def show_channel(self, query, context):
        """Показать информацию о канале (inline кнопки)"""
        channel_text = """
📢 Наш канал:

🔗 Подписывайтесь на наш канал для получения последних новостей и обновлений!

📱 Telegram канал: @your_channel_name
🌐 Веб-сайт: https://your-website.com

📧 Поддержка: @support_username
        """
        
        await query.edit_message_text(channel_text)
    
    def run(self):
        """Запуск бота"""
        logger.info("Starting bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run() 