import math
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import aiogram.utils.markdown as fmt
import sys
import pathlib
import config as cfg
import markups as nav
from dbshka import Database
from garantDB import GarantDB


class ClientState(StatesGroup):
    START = State()
    GETAUCTIONS = State()
    SETAUCTIONCATEGORY = State()
    SETAUCTIONPRODUCT = State()
    SETAUCTIONDESCRIPTION = State()
    FINSIHCREATEAUCTION = State()
    AUCTIONOWNER = State()
    OFFERRATE = State()
    CHANGESTARTCOST = State()
    AUTOSTART = State()
    DESCRIBEDENY = State()
    BAN = State()
    UNBAN = State()
    BALANCE_USER = State()
    BALANCE_SUMM = State()
    NEWSLETTER = State()
    SORT = State()


storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=storage)
script_dir = pathlib.Path(sys.argv[0]).parent
db = Database(script_dir / cfg.db_file)
garantDB = GarantDB(script_dir / cfg.garantDB_file)

db.create_tables()
garantDB.create_table()


async def delete_msg(message, count):
    for i in range(count):
        try:
            await bot.delete_message(message.chat.id, message.message_id - i)
        except:
            pass


async def send_all(users_id, auction_id):
    last_rates = ""
    auction_info = db.get_auction(auction_id)
    for i in range(len(users_id)):
        user_info = db.get_prev_rate(users_id[i])[0]
        last_rates += f'\n👤Участник {i + 1}: {user_info if user_info == "Ставка не сделана⏱" else user_info + " USDT💸"}\n'
    for user_id in users_id:
        user_info_msg = db.get_info_message_id(user_id)[0]
        try:
            await bot.edit_message_text(
                text=f"Вы присоединились к аукциону✅\n\nСостояние аукциона: {auction_info[6]}\n\nКоличество участников: {auction_info[1]}\nПоследние ставки участников: {last_rates}",
                chat_id=user_id,
                message_id=user_info_msg,
            )
        except:
            pass
    try:
        await bot.edit_message_text(
            text=f"Ваш аукцион.\nСостояние аукциона: {auction_info[6]}\nКоличество участников: {auction_info[1]}\nПоследние ставки участников: {last_rates}",
            chat_id=auction_id,
            message_id=db.get_info_message_id(auction_id)[0],
        )
    except:
        pass


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


async def checkMember(
    userid,
):
    # chat_member = await bot.get_chat_member(cfg.required_chat_id, userid)
    # if chat_member.status == "left":
    #     return False
    return True


def sortAuctions(mass: list, increase):
    if increase == "increase":
        mass.sort(key=lambda x: int(x[5]), reverse=True)
    elif increase == "decrease":
        mass.sort(key=lambda x: int(x[5]))
    return mass


@dp.message_handler(commands=["start"])
async def start(message: types.Message, state: FSMContext):
    try:
        if message.chat.type == "private":
            await state.update_data(username=message.from_user.username)
            if not await checkMember(message.chat.id):
                await bot.send_message(
                    message.chat.id,
                    f"Для доступа к боту необходимо подписаться на канал!",
                    reply_markup=nav.channel_url,
                )
                await state.set_state(ClientState.START)
                return
            elif not garantDB.user_exists(message.chat.id):
                await bot.send_message(
                    message.chat.id,
                    "Для доступа к этому боту необходимо нажать на старт в нашем гарант боте💎",
                    reply_markup=nav.garant_check,
                )
                return
            elif garantDB.check_ban(message.chat.id) == "1":
                await bot.send_message(
                    message.chat.id, "❌К сожалению вы получили блокировку❌"
                )
                return
            await bot.send_message(
                message.chat.id,
                f"Приветствуем, @{message.from_user.username}!🙋\nДобро пожаловать внутрь первого в индустрии бота для автоматического проведения аукционов между воркерами.\n\n💎Если вы желаете с интересом провести время и получить лучший товар по лучшей цене - данная ветка проектов для вас.\n\n🤝Мы работаем на базе системы <a href='https://t.me/pradagarant_bot'>PRADA | GARANT</a> - это гарантирует безопасность всех сторону участников аукциона и позволяет забыть о возможности быть обманутым и наслаждаться процессом. \n\n💠Система оплаты происходит напрямую через <i>@CryptoBot,</i> что гарантирует <b>сохранность ваших средств</b> и полную <b>конфиденциальность сделок.</b> \n\n💵Все суммы сделок считаются в долларах <b>(USD)</b>, а все сделки проходят в <b>криптовалюте USDT (TRC20)</b>, без возможности перехода оплаты на другую криптовалюту.\n\n🦾Для улучшения работы бота или по любым другим вопросам вы <b>всегда можете обратиться в нашу круглосуточную поддержку </b>- @pradaaction_sup. Мы всегда <b>рады обратной связи</b> и готовы <b>реализовать любые ваши пожелания.</b>\n\n👉Комиссия за проведение купли-продажи всех товаров и услуг является фиксированной и <b>взамается автоматически нашим гарантом.</b>\n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими!</a>",
                parse_mode="html",
                disable_web_page_preview=True,
                reply_markup=nav.menu,
            )
            await state.update_data(auction_id=None)
            balance = garantDB.get_balance(message.chat.id)[0]
            if not db.user_exists(message.chat.id):
                db.add_user(message.chat.id, float(balance), message.from_user.username)
            db.set_balance(message.chat.id, float(balance))
            await state.update_data(author_id=None)
            await state.set_state(ClientState.START)
    except Exception as e:
        print(e, " start")


