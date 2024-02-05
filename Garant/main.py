from telebot import types
import telebot
from config import (
    TOKEN,
    admin,
    chat_bota,
    nicknameadm,
    procent,
    admin2,
    chat_bota,
    crypto_token,
    crypto_test_token,
    required_chat_id,
    admin3,
)

import datetime
import schedule
from var import error, canel_operation, disable_keyboard, enable_keyboard
import math
import kboard as kb
import functions as func
import requests
import json
import sqlite3
import time

api_link = "https://pay.crypt.bot/api/"
header = {"Crypto-Pay-API-Token": crypto_token}

coin_dict = {"coin": "None", "amount": 0}
balance_dict = {}
bot = telebot.TeleBot(TOKEN)
bot_username = bot.get_me().username


def test():
    print("test")


schedule.every().second.do(test)


def checkMember(
    userid,
):
    chat_member = bot.get_chat_member(required_chat_id, userid)
    if chat_member.status == "left":
        return False
    return True


def notice(chatid, message_id):
    bot.delete_message(chatid, message_id)
    prev_notice = func.get_notice(chatid)[0]
    if prev_notice != 4:
        func.increase_notice(chatid)
        bot.send_message(
            chatid,
            f"Вы получили {prev_notice + 1} из 5 предупреждений! Если у вас будет 5 предупреждений вы будете заблокированы",
            reply_markup=kb.canel,
        )
    else:
        func.ban(chatid)
        func.reset_notice(chatid)
        bot.send_message(chatid, "Вы получили 5 предупреждение и были заблокированы.")
    bot.send_message(chatid, "Включение меню", reply_markup=kb.menu)
    func.delete_customer(chatid)


# except Exception as e:
#     print(e)
#     bot.send_message(chatid, "Что-то пошло не так")


def get_offer_from_string(seller_id, customer_id, offer_type, offer_link_split):
    seller_nick = func.get_nick_from_id(seller_id)
    customer_nick = func.get_nick_from_id(customer_id)
    offer_price = offer_link_split[3]
    check_user = func.search(customer_nick)  # Требует ник
    if check_user == None:
        bot.send_message(
            seller_id,
            text="⛔️ Пользователь не найден, пожалуйста, убедитесь что он уже взаимодействовал с ботом!",
        )
    elif seller_id == customer_id:
        bot.send_message(
            seller_id,
            text="❌Нельзя отправить сделку самому себе",
        )
    else:
        check_deal = func.check_deal(customer_nick)  # Требует ник
        if check_deal == None:
            try:
                func.deal(seller_id, customer_id, offer_type)
                func.edit_price(offer_price, seller_id)
                bot.send_message(
                    chat_id=seller_id,
                    text="✅ Предложение о проведении сделки отправленно!",
                    reply_markup=kb.canel_offer_seller,
                )
                info = func.info_deal_seller(seller_id)
                info1 = func.profile(seller_id)
                bot.send_message(
                    info[0],
                    text="✅ Вам отправлено предложение о сделке!",
                    reply_markup=types.ReplyKeyboardRemove(),
                )
                msg = bot.send_message(
                    info[0],
                    "❕ id - <b><code>{id}</code></b>\n❕ Проведенных сделок - {offers}\n\n🔥 В этой сделке вы покупатель!".format(
                        id=info1[0], offers=info1[1]
                    ),
                    reply_markup=kb.choise,
                    parse_mode="HTML",
                )
                # func.set_notice_id(customer_id, notifier.id)
            except Exception as e:
                print(e)
                bot.send_message(seller_id, text=error)
        else:
            bot.send_message(
                seller_id,
                text="⛔️ Человек сейчас проводит сделку, и не может начать одновременно вторую.",
            )
            bot.send_message(
                info[0],
                "⛔️ С вами пытались провести сделку, однако система её отклонила, ведь вы проводите другую в настоящий момент!",
            )


# Запись в Базу Данных
@bot.message_handler(commands=["start"])
def start(message: types.Message):
    try:
        # if not checkMember(message.chat.id):
        #     bot.send_message(
        #         message.chat.id,
        #         f"Для доступа к каналу необходимо подписаться на канал!",
        #         reply_markup=kb.channel_url,
        #     )
        #     return
        if not message.chat.type == "private":
            return
        chat_id = message.chat.id
        username = message.from_user.username
        if message.from_user.username == None:
            bot.send_message(
                chat_id, "⛔️ Вам необходимо установить логин для работы с ботом!"
            )
        else:
            func.first_join(user_id=chat_id, username=username)
            bot.send_message(
                chat_id,
                f"Приветствуем, @{message.from_user.username}!🙋\n\n🫂 Добро пожаловать на официального бота-гаранта самой крупной ветки проектов в индустрии!\n\n🏡 На базе нашего гаранта строиться работа еще двух проектов представленных в нашей эко-системе. Мы ежедневно помогаем обезопасить наше сообщество от мошенников, а также защищаем интересы воркеров всех категорий.\n\n👉 Комиссия за проведение сделок является фиксированной и <b>равняется 5% от суммы сделки.</b>\n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими!</a>",
                parse_mode="html",
                disable_web_page_preview=True,
                reply_markup=kb.menu,
            )
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Что-то пошло не так")


# Вызов Админ Панели
@bot.message_handler(commands=["admin"])
def start(message: types.Message):
    # if not checkMember(message.chat.id):
    #     bot.send_message(
    #         message.chat.id,
    #         f"Для доступа к каналу необходимо подписаться на канал!",
    #         reply_markup=kb.channel_url,
    #     )
    #     return
    if not message.chat.type == "private":
        return
    if (
        message.chat.id == admin
        or message.chat.id == admin2
        or message.chat.id == admin3
    ):
        bot.send_message(
            message.chat.id,
            f"✅ {message.from_user.username}, вы авторизованы!",
            reply_markup=kb.admin,
        )


@bot.message_handler(commands=["getBalance"])
def getBalance(message: types.Message):
    res = requests.get(api_link + "getBalance", headers=header).json()
    bot.send_message(message.chat.id, f"Доступно {res['result'][0]['available']} USDT")


