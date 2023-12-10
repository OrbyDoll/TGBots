from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import config as cfg
import markups as nav


class ClientState(StatesGroup):
    START = State()
    CRYPT = State()
    DOCS = State()
    SERVICES = State()

class Crypt(StatesGroup):
    START = State()

class Banks(StatesGroup):
    START = State()
    RUSSIA = State()
    KAZAHSTAN = State()
    UKRAINE = State()

class Docs(StatesGroup):
    START = State()
    RUSSIA = State()
    KAZAHSTAN = State()
    UKRAINE = State()

storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=storage)


async def checkMember(
    userid,
):
    chat_member = await bot.get_chat_member(0, userid)
    if chat_member.status == "left":
        return False
    return True


async def delete_msg(message, count):
    for i in range(count):
        try:
            await bot.delete_message(message.chat.id, message.message_id - i)
        except:
            pass


@dp.message_handler(commands=["start"])
async def start(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    await bot.send_message(chatid, 'Меню',reply_markup=nav.start_menu)
    await state.set_state(ClientState.START)

@dp.message_handler(content_types=['text'], state=ClientState.START)
async def text(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    await delete_msg(message, 2)
    if message.text == 'Крипта':
        await state.set_state(Crypt.START)
        await bot.send_message(chatid, 'Крипта',reply_markup=nav.crypt_menu)
    elif message.text == 'Банки':
        await bot.send_message(chatid, 'Выберите банк', reply_markup=nav.banks_menu)
        await state.set_state(Banks.START)
    elif message.text == 'Документы':
        await bot.send_message(chatid, 'Документы меню', reply_markup=nav.banks_menu)
        await state.set_state(Docs.START)
    elif message.text == 'Прочие системы':
        pass
    elif message.text == 'О нас':
        pass

@dp.message_handler(content_types=['text'], state=Crypt.START)
async def text(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    if message.text == 'Хуй1':
        pass
    elif message.text == 'Назад':
        await delete_msg(message, 2)
        await bot.send_message(chatid,'Меню', reply_markup=nav.start_menu)
        await state.set_state(ClientState.START)
    #На этом мои полномочия все

@dp.message_handler(content_types=['text'], state=Banks.START)
async def text(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    await delete_msg(message, 2)
    if message.text == 'Казахстан':
        await bot.send_message(chatid, 'Казах меню', reply_markup=nav.kazahstan_bank_menu)
        await state.set_state(Banks.KAZAHSTAN)
    elif message.text == 'Россия':
        await bot.send_message(chatid,'Россия меню', reply_markup=nav.russia_bank_menu)
        await state.set_state(Banks.RUSSIA)
    elif message.text == 'Украина':
        await bot.send_message(chatid,'Хохол меню',reply_markup=nav.ukraine_bank_menu)
        await state.set_state(Banks.UKRAINE)
    elif message.text == 'Назад':
        await bot.send_message(chatid,'Меню', reply_markup=nav.start_menu)
        await state.set_state(ClientState.START)

@dp.message_handler(content_types=['text'], state=Banks.RUSSIA)
async def text(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    await delete_msg(message, 2)
    if message.text == 'Россия1':
        pass
    elif message.text == 'Назад':
        await bot.send_message(chatid,'Банки', reply_markup=nav.banks_menu)
        await state.set_state(Banks.START)

@dp.message_handler(content_types=['text'], state=Banks.UKRAINE)
async def text(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    await delete_msg(message, 2)
    if message.text == 'Украина1':
        pass
    elif message.text == 'Назад':
        await bot.send_message(chatid,'Банки', reply_markup=nav.banks_menu)
        await state.set_state(Banks.START)

@dp.message_handler(content_types=['text'], state=Banks.KAZAHSTAN)
async def text(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    await delete_msg(message, 2)
    if message.text == 'Казах1':
        pass
    elif message.text == 'Назад':
        await bot.send_message(chatid,'Банки', reply_markup=nav.banks_menu)
        await state.set_state(Banks.START)
    
@dp.message_handler(content_types=['text'], state=Banks.KAZAHSTAN)
async def text(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    await delete_msg(message, 2)
    if message.text == 'Казах1':
        pass
    elif message.text == 'Назад':
        await bot.send_message(chatid,'Банки', reply_markup=nav.banks_menu)
        await state.set_state(Banks.START)

@dp.message_handler(content_types=['text'], state=Docs.START)
async def text(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    await delete_msg(message, 2)
    if message.text == 'Казах1':
        pass
    elif message.text == 'Назад':
        await bot.send_message(chatid,'Меню', reply_markup=nav.start_menu)
        await state.set_state(ClientState.START)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
