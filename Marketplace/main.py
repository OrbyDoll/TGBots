import math
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import pathlib
import sys
import config as cfg
import markups as nav
from dbshka import Database
from garantDB import GarantDB

storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=storage)
script_dir = pathlib.Path(sys.argv[0]).parent
db = Database(script_dir / cfg.db_file)
garantDB = GarantDB(script_dir / cfg.garantDB_file)


class ClientState(StatesGroup):
    START = State()
    CREATEOFFER_CATEGORY = State()
    CREATEOFFER_NAME = State()
    CREATEOFFER_PRICE = State()
    CHOOSESORTTYPE = State()
    CHOOSEPRODUCT_CATEGORY = State()
    DELETEPRODUCT_CATEGORY = State()
    CHANGEPRICE = State()
    DESCRIBEDENY = State()
    ADMINDELETE = State()
    BAN = State()
    # UNBAN = State()
    BALANCE_USER = State()
    BALANCE_SUMM = State()
    NEWSLETTER = State()
    SORT = State()


async def delete_msg(message, count):
    for i in range(count):
        try:
            await bot.delete_message(message.chat.id, message.message_id - i)
        except:
            pass


def checkAvailability(text):
    if "_" in text or "/" in text:
        return False
    return True


async def checkMember(
    userid,
):
    chat_member = await bot.get_chat_member(cfg.required_chat_id, userid)
    if chat_member.status == "left":
        return False
    return True


def check_category(category):
    category_mass = [
        "Теги",
        "Деф",
        "Услуги",
        "Материалы",
        "Софт",
        "Боты",
        "Сайты",
        "Мануалы",
        "Документы",
        "Другое",
    ]
    for categ in category_mass:
        if categ == category:
            return True
    return False


def sortOffers(mass: list, increase):
    if increase == "increase":
        mass.sort(key=lambda x: int(x.split("_")[2]), reverse=True)
    elif increase == "decrease":
        mass.sort(key=lambda x: int(x.split("_")[2]))
    return mass


db.create_tables()


@dp.message_handler(commands=["start"])
async def start(message: types.Message, state: FSMContext):
    try:
        if message.chat.type == "private":
            await state.update_data(username=message.from_user.username)
            await state.set_state(ClientState.START)
            if not await checkMember(message.chat.id):
                await bot.send_message(
                    message.chat.id,
                    f"Для доступа к боту необходимо подписаться на канал!",
                    reply_markup=nav.channel_url,
                )
                await state.set_state(ClientState.START)
                return      
            print(message)
            if not garantDB.user_exists(message.chat.id):
                await bot.send_message(
                    message.chat.id,
                    "Для доступа к этому боту необходимо нажать на старт в нашем гарант боте💎",
                    reply_markup=nav.garant_check
                )
                return
            elif garantDB.check_ban(message.chat.id) == "1":
                await bot.send_message(
                    message.chat.id, "❌К сожалению вы получили блокировку❌"
                )
                return
            balance = garantDB.get_balance(message.chat.id)[0]
            if not db.user_exists(message.chat.id):
                db.add_user(message.chat.id, float(balance), message.from_user.username)
            db.set_balance(message.chat.id, float(balance))
            await bot.send_message(
                message.chat.id,
                f"Приветствуем, @{message.from_user.username}!🙋\n\n🫂 Добро пожаловать в крупнейший в индустрии рынок воркеров, который гарантирует вам быстрый и удобный доступ ко всем существующим на сегодняшний день услугам.\n\n📈<a href='https://t.me/pradamarketplace_bot'> PRADA | MARKETPLACE</a> - единственная в своем роде торговая площадка позволяющая воркерам всех категорий публиковать свои товары <b>вне зависимости от стоимости</b>, актуальности и прочих факторов гарантируя обоим сторонам безопасное проведение сделки.\n\n👉 Комиссия за проведение купли-продажи всех товаров и услуг является фиксированной и <b>взимается автоматически нашим гарантом.</b>\n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими!</a>",
                parse_mode="html",
                disable_web_page_preview=True,
                reply_markup=nav.menu,
            )
    except Exception as e:
        print(e, " start")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(commands=["admin"], state=ClientState.all_states)
async def admin(message: types.Message, state: FSMContext):
    if (
        message.from_user.id == cfg.glav_admin
        or message.from_user.id == cfg.debug_admin
        or message.from_user.id == cfg.admin3
    ):
        await bot.send_message(
            message.chat.id,
            f"Вы авторизованы, {message.from_user.username}",
            reply_markup=nav.admin_panel,
        )