# Команды
@bot.message_handler(content_types=["text"])
def send_text(message):
    if not message.chat.type == "private":
        return
    # if not checkMember(message.chat.id):
    #     bot.send_message(
    #         message.chat.id,
    #         f"Для доступа к каналу необходимо подписаться на канал!",
    #         reply_markup=kb.channel_url,
    #     )
    #     return
    chat_id = message.chat.id
    username = message.from_user.username
    try:
        info = func.check_ban(user_id=chat_id)
        if info[0] == "1":
            bot.send_message(chat_id, "⛔️ К сожалению, Вы получили блокировку!")
            return
        info = func.search_block(chat_id)
        if info != None:
            bot.send_message(
                chat_id,
                "⛔️ Вы не можете взаимодействовать с ботом, пока не завершите сделку!",
            )
        else:
            if message.text.lower() == "👤 профиль":
                info = func.profile(user_id=chat_id)
                photo = open("garant/PROFILE GARANT.png", "rb")
                bot.send_photo(
                    chat_id,
                    photo,
                    f"🧾 Ваш профиль:\n\n⚡️ <b>Ваш ID - <code>{info[0]}</code></b>\n\n👤 <b>Ваш логин</b> - @{message.from_user.username}\n\n🤝 <b>Проведенных сделок</b> - {info[1]}\n\n💰 <b>Ваш баланс</b> - {info[2]} USDT (TRC20)\n\nЕсли вы изменили свой @username <i>вы всегда можете изменить ваш логин по нажатию кнопки внизу</i> \n\n❗️<b>Важно всегда изменять логин когда вы изменили ваш @username, так как при некорректном вводе вашего логина пользователи не смогут найти ваш профиль для проведения сделок.</b>",
                    reply_markup=kb.profile,
                    parse_mode="HTML",
                )
            elif message.text.lower() == "🔒 провести сделку":
                photo = open("garant/PROVEDENIE SDELKI GARANT.png", "rb")
                bot.send_photo(
                    chat_id, photo, "В этой сделке вы...", reply_markup=kb.choise_offer
                )
            elif message.text.lower() == "⭐️ о нас":
                deals_number = func.getOffersNumber()
                gm_deals_number = deals_number["g-m"]
                a_deals_number = deals_number["a"]
                deals_summ = func.getOffersSumm()
                gm_deals_summ = math.ceil(deals_summ["g-m"])
                a_deals_summ = math.ceil(deals_summ["a"])
                photo = open(f"garant/ABOUT US GARANT.png", "rb")
                bot.send_photo(
                    chat_id,
                    photo,
                    f"🙋Добро пожаловать на официального бота-гаранта самой крупной ветки проектов в индустрии!\n\n🤝 <a href='https://t.me/pradagarant_bot'>PRADA | GARANT</a> - <b>уникальная система</b>, позволяющая вам проводить сделки на ваших условиях быстро, удобно и безопасно.\n\n💠Система оплаты происходит напрямую через <i>@CryptoBot</i>, что гарантирует <b>сохранность ваших средств</b> и полную <b>конфиденциальность ваших сделок.</b> \n\n💵Все суммы сделок считаются в долларах <b>(USD)</b>, а все сделки проходят в <b>криптовалюте USDT (TRC20)</b>, без возможности перехода оплаты на другую криптовалюту.\n\n🦾Для улучшения работы бота или по любым другим вопросам <b>вы всегда можете обратиться в нашу круглосуточную поддержку -</b> @pradagarant_sup. Мы всегда <b>рады обратной связи</b> и готовы <b>реализовать любые ваши пожелания.</b>\n\n🗓 Дата открытия проекта - <b>12.10.2023. </b>",
                    parse_mode="html",
                    reply_markup=kb.o_nas,
                )
            elif message.text.lower() == "💵 прошедшие сделки":
                photo = open(f"garant/PROSHEDSHIE SDELKI GARANT.png", "rb")
                info = func.profile(chat_id)
                acts_info = func.check_user_offers(chat_id)
                if int(info[1]) == 0:
                    bot.send_photo(chat_id, 
                                   photo, 
                                   caption = "Вы еще не проводили сделок⛔️",
                                   reply_markup=types.InlineKeyboardMarkup().add(
                                        types.InlineKeyboardButton("Скрыть", callback_data="hide_profile")
                                    ),
                    )
                elif acts_info == "customer":
                    text = func.last_offers_customer(chat_id)
                    bot.send_photo(chat_id, photo, text)
                elif acts_info == "seller":
                    text = func.last_offers_seller(chat_id)
                    bot.send_photo(chat_id, photo, text)
                else:
                    bot.send_photo(
                        chat_id,
                        photo,
                        "Вывести ваши последние сделки где вы...",
                        reply_markup=kb.cors,
                    )
            elif message.text.lower() == "🔐сделка по коду":
                photo = open(f"garant/SDELKA PO KODU GARANT.png", "rb")
                msg = bot.send_photo(chat_id, photo, "Пришлите код для создания сделки")
                bot.register_next_step_handler(msg, decoder)
    except Exception as e:
        print(e, "1")
        bot.send_message(chat_id, "Попробуйте заново⛔️")
        func.first_join(user_id=chat_id, username=username)


