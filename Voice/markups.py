from aiogram import types
from filesMass import files_name
import math

categor_choose = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton(text="🌐Universal🌐", callback_data="cat_universal"),
    types.InlineKeyboardButton(text="📈Trade📈", callback_data="cat_trade"),
    types.InlineKeyboardButton(text="🖼NFT🖼", callback_data="cat_nft"),
    types.InlineKeyboardButton(text="💱Exchange💱", callback_data="cat_exchange"),
    types.InlineKeyboardButton(text="🃏Casino🃏", callback_data="cat_casino"),
    types.InlineKeyboardButton(text="💋Escort💋", callback_data="cat_escort"),
    types.InlineKeyboardButton(text="🎥Antik🎥", callback_data="cat_antik"),
    types.InlineKeyboardButton(text="💊N@rko💊", callback_data="cat_narko"),
)


def get_category_page(category, page):
    item_choose = types.InlineKeyboardMarkup(row_width=1)
    choosed_category = files_name[category]
    category_lenght = math.ceil(len(choosed_category) / 8)
    if 8 * page <= len(choosed_category) and 8 * page >= 0:
        print(page)
        for item in range(
            8 * page,
            8 * (page + 1)
            if 8 * (page + 1) < len(choosed_category)
            else len(choosed_category),
        ):
            item_choose.insert(
                types.InlineKeyboardButton(
                    text=choosed_category[item][0],
                    callback_data=f"{category} {choosed_category[item][1]}",
                )
            )
        button_back = types.InlineKeyboardButton(
            text="Назад⬅️", callback_data=f"page_ {page - 1} {category}"
        )
        button_forward = types.InlineKeyboardButton(
            text="Вперед➡️", callback_data=f"page_ {page + 1} {category}"
        )
        button_middle = types.InlineKeyboardButton(
            text=f"{page + 1}/{category_lenght}", callback_data="aboba"
        )
        item_choose.row(button_back, button_middle, button_forward)
        if not page == 1:
            item_choose.add()
        if not page * 8 >= len(choosed_category):
            item_choose.add()
        return item_choose
    else:
        return "huy"
