from aiogram import types

start_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(
    types.KeyboardButton('Крипта'),
    types.KeyboardButton('Банки'),
    types.KeyboardButton('Документы'),
    types.KeyboardButton('Прочие системы'),
    types.KeyboardButton('О нас'),
)

crypt_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(
    types.KeyboardButton('Binance'),
    types.KeyboardButton('Metamusk'),
    types.KeyboardButton('Хуй3'),
    types.KeyboardButton('Хуй4'),
    types.KeyboardButton('Назад'),
)

banks_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True).add(
    types.KeyboardButton('Казахстан'),
    types.KeyboardButton('Россия'),
    types.KeyboardButton('Украина'),
    types.KeyboardButton('Назад'),
)

russia_bank_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True).add(
    types.KeyboardButton('Россия1'),
    types.KeyboardButton('Россия2'),
    types.KeyboardButton('Россия3'),
    types.KeyboardButton('Назад'),
)

ukraine_bank_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True).add(
    types.KeyboardButton('Украина1'),
    types.KeyboardButton('Украина2'),
    types.KeyboardButton('Украина3'),
    types.KeyboardButton('Назад'),
)

kazahstan_bank_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True).add(
    types.KeyboardButton('Казах1'),
    types.KeyboardButton('Казах2'),
    types.KeyboardButton('Назад'),
)


