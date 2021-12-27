import json
import logging

import aiogram

from Config import API_TOKEN
from database import add_new_user, get_users_info, delete_user, get_users_id, get_user_by_id, update_user_settings
from aiogram import Bot, Dispatcher, executor, types
import sqlite3

from keyboards import create_first_keyboard, loop

con = sqlite3.connect('./bot.db')
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def load():
    with open('data.json', encoding='utf-8', ) as json_file:
        data = json.load(json_file)
    return data


@dp.message_handler(commands=['list_users'])
async def get_users(message: types.Message):
    if get_user_by_id(message['from'].id)[4] == 1:
        info = '\n'.join(''.join(str(elems)) for elems in get_users_info())
        if len(info) == 0:
            await message.reply("список користувачів пустий")
        else:
            await message.reply(info)
    else:
        await message.reply(f'у вас немає доступу!')


@dp.message_handler(commands=['add_admin'])
async def add_admin(message: types.Message):
    user_id = message.text.split(' ')[1]
    user = update_user_settings('admin', True, user_id)
    await message.reply(user)


@dp.message_handler(commands=['all'], content_types=['document'])
async def send_message(message: types.Message):
    if get_user_by_id(message['from'].id)[4] == 1:
        message_info = message.text.split(' ', 1)
        for i in get_users_info():
            try:
                await bot.send_message(i[3], message_info[1])
            except aiogram.utils.exceptions.CantInitiateConversation:
                await message.reply(f'{i[1]} не може отримати повідомлення!')
    else:
        await message.reply(f'у вас немає доступу!')


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    users = get_users_id()
    if str(message["from"].id) in users:
        await message.reply("Рухайтесь по меню", reply_markup=create_first_keyboard())


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    response = add_new_user(message)
    users = get_users_info()
    for i in users:
        if i[4] == 1:
            await bot.send_message(i[3], response)


@dp.message_handler(content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def new_member(message: types.Message):
    response = delete_user(message)
    users = get_users_info()
    for i in users:
        if i[4] == 1:
            await bot.send_message(i[3], response)


@dp.message_handler()
async def answer_text(message: types.Message):
    users = get_users_id()
    if str(message["from"].id) in users:
        if message.text == "назад":
            await message.reply("Рухайтесь по меню", reply_markup=create_first_keyboard())
        else:
            data = load()
            data = next(loop(data, message.text))
            if type(data) == str and len(data) > 4096:
                for x in range(0, len(data), 4096):
                    await message.reply(data[x:x + 4096], parse_mode='HTML')
            else:
                print(data)
                await message.reply(message.text, reply_markup=data, parse_mode='HTML') if type(data) != str else \
                    await message.reply(data, parse_mode='HTML')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