@bot.callback_query_handler(func=lambda call: True)
def handler_call(call: types.CallbackQuery):
    global deal_timer
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.answer_callback_query(callback_query_id=call.id)
    if call.data == "output":
        msg = bot.send_message(
            chat_id,
            "💠Напишите сколько USDT вы хотите вывести",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(
                    text="Отменить вывод⛔️", callback_data="decline"
                )
            ),
        )
        bot.register_next_step_handler(msg, output)
    elif call.data == "seller":
        info = func.last_offers_seller(chat_id)
        if len(info) > 0:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=info)
        elif len(info) == 0:
            bot.edit_message_text(
                chat_id=chat_id, message_id=message_id, text="⛔️ Сделок не обнаружено!"
            )
            bot.edit_message_reply_markup(
                chat_id=chat_id, message_id=message_id, reply_markup=kb.go_back
            )

    elif call.data == "customer":
        info = func.last_offers_customer(chat_id)
        if len(info) > 0:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=info)
        elif len(info) == 0:
            bot.edit_message_text(
                chat_id=chat_id, message_id=message_id, text="⛔️ Сделок не обнаружено!"
            )
            bot.edit_message_reply_markup(
                chat_id=chat_id, message_id=message_id, reply_markup=kb.go_back
            )

    elif call.data == "menu":
        bot.delete_message(chat_id, call.message.message_id)
    elif call.data == "check_member":
        if checkMember(chat_id):
            bot.delete_message(chat_id, call.message.message_id)
            bot.send_message(
                chat_id,
                f"Приветствуем, @{call.message.from_user.username}!🙋\n\n🫂 Добро пожаловать на официального бота-гаранта самой крупной ветки проектов в индустрии!\n\n🏡 На базе нашего гаранта строиться работа еще двух проектов представленных в нашей эко-системе. Мы ежедневно помогаем обезопасить наше сообщество от мошенников, а также защищаем интересы воркеров всех категорий.\n\n👉 Комиссия за проведение сделок является фиксированной и <b>равняется 5% от суммы сделки.</b>\n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими!</a>",
                parse_mode="html",
                disable_web_page_preview=True,
                reply_markup=kb.menu,
            )
    elif call.data == "bor":
        bot.send_message(chat_id, text="Что вы хотите сделать?", reply_markup=kb.bor)

    elif call.data == "unban":
        msg = bot.send_message(
            chat_id,
            text="Введите ID человека, которого хотите разбанить. (Для отмены введите любую букву)",
        )
        bot.register_next_step_handler(msg, unban1)

    elif call.data == "ban":
        msg = bot.send_message(
            chat_id,
            text="Введите ID человека, которого хотите забанить. (Для отмены введите любую букву)",
        )
        bot.register_next_step_handler(msg, ban1)
    elif call.data == "hide":
        try:
            bot.delete_message(chat_id, call.message.message_id)
            bot.delete_message(chat_id, call.message.message_id - 1)
        except:
            pass
    elif call.data == "edit_balance":
        msg = bot.send_message(
            chat_id=chat_id,
            text="Введите ID человека, которому хотите изменить балнс. (Для отмены введите любую букву)",
        )
        bot.register_next_step_handler(msg, give_balance1)

    elif call.data == "input":
        msg = bot.send_message(
            chat_id,
            "💠 Внимание! Наш бот принимет оплату только в валюте USDT (TRC20) 💠  \n\n 💸 Напишите сумму на которую вы хотите пополнить баланс.",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(
                    text="Отменить пополнение", callback_data="decline"
                )
            ),
        )
        bot.register_next_step_handler(msg, getAmount)
    elif call.data == "check_payment":
        invoices = requests.get(api_link + "getInvoices", headers=header).json()
        if invoices["result"]["items"][0]["status"] == "paid":
            bot.delete_message(chat_id=chat_id, message_id=message_id)
            bot.send_message(text="Успешно оплачено!", chat_id=chat_id)
            func.input(chat_id, invoices["result"]["items"][0]["amount"])
        else:
            bot.send_message(chat_id, "Оплата не прошла. Попробуйте еще раз⛔️")

    elif call.data == "canel_payment":
        func.canel_payment(user_id=chat_id)
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Меню")
        bot.send_message(chat_id, text="🔔Включение клавиатуры", reply_markup=kb.menu)

    elif call.data == "message":
        msg = bot.send_message(
            chat_id=chat_id,
            text='Введите текст для рассылки. \n\nДля отмены напишите "-" без кавычек!',
        )
        bot.register_next_step_handler(msg, message1)

    elif call.data == "seller_offer":
        bot.delete_message(chat_id, message_id)
        msg = bot.send_message(
            chat_id=chat_id,
            text='🔔 Введите логин пользователя (Без @), с которым хотите провести сделку. \n\n❌ Для отмены напишите "-" без кавычек!',
        )
        bot.register_next_step_handler(msg, search_seller)

    elif call.data == "customer_offer":
        bot.delete_message(chat_id, message_id)
        msg = bot.send_message(
            chat_id=chat_id,
            text='🔔Введите логин пользователя (Без @), с которым хотите провести сделку. \n\nДля отмены напишите "-" без кавычек!',
        )
        bot.register_next_step_handler(msg, search_customer)
    elif call.data == "decline":
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.clear_step_handler(call.message)
    elif call.data == "proposal_customer":
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="✅ Предложение о проведении сделки отправленно!",
                reply_markup=kb.canel_offer_customer,
            )
            info = func.info_deal_customer(chat_id)
            info1 = func.profile(chat_id)
            bot.send_message(
                info[0],
                text="✅ Вам отправлено предложение о сделке!",
                reply_markup=types.ReplyKeyboardRemove(),
            )
            msg = bot.send_message(
                info[0],
                "❕ id - <b><code>{id}</code></b>\n❕ Логин - @{nick}\n❕ Проведенных сделок - {offers}\n\n🔥 В этой сделке вы продавец!".format(
                    id=info1[0], offers=info1[1], nick=info1[4]
                ),
                reply_markup=kb.choise_seller,
                parse_mode="HTML",
            )
            # time = datetime.datetime
            # run_time = time.now() + datetime.timedelta(seconds=10)
            # notifier = sched.add_job(
            #     func=notice,
            #     trigger="date",
            #     run_date=run_time,
            #     args=[info[0], msg.id],
            # )
            # func.set_notice_id(info[0], notifier.id)
        except Exception as e:
            print(e)
            bot.send_message(chat_id, text=error)

    elif call.data == "proposal_seller":
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="✅ Предложение о проведении сделки отправленно!",
                reply_markup=kb.canel_offer_seller,
            )
            info = func.info_deal_seller(chat_id)
            info1 = func.profile(chat_id)
            bot.send_message(
                info[0],
                text="✅ Вам отправлено предложение о сделке!",
                reply_markup=types.ReplyKeyboardRemove(),
            )
            msg = bot.send_message(
                info[0],
                "❕ id - <b><code>{id}</code></b>\n❕ Логин - @{nick}\n❕ Проведенных сделок - {offers}\n\n🔥 В этой сделке вы покупатель!".format(
                    id=info1[0], offers=info1[1], nick=info1[4]
                ),
                reply_markup=kb.choise,
                parse_mode="HTML",
            )
            # time = datetime.datetime
            # run_time = time.now() + datetime.timedelta(seconds=10)
            # notifier = sched.add_job(
            #     func=notice,
            #     trigger="date",
            #     run_date=run_time,
            #     args=[info[0], msg.id],
            # )
            # func.set_notice_id(info[0], notifier.id)
        except Exception as e:
            print(e)
            bot.send_message(chat_id, text=error)

    elif call.data == "delete_customer":
        try:
            info = func.info_offers_customer(chat_id)
            if info[4] == "dont_open":
                func.delete_customer(chat_id)
                bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id, text="⛔️ Сделка отменена."
                )
                bot.send_message(chat_id, text=enable_keyboard, reply_markup=kb.menu)
                bot.send_message(
                    info[0],
                    text="🌧 Ваше предложение о проведении сделки отклонили, или с вами пытались её провести, но передумали.",
                    reply_markup=kb.menu,
                )
            else:
                bot.send_message(
                    chat_id, text="⛔️ Сделка уже начата, и не может быть отменена."
                )
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "delete_seller":
        try:
            info = func.info_offers_seller(chat_id)
            if info[4] == "dont_open":
                func.delete_seller(chat_id)
                bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id, text="⛔️ Сделка отменена."
                )
                bot.send_message(chat_id, text=enable_keyboard, reply_markup=kb.menu)
                bot.send_message(
                    info[1],
                    text="🌧 Ваше предложение о проведении сделки отклонили, или с вами пытались её провести, но передумали.",
                    reply_markup=kb.menu,
                )
            else:
                bot.send_message(
                    chat_id, text="⛔️ Сделка уже начата, и не может быть отменена."
                )
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "statistics":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=func.stats(),
            reply_markup=kb.admin,
        )

    elif call.data == "accept_customer":
        try:
            func.accept_customer(chat_id)
            info = func.info_offers_customer(chat_id)
            info_c = func.profile(info[1])
            info_s = func.profile(info[0])
            status = info[4]
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"💰 Сделка №{info[3]}\n👤 Покупатель - {info_c[0]}\n💎 Продавец - {info_s[0]}\n\n💳 {'Сумма - Не указана' if info[2] == None else f'{info[2]} USDT'}\n📄 Статус сделки - {status}",
                reply_markup=kb.customer_panel,
            )
            bot.send_message(
                info_s[0],
                text=f"💰 Сделка №{info[3]}\n👤 Покупатель - {info_c[0]}\n💎 Продавец - {info_s[0]}\n\n💳 {'Сумма - Не указана' if info[2] == None else f'{info[2]} USDT'}\n📄 Статус сделки - {status}",
                reply_markup=kb.seller_panel,
            )
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "accept_seller":
        try:
            func.accept_seller(chat_id)
            info = func.info_offers_seller(chat_id)
            info_c = func.profile(info[1])
            info_s = func.profile(info[0])
            sum_offer = info[2]
            status = info[4]
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"💰 Сделка №{info[3]}\n👤 Покупатель - {info_c[0]}\n💎 Продавец - {info_s[0]}\n\n💳 {'Сумма - Не указана' if info[2] == None else f'{sum_offer} USDT'}\n📄 Статус сделки - {status}",
                reply_markup=kb.seller_panel,
            )
            bot.send_message(
                info_c[0],
                text=f"💰 Сделка №{info[3]}\n👤 Покупатель - {info_c[0]}\n💎 Продавец - {info_s[0]}\n\n💳 {'Сумма - Не указана' if info[2] == None else f'{sum_offer} USDT'}\n📄 Статус сделки - {status}",
                reply_markup=kb.customer_panel,
            )
        except Exception as e:
            print(e, " accept_seller")
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "input_panel":
        try:
            info = func.profile(chat_id)
            offer = func.info_offers_customer(chat_id)
            if offer[2] == None:
                bot.answer_callback_query(
                    callback_query_id=call.id,
                    show_alert=True,
                    text="⛔️ Продавец не указал сумму!",
                )
            else:
                if offer[4] == "success":
                    bot.answer_callback_query(
                        callback_query_id=call.id,
                        show_alert=True,
                        text="⛔️ Вы уже оплатили товар, продавец обязан вам его передать. Если продавец отказывается передать товар, откройте спор.",
                    )
                else:
                    if float(info[2]) < float(offer[2]):
                        bot.send_message(
                            chat_id,
                            text="📉 Вам необходимо пополнить баланс!\n💰 Ваш баланс - {user} USDT\n💳 Необходимый баланс - {offer} USDT\n\nДля этого вам необходимо отменить сделку!".format(
                                user=info[2], offer=offer[2]
                            ),
                        )
                    else:
                        bal = float(info[2]) - float(offer[2])
                        func.success(chat_id, bal)
                        info = func.info_offers_customer(chat_id)
                        bot.send_message(
                            info[0],
                            text="✅ Покупатель оплатил товар! \nВам необходимо передать товар.",
                        )
                        bot.send_message(
                            info[1],
                            text="✅ Товар был успешно оплачен, ожидайте получения товара. Если тот не валид, или продавец кинул в ЧС, откройте спор.",
                        )
        except:
            bot.send_message(chat_id, text=error)

    elif call.data == "price":
        try:
            info = func.info_offers_seller(chat_id)
            if info[2] == None:
                msg = bot.send_message(
                    chat_id,
                    text='💰 Введите сумму товара. \n\nДля отмены напишите "-" без кавычек!',
                )
                bot.register_next_step_handler(msg, price)
            else:
                bot.send_message(
                    chat_id,
                    text="🔔Вы уже ввели сумму товара, и не можете её редактировать!",
                )
        except Exception as e:
            print(e)
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "canel_open":
        bot.send_message(
            chat_id,
            text="🔔Вы уверены что хотите отменить сделку?",
            reply_markup=kb.choise_canel,
        )

    elif call.data == "No_canel":
        bot.answer_callback_query(
            callback_query_id=call.id,
            show_alert=True,
            text="✅Процесс отмены сделки аннулирован",
        )

    elif call.data == "Yes_canel":
        try:
            info = func.info_offers_customer(chat_id)
            if info[4] == "open":
                bot.answer_callback_query(
                    callback_query_id=call.id,
                    show_alert=True,
                    text="🔔Запрос на отмену отправлен продавцу",
                )
                bot.send_message(
                    info[0],
                    text="🔔Покупатель предложил отменить сделку.",
                    reply_markup=kb.choise_canel_seller2,
                )
            else:
                bot.answer_callback_query(
                    callback_query_id=call.id,
                    show_alert=True,
                    text="🔔Сделка уже завершена или над ней проходит спор.",
                )
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "Yes_canel_seller":
        try:
            info = func.info_offers_seller(chat_id)
            if info[4] == "open":
                func.yes_canel_seller2(chat_id)
                bot.send_message(
                    info[0], text="✅ Сделка успешно отменена.", reply_markup=kb.menu
                )
                bot.send_message(
                    info[1], text="✅ Сделка успешно отменена.", reply_markup=kb.menu
                )
            else:
                bot.answer_callback_query(
                    callback_query_id=call.id,
                    show_alert=True,
                    text="✅ Сделка уже завершена или над ней проходит спор.",
                )
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "canel_open_seller":
        bot.send_message(
            chat_id,
            text="🔔Вы уверены что хотите отменить сделку?",
            reply_markup=kb.choise_canel_seller,
        )

    elif call.data == "Yes_canel_seller1":
        try:
            info = func.info_offers_seller(chat_id)
            if info[4] == "open":
                bot.answer_callback_query(
                    callback_query_id=call.id,
                    show_alert=True,
                    text="🔔Запрос на отмену отправлен покупателю",
                )
                bot.send_message(
                    info[1],
                    text="🔔Продавец предложил отменить сделку.",
                    reply_markup=kb.choise_canel_customer,
                )
            else:
                bot.answer_callback_query(
                    callback_query_id=call.id,
                    show_alert=True,
                    text="🔔Сделка уже завершена или над ней проходит спор.",
                )
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "No_canel_seller1":
        bot.answer_callback_query(
            callback_query_id=call.id,
            show_alert=True,
            text="✅ Процесс отмены сделки аннулирован",
        )

    elif call.data == "No_canel_seller":
        bot.answer_callback_query(
            callback_query_id=call.id,
            show_alert=True,
            text="✅ Процесс отмены сделки аннулирован",
        )

    elif call.data == "Yes_canel_customer":
        try:
            info = func.info_offers_customer(chat_id)
            if info[4] == "open":
                func.yes_canel_customer2(chat_id)
                bot.send_message(
                    info[0], text="✅ Сделка успешно отменена.", reply_markup=kb.menu
                )
                bot.send_message(
                    info[1], text="✅ Сделка успешно отменена.", reply_markup=kb.menu
                )
            else:
                bot.answer_callback_query(
                    callback_query_id=call.id,
                    show_alert=True,
                    text="✅ Сделка уже завершена или над ней проходит спор.",
                )
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "No_canel_customer":
        bot.answer_callback_query(
            callback_query_id=call.id,
            show_alert=True,
            text="✅ Процесс отмены сделки аннулирован",
        )

    elif call.data == "ok":
        try:
            info = func.info_offer_customer(chat_id)
            if info[0] == "success":
                bot.send_message(
                    chat_id,
                    text="🔔Вы уверены что получили товар, и он валидный? Если нет, или условия не соблюдены, то вам необходимо открыть спор.",
                    reply_markup=kb.ok_choise,
                )
            else:
                bot.send_message(
                    chat_id, text="✅ Вы не оплатили сделку, или над ней ведётся спор."
                )
        except Exception as e:
            print(e)
            bot.send_message(chat_id, text=error)

    elif call.data == "ok_canel":
        bot.answer_callback_query(
            callback_query_id=call.id,
            show_alert=True,
            text="🔔Вы подтвердили, что товар не получен.",
        )

    elif call.data == "ok_ok":
        try:
            info = func.info_offers_customer(chat_id)
            if info[4] == "success":
                info1 = func.profile(info[0])
                info2 = func.profile(info[1])
                func.ok(
                    chat_id,
                    info[0],
                    float(info[2]) * (1 - (procent / 100)),
                    info[3],
                    info1[2],
                    info1[4],
                    info2[4],
                    info1[1],
                    info2[1],
                    info[5],
                )
                bot.send_message(
                    chat_id,
                    text="✅ Сделка успешно завершена!\n📝 Хотите оставить отзыв о продавце?",
                    reply_markup=kb.add_review,
                )
                bot.send_message(
                    info[0],
                    text="✅ Сделка успешно завершена!\n💰 Деньги зачислены на ваш счёт.\n\n📝 Сейчас покупатель оставляет отзыв, подождите пожалуйста.",
                    reply_markup=kb.cancel_wait,
                )
                # bot.send_message(
                #     chat_id_bot,
                #     text="✅ Cделка успешно завершена!\n💰 Сумма - {sum_offer} рублей\n\n👤 Продавец - @{seller_nick}\n👤 Покупатель - @{customer_nick}".format(
                #         sum_offer=info[2], seller_nick=info1[5], customer_nick=info2[5]
                #     ),
                # )
            else:
                bot.send_message(
                    chat_id, text="🔔Вы не оплатили сделку, или над ней ведётся спор."
                )
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "open_dispute":
        try:
            info = func.info_offers_customer(chat_id)
            if info[4] == "dont_open":
                bot.send_message(chat_id, text="⛔️ Сделка ещё не открыта!")
            else:
                if info[4] == "open":
                    bot.send_message(
                        chat_id,
                        text="⛔️ Товар ещё не был вам передан. Если вы считаете что продавец хочет вас обмануть, отмените сделку и напишите администратору @{}.".format(
                            nicknameadm
                        ),
                    )
                else:
                    if info[4] == "dispute":
                        bot.send_message(chat_id, text="⛔️ Спор уже начат.")
                    else:
                        info_c = func.profile(info[1])
                        info_s = func.profile(info[0])
                        func.dispute_customer(chat_id)
                        bot.send_message(
                            chat_id,
                            text="🔔Спор начат, продавец оповещён. Если долго ничего не происходит, напишите администратору @{}.".format(
                                nicknameadm
                            ),
                        )
                        bot.send_message(
                            info[0],
                            text="🔔Покупатель начал спор по вашему товару, скоро вам напишет администратор. Если долго ничего не происходит, напишите администратору @{}.".format(
                                nicknameadm
                            ),
                        )
                        bot.send_message(
                            admin,
                            text="🔔Был начат спор!\n\nID сделки - <b><code>{id}</code></b>\nПродавец - @{seller}\nПокупатель(Организовал спор) - @{customer}".format(
                                id=info[3], seller=info_s[4], customer=info_c[4]
                            ),
                            parse_mode="HTML",
                        )
        except:
            bot.send_message(chat_id, text=error)

    elif call.data == "open_dispute_seller":
        try:
            info = func.info_offers_seller(chat_id)
            if info[4] == "dont_open":
                bot.send_message(chat_id, text="⛔️ Сделка ещё не открыта!")
            else:
                if info[4] == "open":
                    bot.send_message(
                        chat_id,
                        text="🔔Товар ещё не был вам передан. Если вы считаете что продавец хочет вам обмануть, отмените сделку и напишите администратору @{}.".format(
                            nicknameadm
                        ),
                    )
                else:
                    if info[4] == "dispute":
                        bot.send_message(chat_id, text="⛔️ Спор уже начат.")
                    else:
                        info_c = func.profile(info[1])
                        info_s = func.profile(info[0])
                        func.dispute_customer(chat_id)
                        bot.send_message(
                            chat_id,
                            text="🔔Спор начат, покупатель оповещён. Если долго ничего не происходит, напишите администратору @{}.".format(
                                nicknameadm
                            ),
                        )
                        bot.send_message(
                            info[1],
                            text="🔔Продавец начал спор, скоро вам напишет администратор. Если долго ничего не происходит, напишите администратору @{}.".format(
                                nicknameadm
                            ),
                        )
                        bot.send_message(
                            admin,
                            text="🔔Был начат спор!\n\nID сделки - <b><code>{id}</code></b>\nПродавец - @{seller}\nПокупатель(Организовал спор) - @{customer}".format(
                                id=info[3], seller=info_s[5], customer=info_c[5]
                            ),
                            parse_mode="HTML",
                        )
        except:
            bot.send_message(chat_id, text=error)

    elif call.data == "dispute_admin":
        msg = bot.send_message(
            chat_id, text='Введите ID сделки. (Для отмены введите "-" без кавычек)'
        )
        bot.register_next_step_handler(msg, dispute_admin_func)

    elif call.data == "customer_true":
        msg = bot.send_message(
            chat_id,
            text='Покупатель вернёт деньги, а сделка будет отменена!\nДля подтверждения введите ID сделки, для отмены введите "-" без кавычек',
        )
        bot.register_next_step_handler(msg, customer_true_func)
    elif call.data == "hide_profile":
        bot.delete_message(chat_id, call.message.message_id)
        bot.delete_message(chat_id, call.message.message_id - 1)
    elif call.data == "my_reviews":
        if func.reviews(chat_id) == "":
            bot.send_message(
                chat_id,
                "<b>О вас еще не оставили ни одного отзыва 😔</b>",
                parse_mode="HTML",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("Скрыть", callback_data="hide_reviews")
                ),
            )
            return
        bot.send_message(
            chat_id,
            func.reviews(chat_id),
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("Скрыть", callback_data="hide_reviews")
            ),
        )
    elif call.data == "hide_reviews":
        bot.delete_message(chat_id, call.message.message_id)
    elif call.data == "seller_true":
        msg = bot.send_message(
            chat_id,
            text='Продавец получит деньги, а сделка будет отменена!\nДля подтверждения введите ID сделки, для отмены введите "-" без кавычек.',
        )
        bot.register_next_step_handler(msg, seller_true_func)

    elif call.data == "no_true":
        msg = bot.send_message(
            chat_id,
            text='Покупатель вернёт деньги, а сделка будет отменена!\nДля подтверждения введите ID сделки, для отмены введите "-" без кавычек.',
        )
        bot.register_next_step_handler(msg, customer_true_func)

    elif call.data == "canel_open_offer":
        try:
            info = func.canel_open_offer(chat_id)
            if info[0] == "OK":
                bot.send_message(
                    chat_id,
                    text="🔥 Предложение о проведении сделки отозвано.",
                    reply_markup=kb.menu,
                )
                bot.send_message(
                    info[1],
                    text="🔥 Покупатель отозвал своё предложение о проведении сделки.",
                    reply_markup=kb.menu,
                )
            else:
                bot.send_message(
                    chat_id,
                    text="🔥 Вы не можете отозвать предложение когда продавец его уже принял.",
                )
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "canel_open_offer_seller":
        try:
            info = func.canel_open_offer_seller(chat_id)
            if info[0] == "OK":
                bot.send_message(
                    chat_id,
                    text="🔥 Предложение о проведении сделки отозвано.",
                    reply_markup=kb.menu,
                )
                bot.send_message(
                    info[1],
                    text="🔥 Продавец отозвал своё предложение о проведении сделки.",
                    reply_markup=kb.menu,
                )
            else:
                bot.send_message(
                    chat_id,
                    text="🔥 Вы не можете отозвать предложение когда покупатель его уже принял.",
                )
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "reviews":
        try:
            info1 = func.info_offers_customer(chat_id)
            if info1 == None:
                info1 = func.info_offers_seller(chat_id)
                info = func.reviews(info1[1])
                if len(info) > 0:
                    bot.send_message(chat_id=chat_id, text=info)
                elif len(info) == 0:
                    bot.send_message(chat_id=chat_id, text="⛔️ отзывов не обнаружено!")
            else:
                info = func.reviews(info1[0])
                if len(info) > 0:
                    bot.send_message(chat_id=chat_id, text=info)
                elif len(info) == 0:
                    bot.send_message(chat_id=chat_id, text="⛔️ отзывов не обнаружено!")
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    if call.data == "add_review":
        try:
            info = func.info_offer_customer(chat_id)
            if info[0] == "review":
                msg = bot.send_message(
                    chat_id,
                    text='🔥 Напишите отзыв о сделке, для отмены вышлите "-" без кавычек.',
                )
                bot.register_next_step_handler(msg, add_review)
            else:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text="Вы не можете оставить отзыв, так как не завершили сделку⛔️",
                    reply_markup=kb.menu,
                )
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "up_login":
        try:
            info = func.up_login(call.message.chat.username, call.message.chat.id)
            if info == None:
                bot.send_message(chat_id, text="Ваш логин обновлён!")
            else:
                bot.send_message(
                    chat_id,
                    text="Логин, который вы хотите занять уже получил другой пользователь, или вы его уже заняли!⛔️",
                )
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )

    elif call.data == "no_review":
        try:
            info = func.info_offers_customer(chat_id)
            bot.send_message(
                info[0],
                text="❄️ Покупатель отказался оставлять отызв.",
                reply_markup=kb.menu,
            )
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="❄️ Сделка успешно завершена!",
            )
            bot.send_message(chat_id, text=enable_keyboard, reply_markup=kb.menu)
            func.close_offer(chat_id)
        except:
            bot.send_message(chat_id, text=error)

    elif call.data == "cancel_wait":
        try:
            info = func.info_offers_seller(chat_id)
            if info[4] == "review":
                func.close_offer_seller(chat_id)
                bot.send_message(
                    chat_id,
                    text="❄️ Ожидание отменено, покупатель не может больше оставить отзыв.",
                    reply_markup=kb.menu,
                )
                bot.send_message(
                    info[1],
                    "Продавец не захотел ожидать отзыва. Сделка заверешна💔",
                    reply_markup=kb.menu,
                )
            else:
                bot.send_message(chat_id, error)
        except:
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=True, text=error
            )
    elif call.data == "go_back":
        bot.edit_message_text(
            message_id=call.message.message_id,
            chat_id=chat_id,
            text="Вывести ваши последние сделки где вы...",
        )
        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=call.message.message_id,
            inline_message_id=call.message.message_id,
            reply_markup=kb.cors,
        )


