from flask import Flask

app = Flask(__name__)
app.secret_key = '123'  

from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, Blueprint, session, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor


cinema = Blueprint("cinema", __name__)

# Подключение библиотеки psycopg2 для взаимодействия с PostgreSQL
def dbConnect():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="DBsmakcinema",
        user="smakcinema",
        password="123")
    return conn;

# Закрытие соединения с БД
def dbClose(cursor, connection):
    cursor.close()
    connection.close()


login_manager = LoginManager(app)
login_manager.login_view = 'cinema.LoginPage'
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):

    conn = dbConnect()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute("SELECT id, username FROM \"User\" WHERE id = %s", (user_id,))
    result = cur.fetchone()
    dbClose(cur, conn)

    if result is not None:
        user = User(id=result['id'], username=result['username'])
        return user
    return None



def get_current_user():
    return current_user

def get_current_user_id():
    if current_user.is_authenticated:
        return current_user.id
    return None
@cinema.route('/login', methods=["GET", "POST"])
def loginPage():
    errors = ""

    # Обработка GET-запроса
    if request.method == "GET":
        return render_template("login.html", errors=errors)

    username = request.form.get("username")
    password = request.form.get("password")

    # Проверка наличия значений username и password
    if not (username and password):
        errors = "Пожалуйста, заполните все поля"
        return render_template("login.html", errors=errors)

    conn = dbConnect()
    cur = conn.cursor(cursor_factory=DictCursor)

    # Выполнение SQL-запроса для проверки логина и пароля
    cur.execute("SELECT id, password FROM \"User\" WHERE username = %s", (username,))
    result = cur.fetchone()

    # Проверка результата запроса
    if result is None:
        errors = "Неправильный логин или пароль"
        dbClose(cur, conn)
        return render_template("login.html", errors=errors)

    userID, hashPassword = result
    # Проверка совпадения хешированного пароля
    if check_password_hash(hashPassword, password):
        user = User(id=userID, username=username)
        login_user(user)
        dbClose(cur, conn)
        return redirect("/afisha")
    else:
        errors = "Неправильный логин или пароль"
        return render_template("login.html", errors=errors)

@cinema.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@cinema.route('/')
def index():
    return redirect('/afisha')

@cinema.route('/register', methods=["GET", "POST"])
def registerPage():
    errors = ""

    # Обработка GET-запроса
    if request.method == "GET":
        return render_template("register.html", errors=errors)

    username = request.form.get("username")
    password = request.form.get("password")

    # Проверка наличия значений username и password
    if not (username and password):  # Исправлено здесь
        errors = "Пожалуйста, заполните все поля"
        print(errors)
        return render_template("register.html", errors=errors)

    # Хеширование пароля и подключение к БД
    hashPassword = generate_password_hash(password)
    conn = dbConnect()
    cur = conn.cursor()

    # Проверка наличия пользователя с указанным именем
    cur.execute("SELECT username FROM \"User\" WHERE username = %s", (username,))  # Исправлено здесь
    if cur.fetchone() is not None:
        errors = "Пользователь с данным именем уже существует"
        dbClose(cur, conn)
        return render_template("register.html", errors=errors)

    # Вставка нового пользователя в БД
    cur.execute("INSERT INTO \"User\" (username, password) VALUES (%s, %s)", (username, hashPassword))  # Исправлено здесь
    conn.commit()
    dbClose(cur, conn)
    return redirect("/login")


def get_movies_from_database():
    conn = dbConnect()
    cur = conn.cursor()

    cur.execute("SELECT id, title FROM \"Movie\"")  # Note the use of double quotes around "Movie"
    
    # Получаем результат запроса
    result = cur.fetchall()

    dbClose(cur, conn)

    # Возвращаем список фильмов
    return [{'id': movie_id, 'title': title} for movie_id, title in result] if result is not None else []


@cinema.route('/afisha')

def billboard():
    movies = get_movies_from_database()  # Получаем фильмы из базы данных
    return render_template('billboard.html', movies=movies)


@cinema.route('/sessions')
def sessions():
    current_user = get_current_user_id()
    if current_user is None:
        return redirect('/login')
    conn = dbConnect()
    cur = conn.cursor()


    cur.execute("SELECT \"Session\".id, \"Session\".date_time, \"Movie\".title FROM \"Session\" JOIN \"Movie\" ON \"Session\".movie_id = \"Movie\".id")
    sessions = cur.fetchall()

    # Обновление состояния мест в каждом сеансе
    updated_sessions = []
    for session in sessions:
        # Получаем забронированные места для данного сеанса
        cur.execute("SELECT seat_number FROM \"Reservation\" WHERE session_id = %s", (session[0],))
        reserved_seats = [seat[0] for seat in cur.fetchall()]
        available_seats = [i for i in range(1, 31) if i not in reserved_seats]
        
        # Создаем словарь с данными сеанса и местами
        session_data = {
            'id': session[0],
            'date_time': session[1],
            'title': session[2],
            'seats': available_seats
        }
        
        updated_sessions.append(session_data)

    conn.close()

    return render_template('sessions.html', sessions=updated_sessions, current_user=current_user)


