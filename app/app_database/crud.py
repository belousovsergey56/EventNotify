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