def decoder(message):
    try:
        if func.decode_link(message.text).startswith("offer"):
            offer_link_split = func.decode_link(message.text).split()
            seller_id = offer_link_split[1]
            customer_id = offer_link_split[2]
            get_offer_from_string(
                seller_id=seller_id,
                customer_id=customer_id,
                offer_type=offer_link_split[4],
                offer_link_split=offer_link_split,
            )
    except Exception as e:
        print(e, " decoder error")


def getAmount(message):
    try:
        try:
            amount = int(message.text)
        except:
            msg = bot.send_message(message.chat.id, "Введите положительное число!⛔️")
            bot.register_next_step_handler(msg, getAmount)
            return
        api_msg_raw = requests.get(
            url=api_link + f"createInvoice?asset=USDT&amount={amount}", headers=header
        ).json()
        api_msg = api_msg_raw["result"]
        bot.send_message(
            message.chat.id,
            f"💵Запрос на пополнение баланса: \n\n ID: {api_msg['invoice_id']} \n Валюта: {api_msg['asset']} \n Сумма: {api_msg['amount']} \n",
            reply_markup=func.getUrlMarkup(api_msg["pay_url"]),
        )
    except Exception as e:
        print(e, " get amount")
        print(api_msg_raw, " request")


def add_review(message):
    try:
        if message.text.startswith("-"):
            info = func.info_offers_customer(message.chat.id)
            bot.send_message(
                message.chat.id, text=canel_operation, reply_markup=kb.menu
            )
            func.close_offer(message.chat.id)
        else:
            info = func.info_offers_customer(message.chat.id)
            func.add_review(info[0], info[2], message.chat.id, message.text)
            bot.send_message(
                message.chat.id, text="📝 Отзыв успешно оставлен.", reply_markup=kb.menu
            )
            bot.send_message(
                info[0],
                text="📝 О вас оставили отзыв!\n\n" + message.text,
                reply_markup=kb.menu,
            )
            func.close_offer(message.chat.id)
    except:
        bot.answer_callback_query(
            callback_query_id=message.id, show_alert=True, text=error
        )


