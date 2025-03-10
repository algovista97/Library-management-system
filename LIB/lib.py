import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create tables for books and users
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    available INTEGER DEFAULT 1
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS issued_books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    book_id INTEGER,
                    issue_date TEXT,
                    return_date TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(book_id) REFERENCES books(id)
                )''')

conn.commit()

def add_book(title, author):
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    print(f"Book '{title}' added successfully!")

def issue_book(user_id, book_id, issue_date, return_date):
    cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    if book and book[0] == 1:
        cursor.execute("INSERT INTO issued_books (user_id, book_id, issue_date, return_date) VALUES (?, ?, ?, ?)",
                       (user_id, book_id, issue_date, return_date))
        cursor.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
        conn.commit()
        print("Book issued successfully!")
    else:
        print("Book not available!")

def return_book(book_id):
    cursor.execute("DELETE FROM issued_books WHERE book_id = ?", (book_id,))
    cursor.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
    conn.commit()
    print("Book returned successfully!")

def list_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print("\nAvailable Books:")
    for book in books:
        status = "Available" if book[3] == 1 else "Issued"
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Status: {status}")

# Example Usage:
add_book("The Great Gatsby", "F. Scott Fitzgerald")
add_book("1984", "George Orwell")
list_books()
issue_book(1, 1, "2025-03-10", "2025-03-20")
list_books()
return_book(1)
list_books()

# Close connection
conn.close()
