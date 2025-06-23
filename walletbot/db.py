import sqlite3
from config import DATABASE

def get_conn():
    return sqlite3.connect(DATABASE)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        invite_by INTEGER,
        reg_time DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS wallet (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 0
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS wallet_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        change INTEGER,
        reason TEXT,
        note TEXT,
        time DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT balance FROM wallet WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

def change_balance(user_id, amount, reason, note):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO wallet (user_id, balance) VALUES (?, 0)", (user_id,))
    c.execute("UPDATE wallet SET balance = balance + ? WHERE user_id=?", (amount, user_id))
    c.execute("INSERT INTO wallet_log (user_id, change, reason, note) VALUES (?, ?, ?, ?)",
              (user_id, amount, reason, note))
    conn.commit()
    conn.close()
