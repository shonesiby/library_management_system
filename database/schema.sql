-- ============================================================
--  Library Management System – MySQL Schema
--  Run this file in MySQL Workbench once before starting the app
-- ============================================================

CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- ─────────────────────────────────────────
--  BOOKS TABLE
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS books (
    book_id       INT            AUTO_INCREMENT PRIMARY KEY,
    title         VARCHAR(200)   NOT NULL,
    author        VARCHAR(150)   NOT NULL,
    category      VARCHAR(100)   NOT NULL,
    isbn          VARCHAR(20)    UNIQUE NOT NULL,
    total_copies  INT            NOT NULL DEFAULT 1,
    available     INT            NOT NULL DEFAULT 1,
    added_on      TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_copies CHECK (total_copies >= 0),
    CONSTRAINT chk_available CHECK (available >= 0)
);

-- ─────────────────────────────────────────
--  MEMBERS TABLE
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS members (
    member_id    INT           AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(150)  NOT NULL,
    email        VARCHAR(150)  UNIQUE NOT NULL,
    phone        VARCHAR(15)   NOT NULL,
    address      TEXT,
    joined_on    TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
--  ISSUED BOOKS TABLE
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS issued_books (
    issue_id     INT        AUTO_INCREMENT PRIMARY KEY,
    book_id      INT        NOT NULL,
    member_id    INT        NOT NULL,
    issued_on    TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
    due_date     DATE       NOT NULL,
    returned_on  TIMESTAMP  NULL,
    status       ENUM('issued','returned') DEFAULT 'issued',
    FOREIGN KEY (book_id)   REFERENCES books(book_id)   ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- ─────────────────────────────────────────
--  SAMPLE DATA (optional – remove if not needed)
-- ─────────────────────────────────────────
INSERT IGNORE INTO books (title, author, category, isbn, total_copies, available) VALUES
('The Pragmatic Programmer', 'Andrew Hunt',       'Technology',  '978-0135957059', 3, 3),
('Clean Code',               'Robert C. Martin',  'Technology',  '978-0132350884', 2, 2),
('To Kill a Mockingbird',    'Harper Lee',         'Fiction',     '978-0061935466', 4, 4),
('1984',                     'George Orwell',      'Fiction',     '978-0451524935', 3, 3),
('Sapiens',                  'Yuval Noah Harari',  'History',     '978-0062316097', 2, 2);

INSERT IGNORE INTO members (name, email, phone, address) VALUES
('Alice Johnson', 'alice@example.com', '9876543210', '123 Maple St, Springfield'),
('Bob Smith',     'bob@example.com',   '9876543211', '456 Oak Ave, Shelbyville');
