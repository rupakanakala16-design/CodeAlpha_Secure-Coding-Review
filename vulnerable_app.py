import sqlite3
from flask import Flask, request

app = Flask(__name__)
DATABASE = 'vulnerable_users.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    return conn


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        ''')
        conn.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
        conn.commit()


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    conn = get_db_connection()
    result = conn.execute(query).fetchone()
    conn.close()

    if result:
        return 'Login successful'
    return 'Invalid credentials'


if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='127.0.0.1', port=5002)
