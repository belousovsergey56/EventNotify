# Чат-бот EventNotify - рассылка уведомлений о событиях в Санкт-Петербурге

# Содержание
- [Возможности](#возможности)
- [Технологии](#технологии)
- [Установка](#установка)
- [Переменные окружения](#переменные-окружения)
- [Зависимости](#зависимости)
- [Запуск](#запуск)
- [Демонстрация](#демонстрация)

## Возможности
Данное приложение собирает актуальные данные о событиях, кино, спектаклях в г. Санкт-Петербург по апи сервиса [KudaGo](https://docs.kudago.com/api/)
Взаимодействует с чат-бот сервиса тегеграм по [апи телеграм](https://core.telegram.org) и отправляет уведомления пользователю на ежедневной основе путём добавления id чата в список расписания или по запросу пользователя.

Можно:
- Подписаться на уведомления
- Отписаться от уведомлений
- Запросить список событий без подписки

## Технологии
Код проекта написан на python3 с применением микро фреймворка Flask и встроенной базы данных SQLite
Использованы апи сервисов KudaGo и API Telegram

## Установка
Для установки проекта на ПК, исходный код необходимо скачать
- Github, на главной странице [проекта](https://github.com/belousovsergey56/EventNotify)
- Нажать на зелёную кнопку `Code`
- В всплывающем окне выбрать `Download ZIP`
- Разархивировать код проекта в нужную директорию на ПК

## Переменные окружения

Для корректой работы программы, нужно:
- Создать файл `.env` в корне проекта, файл с точкой в начале имени (чтобы был скрыт в системе) 
- Добавить в него переменные, точное имя перененных для копирования ниже
```text
url_kuda_go = https://kudago.com/public-api
api_version = v1.4
tg_token = токен телеграм бота, можно скопировать у BotFather
tg_url = https://api.telegram.org
```

## Зависимости
- python - 3.13
- Flask - 3.1.2
- requests - 2.32.5
- apscheduler - 3.11.1
- python-dotenv - 1.2.1
- сервис для туннелирования (ngrok, tuna, etc.) - нет в файле зависимостей `requirements.txt` т.к. внешний сервис

## Запуск

- Установка зависимостей
```bash
pip install -r requirements.txt
```

- Запуск сервиса туннелирования
```bash
tuna http 5000
```

- Запуск приложения
> Вместо `localhost` нужно прописать https адрес предоставленный сервисом туннелирования
```bash
py main.py localhost
```

## Демонстрация

### Запуск туннеля
<img width="913" height="252" alt="image" src="https://github.com/user-attachments/assets/4133daf5-bbd4-41a6-b7ff-e54676bab26a" />

### Запуск приложения
#### Вариант через консоль
<img width="891" height="218" alt="image" src="https://github.com/user-attachments/assets/e81481e3-ef8c-4dc4-89eb-89e5176c8656" />

#### Вариант через VSCode
- Запуск кода через Debugging возможно только когда в VSCode открыт файл с точкой доступа т.е. `main.py`
<img width="723" height="400" alt="image" src="https://github.com/user-attachments/assets/d8a5119a-4ace-46e4-897c-531bfdf808b8" />

<img width="438" height="113" alt="image" src="https://github.com/user-attachments/assets/1c47a788-77e3-47be-9f92-ec7782f399cc" />

- Выбираем запуск скрипта с аргументом
<img width="635" height="291" alt="image" src="https://github.com/user-attachments/assets/5ff55fc9-ab21-469e-8d07-becaffd5ffcb" />

- В пустое поле вписываем адрес туннеля
<img width="636" height="118" alt="Снимок экрана 2025-12-26 215436" src="https://github.com/user-attachments/assets/c8a43320-ddea-414e-8bca-94c8084c2c7c" />

- Если перейти по адресу, увидим сообщение от бота
<img width="428" height="338" alt="image" src="https://github.com/user-attachments/assets/5ebbe9e1-4e40-4ec5-ad10-3f249ce1686f" />

### Telegram
<img width="638" height="696" alt="image" src="https://github.com/user-attachments/assets/aa1232e1-84f5-452f-aa1e-b17ca6d458f1" />

