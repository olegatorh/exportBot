import sqlite3
import re

try:
    sqlite_connection = sqlite3.connect('./bot.db', isolation_level=None)
    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")

    cursor.execute('''CREATE TABLE users (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       name TEXT NOT NULL,
                                       joining_date datetime NOT NULL,
                                       telegram_id TEXT NOT NULL,
                                       admin boolean default FALSE
                                       );''')
    sqlite_connection.commit()


except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        print("Соединение с SQLite закрыто")


def add_new_user(message):
    user = cursor.execute(f"SELECT name FROM users WHERE telegram_id = {message['new_chat_members'][0].id}").fetchone()
    if user is None:
        cursor.execute("INSERT OR IGNORE INTO users (name, joining_date, telegram_id) VALUES (?, ?, ?)",
                       (message['new_chat_members'][0].username if message['new_chat_members'][0].username is not None
                        else message['new_chat_members'][0].first_name, message.date.strftime('%Y-%m-%d'),
                        message['new_chat_members'][0].id))
        return f"""{message['new_chat_members'][0].username if message['new_chat_members'][0].username is not None
        else message['new_chat_members'][0].first_name} added!"""
    else:
        return f"{user} already in database!"


def delete_user(message):
    user = cursor.execute(f"SELECT name FROM users WHERE telegram_id = {message['left_chat_member'].id}").fetchone()
    if user is None:
        return f"there is no user with this {message['left_chat_member'].id} id"
    else:
        cursor.execute(f"DELETE FROM users WHERE telegram_id = {message['left_chat_member'].id}").fetchone()
        return f"{re.sub(',', '', str(user))} deleted"


def get_users_info():
    return cursor.execute("SELECT * from users").fetchall()


def get_users_id():
    users_id = cursor.execute("SELECT telegram_id from users").fetchall()
    users_id = [i[0] for i in users_id]
    return users_id


def get_user_by_id(user_id):
    return cursor.execute("SELECT * FROM users WHERE telegram_id = ?", [user_id]).fetchone()


def update_user_settings(column, value, telegram_id):
    cursor.execute(f"UPDATE OR IGNORE users SET {column} = {value} WHERE telegram_id = {telegram_id}").fetchone()
    return "адміна добавлено"
