# Настройка туннелирования
> Эта технология позволяет разработанное приложение на своем компьютере, через туннель протестировать в интернете, не размещая на сервере.

- Переходима на сайт [tuna](https://tuna.am)
- `Войти` - можно или создать аккаунт или войти под учётной записью от `google`, `yandex`, `mail.ru`
<img width="852" height="704" alt="image" src="https://github.com/user-attachments/assets/70f883aa-ebb1-42bc-b0ea-b510b28af780" />

- В левом сайдбаре если не открылось по умолчанию, выбираем `Быстрый старт`
<img width="369" height="256" alt="image" src="https://github.com/user-attachments/assets/b4931b02-6a57-46af-95f0-b098e9ae9910" />

- Справа окно с контентом, выбираем `Windows`
<img width="1006" height="190" alt="image" src="https://github.com/user-attachments/assets/cef66ea7-97fd-408c-b76d-0a54f33594ba" />

- Запускаем на ПК `Windows PowerShell` (если не хватит прав на установку, то открыть PowerShell от имени администратора)
- Выполняем шаг 1 - установка клиента 
<img width="1122" height="733" alt="image" src="https://github.com/user-attachments/assets/a51904b7-b2aa-48ca-848a-ad5be45a4b0e" />

- Выполняем шаг 2 (PowerShell пользователя, НЕ администратора)
<img width="1282" height="385" alt="image" src="https://github.com/user-attachments/assets/ad891272-5be0-49da-8b60-40dcda50107d" />

- Запуск туннеля в PowerShell с помощью команды `tuna http 8080` (порт 8080 нужно заменить тем портом, на которым работает приложение)
<img width="886" height="286" alt="image" src="https://github.com/user-attachments/assets/cfc1a70a-8681-4301-be8a-93f5f5adc462" />

- `https://kdmxze-178-252-83-236.ru.tuna.am` - tuna генерирует dns адрес по которому будет доступно приложение в течении 30 минут (т.к. тестовый аккаунт), этот адрес и нужен будет для тестирования приложения.
При переходе по адресу, откроется сайт с информационным окном, нужно подтвердить переход на страницу
<img width="1009" height="548" alt="image" src="https://github.com/user-attachments/assets/b712a887-af1a-4c9b-81a4-af5a268a3dc4" />

 т.к. на localhot сейчас ничего нет возникнет ошибка `502`, при запуске приложения будет страничка бота.
 <img width="1003" height="303" alt="image" src="https://github.com/user-attachments/assets/d1dc3ea8-ee2f-43e6-ab91-d71c0ddf80e2" />

В териминале будут логгироваться запросы и ответы
<img width="812" height="250" alt="image" src="https://github.com/user-attachments/assets/f1a3e8ae-9f22-48ce-96f5-b6730823c8ab" />

Можно перейти на страницу `http://127.0.0.1:4040`, чтобы увидеть более подробно заголовки и тело запросов/ответов (полезно при отладке)
<img width="1549" height="1020" alt="image" src="https://github.com/user-attachments/assets/99806660-e3aa-4deb-83a7-904ba224586b" />

> Чтобы остановить скрипт запущенный в терминале, нужно нажать сочетание клавиш `ctrl+c`
>
> Это касается любого скрипта запущенного вручную и работа которого перед глазами: tuna, запущенный сервер приложения, чтение логов и т.д.
<img width="906" height="295" alt="image" src="https://github.com/user-attachments/assets/6d8fe8d2-0ab6-43d2-98d2-24a9b7088994" />
