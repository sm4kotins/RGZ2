from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, Blueprint, session
import psycopg2
lab5 =Blueprint("lab5", __name__)

def dbConnect():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="knowledge_base",
        user="egor_knowledge_base",
        password="admin")
    return conn;

def dbClose(cursor, connection):
    cursor.close ()
    connection.close()


@lab5.route("/lab5")
def main():
    visibleUser = "Аноним"
    if 'username' in session:
        visibleUser = session['username']
    return render_template('lab5.html', username=visibleUser)


@lab5.route("/lab5/users")
def users():
    # Прописываем параметры подключения к БД
    conn=dbConnect()
    # Получаем курсор. С помощью него мы можем выполнять SQL-запросы
    cur = conn.cursor()
    # Пишем запрос, который psycopg2 должен выполнить
    cur.execute("SELECT username FROM users;")
    # fetchall - получить все строки, которые получились в результате выполнения SQL-запроса в execute
    # Сохраняем эти строки в переменную result
    result = cur.fetchall()
    # Закрываем соединение с БД
    dbClose(cur,conn)
    
    # Создаем список имен пользователей из результата запроса
    user_names = [user[0] for user in result]
    
    # Возвращаем HTML-страницу, передавая список имен пользователей в шаблон
    return render_template('users.html', users=user_names)


@lab5.route('/lab5/register', methods=["GET"
, "POST"])
def registerPage():
    errors = ""
    # Если это метод GET, то верни шаблон и заверши выполнение
    if request.method == "GET":
        return render_template("register.html", errors=errors)
    # Если мы попали сюда, значит это метод POST, # так как GET мы уже обработали и сделали return.
    # После return функция немедленно завершается
    username = request. form.get ("username")
    password = request.form.get ("password")
    # Провряем username и password на пустоту
    # Если любой из них пустой, то добавляем ошибку # и рендерим шаблон
    if not (username or password):
        errors = "Пожалуйста, заполните все поля"
        print(errors)
        return render_template("register.html", errors=errors)
    # Если мы попали сюда, значит username и password заполненны
    # Подключаемся к БД
    hashPassword = generate_password_hash(password)
    conn = dbConnect()
    cur = conn.cursor()
    # Проверяем наличие клиента в базе
    # У нас не может быть два пользователя с одинаковыми логинами
    # WARNING: мы используем f-строки, что не рекомендуется делать # позже мы разберемся с Вами почему не стоит так делать
    cur.execute(f"SELECT username FROM users WHERE username = '{username}';")
    # fetchone, в отличие, от fetchall, получает только одну строку # мы задали свойство UNIQUE для пользователя, значит # больше одной строки мы не можем получить
    # Только один пользователь с таким именем может быть в БД
    if cur.fetchone() is not None:
        errors = "Пользователь с данным именем уже существует"
        dbClose (cur, conn)
        return render_template("register.html", errors=errors)
    # Если мы попали сюда, то значит в cur.fetchone нет ни одной строки # значит пользователя с таким же логином не существует
    cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{hashPassword}');")
    conn.commit()
    dbClose (cur, conn)
    return redirect("/lab5/login")


@lab5.route('/lab5/login', methods=["GET", "POST"])
def loginPage():
    errors = "";
    if request.method == "GET":
        return render_template("login2.html", errors=errors)

    username = request.form.get ("username")
    password = request.form.get("password")
    if not (username or password):
        errors = "Пожалуйста, заполните все поля"
        return render_template("login2.html", errors=errors)
    conn = dbConnect ()
    cur = conn.cursor ()
    cur.execute(F"SELECT id, password FROM users WHERE username = '{username}'")
# OUTPUT = (idValue, passwordValue)
# INDEX
    result = cur.fetchone()
    if result is None:
        errors.append ("Неправильный логин или пароль")
        dbClose (cur, conn)
        return render_template("login.html", errors=errors)
    userID, hashPassword = result
# С помощью check_password_hash сравниваем хэш и # пароль из базы данных. Функция "check_password_hash" # сама переведет password в хэш
# С помощью check_password_hash сравниваем хэш # пароль из базы данных. Функция "check_password_hash" # сама переведет password в хэш
    if check_password_hash(hashPassword, password) :
    # Пароль правильный
    # Сохраняем id и username # в сессию (JWT токен)
        session['id'] = userID
        session ['username'] = username
        dbClose (cur, conn)
        return redirect("/lab5")
    else:
        errors = "Неправильный логин или пароль"
        return render_template("login2.html", errors=errors)