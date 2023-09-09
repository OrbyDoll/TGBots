from aiogram import types
import config as cfg

categor_choose_forward = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(text="НЕДВИГА 2.0 BY PRADA", callback_data='nedviga'),
    types.InlineKeyboardButton(text="N@RKO BY PRADA", callback_data='narko'),
    types.InlineKeyboardButton(text="МФО BY PRADA", callback_data='mfo'),
    types.InlineKeyboardButton(text="ШАНТАЖ Х3 BY PRADA", callback_data='shantazh'),
    types.InlineKeyboardButton(text="EXCHANGE BY PRADA", callback_data='exchange'),
    types.InlineKeyboardButton(text="Вперед", callback_data='forward')
)

categor_choose_back = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(text="ПОСОБИЯ BY PRADA", callback_data='posobiya'),
    types.InlineKeyboardButton(text="NEW! АУКЦИОН BY PRADA", callback_data='auction'),
    types.InlineKeyboardButton(text="SAFETY 1.0 BY PRADA (техника)", callback_data='tehnica'),
    types.InlineKeyboardButton(text="SAFETY 2.0 BY PRADA (поведение)", callback_data='povedeniye'),
    types.InlineKeyboardButton(text="SAFETY 3.0 BY PRADA (отмыв)", callback_data='otmiv'),
    types.InlineKeyboardButton(text="Назад", callback_data='back')
)