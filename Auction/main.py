from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import sys
import pathlib
import config as cfg
import markups as nav
from dbshka import Database
from garantDB import GarantDB


class ClientState(StatesGroup):
    START = State()
    CREATEAUCTION = State()
    AUCTIONOWNER = State()
    OFFERRATE = State()
    CHANGESTARTCOST = State()


storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=storage)
script_dir = pathlib.Path(sys.argv[0]).parent
db = Database(script_dir / cfg.db_file)
garantDB = GarantDB(script_dir / cfg.garantDB_file)

db.create_tables()
garantDB.create_table()


@dp.message_handler(commands=["start"])
async def start(message: types.Message, state: FSMContext):
    try:
        if message.chat.type == "private":
            if not garantDB.user_exists(message.chat.id):
                await bot.send_message(
                    message.chat.id,
                    "Для доступа к этому боту необходимо нажать на старт в нашем гарант боте.",
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton(
                            text="Перейти в гарант бота",
                            url="https://t.me/pradagarantbot",
                        )
                    ),
                )
                return
            await state.update_data(auction_id=None)
            balance = garantDB.get_balance(message.chat.id)[0]
            if not db.user_exists(message.chat.id):
                db.add_user(message.chat.id, float(balance), message.from_user.username)
            db.set_balance(message.chat.id, float(balance))
            await bot.send_message(
                message.chat.id,
                f"Привет {message.from_user.username}! \n\nСоздавай собственный аукцион или присоединяйся к уже сущетсвующему.",
                reply_markup=nav.action_choose,
            )
            await state.update_data(author_id=None)
            current_state = await state.get_state()
            if current_state == None:
                await state.set_state(ClientState.START)
    except Exception as e:
        print(e, " start")