@cinema.route('/reserve_seat/<int:session_id>', methods=['POST'])
def reserve_seat(session_id):
    conn = dbConnect()
    cur = conn.cursor()

    try:
        selected_seat = request.form.get('seat')  # Используйте правильное имя поля из вашей формы HTML
        # Проверяем, что место доступно для бронирования
        cur.execute("SELECT * FROM \"Reservation\" WHERE session_id = %s AND seat_number = %s", (session_id, selected_seat))
        existing_reservation = cur.fetchone()

        if existing_reservation:
            # Место уже забронировано, обработайте этот случай по вашему усмотрению
            return "Место уже забронировано"
        # Проверка на количество бронирований
        cur.execute("SELECT COUNT(*) FROM \"Reservation\" WHERE user_id = %s", (current_user.id,))
        num_reservations = cur.fetchone()[0]

        if num_reservations >= 5:
            return "Вы не можете забронировать больше 5 мест"

        # Бронируем место
        cur.execute("INSERT INTO \"Reservation\" (session_id, user_id, seat_number) VALUES (%s, %s, %s)", (session_id, current_user.id, selected_seat))
        conn.commit()

        return redirect(url_for('cinema.sessions'))

    except Exception as e:
        # Обработка ошибок
        print(f"Error reserving seat: {e}")
        print(f"selected_seat: {selected_seat}")
        conn.rollback()
        return "Ошибка бронирования места"



    finally:
        conn.close()

def get_user_info(user_id):
    conn = dbConnect()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM \"User\" WHERE id = %s", (user_id,))
        user_info = cur.fetchone()
        return user_info
    
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None
    
    finally:
        conn.close()

def get_user_reservations(user_id):
    conn = dbConnect()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT 
                "Reservation".*,
                "Session"."date_time",
                "Movie"."title"  -- Добавляем название фильма
            FROM "Reservation"
            JOIN "Session" ON "Reservation".session_id = "Session".id
            JOIN "Movie" ON "Session".movie_id = "Movie".id  -- Присоединяем таблицу Movie
            WHERE "Reservation".user_id = %s
        """, (user_id,))
        reservations = cur.fetchall()
        return reservations
    
    except Exception as e:
        print(f"Error getting user reservations: {e}")
        return None
    
    finally:
        conn.close()





@cinema.route('/my_account')
def my_account():
    user_id = get_current_user_id()
    print(f"Current User ID: {user_id}")
    if user_id is None:
        return redirect('/login')
    
    # Получаем информацию о пользователе и забронированных сеансах
    user_info = get_user_info(user_id)
    reservations = get_user_reservations(user_id)

    # Печатаем информацию для отладки
    print(f"User Info: {user_info}")
    print(f"Reservations: {reservations}")

    return render_template('my_account.html', user_info=user_info, reservations=reservations)


from flask import redirect, url_for, flash

@cinema.route('/delete_account', methods=['POST'])
def delete_account():
    user_id = get_current_user_id()  # Получите ID текущего пользователя
    if user_id is not None:
        conn = dbConnect()
        cur = conn.cursor()

        try:
            # Удаление пользователя и связанных данных из базы данных
            cur.execute("DELETE FROM \"Reservation\" WHERE user_id = %s", (user_id,))
            cur.execute("DELETE FROM \"User\" WHERE id = %s", (user_id,))
            conn.commit()

            flash('Your account has been successfully deleted.', 'success')
            return redirect(url_for('cinema.logout'))  # Предполагается, что у вас есть функция logout для выхода из системы

        except Exception as e:
            print(f"Error deleting account: {e}")
            conn.rollback()
            flash('Error deleting account. Please try again later.', 'error')

        finally:
            conn.close()

    return redirect(url_for('cinema.loginPage'))



@cinema.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    conn = dbConnect()
    cur = conn.cursor()

    try:

        cur.execute("DELETE FROM \"Reservation\" WHERE id = %s", (reservation_id,))
        conn.commit()

        return redirect(url_for('cinema.my_account'))

    except Exception as e:
        print(f"Error cancelling reservation: {e}")
        conn.rollback()
        return "Error cancelling reservation"

    finally:
        conn.close()


# Пример маршрутов для администратора
@cinema.route('/admin')
@login_required  # Декоратор для проверки, что пользователь авторизован
def admin_dashboard():
    # Проверяем, является ли пользователь администратором
    if current_user.is_admin:
        return render_template('admin_dashboard.html', user=current_user)
    else:
        return abort(403)  # Возвращаем ошибку 403 Forbidden, если пользователь не администратор

@cinema.route('/admin/create_session', methods=['GET', 'POST'])
@login_required
def create_session():
    if current_user.is_admin:
        if request.method == 'POST':
            # Обработка создания нового сеанса
            # ...
            flash('Session created successfully', 'success')
            return redirect(url_for('cinema.admin_dashboard'))
        else:
            # Отображение формы для создания сеанса
            # ...
            return render_template('create_session.html')
    else:
        return abort(403)

# Добавьте аналогичные маршруты для удаления сеанса и снятия брони

app.register_blueprint(cinema)