@dp.callback_query_handler(state=ClientState.all_states)
async def callback_message(call: types.CallbackQuery, state: FSMContext):
    chatid = call.message.chat.id
    await bot.answer_callback_query(callback_query_id=call.id)
    if garantDB.user_exists(chatid):
        if garantDB.check_ban(chatid) == "1":
            await bot.send_message(chatid, "❌К сожалению вы получили блокировку❌")
            return
    try:
        if "buy_" in call.data:
            balance = garantDB.get_balance(chatid)[0]
            db.set_balance(chatid, float(balance))
            if int(call.data.split()[1]) == chatid:
                await bot.send_message(chatid, "❌Нельзя купить свой товар❌")
                await state.set_state(ClientState.START)
                return
            elif int(db.get_user(chatid)[1]) < int(call.data.split()[3]):
                await bot.send_message(
                    chatid,
                    f"❌Недостаточно денег на балансе. Ваш баланс {db.get_user(chatid)[1]} USDT❌",
                )
                await state.set_state(ClientState.START)
                return
            await state.update_data(seller_id=call.data[4:])
            await bot.send_message(
                chatid,
                "🔔Вы уверены что хотите купить этот товар? Потом это действие нельзя будет отменить🔔",
                reply_markup=nav.buy_choose,
            )
        elif call.data == "newsletter":
            await bot.send_message(
                chatid,
                "Введите текст для рассылки. Для отмены введите '-' без кавычек",
            )
            await state.set_state(ClientState.NEWSLETTER)
        elif call.data == "edit_balance":
            await bot.send_message(
                chatid,
                "Введите ник пользователя, баланс которого вы хотите поменять. Для отмены введите '-' без кавычек",
            )
            await state.set_state(ClientState.BALANCE_USER)
        elif call.data == "stats":
            await bot.send_message(
                chatid, db.stats(garantDB.getOffersNumber()), reply_markup=nav.hide
            )
        elif call.data == "bor":
            await bot.send_message(
                chatid, "Выберите, что вы хотите сделать", reply_markup=nav.bor
            )
        elif call.data == "ban":
            await delete_msg(call.message, 1)
            await bot.send_message(
                chatid,
                "Пришлите ник человека, которого вы хотите забанить. Для отмены введите '-' без кавычек",
            )
            await state.set_state(ClientState.BAN)
        elif call.data == "unban":
            await delete_msg(call.message, 1)
            all_banned = garantDB.get_all_banned_users()
            if len(all_banned) == 0:
                await bot.send_message(
                    chatid, "Не найдено забаненых пользователей", reply_markup=nav.hide
                )
                return
            for user in all_banned:
                await bot.send_message(
                    chatid,
                    f"Ник: {user[4]}",
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton(
                            "Разбанить", callback_data=f"unban_{user[0]}"
                        )
                    ),
                )
            await bot.send_message(
                chatid,
                f"Найдено {len(all_banned)} пользователей",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        "Скрыть сообщения",
                        callback_data=f"hide_users_{len(all_banned)}",
                    )
                ),
            )
        elif "hide_users" in call.data:
            users_count = int(call.data.split("_")[2])
            await delete_msg(call.message, users_count + 1)
        elif "unban" in call.data:
            desired_user = call.data.split("_")[1]
            garantDB.unban(desired_user)
            await bot.edit_message_text(
                "Пользователь успешно разбанен", chatid, call.message.message_id
            )
        elif call.data == "admin_delete":
            await delete_msg(call.message, 1)
            await bot.send_message(
                chatid,
                "Напишите никнейм пользователя, товары которого вы хотите удалить",
            )
            await state.set_state(ClientState.ADMINDELETE)
        elif call.data == "cancel_admin_del":
            await delete_msg(call.message, 2)
            await state.set_state(ClientState.START)
        elif call.data == "check_products":
            all_products = db.get_all_tempOffers()
            res = True
            for owner_product in all_products:
                owner = owner_product[0]
                for product in owner_product[1].split("/"):
                    if not product == "":
                        res = False
                        product_data = product.split("_")
                        await bot.send_message(
                            chatid,
                            f"Категория: {product_data[0]}\nТовар: {product_data[1]}\nЦена: {product_data[2]}",
                            reply_markup=nav.get_admin_solution_markup(
                                owner, product_data[1]
                            ),
                        )
            if res:
                await bot.send_message(
                    chatid, "Сейчас нет запросов на расмотрение", reply_markup=nav.hide
                )
        elif call.data == "accept_buy":
            state_data = await state.get_data()
            buy_link = state_data["seller_id"]
            await bot.edit_message_text(
                chat_id=chatid,
                text=f"📨Отправьте данный текст нашему гаранту для начала сделки: `{nav.code_link(buy_link.encode())}`📨",
                message_id=call.message.message_id,
                parse_mode="MARKDOWN",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        text="Перейти в гарант бота➡️",
                        url="https://t.me/pradagarant_bot",
                    )
                ),
            )
            await state.set_state(ClientState.START)
        elif call.data == "deny_buy":
            await bot.delete_message(chatid, call.message.message_id)
            await state.set_state(ClientState.START)
            await bot.send_message(chatid, "Выберите действие📋", reply_markup=nav.menu)
        elif call.data == "category_back":
            await bot.delete_message(chatid, call.message.message_id)
            photo = open(f"files/VKM.png", "rb")
            await bot.send_photo(               
                chatid,
                photo=photo,
                caption="Выберете категорию интересующего товара📋",
                reply_markup=nav.categor,
            )
            await state.set_state(ClientState.CHOOSEPRODUCT_CATEGORY)
        elif call.data == "back_name":
            await delete_msg(call.message, 4)
            await bot.send_message(chatid, "Включение меню", reply_markup=nav.menu)
            await state.set_state(ClientState.START)
        elif call.data == "back_price":
            await delete_msg(call.message, 6)
            await bot.send_message(chatid, "Включение меню", reply_markup=nav.menu)
            await state.set_state(ClientState.START)
        elif "service" in call.data:
            await bot.delete_message(chatid, call.message.message_id)
            choosed_service = call.data[8:]
            await bot.send_message(
                chatid,
                nav.prada_service_list[choosed_service]["text"],
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        text="Заказать🛍", callback_data=f"order_{choosed_service}"
                    ),
                    types.InlineKeyboardButton(text="⬅️Назад", callback_data="choose"),
                ),
            )
            await state.set_state(ClientState.START)
        elif call.data == "choose":
            await bot.delete_message(chatid, call.message.message_id)
            await bot.send_message(
                chatid, "Выберите интересующую услугу📋", reply_markup=nav.service_markup
            )
        elif "order" in call.data:
            choosed_service = call.data[6:]
            await bot.send_message(
                chatid,
                nav.prada_service_list[choosed_service]["contacts"],
                reply_markup=nav.hide,
            )
        elif "hide" in call.data:
            if call.data[-1] == "2":
                await delete_msg(call.message, 2)
            else:
                await delete_msg(call.message, 1)
        elif "del" in call.data:
            offer_str = call.data[4:]
            await bot.edit_message_text(
                "🔔Вы уверены? Это действие нельзя будет отменить",
                chatid,
                call.message.message_id,
            )
            await bot.edit_message_reply_markup(
                chatid,
                call.message.message_id,
                call.message.message_id,
                types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        text="Удалить🗑", callback_data=f"confirm_{offer_str}_yes"
                    ),
                    types.InlineKeyboardButton(
                        text="Отмена⛔️", callback_data=f"confirm_{offer_str}_no"
                    ),
                ),
            )
        elif call.data == "close_msg":
            state_data = await state.get_data()
            for i in range(state_data["opened_msgs"] + 2):
                await bot.delete_message(chatid, call.message.message_id - i)
        elif call.data == "check_member_channel":
            if await checkMember(chatid):
                await bot.delete_message(chatid, call.message.message_id)
                if not garantDB.user_exists(call.message.chat.id):
                    await bot.send_message(
                        call.message.chat.id,
                        "Для доступа к этому боту необходимо нажать на старт в нашем гарант боте💎",
                        reply_markup=nav.garant_check,
                    )
                    return
                elif garantDB.check_ban(chatid) == "1":
                    await bot.send_message(
                        chatid, "❌К сожалению вы получили блокировку❌"
                    )
                    return
                state_data = await state.get_data()
                username = state_data["username"]
                await bot.send_message(
                    chatid,
                    f"Приветствуем, @{username}!🙋\n\n🫂 Добро пожаловать в крупнейший в индустрии рынок воркеров, который гарантирует вам быстрый и удобный доступ ко всем существующим на сегодняшний день услугам.\n\n📈 PRADA | MARKETPLACE (https://t.me/pradamarketplace_bot) - единственная в своем роде торговая площадка позволяющая воркерам всех категорий публиковать свои товары <b>вне зависимости от стоимости</b>, актуальности и прочих факторов гарантируя обоим сторонам безопасное проведение сделки.\n\n👉 Комиссия за проведение купли-продажи всех товаров и услуг является фиксированной и <b>взамается автоматически нашим гарантом.</b>\n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими!</a>",
                    parse_mode="html",
                    disable_web_page_preview=True,
                    reply_markup=nav.menu,
                )
                balance = garantDB.get_balance(call.message.chat.id)[0]
                if not db.user_exists(call.message.chat.id):
                    db.add_user(call.message.chat.id, float(balance), username)
                db.set_balance(call.message.chat.id, float(balance))
        elif call.data == "check_member_garant":
            if garantDB.user_exists(call.message.chat.id):
                await bot.delete_message(chatid, call.message.message_id)
                if garantDB.check_ban(chatid) == "1":
                    await bot.send_message(
                        chatid, "❌К сожалению вы получили блокировку❌"
                    )
                    return
                state_data = await state.get_data()
                username = state_data["username"]
                await bot.send_message(
                    chatid,
                    f"Приветствуем, @{username}!🙋\n\n🫂 Добро пожаловать в крупнейший в индустрии рынок воркеров, который гарантирует вам быстрый и удобный доступ ко всем существующим на сегодняшний день услугам.\n\n📈<a href='https://t.me/pradamarketplace_bot'> PRADA | MARKETPLACE</a> - единственная в своем роде торговая площадка позволяющая воркерам всех категорий публиковать свои товары <b>вне зависимости от стоимости</b>, актуальности и прочих факторов гарантируя обоим сторонам безопасное проведение сделки.\n\n👉 Комиссия за проведение купли-продажи всех товаров и услуг является фиксированной и <b>взимается автоматически нашим гарантом.</b>\n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими!</a>",
                    parse_mode="html",
                    disable_web_page_preview=True,
                    reply_markup=nav.menu,
                )
                balance = garantDB.get_balance(call.message.chat.id)[0]
                if not db.user_exists(call.message.chat.id):
                    db.add_user(call.message.chat.id, float(balance), username)
                db.set_balance(call.message.chat.id, float(balance))
        elif "confirm" in call.data:
            data_split = call.data.split("_")
            offer_data = data_split[1].split("/")
            if data_split[2] == "no":
                await bot.edit_message_text(
                    f"💼Категория: {offer_data[0]}\n📦Товар: {offer_data[1]}\n💲Цена: {offer_data[2]} USDT",
                    chatid,
                    call.message.message_id,
                )
                await bot.edit_message_reply_markup(
                    chatid,
                    call.message.message_id,
                    call.message.message_id,
                    nav.get_offer_del_button(data_split[1], 1),
                )
                return
            if len(offer_data) == 4:
                chatid = offer_data[3]
                offer_data.pop(3)
            db.del_offer_products(chatid, offer_data)
            await bot.edit_message_text(
                "Товар удален✔️",
                call.message.chat.id,
                call.message.message_id,
            )
        elif "cp" in call.data:
            offer_str = call.data.split("_")[1]
            await bot.send_message(chatid, "📝Напишите новую цену")
            await state.update_data(
                changeprice_dict={
                    "offer_str": offer_str,
                    "message_id": call.message.message_id,
                }
            )
            await state.set_state(ClientState.CHANGEPRICE)
        elif "ap" in call.data:
            add_info = call.data[3:].split("_")
            user_temps = db.get_user_tempOffers(add_info[0])[0].split("/")
            user_temps.pop(0)
            for temp_product in user_temps:
                temp_data = temp_product.split("_")
                if temp_data[1] == add_info[1]:
                    db.del_tempOffer_products(add_info[0], temp_data)
                    db.add_offer(add_info[0], temp_data)
                    break
            await bot.delete_message(chatid, call.message.message_id)
            await bot.send_message(
                add_info[0],
                "Админ одобрил добавление вашего товара✔️",
                reply_markup=nav.hide,
            )
        elif "dp" in call.data:
            product_owner_id = call.data[3:].split("_")[0]
            await state.update_data(product_owner_id=product_owner_id)
            await state.update_data(product_name_del=call.data[3:].split("_")[1])
            await bot.delete_message(chatid, call.message.message_id)
            await bot.send_message(chatid, "Напишите причину отказа")
            await state.set_state(ClientState.DESCRIBEDENY)
        # elif "sort" in call.data:
        # try:
        #     state_data = await state.get_data()
        #     choosed_category = state_data["choosed_category"]
        #     all_offers = db.get_all_offers()
        #     res = False
        #     for user_offers in all_offers:
        #         owner_id = user_offers[0]
        #         user_offers_list = sortOffers(
        #             user_offers[1].split("/"), call.data[5:]
        #         )
        #         for offer in user_offers_list:
        #             if not offer == "":
        #                 offer_list = offer.split("_")
        #                 product_category = offer_list[0]
        #                 product_name = offer_list[1]
        #                 product_price = offer_list[2]
        #                 buy_link = f"offer {owner_id} {chatid} {product_price} m"
        #                 if choosed_category == product_category:
        #                     res = True
        #                     await bot.send_message(
        #                         chatid,
        #                         f"💼Категория: {product_category}\n📦Товар: {product_name}\nАвтор: {owner_id}\n💲Цена: {product_price} USDT",
        #                         reply_markup=nav.get_offer_buy_button(buy_link),
        #                     )
        #     if not res:
        #         await bot.send_message(
        #             chatid,
        #             "Товаров в данной категории не найдено❌.",
        #             reply_markup=nav.menu,
        #         )
        #     else:
        #         await bot.send_message(chatid, "🏆", reply_markup=nav.menu)
        #     await state.set_state(ClientState.START)
        # except Exception as e:
        #     print(e, " sort")
        #     print(e.args)
        #     await bot.send_message(chatid, "Что-то пошло не так⛔️")
    except Exception as e:
        print(e, " callback ", call.data)
        await bot.send_message(chatid, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.NEWSLETTER)
