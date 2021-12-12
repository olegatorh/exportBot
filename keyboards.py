from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup
import json

with open('data.json', encoding='utf-8', ) as json_file:
    data = json.load(json_file)


def keyboards_creator(content):
    return list(item for sublist in content for item in sublist)


def content_creator(content):
    return list(item for sublist in content for item in sublist.values())


def add_buttons(button_value, index):
    return InlineKeyboardButton(button_value, callback_data=index)


def create_first_keyboard():
    button_names = get_categories(data)
    inline_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_buttons = [add_buttons(button, index) for index, button in enumerate(button_names)]
    for button in kb_buttons:
        inline_kb.add(button)
    return inline_kb


def get_categories(data):
    category_names = [i["category_name"] for i in data]
    return category_names


def create_keyboard(data):
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_buttons = [add_buttons(button["category_name"], index) for index, button in enumerate(data)]
    for button in kb_buttons:
        reply_keyboard.add(button)
    return reply_keyboard.add(InlineKeyboardButton("назад", callback_data="назад"))


def loop(data, category_word):
    for i in data:
        if i["category_name"] == category_word and type(i["category_data"]) != str:
            yield create_keyboard(i["category_data"])
        if i["category_name"] == category_word and type(i["category_data"]) == str:
            yield i["category_data"]
        else:
            if type(i["category_data"]) != str:
                for n in i["category_data"]:
                    if n["category_name"] == category_word and type(n["category_data"]) == str:
                        yield n["category_data"]