@dp.message_handler(commands=["admin"], state=ClientState.all_states)
async def admin(message: types.Message, state: FSMContext):
    if (
        message.chat.id == cfg.glav_admin
        or message.chat.id == cfg.debug_admin
        or message.chat.id == cfg.admin3
    ):
        await bot.send_message(
            message.chat.id,
            f"Вы авторизованы, {message.from_user.username}",
            reply_markup=nav.admin_panel,
        )


@dp.message_handler(state=ClientState.GETAUCTIONS)
async def getAuctions(message: types.Message, state: FSMContext):
    try:
        if message.text == "Назад":
            await delete_msg(message, 3)
            await bot.send_message(
                message.chat.id,
                "Включение меню",
                reply_markup=nav.menu,
            )
            return
        # await bot.delete_message(chat_id=chatid, message_id=call.message.message_id)
        # sort_type = call.data[5:]
        # auction_data = await state.get_data()
        # auction_category = auction_data["desired_category"]
        # all_auctions = sortAuctions(all_auctions_unsorted, sort_type)
        chatid = message.chat.id
        desired_category = message.text[:-1]
        await state.update_data(desired_category=desired_category)
        all_auctions = db.get_all_auctions()
        auctions_markup = nav.get_auctions_buttons(all_auctions, desired_category)
        await state.update_data(auctions_list=auctions_markup)
        if auctions_markup == None:
            await bot.send_message(
                chatid,
                "Сейчас нет активных аукционов этой категории.⛔️",
                reply_markup=nav.menu,
            )
            await state.set_state(ClientState.START)
            return
        msg = await bot.send_message(
            chatid,
            "Выберите интересующий аукцион📊",
            reply_markup=auctions_markup,
        )
        await state.update_data(auctions_msg=msg)
        await bot.send_message(chatid, "🏆", reply_markup=nav.sort_choose)
        await state.set_state(ClientState.SORT)
    # try:
    #         await bot.delete_message(message.chat.id, message.message_id)
    #         await bot.delete_message(message.chat.id, message.message_id - 1)
    #         await bot.delete_message(message.chat.id, message.message_id - 2)
    #         await state.set_state(ClientState.START)
    #         return
    #     await state.update_data(desired_category=message.text[:-1])
    #     # await bot.send_message(
    #     #     message.chat.id,
    #     #     "Выберите вариант сортировки📋",
    #     #     reply_markup=nav.sort_choose,
    #     # )
    except Exception as e:
        print(e, "get auctions")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.SORT)
async def setAuctionCategory(message: types.Message, state: FSMContext):
    try:
        if message.text == "Назад":
            await delete_msg(message, 2)
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
            state_data = await state.get_data()
            auction_message = state_data["auctions_msg"]
            category = state_data["desired_category"]
            all_auctions = db.get_all_auctions()
            sorted_auctions = sortAuctions(all_auctions, sort_type)
            sorted_markup = nav.get_auctions_buttons(sorted_auctions, category)
            try:
                await delete_msg(auction_message, 1)
                await bot.send_message(
                    message.chat.id,
                    "Выберите интересующий аукцион📊",
                    reply_markup=sorted_markup,
                )
                # await bot.edit_message_reply_markup(
                #     chat_id=message.chat.id,
                #     message_id=auction_message.message_id,
                #     reply_markup=sorted_markup,
                # )
            except:
                pass
    except Exception as e:
        print(e, "get auctions")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.SETAUCTIONCATEGORY)
async def setAuctionCategory(message: types.Message, state: FSMContext):
    try:
        if message.text == "Назад":
            await bot.send_message(
                chat_id=message.chat.id,
                text="Включение меню",
                reply_markup=nav.menu,
            )
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.delete_message(message.chat.id, message.message_id - 1)
            await bot.delete_message(message.chat.id, message.message_id - 2)
            await state.set_state(ClientState.START)
            return
        auctionCategory = message.text[:-1]
        if not check_category(auctionCategory):
            await bot.send_message(
                message.chat.id,
                "Выберите одну из предложенных категорий📋",
                reply_markup=nav.categor,
            )
            return
        await state.update_data(product_category=auctionCategory)
        await bot.send_message(
            message.chat.id,
            "Напишите название товара📦",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text="Назад", callback_data="back_2")
            ),
        )
        await state.set_state(ClientState.SETAUCTIONPRODUCT)
    except Exception as e:
        print(e, "set category")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.SETAUCTIONPRODUCT)
async def setAuctionProduct(message: types.Message, state: FSMContext):
    try:
        productName = message.text
        await state.update_data(product_name=productName)
        await bot.send_message(message.chat.id, "Напишите описание вашего товара📝")
        await state.set_state(ClientState.SETAUCTIONDESCRIPTION)
    except Exception as e:
        print(e, "set product")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.SETAUCTIONDESCRIPTION)