@dp.callback_query_handler(state=ClientState.all_states)
async def call_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.answer_callback_query(callback_query_id=call.id)
        chatid = call.message.chat.id
        if "get_auctions" in call.data:
            try:
                state_data = await state.get_data()
                author_id = state_data["auction_id"]
                if db.check_active_auction(chatid) or not author_id == None:
                    await bot.send_message(
                        chatid, "Вам необходимо закончить все аукционы!"
                    )
                    return
                all_auctions = db.get_all_auctions()
                if len(all_auctions) == 0:
                    await bot.send_message(chatid, "Сейчас нет активных аукционов.")
                    return
                for auction in all_auctions:
                    if auction[1] < 5:
                        await bot.send_message(
                            chatid,
                            f'Аукцион: №{auction[0]}\nТовар: {auction[4]}\n{"Начальная ставка" if auction[6] == "inactive" else "Текущая ставка"} : {auction[2] if auction[6] == "inactive" else auction[5]}\nУчастников: {auction[1]}\nСтатус: {auction[6]} ',
                            reply_markup=nav.get_auction_offer(auction[3]),
                        )
            except Exception as e:
                print(e, " get auctions")
        elif "create_auction" in call.data:
            try:
                state_data = await state.get_data()
                author_id = state_data["auction_id"]
                if db.check_active_auction(chatid):
                    await bot.send_message(chatid, "У вас уже есть аукцион!")
                    return
                if not author_id == None:
                    await bot.send_message(
                        chatid, "Вам необходимо закончить все аукционы!"
                    )
                    return
                await bot.send_message(chatid, "Напишите название товара")
                await state.set_state(ClientState.CREATEAUCTION)
            except Exception as e:
                print(e)
        elif "my_auction" in call.data:
            if db.check_active_auction(chatid):
                current_state = await state.get_state()
                if current_state == "ClientState:AUCTIONOWNER":
                    await bot.send_message(
                        chatid, "Вы уже находитесь в своем аукционе."
                    )
                else:
                    await bot.send_message(
                        chatid,
                        "Ваш аукцион, ожидайте участников",
                        reply_markup=nav.owner_actions,
                    )
                    await state.set_state(ClientState.AUCTIONOWNER)
            else:
                await bot.send_message(chatid, "У вас нет активного аукциона")
        elif "remove_auction" in call.data:
            try:
                members_id = db.get_members_id(chatid)[0].split("/")
                db.del_auction(chatid)
                for member in members_id:
                    if not member == "":
                        await bot.send_message(
                            int(member),
                            "Аукцион удален. Можно расходиться",
                            reply_markup=nav.del_auction,
                        )
                await bot.delete_message(chatid, call.message.message_id)
                await bot.delete_message(chatid, call.message.message_id - 1)
                await bot.send_message(
                    chatid, "Аукцион успешно удален!", reply_markup=nav.action_choose
                )
            except Exception as e:
                print(e, call.data)
                await bot.send_message(chatid, "Что-то пошло не так.")
        elif "start_cost" in call.data:
            try:
                auction_info = db.get_auction(chatid)
                if auction_info[2] < auction_info[5]:
                    await bot.send_message(
                        chatid, "Уже нельзя поменять начальную ставку."
                    )
                return
                await bot.send_message(chatid, "Введите новую начальную ставку.")
                await state.set_state(ClientState.CHANGESTARTCOST)
            except Exception as e:
                print(e, call.data)
                await bot.send_message(chatid, "Что-то пошло не так.")
        elif "enter_auction" in call.data:
            try:
                author_id = int(call.data[13:])
                db.change_members(author_id, 1)
                auction_info = db.get_auction(author_id)
                current_members_id = db.get_members_id(author_id)[0]
                new_members_id = current_members_id + "/" + str(chatid)
                db.set_members_id(author_id, new_members_id)
                await bot.send_message(
                    author_id,
                    f"К вашему аукциону присоединился новый участник \nКоличество участников: {db.get_auction_members(author_id)[0]}",
                )
                await bot.send_message(
                    chatid,
                    f'Вы присоединились к аукциону №{auction_info[0]}\nТовар: {auction_info[4]}\n{"Начальная ставка" if auction_info[6] == "inactive" else "Текущая ставка"} : {auction_info[2] if auction_info[6] == "inactive" else auction_info[5]}\nУчастников: {auction_info[1]}',
                    reply_markup=nav.member_actions,
                )
                await state.update_data(auction_id=author_id)
            except Exception as e:
                print(e, call.data)
                await bot.send_message(chatid, "Что-то пошло не так.")
        elif "leave_auction" in call.data:
            try:
                state_data = await state.get_data()
                author_id = state_data["auction_id"]
                await bot.send_message(
                    chatid, "Вы вышли из аукциона", reply_markup=nav.action_choose
                )
                await state.update_data(auction_id=None)
                db.change_members(author_id, -1)
                current_members_id = db.get_members_id(author_id)[0]
                replace_member_id = "/" + str(chatid)
                new_members_id = current_members_id.replace(replace_member_id, "")
                db.set_members_id(author_id, new_members_id)
                await bot.send_message(
                    author_id,
                    f"Участник вышел из аукциона. Количсетво участников: {db.get_auction_members(author_id)[0]}",
                )
            except Exception as e:
                print(e, call.data)
                await bot.send_message(chatid, "Что-то пошло не так.")
        elif "offer_rate" in call.data:
            try:
                gbalance = garantDB.get_balance(chatid)[0]
                db.set_balance(chatid, float(gbalance))
                state_data = await state.get_data()
                author_id = state_data["auction_id"]
                if db.get_auction(author_id)[6] == "inactive":
                    await bot.send_message(chatid, "Аукцион еще не начат.")
                else:
                    await bot.send_message(
                        chatid,
                        f"Напишите вашу ставку. Минимальный шаг: 1 USDT. Ваш баланс: {db.get_user(chatid)[1]} USDT",
                    )
                    await state.set_state(ClientState.OFFERRATE)
            except Exception as e:
                print(e, call.data)
                await bot.send_message(chatid, "Что-то пошло не так.")
        elif "start_auction" in call.data:
            try:
                if db.get_auction_members(chatid)[0] > 1:
                    if db.get_auction(chatid)[6] == "active":
                        await bot.send_message(chatid, "Аукцион уже начат.")
                        return
                    db.set_auction_status(chatid, "active")
                    await bot.send_message(
                        chatid, "Аукцион начат. Участники могут делать ставки."
                    )
                    members_id = db.get_members_id(chatid)[0].split("/")
                    for member in members_id:
                        if not member == "":
                            await bot.send_message(
                                int(member),
                                "Аукцион начат. Можно предлагать ставки",
                                reply_markup=nav.member_actions,
                            )
                else:
                    await bot.send_message(
                        chatid,
                        "Недостаточно пользователей для начала аукциона. Необходимо 2 и более участников",
                    )
            except Exception as e:
                print(e, call.data)
                await bot.send_message(chatid, "Что-то пошло не так.")
        elif "return" in call.data:
            await bot.send_message(
                chatid, "Выбирайте действие", reply_markup=nav.action_choose
            )
            await state.update_data(author_id=None)
        elif "accept_offer":
            try:
                author_id = int(call.data[12:])
                members_id = db.get_members_id(chatid)[0].split("/")
                auction_info = db.get_auction(chatid)
                user_info = db.get_user(author_id)
                offer_link = f"offer {db.get_user(chatid)[2]} {user_info[2]} {auction_info[5]} seller-customer"
                await bot.send_message(
                    author_id,
                    f"Вы выиграли аукцион. Ваша ставка: {auction_info[5]} USDT. Продавец предложит вам сделку в нашем гаранте",
                    reply_markup=nav.del_auction,
                )
                await bot.send_message(
                    chatid,
                    f"Ваш аукцион закончился на ставке {auction_info[5]} USDT.\nОтправьте данный текст нашему гаранту для начала сделки: `{nav.code_link(offer_link.encode())}`",
                    parse_mode="MARKDOWN",
                    reply_markup=nav.del_auction,
                )
                db.del_auction(chatid)
                for member in members_id:
                    if not member == "" and not int(member) == author_id:
                        await bot.send_message(
                            int(member),
                            "Аукцион закончился",
                            reply_markup=nav.del_auction,
                        )
            except Exception as e:
                print(e)
                await bot.send_message(chatid, "Что-то пошло не так.")
    except Exception as e:
        print(e, "callback")
        await bot.send_message(chatid, "Что-то пошло не так")


