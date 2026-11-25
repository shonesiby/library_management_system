# ──────────────────────────────────────────────────────────────
#  members.py  –  Member Management Module (CRUD)
# ──────────────────────────────────────────────────────────────

from db import get_connection, close_connection
from utils import print_header, print_table, input_int, confirm
import re


# ─────────────── helpers ───────────────

def _valid_email(email: str) -> bool:
    return bool(re.match(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$", email))

def _valid_phone(phone: str) -> bool:
    return phone.isdigit() and 7 <= len(phone) <= 15


# ─────────────── CREATE ────────────────

def add_member():
    print_header("Register New Member")
    name    = input("  Full Name : ").strip()
    email   = input("  Email     : ").strip()
    phone   = input("  Phone     : ").strip()
    address = input("  Address   : ").strip()

    if not name:
        print("  [!] Name is required.")
        return
    if not _valid_email(email):
        print("  [!] Invalid email address.")
        return
    if not _valid_phone(phone):
        print("  [!] Phone must be 7-15 digits.")
        return

    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO members (name, email, phone, address) VALUES (%s,%s,%s,%s)",
            (name, email, phone, address)
        )
        conn.commit()
        print(f"\n  ✅ Member '{name}' registered (ID: {cursor.lastrowid}).")
    except Exception as e:
        print(f"\n  [!] Error: {e}")
    finally:
        close_connection(conn, cursor)


# ─────────────── READ ──────────────────

def view_all_members():
    print_header("All Members")
    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT member_id, name, email, phone, address, DATE(joined_on)
               FROM members ORDER BY member_id"""
        )
        rows    = cursor.fetchall()
        headers = ["ID", "Name", "Email", "Phone", "Address", "Joined On"]
        print_table(headers, rows)
    finally:
        close_connection(conn, cursor)


def get_member_by_id(member_id: int):
    """Return a single member row dict, or None."""
    conn   = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM members WHERE member_id=%s", (member_id,))
        return cursor.fetchone()
    finally:
        close_connection(conn, cursor)


# ─────────────── UPDATE ────────────────

def update_member():
    print_header("Update Member")
    view_all_members()
    member_id = input_int("\n  Enter Member ID to update: ", min_val=1)
    member    = get_member_by_id(member_id)
    if not member:
        print("  [!] Member not found.")
        return

    print(f"\n  Editing: [{member['member_id']}] {member['name']}")
    print("  (Press ENTER to keep current value)\n")

    name    = input(f"  Name    [{member['name']}]    : ").strip() or member['name']
    email   = input(f"  Email   [{member['email']}]   : ").strip() or member['email']
    phone   = input(f"  Phone   [{member['phone']}]   : ").strip() or member['phone']
    address = input(f"  Address [{member['address']}] : ").strip() or member['address']

    if email != member['email'] and not _valid_email(email):
        print("  [!] Invalid email.")
        return
    if phone != member['phone'] and not _valid_phone(phone):
        print("  [!] Invalid phone.")
        return

    if not confirm("\n  Confirm update? (y/n): "):
        print("  Update cancelled.")
        return

    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE members SET name=%s, email=%s, phone=%s, address=%s WHERE member_id=%s",
            (name, email, phone, address, member_id)
        )
        conn.commit()
        print(f"\n  ✅ Member ID {member_id} updated successfully.")
    except Exception as e:
        print(f"\n  [!] Error: {e}")
    finally:
        close_connection(conn, cursor)


# ─────────────── DELETE ────────────────

def delete_member():
    print_header("Delete Member")
    view_all_members()
    member_id = input_int("\n  Enter Member ID to delete: ", min_val=1)
    member    = get_member_by_id(member_id)
    if not member:
        print("  [!] Member not found.")
        return

    # Check if member has active issues
    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT COUNT(*) FROM issued_books WHERE member_id=%s AND status='issued'",
            (member_id,)
        )
        active = cursor.fetchone()[0]
        if active > 0:
            print(f"\n  [!] Cannot delete – member has {active} book(s) currently issued.")
            return

        print(f"\n  About to delete: [{member['member_id']}] {member['name']}")
        if not confirm("  Confirm deletion? (y/n): "):
            print("  Deletion cancelled.")
            return

        cursor.execute("DELETE FROM members WHERE member_id=%s", (member_id,))
        conn.commit()
        print(f"\n  ✅ Member ID {member_id} deleted successfully.")
    except Exception as e:
        print(f"\n  [!] Error: {e}")
    finally:
        close_connection(conn, cursor)