async def setAuctionProduct(message: types.Message, state: FSMContext):
    try:
        product_description = message.text
        await state.update_data(product_description=product_description)
        await bot.send_message(
            message.chat.id,
            "Введите начальную ставку для вашего аукциона💸",
        )
        await state.set_state(ClientState.FINSIHCREATEAUCTION)
    except Exception as e:
        print(e, " set description")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.FINSIHCREATEAUCTION)
async def createAuction(message: types.Message, state: FSMContext):
    try:
        try:
            product_cost = int(message.text)
        except:
            await bot.send_message(message.chat.id, "Введите число!")
            return
        auction_data = await state.get_data()
        product_category = auction_data["product_category"]
        product_name = auction_data["product_name"]
        product_description = auction_data["product_description"]
        db.add_auction(
            message.chat.id,
            product_name,
            product_cost,
            product_category,
            product_description,
        )
        db.set_auction_status(message.chat.id, "check")
        await state.update_data(auction_owner=message.chat.id)
        await bot.send_message(
            message.chat.id,
            "Ваш аукцион отправлен на рассмотрение, ожидайите в течение 10-15 минут.",
            reply_markup=nav.hide,
        )
        await bot.send_message(message.chat.id, "Включение меню", reply_markup=nav.menu)
        await state.set_state(ClientState.START)
    except Exception as e:
        print(e, "finish create auction")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.AUTOSTART)
async def autoStart(message: types.Message, state: FSMContext):
    try:
        try:
            members_number = int(message.text)
        except:
            await bot.send_message(message.chat.id, "⛔️Введите целое число!")
            return
        if db.get_auction(message.chat.id)[6] == "active":
            await bot.send_message("⛔️Аукцион уже начат")
        elif members_number < 2:
            await bot.send_message(
                message.chat.id, "⛔️Число участников должно быть больше 1!"
            )
        elif members_number < int(db.get_auction_members(message.chat.id)[0]):
            await bot.send_message(
                message.chat.id,
                f"👥В вашем аукционе {db.get_auction_members(message.chat.id)[0]} участников. \n\n 🔔Введите большее число для авто старта",
            )
        else:
            db.set_autostart(message.chat.id, members_number)
            await bot.send_message(message.chat.id, "Авто старт успешно установлен✅")
            await state.set_state(ClientState.START)

    except Exception as e:
        print(e, " auto start")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.CHANGESTARTCOST)
async def changeStartCost(message: types.Message, state: FSMContext):
    try:
        new_start_cost = int(message.text)
        db.set_start_cost(message.chat.id, new_start_cost)
        members_id = db.get_members_id(message.chat.id)[0].split("/")
        auction_info = db.get_auction(message.chat.id)
        for member in members_id:
            if not member == "":
                await bot.send_message(
                    int(member),
                    f'🛎Была изменена начальная ставка аукциона: №{auction_info[0]}\n📦Товар: {auction_info[4]}\n{"💵Начальная ставка" if auction_info[6] == "inactive" else "💲Текущая ставка"} : {auction_info[2] if auction_info[6] == "inactive" else auction_info[5]}\n👥Участников: {auction_info[1]}\n📢Статус: {auction_info[6]}',
                    reply_markup=nav.member_actions,
                )
        await bot.send_message(message.chat.id, "Начальная ставка успешно изменена✅")
    except Exception as e:
        print(e, "change start cost")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.DESCRIBEDENY)
async def describeDeny(message: types.Message, state: FSMContext):
    try:
        describe = message.text
        state_data = await state.get_data()
        auction_owner = state_data["auction_owner"]
        await bot.send_message(
            auction_owner,
            f"Админ отклонил добавление вашего аукциона по причине:\n{describe}",
            reply_markup=nav.hide,
        )
        db.del_auction(auction_owner)
        await delete_msg(message, 2)
        await state.set_state(ClientState.START)
    except Exception as e:
        print(e, " describe deny")
        await bot.send_message(cfg.glav_admin, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.OFFERRATE)
async def offerRate(message: types.Message, state: FSMContext):
    try:
        if message.text == "Назад":
            await bot.delete_message(message.message_id)
            await bot.delete_message(message.message_id - 1)
            return
        offer = int(message.text)
        user_info = db.get_user(message.chat.id)
        state_data = await state.get_data()
        author_id = state_data["auction_id"]
        auction_info = db.get_auction(author_id)
        if offer > user_info[1]:
            await bot.send_message(
                message.chat.id,
                f"Ставка не может быть больше баланса. Ваш баланс: {user_info[1]}⛔️",
            )
        elif offer <= auction_info[5]:
            await bot.send_message(
                message.chat.id, "Ставка не может быть меньше предыдущей.⛔️"
            )
        else:
            members_id = db.get_members_id(author_id)[0].split("/")
            members_id.pop(0)
            db.set_prev_rate(message.chat.id, offer)
            # await send_all(members_id, author_id)
            for member in members_id:
                if not member == "":
                    await bot.send_message(
                        int(member),
                        f"Ставка поднята до {offer}✅",
                        reply_markup=nav.member_actions,
                    )
            await bot.send_message(
                author_id,
                f"Ставка поднята до {offer}✅",
                reply_markup=nav.accept_offer(message.chat.id),
            )
            db.set_current_cost(author_id, offer)
    except Exception as e:
        print(e, "offer rate")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


