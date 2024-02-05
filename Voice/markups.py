from aiogram import types
import config as cfg
from filesMass import voices, circles, pictures
import math

start_menu = types.ReplyKeyboardMarkup(
    row_width=3, resize_keyboard=True, one_time_keyboard=True
).add(
    types.KeyboardButton("Голосовые🎙"),
    types.KeyboardButton("Кружки🔘"),
    types.KeyboardButton("Фото🖼"),
    types.KeyboardButton("Кружок из видео🔧"),
)

menu_hide = types.ReplyKeyboardRemove()
msg_desc_hide = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Скрыть", callback_data="hide_voice")
)


def girl_photos_actions(message_num):
    return types.InlineKeyboardMarkup().add(
        # types.InlineKeyboardButton(
        #     "Назад к выбору девушки", callback_data="back_to_girl_choose"
        # ),
        types.InlineKeyboardButton(
            "Скрыть", callback_data=f"hide_photos_{message_num}"
        ),
    )


back_to_menu = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text="⬅️Назад в меню", callback_data="back_to_menu"),
)

categor_choose = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton(text="🌐UNIVERSAL🌐", callback_data="cat_universal"),
    types.InlineKeyboardButton(text="📈TRADE📈", callback_data="cat_trade"),
    types.InlineKeyboardButton(text="🖼NFT🖼", callback_data="cat_nft"),
    types.InlineKeyboardButton(text="💱EXCHANGE💱", callback_data="cat_exchange"),
    types.InlineKeyboardButton(text="🃏CASINO🃏", callback_data="cat_casino"),
    types.InlineKeyboardButton(text="💋ESCORT💋", callback_data="cat_eskort"),
    types.InlineKeyboardButton(text="🎥ANTIK🎥", callback_data="cat_antik"),
    types.InlineKeyboardButton(text="💊N@RKO💊", callback_data="cat_narko"),
    types.InlineKeyboardButton(text="⬅️Назад в меню", callback_data="back_to_menu"),
)

back_to_files = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text="⬅️Назад", callback_data="choose")
)

channel_url = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Перейти в канал", url=cfg.channel_url),
    types.InlineKeyboardButton("Я подписался", callback_data="check_member"),
)


def get_category_page(category, page, flag, key):
    item_choose = types.InlineKeyboardMarkup(row_width=1)
    stickers = ["👩🏻",'👩🏼','👩🏽']
    # if category == "circles":
    #     choosed_category = circles
    if category == "pictures":
        choosed_category = pictures
    else:
        if category == "circles" and flag == 0:
            choosed_category = circles
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
            if category == "pictures":
                text = f"Девушка {item + 1} {stickers[item % 3]}"
                cb_data = f"{category}/{item+1}"
            else:
                text = choosed_category[item][0]
                cb_data = f"{category}/{choosed_category[item][1]}"
            item_choose.insert(
                types.InlineKeyboardButton(
                    text=text,
                    callback_data=cb_data,
                )
            )
        button_back = types.InlineKeyboardButton(
            text="⬅️", callback_data=f"page {page - 1} {category} {type_page}"
        )
        button_forward = types.InlineKeyboardButton(
            text="➡️", callback_data=f"page {page + 1} {category} {type_page}"
        )
        button_middle = types.InlineKeyboardButton(
            text=f"{page + 1}/{category_lenght}", callback_data="aboba"
        )
        item_choose.row(button_back, button_middle, button_forward)
        if category != "pictures":
            item_choose.row(
                types.InlineKeyboardButton(
                    text="Поиск🔎", callback_data=f"search_{category}"
                )
            )
        if category != "circles" and category != "pictures":
            item_choose.row(
                types.InlineKeyboardButton(
                    text="⬅️Назад к выбору категории", callback_data="back"
                )
            )
        else:
            item_choose.row(
                types.InlineKeyboardButton(
                    text="⬅️Назад в меню", callback_data="back_to_menu"
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
    desired_files = voices[category] if category != "circles" else circles
    res_mass = []
    for file in desired_files:
        if key.lower() in file[0].lower():
            res_mass.append(file)
    if len(res_mass) == 0:
        return False
    return get_category_page(category, page, res_mass, key)
