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

# Что нового
- В директорию `api_telegram` добавлен модуль `api_telegram_bot.py`
- В директорию `app` добавлен `Makefile`
- В директорию `app` добавлен `check_bot.py`
- `main.py` обновлён

## Модуль api_telegram_bot
- функция check_bot() - Протой тест на проверку валидности токена и что бот жив и настроен, если токен корректный, то в словаре ключ "ok" будет иметь значение `True`. Так же в словаре будет другая информация по настройкам бота.
- функция send_message(chat_id: str, message: str) - принимает такие аргументы, как chat_id - идентификатор чата, message - текст который мы будем отправлять, возможно ещё parse_mode, но скорей всего этот аргумент уберём т.к. текст из KudaGo не требует форматирования. Результат запроса(отправки сообщения) так же словарь с данными об успешности или ошибке отправки.
- функция send_image(chat_id: str, image_url: str, caption_text: str) - нужна для отправки картинки с подписью, своего рода пост, чтобы картинка и текст были в одном сообщении. Функия принимает chat_id - идентификатор чата, image_url - ссылка в интернете на файл с картинкой (то что предоставляет сервис KudaGo), caption_text - это текст подписи под картинкой, максималоьный объём символов включая символы ссылки - 1024 символов
- функция set_webhook(https_url: str) - нужна для установки вебхука, чтобы не опрашивать каждую секунду телеграм на наличие новых сообщений, ТГ связывает наш адрес сервера с ботом и если в бот поступаю сообщения, ТГ сам отправляет сообщение к нам на сервер. В аргументах функции нужно указать адрес нашего серовера.

## Makefile
```Makefile
run_tuna:
        tuna http 5000
check_bot:
        uv run check_bot.py
```
Makefile - инструмент для работы с проектом, создаём имя точки запуска, а в тело записываем список команд, что упрощает работу и позволяет каждый раз не писать руками команды.
Команда:
```bash
make run_tuna
```
Результат выполнения:
```bash
tuna http 5000
INFO[14:06:13] Welcome to Tuna
INFO[14:06:14] Account: belousovsergej56@gmail.com (Free)
INFO[14:06:14] Web Interface: http://127.0.0.1:4040
INFO[14:06:15] Forwarding https://zno4mu-178-252-83-236.ru.tuna.am -> 127.0.0.1:5000
```
Первая строка это Makefile автоматически прописал в консоли команду и нажал ввод. 

## check_bot.py
```python
from api_telegram.api_telegram_bot import check_bot

if __name__ == "__main__":
    print(check_bot())
```
В целом, тут просто точка входа, которая выполняет функцияю `check_bot()`
- `from api_telegram.api_telegram_bot import check_bot` - если перевести на русский то можно узнать, что из модуля `api_telegram_bot`, который находится в пакете `api_telegram` берём функцию `check_bot`
- `if __name__ == "__main__":` - конструкция, котороая определяет, что этот пакет можно выполнять. Все функции находящиеся ниже этой строки выполдняются т.е. используются, все функции, которые находится до этой строки являются определнеием. В общем точка запуска конкретного файла.
- `print(check_bot())` - функция `check_bot()` выполняется и возвращает результат в формате словарь, функция `print()` выводит эти данные в консоль.
Результат выполнения функции
```bash
make check_bot                                                                                                                                                                12/12/25 14:09
uv run check_bot.py
{'ok': True, 'result': {'id': 1337479154, 'is_bot': True, 'first_name': 'event_notify', 'username': 'bsa56_currency_bot', 'can_join_groups': True, 'can_read_all_group_messages': True, 'supports_inline_queries': False, 'can_connect_to_business': False, 'has_main_web_app': False}}
```
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
А `http://127.0.0.1:5000/about` - `/about` это уже другая директория на нашем сервере, которую можно вывести как страницу сайта и казать в ней данные о нашем сайте, компании, продукте и т.д.
Т.е `http://127.0.0.1:5000` - это адрес сайта в сети, конкретный пример локальная сеть, к которой из интернета не подключиться. Состоит из нескольких частей
  - `http` - протокол передачи данных в сети
  - `127.0.0.1` - ip адрес сайта
  - `5000` - порт по которому можно сайт обнаружить - как номер подъезда
  - `/` - корневая директория сайта - номер квартиры
  - `/about` - ещё одна квартира
- `ssl_certificate = SSLify(app)` - переенная `ssl_certificate` инициализирует экземпляр класса `SSLify`, который наследует эксземпляр класса `Flask`, который находится в переменной `app` - ssl нужен для того, чтобы протокол передачи данных был безопасным т.е. `http` -> `https` - это обязательно нужно сделать т.к. телеграм работает только в защищённой среде, а протоко `https` шифрует данные, которые передаёт
- Создаём корневую директорию сервера
```python
@app.route("/", methods=["POST", "GET"])
def index():
    return "<h1>Bot it is worked </h1>"
```
- `@app.route("/", methods=["POST", "GET"])` - это синтаксис фреймворка `Flask`, маршрут к директории `/` определяем в дероаторе к функции `index`, HTTP методы которые может выполнять этот маршрут `GET` - получить данные и `POST` -изменить данные.
- `def index():` - опредленеие функции, без аргументов
- `return "<h1>Bot it is worked </h1>"` - функция возвращает одну HTML строку в формате заголовка первого уровня `<h1>Bot it is worked </h1>`
<img width="663" height="234" alt="изображение" src="https://github.com/user-attachments/assets/bdd38d5c-9e6f-40f0-929c-b5ff082098e0" />

- Второй маршрут `/webhook`
```python
@app.route("/webhook", methods=["POST"])
def webhook():
```
Маршрут называется имеено `wrbhook` т.к. функция `setweb_hook` привязывает бота именно к этому маршруту - эта строка `"url": f"{https_url}/webhook"`, сама функция ниже
```python
def set_webhook(https_url: str) -> dict:
    param = {
            "url": f"{https_url}/webhook"
            }
    url = f"{URL_TMP}/setWebhook"
    response = requests.post(url, json=param)
    return response.json()
```
Это пока тест проверки взаимодействия с ТГ, что мы можем отправлять и можем получать сообщения.
- Данная реализация обёрнута в блок `try/except` - данная конструкция ловит возникающие ошибки, при этом программа не останавливается в случае ошибки, если бы этого блока небыло, то при ошибке программа перестанет работать.
- `update = request.get_json()` - переменная содерожит словарь полученный из бота
- `if 'message' in update:` - если ключ `message` содержится в словаре `update`, тогда выполняется код ниже
- `chat_id = update['message']['chat']['id']` - в переменную `chat_id` извлекаем из словаря `id` значение идентификатор чата, который находится в словаре `chat`, который находится в словаре `message`
- `text = update['message'].get('text', '')` - в переменную `text` извлекаем полученный из ТГ текст сообщения по тому же приципу, текст лежит в словаре по ключу `text`, если текста нет то будет присвоена пустая строка, словарь `text` лежит в словаре `message`
- >Как выглядит словарь `update` из которого извлекаются данные
  >
  >{'update_id': 411681892, 'message': {'message_id': 1046, 'from': {'id': 765412602, 'is_bot': False, 'first_name': 'Сергей', 'last_name': 'Белоусов', 'username': 'sbelousov56', 'language_code': 'en'}, 'chat': {'id': 765412602, 'first_name': 'Сергей', 'last_name': 'Белоусов', 'username': 'sbelousov56', 'type': 'private'}, 'date': 1765553137, 'text': 'hello world'}}
  >
