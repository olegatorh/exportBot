import sqlite3

try:
    sqlite_connection = sqlite3.connect('../telegram_bot.db', isolation_level=None)
    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")

    sqlite_create_table_query = '''CREATE TABLE users (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       name TEXT NOT NULL,
                                       joining_date datetime NOT NULL,
                                       telegram_id TEXT NOT NULL
                                       );'''
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        print("Соединение с SQLite закрыто")


def add_new_user(message):
    user = cursor.execute("SELECT id, name FROM users WHERE name = ?",
                          (message['new_chat_members'][0].username,)).fetchone()
    if user is None:
        cursor.execute("INSERT OR IGNORE INTO users (name, joining_date, telegram_id) VALUES (?, ?, ?)",
                       (message['new_chat_members'][0].username,
                        message.date.strftime('%Y-%m-%d'),
                        message['new_chat_members'][0].id))
        return f"{message['new_chat_members'][0].username} added!"
    else:
        return f"{user} already in database!"


def get_users_info():
    return cursor.execute("SELECT * from users").fetchall()


def get_users_id():
    users_id = cursor.execute("SELECT telegram_id from users").fetchall()
    users_id = [i[0] for i in users_id]
    return users_id


def delete_user(user_id):
    user = cursor.execute("SELECT id, name FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        return f"there is no user with this {user_id}-id"
    else:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,)).fetchone()
        return f"{user} deleted"