async def balanceUser(message: types.Message, state: FSMContext):
    try:
        await delete_msg(message, 2)
        if message.text == "-":
            await state.set_state(ClientState.START)
            return
        info = db.get_all_users()
        await bot.send_message(message.chat.id, text="✅ Рассылка начата!")
        for i in range(len(info)):
            try:
                time.sleep(1)
                await bot.send_message(info[i][0], str(message.text))
            except:
                pass
        await bot.send_message(message.chat.id, text="✅ Рассылка завершена!")
        await state.set_state(ClientState.START)
    except Exception as e:
        print(e, " newsletter")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.BALANCE_USER)
async def balanceUser(message: types.Message, state: FSMContext):
    try:
        await delete_msg(message, 2)
        if message.text == "-":
            await state.set_state(ClientState.START)
            return
        user = db.get_user_from_nick(message.text)
        if user == None:
            await bot.send_message(
                message.chat.id,
                'Пользователь не найден. Попробуйте еще раз или введите "-" для отмены',
            )
            return
        await state.update_data(edit_balance_user=user)
        await bot.send_message(
            message.chat.id,
            f"Пользователь: {user[2]}\nБаланс: {user[1]}\n\nВведите новый баланс или напишите '-' для отмены",
        )
        await state.set_state(ClientState.BALANCE_SUMM)
    except Exception as e:
        print(e, " balance user")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.BALANCE_SUMM)