# @dp.message_handler(state=ClientState.ADMINDELETE)
# async def adminDelete(message: types.Message, state: FSMContext):
#     try:
#         user_info = db.get_user_from_nick(message.text)
#         if user_info == None:
#             await bot.send_message(
#                 message.chat.id,
#                 "Пользователь не найден. Попробуйте еще раз",
#                 reply_markup=nav.cancel_admin_del,
#             )
#             return
#         userid = user_info[0]
#         if not db.check_active_auction(userid):
#             await bot.send_message(
#                 message.chat.id,
#                 "У этого пользователя нет активных предложений. Попробуйте еще раз",
#                 reply_markup=nav.cancel_admin_del,
#             )
#             return
#         members_id = db.get_members_id(userid)[0].split("/")
#         db.del_auction(userid)
#         for member in members_id:
#             if not member == "":
#                 await bot.send_message(
#                     int(member),
#                     "Аукцион удален. Можно расходиться🗑",
#                     reply_markup=nav.del_auction,
#                 )
#         await bot.delete_message(message.chat.id, message.message_id)
#         await bot.delete_message(message.chat.id, message.message_id - 1)
#         await bot.send_message(
#             userid, "Ваш аукцион был удален админом✅", reply_markup=nav.menu
#         )
#         await state.set_state(ClientState.START)
#     except Exception as e:
#         print(e, "admin delete")
#         await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


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


