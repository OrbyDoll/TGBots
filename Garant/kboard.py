from telebot import types
import config

# Меню
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    types.KeyboardButton("💵 Прошедшие сделки"),
    types.KeyboardButton("👤 Профиль"),
    types.KeyboardButton("⭐️ О нас"),
    types.KeyboardButton('🔐Сделка по коду'),
    types.KeyboardButton("🔒 Провести сделку"),
)

o_nas = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(
        text="🧑‍💻КРУГЛОСУТОЧНАЯ ПОДДЕРЖКА", url="https://t.me/pradagarant_sup"
    ),
    types.InlineKeyboardButton(
        text="📰ИНФОРМАЦИЯ ОБ ОБНОВЛЕНИЯХ БОТОВ",
        url="https://t.me/+gbEsSZAUQTU4OWZi",
    ),
    types.InlineKeyboardButton(
        text="🌎ВСЕ НАШИ ПРОЕКТЫ", url="https://t.me/PRADAEMPlRE"
    ),
    types.InlineKeyboardButton(text="Скрыть", callback_data="hide"),
)

channel_url = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton("Перейти в канал", url=config.channel_url),
    types.InlineKeyboardButton("Я подписался", callback_data="check_member"),
)
profile = types.InlineKeyboardMarkup(row_width=2)
profile.add(
    types.InlineKeyboardButton("Вывод средств💸", callback_data="output"),
    types.InlineKeyboardButton("Пополнить счёт💠", callback_data="input"),
    types.InlineKeyboardButton("Обновить логин🌀", callback_data="up_login"),
    types.InlineKeyboardButton("Отзывы", callback_data="my_reviews"),
    types.InlineKeyboardButton("Скрыть", callback_data="hide_profile"),
)

go_back = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back")
)
cors = types.InlineKeyboardMarkup()
cors.add(
    types.InlineKeyboardButton("💎 Продавец", callback_data="seller"),
    types.InlineKeyboardButton("💰 Покупатель", callback_data="customer"),
)
admin = types.InlineKeyboardMarkup(row_width=2)
admin.add(
    types.InlineKeyboardButton("Бан-система🔕", callback_data="bor"),
    types.InlineKeyboardButton("Рассылка💬", callback_data="message"),
    types.InlineKeyboardButton("Изменение баланса📝", callback_data="edit_balance"),
    types.InlineKeyboardButton("Статистика📊", callback_data="statistics"),
    types.InlineKeyboardButton("Решение спора🔎", callback_data="dispute_admin"),
    types.InlineKeyboardButton("⬅️Назад", callback_data="menu"),
)
bor = types.InlineKeyboardMarkup(row_width=2).add(
    types.InlineKeyboardButton("Забанить🔕", callback_data="ban"),
    types.InlineKeyboardButton("Разбанить🔔", callback_data="unban"),
)

canel = types.InlineKeyboardMarkup()
canel.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="menu"))

choise = types.InlineKeyboardMarkup()
choise.add(
    types.InlineKeyboardButton("✅ Принять", callback_data="accept_customer"),
    types.InlineKeyboardButton("❌ Отклонить", callback_data="delete_customer"),
)

choise_seller = types.InlineKeyboardMarkup()
choise_seller.add(
    types.InlineKeyboardButton("✅ Принять", callback_data="accept_seller"),
    types.InlineKeyboardButton("❌ Отклонить", callback_data="delete_seller"),
)

sentence = types.InlineKeyboardMarkup(row_width=2)
sentence.add(
    types.InlineKeyboardButton(
        "📝 Предложить сделку", callback_data="proposal_customer"
    ),
    types.InlineKeyboardButton("📄 Отзывы", callback_data="reviews"),
    types.InlineKeyboardButton("⬅️ Назад", callback_data="delete_customer"),
)

sentence_seller = types.InlineKeyboardMarkup(row_width=2)
sentence_seller.add(
    types.InlineKeyboardButton("📝 Предложить сделку", callback_data="proposal_seller"),
    types.InlineKeyboardButton("📄 Отзывы", callback_data="reviews"),
    types.InlineKeyboardButton("⬅️ Назад", callback_data="delete_seller"),
)

