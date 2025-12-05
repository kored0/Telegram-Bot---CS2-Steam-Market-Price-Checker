from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🗓️ Расписание", callback_data="расписание")
        ]
    ]
)