async def balanceSumm(message: types.Message, state: FSMContext):
    try:
        await delete_msg(message, 2)
        if message.text == "-":
            await state.set_state(ClientState.START)
            return
        try:
            new_balance = int(message.text)
        except:
            await bot.send_message(
                message.chat.id, 'Введите число или напишите "-" для отмены'
            )
            return
        state_data = await state.get_data()
        user = state_data["edit_balance_user"]
        db.set_balance(user[0], new_balance)
        garantDB.set_balance(user[0], new_balance)
        await bot.send_message(
            message.chat.id, "Баланс успешно изменен", reply_markup=nav.hide
        )
        await state.set_state(ClientState.START)
    except Exception as e:
        print(e, " balance summ")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.BAN)
async def ban(message: types.Message, state: FSMContext):
    try:
        await delete_msg(message, 2)
        if message.text == "-":
            await state.set_state(ClientState.START)
            return
        user = db.get_user_from_nick(message.text)
        if user == None:
            await bot.send_message(
                message.chat.id,
                'Пользователь не найден. Попробуйте еще раз или введите "-" для отмены',
            )
            return
        garantDB.ban(user[0])
        await bot.send_message(
            message.chat.id,
            f"Пользователь {message.text} забанен.",
            reply_markup=nav.hide,
        )
        await state.set_state(ClientState.START)
    except Exception as e:
        print(e, " ban")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


