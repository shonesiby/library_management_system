# ──────────────────────────────────────────
#  config.example.py  –  Template for config.py
#  Copy this file to config.py and fill in your credentials.
#  DO NOT commit config.py to GitHub (it's in .gitignore)
# ──────────────────────────────────────────

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",          # ← your MySQL username
    "password": "your_password", # ← your MySQL password
    "database": "library_db",
    "port":     3306,
}
