# Дерево проекта
```bash
.
├── app
│   ├── api
│   │   ├── api_kuda_go.py
│   │   └── api_telegram_bot.py
│   ├── app_database
│   │   ├── crud.py
│   │   └── users.db
│   ├── main.py
│   └── Makefile
├── pyproject.toml
├── README.md
├── reports
│   ├── record_001.md
│   ├── record_002.md
│   ├── record_003.md
│   ├── record_004.md
│   └── договорённости по задаче
├── requirements.txt
└── uv.lock

5 directories, 15 files
```
---

# Изменения
- Объекдинил api модули в одну директорию: `api_telegram` и `api_kuda_go` удалены, создана новая дректория `api`, кода перенесны модули `api_kuda_go.py` и `api_telegram_bot.py`
- Создана директория `app_database`, в которой хранится модуль `crud.py` и база `users.db`
- Добавил файл с зависимостями `requirements.txt`
- Версия проекта обновлена с `0.1.0` -> `1.0.0`
- В `main.py` - добавил настройки планировщика, добавил функцию prepare_message - для подготовки текста сообщения, post_event - для отправки текста сообщения, send_event - использует первые две функции, send_daily_post - функция для планировщика, занимается рассылкой в фоне. В webhook - добавил обработку присылаеымх пользователем сообщений /start, /delete, /event, /help. В index добавил вывод текста от бота - его состояние
---

### main.py
```python
import atexit
import sys

from api.api_kuda_go import collect_data_for_sending
from api.api_telegram_bot import (
    check_bot,
    set_webhook,
    send_image,
    send_message,
)
from app_database.crud import add_id, get_all_id, remove_id
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, request
from flask_sslify import SSLify
```
#### Импорты
- `import atexit` - модуль для автоматического завершения планировщика
- `sys` - модуль для роботы с системой, с ПК
- `from api.api_kuda_go import collect_data_for_sending` - из модуля `api_kuda_go` в пакете `api`, имортируем функцию `collect_data_for_sending` для поллучения списка с данными из апи KudaGo
- `from api.api_telegram_bot import` - из модуля `api_telegram_bot` в пакете `api`, импортируем блок функций: `check_bot`, `set_webhook`, `send_image`, `send_message` для отправки картинок с пописью, отправки текста, установки вебхка и провери токена бота.
- `from app_database.crud import add_id, get_all_id, remove_id` - из модуля `crud` в пакете `app_database`, импортируем функции: `add_id`, `get_all_id`, `remove_id`
- `from apscheduler.schedulers.background import BackgroundScheduler` - из библиотеки `apscheduler` импортируем `BackgroundScheduler` для настройки планировщика работы в фоне
- `from apscheduler.triggers.cron import CronTrigger` - из библиотеки `apscheduler` импортируем `CronTrigger` для установки времени в расписании
- `from flask import Flask, request` - из библиотеки flask
- `from flask_sslify import SSLify`

