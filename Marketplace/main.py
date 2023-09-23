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


def sortOffers(mass: list, increase):
    mass1 = mass
    mass1.pop(0)
    if increase == "increase":
        mass1.sort(key=lambda x: int(x.split("_")[2]), reverse=True)
    elif increase == "decrease":
        mass1.sort(key=lambda x: int(x.split("_")[2]))
    return mass1


db.create_tables()


@dp.message_handler(commands=["start"])
async def start(message: types.Message, state: FSMContext):
    try:
        if message.chat.type == "private":
            if not garantDB.user_exists(message.chat.id):
                await bot.send_message(
                    message.chat.id,
                    "🗣️ Добро пожаловать в PRADA | MARKETPLACE - уникальную площадку по размещению ваших услуг и товаров, которая гарантирует безопасность как покупателя, так и продавца.\n💬 Внизу будет представлено пользовательское соглашение, запустив бота Вы автоматически подтверждаете что вы со всем ознакомились и даете свое согласие.\n🏆 PRADA | MARKETLACE - работай с лучшими!",
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton(
                            text="Перейти в гарант бота💎",
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
                message.chat.id, "Тестовое сообщение абоба буба", reply_markup=nav.menu
            )
            # await bot.send_message(
            #     message.from_user.id,
            #     "Выберите действие📋",
            #     reply_markup=nav.choose_action,
            # )
            await state.set_state(ClientState.START)
    except Exception as e:
        print(e, " start")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.callback_query_handler(state=ClientState.all_states)
async def callback_message(call: types.CallbackQuery, state: FSMContext):
    chatid = call.message.chat.id
    try:
        if "create_offer" in call.data:
            if len(db.get_user_offers(chatid)[0].split("/")) > 7:
                await bot.send_message(
                    chatid,
                    "Предложений не может быть больше 7!",
                )
                return
            await bot.send_message(
                chatid,
                "К какой категории относиться ваш товар?📦",
                reply_markup=nav.categor,
            )
            await state.set_state(ClientState.CREATEOFFER_CATEGORY)
        elif "choose_product" in call.data:
            await bot.send_message(
                chatid, "Выберите категорию💼", reply_markup=nav.categor
            )
            await state.set_state(ClientState.CHOOSEPRODUCT_CATEGORY)
        elif "buy" in call.data:
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
        elif "accept" in call.data:
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
                        url="https://t.me/pradagarantbot",
                    )
                ),
            )
            await state.set_state(ClientState.START)
        elif "deny" in call.data:
            await bot.delete_message(chatid, call.message.message_id)
            await state.set_state(ClientState.START)
            await bot.send_message(
                chatid, "Выберите действие📋", reply_markup=nav.choose_action
            )
        elif "my_products" in call.data:
            if db.get_user_offers(chatid) == None:
                await bot.send_message(chatid, "У вас нет активных предложений")
                return
            await bot.send_message(
                chatid, "Выберите категорию📋", reply_markup=nav.categor
            )
            await state.set_state(ClientState.DELETEPRODUCT_CATEGORY)
        elif "del" in call.data:
            offer_str = call.data[4:]
            db.del_offer_products(chatid, offer_str.split("/"))
            await bot.delete_message(chatid, call.message.message_id)
            await state.set_state(ClientState.START)
            await bot.send_message(chatid, "Товар удален✔️")
        elif "sort" in call.data:
            await state.update_data(choosed_sort=call.data[5:])
            await bot.send_message(
                chatid, "Выберите категорию", reply_markup=nav.categor
            )
            await state.set_state(ClientState.CHOOSEPRODUCT_CATEGORY)
    except Exception as e:
        print(e, " callback")
        await bot.send_message(chatid, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.DELETEPRODUCT_CATEGORY)
