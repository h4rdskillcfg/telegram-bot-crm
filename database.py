import sqlite3
import datetime
from config import DATABASE_PATH

class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица статистики
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE DEFAULT CURRENT_DATE,
                new_users INTEGER DEFAULT 0,
                active_users INTEGER DEFAULT 0,
                total_users INTEGER DEFAULT 0
            )
        ''')
        
        # Таблица сообщений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message_text TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id, username=None, first_name=None, last_name=None):
        """Добавление нового пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, join_date, is_active, last_activity)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP)
        ''', (user_id, username, first_name, last_name))
        
        conn.commit()
        conn.close()
    
    def update_user_activity(self, user_id):
        """Обновление активности пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET last_activity = CURRENT_TIMESTAMP, is_active = 1
            WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id):
        """Получение информации о пользователе"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        return user
    
    def get_all_users(self):
        """Получение всех пользователей"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users ORDER BY join_date DESC')
        users = cursor.fetchall()
        
        conn.close()
        return users
    
    def get_active_users(self):
        """Получение активных пользователей (активность за последние 7 дней)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE last_activity >= datetime('now', '-7 days')
            ORDER BY last_activity DESC
        ''')
        users = cursor.fetchall()
        
        conn.close()
        return users
    
    def get_statistics(self):
        """Получение статистики"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Общее количество пользователей
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        # Активные пользователи за последние 7 дней
        cursor.execute('''
            SELECT COUNT(*) FROM users 
            WHERE last_activity >= datetime('now', '-7 days')
        ''')
        active_users = cursor.fetchone()[0]
        
        # Новые пользователи за сегодня
        cursor.execute('''
            SELECT COUNT(*) FROM users 
            WHERE DATE(join_date) = DATE('now')
        ''')
        new_users_today = cursor.fetchone()[0]
        
        # Новые пользователи за неделю
        cursor.execute('''
            SELECT COUNT(*) FROM users 
            WHERE join_date >= datetime('now', '-7 days')
        ''')
        new_users_week = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'new_users_today': new_users_today,
            'new_users_week': new_users_week
        }
    
    def log_message(self, user_id, message_text):
        """Логирование сообщений"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (user_id, message_text)
            VALUES (?, ?)
        ''', (user_id, message_text))
        
        conn.commit()
        conn.close()
    
    def get_users_for_broadcast(self):
        """Получение пользователей для массовой рассылки"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id FROM users WHERE is_active = 1')
        users = cursor.fetchall()
        
        conn.close()
        return [user[0] for user in users] 