# @dp.message_handler(state=ClientState.UNBAN)
# async def ban(message: types.Message, state: FSMContext):
#     try:
#         await delete_msg(message, 2)
#         if message.text == "-":
#             await state.set_state(ClientState.START)
#             return
#         user = db.get_user_from_nick(message.text)
#         if user == None:
#             await bot.send_message(
#                 message.chat.id,
#                 'Пользователь не найден. Попробуйте еще раз или введите "-" для отмены',
#             )
#             return
#         garantDB.unban(user[0])
#         await bot.send_message(
#             message.chat.id,
#             f"Пользователь {message.text} разбанен.",
#             reply_markup=nav.hide,
#         )
#         await state.set_state(ClientState.START)
#     except Exception as e:
#         print(e, " unban")
#         await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.DESCRIBEDENY)
async def describeDeny(message: types.Message, state: FSMContext):
    try:
        describe = message.text
        state_data = await state.get_data()
        product_owner_id = state_data["product_owner_id"]
        product_name = state_data["product_name_del"]
        user_temps = db.get_user_tempOffers(product_owner_id)[0].split("/")
        user_temps.pop(0)
        for temp_product in user_temps:
            temp_data = temp_product.split("_")
            if temp_data[1] == product_name:
                db.del_tempOffer_products(product_owner_id, temp_data)
                break
        await bot.send_message(
            product_owner_id,
            f"Админ отклонил добавление вашего товара по причине:\n{describe}",
            reply_markup=nav.hide,
        )
        await delete_msg(message, 2)
        await state.set_state(ClientState.START)
    except Exception as e:
        print(e, " describe deny")
        await bot.send_message(cfg.glav_admin, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.ADMINDELETE)
