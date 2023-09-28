from aiogram import types
import config as cfg
from cryptography.fernet import Fernet

coder = Fernet(cfg.key)


def code_link(text):
    return coder.encrypt(text).decode()


def get_auctions_buttons(auct_mass, category):
    res_markup = types.InlineKeyboardMarkup(row_width=3)
    isThereAuctions = False
    for auct in auct_mass:
        if auct[8] == category:
            isThereAuctions = True
            res_markup.insert(
                types.InlineKeyboardButton(
                    text=f"{auct[5]} | {auct[4]}", callback_data=f"detail {auct[3]}"
                )
            )
    if not isThereAuctions:
        return None
    return res_markup


menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    types.KeyboardButton(text="Список аукционов ⚖️"),
    types.KeyboardButton(text="Создать аукцион 💎"),
    types.KeyboardButton(text="Перейти к своему аукциону 🔓"),
)

action_choose = types.InlineKeyboardMarkup(row_width=2)
action_choose.add(
    types.InlineKeyboardButton(
        text="Список аукционов ⚖️", callback_data="get_auctions"
    ),
    types.InlineKeyboardButton(
        text="Создать аукцион 💎", callback_data="create_auction"
    ),
    types.InlineKeyboardButton(
        text="Перейти к своему аукциону 🔓", callback_data="my_auction"
    ),
)

sort_choose = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton(text="Сначала дорогие", callback_data="sort_increase"),
    types.InlineKeyboardButton(text="Сначала дешевые", callback_data="sort_decrease"),
    types.InlineKeyboardButton(text="Сначала новые", callback_data="sort_no"),
)
categor = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True).add(
    types.KeyboardButton(text="Мануалы📓"),
    types.KeyboardButton(text="Теги📧"),
    types.KeyboardButton(text="Деф🛡"),
    types.KeyboardButton(text="Услуги🤝"),
    types.KeyboardButton(text="Материалы🗃"),
    types.KeyboardButton(text="Софт🖥"),
    types.KeyboardButton(text="Боты🤖"),
    types.KeyboardButton(text="Сайты🌐"),
    types.KeyboardButton(text="PRADA🏆"),
    types.KeyboardButton(text="Другое⚙️"),
    types.KeyboardButton(text="Назад"),
)
owner_actions = types.InlineKeyboardMarkup(row_width=1)
owner_actions.add(
    types.InlineKeyboardButton(
        text="Удалить аукцион 🗑", callback_data="remove_auction"
    ),
    types.InlineKeyboardButton(
        text="Изменить начальную ставку 💰", callback_data="start_cost"
    ),
    types.InlineKeyboardButton(text="Начать аукцион", callback_data="start_auction"),
)

member_actions = types.InlineKeyboardMarkup(row_width=2)
member_actions.add(
    types.InlineKeyboardButton(text="Покинуть аукцион", callback_data="leave_auction"),
    types.InlineKeyboardButton(text="Предложить ставку", callback_data="offer_rate"),
)


def accept_offer(offer_id):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            text="Приянть ставку", callback_data=f"accept_offer{offer_id}"
        )
    )


del_auction = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(
        text="Перейти в гарант бота ➡️", url="https://t.me/pradagarantbot"
    ),
)


def get_auction_offer(author_id):
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(
            text="Вступить в аукцион", callback_data=f"enter_auction{author_id}"
        ),
        types.InlineKeyboardButton(text="Назад", callback_data="back_offer_list"),
    )


# offer Продавец Покупатель Сумма
