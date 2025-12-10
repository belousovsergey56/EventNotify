import os
import requests

from dotenv import load_dotenv


load_dotenv()

URL = os.getenv("tg_url")
TOKEN = os.getenv("tg_token")
URL_TMP= f"{URL}/bot{TOKEN}"


def check_bot() -> dict:
    """Проверить токен
    Протой тест на проверку валидности токена и
    что бот жив и настроен.
    Returns:
        dict: 
            {
                'ok': True,
                'result': 
                {
                    'id': 13345678910, 
                    'is_bot': True, 
                    'first_name': 'event_notify', 
                    'username': 'some_bot', 
                    'can_join_groups': True, 
                    'can_read_all_group_messages': True, 
                    'supports_inline_queries': False, 
                    'can_connect_to_business': False, 
                    'has_main_web_app': False
                    }
                }
    """
    url = f"{URL_TMP}/getMe"
    return requests.get(url).json()


def send_message(chat_id: str, message: str, parse_mode="HTML") -> dict:
    """Отправить сообщение
    Функция отправки сообщения на ресурс - в чат бот
    Args:
        chat_id (str): идентификатор чата
        message (str): сообщение, котрое отправляем в чат
    Returns:
        dict: возвращается словарь
    """
    url = f"{URL_TMP}/sendMessage"
    param = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": parse_mode
            }
    response = requests.post(url, json=param)
    return response.json()


def send_image(chat_id: str, image_url: str, caption_text: str) -> dict:
    """Отправить фото с подписью
    Args:
        chat_id (str): идентификатор чата
        image_url (str): урл адрес картинки
        caption_text (str): пост в 1024 символа и короткая подпись
    """
    url = f"{URL_TMP}/sendPhoto"
    param = {
            "chat_id": chat_id,
            "photo": image_url,
            "caption": caption_text
            }
    response = requests.post(url, data=param)
    return response.json()


def set_webhook(https_url: str) -> dict:
    param = {
            "url": f"{https_url}/webhook"
            }
    url = f"{URL_TMP}/setWebhook"
    response = requests.post(url, json=param)
    return response.json()
