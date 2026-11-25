# ──────────────────────────────────────────────────────────────
#  transactions.py  –  Issue & Return Book Module
# ──────────────────────────────────────────────────────────────

from datetime import date, timedelta
from db import get_connection, close_connection
from utils import print_header, print_table, input_int, confirm
from books import view_all_books, get_book_by_id
from members import view_all_members, get_member_by_id


DEFAULT_LOAN_DAYS = 14   # 2-week loan period


# ───────────────── ISSUE BOOK ──────────────────

def issue_book():
    print_header("Issue Book to Member")

    # Pick member
    view_all_members()
    member_id = input_int("\n  Enter Member ID: ", min_val=1)
    member    = get_member_by_id(member_id)
    if not member:
        print("  [!] Member not found.")
        return

    # Pick book
    view_all_books()
    book_id = input_int("\n  Enter Book ID: ", min_val=1)
    book    = get_book_by_id(book_id)
    if not book:
        print("  [!] Book not found.")
        return
    if book['available'] <= 0:
        print(f"  [!] Sorry, '{book['title']}' has no copies available.")
        return

    # Check if member already issued same book and hasn't returned
    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT COUNT(*) FROM issued_books
               WHERE book_id=%s AND member_id=%s AND status='issued'""",
            (book_id, member_id)
        )
        already = cursor.fetchone()[0]
        if already:
            print("  [!] This member already has this book issued.")
            return

        due_date = date.today() + timedelta(days=DEFAULT_LOAN_DAYS)
        print(f"\n  Issuing  : {book['title']}")
        print(f"  To       : {member['name']}")
        print(f"  Due Date : {due_date}")
        if not confirm("\n  Confirm issue? (y/n): "):
            print("  Issue cancelled.")
            return

        # Insert issue record
        cursor.execute(
            """INSERT INTO issued_books (book_id, member_id, due_date, status)
               VALUES (%s, %s, %s, 'issued')""",
            (book_id, member_id, due_date)
        )
        # Decrement available count
        cursor.execute(
            "UPDATE books SET available = available - 1 WHERE book_id = %s",
            (book_id,)
        )
        conn.commit()
        print(f"\n  ✅ Book issued successfully! Due back by {due_date}.")
    except Exception as e:
        conn.rollback()
        print(f"\n  [!] Error: {e}")
    finally:
        close_connection(conn, cursor)


# ───────────────── RETURN BOOK ─────────────────

def return_book():
    print_header("Return Book")

    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        # Show all currently issued books
        cursor.execute(
            """SELECT ib.issue_id, b.title, m.name, ib.issued_on, ib.due_date,
                      CASE WHEN ib.due_date < CURDATE() THEN 'OVERDUE' ELSE 'On time' END AS status
               FROM issued_books ib
               JOIN books b   ON ib.book_id   = b.book_id
               JOIN members m ON ib.member_id = m.member_id
               WHERE ib.status = 'issued'
               ORDER BY ib.due_date"""
        )
        rows = cursor.fetchall()
        headers = ["Issue ID", "Book Title", "Member", "Issued On", "Due Date", "Status"]
        print_table(headers, rows)

        if not rows:
            return

        issue_id = input_int("\n  Enter Issue ID to return: ", min_val=1)

        # Validate issue ID
        cursor.execute(
            """SELECT ib.issue_id, ib.book_id, b.title, m.name
               FROM issued_books ib
               JOIN books b   ON ib.book_id   = b.book_id
               JOIN members m ON ib.member_id = m.member_id
               WHERE ib.issue_id=%s AND ib.status='issued'""",
            (issue_id,)
        )
        record = cursor.fetchone()
        if not record:
            print("  [!] Issue record not found or already returned.")
            return

        _, book_id, book_title, member_name = record
        print(f"\n  Returning : {book_title}")
        print(f"  Returned by: {member_name}")
        if not confirm("\n  Confirm return? (y/n): "):
            print("  Return cancelled.")
            return

        # Mark returned
        cursor.execute(
            """UPDATE issued_books
               SET status='returned', returned_on=NOW()
               WHERE issue_id=%s""",
            (issue_id,)
        )
        # Increment available count
        cursor.execute(
            "UPDATE books SET available = available + 1 WHERE book_id = %s",
            (book_id,)
        )
        conn.commit()
        print(f"\n  ✅ '{book_title}' returned successfully.")
    except Exception as e:
        conn.rollback()
        print(f"\n  [!] Error: {e}")
    finally:
        close_connection(conn, cursor)
