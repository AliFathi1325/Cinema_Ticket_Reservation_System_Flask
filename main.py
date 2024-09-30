import sqlite3
from datetime import datetime

class UserAuth:
    def __init__(self, db_path='cinema.db'):
        """ایجاد اتصال به دیتابیس"""
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def register(self, username, password, email):
        try:
            self.cursor.execute('''
                INSERT INTO users (username, password, email)
                VALUES (?, ?, ?)
            ''', (username, password, email))
            self.conn.commit()
            return "Registration successful."
        except sqlite3.IntegrityError as e:
            return f"Error: {e}. Username or email already exists."

    def login(self, username, password):
        """ورود کاربر و اعتبارسنجی رمز عبور"""
        self.cursor.execute('''
            SELECT * FROM users WHERE username=? AND password=?
        ''', (username, password))
        user = self.cursor.fetchone()
        if user:
            return "Login successful."
        else:
            return "Login failed. Invalid username or password.", False


    def close(self):
        """بستن اتصال به دیتابیس"""
        self.conn.close()

class AdminAuth:
    def __init__(self, db_path='cinema.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def users_tible(self):
        self.cursor.execute("SELECT * FROM users;")
        users = self.cursor.fetchall()
        users_list = []
        for user_data in users:
            clean_text = f"User ID: {user_data[0]}\nUsername: {user_data[1]}\nEmail: {user_data[3]}\nStatus: {'Active' if user_data[4] == 1 else 'Inactive'}"
            users_list.append(clean_text)
        return users_list

    def screening_movies_tible(self):
        self.cursor.execute('SELECT * FROM movies')
        movies = self.cursor.fetchall()
        today = datetime.today().strftime("%Y-%m-%d")
        today = datetime.strptime(today, "%Y-%m-%d")
        movies_list = []
        for movie in movies:
            date_object = datetime.strptime(movie[8], "%Y-%m-%d")
            if date_object >= today:
                clean_text = f"""
    Title: {movie[1]}
    Director: {movie[2]}
    Genre: {movie[3]}
    Story: {movie[4]}
    Year of Manufacture: {movie[5]}
    All Seats: {movie[6]}
    Available Seats: {movie[7]}
    Release Date: {movie[8]}
    """
                movies_list.append((clean_text, movie[0]))
        return movies_list

    def released_movies_tible(self):
        self.cursor.execute('SELECT * FROM movies')
        movies = self.cursor.fetchall()
        today = datetime.today().strftime("%Y-%m-%d")
        today = datetime.strptime(today, "%Y-%m-%d")
        movies_list = []
        for movie in movies:
            date_object = datetime.strptime(movie[8], "%Y-%m-%d")
            if date_object < today:
                clean_text = f"""
    Title: {movie[1]}
    Director: {movie[2]}
    Genre: {movie[3]}
    Story: {movie[4]}
    Year of Manufacture: {movie[5]}
    All Seats: {movie[6]}
    Available Seats: {movie[7]}
    Release Date: {movie[8]}
    """
                movies_list.append(clean_text)
        return movies_list

    def history_reservations_tible(self):
        self.cursor.execute("SELECT * FROM reservations;")
        reservations = self.cursor.fetchall()
        reservations_list = []
        for reservation in reservations:
            self.cursor.execute('SELECT username FROM users WHERE id = ?', (reservation[1],))
            username_result = self.cursor.fetchone()
            username = username_result[0]
            self.cursor.execute('SELECT title FROM movies WHERE id = ?', (reservation[2],))
            title_result = self.cursor.fetchone()
            title = title_result[0]
            self.conn.commit()
            reservations_list.append(f'Reservation ID: {reservation[0]}\n{username} bought {reservation[3]} tickets for {title} movie')
        return reservations_list

    def add_film(self, title, director, genre, story, year_manufacture, all_seats, release_date):
        try:
            available_seats = all_seats
            self.cursor.execute('''
                INSERT INTO movies (title, director, genre, story, year_manufacture, all_seats, available_seats, release_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, director, genre, story, year_manufacture, all_seats, available_seats, release_date))
            self.conn.commit()
            return 'Video added successfully!'
        except sqlite3.Error as e:
            return f"Error adding video: {e}"

    def close(self):
        self.conn.close()

class ReservationAuth:
    def __init__(self, db_path='cinema.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.cursor = self.conn.cursor()

    def reserve_seats(self, user_id, movie_id, num_seats):
        # Fetch available seats for the movie
        self.cursor.execute('SELECT available_seats FROM movies WHERE id = ?', (movie_id,))
        result = self.cursor.fetchone()
        if result is None:
            return 'Movie not found.'
        available_seats = result[0]
        if available_seats >= num_seats:
            self.cursor.execute('''
                UPDATE movies
                SET available_seats = available_seats - ?
                WHERE id = ?
            ''', (num_seats, movie_id))
            self.cursor.execute('''
                INSERT INTO reservations (user_id, movies_id, seats)
                VALUES (?, ?, ?)
            ''', (user_id, movie_id, num_seats))
            self.cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
            username_result = self.cursor.fetchone()
            username = username_result[0]
            self.cursor.execute('SELECT title FROM movies WHERE id = ?', (movie_id,))
            title_result = self.cursor.fetchone()
            title = title_result[0]
            self.conn.commit()
            return f'{num_seats} seat has been successfully reserved for user {username} in movie {title}.'
        else:
            return 'This number of seats is not available.'

    def username_id(self, username):
        self.cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = self.cursor.fetchone()
        return user_id[0]

    def history_reservations(self, username):
        self.cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        userid_result = self.cursor.fetchone()
        userid = userid_result[0]
        self.cursor.execute('''
            SELECT * FROM reservations
            WHERE user_id = ?
        ''', (userid,))
        reservations = self.cursor.fetchall()
        reservations_list = []
        for reservation in reservations:
            self.cursor.execute('SELECT username FROM users WHERE id = ?', (reservation[1],))
            username_result = self.cursor.fetchone()
            username = username_result[0]
            self.cursor.execute('SELECT title FROM movies WHERE id = ?', (reservation[2],))
            title_result = self.cursor.fetchone()
            title = title_result[0]
            self.conn.commit()
            reservations_list.append(f'{username} bought {reservation[3]} tickets for {title} movie')
        return reservations_list

    def close(self):
        self.cursor.close()
        self.conn.close()
