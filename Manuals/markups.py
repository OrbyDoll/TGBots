from aiogram import types
import config as cfg

categor_choose_forward = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(
        text="NEW!🏺АУКЦИОН BY PRADA🏺", callback_data="АУКЦИОН BY PRADA"
    ),
    types.InlineKeyboardButton(
        text="🏠НЕДВИГА 1.0 BY PRADA🏠", callback_data="НЕДВИГА 1.0 BY PRADA"
    ),
    types.InlineKeyboardButton(
        text="🏠НЕДВИГА 2.0 BY PRADA🏠", callback_data="НЕДВИГА 2.0 BY PRADA"
    ),
    types.InlineKeyboardButton(text="💊N@RKO BY PRADA💊", callback_data="N@RKO BY PRADA"),
    types.InlineKeyboardButton(text="📑МФО BY PRADA📑", callback_data="МФО BY PRADA"),
    types.InlineKeyboardButton(text="⛓ШАНТАЖ Х3 BY PRADA⛓", callback_data="shantazh"),
    types.InlineKeyboardButton(text="Вперед➡️", callback_data="forward"),
)

categor_choose_back = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(
        text="💱EXCHANGE BY PRADA💱", callback_data="EXCHANGE BY PRADA"
    ),
    types.InlineKeyboardButton(text="⚙️ADMINISTRATOR⚙️", callback_data="ADMINISTRATOR"),
    types.InlineKeyboardButton(
        text="📜ПОСОБИЯ BY PRADA📜", callback_data="ПОСОБИЯ BY PRADA"
    ),
    types.InlineKeyboardButton(
        text="🕵️‍♂️SAFETY 1.0 BY PRADA💻 (техника)", callback_data="SAFETY 1.0 BY PRADA (техника)"
    ),
    types.InlineKeyboardButton(
        text="🕵️‍♂️SAFETY 2.0 BY PRADA🧠 (поведение)", callback_data="SAFETY 2.0 BY PRADA (поведение)"
    ),
    types.InlineKeyboardButton(
        text="🕵️‍♂️SAFETY 3.0 BY PRADA💰 (отмыв)", callback_data="SAFETY 3.0 BY PRADA (отмыв)"
    ),
    types.InlineKeyboardButton(text="Назад⬅️", callback_data="back"),
)
