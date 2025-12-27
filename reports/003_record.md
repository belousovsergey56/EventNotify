# Дерево проекта на текущую запись
```bash
➜  EventNotify git:(main) tree                                                                                                                                                                    12/12/25 12:53
.
├── app
│   ├── api_event
│   │   └── api_kuda_go.py
│   ├── api_telegram
│   │   └── api_telegram_bot.py
│   ├── check_bot.py
│   ├── main.py
│   └── Makefile
├── pyproject.toml
├── README.md
├── reports
│   ├── record_001.md
│   ├── record_002.md
│   └── договорённости по задаче
└── uv.lock

5 directories, 11 files
```
---

# Что нового
- В директорию `api_telegram` добавлен модуль `api_telegram_bot.py`
- В директорию `app` добавлен `Makefile`
- В директорию `app` добавлен `check_bot.py`
- `main.py` обновлён тестируемыми данными
---

## api_telegram_bot.py
- функция check_bot() - Протой тест на проверку валидности токена и что бот жив и настроен, если токен корректный, то в словаре ключ "ok" будет иметь значение `True`. Так же в словаре будет другая информация по настройкам бота.
```python
def check_bot() -> dict:
    url = f"{URL_TMP}/getMe"
    return requests.get(url).json()
```

- функция send_message(chat_id: str, message: str) - принимает такие аргументы, как chat_id - идентификатор чата, message - текст который мы будем отправлять, возможно ещё parse_mode, но скорей всего этот аргумент уберём т.к. текст из KudaGo не требует форматирования. Результат запроса(отправки сообщения) так же словарь с данными об успешности или ошибке отправки.
```python
def send_message(chat_id: str, message: str, parse_mode="HTML") -> dict:
    url = f"{URL_TMP}/sendMessage"
    param = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": parse_mode
            }
    response = requests.post(url, json=param)
    return response.json()
```

- функция send_image(chat_id: str, image_url: str, caption_text: str) - нужна для отправки картинки с подписью, своего рода пост, чтобы картинка и текст были в одном сообщении. Функия принимает chat_id - идентификатор чата, image_url - ссылка в интернете на файл с картинкой (то что предоставляет сервис KudaGo), caption_text - это текст подписи под картинкой, максималоьный объём символов включая символы ссылки - 1024 символов
```python
def send_image(chat_id: str, image_url: str, caption_text: str) -> dict:
    url = f"{URL_TMP}/sendPhoto"
    param = {
            "chat_id": chat_id,
            "photo": image_url,
            "caption": caption_text
            }
    response = requests.post(url, data=param)
    return response.json()
```

- функция set_webhook(https_url: str) - нужна для установки вебхука, чтобы не опрашивать каждую секунду телеграм на наличие новых сообщений, ТГ связывает наш адрес сервера с ботом и если в бот поступаю сообщения, ТГ сам отправляет сообщение к нам на сервер. В аргументах функции нужно указать адрес нашего серовера.
```python
def set_webhook(https_url: str) -> dict:
    param = {
            "url": f"{https_url}/webhook"
            }
    url = f"{URL_TMP}/setWebhook"
    response = requests.post(url, json=param)
    return response.json()
```

---

## Makefile
```Makefile
run_tuna:
        tuna http 5000
check_bot:
        uv run check_bot.py
```
Makefile - просто текстовый файл, который содержит набор правил для автоматизации задач в проекте, например, запуск скриптов, сборка программы или установка зависимостей.Команда:
Результат выполнения команды `make run_tuna`:
```bash
tuna http 5000
INFO[14:06:13] Welcome to Tuna
INFO[14:06:14] Account: belousovsergej56@gmail.com (Free)
INFO[14:06:14] Web Interface: http://127.0.0.1:4040
INFO[14:06:15] Forwarding https://zno4mu-178-252-83-236.ru.tuna.am -> 127.0.0.1:5000
```
Первая строка это Makefile автоматически прописал в консоли команду и нажал ввод. 

---

## check_bot.py

