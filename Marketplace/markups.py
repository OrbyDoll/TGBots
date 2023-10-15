import config as cfg
from aiogram import types
from cryptography.fernet import Fernet

coder = Fernet(cfg.key)


def code_link(text):
    return coder.encrypt(text).decode()


prada_service_list = {
    "DESIGN": {
        "text": "статичная аватарка: 8$ ~ 750 ₽ | 300 ₴ | 3500 ₸ \n\nанимированная аватарка: 12$ ~ 1100 ₽ | 450 ₴ | 5500 ₸ \n\n__________________________\n\n\nстатичный баннер: 10$ ~ 1000 ₽ | 400 ₴ | 4500 ₸ \n\nанимированный баннер: 15$ ~ 1500 ₽ | 500 ₴ | 7000 ₸ \n\n__________________________\n\n\nпревью: 10$ ~ 1000 ₽ | 400 ₴ | 4500 ₸\n\nшапка: 10$ ~ 1000 ₽ | 400 ₴ | 4500 ₸\n\n__________________________\n\n\nстатичный оверлей: 8$ ~ 700 ₽ | 300 ₴ | 3500 ₸ \n\nанимированный оверлей: 15$ ~ 1500 ₽ | 550 ₴ | 7000 ₸ \n\n__________________________\n\n\nстатичные стикеры: 2$ (штука) ~ 200 ₽ | 80 ₴ | 900 ₸ (заказ от 5 штук) \n\nанимированные стикеры: 4$ (штука) ~ 400 ₽ | 150 ₴ | 1800 ₸ (заказ от 5 штук) \n\n__________________________\n\n\nоформление проекта: договорная, в зависимости от объема работы",
        "contacts": "заказать - @pradadesign\n\nоплатить - @pradaoplata",
    },
    "MATERIALS": {
        "text": "подписка на 1 день - 12$ | 1000 ₽ | 450 ₴ | 5500 ₸\n\nподписка на 2 дня - 20$ | 1600 ₽ | 750 ₴ | 9000 ₸\n\nподписка на 3 дня -  26$ | 2100 ₽ | 950 ₴ | 11500 ₸",
        "contacts": "заказать - @pradamaterialsmng\n\nоплатить - @pradaoplata\n\nполучить гс - @pradamateriaIs",
    },
    "DOX": {
        "text": "DOX = oт 30$ ~ 2700 ₽ | 1100 ₴ | 13300 ₸\n\nSW@T (RU/URK/KZ/EU) = oт 40$ ~ 3600 ₽ | 1400 ₴ | 18000 ₸\n\nDELIVERY = om 30$ ~ 2700 ₽ | 1100 ₴ | 13000 ₸\n\nСНОВ ЧАТОВ/КАНАЛОВ = oт 25$ ~ 2300 ₽ | 900 ₴ | 11000 ₸\n\nЗАЩИТА (DEF) - oт 100$ ~ 9000 ₽ | 3700 ₴ | 45000 ₸",
        "contacts": "заказать - @pradadoxing\n\nоплатить - @pradaoplata",
    },
    "SMM": {
        "text": "ИНВАЙТИНГ: \n\nминимальный заказ = 1000 человек.\n\n3р / человек - до 3000 человек.\n2.5р / человек - до 5000 человек.\n2р / человек - от 5000 человек.\n\n\nРАССЫЛКА ПО ЛС:\n\nминимальный заказ = 1000 человек. \n\n3р / смс - до 1000-3000 человек 2.5р / человек - до 5000 человек 2р / человек - от 5000 человек\n\n\nПАРСИНГ ЧАТОВ: \n\nминимальный заказ = 500 человек.\n\n2.5р - человек.\n\n\nПРОЛИВ ВИДЕО ЛЮБОГО ВИДА:\n\nминимальный заказ - 5 видео.\n\nшортс / рилс / тик ток - 5$ ~ 400 ₽ | 200 ₴ | 2500 ₸ за видео.\nлюбая тематика, цена зависит от сложности видео. проливаем либо на личных прогретых аккаунтах.\n\n\nТАРГЕТ: \n\n\nвконтакте -  50$ ~ 5000 ₽ | 2000 ₴ | 23000 ₸. \nв таргет входит настройка рекламного кабинета, настройка рекламного поста, масса советов по ведению.\n\n\nПРОЕКТ ПО ИНДИВИДУАЛЬНОМУ ЗАКАЗУ: \n\nлюбой источник трафика - от 50$ ~ 5000 ₽ | 2000 ₴ | 23000 ₸.\nкак только вы определились с нужным источником трафика и написали нам - мы создаем необходимый вам источник трафика под ваши нужды и полностью под вашим наблюдением, также помогает с базовой обработкой вашего источника трафика.",
        "contacts": "заказать - @pradasmm\n\nоплатить - @pradaoplata",
    },
}

