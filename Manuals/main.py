from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import config as cfg
import markups as nav


class ClientState(StatesGroup):
    START = State()
    CREATEAUCTION = State()
    AUCTIONOWNER = State()
    OFFERRATE = State()
    CHANGESTARTCOST = State()


storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.chat.type == "private":
        await bot.send_message(
            message.chat.id,
            "Пожалуйста, выберите нужное вам направление для прочтения мануала📃",
            reply_markup=nav.categor_choose_forward,
        )


@dp.callback_query_handler()
async def call_handler(call: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=call.id)
    chatid = call.message.chat.id
    if call.data == "forward":
        await bot.edit_message_reply_markup(
            chatid,
            call.message.message_id,
            call.message.message_id,
            nav.categor_choose_back,
        )
    elif call.data == "back":
        await bot.edit_message_reply_markup(
            chatid,
            call.message.message_id,
            call.message.message_id,
            nav.categor_choose_forward,
        )
    elif call.data == "shantazh":
        await bot.send_message(chatid, "К сожалению, в данный момент мануал недоступен так как он находиться в разработке⛔️. Вы можете вернуться к остальным мануалам нажав кнопку ниже", reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text='Назад', callback_data='delete')
        ), )
    elif call.data == 'delete':
        await bot.delete_message(chatid, call.message.message_id)
    elif call.data == "close":
        await bot.delete_message(chatid, call.message.message_id)
        await bot.delete_message(chatid, call.message.message_id - 1)
    else:
        file_name = call.data
        open_file = open(f"files/{file_name}.txt", "rb")
        if file_name == 'АУКЦИОН BY PRADA':
            await bot.send_message(chatid, "💸Для добавления в чат и начала работы по данному направлению напиши в личные сообщения @Imperator_Kuzco.\n\n⚡️В случае успешного прохождения небольшого собеседования вы будете добавлены в чат и сможете приступить к работе. Заряду!")
        await bot.send_document(
            chatid,
            open_file,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text="Скрыть", callback_data="delete")
            ),
        )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
