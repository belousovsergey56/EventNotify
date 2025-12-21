# База данных

### Директория с файлом в проекте
```bash
├── app_database
│   └── crud.py
```
---

> Добавил в проект базау данных.
> База на SQLite - она идёт вместе с python и отдельно скачивать не нужно.
> Для не больших проектов то что нужно.

Добавил в проект директорию `app_database`, в неё добавил файл `crud.py`
**C** - create,
**R** - read,
**U** - update,
**D** - delete

Т.е. в файле содержатся функции по управлению данными базы данных

### Содержание файла
```python
import sqlite3

from functools import wraps
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def db_handler(func):
    """Декоратор подключения к базе и обработки ошибок"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with sqlite3.connect(f"{BASE_DIR}/users.db") as conn:
                return func(conn, *args, **kwargs)
        except sqlite3.OperationalError as e:
            print(f"Операционная ошибка: {e}")
            return {"error": "Ошибка выполнения операции с БД"}
        except sqlite3.Error as e:
            print(f"Ошибка SQLite: {e}")
            return {"error": "Ошибка базы данных"}
    return wrapper


@db_handler
def create_user_table(conn):
    """Создать таблицу user
    В базе данных users.db создаёт таблицу для хранения id пользователей.
    Таблица имеет всего один столбец, имя столбца user_id
    |user_id|
    +-------+
    |2      |
    +-------+
    |5      |
    +-------+
    и т.д.
    """
    cursor = conn.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS user (
                user_id varchar(100) PRIMARY KEY
            )
        """
    )
    conn.commit()


@db_handler
def add_id(conn, uid: str) -> bool:
    """Добавить id чата, пользователя в базу

    Returns:
        bool: True если операция удалась, False если завершилась с ошибкой
    """
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO user (user_id) VALUES (?)", (uid,))
    conn.commit()
    return cursor.rowcount > 0


@db_handler
def remove_id(conn, uid: str) -> bool:
    """Удалить id чата, пользователя из базы

    Returns:
        bool: True если операция удалась, False если завершилась с ошибкой
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE user_id = ?", (uid,))
    conn.commit()
    return cursor.rowcount > 0


@db_handler
def get_all_id(conn) -> list:
    """Получить все id в списке
    Returns:
        list[str]: Список id, [1, 2, 3, 4]
    """
    cursor = conn.cursor()
    uid_list = [i[0] for i in cursor.execute("SELECT user_id FROM user")]
    return uid_list
```

#### Импорты
- `sqlite3` - пакет который содержит методы взаимодействия python с базой
- `from functools import wraps` - из модуля `functools` имортируем `wraps` - это инструмент для реализации декоратора, чтобы не повторять один и тот же код
- `from pathlib import Path` - из модуля `pathlib` импортируем `Path` - библиотека для работы с путями в системе
- `BASE_DIR = Path(__file__).resolve().parent` - константа `BASE_DIR` - один раз объявляется в начале модуля, не меняет своего содержимого, в данном случае собирает в переменную путь до директории в которой содержится файл, где объявлена константа
`Path(__file__).resolve()` - это текущий файл в котором объявлена константа, т.е. вывод такой `/home/belousov/code/EventNotify/app/app_database/crud.py`
`parent` - убирает из пути файл, оставляя только путь к директории
Например как выглядит этот путь на моей системе: `/home/belousov/code/EventNotify/app/app_database`
На другом сервере будет другой путь, например: `/home/main_server/application/telegram_bots/EventNotify/app/app_database`
Это обеспечивает переносимость кода с одного ПК/сервера на другой.

### Функции
```python
def db_handler(func):
    """Декоратор подключения к базе и обработки ошибок"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with sqlite3.connect(f"{BASE_DIR}/users.db") as conn:
                return func(conn, *args, **kwargs)
        except sqlite3.OperationalError as e:
            print(f"Операционная ошибка: {e}")
            return {"error": "Ошибка выполнения операции с БД"}
        except sqlite3.Error as e:
            print(f"Ошибка SQLite: {e}")
            return {"error": "Ошибка базы данных"}
    return wrapper
```
- `def db_handler(func)` - объявление функции, аргументом будет другая функия
- `@wraps(func)` - декоратор для реализации декоратора, аргумент `func` пробрасывается сверху вниз
- `def wrapper(*args, **kwargs):` - объявление вложенной функци, которая реализует нужный нам функционал, чтобы не прописывать его в каждой функции. Функция принимает аргументы `*args` и `**kwargs`.
т.к. мы не можем знать какое количество аргументов будут содержать будущие функции, чтобы универсализировать этот момент в python реализован функционал распаковки `*` и `**`, одна `*` распаковывает позиционные аргументы: ("hello", "name", 5445), две `**` распаковыввает позиционные аргументы: (name="name", age=30)

