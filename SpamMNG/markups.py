from aiogram import types

answer_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton(text="Answer User", one_time_keyboard=True)
)
types.reply

def get_users_markup(database):
    users_markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, row_width=2
    )
    for user in database.get_active_users():
        users_markup.add(
            types.KeyboardButton(text=f"{user[0]} - {user[1]} Написал - {user[2]}")
        )
    return users_markup