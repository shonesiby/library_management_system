# ──────────────────────────────────────────────────────────────
#  books.py  –  Book Management Module (CRUD + Search)
# ──────────────────────────────────────────────────────────────

from db import get_connection, close_connection
from utils import print_header, print_table, input_int, confirm


# ─────────────────────────── CREATE ───────────────────────────

def add_book():
    print_header("Add New Book")
    title   = input("  Title        : ").strip()
    author  = input("  Author       : ").strip()
    category= input("  Category     : ").strip()
    isbn    = input("  ISBN         : ").strip()
    copies  = input_int("  Total Copies : ", min_val=1)

    if not all([title, author, category, isbn]):
        print("  [!] All fields are required.")
        return

    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO books (title, author, category, isbn, total_copies, available)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (title, author, category, isbn, copies, copies)
        )
        conn.commit()
        print(f"\n  ✅ Book '{title}' added successfully (ID: {cursor.lastrowid}).")
    except Exception as e:
        print(f"\n  [!] Error: {e}")
    finally:
        close_connection(conn, cursor)


# ─────────────────────────── READ ─────────────────────────────

def view_all_books():
    print_header("All Books")
    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT book_id, title, author, category, isbn,
                      total_copies, available, DATE(added_on)
               FROM books ORDER BY book_id"""
        )
        rows = cursor.fetchall()
        headers = ["ID", "Title", "Author", "Category", "ISBN",
                   "Total", "Available", "Added On"]
        print_table(headers, rows)
    finally:
        close_connection(conn, cursor)


def get_book_by_id(book_id: int):
    """Return a single book row dict, or None."""
    conn   = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
        return cursor.fetchone()
    finally:
        close_connection(conn, cursor)


# ─────────────────────────── UPDATE ───────────────────────────

def update_book():
    print_header("Update Book")
    view_all_books()
    book_id = input_int("\n  Enter Book ID to update: ", min_val=1)
    book    = get_book_by_id(book_id)
    if not book:
        print("  [!] Book not found.")
        return

    print(f"\n  Editing: [{book['book_id']}] {book['title']}")
    print("  (Press ENTER to keep current value)\n")

    title    = input(f"  Title        [{book['title']}]    : ").strip() or book['title']
    author   = input(f"  Author       [{book['author']}]   : ").strip() or book['author']
    category = input(f"  Category     [{book['category']}] : ").strip() or book['category']
    isbn     = input(f"  ISBN         [{book['isbn']}]     : ").strip() or book['isbn']
    total    = input(f"  Total Copies [{book['total_copies']}]            : ").strip()
    total    = int(total) if total.isdigit() else book['total_copies']

    # Recalculate available based on issued books
    issued_count = book['total_copies'] - book['available']
    new_available = max(0, total - issued_count)

    if not confirm("\n  Confirm update? (y/n): "):
        print("  Update cancelled.")
        return

    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE books
               SET title=%s, author=%s, category=%s, isbn=%s,
                   total_copies=%s, available=%s
               WHERE book_id=%s""",
            (title, author, category, isbn, total, new_available, book_id)
        )
        conn.commit()
        print(f"\n  ✅ Book ID {book_id} updated successfully.")
    except Exception as e:
        print(f"\n  [!] Error: {e}")
    finally:
        close_connection(conn, cursor)


# ─────────────────────────── DELETE ───────────────────────────

def delete_book():
    print_header("Delete Book")
    view_all_books()
    book_id = input_int("\n  Enter Book ID to delete: ", min_val=1)
    book    = get_book_by_id(book_id)
    if not book:
        print("  [!] Book not found.")
        return

    print(f"\n  About to delete: [{book['book_id']}] {book['title']}")
    if not confirm("  This will also remove all issue records. Confirm? (y/n): "):
        print("  Deletion cancelled.")
        return

    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
        conn.commit()
        print(f"\n  ✅ Book ID {book_id} deleted successfully.")
    except Exception as e:
        print(f"\n  [!] Error: {e}")
    finally:
        close_connection(conn, cursor)


# ─────────────────────────── SEARCH ───────────────────────────

def search_books():
    print_header("Search Books")
    print("  Search by:")
    print("   1. Title")
    print("   2. Author")
    print("   3. Category")
    print("   4. ISBN")
    choice = input_int("  Enter choice: ", 1, 4)

    field_map = {1: ("title", "Title"), 2: ("author", "Author"),
                 3: ("category", "Category"), 4: ("isbn", "ISBN")}
    field, label = field_map[choice]
    keyword = input(f"  Enter {label}: ").strip()

    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""SELECT book_id, title, author, category, isbn,
                       total_copies, available
                FROM books
               WHERE {field} LIKE %s
               ORDER BY book_id""",
            (f"%{keyword}%",)
        )
        rows = cursor.fetchall()
        headers = ["ID", "Title", "Author", "Category", "ISBN", "Total", "Available"]
        print(f"\n  Results for '{keyword}' in {label}:")
        print_table(headers, rows)
    finally:
        close_connection(conn, cursor)