async def createOffer(message: types.Message, state: FSMContext):
    try:
        choosed_category = message.text[:-1]
        user_offers = db.get_user_offers(message.chat.id)[0].split("/")
        res = True
        for offer in user_offers:
            if not offer == "":
                offer_list = offer.split("_")
                product_category = offer_list[0]
                product_name = offer_list[1]
                product_price = offer_list[2]
                del_link = f"{product_category}/{product_name}/{product_price}"
                if choosed_category == product_category:
                    res = False
                    await bot.send_message(
                        message.chat.id,
                        f"💼Категория: {product_category}\n📦Товар: {product_name}\n💲Цена: {product_price} USDT",
                        reply_markup=nav.get_offer_del_button(del_link),
                    )
        if res:
            await bot.send_message(
                message.chat.id,
                "Ваших товаров данной категории не найдено",
                reply_markup=nav.menu,
            )
            await state.set_state(ClientState.START)
        else:
            await bot.send_message(
                message.chat.id, "Включение меню", reply_markup=nav.menu
            )

    except Exception as e:
        print(e, " delete product")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.CHOOSEPRODUCT_CATEGORY)
async def chooseProduct(message: types.Message, state: FSMContext):
    try:
        state_data = await state.get_data()
        choosed_category = message.text[:-1]
        all_offers = db.get_all_offers()
        res = False
        for user_offers in all_offers:
            owner_id = user_offers[0]
            user_offers_list = sortOffers(
                user_offers[1].split("/"), state_data["choosed_sort"]
            )
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
                            f"💼Категория: {product_category}\n📦Товар: {product_name}\nАвтор: {owner_id}\n💲Цена: {product_price} USDT",
                            reply_markup=nav.get_offer_buy_button(buy_link),
                        )
        if not res:
            await bot.send_message(
                message.chat.id,
                "Товаров в данной категории не найдено❌.",
                reply_markup=nav.menu,
            )
        else:
            await bot.send_message(
                message.chat.id, "Включение меню", reply_markup=nav.menu
            )
        await state.set_state(ClientState.START)
    except Exception as e:
        print(e, " create offer 1")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.CREATEOFFER_CATEGORY)
async def createOffer(message: types.Message, state: FSMContext):
    try:
        await state.update_data(product_category=message.text[:-1])
        await bot.send_message(
            message.chat.id,
            "Напишите краткое описание вашего товара✏️",
            reply_markup=nav.menu,
        )
        await state.set_state(ClientState.CREATEOFFER_NAME)
    except Exception as e:
        print(e, " create offer 2")
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(state=ClientState.CREATEOFFER_NAME)
async def createOffer(message: types.Message, state: FSMContext):
    try:
        await state.update_data(product_name=message.text)
        await bot.send_message(
            message.chat.id, "Напишите стоимость вашего товара в USDT💲"
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
        try:
            product_price = int(message.text)
            product_price = str(product_price)
        except:
            await bot.send_message(message.chat.id, "Введите число!")
            return
        state_data = await state.get_data()
        product_category = state_data["product_category"]
        product_name = state_data["product_name"]
        db.add_offer(message.chat.id, [product_category, product_name, product_price])
        await bot.send_message(
            message.chat.id,
            "Продукт успешно добавлен✔️",
            reply_markup=nav.choose_action,
        )
        await state.set_state(ClientState.START)
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, "Что-то пошло не так⛔️")


@dp.message_handler(content_types=["text"], state=ClientState.all_states)
async def textHandler(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    if message.text == "Создать предложение":
        try:
            if len(db.get_user_offers(chatid)[0].split("/")) > 7:
                await bot.send_message(
                    chatid,
                    "Предложений не может быть больше 7!",
                )
                return
        except:
            pass
        await bot.send_message(
            chatid,
            "К какой категории относиться ваш товар?📦",
            reply_markup=nav.categor,
        )
        await state.set_state(ClientState.CREATEOFFER_CATEGORY)
    elif message.text == "Выбрать товар":
        await bot.send_message(
            chatid, "Выберите вариант сортировки", reply_markup=nav.sort_choose
        )
    elif message.text == "Мои товары":
        if db.get_user_offers(chatid) == None:
            await bot.send_message(chatid, "У вас нет активных предложений")
            return
        await bot.send_message(chatid, "Выберите категорию📋", reply_markup=nav.categor)
        await state.set_state(ClientState.DELETEPRODUCT_CATEGORY)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
