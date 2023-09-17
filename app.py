from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)

@app.route("/menu")
def menu():
    return """
    <!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <h1><a href="/lab1">Лабороторная работа 1</a></h1>

        <footer>
            &copy; Егор Панченко, ФБИ-13, 3 курс, 2023
        </footer>
    </body>
</html>
"""

@app.route("/lab1")
def lab():
    return  """
<!doctype html>
<html>
    <head>
        <title>Панченко Егор Михайлович, лабораторная 1</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <div>Flask — фреймворк для создания веб-приложений на языке программирования Python,
        использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2.
        Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений,
        сознательно предоставляющих лишь самые базовые возможности</div>
        <a href="/menu">Меню</a>
        <h1>Реализованные роуты</h1>
        <ol>
            <li><a href="/lab1/oak">Дуб</a></li>
            <li><a href="/lab1/student">Студент</a></li>
            <li><a href="/lab1/python">Python</a></li>
            <li><a href="/lab1/toner">Llumar</a></li>
        </ol>
        <footer>
            &copy; Егор Панченко, ФБИ-13, 3 курс, 2023
        </footer>
    </body>
</html>
"""

@app.route('/lab1/oak')
def oak():
    return '''
<!doctype html>
<html>
<link rel="stylesheet" href="''' + url_for ('static', filename='lab1.css') + '''">
    <body>
    <h1>Дуб</h1>
    <img src="''' + url_for ('static', filename='oak.jpg') + '''">
    </body>
</html>
'''
@app.route('/lab1/student')
def student():
    return '''
<!doctype html>
<html>
<link rel="stylesheet" href="''' + url_for ('static', filename='lab1.css') + '''">
    <body>
    <h1>Панченко Егор Михайлович</h1>
    <img src="''' + url_for ('static', filename='nstu_logo.jpeg') + '''">
    </body>
</html>
'''
@app.route('/lab1/python')
def python():
    return '''
<!doctype html>
<html>
<link rel="stylesheet" href="''' + url_for ('static', filename='lab1.css') + '''">
    <body>
    <h1>Python — высокоуровневый язык программирования общего назначения с динамической строгой типизацией и автоматическим управлением памятью,
    ориентированный на повышение производительности разработчика, читаемости кода и его качества,
    а также на обеспечение переносимости написанных на нём программ.</h1>
    <img src="''' + url_for ('static', filename='python.jpg') + '''">
    </body>
</html>
'''
@app.route('/lab1/toner')
def toner():
    return '''
<!doctype html>
<html>
<link rel="stylesheet" href="''' + url_for ('static', filename='lab1.css') + '''">
    <body>
    <h1>LLumar – наиболее известный в мире бренд высококачественных оконных пленок.
    Тонировочные, автомобильные, архитектурные и противоударные защитные пленки под маркой Llumar
    производятся в США компанией CPFilms Inc., крупнейшим производителем оконных пленок в мире.</h1>
    <img src="''' + url_for ('static', filename='llumar.webp') + '''">
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name, number, groupe, course='Егор Панченко', 2, 'ФБИ-13', '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95}, 
        {'name': 'манго', 'price': 321},
    ]
    books = [
        {'author': 'Джеймс Джойс', 'name': 'Улисс', 'genre': 'роман', 'pages': '1056'},
        {'author': 'Драйзер Т.', 'name': 'Трилогия желания', 'genre': 'роман', 'pages': '1152'},
        {'author': 'Толстой Л.', 'name': 'Война и мир', 'genre': 'роман-эпопея', 'pages': '1360'},
        {'author': 'Голсуорси Дж.', 'name': 'Сага о Форсайтах', 'genre': 'роман', 'pages': '1376'},
        {'author': 'Солженицын А.', 'name': 'Архипелаг ГУЛАГ', 'genre': 'роман', 'pages': '1424'},
        {'author': 'Палиссер Ч.', 'name': 'Квинканкс', 'genre': 'роман', 'pages': '1472'},
        {'author': 'Манн Т.', 'name': 'Иосиф и его братья', 'genre': 'роман', 'pages': '1492'},
        {'author': 'Музиль Р.', 'name': 'Человек без свойств', 'genre': 'роман', 'pages': '1774'},
        {'author': 'Пруст М.', 'name': 'В поисках утраченного времени', 'genre': 'роман', 'pages': '3031'},
        {'author': 'Кнаусгор К.', 'name': 'Моя борьба', 'genre': 'биография', 'pages': '3600'},
    ]
    return render_template('example.html', name=name, number=number, groupe=groupe, course=course, fruits=fruits, books=books)
