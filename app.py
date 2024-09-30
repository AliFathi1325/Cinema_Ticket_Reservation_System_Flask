from flask import Flask, render_template, request, redirect, url_for, session
from main import UserAuth, AdminAuth, ReservationAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

@app.route('/')
def home():
    admin_auth = AdminAuth()
    screening_filmt_tible = admin_auth.screening_movies_tible()
    released_filmt_tible = admin_auth.released_movies_tible()
    admin_auth.close()
    return render_template('home.html', screening_filmt_tible=screening_filmt_tible, released_filmt_tible=released_filmt_tible)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        auth = UserAuth()
        auth.register(username, password, email)
        auth.close()
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        auth = UserAuth()
        login_status = auth.login(username, password)

        if login_status == 'Login successful.':
            session['username'] = username
            auth.close()
            if username == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('dashboard'))
        else:
            auth.close()
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        reservation_auth = ReservationAuth()
        history_reservations = reservation_auth.history_reservations(username)
        reservation_auth.close()
        return render_template('dashboard.html', username=username, history_reservations=history_reservations)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['username'] == 'admin':
        admin_auth = AdminAuth()
        users_tible = admin_auth.users_tible()
        screening_filmt_tible = admin_auth.screening_movies_tible()
        released_filmt_tible = admin_auth.released_movies_tible()
        history_reservations_tible = admin_auth.history_reservations_tible()
        admin_auth.close()
        return render_template('admin.html', users_tible=users_tible, screening_filmt_tible=screening_filmt_tible, released_filmt_tible=released_filmt_tible, history_reservations_tible=history_reservations_tible)
    return "You do not have permission to access this page."

@app.route('/submit_add_film', methods=['POST'])
def submit():
    title = request.form['title']
    director = request.form['director']
    genre = request.form['genre']
    story = request.form['story']
    year_manufacture = request.form['year_manufacture']
    all_seats = request.form['all_seats']
    release_date = request.form['release_date']
    admin_auth = AdminAuth()
    result_message = admin_auth.add_film(
    title, director, genre, story, year_manufacture, all_seats, release_date
    )
    admin_auth.close()
    return render_template('message.html', message=result_message)

@app.route('/handle_movie_action', methods=['POST'])
def handle_movie_action():
    movie_id = request.form.get('movie_id')
    seats = request.form.get('seats')
    username = session['username']
    reservation_auth = ReservationAuth()
    user_id = reservation_auth.username_id(str(username))
    message = reservation_auth.reserve_seats(user_id, int(movie_id), int(seats))
    reservation_auth.close()
    return render_template('message.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