```python
from api_telegram.api_telegram_bot import check_bot

if __name__ == "__main__":
    print(check_bot())
```
В целом, тут просто точка входа, которая выполняет функцияю `check_bot()`
- `from api_telegram.api_telegram_bot import check_bot` - если перевести на русский то можно узнать, что из модуля `api_telegram_bot`, который находится в пакете `api_telegram` берём функцию `check_bot`
- `if __name__ == "__main__":` - это способ понять, запускается ли файл как основная программа или он импортируется как модуль в другой код, код внутри этого условия выполняется.
- `print(check_bot())` - функция `check_bot()` выполняется и возвращает результат в формате словарь, функция `print()` выводит эти данные в консоль.
Результат выполнения функции
```bash
make check_bot                                                                                                                                                                12/12/25 14:09
uv run check_bot.py
{'ok': True, 'result': {'id': 1337479154, 'is_bot': True, 'first_name': 'event_notify', 'username': 'bsa56_currency_bot', 'can_join_groups': True, 'can_read_all_group_messages': True, 'supports_inline_queries': False, 'can_connect_to_business': False, 'has_main_web_app': False}}
```

---

## main.py
```python
import sys

from flask import Flask, request
from flask_sslify import SSLify

from api_telegram.api_telegram_bot import send_message, set_webhook, send_image


app = Flask("__name__")
ssl_certificate = SSLify(app)


@app.route("/", methods=["POST", "GET"])
def index():
    return "<h1>Bot it is worked </h1>"


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = request.get_json()
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')
            if text == "/start":
                send_message(chat_id, "Привет. Мой <a href='https://www.w3schools.com/html/default.asp'>w3schools</a>\nТекстовое сообщение с ссылкой на ресурс", parse_mode="HTML")
            elif text == "img":
                send_image(
                        chat_id, "https://www.thewowstyle.com/wp-content/uploads/2015/01/Most-Beautiful-Places-in-the-World.jpg", "Отправка картинки с постом под ней, в данном случае просто подпись.\nНо для теста хватает."
                        )
            else:
                send_message(chat_id, f'Зеркалим написанное в бот: {text}')
    except Exception as e:
        print(f"Ошибка: {e}")
    return "Ok"


if __name__ == "__main__":
    public_url = sys.argv[1]
    result = set_webhook(public_url)
    print(result)
    app.run(host="0.0.0.0", port=5000)
```
- Импортируем нужные модули и функции
```python
import sys
from flask import Flask, request
from flask_sslify import SSLify
from api_telegram.api_telegram_bot import send_message, set_webhook, send_image
```
- `app = Flask("__name__")` - переменная `app` инициализирует экземпляр класса `Flask`, это фреймворк, который позволит запускать сервер и создавать маршруты к элементам сервера.
Например `http://127.0.0.1:5000/` - `/` слэш в конце адреса сайта это корень, домашняя директория сайта.
А `http://127.0.0.1:5000/about` - `/about` это уже другая директория на нашем сервере, которую можно вывести как страницу сайта и показать в ней данные о нашем сайте, компании, продукте и т.д.
Т.е `http://127.0.0.1:5000` - это адрес сайта в сети, конкретный пример локальная сеть, к которой из интернета не подключиться. Состоит из нескольких частей
  - `http` - протокол передачи данных в сети
  - `127.0.0.1` - ip адрес сайта - как адрес дома
  - `5000` - порт по которому можно сайт обнаружить - как номер подъезда
  - `/` - корневая директория сайта - как номер квартиры
  - `/about` - ещё одна квартира
- `ssl_certificate = SSLify(app)` - переменная `ssl_certificate` инициализирует экземпляр класса `SSLify`, который наследует эксземпляр класса `Flask`, который находится в переменной `app` - ssl нужен для того, чтобы протокол передачи данных был безопасным т.е. `http` -> `https` - это обязательно нужно сделать т.к. телеграм работает только в защищённой среде, а протокол `https` шифрует данные, которые передаёт
- Создаём корневую директорию сервера
```python
@app.route("/", methods=["POST", "GET"])
def index():
    return "<h1>Bot it is worked </h1>"
```
- `@app.route("/", methods=["POST", "GET"])` - это синтаксис фреймворка `Flask`, маршрут к директории `/` определяем в декораторе к функции `index`, HTTP методы которые может выполнять этот маршрут `GET` - получить данные и `POST` -изменить данные.
- `def index():` - опредленеие функции, без аргументов
- `return "<h1>Bot it is worked </h1>"` - функция возвращает одну HTML строку, заголовок первого уровня `<h1>Bot it is worked </h1>`
<img width="663" height="234" alt="изображение" src="https://github.com/user-attachments/assets/bdd38d5c-9e6f-40f0-929c-b5ff082098e0" />