async def adminDelete(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(message.chat.id, message.message_id - 1)
        user_info = db.get_user_from_nick(message.text)
        if user_info == None:
            await bot.send_message(
                message.chat.id,
                "Пользователь не найден. Попробуйте еще раз",
                reply_markup=nav.cancel_admin_del,
            )
            return
        userid = user_info[0]
        if db.get_user_offers(userid) == None:
            await bot.send_message(
                message.chat.id,
                "У этого пользователя нет активных предложений. Попробуйте еще раз",
                reply_markup=nav.cancel_admin_del,
            )
            return
        elif db.get_user_offers(userid)[0] == "":
            await bot.send_message(
                message.chat.id,
                "У этого пользователя нет активных предложений. Попробуйте еще раз",
                reply_markup=nav.cancel_admin_del,
            )
            return
        user_offers = db.get_user_offers(userid)[0].split("/")
        await state.update_data(opened_msgs=len(user_offers) - 1)
        for offer in user_offers:
            if not offer == "":
                offer_list = offer.split("_")
                product_category = offer_list[0]
                product_name = offer_list[1]
                product_price = offer_list[2]
                del_link = f"{product_category}/{product_name}/{product_price}/{userid}"
                await bot.send_message(
                    message.chat.id,
                    f"💼Категория: {product_category}\n📦Товар: {product_name}\n💲Цена: {product_price} USDT",
                    reply_markup=nav.get_offer_del_button(del_link, 0),
                )
        await bot.send_message(
            message.chat.id,
            "🏆",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text="Скрыть⬆️", callback_data="close_msg")
            ),
        )
        await state.set_state(ClientState.START)

    except Exception as e:
        print(e, " admin delete")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.CHANGEPRICE)
async def changePrice(message: types.Message, state: FSMContext):
    try:
        try:
            new_price = int(message.text)
        except:
            await bot.send_message(message.chat.id, "Введите число⛔️")
            return
        state_data = await state.get_data()
        product_data = state_data["changeprice_dict"]["offer_str"].split("/")
        message_id = state_data["changeprice_dict"]["message_id"]
        await bot.edit_message_text(
            f"💼Категория: {product_data[0]}\n📦Товар: {product_data[1]}\n💲Цена: {new_price} USDT",
            message.chat.id,
            message_id,
        )
        await bot.edit_message_reply_markup(
            message.chat.id,
            message_id,
            message_id,
            nav.get_offer_del_button(state_data["changeprice_dict"]["offer_str"], 1),
        )
        db.update_price(
            message.chat.id, state_data["changeprice_dict"]["offer_str"], new_price
        )
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.delete_message(message.chat.id, message.message_id - 1)
        await state.set_state(ClientState.START)
    except Exception as e:
        print(e, "change price")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.CHOOSEPRODUCT_CATEGORY)
