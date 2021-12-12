import json
import logging

import aiogram

from exportBot.Config import API_TOKEN
from database import add_new_user, get_users_info, delete_user, get_users_id
from aiogram import Bot, Dispatcher, executor, types
import sqlite3

from keyboards import create_first_keyboard, loop

con = sqlite3.connect('../bot.db')
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
superUser = [{
    "name": "admin",
    "user_id": 1158833233
}]


def IsAdmin(user_id):
    for i in superUser:
        if user_id == i["user_id"]:
            return True
        else:
            return False


def load():
    with open('data.json', encoding='utf-8', ) as json_file:
        data = json.load(json_file)
    return data


@dp.message_handler(commands=['list_users'])
async def get_users(message: types.Message):
    if IsAdmin(message['from'].id):
        info = '\n'.join(''.join(str(elems)) for elems in get_users_info())
        print(info)
        if len(info) == 0:
            await message.reply("список користувачів пустий")
        else:
            await message.reply(info)
    else:
        await message.reply("У вас немає доступу!")


@dp.message_handler(commands=['add_admin'])
async def add_admin(message: types.Message):
    if IsAdmin(message['from'].id):
        user_id = message.text.split(' ')
        superUser.append({"name": user_id[1], "user_id": user_id[2]})
        print(superUser)
        await message.reply("адміна добавлено")
    else:
        await message.reply("У вас немає доступу!")


@dp.message_handler(commands=['delete_admin'])
async def delete_admin(message: types.Message):
    if IsAdmin(message['from'].id):
        user_id = message.text.split(' ')
        for i in superUser:
            if i["user_id"] == user_id:
                superUser.remove(i)
                await message.reply("адміна видалено")
    else:
        await message.reply("У вас немає доступу!")


@dp.message_handler(commands=['list_admins'])
async def get_admins(message: types.Message):
    if IsAdmin(message['from'].id):
        await message.reply([*superUser])
    else:
        await message.reply("У вас немає доступу!")


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    response = add_new_user(message)
    await bot.send_message(message['from'].id, response)


@dp.message_handler(content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def new_member(message: types.Message):
    response = delete_user(message['from'].id)
    await bot.send_message(message['from'].id, response)


@dp.message_handler(commands=['н'])
async def send_message(message: types.Message):
    if IsAdmin(message['from'].id):
        message_info = message.text.split(' ', 1)
        for i in get_users_info():
            try:
                await bot.send_message(i[3], message_info[1])
            except aiogram.utils.exceptions.CantInitiateConversation:
                await message.reply(f'{i[1]} не можу отримати повіомлення!')
    else:
        await message.reply("У вас немає доступу!")


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    users = get_users_id()
    if str(message['from'].id) in users:
        await message.reply("Рухайтесь по меню", reply_markup=create_first_keyboard())
    else:
        await message.reply("У вас немає доступу!")


@dp.message_handler()
async def answer_text(message: types.Message):
    if message.text == "назад":
        await message.reply("Рухайтесь по меню", reply_markup=create_first_keyboard())
    else:
        data = load()
        data = next(loop(data, message.text))
        if type(data) == str and len(data) > 4096:
            for x in range(0, len(data), 4096):
                await message.reply(data[x:x + 4096])
        else:
            await message.reply(message.text, reply_markup=data) if type(data) != str else await message.reply(data)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
