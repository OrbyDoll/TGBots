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
            "Выберите категорию📋",
            reply_markup=nav.categor_choose_forward,
        )


@dp.callback_query_handler()
async def call_handler(call: types.CallbackQuery):
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
    else:
        open_file = open(f"./test.txt", "rb")
        await bot.send_document(chatid, open_file)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