def customer_true_func(message):
    try:
        if message.text.startswith("-"):
            bot.send_message(message.chat.id, text=canel_operation)
        else:
            if message.text.isdigit():
                info = func.dispute_info(message.text)
                info1 = func.profile(info[1])
                func.customer_true(message.text, info[1], info1[2], info[2])
                bot.send_message(message.chat.id, text="✅ Вердикт успешно вынесен.")
                bot.send_message(
                    info[1],
                    text="✅ Вердикт был вынесен в вашу пользу!",
                    reply_markup=kb.menu,
                )
                bot.send_message(
                    info[0],
                    text="✅ Вердикт был вынесен в пользу покупателя!",
                    reply_markup=kb.menu,
                )
            else:
                bot.send_message(message.chat.id, text="⛔️ Вы ввели ID сделки буквами!")
    except:
        bot.send_message(message.chat.id, text=error)


def seller_true_func(message):
    try:
        if message.text.startswith("-"):
            bot.send_message(message.chat.id, text=canel_operation)
        else:
            if message.text.isdigit():
                info = func.dispute_info(message.text)
                info_s = func.profile(info[0])
                info_c = func.profile(info[1])
                func.seller_true(
                    message.text, info[0], info[1], info_s[2], info_c[2], info[2]
                )
                bot.send_message(message.chat.id, text="✅ Вердикт успешно вынесен.")
                bot.send_message(
                    info[1],
                    text="✅ Вердикт был вынесен в пользу продавца!",
                    reply_markup=kb.menu,
                )
                bot.send_message(
                    info[0],
                    text="✅ Вердикт был вынесен в вашу пользу!",
                    reply_markup=kb.menu,
                )
            else:
                bot.send_message(message.chat.id, text="⛔️ Вы ввели ID сделки буквами!")
    except:
        bot.send_message(message.chat.id, text=error)