admin_panel = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Заявки на одобрение", callback_data="check_products"),
    types.InlineKeyboardButton("Удалить товар", callback_data="admin_delete"),
    types.InlineKeyboardButton("Бан-система🔕", callback_data="bor"),
    types.InlineKeyboardButton("Рассылка💬", callback_data="newsletter"),
    types.InlineKeyboardButton("Изменение баланса📝", callback_data="edit_balance"),
    types.InlineKeyboardButton("Статистика📊", callback_data="stats"),
    types.InlineKeyboardButton("⬅️Назад", callback_data="hide"),
)

service_markup = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(text="DESIGN", callback_data="service_DESIGN"),
    types.InlineKeyboardButton(text="MATERIALS", callback_data="service_MATERIALS"),
    types.InlineKeyboardButton(text="DOX", callback_data="service_DOX"),
    types.InlineKeyboardButton(text="SMM", callback_data="service_SMM"),
    types.InlineKeyboardButton(text="⬅️Назад", callback_data="category_back"),
)

bor = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Забанить🔕", callback_data="ban"),
    types.InlineKeyboardButton("Разбанить🔔", callback_data="unban"),
)

menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
    types.KeyboardButton(text="Создать товар📝"),
    types.KeyboardButton(text="Выбрать товар📋"),
    types.KeyboardButton("О нас🌟"),
    types.KeyboardButton(text="Мои товары🛍"),
)

channel_url = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Перейти в канал", url=cfg.channel_url),
    types.InlineKeyboardButton("Я подписался", callback_data="check_member_channel"),
)

garant_check = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(
        text="Перейти в гарант бота💎",
        url="https://t.me/pradagarant_bot",
    ),
    types.InlineKeyboardButton(text="Я нажал", callback_data="check_member_garant"),
)

hide = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text="Скрыть", callback_data="hide")
)


categor = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
categor.row(types.KeyboardButton(text="PRADA🏆"))
categor.add(
    types.KeyboardButton(text="Теги📧"),
    types.KeyboardButton(text="Деф🛡"),
    types.KeyboardButton(text="Услуги🤝"),
    types.KeyboardButton(text="Материалы🗃"),
    types.KeyboardButton(text="Софт🖥"),
    types.KeyboardButton(text="Боты🤖"),
    types.KeyboardButton(text="Сайты🌐"),
    types.KeyboardButton(text="Мануалы📓"),
    types.KeyboardButton(text="Документы📄"),
    types.KeyboardButton(text="Другое⚙"),
    types.KeyboardButton(text="⬅️Назад"),
)

o_nas = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton(
        text="🧑‍💻КРУГЛОСУТОЧНАЯ ПОДДЕРЖКА", url="https://t.me/pradamarketplace_sup"
    ),
    types.InlineKeyboardButton(
        text="📰ИНФОРМАЦИЯ ОБ ОБНОВЛЕНИЯХ БОТОВ",
        url="https://t.me/+gbEsSZAUQTU4OWZi",
    ),
    types.InlineKeyboardButton(
        text="🌎ВСЕ НАШИ ПРОЕКТЫ", url="https://t.me/PRADAEMPlRE"
    ),
    types.InlineKeyboardButton(text="Скрыть", callback_data="hide_2"),
)

back_from_name = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Назад", callback_data="back_name")
)

back_from_price = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Назад", callback_data="back_price")
)

categor_without_prada = types.ReplyKeyboardMarkup(
    row_width=2, one_time_keyboard=True
).add(
    types.KeyboardButton(text="Мануалы📓"),
    types.KeyboardButton(text="Теги📧"),
    types.KeyboardButton(text="Деф🛡"),
    types.KeyboardButton(text="Услуги🤝"),
    types.KeyboardButton(text="Материалы🗃"),
    types.KeyboardButton(text="Софт🖥"),
    types.KeyboardButton(text="Боты🤖"),
    types.KeyboardButton(text="Сайты🌐"),
    types.KeyboardButton(text="Документы📄"),
    types.KeyboardButton(text="Другое⚙"),
    types.KeyboardButton(text="⬅️Назад"),
)

buy_choose = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Да✔️", callback_data="accept_buy"),
    types.InlineKeyboardButton("Нет❌", callback_data="deny_buy"),
)

sort_choose = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton(text="Сначала дорогие📈", callback_data="sort_increase"),
    types.InlineKeyboardButton(text="Сначала дешевые📉", callback_data="sort_decrease"),
    types.InlineKeyboardButton(text="Сначала новые⏱", callback_data="sort_no"),
)

cancel_admin_del = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Отмена", callback_data="cancel_admin_del")
)


def get_offer_buy_button(offer_str):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text="Купить🛍", callback_data=f"buy_{offer_str}")
    )


def get_offer_del_button(offer_str, type):
    offer_del = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text="Удалить🗑", callback_data=f"del_{offer_str}"),
    )
    if type == 1:
        offer_del.add(
            types.InlineKeyboardButton(
                text="Изменить цену⚙️", callback_data=f"cp_{offer_str}"
            )
        )
    return offer_del


def get_admin_solution_markup(owner, product_name):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            "Одобрить", callback_data=f"ap_{owner}_{product_name}"
        ),
        types.InlineKeyboardButton(
            "Отклонить", callback_data=f"dp_{owner}_{product_name}"
        ),
    )
