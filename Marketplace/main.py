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
    CHOOSEPRODUCT_CATEGORY = State()
    DELETEPRODUCT_CATEGORY = State()


db.create_tables()


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
            balance = garantDB.get_balance(message.chat.id)[0]
            if not db.user_exists(message.chat.id):
                db.add_user(message.chat.id, float(balance), message.from_user.username)
            db.set_balance(message.chat.id, float(balance))
            await bot.send_message(
                message.from_user.id,
                "Выберите действие",
                reply_markup=nav.choose_action,
            )
            await state.set_state(ClientState.START)
    except Exception as e:
        print(e, " start")
        await bot.send_message(message.chat.id, "Что-то пошло не так")


@dp.callback_query_handler(state=ClientState.all_states)
async def callback_message(call: types.CallbackQuery, state: FSMContext):
    chatid = call.message.chat.id
    try:
        if "create_offer" in call.data:
            await bot.send_message(
                chatid,
                "К какой категории относиться ваш товар?",
                reply_markup=nav.categor,
            )
            await state.set_state(ClientState.CREATEOFFER_CATEGORY)
        elif "choose_product" in call.data:
            await bot.send_message(
                chatid, "Выберите категорию", reply_markup=nav.categor
            )
            await state.set_state(ClientState.CHOOSEPRODUCT_CATEGORY)
        elif "buy" in call.data:
            balance = garantDB.get_balance(chatid)[0]
            db.set_balance(chatid, float(balance))
            if int(call.data.split()[1]) == chatid:
                await bot.send_message(chatid, "Нельзя купить свой товар")
                await state.set_state(ClientState.START)
                return
            elif int(db.get_user(chatid)[1]) < int(call.data.split()[3]):
                await bot.send_message(
                    chatid,
                    f"Недостаточно денег на балансе. Ваш баланс {db.get_user(chatid)[1]} USDT",
                )
                await state.set_state(ClientState.START)
                return
            await state.update_data(seller_id=call.data[4:])
            await bot.send_message(
                chatid,
                "Вы уверены что хотите купить этот товар? Потом это действие нельзя будет отменить",
                reply_markup=nav.buy_choose,
            )
        elif "accept" in call.data:
            state_data = await state.get_data()
            buy_link = state_data["seller_id"]
            await bot.edit_message_text(
                chat_id=chatid,
                text=f"Отправьте данный текст нашему гаранту для начала сделки: `{nav.code_link(buy_link.encode())}`",
                message_id=call.message.message_id,
                parse_mode="MARKDOWN",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        text="Перейти в гарант бота", url="https://t.me/pradagarantbot"
                    )
                ),
            )
            await state.set_state(ClientState.START)
        elif "deny" in call.data:
            await bot.delete_message(chatid, call.message.message_id)
            await state.set_state(ClientState.START)
            await bot.send_message(
                chatid, "Выберите действие", reply_markup=nav.choose_action
            )
        elif "my_products" in call.data:
            await bot.send_message(
                chatid, "Выберите категорию", reply_markup=nav.categor
            )
            await state.set_state(ClientState.DELETEPRODUCT_CATEGORY)
        elif "del" in call.data:
            offer_str = call.data[4:]
            db.del_offer_products(chatid, offer_str.split("/"))
            await bot.delete_message(chatid, call.message.message_id)
            await state.set_state(ClientState.START)
            await bot.send_message(chatid, "Товар удален")
    except Exception as e:
        print(e, " callback")
        await bot.send_message(chatid, "Что-то пошло не так")


@dp.message_handler(state=ClientState.DELETEPRODUCT_CATEGORY)
async def createOffer(message: types.Message, state: FSMContext):
    choosed_category = message.text
    user_offers = db.get_user_offers(message.chat.id)[0].split("/")
    for offer in user_offers:
        if not offer == "":
            offer_list = offer.split("_")
            product_category = offer_list[0]
            product_name = offer_list[1]
            product_price = offer_list[2]
            del_link = f"{product_category}/{product_name}/{product_price}"
            if choosed_category == product_category:
                await bot.send_message(
                    message.chat.id,
                    f"Категория: {product_category}\nТовар: {product_name}\nЦена: {product_price} USDT",
                    reply_markup=nav.get_offer_del_button(del_link),
                )


@dp.message_handler(state=ClientState.CHOOSEPRODUCT_CATEGORY)
async def createOffer1(message: types.Message, state: FSMContext):
    try:
        choosed_category = message.text
        all_offers = db.get_all_offers()
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
                    buy_link = f"offer {owner_id} {message.chat.id} {product_price} customer-seller"
                    if choosed_category == product_category:
                        res = True
                        await bot.send_message(
                            message.chat.id,
                            f"Категория: {product_category}\nТовар: {product_name}\nАвтор: {owner_id}\nЦена: {product_price} USDT",
                            reply_markup=nav.get_offer_buy_button(buy_link),
                        )
        if not res:
            await bot.send_message(
                message.chat.id, "Товаров в данной категории не найдено."
            )
    except Exception as e:
        print(e, " create offer 1")
        await bot.send_message(message.chat.id, "Что-то пошло не так")


@dp.message_handler(state=ClientState.CREATEOFFER_CATEGORY)
async def createOffer(message: types.Message, state: FSMContext):
    try:
        await state.update_data(product_category=message.text)
        await bot.send_message(
            message.chat.id, "Напишите краткое описание вашего товара"
        )
        await state.set_state(ClientState.CREATEOFFER_NAME)
    except Exception as e:
        print(e, " create offer 2")
        await bot.send_message(message.chat.id, "Что-то пошло не так")


@dp.message_handler(state=ClientState.CREATEOFFER_NAME)
async def createOffer(message: types.Message, state: FSMContext):
    try:
        await state.update_data(product_name=message.text)
        await bot.send_message(
            message.chat.id, "Напишите стоимость вашего товара в USDT"
        )
        await state.set_state(ClientState.CREATEOFFER_PRICE)
    except Exception as e:
        print(e, " create offer 3")
        await bot.send_message(message.chat.id, "Что-то пошло не так")


@dp.message_handler(state=ClientState.CREATEOFFER_PRICE)
async def createOffer(message: types.Message, state: FSMContext):
    try:
        if db.get_user_offers(message.chat.id) == None:
            db.insert_offer_owner(message.chat.id)
        product_price = message.text
        state_data = await state.get_data()
        product_category = state_data["product_category"]
        product_name = state_data["product_name"]
        db.add_offer(message.chat.id, [product_category, product_name, product_price])
        await bot.send_message(
            message.chat.id, "Продукт успешно добавлен", reply_markup=nav.choose_action
        )
        await state.set_state(ClientState.START)
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, "Что-то пошло не так.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
