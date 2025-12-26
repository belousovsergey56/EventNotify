import atexit
import json
import sys

from api.api_kuda_go import collect_data_for_sending
from api.api_telegram_bot import (
    check_bot,
    set_webhook,
    send_image,
    send_message,
)
from app_database.crud import add_id, get_all_id, remove_id, create_user_table
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, request


app = Flask("__name__")
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
    data_bot = json.dumps(check_bot(), indent=4)
    message = f"<h1>Бот работает</h1>\n<pre>{data_bot}</pre>"
    return message


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = request.get_json()
        if 'message' in update:
            chat_id_list = get_all_id()
            chat_id = str(update['message']['chat']['id'])
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
                    send_message(chat_id, "В списке рассылок нет текущего чата")
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
    create_user_table()
    public_url = sys.argv[1]
    result = set_webhook(public_url)
    print(result)
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    print("Серрвер остановлен")