```
app = Flask("__name__")
ssl_certificate = SSLify(app)
scheduler = BackgroundScheduler()

def prepare_message(event: dict) -> str:
    """Подготовить сообщение.
    В цикле проходит по словарю и записывает данные в строку message
    
    Args:
        event (dict): словарь с данными по событию
    Returns:
        str: готовое сообщение
        Новогодний фестиваль хендмейда и дизайна «Петербургская ярмарка»
        Предпраздничная «Петербургская ярмарка» во 2-м павильоне «Ленфильме» согреет гостей тёплой новогодней атмосферой. Мастера и дизайнеры представят интересные товары ручной работы и в очередной раз докажут, что изделия от местных брендов — это круто.
        Дата проведения: С 2025-12-20 12:00:00 по 2025-12-21 21:00:00
    """
    message = ""
    for key, value in event.items():
        if "image" == key:
            continue
        if len(value) == 0:
            continue
        if "place" == key and "title" in value.keys():
            message += f"{value.get("title")}, {value.get("address")}\n"
            continue
        if "publication_date" == key:
            continue
        if "dates" == key:
            message += f"Дата проведения: {value}\n"
            continue
        message += f"{value}\n"
    return message


def post_event(chat_id: str, message: str, url_image: str=None) -> bool:
    """Отправить пост в телеграм.
    Отправляем сообщение в ТГ. Если есть картинка, отправляем текс с картинкой
    одним сообщением, иначе только текст.

    Args:
        chat_id (str): идентификатор чата
        message (str): подготовленный текст сообщения
        url_message (str): адрес к картинке, по умолчанию None
    Returns:
        bool: если отправка сообщения прошла без ошибок возвращается True
        иначе False
    """
    try:
        if url_image is None:
            send_message(chat_id, message)
        else:
            send_image(chat_id, url_image, message)
        return True
    except Exception as e:
        print(f"Не предвиденная ошибка: {e}")
        return False


def send_event_response(chat_id: str) -> bool:
    """Подготоваить и отправить сообщение о событиях

    Args:
        chat_id (str): id чата с пользовтелем
    Returns:
        bool: True если сообщения отправлены, False если нет 
    """
    try:
        event_data = collect_data_for_sending()
        for event in event_data:
            message = prepare_message(event)
            post_event(chat_id, message, event.get("image"))
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def send_daily_post():
    """Подготвить и отправить ежедневное сообщение
    Функция готовит и отправляет сообщения всем чатам,
    которые на ходятся в базе даненых.
    """
    try:
        event_data = collect_data_for_sending()
        chat_ids = get_all_id()
        for event in event_data:
            for chat_id in chat_ids:
                message = prepare_message(event)
                post_event(chat_id, message, event.get("image"))
    except Exception as e:
        print(f"Ошибка при отправке поста: {e}")        


scheduler.add_job(
    func=send_daily_post,
    trigger=CronTrigger(hour=13, minute=12),
    id="daily_post_job",
    name="Ежедневные уведомления по БД",
    replace_existing=True
)


def shutdown_scheduler():
    print("Планировщик останавливается...")
    scheduler.shutdown()
    print("Планировщик остановлен.")


atexit.register(shutdown_scheduler)

scheduler.start()
print("Планировщик запущен при старте приложения.")


@app.route("/", methods=["POST", "GET"])
def index():
    """Главная страница приложения
    Печатет заголовок первого уровня, что бот работает.
    На второй строке техническое сообщение сv данными о боте.
    """
    message = f"<h1>Бот работает</h1>\n{check_bot()}"
    return message


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = request.get_json()
        if 'message' in update:
            chat_id_list = get_all_id()
            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')
            if text == "/start":
                if chat_id in chat_id_list:
                    send_message(chat_id, "Чат в расписание уже был добавлен")
                else:
                    send_message(
                             chat_id,
                             "Чат добавлен в расписание, события каждый день"
                         )
                    add_id(chat_id)
                    send_message(chat_id, "Подготовка к отправке первых событий")
                    send_event_response(chat_id)                    
            elif text == "/delete":
                removed_chat_id = remove_id(chat_id)
                if removed_chat_id:
                    send_message(chat_id, "Чат из расписания убран, рассылка отменена.")
                else:
                    send_message(chat_id, "Не предвидженная ошибка, попробуй позже")
            elif text == "/event":
                send_message(chat_id, "Собираем данные о событиях, минуту...")
                send_event_response(chat_id)
            elif text == "/help":
                message = """- Команда /start - добавляет чат в расписание для ежедневной отправки сообщений о событиях в городе
- Команда /delete - убирает чат из расписания
- Команда /event - подготавливает данные о событиях и однократно отправляет в чат
- Команда /help - печатает это сообщение
            """
                send_message(chat_id, message)
    except Exception as e:
        print(f"Ошибка: {e}")
    return "Ok"


if __name__ == "__main__":
    public_url = sys.argv[1]
    result = set_webhook(public_url)
    print(result)
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    print("Серрвер остановлен")
```
