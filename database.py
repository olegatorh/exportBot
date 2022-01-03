import sqlite3
import re

try:
    sqlite_connection = sqlite3.connect('./bot.db', isolation_level=None)
    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")

    cursor.execute('''CREATE TABLE users (
                                       user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       name TEXT NOT NULL,
                                       joining_date datetime NOT NULL,
                                       telegram_id TEXT NOT NULL,
                                       admin boolean default FALSE
                                       );''')

    cursor.execute('''CREATE TABLE keyboards (
                                           keyboard_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                           keyboard_name TEXT NOT NULL,
                                           date datetime NOT NULL
                                           );''')

    cursor.execute('''CREATE TABLE categories (
                                           category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                           category_name TEXT NOT NULL,
                                           keyboard_list INTEGER,
                                           date datetime NOT NULL,
                                           FOREIGN KEY(keyboard_list) REFERENCES keyboards(keyboard_id)

                                           );''')

    cursor.execute('''CREATE TABLE categoriesData (
                                               data_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                               info_name TEXT,
                                               info_data TEXT,
                                               category_id INTEGER,
                                               date datetime NOT NULL,
                                               FOREIGN KEY(category_id) REFERENCES categories(category_id)
                                               );''')
    sqlite_connection.commit()


except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        print("Соединение с SQLite закрыто")


def add_new_user(message):
    user = cursor.execute(f"SELECT name FROM users WHERE telegram_id = {message['new_chat_members'][0].id}").fetchone()
    print(f'user in database - {user}')
    if user is None and message["from"].is_bot is False:
        cursor.execute("INSERT OR IGNORE INTO users (name, joining_date, telegram_id) VALUES (?, ?, ?)",
                       (message['new_chat_members'][0].username if message['new_chat_members'][0].username is not None
                        else message['new_chat_members'][0].first_name, message.date.strftime('%Y-%m-%d'),
                        message['new_chat_members'][0].id))
        return f"""{message['new_chat_members'][0].username if message['new_chat_members'][0].username is not None
        else message['new_chat_members'][0].first_name} added!"""
    elif user:
        return f"{user} вже існує в базі!"
    else:
        return f"не може бути добавлено!"
<<<<<<< HEAD


def add_new_keyboard(message):
    message_info = message.text.split(' ', 1)[1]
    cursor.execute(f"INSERT INTO keyboards (keyboard_name, date) VALUES (?, ?)",
                   (message_info, message.date.strftime('%Y-%m-%d'),)).fetchone()
    return "Добавлено нову клавіатуру!"


def add_new_category(message):
    message_info = message.text.split(' ', 2)
    print(message_info)
    cursor.execute(f"INSERT INTO categories (category_name, keyboard_list, date) VALUES (?, ?, ?)",
                   (message_info[1], message_info[2], message.date.strftime('%Y-%m-%d'),)).fetchone()
    return "Добавлено нову категорію!"


def add_new_category_data(message):
    message_info = message.text.split(' ', 2)
    print(message_info)
    cursor.execute(f"INSERT INTO categoriesData (info_name, info_data, category_id, date) VALUES (?, ?, ?, ?)",
                   (message_info[1], message_info[2], message.date.strftime('%Y-%m-%d'),)).fetchone()
    return "Добавлено нову категорію!"
=======
>>>>>>> 406bf491d317a16973b2d2e5f8c50b1382a8bae5


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
