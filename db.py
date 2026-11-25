# ──────────────────────────────────────────
#  db.py  –  Database connection helper
# ──────────────────────────────────────────

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def get_connection():
    """Return a live MySQL connection, or None on failure."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"\n[DB ERROR] Could not connect to MySQL: {e}")
        return None


def close_connection(conn, cursor=None):
    """Safely close cursor and connection."""
    if cursor:
        cursor.close()
    if conn and conn.is_connected():
        conn.close()