Пример на простых функциях

`**args` возвращает словарь
```python
>>> def a(**args):
...     print(args)
...
>>> a()
{}
>>> a(name="sergey", age=39)
{'name': 'sergey', 'age': 39}
>>>
```

`*args` возвращает кортеж
```python
>>> def a(*args):
...     print(args)
...
>>>
>>> a()
()
>>> a(1)
(1,)
>>> a("hello", "world", 123, 456)
('hello', 'world', 123, 456)
>>>
```
Т.е. можно не думать о количестве аргументов, которые будут в функции. Имена `args` и `kwarg` - можно менять на любые другие, но рекомоендуются `args`, `kwargs` чтобы при чтении кода было понятно какой смысл несут аргументы функции.

- `try:` - попытка выполнить код
- `with sqlite3.connect(f"{BASE_DIR}/users.db") as conn:` - подключение к базе данных через контекстный менеджер `with` т.о. у нас обеспечивается автоматическое управление соединением с базой данных и гарантированое закрытие подлючение к базе.
`as conn` - означает что считать конструкцию до ключевого слова `as` как переменную `conn`. Если не использовать контекстый менеджер, то запись будет выглядеть следующим образом `conn = sqlite3.connect(f"{BASE_DIR}/users.db")`
- `sqlite3.connect` - вызов метода подключения к базе, аргументом служит строка которая содержит путь к базе, конструкция `f"{BASE_DIR}/users.db"` при выполнеии буде иметь вид `/home/belousov/code/EventNotify/app/app_database/users.db`
- `users.db` - файл базы данных
- `return func(conn, *args, **kwargs)` - функция возвращает переменную `conn` и остальные аргументы
- `except sqlite3.OperationalError as e:` - в блоке с подключением к базе мы можем ожидать операционную ошибку, чтобы программа не упала/не остановилась, прописываем возможную ошибку в коде блок `exception`
  - `print(f"Операционная ошибка: {e}")` - вывод текста ошибки в консоль
  - `return {"error": "Ошибка выполнения операции с БД"}` - возвращаемое значение функции в случае ошибки
- `except sqlite3.Error as e:` - ещё один обработчик ошибиа, но более обзего характера 
  - `print(f"Ошибка SQLite: {e}")` - вывод ошибки в консоль
  - `return {"error": "Ошибка базы данных"}` - возвращаемое значение функции в случае возбуждения ошибки
- `return wrapper` - возврашаемое значениме вложенной функции
---

```python
@db_handler
def create_user_table(conn):
    """Создать таблицу user
    В базе данных users.db создаёт таблицу для хранения id пользователей.
    Таблица имеет всего один столбец, имя столбца user_id
    |user_id|
    +-------+
    |2      |
    +-------+
    |5      |
    +-------+
    и т.д.
    """
    cursor = conn.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS user (
                user_id varchar(100) PRIMARY KEY
            )
        """
    )
    conn.commit()
```

- `@db_handler` - созданный ранее декоратор т.е. можно считать что блок `def wrapper(*args, **kwargs):` оборачивает текущую функцию, добавляя в нее реализованную в декораторе логику (код)
- `def create_user_table(conn):` - объявление функции, аргументом выступает созданное в декораторе подключение к базе данных
- `cursor = conn.cursor()` - в переменную `cursor` присваиваем объект курсор, если простыми словами ретрантранслятор команд в базу данных из кода python
- `cursoe.execute()` - данная функция позволяет текстовой строкой передать sql запрос используя синтаксис SQL
-  `CREATE TABLE IF NOT EXISTS user (user_id varchar(100) PRIMARY KEY)` - синтаксис sql довольно простой, практически английский
  - `CREATE TABLE IF NOT EXISTS` - Создать таблицу, если она не существует
  - имя таблицы `users`
  - `user_id varchar(100)` - таблица будет содержать одно поле(колонку) с имеменем `user_id`, тип поля `varchar`, колисчество символов 100
  - `PRIMARY KEY` - user_id считать уникальным и запретить запись дублей
- `conn.commit()` - записать изменения
---

