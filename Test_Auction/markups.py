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
        if auct[8] == category and not auct[6] == "check":
            isThereAuctions = True
            res_markup.insert(
                types.InlineKeyboardButton(
                    text=f"{auct[5]} | {auct[4]}", callback_data=f"detail {auct[3]}"
                )
            )
    res_markup.add(types.InlineKeyboardButton("Скрыть", callback_data="hide"))
    if not isThereAuctions:
        return None
    return res_markup


menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
    types.KeyboardButton(text="Список аукционов ⚖️"),
    types.KeyboardButton(text="Создать аукцион 💎"),
    types.KeyboardButton(text="О нас🌟"),
    types.KeyboardButton(text="Перейти к своему аукциону 🔓"),
)


admin_panel = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Заявки на одобрение", callback_data="check_auctions"),
    types.InlineKeyboardButton("Удалить аукцион", callback_data="admin_delete"),
    types.InlineKeyboardButton("Бан-система🔕", callback_data="bor"),
    types.InlineKeyboardButton("Рассылка💬", callback_data="newsletter"),
    types.InlineKeyboardButton("Изменение баланса📝", callback_data="edit_balance"),
    types.InlineKeyboardButton("Статистика📊", callback_data="stats"),
    types.InlineKeyboardButton("⬅️Назад", callback_data="hide"),
)


garant_check = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(
        text="Перейти в гарант бота💎",
        url="https://t.me/pradagarant_bot",
    ),
    types.InlineKeyboardButton(text="Я нажал", callback_data="check_member_garant"),
)

bor = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Забанить🔕", callback_data="ban"),
    types.InlineKeyboardButton("Разбанить🔔", callback_data="unban"),
)

o_nas = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton(
        text="🧑‍💻КРУГЛОСУТОЧНАЯ ПОДДЕРЖКА", url="https://t.me/pradaauction_sup"
    ),
    types.InlineKeyboardButton(
        text="📰ИНФОРМАЦИЯ ОБ ОБНОВЛЕНИЯХ БОТОВ",
        url="https://t.me/+gbEsSZAUQTU4OWZi",
    ),
    types.InlineKeyboardButton(
        text="🌎ВСЕ НАШИ ПРОЕКТЫ", url="https://t.me/PRADAEMPlRE"
    ),
    types.InlineKeyboardButton(text="Скрыть", callback_data="close"),
)

hide = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text="Скрыть", callback_data="hide")
)


channel_url = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Перейти в канал", url=cfg.channel_url),
    types.InlineKeyboardButton("Я подписался", callback_data="check_member"),
)

sort_choose = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(
    types.KeyboardButton(text="Сначала дорогие📈"),
    types.KeyboardButton(text="Сначала дешевые📉"),
    types.KeyboardButton(text="Назад"),
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
    types.KeyboardButton(text="Другое⚙️"),
    types.KeyboardButton(text="Назад"),
)
owner_actions = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(
        text="Удалить аукцион 🗑", callback_data="remove_auction"
    ),
    types.InlineKeyboardButton(
        text="Изменить начальную ставку 💰", callback_data="start_cost"
    ),
    types.InlineKeyboardButton(
        text="Настроить автостарт⚙️", callback_data="auto_start"
    ),
    types.InlineKeyboardButton(text="Начать аукцион🛎", callback_data="start_auction"),
)

cancel_admin_del = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Отмена", callback_data="cancel_admin_del")
)

member_actions = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton(text="Покинуть аукцион❌", callback_data="leave_auction"),
    types.InlineKeyboardButton(text="Предложить ставку🔊", callback_data="offer_rate"),
)

close_info_message = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text="Скрыть", callback_data="close")
)

get_auction_info = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton(text="Информация об аукционе📜", callback_data="info_auction")
)

del_auction = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text="⬅️Назад", callback_data="move"),
    # types.InlineKeyboardButton(
    #     text="Перейти в гарант бота💎", url="https://t.me/pradagarant_bot"
    # ),
)


def accept_offer(offer_id):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            text="Приянть ставку✅", callback_data=f"accept_offer{offer_id}"
        )
    )


def get_auction_offer(author_id):
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(
            text="Вступить в аукцион✅", callback_data=f"enter_auction{author_id}"
        ),
        types.InlineKeyboardButton(text="Назад", callback_data="back_offer_list"),
    )


def get_admin_solution_markup(owner):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("Одобрить", callback_data=f"acceptproduct_{owner}"),
        types.InlineKeyboardButton("Отклонить", callback_data=f"denyproduct_{owner}"),
    )


# offer Продавец Покупатель Сумма
