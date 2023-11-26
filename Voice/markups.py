from aiogram import types
import config as cfg
from filesMass import voices, circles, pictures
import math

start_menu = types.ReplyKeyboardMarkup(
    row_width=2, resize_keyboard=True, one_time_keyboard=True
).add(
    types.KeyboardButton("Гс"),
    types.KeyboardButton("Кружки"),
    types.KeyboardButton("Картинки"),
    types.KeyboardButton("Хуйня"),
)

menu_hide = types.ReplyKeyboardRemove()

categor_choose = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton(text="🌐UNIVERSAL🌐", callback_data="cat_universal"),
    types.InlineKeyboardButton(text="📈TRADE📈", callback_data="cat_trade"),
    types.InlineKeyboardButton(text="🖼NFT🖼", callback_data="cat_nft"),
    types.InlineKeyboardButton(text="💱EXCHANGE💱", callback_data="cat_exchange"),
    types.InlineKeyboardButton(text="🃏CASINO🃏", callback_data="cat_casino"),
    types.InlineKeyboardButton(text="💋ESCORT💋", callback_data="cat_eskort"),
    types.InlineKeyboardButton(text="🎥ANTIK🎥", callback_data="cat_antik"),
    types.InlineKeyboardButton(text="💊N@RKO💊", callback_data="cat_narko"),
    types.InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu"),
)

back_to_files = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text="Назад", callback_data="choose")
)

channel_url = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Перейти в канал", url=cfg.channel_url),
    types.InlineKeyboardButton("Я подписался", callback_data="check_member"),
)


def get_category_page(category, page, flag, key):
    item_choose = types.InlineKeyboardMarkup(row_width=1)
    if category == "circles":
        choosed_category = circles
    elif category == "pictures":
        choosed_category = pictures
    else:
        choosed_category = voices[category] if flag == 0 else flag
    category_lenght = math.ceil(len(choosed_category) / 8)
    type_page = "normal" if flag == 0 else key
    if 8 * page <= len(choosed_category) and 8 * page >= 0:
        for item in range(
            8 * page,
            8 * (page + 1)
            if 8 * (page + 1) < len(choosed_category)
            else len(choosed_category),
        ):
            item_choose.insert(
                types.InlineKeyboardButton(
                    text=choosed_category[item][0],
                    callback_data=f"{category}/{choosed_category[item][1]}",
                )
            )
        button_back = types.InlineKeyboardButton(
            text="Назад⬅️", callback_data=f"page {page - 1} {category} {type_page}"
        )
        button_forward = types.InlineKeyboardButton(
            text="Вперед➡️", callback_data=f"page {page + 1} {category} {type_page}"
        )
        button_middle = types.InlineKeyboardButton(
            text=f"{page + 1}/{category_lenght}", callback_data="aboba"
        )
        item_choose.row(button_back, button_middle, button_forward)
        if category != "circles" and category != "pictures":
            item_choose.row(
                types.InlineKeyboardButton(
                    text="Поиск", callback_data=f"search_{category}"
                )
            )
            item_choose.row(
                types.InlineKeyboardButton(
                    text="Назад к выбору категории", callback_data="back"
                )
            )
        else:
            item_choose.row(
                types.InlineKeyboardButton(
                    text="Назад в меню", callback_data="back_to_menu"
                )
            )
        return item_choose
    elif 8 * page >= len(choosed_category):
        if flag == 0:
            return get_category_page(category, 0, flag, key)
        return get_category_page(category, 0, flag, key)
    elif page < 0:
        if flag == 0:
            return get_category_page(
                category, math.floor(len(choosed_category) / 8), flag, key
            )
        return get_category_page(
            category, math.floor(len(choosed_category) / 8), flag, key
        )


def get_search_markup(category: str, key: str, page):
    desired_files = voices[category]
    res_mass = []
    for file in desired_files:
        if key.lower() in file[0].lower():
            res_mass.append(file)
    if len(res_mass) == 0:
        return False
    return get_category_page(category, page, res_mass, key)
