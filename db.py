import sqlite3

def init_db():
    conn = sqlite3.connect("wallet.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            usdt REAL DEFAULT 0,
            cny REAL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_user(user_id, username):
    conn = sqlite3.connect("wallet.db")
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    row = c.fetchone()
    if not row:
        c.execute('INSERT INTO users (user_id, username) VALUES (?,?)', (user_id, username))
        conn.commit()
        c.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        row = c.fetchone()
    conn.close()
    return row

def update_balance(user_id, usdt=None, cny=None):
    conn = sqlite3.connect("wallet.db")
    c = conn.cursor()
    if usdt is not None:
        c.execute('UPDATE users SET usdt=? WHERE user_id=?', (usdt, user_id))
    if cny is not None:
        c.execute('UPDATE users SET cny=? WHERE user_id=?', (cny, user_id))
    conn.commit()
    conn.close()