- Второй маршрут `/webhook`
```python
@app.route("/webhook", methods=["POST"])
def webhook():
```
Маршрут называется именно `/webhook` т.к. функция `set_webhook` привязывает бота именно к этому маршруту - эта строка `"url": f"{https_url}/webhook"`, сама функция ниже
```python
def set_webhook(https_url: str) -> dict:
    param = {
            "url": f"{https_url}/webhook"
            }
    url = f"{URL_TMP}/setWebhook"
    response = requests.post(url, json=param)
    return response.json()
```
> Это пока тест проверки взаимодействия с ТГ, что мы можем отправлять и можем получать сообщения.

- Данная реализация обёрнута в блок `try/except` - данная конструкция ловит возникающие ошибки, при этом программа не останавливается в случае ошибки, если бы этого блока небыло, то при ошибке программа перестанет работать.
- `update = request.get_json()` - переменная содержит словарь полученный от апи телеграм, при отправки сообщения из бота
- `if 'message' in update:` - если ключ `message` содержится в словаре `update`, тогда выполняется код ниже
- `chat_id = update['message']['chat']['id']` - в переменную `chat_id` извлекаем значение идентификатор чата из словаря `id` , который находится в словаре `chat`, который находится в словаре `message`
- `text = update['message'].get('text', '')` - в переменную `text` извлекаем полученный из ТГ текст сообщения по тому же приципу, текст лежит в словаре по ключу `text`, если текста нет то будет присвоена пустая строка, словарь `text` лежит в словаре `message`
>Как выглядит словарь `update` из которого извлекаются данные
>
  
  ```python
  [{'message': {'chat': {'first_name': 'Сергей',
                       'id': 765412602,
                       'last_name': 'Белоусов',
                       'type': 'private',
                       'username': 'sbelousov56'},
              'date': 1765553137,
              'from': {'first_name': 'Сергей',
                       'id': 765412602,
                       'is_bot': False,
                       'language_code': 'en',
                       'last_name': 'Белоусов',
                       'username': 'sbelousov56'},
              'message_id': 1046,
              'text': 'hello world'},
  'update_id': 411681892}]
  ```
- Далее блок ветвления `if/elif/else`

- `if text == "/start"` - если переменная `text` содержит строку `/start` отправляем ответное сообщение в ТГ, используем метод `send_message`
- `send_message(chat_id, "Привет. Мой <a href='https://www.w3schools.com/html/default.asp'>w3schools</a>\nТекстовое сообщение с ссылкой на ресурс", parse_mode="HTML)`
  - Первый аргумент - идентификатор чата
  - Второй аргумент - отправляемое сообщение
  - Третий аргумент - в каком формате отправленное сообщение (этот аргумент уберём т.к. KudaGo содержит обычный текст)
 
Результат выполнения:

<img width="483" height="241" alt="изображение" src="https://github.com/user-attachments/assets/962f6871-a2cd-4556-9eda-ac0dc646beb7" />

---
- `elif text == "img"` - иначе, если переменная `text` содержит строку `img` будет выполнена функция `send_image`
- `send_image(chat_id, "https://www.thewowstyle.com/wp-content/uploads/2015/01/Most-Beautiful-Places-in-the-World.jpg", "Отправка картинки с постом под ней, в данном случае просто подпись.\nНо для теста хватает.")`
  - Первый аргумент - идентификатор чата, куда отправляем
  - Второй аргумент - ссылка на картинку
  - Третий аргумент - подпись под картинкой, получается пост. Единая структура картинка + текст

Результат выполнения:

<img width="473" height="348" alt="изображение" src="https://github.com/user-attachments/assets/498ed7f4-a0c9-4938-aab4-37d02fe067ae" />