@dp.message_handler(content_types=["text"], state=ClientState.all_states)
async def writeText(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    if not await checkMember(message.chat.id):
        await bot.send_message(
            message.chat.id,
            f"Для доступа к боту необходимо подписаться на канал!",
            reply_markup=nav.channel_url,
        )
        await state.set_state(ClientState.START)
        return
    if garantDB.check_ban(chatid) == "1":
        await bot.send_message(chatid, "К сожалению вы получили блокировку.")
        return
    if message.text == "Список аукционов ⚖️":
        try:
            state_data = await state.get_data()
            author_id = state_data["auction_id"]
            if db.check_active_auction(chatid) or not author_id == None:
                await bot.send_message(
                    chatid, "Вам необходимо закончить все аукционы!⛔️"
                )
                return
            await bot.send_message(
                chatid, "Выберите категорию", reply_markup=nav.categor
            )
            await state.set_state(ClientState.GETAUCTIONS)
        except Exception as e:
            print(e, " get auctions")
            await bot.send_message(chatid, "Что-то пошло не так⛔️")
    elif message.text == "Создать аукцион 💎":
        try:
            state_data = await state.get_data()
            author_id = state_data["auction_id"]
            if db.check_active_auction(chatid):
                await bot.send_message(chatid, "У вас уже есть аукцион!⛔️")
                return
            if not author_id == None:
                await bot.send_message(
                    chatid, "Вам необходимо закончить все аукционы!⛔️"
                )
                return
            await bot.send_message(
                chatid,
                "🗃 К какой категории относиться ваш товар?",
                reply_markup=nav.categor,
            )
            await state.set_state(ClientState.SETAUCTIONCATEGORY)
        except Exception as e:
            print(e, " create auction")
            await bot.send_message(chatid, "Что-то пошло не так⛔️")
    elif message.text == "Перейти к своему аукциону 🔓":
        try:
            if db.check_active_auction(chatid):
                await bot.send_message(
                    chatid,
                    "Ваш аукцион, ожидайте участников👥",
                    reply_markup=nav.owner_actions,
                )
            else:
                await bot.send_message(chatid, "У вас нет активного аукциона⛔️")
        except Exception as e:
            print(e)
            await bot.send_message(chatid, "Что-то пошло не так⛔️")
    elif message.text == "О нас🌟":
        deals_number = garantDB.getOffersNumber()
        gm_deals_number = deals_number["g-m"]
        a_deals_number = deals_number["a"]
        deals_summ = garantDB.getOffersSumm()
        gm_deals_summ = math.ceil(deals_summ["g-m"])
        a_deals_summ = math.ceil(deals_summ["a"])
        await bot.send_message(
            chatid,
            f"Мы - первое в своем роде <b>средство проведения автоматических и безопасных аукционов</b> внутри комьюнити, гарантирующее вам полную <b>конфиденциальность и безопасность.</b> Мы работаем на основе системы <a href='https://t.me/pradagarant_bot'>PRADA | GARANT</a> для <b>гарантии безопасности</b> всех сторон, а также на базе платежной системы <i>@CryptoBot</i>, а сами сделки проходят в криптовалюте <b>USDT (TRC20)</b>, а значит и ценны соответственно приравниваются к доллару <b>(USD).</b>\n\n🫂Количество сделок гарант-маркет: {gm_deals_number}\n🤑Сумма сделок гарант-маркет: {gm_deals_summ} USDT\n\n🫂Количество сделок аукциона: {a_deals_number}\n🤑Сумма сделок аукциона: {a_deals_summ} USDT",
            parse_mode="html",
            reply_markup=nav.o_nas,
            disable_web_page_preview=True,
        )
    elif message.text == "Информация об аукционе📜":
        try:
            state_data = await state.get_data()
            author_id = (
                chatid if db.check_active_auction(chatid) else state_data["auction_id"]
            )
            auction_info = db.get_auction(author_id)
            last_rates = ""
            users_id = auction_info[7].split("/")
            users_id.pop(0)
            for i in range(len(users_id)):
                user_info = db.get_prev_rate(users_id[i])[0]
                last_rates += f'\nУчастник {i + 1}: {user_info if user_info == "🔔Ставка не сделана" else user_info + " USDT"}\n'
            msg = await bot.send_message(
                chatid,
                f"📰Состояние аукциона: {auction_info[6]}\n\n👥Количество участников: {auction_info[1]}\n\n💸Последние ставки участников: {last_rates}",
                reply_markup=nav.close_info_message,
            )
            db.set_info_message_id(chatid, msg.message_id)
        except Exception as e:
            print(e)
            await bot.send_message(chatid, "Что-то пошло не так⛔️")


@dp.callback_query_handler(state=ClientState.all_states)
async def call_handler(call: types.CallbackQuery, state: FSMContext):
    chatid = call.message.chat.id
    if garantDB.check_ban(chatid) == "1":
        await bot.send_message(chatid, "❌К сожалению вы получили блокировку❌")
        return
    try:
        await bot.answer_callback_query(callback_query_id=call.id)
        if call.data == "newsletter":
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
            all_auctions = db.get_all_auctions()
            if len(all_auctions) == 0:
                await bot.send_message(
                    chatid, "Сейчас нет активных аукционов", reply_markup=nav.hide
                )
                return
            for auction in all_auctions:
                await bot.send_message(
                    chatid,
                    f"Владелец: {db.get_user(auction[3])[2]}\nТовар: {auction[4]}\nОписание: {auction[9]}\nСтатус: {auction[6]}\nСтавка: {auction[5]}",
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton(
                            "Удалить", callback_data=f"aremove_auction_{auction[3]}"
                        )
                    ),
                )
            await bot.send_message(
                chatid,
                f"Найдено {len(all_auctions)} аукционов",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        "Скрыть сообщения",
                        callback_data=f"hide_auctions_{len(all_auctions)}",
                    )
                ),
            )
        elif "hide_auctions" in call.data:
            auction_count = int(call.data.split("_")[2])
            await delete_msg(call.message, auction_count + 1)
        elif call.data == "cancel_admin_del":
            await delete_msg(call.message, 2)
            await state.set_state(ClientState.START)
        elif call.data == "auto_start":
            await bot.send_message(
                chatid,
                "Напишите сколько участников необходимо для автоматическго старта📢",
            )
            await state.set_state(ClientState.AUTOSTART)
        elif call.data == "back_offer_list":
            await bot.delete_message(chatid, call.message.message_id)
            state_data = await state.get_data()
            await bot.send_message(
                chatid,
                "Выберите интересующий аукцион📊",
                reply_markup=state_data["auctions_list"],
            )
        elif call.data == "hide":
            await delete_msg(call.message, 1)
        elif call.data == "check_auctions":
            all_auctions = db.get_all_auctions()
            res = True
            for auction in all_auctions:
                if auction[6] == "check":
                    res = False
                    await bot.send_message(
                        chatid,
                        f"Пользователь: {db.get_user(auction[3])[2]}\nТовар: {auction[4]}\nОписание: {auction[9]}\nЦена: {auction[5]}",
                        reply_markup=nav.get_admin_solution_markup(auction[3]),
                    )
            if res:
                await bot.send_message(chatid, "Сейчас нет запросов на расмотрение")
        elif call.data == "check_member":
            if await checkMember(chatid):
                await bot.delete_message(chatid, call.message.message_id)
                if not garantDB.user_exists(chatid):
                    await bot.send_message(
                        chatid,
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
                    f"Приветствуем, @{username}!🙋\nДобро пожаловать внутрь первого в индустрии бота для автоматического проведения аукционов между воркерами.\n\n💎Если вы желаете с интересом провести время и получить лучший товар по лучшей цене - данная ветка проектов для вас.\n\n🤝Мы работаем на базе системы <a href='https://t.me/pradagarant_bot'>PRADA | GARANT</a> - это гарантирует безопасность всех сторону участников аукциона и позволяет забыть о возможности быть обманутым и наслаждаться процессом. \n\n💠Система оплаты происходит напрямую через <i>@CryptoBot,</i> что гарантирует <b>сохранность ваших средств</b> и полную <b>конфиденциальность сделок.</b> \n\n💵Все суммы сделок считаются в долларах <b>(USD)</b>, а все сделки проходят в <b>криптовалюте USDT (TRC20)</b>, без возможности перехода оплаты на другую криптовалюту.\n\n🦾Для улучшения работы бота или по любым другим вопросам вы <b>всегда можете обратиться в нашу круглосуточную поддержку </b>- @pradaaction_sup. Мы всегда <b>рады обратной связи</b> и готовы <b>реализовать любые ваши пожелания.</b>\n\n👉Комиссия за проведение купли-продажи всех товаров и услуг является фиксированной и <b>взамается автоматически нашим гарантом.</b>\n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими!</a>",
                    parse_mode="html",
                    disable_web_page_preview=True,
                    reply_markup=nav.menu,
                )
                balance = garantDB.get_balance(call.message.chat.id)[0]
                if not db.user_exists(call.message.chat.id):
                    db.add_user(call.message.chat.id, float(balance), username)
                db.set_balance(call.message.chat.id, float(balance))
                await state.update_data(auction_id=None)
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
                    f"Приветствуем, @{username}!🙋\nДобро пожаловать внутрь первого в индустрии бота для автоматического проведения аукционов между воркерами.\n\n💎Если вы желаете с интересом провести время и получить лучший товар по лучшей цене - данная ветка проектов для вас.\n\n🤝Мы работаем на базе системы <a href='https://t.me/pradagarant_bot'>PRADA | GARANT</a> - это гарантирует безопасность всех сторону участников аукциона и позволяет забыть о возможности быть обманутым и наслаждаться процессом. \n\n💠Система оплаты происходит напрямую через <i>@CryptoBot,</i> что гарантирует <b>сохранность ваших средств</b> и полную <b>конфиденциальность сделок.</b> \n\n💵Все суммы сделок считаются в долларах <b>(USD)</b>, а все сделки проходят в <b>криптовалюте USDT (TRC20)</b>, без возможности перехода оплаты на другую криптовалюту.\n\n🦾Для улучшения работы бота или по любым другим вопросам вы <b>всегда можете обратиться в нашу круглосуточную поддержку </b>- @pradaaction_sup. Мы всегда <b>рады обратной связи</b> и готовы <b>реализовать любые ваши пожелания.</b>\n\n👉Комиссия за проведение купли-продажи всех товаров и услуг является фиксированной и <b>взамается автоматически нашим гарантом.</b>\n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими!</a>",
                    parse_mode="html",
                    disable_web_page_preview=True,
                    reply_markup=nav.menu,
                )
                balance = garantDB.get_balance(chatid)[0]
                if not db.user_exists(chatid):
                    db.add_user(chatid, float(balance), username)
                db.set_balance(chatid, float(balance))
        elif "remove_auction" in call.data:
            if call.data[0] == "a":
                chatid = call.data[16:]
            try:
                members_id = db.get_members_id(chatid)[0].split("/")
                db.del_auction(chatid)
                for member in members_id:
                    if not member == "":
                        await bot.send_message(
                            int(member),
                            "Аукцион удален. Можно расходиться🗑",
                            reply_markup=nav.del_auction,
                        )
                if call.data[0] == "a":
                    await delete_msg(call.message, 1)
                else:
                    await delete_msg(call.message, 2)
                await bot.send_message(
                    chatid, "Аукцион успешно удален✅", reply_markup=nav.menu
                )
            except Exception as e:
                print(e, call.data)
                await bot.send_message(chatid, "Что-то пошло не так⛔️")
        elif "move" in call.data:
            await delete_msg(call.message, 1)
            await bot.send_message(chatid, "Выбирайте действие📋", reply_markup=nav.menu)
            await state.set_state(ClientState.START)
        elif "close" in call.data:
            await delete_msg(call.message, 2)
        elif "start_cost" in call.data:
            try:
                auction_info = db.get_auction(chatid)
                if auction_info[2] < auction_info[5]:
                    await bot.send_message(
                        chatid, "Уже нельзя поменять начальную ставку⛔️"
                    )
                    return
                await bot.send_message(
                    chatid,
                    "Введите новую начальную ставку💵",
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton(text="Назад", callback_data="back_1")
                    ),
                )
                await state.set_state(ClientState.CHANGESTARTCOST)
            except Exception as e:
                print(e, call.data)
                await bot.send_message(chatid, "Что-то пошло не так⛔️")
        elif "back" in call.data:
            try:
                await bot.delete_message(chatid, call.message.message_id)
                if call.data[-1] == "2":
                    await bot.delete_message(chatid, call.message.message_id - 1)
                    await bot.send_message(chatid, "🏆", reply_markup=nav.menu)
                await state.set_state(ClientState.START)
            except Exception as e:
                print(e, call.data)
                await bot.send_message(chatid, "Что-то пошло не так⛔️")
        elif "acceptproduct" in call.data:
            auction_owner = call.data[14:]
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            db.set_auction_status(auction_owner, "inactive")
            await bot.send_message(
                auction_owner,
                "Админ одобрил добавление вашего аукциона, ожидайте участников✅",
                reply_markup=nav.owner_actions,
            )
            await bot.send_message(
                auction_owner, "Ожидайте участников⏱", reply_markup=nav.get_auction_info
            )
        elif "denyproduct" in call.data:
            await state.update_data(auction_owner=call.data[12:])
            await bot.delete_message(cfg.glav_admin, call.message.message_id)
            await bot.send_message(cfg.glav_admin, "Напишите причину отказа")
            await state.set_state(ClientState.DESCRIBEDENY)
        elif "enter_auction" in call.data:
            try:
                author_id = int(call.data[13:])
                db.change_members(author_id, 1)
                auction_info = db.get_auction(author_id)
                current_members_id = db.get_members_id(author_id)[0]
                new_members_id = current_members_id + "/" + str(chatid)
                db.set_members_id(author_id, new_members_id)
                db.set_prev_rate(chatid, "Ставка не сделана")
                await bot.send_message(
                    author_id,
                    f"К вашему аукциону присоединился новый участник \nКоличество участников: {db.get_auction_members(author_id)[0]} 👥",
                )
                last_rates = ""
                members_list = []
                if not current_members_id == "":
                    members_list = current_members_id.split("/")
                    members_list.pop(0)
                    for i in range(len(members_list)):
                        user_info = db.get_prev_rate(members_list[i])[0]
                        last_rates += f'Участник {i + 1}: {user_info if user_info == "Ставка не сделана" else user_info + " USDT"}\n'
                # await send_all(members_list, author_id)
                await bot.send_message(
                    chatid,
                    f'Вы присоединились к аукциону №{auction_info[0]}\n📦Товар: {auction_info[4]}\n{"💵Начальная ставка" if auction_info[6] == "inactive" else "💲Текущая ставка"} : {auction_info[2] if auction_info[6] == "inactive" else auction_info[5]}\n👥Участников: {auction_info[1]}',
                    reply_markup=nav.member_actions,
                )
                await bot.send_message(
                    chatid,
                    "Ожидайте начала аукциона",
                    reply_markup=nav.get_auction_info,
                )
                if int(db.get_auction_members(author_id)[0]) == int(
                    db.get_autostart(author_id)[0]
                ):
                    db.set_auction_status(author_id, "active")
                    await bot.send_message(
                        author_id,
                        "Сработал автостарт. Участники могут предлагать ставки",
                    )
                    for member in new_members_id.split("/"):
                        if not member == "":
                            try:
                                await bot.send_message(
                                    int(member),
                                    "Аукцион начат. Можно предлагать ставки✅",
                                    reply_markup=nav.member_actions,
                                )
                            except:
                                pass

                await state.update_data(auction_id=author_id)
            except Exception as e:
                print(e, e.args, call.data)
                await bot.send_message(chatid, "Что-то пошло не так.⛔️")
        elif "leave_auction" in call.data:
            try:
                state_data = await state.get_data()
                author_id = state_data["auction_id"]
                await bot.send_message(
                    chatid, "Вы вышли из аукциона⭕️", reply_markup=nav.menu
                )
                await state.update_data(auction_id=None)
                db.change_members(author_id, -1)
                current_members_id = db.get_members_id(author_id)[0]
                replace_member_id = "/" + str(chatid)
                new_members_id = current_members_id.replace(replace_member_id, "")
                db.set_members_id(author_id, new_members_id)
                members_id = new_members_id.split("/")
                members_id.pop(0)
                # await send_all(members_id, author_id)
                await bot.send_message(
                    author_id,
                    f"Участник вышел из аукциона. Количсетво участников: {db.get_auction_members(author_id)[0]} 👥",
                )
            except Exception as e:
                print(e, call.data)
                await bot.send_message(chatid, "Что-то пошло не так⛔️")
        elif "offer_rate" in call.data:
            try:
                gbalance = garantDB.get_balance(chatid)[0]
                db.set_balance(chatid, float(gbalance))
                state_data = await state.get_data()
                author_id = state_data["auction_id"]
                if db.get_auction(author_id)[6] == "inactive":
                    await bot.send_message(chatid, "Аукцион еще не начат⛔️")
                else:
                    await bot.send_message(
                        chatid,
                        f"Напишите вашу ставку. Минимальный шаг: 1 USDT. Ваш баланс: {db.get_user(chatid)[1]} USDT💵",
                    )
                    await state.set_state(ClientState.OFFERRATE)
            except Exception as e:
                print(e, call.data)
                await bot.send_message(chatid, "Что-то пошло не так⛔️")
        elif "start_auction" in call.data:
            try:
                if db.get_auction_members(chatid)[0] > 1:
                    if db.get_auction(chatid)[6] == "active":
                        await bot.send_message(chatid, "Аукцион уже начат⛔️")
                        return
                    db.set_auction_status(chatid, "active")
                    await bot.send_message(
                        chatid, "Аукцион начат. Участники могут делать ставки✅"
                    )
                    members_id = db.get_members_id(chatid)[0].split("/")
                    members_id.pop(0)
                    # await send_all(members_id, chatid)
                    for member in members_id:
                        if not member == "":
                            await bot.send_message(
                                int(member),
                                "Аукцион начат. Можно предлагать ставки✅",
                                reply_markup=nav.member_actions,
                            )
                else:
                    await bot.send_message(
                        chatid,
                        "Недостаточно пользователей для начала аукциона. Необходимо 2 и более участников⛔️",
                    )
            except Exception as e:
                print(e, call.data)
                await bot.send_message(chatid, "Что-то пошло не так.⛔️")
        elif "return" in call.data:
            await bot.send_message(chatid, "Выбирайте действие📋", reply_markup=nav.menu)
            await state.update_data(author_id=None)
        elif "accept_offer" in call.data:
            try:
                author_id = int(call.data[12:])
                members_id = db.get_members_id(chatid)[0].split("/")
                auction_info = db.get_auction(chatid)
                user_info = db.get_user(author_id)
                offer_link = (
                    f"offer {db.get_user(chatid)[0]} {user_info[0]} {auction_info[5]} a"
                )
                if not str(author_id) in auction_info[7]:
                    await bot.send_message(
                        chatid, "Участник покинул аукцион. Его ставка анулирована"
                    )
                    return
                await bot.send_message(
                    author_id,
                    f"Вы выиграли аукцион. Ваша ставка: {auction_info[5]} USDT. Продавец предложит вам сделку в нашем гаранте✅",
                    reply_markup=nav.del_auction,
                )
                await bot.send_message(
                    chatid,
                    f"Ваш аукцион закончился на ставке {auction_info[5]} USDT💵\nОтправьте данный текст нашему гаранту для начала сделки: `{nav.code_link(offer_link.encode())}`",
                    parse_mode="MARKDOWN",
                    reply_markup=nav.del_auction,
                )
                await state.set_state(ClientState.START)
                db.del_auction(chatid)
                for member in members_id:
                    if not member == "" and not int(member) == author_id:
                        await bot.send_message(
                            int(member),
                            "Аукцион закончился⌛️",
                            reply_markup=nav.del_auction,
                        )
            except Exception as e:
                print(e)
                await bot.send_message(chatid, "Что-то пошло не так⛔️")
        elif "detail" in call.data:
            await bot.delete_message(chat_id=chatid, message_id=call.message.message_id)
            auction = db.get_auction(int(call.data[7:]))
            await bot.send_message(
                chatid,
                f'Аукцион: №{auction[0]}\n📦Товар: {auction[4]}\nОписание товара: {auction[9]}\n{"💵Начальная ставка" if auction[6] == "inactive" else "💲Текущая ставка"} : {auction[2] if auction[6] == "inactive" else auction[5]}\n👥Участников: {auction[1]}\n📢Статус: {auction[6]} ',
                reply_markup=nav.get_auction_offer(auction[3]),
            )
    except Exception as e:
        print(e, call.data)
        await bot.send_message(chatid, "Что-то пошло не так⛔️")


