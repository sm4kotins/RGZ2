from flask import Flask
app = Flask(__name__)

@app.route("/")
def start():
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

        <h1>web-сервер на flask</h1>

        <footer>
            &copy; Егор Панченко, ФБИ-13, 3 курс, 2023
        </footer>
    </body>
</html>
"""