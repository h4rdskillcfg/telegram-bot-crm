from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from database import Database
from config import ADMIN_ID, WEB_HOST, WEB_PORT, WEB_DEBUG
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Измените на свой секретный ключ
db = Database()

@app.route('/')
def index():
    """Главная страница с статистикой"""
    stats = db.get_statistics()
    users = db.get_all_users()[:10]  # Последние 10 пользователей
    
    return render_template('index.html', stats=stats, users=users)

@app.route('/users')
def users():
    """Страница со списком всех пользователей"""
    users = db.get_all_users()
    return render_template('users.html', users=users)

@app.route('/active_users')
def active_users():
    """Страница с активными пользователями"""
    users = db.get_active_users()
    return render_template('active_users.html', users=users)

@app.route('/broadcast', methods=['GET', 'POST'])
def broadcast():
    """Страница массовой рассылки"""
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            users = db.get_users_for_broadcast()
            return jsonify({
                'success': True,
                'message': f'Готово к отправке {len(users)} пользователям',
                'user_count': len(users)
            })
        else:
            return jsonify({'success': False, 'message': 'Введите текст сообщения'})
    
    return render_template('broadcast.html')

@app.route('/api/stats')
def api_stats():
    """API для получения статистики"""
    stats = db.get_statistics()
    return jsonify(stats)

@app.route('/api/users')
def api_users():
    """API для получения списка пользователей"""
    users = db.get_all_users()
    user_list = []
    for user in users:
        user_list.append({
            'user_id': user[0],
            'username': user[1],
            'first_name': user[2],
            'last_name': user[3],
            'join_date': user[4],
            'is_active': user[5],
            'last_activity': user[6]
        })
    return jsonify(user_list)

@app.route('/api/broadcast', methods=['POST'])
def api_broadcast():
    """API для выполнения массовой рассылки"""
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({'success': False, 'message': 'Текст сообщения не указан'})
    
    users = db.get_users_for_broadcast()
    return jsonify({
        'success': True,
        'message': f'Сообщение будет отправлено {len(users)} пользователям',
        'user_count': len(users)
    })

if __name__ == '__main__':
    app.run(host=WEB_HOST, port=WEB_PORT, debug=WEB_DEBUG) 