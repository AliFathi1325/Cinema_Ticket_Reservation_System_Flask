<!-- @format -->

# Cinema Booking System whit Flask

This is a simple cinema booking system built with Flask and SQLite. Users can sign up, log in, view movie listings, and make reservations for available movies. There is also an admin interface for managing movies and viewing all user reservations.

## Features

- User registration and login system.
- Admin and user dashboard.
- Users can view movies and make reservations.
- Admin can add new movies, view current screenings, and released movies.
- Movie listings with seat availability.
- Admin-only access to manage movie screenings and reservations.

## Installation

### Prerequisites

- Python 3.x
- Flask
- SQLite3 (pre-installed with Python)

### Step 1: Clone the repository

```bash
git clone https://github.com/AliFathi1325/Cinema_Ticket_Reservation_System_Flask.git
cd cinema-booking-system
```

### Step 2: Set up the virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize the database

The database is initialized with SQLite using the `models.py` file. It creates tables for users, movies, and reservations. It also inserts a default admin user.

```bash
python models.py
```

### Step 5: Run the application

```bash
python app.py
```

Visit `http://127.0.0.1:5000/` in your browser to access the application.

## Default Admin Credentials

- Username: `admin`
- Password: `123`
- Email: `admin@example.com`

## Project Structure

## Usage

1. **Sign up**: New users can register by visiting the signup page.
2. **Login**: After signing up, users can log in with their credentials.
3. **Dashboard**: Users will be directed to their dashboard to view reservation history.
4. **Movie Listings**: On the home page, users can view available movies.
5. **Admin Functions**: The admin user can manage movies and view reservations.

## Admin Access

To access the admin functionality, login with the default admin credentials, or modify the database to set `is_admin = 1` for any user in the `users` table.
