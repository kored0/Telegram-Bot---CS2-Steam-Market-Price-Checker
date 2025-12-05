from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='💵Найти цену.', callback_data="price")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Кто вы?"
)