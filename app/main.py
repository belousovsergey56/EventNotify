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
