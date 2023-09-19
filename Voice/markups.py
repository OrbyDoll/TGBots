from aiogram import types
from filesMass import files_name


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
    item_choose = types.InlineKeyboardMarkup(row_width=2)
    choosed_category = files_name[category]
    for item in range(
        8 * (page - 1),
        8 * page if 8 * page < len(choosed_category) else len(choosed_category),
    ):
        item_choose.insert(
            types.InlineKeyboardButton(
                text=choosed_category[item][0], callback_data=choosed_category[item][1]
            )
        )
    if not page == 1:
        item_choose.add(
            types.InlineKeyboardButton(
                text="Назад⬅️", callback_data=f"page_ {page - 1} {category}"
            )
        )
    if not page * 8 >= len(choosed_category):
        item_choose.add(
            types.InlineKeyboardButton(
                text="Вперед➡️", callback_data=f"page_ {page + 1} {category}"
            )
        )
    return item_choose
