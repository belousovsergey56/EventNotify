# Создание и настройка телеграм бот

## Создать телеграм бот

- Открыть приложение Telegram (любой доступный клиент веб, десктоп или мобильный)
- Ищем чатик [BotFather](https://t.me/BotFather)
<img width="413" height="775" alt="image" src="https://github.com/user-attachments/assets/26dd0fd9-ac81-43e2-b470-a8835f0e8905" />

> это бот по созданию ...ботов

- Откроется чатик. Если начать вводить сообщение с символа слэш `/` - появится выбор команд, выбираем `/create a new bot`
<img width="550" height="615" alt="image" src="https://github.com/user-attachments/assets/bfd852e6-e815-4be8-81b1-98b9dbe85ecc" />

- Далее нужно выполнять комнадны бота
  - Дать название боту
  <img width="499" height="168" alt="image" src="https://github.com/user-attachments/assets/ddbc41d4-f3ae-41c6-bab4-d2c55478d06f" />

  - Дать имя пользователя боту (имя пользователя поменять будет нельзя, только пересоздать бот)
  - Как результат получим ответ. что бот создан и можно его настроить.
  - Кроме этого в сообщении будет api токен бота, который нам нужен
  <img width="497" height="382" alt="image" src="https://github.com/user-attachments/assets/db749eb2-19b7-4807-95e8-7e0f3ce485e4" />
---

## Настройка бота

> Необходимо минимально настроить бот
>
> Прописать описание и команды, картинка на усмотрение

- Пишем BotFather команду `/mybots`
- Выбираем соданного бота 
<img width="476" height="174" alt="image" src="https://github.com/user-attachments/assets/6dd7aa91-71a8-4c7f-9428-f1bfa48569c9" />

- В открывшемся меню выбираем `Edit Bot`
<img width="378" height="204" alt="image" src="https://github.com/user-attachments/assets/9d441315-6683-4850-b6e0-8654bb34b93e" />

- Далее `Edit Commands`, так же выше списка возможностей изменения указаны статусы, что хорошо бы поправить
<img width="427" height="352" alt="image" src="https://github.com/user-attachments/assets/82d6866e-4b0d-4d12-b04e-705e0f87a89a" />

- После нажатия кнопки, BotFather будет ждать ввода команд для бота, отправляем всё в одном сообщении (каждая команда имеет свою логику в коде)
```text
start - Добавить в рассылку
delete - Убрать из рассылки
event - Отправить в чат данные по событиям без подписки
help - Что умеет этот бот
```
<img width="533" height="434" alt="image" src="https://github.com/user-attachments/assets/0f843907-3e8a-4197-99de-1d97d011be15" />

Данные обновились

<img width="451" height="188" alt="image" src="https://github.com/user-attachments/assets/a553dee3-efbe-4a6c-b201-b4ee7b9b8804" />

> Команды отобразятся в списке выбора при нажатии на кнопку `Меню` или если начать вводить символ слэш `/`

<img width="598" height="233" alt="image" src="https://github.com/user-attachments/assets/d82d996e-ae56-4d05-b7ef-aaefbc206aa7" />
---

### Опиционально
- Добавить описание в профиль

<img width="501" height="426" alt="image" src="https://github.com/user-attachments/assets/b0792e4f-47ea-4d80-893f-c018c2b09657" />

<img width="416" height="626" alt="image" src="https://github.com/user-attachments/assets/4065b742-5511-461e-b781-0594e451d92c" />

---

- Добавить описание в приветственное сообщение

<img width="520" height="451" alt="image" src="https://github.com/user-attachments/assets/5b272e95-d76a-403d-ad37-679a2bc61773" />

<img width="534" height="185" alt="image" src="https://github.com/user-attachments/assets/52f3ff74-5341-4b6a-8202-e34faf17772a" />

---

- Добавить картинку в профиль бота
- В сообщение просто отправить файл с картинкой

<img width="444" height="378" alt="image" src="https://github.com/user-attachments/assets/417415a5-aae8-4fbf-a689-87ef1042083e" />

<img width="519" height="496" alt="image" src="https://github.com/user-attachments/assets/a0e121d3-b066-4eda-a210-27930dedb8c1" />

<img width="409" height="400" alt="image" src="https://github.com/user-attachments/assets/f3558426-0c52-4fa7-ad76-f431528ccadb" />

---

- Поменять картинку в приветсвенном сообщении
<img width="478" height="281" alt="image" src="https://github.com/user-attachments/assets/4857b645-d212-4a7f-b179-bff994001449" />

<img width="513" height="361" alt="image" src="https://github.com/user-attachments/assets/d7700c48-72f1-462b-983d-0111de5d5956" />

<img width="525" height="379" alt="image" src="https://github.com/user-attachments/assets/cfecb47e-3950-45b4-a110-804c81c355ad" />

---

### Получить токен

- В главном меню выбранного бота выбрать `API Token`
<img width="454" height="266" alt="image" src="https://github.com/user-attachments/assets/c844d180-804a-4c49-852a-df79953950dc" />

- В ответ полуим токен для копирования
<img width="513" height="197" alt="image" src="https://github.com/user-attachments/assets/6f5e7256-8ac5-4eb3-8713-98ee500d9cde" />

### Перейти к созданному боту
- В сообщении от `BotFather` после создания будет ссылка на созданный бот, там можно проверить все примененные натройки
<img width="497" height="382" alt="image" src="https://github.com/user-attachments/assets/339ce83c-3603-402b-9a48-187cde27f25b" />

- Или можно найти бот по имени пользователя бота, которое изменить нельзя
<img width="995" height="829" alt="image" src="https://github.com/user-attachments/assets/31ca1a27-689e-4975-9a63-9383b5357b3d" />