async def chooseProduct(message: types.Message, state: FSMContext):
    try:
        chatid = message.chat.id
        if message.text == "⬅️Назад":
            await delete_msg(message, 3)
            await bot.send_message(message.chat.id, "🏆", reply_markup=nav.menu)
            await state.set_state(ClientState.START)
            return
        elif message.text == "PRADA🏆":
            await bot.send_message(
                message.chat.id,
                "Выберите интересующую услугу",
                reply_markup=nav.service_markup,
            )
            return
        choosed_category = message.text[:-1]
        photo = open(f"files/{choosed_category}.png", "rb")
        await bot.send_photo(
            chatid,
            photo=photo,
        )
        await state.update_data(choosed_category=message.text[:-1])
        all_offers = db.get_all_offers()
        msgs = []
        text_for_sort = []
        res = False
        for user_offers in all_offers:
            owner_id = user_offers[0]
            user_offers_list = user_offers[1].split("/")
            for offer in user_offers_list:
                if not offer == "":
                    offer_list = offer.split("_")
                    product_category = offer_list[0]
                    product_name = offer_list[1]
                    product_price = offer_list[2]
                    buy_link = f"offer {owner_id} {chatid} {product_price} m"
                    if choosed_category == product_category:
                        res = True
                        msg = await bot.send_message(
                            chatid,
                            f"💼Категория: {product_category}\n📦Товар: {product_name}\nАвтор: {owner_id}\n💲Цена: {product_price} USDT",
                            reply_markup=nav.get_offer_buy_button(buy_link),
                        )
                        text_for_sort.append(f"{offer}_{owner_id}")
                        msgs.append(msg)
        if not res:
            await bot.send_message(
                chatid,
                "Товаров в данной категории не найдено❌.",
                reply_markup=nav.menu,
            )
            await state.set_state(ClientState.START)
        else:
            await state.update_data(msgs=msgs)
            await state.update_data(text_for_sort=text_for_sort)
            await bot.send_message(chatid, "🏆", reply_markup=nav.sort_choose)
            await state.set_state(ClientState.SORT)

        # await bot.send_message(
        #     message.chat.id, "Выберите вариант сортировки", reply_markup=nav.sort_choose
        # )
        # await state.set_state(ClientState.START)
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.SORT)
async def setAuctionCategory(message: types.Message, state: FSMContext):
    try:
        state_data = await state.get_data()
        messages = state_data["msgs"]
        if message.text == "⬅️Назад":
            await delete_msg(message, 1)
            for msg in messages:
                await delete_msg(msg, 1)
            await bot.send_message(
                message.chat.id, "Включение меню", reply_markup=nav.menu
            )
            await state.set_state(ClientState.START)
        elif message.text == "Сначала дорогие📈" or message.text == "Сначала дешевые📉":
            await delete_msg(message, 1)
            if message.text == "Сначала дорогие📈":
                sort_type = "increase"
            else:
                sort_type = "decrease"
            for msg in messages:
                await delete_msg(msg, 1)
            msgs = []
            choosed_category = state_data["choosed_category"]
            unsorted_list = state_data["text_for_sort"]
            user_offers_list = sortOffers(unsorted_list, sort_type)
            for offer in user_offers_list:
                offer_list = offer.split("_")
                product_category = offer_list[0]
                product_name = offer_list[1]
                product_price = offer_list[2]
                owner_id = offer_list[3]
                buy_link = f"offer {owner_id} {message.chat.id} {product_price} m"
                if choosed_category == product_category:
                    msg = await bot.send_message(
                        message.chat.id,
                        f"💼Категория: {product_category}\n📦Товар: {product_name}\nАвтор: {owner_id}\n💲Цена: {product_price} USDT",
                        reply_markup=nav.get_offer_buy_button(buy_link),
                    )
                    msgs.append(msg)
            await state.update_data(msgs=msgs)
    except Exception as e:
        print(e, "get auctions")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.CREATEOFFER_CATEGORY)
async def createOffer(message: types.Message, state: FSMContext):
    try:
        if message.text == "⬅️Назад":
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.send_message(message.chat.id, "🏆", reply_markup=nav.menu)
            await state.set_state(ClientState.START)
            return
        elif not check_category(message.text[:-1]):
            photo = open(f"files/VKM.png", "rb")
            await bot.send_photo(               
                message.chatid,
                photo=photo,
                caption="Выберите одну из предложенных категорий📋",
                reply_markup=nav.categor_without_prada,
            )
            return
        await state.update_data(product_category=message.text[:-1])
        await bot.send_message(
            message.chat.id,
            "Напишите краткое описание вашего товара✏️",
            reply_markup=nav.back_from_name,
        )
        await state.set_state(ClientState.CREATEOFFER_NAME)
    except Exception as e:
        print(e, " create offer 2")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.CREATEOFFER_NAME)
async def createOffer(message: types.Message, state: FSMContext):
    try:
        if not checkAvailability(message.text):
            await bot.send_message(
                message.chat.id,
                'Символы "_" "/" запрешены. Введите новое название для вашего товара.',
            )
            return
        await state.update_data(product_name=message.text)
        await bot.send_message(
            message.chat.id,
            "Напишите стоимость вашего товара в USDT💲",
            reply_markup=nav.back_from_price,
        )
        await state.set_state(ClientState.CREATEOFFER_PRICE)
    except Exception as e:
        print(e, " create offer 3")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.CREATEOFFER_PRICE)
