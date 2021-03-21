from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json
import requests
import uuid

from models.Post import *
from models.User import *
from config import TOKEN
from keyboard import *

user_list = {}
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
post = Post()


# ========== start ===========
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Щоб завершити реєстрацію додайте номер телефону", reply_markup=markup_request)
    user = link_user(message.from_user)
    user.token = message.text[7:]


# ========== categories ===========
@dp.message_handler(commands=['categories'])
async def process_help_command(message: types.Message):
    user = link_user(message.from_user)
    if user.status_code == 0:
        user.status_code += 1
        await message.reply("Оберіть категорію, яка стосуеться вашого посту", reply_markup=inline_kb)


# ========== buttons handler ===========
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_button1(callback_query: types.CallbackQuery):
    user = link_user(callback_query.from_user)
    if user.status_code == 1:
        user.status_code += 1
        code = callback_query.data[-1]
        user.post.category = button_dictionary[callback_query.data].text
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Додайте фотографії')
    if user.status_code == 5:
        user = link_user(callback_query.from_user)
        code = callback_query.data[-1]
        if code == 'k':
            user.status_code = 0
            await bot.send_message(callback_query.from_user.id, 'Пост успішно надіслано !')
            send_post(user)
            user.post = Post()
        if code == 'l':
            user.status_code = 0
            user.post = Post()
            await bot.send_message(callback_query.from_user.id, 'Пост скасований !')


# ========== images handler ===========
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    user = link_user(message.from_user)
    if user.status_code == 2:
        user.status_code += 1
        await message.reply("Напишіть заголовок до посту")
        lll = len(message.photo)
        print(lll)
        for i in range(lll):
            path = str(uuid.uuid4()) + '.jpg'
            await message.photo[i].download('images/' + path)
            user.post.img_path.append({'path': path})


@dp.message_handler()
async def echo_message(msg: types.Message):
    user = link_user(msg.from_user)
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
        'title': user.post.title,
        'location': {"x": user.post.location["latitude"], "y": user.post.location["longitude"]},
        'category': {'name': user.post.category},
        'description': user.post.description,
        'images': user.post.img_path,
    }

    data_json = json.dumps(data, ensure_ascii=False)

    print(data_json)
    encode_data = data_json.encode('utf-8')
    response = requests.post('http://194.62.98.10:8075/api/problems/', encode_data,
                             headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    print(response)


def link_user(user):
    if user_list.get(user.id):
        return user_list[user.id]

    else:
        new_user = User(user.id,
                        user.username,
                        user.first_name,
                        user.last_name,
                        0,
                        Post())

        user_list[user.id] = new_user
        return new_user


def registration(user):
    data = {
        'user_id': user.user_id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'token': user.token
    }

    data_json = json.dumps(data)
    print(data_json)
    response = requests.post('http://194.62.98.10:8075/api/auth/telegram', data_json,
                             headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    print(response)


@dp.message_handler(content_types=['location'])
async def handle_loc(message: types.Message):
    user = link_user(message.from_user)
    user.post.location['latitude'] = message.location.latitude
    user.post.location['longitude'] = message.location.longitude
    print(message.location)


@dp.message_handler(content_types=['contact'])
async def handle_con(message: types.Message):
    user = link_user(message.from_user)
    print(message)
    user.post.first_name = message.from_user.first_name
    user.post.last_name = message.from_user.last_name
    user.username = message.from_user.username
    user.phone = message.contact["phone_number"][1:]
    registration(user)


if __name__ == '__main__':
    executor.start_polling(dp)
