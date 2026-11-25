# 📚 Library Management System

A complete **Python + MySQL** command-line application implementing full **CRUD** operations for managing books, members, book issuance, and returns.

---

## 🚀 Features

- **Book Management** — Add, View, Update, Delete books
- **Member Management** — Register, View, Update, Delete members
- **Issue Book** — Issue books to registered members (14-day loan)
- **Return Book** — Return issued books, auto-update availability
- **Search Books** — Search by Title, Author, Category, or ISBN
- **View Reports** — All books, members, currently issued, returned history, overdue books

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.x |
| Database | MySQL 8.x |
| DB Driver | mysql-connector-python |

---

## 📁 Project Structure

```
library_management_system/
│
├── main.py              # Entry point (main menu)
├── config.py            # DB credentials (create from config.example.py)
├── db.py                # MySQL connection helper
├── utils.py             # Shared utilities
│
├── books.py             # Book CRUD + Search
├── members.py           # Member CRUD
├── transactions.py      # Issue Book & Return Book
├── reports.py           # All report views
│
├── requirements.txt     # pip dependencies
└── database/
    └── schema.sql       # MySQL schema + sample data
```

---

## ⚙️ Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/library_management_system.git
cd library_management_system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up the database
- Open **MySQL Workbench**
- Run `database/schema.sql` (creates `library_db` with all tables + sample data)

### 4. Configure database credentials
Create a `config.py` file from the example:
```bash
cp config.example.py config.py
```
Then edit `config.py` with your MySQL credentials:
```python
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "your_password",   # ← change this
    "database": "library_db",
    "port":     3306,
}
```

### 5. Run the application
```bash
python main.py
```

---

## 🗄️ Database Schema

| Table | Description |
|-------|-------------|
| `books` | Stores book details and copy counts |
| `members` | Registered library members |
| `issued_books` | Tracks all book issues and returns |

---

## 📋 CRUD Operations

| Module | Create | Read | Update | Delete |
|--------|--------|------|--------|--------|
| Books | ✅ | ✅ | ✅ | ✅ |
| Members | ✅ | ✅ | ✅ | ✅ |
| Issue/Return | ✅ | ✅ | — | — |

---

## 📌 Notes

- `config.py` is excluded from version control (listed in `.gitignore`) to protect your database password.
- Deleting a member is blocked if they have books currently issued.
- Book availability updates automatically on issue and return using atomic transactions.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
