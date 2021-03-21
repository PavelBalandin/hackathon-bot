from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# ======== buttons ========
line_btn_1 = InlineKeyboardButton('транспорт та дороги', callback_data='btn1', content_types=['location'])
line_btn_2 = InlineKeyboardButton('благоустрій міста та будівництво', callback_data='btn2', content_types=['location'])
line_btn_3 = InlineKeyboardButton('соціальний захист та охорона праці', callback_data='btn3')
line_btn_4 = InlineKeyboardButton('сім’я, молодь, діти', callback_data='btn4')
line_btn_5 = InlineKeyboardButton('освіта', callback_data='btn5')
line_btn_6 = InlineKeyboardButton('екологія', callback_data='btn6')
line_btn_7 = InlineKeyboardButton('охорона здоровя', callback_data='btn7')
line_btn_8 = InlineKeyboardButton('житлово-комунальне господарство', callback_data='btn8')
line_btn_9 = InlineKeyboardButton('економіка та фінанси', callback_data='btn9')
line_btn_10 = InlineKeyboardButton('інші', callback_data='btn10')

# ======== keyboard ========
inline_kb = InlineKeyboardMarkup().add(line_btn_1)
inline_kb.add(line_btn_2)
inline_kb.add(line_btn_3)
inline_kb.add(line_btn_4)
inline_kb.add(line_btn_5)
inline_kb.add(line_btn_6)
inline_kb.add(line_btn_7)
inline_kb.add(line_btn_8)
inline_kb.add(line_btn_9)
inline_kb.add(line_btn_10)

button_dictionary = {
    line_btn_1.callback_data: line_btn_1,
    line_btn_2.callback_data: line_btn_2,
    line_btn_3.callback_data: line_btn_3,
    line_btn_4.callback_data: line_btn_4,
    line_btn_5.callback_data: line_btn_5,
    line_btn_6.callback_data: line_btn_6,
    line_btn_7.callback_data: line_btn_7,
    line_btn_8.callback_data: line_btn_8,
    line_btn_9.callback_data: line_btn_9,
    line_btn_10.callback_data: line_btn_10,
}

# ======== confirm buttons ========
line_btn_ok = InlineKeyboardButton('Надіслати', callback_data='btn_ok', request_location=True)
line_btn_cancel = InlineKeyboardButton('Скасувати', callback_data='btn_cancel')

# ======== confirm keyboard ========
inline_confirm_kb = InlineKeyboardMarkup().add(line_btn_ok)
inline_confirm_kb.add(line_btn_cancel)

markup_request = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(KeyboardButton('Відправити телефон ☎️', request_contact=True)) \
    .add(KeyboardButton('Відправити геолокацію 🗺️', request_location=True))