canel_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
canel_button.add(types.KeyboardButton("⬅️ Назад"))

choise_offer = types.InlineKeyboardMarkup()
choise_offer.add(
    types.InlineKeyboardButton("💎 Покупатель", callback_data="customer_offer"),
    types.InlineKeyboardButton("💰 Продавец", callback_data="seller_offer"),
    types.InlineKeyboardButton("⬅️ Назад", callback_data="hide_profile")
)

seller_panel = types.InlineKeyboardMarkup(row_width=2)
seller_panel.add(
    types.InlineKeyboardButton("📢Открыть спор", callback_data="open_dispute_seller"),
    types.InlineKeyboardButton("❌Отменить сделку", callback_data="canel_open_seller"),
    types.InlineKeyboardButton("💸Указать стоимость", callback_data="price"),
)

customer_panel = types.InlineKeyboardMarkup(row_width=2)
customer_panel.add(
    types.InlineKeyboardButton("💸Оплатить товар", callback_data="input_panel"),
    types.InlineKeyboardButton("❌Отменить сделку", callback_data="canel_open"),
    types.InlineKeyboardButton("📢Открыть спор", callback_data="open_dispute"),
    types.InlineKeyboardButton("✅Подтвердить получение", callback_data="ok"),
)

choise_canel = types.InlineKeyboardMarkup()
choise_canel.add(
    types.InlineKeyboardButton("✅ Да", callback_data="Yes_canel"),
    types.InlineKeyboardButton("❌ Нет", callback_data="No_canel"),
)

choise_canel_seller = types.InlineKeyboardMarkup()
choise_canel_seller.add(
    types.InlineKeyboardButton("✅ Да", callback_data="Yes_canel_seller1"),
    types.InlineKeyboardButton("❌ Нет", callback_data="No_canel_seller1"),
)

choise_canel_seller2 = types.InlineKeyboardMarkup()
choise_canel_seller2.add(
    types.InlineKeyboardButton("✅ Согласиться", callback_data="Yes_canel_seller"),
    types.InlineKeyboardButton("❌ Отказаться", callback_data="No_canel_seller"),
)

choise_canel_customer = types.InlineKeyboardMarkup()
choise_canel_customer.add(
    types.InlineKeyboardButton("✅ Согласиться", callback_data="Yes_canel_customer"),
    types.InlineKeyboardButton("❌ Отказаться", callback_data="No_canel_customer"),
)

ok_choise = types.InlineKeyboardMarkup()
ok_choise.add(
    types.InlineKeyboardButton("✅ Согласиться", callback_data="ok_ok"),
    types.InlineKeyboardButton("❌ Отказаться", callback_data="ok_canel"),
)

choise_admin = types.InlineKeyboardMarkup(row_width=2)
choise_admin.add(
    types.InlineKeyboardButton("💎 Покупатель", callback_data="customer_true"),
    types.InlineKeyboardButton("💰 Продавец", callback_data="seller_true"),
    types.InlineKeyboardButton("❌ Никто", callback_data="no_true"),
)

canel_offer_customer = types.InlineKeyboardMarkup()
canel_offer_customer.add(
    types.InlineKeyboardButton("💥 Отменить сделку", callback_data="canel_open_offer")
)

canel_offer_seller = types.InlineKeyboardMarkup()
canel_offer_seller.add(
    types.InlineKeyboardButton(
        "💥 Отменить сделку", callback_data="canel_open_offer_seller"
    )
)

add_review = types.InlineKeyboardMarkup(row_width=2)
add_review.add(
    types.InlineKeyboardButton("✨ Да", callback_data="add_review"),
    types.InlineKeyboardButton("💤 Нет", callback_data="no_review"),
)

cancel_wait = types.InlineKeyboardMarkup()
cancel_wait.add(
    types.InlineKeyboardButton("💥 Отменить ожидание", callback_data="cancel_wait")
)