def dispute_admin_func(message):
    try:
        if message.text.startswith("-"):
            bot.send_message(message.chat.id, text=canel_operation)
        else:
            if message.text.isdigit():
                info = func.dispute_info(message.text)
                if info == None:
                    bot.send_message(message.chat.id, text="⛔️ Сделка не обнаружена!")
                else:
                    info_s = func.profile(info[0])
                    info_c = func.profile(info[1])
                    bot.send_message(
                        message.chat.id,
                        text="🧾 Информация о сделке №{id}\n\n❕ Покупатель - ID{customer}(@{customer_nick})\n❕ Продавец - ID{seller}(@{seller_nick})\n💰 Сумма сделки - {sum_offer} USDT\n📊 Статус сделки - {status}\n\nКто прав в данном споре?".format(
                            id=info[3],
                            customer=info[1],
                            seller=info[0],
                            status=info[4],
                            sum_offer=info[2],
                            customer_nick=info_c[4],
                            seller_nick=info_s[4],
                        ),
                        reply_markup=kb.choise_admin,
                    )
            else:
                bot.send_message(message.chat.id, text="⛔️ Вы ввели ID сделки буквами!")
    except:
        bot.send_message(message.chat.id, text=error)


def ban1(message):
    ban = message.text
    try:
        int(ban)
        func.ban(ban)
        bot.send_message(message.chat.id, text="✅ Человек успешно забанен!")
    except:
        bot.send_message(message.chat.id, text=canel_operation)


