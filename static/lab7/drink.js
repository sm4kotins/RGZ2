// Функция для отправки запроса на получение цены напитка
function get_price() {
    // Получаем значения из формы
    const milk = document.querySelector('[name=milk]').checked; // Получаем значение чекбокса "молоко"
    const sugar = document.querySelector('[name=sugar]').checked; // Получаем значение чекбокса "сахар"
    const drink = document.querySelector('[name=drink]:checked').value; // Получаем значение выбранного радиокнопки "напиток"

    // Создаем объект для отправки на сервер
    const obj = {
        "method": "get-price", // Задаем метод запроса как "get-price", указывая, что хотим получить цену напитка
        "params": { // Передаем параметр "drink" с выбранным напитком
            drink: drink, // Передаем параметр "milk" с информацией о наличии молока
            milk: milk, // Передаем параметр "sugar" с информацией о наличии сахара
            sugar: sugar
        }
    };

    // Отправляем запрос на сервер
    fetch('/lab7/api', {
        method: 'POST', // Используем метод POST для отправки данных на сервер
        headers: {'Content-Type': 'application/json'}, // Устанавливаем заголовок Content-Type для отправки данных в формате JSON
        body: JSON.stringify(obj) // Преобразуем объект `obj` в JSON-строку и передаем в теле запроса
    })
    // Обрабатываем ответ от сервера в формате JSON
    .then(function(resp) { // then(function(resp) {: Эта строка начинает блок кода, который будет выполнен после того, как запрос на сервер будет успешно выполнен. В данном случае, он обрабатывает объект resp, который представляет собой ответ от сервера.
        return resp.json(); // eturn resp.json();: Эта строка вызывает метод .json() на объекте ответа resp. Этот метод асинхронно читает тело ответа в формате JSON и возвращает новый Promise, который разрешится данными в формате JSON.
    })
    // Обрабатываем данные, полученные от сервера
    .then(function(data){
        // Обновляем интерфейс с полученной ценой
        document.querySelector('#price').innerHTML = `Цена напитка: ${data.result} руб`;
        document.querySelector('#pay').style.display = ''; // Показываем кнопку "оплатить"
        document.querySelector('#refund').style.display = ''; // Показываем кнопку "возврат"
    });
}

// Функция для осуществления платежа
function pay() {
    // Получаем значения из формы
    const cardNum = document.querySelector('[name=card]').value; // Получаем значение поля "номер карты"
    const cardName = document.querySelector('[name=name]').value; // Получаем значение поля "имя на карте"
    const cvv = document.querySelector('[name=cvv]').value; // Получаем значение поля "CVV"
    const milk = document.querySelector('[name=milk]').checked; // Получаем значение чекбокса "молоко"
    const sugar = document.querySelector('[name=sugar]').checked; // Получаем значение чекбокса "сахар"
    const drink = document.querySelector('[name=drink]:checked').value; // Получаем значение выбранного радиокнопки "напиток"

// Создаем объект для отправки на сервер
const obj = {
    "method": "pay", // Указываем метод запроса как "pay", указывая, что хотим осуществить платеж
    "params": {
        card_num: cardNum, // Передаем параметр "card_num" с номером карты
        card_name: cardName, // Передаем параметр "card_name" с именем на карте
        cvv: cvv, // Передаем параметр "cvv" с кодом CVV
        drink: drink, // Передаем параметр "drink" с выбранным напитком
        milk: milk, // Передаем параметр "milk" с информацией о наличии молока
        sugar: sugar // Передаем параметр "sugar" с информацией о наличии сахара
    }
};


    // Отправляем запрос на сервер
    fetch('/lab7/api', {
        method: 'POST', // Используем метод POST для отправки данных на сервер
        headers: {'Content-Type': 'application/json'}, // Устанавливаем заголовок Content-Type для отправки данных в формате JSON
        body: JSON.stringify(obj) // Преобразуем объект `obj` в JSON-строку и передаем в теле запроса
    })
    // Обрабатываем ответ от сервера в формате JSON
    .then(function(resp) {
        return resp.json();
    })
    // Обрабатываем данные, полученные от сервера
    .then(function(data){
        // Выводим результат платежа или ошибку
        if (data.error) {
            alert(data.error); // Если есть ошибка, выводим ее в виде всплывающего сообщения
        } else {
            alert(data.result); // В противном случае выводим результат платежа в виде всплывающего сообщения
        }
    });

}

// Функция для возврата средств
function refund() {
    // Получаем значения из формы
    const cardNum = document.querySelector('[name=card]').value; // Получаем значение поля "номер карты"
    const cvv = document.querySelector('[name=cvv]').value; // Получаем значение поля "CVV"
    const drink = document.querySelector('[name=drink]:checked').value; // Получаем значение выбранного радиокнопки "напиток"
    const milk = document.querySelector('[name=milk]').checked; // Получаем значение чекбокса "молоко"
    const sugar = document.querySelector('[name=sugar]').checked; // Получаем значение чекбокса "сахар"

// Создаем объект для отправки на сервер
const obj = {
    "method": "refund", // Указываем метод запроса как "refund", указывая, что хотим осуществить возврат средств
    "params": {
        card_num: cardNum, // Передаем параметр "card_num" с номером карты
        cvv: cvv, // Передаем параметр "cvv" с кодом CVV
        drink: drink, // Передаем параметр "drink" с выбранным напитком
        milk: milk, // Передаем параметр "milk" с информацией о наличии молока
        sugar: sugar // Передаем параметр "sugar" с информацией о наличии сахара
    }
};


// Отправляем запрос на сервер
fetch('/lab7/refund', {
    method: 'POST', // Используем метод POST для отправки данных на сервер
    headers: {'Content-Type': 'application/json'}, // Устанавливаем заголовок Content-Type для отправки данных в формате JSON
    body: JSON.stringify(obj) // Преобразуем объект `obj` в JSON-строку и передаем в теле запроса
})
// Обрабатываем ответ от сервера в формате JSON
.then(function(resp) {
    return resp.json();
})
// Обрабатываем данные, полученные от сервера
.then(function(data){
    // Выводим результат возврата или ошибку
    if (data.error) {
        alert(data.error); // Если есть ошибка, выводим ее в виде всплывающего сообщения
    } else {
        alert(data.result); // В противном случае выводим результат возврата в виде всплывающего сообщения
    }
});

}