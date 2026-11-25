#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════
#   main.py  –  Library Management System  |  Entry Point
#   Python + MySQL  |  Complete CRUD + Issue/Return + Reports
# ════════════════════════════════════════════════════════════════

from db import get_connection, close_connection
from utils import print_header, input_int

# Module imports
from books import (
    add_book, view_all_books, update_book, delete_book, search_books
)
from members import (
    add_member, view_all_members, update_member, delete_member
)
from transactions import issue_book, return_book
from reports import (
    report_all_books, report_all_members,
    report_currently_issued, report_returned_books, report_overdue
)


# ─────────────────── SUB-MENUS ──────────────────────

def menu_books():
    while True:
        print_header("Book Management")
        print("   1. Add New Book")
        print("   2. View All Books")
        print("   3. Update Book")
        print("   4. Delete Book")
        print("   5. Search Books")
        print("   0. ← Back to Main Menu")
        choice = input_int("\n  Enter choice: ", 0, 5)
        actions = {
            1: add_book,
            2: view_all_books,
            3: update_book,
            4: delete_book,
            5: search_books,
        }
        if choice == 0:
            break
        actions[choice]()
        input("\n  Press ENTER to continue...")


def menu_members():
    while True:
        print_header("Member Management")
        print("   1. Register New Member")
        print("   2. View All Members")
        print("   3. Update Member")
        print("   4. Delete Member")
        print("   0. ← Back to Main Menu")
        choice = input_int("\n  Enter choice: ", 0, 4)
        actions = {
            1: add_member,
            2: view_all_members,
            3: update_member,
            4: delete_member,
        }
        if choice == 0:
            break
        actions[choice]()
        input("\n  Press ENTER to continue...")


def menu_reports():
    while True:
        print_header("View Reports")
        print("   1. All Books (with stock)")
        print("   2. All Members (with issue counts)")
        print("   3. Currently Issued Books")
        print("   4. Returned Books History")
        print("   5. Overdue Books")
        print("   0. ← Back to Main Menu")
        choice = input_int("\n  Enter choice: ", 0, 5)
        actions = {
            1: report_all_books,
            2: report_all_members,
            3: report_currently_issued,
            4: report_returned_books,
            5: report_overdue,
        }
        if choice == 0:
            break
        actions[choice]()
        input("\n  Press ENTER to continue...")


# ─────────────────── MAIN MENU ──────────────────────

BANNER = r"""
╔══════════════════════════════════════════════════════╗
║          📚  LIBRARY MANAGEMENT SYSTEM  📚           ║
╚══════════════════════════════════════════════════════╝
"""


def main():
    # Verify DB connectivity on startup
    conn = get_connection()
    if not conn:
        print("\n  Could not connect to the database. Check config.py and ensure MySQL is running.")
        return
    close_connection(conn)

    while True:
        print(BANNER)
        print("   1.  📖  Book Management")
        print("   2.  👤  Member Management")
        print("   3.  📤  Issue Book")
        print("   4.  📥  Return Book")
        print("   5.  🔍  Search Books")
        print("   6.  📊  View Reports")
        print("   0.  🚪  Exit")
        print()
        choice = input_int("  Enter choice: ", 0, 6)

        if choice == 1:
            menu_books()
        elif choice == 2:
            menu_members()
        elif choice == 3:
            issue_book()
            input("\n  Press ENTER to continue...")
        elif choice == 4:
            return_book()
            input("\n  Press ENTER to continue...")
        elif choice == 5:
            search_books()
            input("\n  Press ENTER to continue...")
        elif choice == 6:
            menu_reports()
        elif choice == 0:
            print("\n  👋  Thank you for using Library Management System. Goodbye!\n")
            break


if __name__ == "__main__":
    main()