async def createOffer(message: types.Message, state: FSMContext):
    try:
        if db.get_user_offers(message.chat.id) == None:
            db.insert_offer_owner(message.chat.id)
        if db.get_user_tempOffers(message.chat.id) == None:
            db.insert_owner_temp(message.chat.id)
        try:
            product_price = int(message.text)
            product_price = str(product_price)
        except:
            await bot.send_message(message.chat.id, "Введите число⛔️")
            return
        await delete_msg(message, 7)
        state_data = await state.get_data()
        product_category = state_data["product_category"]
        product_name = state_data["product_name"]
        add_link = (
            f"{message.chat.id}_{product_category}_{product_name}_{product_price}"
        )
        await bot.send_message(message.chat.id, "Включение меню", reply_markup=nav.menu)
        await bot.send_message(
            message.chat.id,
            "Ваш товар отправлен на рассмотрение, ожидайите в течение 10-15 минут.",
            reply_markup=nav.hide,
        )
        db.add_tempOffer(
            message.chat.id, [product_category, product_name, product_price]
        )
        await state.set_state(ClientState.START)
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(content_types=["text"], state=ClientState.all_states)
async def textHandler(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    if not await checkMember(message.chat.id):
        await bot.send_message(
            message.chat.id,
            f"Для доступа к каналу необходимо подписаться на канал!",
            reply_markup=nav.channel_url,
        )
        await state.set_state(ClientState.START)
        return
    if garantDB.check_ban(chatid) == "1":
        await bot.send_message(chatid, "К сожалению вы получили блокировку⛔️")
        return
    if message.text == "Создать товар📝":
        try:
            if (
                len(db.get_user_offers(chatid)[0].split("/"))
                + len(db.get_user_tempOffers(chatid)[0].split("/"))
                > 7
            ):
                await bot.send_message(
                    chatid,
                    f"Товаров не может быть больше 7⛔️\nУ вас {len(db.get_user_offers(chatid)[0].split('/'))} активных товара и {len(db.get_user_tempOffers(chatid)[0])} товара на расмотрении",
                )
                return
        except:
            pass
        photo = open(f"files/VKM.png", "rb")
        await bot.send_photo(               
            chatid,
            photo=photo,
            caption="К какой категории относиться ваш товар?📦",
            reply_markup=nav.categor_without_prada,
        )
        await state.set_state(ClientState.CREATEOFFER_CATEGORY)
    elif message.text == "Выбрать товар📋":
        photo = open(f"files/VKM.png", "rb")
        await bot.send_photo(               
            chatid,
            photo=photo,
            caption="Выберите категорию💼", reply_markup=nav.categor)
        await state.set_state(ClientState.CHOOSEPRODUCT_CATEGORY)
    elif message.text == "О нас🌟":
        deals_number = garantDB.getOffersNumber()
        gm_deals_number = deals_number["g-m"]
        a_deals_number = deals_number["a"]
        deals_summ = garantDB.getOffersSumm()
        gm_deals_summ = math.ceil(deals_summ["g-m"])
        a_deals_summ = math.ceil(deals_summ["a"])
        photo = open(f"files/AUM.png", "rb")
        await bot.send_photo(               
            chatid,
            photo=photo,
            caption=f"⚡️<a href='https://t.me/pradamarketplace_bot'>PRADA | MARKETPLACE</a> - единственная в своем роде торговая площадка позволяющая воркерам всех категорий публиковать свои товары <b>вне зависимости от стоимости,</b> актуальности и прочих факторов гарантируя обоим сторонам безопасное проведение сделки.\n\n🤝Мы работаем на базе <a href='https://t.me/pradagarant_bot'>PRADA | GARANT</a><b> - системе защиты от мошенников,</b> позволяющей вам забыть обо всех нюансах торговли в сети и наслаждаться <b>безопасной продажей/покупкой любых товаров и услуг.</b>\n\n💠Система оплаты происходит напрямую через <i>@CryptoBot,</i> что гарантирует <b>сохранность ваших средств</b> и полную <b>конфиденциальность сделок.</b> \n\n💵Все суммы сделок считаются в долларах <b>(USD)</b>, а все сделки проходят в <b>криптовалюте USDT (TRC20)</b>, без возможности перехода оплаты на другую криптовалюту.\n\n🦾Для улучшения работы бота или по любым другим вопросам вы <b>всегда можете обратиться в нашу круглосуточную поддержку </b>- @pradamarketplace_sup. Мы всегда <b>рады обратной связи</b> и готовы <b>реализовать любые ваши пожелания.</b> \n\n 🗓 Дата открытия проекта - <b>12.10.2023. </b>",
            parse_mode="html",
            reply_markup=nav.o_nas,
        )
    elif message.text == "Мои товары🛍":
        try:
            if db.get_user_offers(chatid) == None:
                await bot.send_message(chatid, "У вас нет активных предложений❌")
                return
            elif db.get_user_offers(chatid)[0] == "":
                await bot.send_message(chatid, "У вас нет активных предложений❌")
                return
            user_offers = db.get_user_offers(message.chat.id)[0].split("/")
            await state.update_data(opened_msgs=len(user_offers) - 1)
            for offer in user_offers:
                if not offer == "":
                    offer_list = offer.split("_")
                    product_category = offer_list[0]
                    product_name = offer_list[1]
                    product_price = offer_list[2]
                    del_link = f"{product_category}/{product_name}/{product_price}"
                    await bot.send_message(
                        message.chat.id,
                        f"💼Категория: {product_category}\n📦Товар: {product_name}\n💲Цена: {product_price} USDT",
                        reply_markup=nav.get_offer_del_button(del_link, 1),
                    )
            await bot.send_message(
                message.chat.id,
                "🏆",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        text="Скрыть⬆️", callback_data="close_msg"
                    )
                ),
            )
        except Exception as e:
            print(e, " my products ")
            await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
