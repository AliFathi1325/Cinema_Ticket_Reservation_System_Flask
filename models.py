import sqlite3

conn = sqlite3.connect('cinema.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        director TEXT NOT NULL,
        genre TEXT NOT NULL,
        story TEXT,
        year_manufacture INTEGER NOT NULL,
        all_seats INTEGER NOT NULL,
        available_seats INTEGER NOT NULL,
        release_date DATE
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        is_admin INTEGER NOT NULL DEFAULT 0  -- Added is_admin column
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        movies_id INTEGER NOT NULL,
        seats INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (movies_id) REFERENCES movies(id)
    )
''')
cursor.execute('''
        INSERT INTO users (username, password, email, is_admin)
        VALUES (?, ?, ?, ?)
    ''', ('admin', '123', 'admin@example.com', 1))

conn.commit()
conn.close()