```python
@db_handler
def add_id(conn, uid: str) -> bool:
    """Добавить id чата, пользователя в базу

    Returns:
        bool: True если операция удалась, False если завершилась с ошибкой
    """
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO user (user_id) VALUES (?)", (uid,))
    conn.commit()
    return cursor.rowcount > 0
```
- `add_id(conn, uid: str) -> bool:` - функция принимает уникальный id
- `cursor.execute("INSERT OR IGNORE INTO user (user_id) VALUES (?)", (uid,))`
  - `INSERT OR IGNORE INTO` - добавить или игнориоровать. Если значение в базе есть, то игнорировать, если нет, то записать
  - `user (user_id)` - запись в таблицу `user` в поле `user_id`
  - `VALUES (?)` - значениия, (?) - параметризированный sql запрос.
  - `(uid,)` - подтавляемое значение

> Параметризованный sql запрос является выжным элементом безопасности. SQL в данном случае будет его считать аргументом
> `f"cursor.execute("INSERT OR IGNORE INTO user (user_id) VALUES ({uid})"` - безопасным не считает т.к. sql будет считать всю строку запросом и не разделять на аргументы
> т.о. можно атаковать базу данных из вне sql инъекцией, параметризованный запрос исключает возможность инъекции.

- `conn.commit()` - принять изменения
- `return cursor.rowcount > 0` - вернуть `True`, если счётчик записи больше нуля(т.е. произошла запись в базу) иначе `False`
---

```python
@db_handler
def remove_id(conn, uid: str) -> bool:
    """Удалить id чата, пользователя из базы

    Returns:
        bool: True если операция удалась, False если завершилась с ошибкой
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE user_id = ?", (uid,))
    conn.commit()
    return cursor.rowcount > 0
```

- `remove_id(conn, uid: str) -> bool:` - удалить уникальный id из базы, принимаемый аргумент уникальный id
- `cursor.execute("DELETE FROM user WHERE user_id = ?", (uid,))`
  - `DELETE FROM user` - удалить из таблицы `user`
  - где значение поля `user_id` = `uid`
- `conn.commit()` - принять изменения
- `return cursor.rowcount > 0` - если удаление произошло успешно вернуть `True` иначе `False`
---

```python
@db_handler
def get_all_id(conn) -> list:
    """Получить все id в списке
    Returns:
        list[str]: Список id, [1, 2, 3, 4]
    """
    cursor = conn.cursor()
    uid_list = [i[0] for i in cursor.execute("SELECT user_id FROM user")]
    return uid_list
```

- `get_all_id(conn) -> list:` - функция возвращает список всех уникальных id
- `uid_list = [i[0] for i in cursor.execute("SELECT user_id FROM user")]` конструкция в `[]` называется `comprehension` - короткий способ записать цикл для создания списков, словарей или множеств вместо длинного for
  - `SELECT user_id FROM user` - из таблицы `user` выбрать столбец `user_id` и отдать занчения
    - возвращаемое занчение объект `cursor`, который является итератором и его можжно передать в цикл.
  - `for i in ` - пройти по каждому элементу списка, т.е `python` будет воспримнимать эту конструкцию как `for i in [(1,), (2,), (3,)]`
  - `i[0]` - вопринимается как `(1,)[0]`, получаемый результат `1` - `i[0]` это обращение к первому(и единственному) элементу кортежа
  - Получаемые данные добавляются в список, который будет храниться в переменной `uid_list`
  > Альтернативная форма записи
  >
  > ```python
  > uid_list = []
  > for i in cursor.execute("SELECT user_id FROM user"):
  >   uid_list.append(i[0])
  > ```
- `return uid_list` - возвращаем список элементов. `[1, 2, 3, 4, 5]`
---

> Есть конечно нюансы
> 
> Например `user_id varchar(100) PRIMARY KEY` - уникальное значение лучше делать не строковым, а числовым.
> 
> Так же пр проектировании базы данных один столбец всегда выступает индексом.
> 
> Имя базы `users.db`, а имя таблицы `user`. В сообществе разработчиков мнения расходятся, многие считают что имя таблицы должно быть во множественном числе, многие что в единственном.
> Я пробовал и так и так, мне кажется, что в единственном числе более читаемо получается.
> Таблица `user`, поля `name`, `user_id`, `age`, `address`. При обращении к таблице `select name, age from user` - запрашиваем имя и возраст пользовавтеля, а не пользователей.
>
> В общем это для справки.