def unban1(message):
    try:
        unban = message.text
        int(unban)
        func.unban(unban)
        bot.send_message(message.chat.id, text="✅ Человек успешно разбанен!")
    except:
        bot.send_message(message.chat.id, text=canel_operation)


def give_balance1(message):
    balance = func.GiveBalance(message.text)
    balance_dict[message.chat.id] = balance
    msg = bot.send_message(
        message.chat.id,
        text="Введите сумму, на которую хотите изменить баланс. (Для отмены введите любую букву)",
    )
    bot.register_next_step_handler(msg, give_balance2)


def give_balance2(message):
    balance = balance_dict[message.chat.id]
    balance.balance = message.text
    balance = balance_dict[message.chat.id]
    func.edit_balance(balance)
    bot.send_message(message.chat.id, text="✅ Баланс успешно отредактирован")


def search_seller(message):
    try:
        if message.text.startswith("-"):
            bot.send_message(message.chat.id, text=canel_operation)
        else:
            info1 = func.profile(message.chat.id)
            if (
                str(message.text) == message.from_user.username
                or info1[4] != message.from_user.username
            ):
                bot.send_message(
                    message.chat.id,
                    text="⛔️ С самим собой провести сделку невозможно, или вы изменили ник. Если это так, то Вам необходимо его обновить в профиле.",
                )
            else:
                info = func.search(message.text)
                if info == None:
                    bot.send_message(
                        message.chat.id,
                        text="⛔️ Пользователь не найден, пожалуйста, убедитесь что он уже взаимодействовал с ботом!",
                    )
                else:
                    info1 = func.check_deal(message.text)
                    if info1 == None:
                        func.deal(
                            seller_id=message.chat.id,
                            customer_id=info[0],
                            deal_type="g",
                        )
                        bot.send_message(
                            message.chat.id,
                            "🧾 Профиль:\n\n❕ Id - <b><code>{id}</code></b>\n❕ Логин - @{nickname}\n❕ Проведенных сделок - {offers}\n\n🔥 В этой сделке вы будете продавцом!".format(
                                id=info[0], nickname=info[4], offers=info[1]
                            ),
                            reply_markup=kb.sentence_seller,
                            parse_mode="HTML",
                        )
                        bot.send_message(
                            message.chat.id,
                            text=disable_keyboard,
                            reply_markup=types.ReplyKeyboardRemove(),
                        )
                    else:
                        bot.send_message(
                            message.chat.id,
                            text="⛔️ Человек сейчас проводит сделку, и не может начать одновременно вторую.",
                        )
                        bot.send_message(
                            info[0],
                            "⛔️ С вами пытались провести сделку, однако система её отклонила, ведь вы проводите другую в настоящий момент!",
                        )
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, text=error)