@dp.message_handler(state=ClientState.CREATEAUCTION)
async def createAuction(message: types.Message, state: FSMContext):
    product_name = message.text
    try:
        db.add_auction(message.chat.id, product_name, 0)
        await bot.send_message(
            message.chat.id,
            "Аукцион успешно создан, ожидайте участников.",
            reply_markup=nav.owner_actions,
        )
        await state.set_state(ClientState.AUCTIONOWNER)
    except Exception as e:
        print(e, "create auction")
        await bot.send_message(message.chat.id, "Что-то пошло не так.")


@dp.message_handler(state=ClientState.CHANGESTARTCOST)
async def changeStartCost(message: types.Message, state: FSMContext):
    new_start_cost = int(message.text)
    try:
        db.set_start_cost(message.chat.id, new_start_cost)
        members_id = db.get_members_id(message.chat.id)[0].split("/")
        auction_info = db.get_auction(message.chat.id)
        for member in members_id:
            if not member == "":
                await bot.send_message(
                    int(member),
                    f'Была изменена начальная ставка аукциона: №{auction_info[0]}\nТовар: {auction_info[4]}\n{"Начальная ставка" if auction_info[6] == "inactive" else "Текущая ставка"} : {auction_info[2] if auction_info[6] == "inactive" else auction_info[5]}\nУчастников: {auction_info[1]}\nСтатус: {auction_info[6]}',
                    reply_markup=nav.member_actions,
                )
        await bot.send_message(message.chat.id, "Начальная ставка успешно изменена.")
    except Exception as e:
        print(e, "change start cost")
        await bot.send_message(message.chat.id, "Что-то пошло не так.")


@dp.message_handler(state=ClientState.OFFERRATE)
async def offerRate(message: types.Message, state: FSMContext):
    try:
        offer = int(message.text)
        user_info = db.get_user(message.chat.id)
        state_data = await state.get_data()
        author_id = state_data["auction_id"]
        auction_info = db.get_auction(author_id)
        if offer > user_info[1]:
            await bot.send_message(
                message.chat.id,
                f"Ставка не может быть больше баланса. Ваш баланс: {user_info[1]}",
            )
        elif offer <= auction_info[5]:
            await bot.send_message(
                message.chat.id, "Ставка не может быть меньше предыдущей."
            )
        else:
            members_id = db.get_members_id(author_id)[0].split("/")
            for member in members_id:
                if not member == "":
                    await bot.send_message(
                        int(member),
                        f"Ставка поднята до {offer}",
                        reply_markup=nav.member_actions,
                    )
            await bot.send_message(
                author_id,
                f"Ставка поднята до {offer}",
                reply_markup=nav.accept_offer(message.chat.id),
            )
            db.set_current_cost(author_id, offer)
    except Exception as e:
        print(e, "offer rate")
        await bot.send_message(message.chat.id, "Что-то пошло не так.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
