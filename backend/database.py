import sqlite3
import os
from config import Config


# Set database path (default to backend/users.db if not set in .env)
DB_PATH = Config.DB_PATH

def get_db():
    """Establish and return a database connection."""


    if not DB_PATH:  # Check if DB exists before connecting
        raise FileNotFoundError(f"DB_PATH is not set. Check config.py.")


    if not os.path.exists(DB_PATH):  # Check if DB exists before connecting
        raise FileNotFoundError(f"Database file not found at {DB_PATH}")


    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row


    # Ensure the users table exists
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    otp TEXT DEFAULT NULL,
                    otp_expiry TIMESTAMP DEFAULT NULL)''')

    conn.commit()
    return conn


def get_user(username, conn):
    """Retrieve a user by username using an existing database connection."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()


def add_user(username, password, email, conn):
    """Insert a new user into the database."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                   (username, password, email))
    conn.commit()


def update_otp(username, otp, otp_expiry, conn):
    """Update OTP and expiry timestamp for a user."""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET otp = ?, otp_expiry = ? WHERE username = ?", 
                   (otp, otp_expiry, username))
    conn.commit()


def delete_user(username, conn):
    """Delete a user by username."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()




'''
def get_user_by_email(email, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    return cursor.fetchone()
'''
