from aiogram import types

start_menu = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True).row(
    types.KeyboardButton('Заказать'),
).row(
    types.KeyboardButton('Условия'),
    types.KeyboardButton('О нас'),
)

back_to_start_menu = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton('Назад в меню', callback_data='back_to_start_menu')
)