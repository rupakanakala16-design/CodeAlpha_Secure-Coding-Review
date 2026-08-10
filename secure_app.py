import os
from flask import Flask, render_template_string, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'demo-secure-secret-key')
DATABASE = 'secure_users.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.execute(
            "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
            ('admin', generate_password_hash('StrongPassword!2025'))
        )
        conn.commit()


@app.route('/')
def index():
    if 'username' in session:
        return render_template_string('''<h1>Welcome {{ username }}</h1><a href="/logout">Logout</a>''', username=session['username'])
    return render_template_string('''
        <h2>Secure Login Demo</h2>
        <form method="post" action="/login">
            <p>Username: <input name="username" required></p>
            <p>Password: <input type="password" name="password" required></p>
            <button type="submit">Login</button>
        </form>
    ''')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not username or len(username) < 3 or len(username) > 30:
        return 'Invalid username', 400

    if not password or len(password) < 8:
        return 'Invalid password length', 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        session['username'] = username
        return redirect(url_for('index'))

    return 'Invalid credentials', 401


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='127.0.0.1', port=5001)
