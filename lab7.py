# Импорт необходимых объектов из библиотеки Flask
from flask import Blueprint, render_template, request, redirect, session, abort

# Создание объекта Flask Blueprint с именем 'lab7'
lab7 = Blueprint('lab7', __name__)

# Определение маршрута для главной страницы
@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

# Определение маршрута для страницы с напитками
@lab7.route('/lab7/drink')
def drink():
    return render_template('lab7/drink.html')

# Определение конечной точки API для обработки POST-запросов
# Когда приходит POST-запрос по пути /lab7/api, Flask вызывает функцию api, 
# которая обрабатывает данные этого запроса, извлекает JSON-данные и в зависимости от 
# значения параметра method в JSON-данных вызывает соответствующую функцию для обработки запроса (например, get_price или pay).
@lab7.route('/lab7/api', methods=['POST'])
def api():
    # Извлечение JSON-данных из запроса
    data = request.json

    # Проверка параметра 'method' в JSON-данных и вызов соответствующей функции
    if data['method'] == 'get-price': #if data['method'] == 'get-price':: Эта строка проверяет, равно ли значение параметра method в JSON-данных строке 'get-price'. Если это условие выполняется, то это означает, что клиент хочет получить цену напитка.
        return get_price(data['params'])#return get_price(data['params']): Если условие выше истинно, то вызывается функция get_price, передавая ей параметры из JSON-данных data['params']
#if data['method'] == 'pay':: Эта строка проверяет, равно ли значение параметра method в JSON-данных строке 'pay'. Если это условие выполняется, то это означает, что клиент хочет осуществить платеж.  
    if data['method'] == 'pay':
        return pay(data['params'])
#return pay(data['params']): Если условие выше истинно, то вызывается функция pay, передавая ей параметры из JSON-данных (data['params']).   
    # Если метод не распознан, возврат HTTP-статуса 400 Bad Request
    abort(400)

# Функция для обработки метода 'get-price'
def get_price(params):#def get_price(params):: Объявление функции get_price с параметром params, который предполагается содержать информацию о напитке
    return {"result": calculate_price(params), "errors": None}#calculate_price(params): Вызов функции calculate_price с передачей ей параметров для расчёта цены
#errors" установлен в None, предполагая, что в данной реализации нет ошибок при получении цены.
# Функция для вычисления цены на основе параметров напитка
def calculate_price(params):
    drink = params['drink']
    milk = params['milk']
    sugar = params['sugar']

    # Назначение базовой цены в зависимости от выбранного напитка
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    # Добавление дополнительных затрат за молоко и сахар
    if milk:
        price += 30 #присвоить
    if sugar:
        price += 10

    return price

# Функция для обработки метода 'pay'
def pay(params):#Предполагается, что params содержит информацию, необходимую для проведения платежа, и передается в функцию в качестве аргумента
    card_num = params['card_num']#card_num = params['card_num']: Извлечение значения параметра 'card_num' из словаря params и присвоение его переменной card_num

    # Проверка корректности номера карты
    if len(card_num) != 16 or not card_num.isdigit():#not card_num.isdigit(): Эта часть условия проверяет, что все символы в строке card_num являются цифрами. card_num.isdigit() возвращает True, если все символы в строке - цифры. 
        return {"result": None, "error": "Неверный номер карты"}
    
    cvv = params['cvv']#cvv = params['cvv']: Извлечение значения параметра 'cvv' из словаря params и присвоение его переменной cvv

    # Проверка корректности CVV
    if len(cvv) != 3 or not cvv.isdigit():#not cvv.isdigit(): Эта часть условия проверяет, что все символы в строке cvv являются цифрами
        return {"result": None, "error": "Неверный номер CVV/CVC"}
#Таким образом, если длина cvv не равна 3 или хотя бы один символ не является цифрой, то условие становится истинным. В этом случае 
# возвращается словарь с ключом "result", установленным в None, и ключом "error", содержащим сообщение об ошибке "Неверный номер CVV/CVC".    
    # Вычисление цены и возврат сообщения об успешной транзакции
    price = calculate_price(params)
    return {"result": f'С карты {card_num} списано {price} руб', "error": None}

# Определение маршрута для обработки возвратов
@lab7.route('/lab7/refund', methods=['POST'])
def refund():
    # Извлечение JSON-данных из запроса
    data = request.json #Таким образом, строка data = request.json извлекает JSON-данные из тела запроса и сохраняет их в переменной data
#Объект request предоставляется фреймворком Flask и содержит информацию о текущем HTTP-запросе
    # Извлечение параметров для валидации
    card_num = data['params']['card_num']
    cvv = data['params']['cvv']
    drink = data['params']['drink']
    milk = data['params']['milk']
    sugar = data['params']['sugar']

    # Валидация номера карты
    if not is_valid_card(card_num):
        return {"result": None, "error": "Неверный номер карты"}

    # Валидация CVV
    if not is_valid_cvv(cvv):
        return {"result": None, "error": "Неверный номер CVV/CVC"}

    # Вычисление суммы возврата и возврат сообщения об успешной транзакции
    refund_amount = calculate_price(data['params'])
    return {"result": f'Деньги вернулись на карту: {refund_amount} руб', "error": None}

# Функция для валидации номера карты
def is_valid_card(card_num):
    return len(card_num) == 16 and card_num.isdigit()

# Функция для валидации CVV
def is_valid_cvv(cvv):
    return len(cvv) == 3 and cvv.isdigit()