def search_customer(message):
    try:
        if message.text.startswith("-"):
            bot.send_message(message.chat.id, text=canel_operation)
        else:
            info1 = func.profile(message.chat.id)
            if (
                str(message.text) == message.from_user.username
                or info1[4] != message.from_user.username
            ):
                bot.send_message(
                    message.chat.id,
                    text="⛔️ С самим собой провести сделку невозможно, или вы изменили ник. Если это так, то Вам необходимо его обновить в профиле.",
                )
            else:
                info = func.search(message.text)
                if info == None:
                    bot.send_message(
                        message.chat.id,
                        text="⛔️ Пользователь не найден, пожалуйста, убедитесь что он уже взаимодействовал с ботом!",
                    )
                else:
                    result = func.check_deal(message.text)
                    if result == None:
                        func.deal(
                            seller_id=info[0],
                            customer_id=message.chat.id,
                            deal_type="g",
                        )
                        bot.send_message(
                            message.chat.id,
                            "🧾 Профиль:\n\n❕ Id - <b><code>{id}</code></b>\n❕ Логин - @{nickname}\n❕ Проведенных сделок - {offers}\n\n🔥В этой сделке вы будете покупателем!".format(
                                id=info[0], nickname=info[4], offers=info[1]
                            ),
                            reply_markup=kb.sentence,
                            parse_mode="HTML",
                        )
                        bot.send_message(
                            message.chat.id,
                            text=disable_keyboard,
                            reply_markup=types.ReplyKeyboardRemove(),
                        )
                    else:
                        bot.send_message(
                            message.chat.id,
                            text="⛔️ Человек сейчас проводит сделку, и не может начать одновременно вторую.",
                        )
                        bot.send_message(
                            info[0],
                            "⛔️ С вами пытались провести сделку, однако система её отклонила, ведь вы проводите другую в настоящий момент!",
                        )
    except Exception as e:
        print(e, " search customer")
        bot.send_message(message.chat.id, text=error)


def output(message):
    try:
        if message.text.startswith("-"):
            bot.send_message(message.chat.id, text="⛔️ Не в мою смену...")
        else:
            try:
                output_amount = float(message.text)
            except:
                msg = bot.send_message(message.chat.id, "Введите число!")
                bot.register_next_step_handler(msg, output)
            if output_amount * func.getExchangeRate() < 1:
                msg = bot.send_message(
                    message.chat.id,
                    f"Минимальная сумма пополнения 1 USD \n Актульный курс USDT/USD = {func.getExchangeRate()}💵",
                )
                bot.register_next_step_handler(msg, output)
            else:
                info = func.profile(message.chat.id)
                if float(info[2]) < output_amount:
                    msg = bot.send_message(
                        message.chat.id,
                        "Недостаточно денег на балансе. Попробуйте еще раз⛔️",
                    )
                    bot.register_next_step_handler(msg, output)
                else:
                    try:
                        transfer = requests.get(
                            api_link
                            + f"transfer?user_id={message.chat.id}&spend_id={func.generate_random_string(16)}&asset=USDT&amount={output_amount}",
                            headers=header,
                        ).json()["result"]
                        func.output(message.chat.id, output_amount)
                        bot.send_message(
                            message.chat.id,
                            f"Успешно выведено {transfer['amount']} USDT.",
                        )
                    except Exception as e:
                        print(e, " transfer error")
                        msg = bot.send_message(
                            message.chat.id, "Что-то пошло не так. Попробуйте еще раз⛔️"
                        )
                        bot.register_next_step_handler(msg, output)
    except Exception as e:
        print(e, " output error")
        bot.send_message(message.chat.id, text=error)


def message1(message):
    text = message.text
    if message.text.startswith("-"):
        bot.send_message(message.chat.id, text=canel_operation)
    else:
        info = func.admin_message(text)
        bot.send_message(message.chat.id, text="✅ Рассылка начата!")
        for i in range(len(info)):
            try:
                time.sleep(1)
                bot.send_message(info[i][0], str(text))
            except:
                pass
        bot.send_message(message.chat.id, text="✅ Рассылка завершена!")


def price(message):
    money = message.text
    info = func.info_offers_seller(message.chat.id)
    try:
        if message.text.startswith("-"):
            bot.send_message(message.chat.id, text=canel_operation)
        else:
            info_c = func.profile(info[1])
            info_s = func.profile(info[0])
            int(money)
            status = info[4]
            func.edit_price(money, message.chat.id)
            info = func.info_offers_seller(message.chat.id)
            bot.send_message(
                message.chat.id,
                text="💥 Сумма сделки успешно изменена\n\n💰 Сделка №{id}\n👤 Покупатель - {customer_id}\n💎 Продавец - {seller_id}\n\n💳 Сумма - {sum} USDT\n📄 Статус сделки - {status}".format(
                    id=info[3],
                    customer_id=info_c[0],
                    customer_nick=info_c[4],
                    seller_id=info_s[0],
                    seller_nick=info_s[4],
                    sum=info[2],
                    status=status,
                ),
                reply_markup=kb.seller_panel,
            )
            bot.send_message(
                info[1],
                text="💥 Была изменена сумма сделки!\n\n💰 Сделка №{id}\n👤 Покупатель - {customer_id}\n💎 Продавец - {seller_id}\n\n💳 Сумма - {sum} USDT\n📄 Статус сделки - {status}".format(
                    id=info[3],
                    customer_id=info_c[0],
                    customer_nick=info_c[4],
                    seller_id=info_s[0],
                    seller_nick=info_s[4],
                    sum=info[2],
                    status=status,
                ),
                reply_markup=kb.customer_panel,
            )
    except:
        bot.send_message(message.chat.id, text=error)


print("zapuskaemsya")
# Поддержание работы
if __name__ == "__main__":
    while True:
        try:
            schedule.run_pending()
            bot.polling(none_stop=True)
            time.sleep(1)
        except Exception as e:
            print(e, " бот попытался умереть")