@dp.message_handler()
async def non_start(message: types.Message, state: FSMContext):
    try:
        if message.chat.type == "private":
            await state.update_data(username=message.from_user.username)
            if not await checkMember(message.chat.id):
                await bot.send_message(
                    message.chat.id,
                    f"Для доступа к боту необходимо подписаться на канал!",
                    reply_markup=nav.channel_url,
                )
                await state.set_state(ClientState.START)
                return
            elif not garantDB.user_exists(message.chat.id):
                await bot.send_message(
                    message.chat.id,
                    "Для доступа к этому боту необходимо нажать на старт в нашем гарант боте💎",
                    reply_markup=nav.garant_check,
                )
                return
            elif garantDB.check_ban(message.chat.id) == "1":
                await bot.send_message(
                    message.chat.id, "❌К сожалению вы получили блокировку❌"
                )
                return
            await bot.send_message(
                message.chat.id,
                f"Приветствуем, @{message.from_user.username}!🙋\nДобро пожаловать внутрь первого в индустрии бота для автоматического проведения аукционов между воркерами.\n\n💎Если вы желаете с интересом провести время и получить лучший товар по лучшей цене - данная ветка проектов для вас.\n\n🤝Мы работаем на базе системы <a href='https://t.me/pradagarant_bot'>PRADA | GARANT</a> - это гарантирует безопасность всех сторону участников аукциона и позволяет забыть о возможности быть обманутым и наслаждаться процессом. \n\n💠Система оплаты происходит напрямую через <i>@CryptoBot,</i> что гарантирует <b>сохранность ваших средств</b> и полную <b>конфиденциальность сделок.</b> \n\n💵Все суммы сделок считаются в долларах <b>(USD)</b>, а все сделки проходят в <b>криптовалюте USDT (TRC20)</b>, без возможности перехода оплаты на другую криптовалюту.\n\n🦾Для улучшения работы бота или по любым другим вопросам вы <b>всегда можете обратиться в нашу круглосуточную поддержку </b>- @pradaaction_sup. Мы всегда <b>рады обратной связи</b> и готовы <b>реализовать любые ваши пожелания.</b>\n\n👉Комиссия за проведение купли-продажи всех товаров и услуг является фиксированной и <b>взамается автоматически нашим гарантом.</b>\n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими!</a>",
                parse_mode="html",
                disable_web_page_preview=True,
                reply_markup=nav.menu,
            )
            await state.update_data(auction_id=None)
            balance = garantDB.get_balance(message.chat.id)[0]
            if not db.user_exists(message.chat.id):
                db.add_user(message.chat.id, float(balance), message.from_user.username)
            db.set_balance(message.chat.id, float(balance))
            await state.update_data(author_id=None)
            await state.set_state(ClientState.START)
    except Exception as e:
        print(e, " start 2")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
