# Установка среды разработки
### Скачать VSCode
- Переходим на сайт [VSCode](https://code.visualstudio.com)
- Жмём `Скачать для Windows`
<img width="748" height="356" alt="Снимок экрана 2025-12-23 225943" src="https://github.com/user-attachments/assets/2b30cec0-2f4e-4693-894f-602c66c10f3e" />


### Установка
- Запускаем скрипт установки
- Принимаем условия соглашения
- Если нужно меняем директорию установки файла
- Если нужно создаём ярлык на рабочем столе
- Можно установить галочки в чекбоксы, чтобы при нажатии правым кликом на файл была возможность открыть с помощью VSCode
- В общем и целом по всем пунктам можно всегда жать `Далее`
- VSCode после установки можно пока не открывать

### Настройка VSCode
- Скачиваем проект с [github](https://github.com/belousovsergey56/EventNotify)
<img width="1012" height="641" alt="image" src="https://github.com/user-attachments/assets/1ffdf838-1251-46c0-960d-b388e7241155" />

- Правым кликом на скаченный архив -> Извлеч всё.. -> Нажать на Обзор и выбрать директорию, куда распаковать архив. Я выбрал Документы и создал там директорию `test`, лучше назвать понятнее, например `code`
<img width="615" height="455" alt="image" src="https://github.com/user-attachments/assets/247d22f2-2318-482e-8771-a10df4a4aad9" />

- Откроется окно с распакованным проектом
- Правым кликом на директорию -> Открыть с помощью Code (если windows 11, тогда правый клик -> Показать дополнительные параметры -> Открыть с помощью Code)
<img width="477" height="320" alt="image" src="https://github.com/user-attachments/assets/e2a58d5e-cd6a-4a76-a61f-35066b622ade" />

- Откроется окно
- Ставим галочку, соглашаемся
<img width="544" height="408" alt="image" src="https://github.com/user-attachments/assets/4f187516-fe01-41c1-a24c-2cf85d0dbbc2" />

- При первом запуске будет Welcome гайд по VSCode, в целом можно закрыть или чтобы избежать повторных открытий Welcome, поставить галочку на `Mark Done`
<img width="564" height="564" alt="image" src="https://github.com/user-attachments/assets/2ed1de09-07ed-4fa4-9833-796fa70215e5" />

- Справа чат закрывем панель
- Слева открываем `Расширения`/`Extensions`
<img width="1205" height="806" alt="image" src="https://github.com/user-attachments/assets/8fd997e0-571a-4643-b4a8-c7fb0118d8dc" />

- В поле поиска пишем `Python`, устанавливаем Python от Microsoft (данное расширение помогает при написании кода (подсказки, ошибки и т.д.) и его запуске)
- Обычно можно python даже не искать расширение может быть в разделе Популярное
<img width="402" height="363" alt="Снимок экрана 2025-12-23 233124" src="https://github.com/user-attachments/assets/2620fe46-50ae-41f8-9025-2bcd012e52e3" />

<img width="387" height="193" alt="Снимок экрана 2025-12-23 233152" src="https://github.com/user-attachments/assets/f38f79f4-f02b-46be-9860-1985fee1c94e" />

- Открываем консоль: Terminal -> New Terminal или сочетанием клавиш ctrl+shift+` (это русское ё)
<img width="626" height="124" alt="image" src="https://github.com/user-attachments/assets/0d5c1af2-eab1-474b-845e-1b35d7e897b0" />

- Нужно создать виртуальное окружение, для этого вводим команду в открывшемся терминале `py -m venv .venv`
- Соглашаемся с VSCode
<img width="1579" height="324" alt="image" src="https://github.com/user-attachments/assets/48e9fe74-87fb-4d9f-a49e-caceb5c5b253" />

- После установки, VSCode подтянет виртуальное окружение, в правом нижнем углу в стороке состояния, версия python сменится с глобальной на версию виртуального окружения
<img width="455" height="56" alt="image" src="https://github.com/user-attachments/assets/0a015cca-d226-4609-b0ba-b10b269a932d" />


- Активируем виртуальное окружение в терминале (виртуальное окружение необходимо для того, чтобы не засорять операционную систему ненужными файлами, все файлы которые ставятся легко удаляются при уничтожении директории .venv, так же можно хранить на ПК моно разных проектов с разными версиями пакетов(библиотек) и они никогда не пересекутся т.к. ставятся не глобально в систему, а только в конкретный проект)
  - `.\.venv\Scripts\activate`
  - Если ошибка
  <img width="1536" height="154" alt="image" src="https://github.com/user-attachments/assets/b3d0c314-bb26-4696-befa-f3473c3cf712" />

  - Пуск -> PowerShell -> Запуск от имени администратора
  - `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` -> `Y` -> `Enter` - это позволяет выполнять скрипты в powershell
  - `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Restricted` -> `S` -> `Enter` - это чтобы приостановить разрешение
  <img width="984" height="333" alt="image" src="https://github.com/user-attachments/assets/9ec732a1-df13-46a0-8efb-0c66fbd82ca8" />

- При активации окружения, в терминале появится подпись
> Возможно даже не придётся вводить команду активации `.\.venv\Scripts\activate`, после получения разрешения, `vscode` сам может активировать при перезагрузке терминала
<img width="495" height="116" alt="image" src="https://github.com/user-attachments/assets/557cf723-54ba-490a-a84b-019b8eff1e7a" />

- Для проверки, что код запускается в корне проекта создать файл `test.py`
<img width="321" height="498" alt="image" src="https://github.com/user-attachments/assets/1384d0eb-feda-4e9d-9160-0c39eb39396a" />

- Справа в окне ввода текст, пишем простоую программу `print("Hello, World!")` - сохраняем ctrl+s
<img width="370" height="151" alt="image" src="https://github.com/user-attachments/assets/2f9082c6-066f-46fc-86ee-a9570782c12c" />

- Запускаем `F5`
- При первом запуске всплывёт окно, выбираем Python Debugger
<img width="880" height="196" alt="image" src="https://github.com/user-attachments/assets/b03482c1-321f-4a66-8249-6419fc20bc1e" />

- выбираем первую строчку, текущий файл без аргументов
<img width="829" height="137" alt="image" src="https://github.com/user-attachments/assets/5d332826-046f-42b0-b3c1-3a92c1e20545" />

- Результат в консоли
<img width="938" height="134" alt="image" src="https://github.com/user-attachments/assets/434efd30-1197-497c-ac9e-bea163736612" />

- Так же можно запустить выполнение айла из консоли `py .\test.py`
<img width="573" height="106" alt="image" src="https://github.com/user-attachments/assets/22f00e60-ea5f-4a17-9063-f82cdd4154ea" />

- Файл `test.py` можно удалить
