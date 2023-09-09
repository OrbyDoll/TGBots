import config as cfg
from aiogram import types
from cryptography.fernet import Fernet

coder = Fernet(cfg.key)
def code_link(text):
    return coder.encrypt(text).decode()

choose_action = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton(text='Создать предложение', callback_data='create_offer'),
    types.InlineKeyboardButton(text='Выбрать товар', callback_data='choose_product'),
    types.InlineKeyboardButton(text='Мои товары', callback_data='my_products')
)

categor = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True).add(
    types.KeyboardButton(text='Мануалы'),
    types.KeyboardButton(text='Теги'),
    types.KeyboardButton(text='Деф'),
    types.KeyboardButton(text='Услуги'),
    types.KeyboardButton(text='Материалы'),
    types.KeyboardButton(text='Софт'),
    types.KeyboardButton(text='Боты'),
    types.KeyboardButton(text='Сайты'),
    types.KeyboardButton(text='PRADA'),
    types.KeyboardButton(text='Другое')
)

buy_choose = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Да", callback_data='accept'),
    types.InlineKeyboardButton("Нет", callback_data='deny')
)

def get_offer_buy_button(offer_str):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Купить', callback_data=f'buy_{offer_str}')
    )
def get_offer_del_button(offer_str):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='Удалить', callback_data=f'del_{offer_str}')
    )

# category_selection_menu = types.InlineKeyboardMarkup(row_width=2)
# for categories in cfg.product_list:
#     category_selection_button = types.InlineKeyboardButton(
#         text=categories["name"], callback_data=categories["name"]
#     )
#     category_selection_menu.insert(category_selection_button)


# def getProductsMarkup(category):
#     if category == "Back":
#         return category_selection_menu
#     products_selection_markup = types.InlineKeyboardMarkup(row_width=1)
#     for i in cfg.product_list:
#         if i["name"] == category:
#             for j in i["items"]:
#                 products_selection_button = types.InlineKeyboardButton(
#                     text=j, callback_data=j
#                 )
#                 products_selection_markup.insert(products_selection_button)
#     products_selection_markup.insert(
#         types.InlineKeyboardButton(text="Back", callback_data="Back")
#     )
#     return products_selection_markup
#     products_selection_markup.insert(
#         types.InlineKeyboardButton(text="Nothing", callback_data="adad")
#     )
#     return products_selection_markup
