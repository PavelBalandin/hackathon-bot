from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from User import *
import uuid

import requests
from config import TOKEN
from keyboard import *

from Post import *

import json

user_list = {}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
post = Post()


# ========== start ===========
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Покращимо Чернігів разом", reply_markup=markup_request)
    user = link_user(message.from_user.id)
    user.token = message.text[7:]
    print(user.token)
    print(message.text)
    # registration(message.from_user)


# ========== categories ===========
@dp.message_handler(commands=['categories'])
async def process_help_command(message: types.Message):
    user = link_user(message.from_user.id)

    user.post.first_name = message.from_user.first_name
    user.post.last_name = message.from_user.last_name

    if user.status_code == 0:
        user.status_code += 1
        await message.reply("Оберіть категорію, яка стосуеться вашого посту", reply_markup=inline_kb)


# ========== buttons handler ===========
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_button1(callback_query: types.CallbackQuery):
    user = link_user(callback_query.from_user.id)
    if user.status_code == 1:
        user.status_code += 1
        code = callback_query.data[-1]
        user.post.category = button_dictionary[callback_query.data].text
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Додайте фотографії')
    if user.status_code == 5:
        user = link_user(callback_query.from_user.id)
        code = callback_query.data[-1]
        if code == 'k':
            user.status_code = 0
            print(user.post.first_name)
            post.location = callback_query.message.location
            send_post(user)
        if code == 'l':
            user.status_code = 0
            await bot.send_message(callback_query.from_user.id, 'Cancel')


# ========== images handler ===========
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    user = link_user(message.from_user.id)
    if user.status_code == 2:
        user.status_code += 1
        await message.reply("Напишіть заголовок до посту")
        lll = len(message.photo)
        print(lll)
        for i in range(lll):
            path = 'images/' + str(uuid.uuid4()) + '.jpg'
            await message.photo[i].download(path)
            user.post.img_path.append({'path': path})


@dp.message_handler()
async def echo_message(msg: types.Message):
    user = link_user(msg.from_user.id)
    if user.status_code == 3:
        user.status_code += 1
        user.post.title = msg.text
        await msg.reply("Опишитіть проблему")
    elif user.status_code == 4:
        user.post.description = msg.text
        user.status_code += 1
        await msg.reply("Пост створенно, Ви дійсно хочете надіслати пост?", reply_markup=inline_confirm_kb)
    else:
        pass


def send_post(user):
    data = {
        'user_id': user.user_id,
        'first_name': user.post.first_name,
        'last_name': user.post.last_name,
        'category': user.post.category,
        'title': user.post.title,
        'description': user.post.description,
        'location': user.post.location,
        'images': user.post.img_path,
    }

    data_json = json.dumps(data, ensure_ascii=False)
    print(data_json)

    response = requests.post('https://httpbin.org/post', data={'key': 'value'})
    print(response)


def link_user(user_id):
    if user_list.get(user_id):
        return user_list[user_id]

    else:
        user = User(user_id, 0, Post())
        user_list[user_id] = user
        return user


def registration(user):
    data = {
        'user_id': user.user_id,
        'username': user.username,
        'first_name': user.post.first_name,
        'last_name': user.post.last_name,
        'phone': user.phone,
        'token': user.token
    }

    data_json = json.dumps(data, ensure_ascii=False)
    print(data_json)


@dp.message_handler(content_types=['location'])
async def handle_loc(message: types.Message):
    user = link_user(message.from_user.id)
    user.post.location['latitude'] = message.location.latitude
    user.post.location['longitude'] = message.location.longitude
    print(message.location)


@dp.message_handler(content_types=['contact'])
async def handle_con(message: types.Message):
    user = link_user(message.from_user.id)
    print(message)
    user.post.first_name = message.from_user.first_name
    user.post.last_name = message.from_user.last_name
    user.username = message.from_user.username
    user.phone = message.contact["phone_number"][1:]
    registration(user)


if __name__ == '__main__':
    executor.start_polling(dp)