---
- `else:` - иначе будет выполнена функция `send_message`, которая отправляет введённый в бот текст
- `send_message(chat_id, f'Зеркалим написанное в бот: {text}')`
  - Первый аргумент - идентификатор чата, куда отправялем
  - Второй аргумент - наш текст + то что написал пользователь

Результат выполнения:

<img width="471" height="108" alt="изображение" src="https://github.com/user-attachments/assets/673e67a3-444b-40fc-81cb-df665d13701d" />

---
- `except Exception as e:` - возбуждаем исключение в случае если возникнет ошибка.
- `print(f"Ошибка: {e}")` - выводим в консоль текст `Ошибка: текст ошибки`
- Пример ошибки `Ошибка: send_message() takes from 2 to 3 positional arguments but 4 were given`
  - Программа не остановилась и продолжает работать, но в консоль выведен текст ошибки, что в функцию передали четыре позиционных аргумента вместо трёх
  - Функция с ошибкой `send_message("765412602", "yo", "HTML", "dkd")`
  - Как функция пределена `def send_message(chat_id: str, message: str, parse_mode="HTML") -> dict`
- `return "Ok"` - это то, что возвращет HTTPS метод в теле ответа, в самом низу скрина

<img width="730" height="689" alt="изображение" src="https://github.com/user-attachments/assets/30327bb1-cbfc-43c5-9162-ea24d6fdd75b" />

---
```python
if __name__ == "__main__":
    public_url = sys.argv[1]
    result = set_webhook(public_url)
    print(result)
    app.run(host="0.0.0.0", port=5000)
```
- `if __name__ == "__main__":`
> в Python — это способ понять, запускается ли файл как основная программа или он импортируется как модуль в другой код.
> Если файл запускается напрямую (например, через python3 my_file.py), то Python автоматически присваивает переменной __name__ значение "__main__", и код внутри этого условия выполняется.
> Если же файл импортируется в другой скрипт (например, через import my_file), то __name__ будет равен имени файла, и код внутри условия не запускается.
> Это позволяет писать код, который можно использовать и как модуль, и как самостоятельную программу, не выполняя лишние действия при импорте.
> Простыми словами: это «ограда», которая разделяет запуск скрипта от его импорта.

- `public_url = sys.argv[1]` - переменной `public_url` присваиваем аргумент под индексом 1, который передали при запуске скрипта
- `result = set_webhook(public_url)` - в эту переменную сохраняется результат выполнения функции `set_webhook` в которую передали `public_url`
- `print(result)` - выводим результат в консоль
- `app.run(host="0.0.0.0", port=5000)` - веб-приложение будет запущено на всех доступных сетевых интерфейсах на порту 5000
Как это выглядит
```bash
➜  app git:(main) ✗ uv run main.py https://rejp1b-178-252-83-236.ru.tuna.am                                                                                                                             
{'ok': True, 'result': True, 'description': 'Webhook was set'}
 * Serving Flask app '__name__'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.0.42:5000
Press CTRL+C to quit
127.0.0.1 - - [12/Dec/2025 22:16:21] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [12/Dec/2025 22:16:39] "POST /webhook HTTP/1.1" 200 -
```
- `uv run main.py https://rejp1b-178-252-83-236.ru.tuna.am` - запуск скрипта с помощью менеджера пакетов `uv`, равнознаяный запуск `python3 main.py https://rejp1b-178-252-83-236.ru.tuna.am`
  - `python3` или `uv run` это команда запуска
  - `main.py` - первый аргумент команды запуска под индексом 0
  - `https://rejp1b-178-252-83-236.ru.tuna.am` - второй аргумент под индексом 1
  - Для python это выглядит как массив [`main.py`, `https://rejp1b-178-252-83-236.ru.tuna.am`], индексы в массиве, да и в целом в программировании начинаются с нуля, поэтому чтобы установить вебхук, мы берём аргумент под индексом 1 (`sys.argv[1]`)
  - `{'ok': True, 'result': True, 'description': 'Webhook was set'}` - это вывод на печать `print(result)`
  - Всё остальное служебные сообщения при запуске сервера, адреса на которых доступен веб-приложение и логи (ответы http методов на выполнение запросов)
 
---
