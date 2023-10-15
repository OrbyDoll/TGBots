from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import config as cfg
import markups as nav
from filesMass import files_name

storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=storage)


class ClientState(StatesGroup):
    START = State()
    SEARCH = State()


def find_voice_desc(name, category):
    for voices in files_name[category]:
        if voices[1] == name:
            return voices[0]


async def checkMember(
    userid,
):
    chat_member = await bot.get_chat_member(cfg.required_chat_id, userid)
    if chat_member.status == "left":
        return False
    return True


state = FSMContext


print(ClientState.all_states)


@dp.message_handler(commands=["start"])
async def start(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if not await checkMember(message.chat.id):
            await bot.send_message(
                message.chat.id,
                f"Для доступа к боту необходимо подписаться на канал!",
                reply_markup=nav.channel_url,
            )
            await state.set_state(ClientState.START)
            return
        await bot.send_message(
            message.chat.id,
            f"Приветствуем, @{message.from_user.username}!🙋\n\n👱🏻‍♀️Данный бот - <b>удобное и бесплатное средство </b>получения самых актуальным материалов для обработки мамонтов путем голосовых сообщений.\n\n🎙<b>Внутри вас ждет более 600 голосовых сообщения для 8 разных направлений ворка, которые позволяют вам сэкономить ваше время и увеличить профиты.</b> \n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими]</a>",
            parse_mode="html",
            disable_web_page_preview=True,
        )
        await bot.send_message(
            message.chat.id, "Выберите категорию", reply_markup=nav.categor_choose
        )
        await state.set_state(ClientState.START)


@dp.callback_query_handler(state=ClientState.all_states)
async def callback(call: types.CallbackQuery, state: FSMContext):
    chatid = call.message.chat.id
    await bot.answer_callback_query(callback_query_id=call.id)
    if call.data == "check_member":
        if await checkMember(chatid):
            await bot.delete_message(chatid, call.message.message_id)
            await bot.send_message(
                chatid,
                f"Приветствуем, @{call.message.from_user.username}!🙋\n\n👱🏻‍♀️Данный бот - <b>удобное и бесплатное средство </b>получения самых актуальным материалов для обработки мамонтов путем голосовых сообщений.\n\n🎙<b>Внутри вас ждет более 600 голосовых сообщения для 8 разных направлений ворка, которые позволяют вам сэкономить ваше время и увеличить профиты.</b> \n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими]</a>",
                parse_mode="html",
                disable_web_page_preview=True,
            )
            await bot.send_message(
                chatid, "Выберите категорию", reply_markup=nav.categor_choose
            )
    elif call.data.startswith("cat_"):
        choosed_category = call.data[4:]
        await bot.delete_message(chat_id=chatid, message_id=call.message.message_id)
        await bot.send_message(
            chatid,
            "Выберите файл📋",
            reply_markup=nav.get_category_page(choosed_category, 0, 0, "no"),
        )
    elif call.data.startswith("page"):
        data_split = call.data.split()
        choosed_category = data_split[2]
        page = int(data_split[1])
        markup = (
            nav.get_category_page(choosed_category, page, 0, "no")
            if data_split[3] == "normal"
            else nav.get_search_markup(choosed_category, data_split[3], page)
        )
        try:
            await bot.edit_message_reply_markup(
                chatid,
                call.message.message_id,
                call.message.message_id,
                reply_markup=markup,
            )
        except:
            pass
    elif call.data == "back":
        await bot.edit_message_text(
            chat_id=chatid,
            message_id=call.message.message_id,
            text=f"Приветствую, {call.message.from_user.username} ✅\n\nPRADA MATERIALS - универсальный, полностью бесплатный бот, позволяющий вам брать материалы для комфортной работы по любым направлениям💎\n\n🏆PRADA EMPIRE - работай с лучшим🏆",
        )
        await bot.edit_message_reply_markup(
            chat_id=chatid,
            message_id=call.message.message_id,
            reply_markup=nav.categor_choose,
        )
    elif "search" in call.data:
        await bot.delete_message(chatid, call.message.message_id)
        await bot.send_message(
            chatid,
            "Введите ключ по которому будет происходить поиск",
            reply_markup=nav.back_to_files,
        )
        await state.update_data(category=call.data[7:])
        await state.set_state(ClientState.SEARCH)
    elif call.data == "choose":
        await bot.delete_message(chatid, call.message.message_id)
        state_data = await state.get_data()
        category = state_data["category"]
        await bot.send_message(
            chatid,
            "Выберите файл📋",
            reply_markup=nav.get_category_page(category, 0, 0, "no"),
        )
        await state.set_state(ClientState.START)
    elif call.data == "hide_voice":
        await bot.delete_message(chatid, call.message.message_id)
        await bot.delete_message(chatid, call.message.message_id - 1)
    elif not call.data == "aboba":
        try:
            data_split = call.data.split("/")
            open_file = open(
                f"files/{data_split[0]}/{data_split[1]}.ogg",
                "rb",
            )
            await bot.send_message(
                chatid, find_voice_desc(data_split[1], data_split[0])
            )
            await bot.send_audio(
                chat_id=chatid,
                audio=open_file,
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("Скрыть", callback_data="hide_voice")
                ),
            )
        except Exception as e:
            print(e)
            await bot.send_message(chatid, "Этот файл недоступен⛔️")


@dp.message_handler(state=ClientState.SEARCH)
async def Search(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id)
    key = message.text
    state_data = await state.get_data()
    category = state_data["category"]
    if not nav.get_search_markup(category, key, 0):
        await bot.send_message(
            message.chat.id,
            "По этому ключу не найдо голосовых сообщений. Вы можете продолжить вводить ключи или вернуться к выбору файлов",
            reply_markup=nav.back_to_files,
        )
        return
    await bot.send_message(
        message.chat.id,
        "Выберите файл📋",
        reply_markup=nav.get_search_markup(category, key, 0),
    )
    await state.set_state(ClientState.START)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
