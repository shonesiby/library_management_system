# ──────────────────────────────────────────────────────────────
#  reports.py  –  View Reports Module
# ──────────────────────────────────────────────────────────────

from db import get_connection, close_connection
from utils import print_header, print_table


def report_all_books():
    print_header("Report – All Books")
    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT book_id, title, author, category, isbn,
                      total_copies, available,
                      (total_copies - available) AS issued,
                      DATE(added_on)
               FROM books ORDER BY category, title"""
        )
        rows    = cursor.fetchall()
        headers = ["ID", "Title", "Author", "Category", "ISBN",
                   "Total", "Available", "Issued", "Added On"]
        print_table(headers, rows)
    finally:
        close_connection(conn, cursor)


def report_all_members():
    print_header("Report – All Members")
    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT m.member_id, m.name, m.email, m.phone,
                      COUNT(ib.issue_id) AS total_issued,
                      SUM(CASE WHEN ib.status='issued' THEN 1 ELSE 0 END) AS currently_holding,
                      DATE(m.joined_on)
               FROM members m
               LEFT JOIN issued_books ib ON m.member_id = ib.member_id
               GROUP BY m.member_id
               ORDER BY m.member_id"""
        )
        rows    = cursor.fetchall()
        headers = ["ID", "Name", "Email", "Phone",
                   "Total Issued", "Holding Now", "Joined On"]
        print_table(headers, rows)
    finally:
        close_connection(conn, cursor)


def report_currently_issued():
    print_header("Report – Currently Issued Books")
    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT ib.issue_id, b.title, b.isbn, m.name, m.phone,
                      DATE(ib.issued_on), ib.due_date,
                      DATEDIFF(ib.due_date, CURDATE()) AS days_left,
                      CASE WHEN ib.due_date < CURDATE() THEN '⚠ OVERDUE' ELSE '✓ OK' END AS remark
               FROM issued_books ib
               JOIN books   b ON ib.book_id   = b.book_id
               JOIN members m ON ib.member_id = m.member_id
               WHERE ib.status = 'issued'
               ORDER BY ib.due_date"""
        )
        rows    = cursor.fetchall()
        headers = ["Issue ID", "Book", "ISBN", "Member", "Phone",
                   "Issued On", "Due Date", "Days Left", "Remark"]
        print_table(headers, rows)
    finally:
        close_connection(conn, cursor)


def report_returned_books():
    print_header("Report – Returned Books History")
    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT ib.issue_id, b.title, m.name,
                      DATE(ib.issued_on), ib.due_date, DATE(ib.returned_on),
                      DATEDIFF(ib.returned_on, ib.due_date) AS days_overdue
               FROM issued_books ib
               JOIN books   b ON ib.book_id   = b.book_id
               JOIN members m ON ib.member_id = m.member_id
               WHERE ib.status = 'returned'
               ORDER BY ib.returned_on DESC"""
        )
        rows    = cursor.fetchall()
        headers = ["Issue ID", "Book", "Member",
                   "Issued On", "Due Date", "Returned On", "Days Overdue"]
        print_table(headers, rows)
    finally:
        close_connection(conn, cursor)


def report_overdue():
    print_header("Report – Overdue Books")
    conn   = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT ib.issue_id, b.title, m.name, m.phone,
                      ib.due_date,
                      DATEDIFF(CURDATE(), ib.due_date) AS days_overdue
               FROM issued_books ib
               JOIN books   b ON ib.book_id   = b.book_id
               JOIN members m ON ib.member_id = m.member_id
               WHERE ib.status = 'issued' AND ib.due_date < CURDATE()
               ORDER BY ib.due_date"""
        )
        rows    = cursor.fetchall()
        headers = ["Issue ID", "Book", "Member", "Phone", "Due Date", "Days Overdue"]
        print_table(headers, rows)
        if not rows:
            print("  🎉 No overdue books!")
    finally:
        close_connection(conn, cursor)
