from flask import Blueprint, redirect, url_for, render_template
lab1 = Blueprint('lab1',__name__)


@lab1.route("/")


@lab1.route("/index")
def start():
    return redirect("/menu", code=302)


@lab1.route("/menu")
def menu():
    return render_template('menu.html')

@lab1.route("/lab1")
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


@lab1.route('/lab1/oak')
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


@lab1.route('/lab1/student')
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


@lab1.route('/lab1/python')
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


@lab1.route('/lab1/toner')
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