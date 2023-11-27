from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from moviepy.editor import *

import config as cfg
import markups as nav
from filesMass import voices, circles, pictures

storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=storage)


class ClientState(StatesGroup):
    START = State()
    SEARCH = State()
    VIDEO_CONVERT = State()


def find_voice_desc(name, category, mass):
    searching_mass = mass[category] if category != "circles" else mass
    for audio in searching_mass:
        if audio[1] == name:
            return audio[0]


async def checkMember(
    userid,
):
    # chat_member = await bot.get_chat_member(cfg.required_chat_id, userid)
    # if chat_member.status == "left":
    #     return False
    return True


async def delete_msg(message, count):
    for i in range(count):
        try:
            await bot.delete_message(message.chat.id, message.message_id - i)
        except:
            pass


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
        await delete_msg(message, 1)
        await bot.send_message(
            message.chat.id,
            f"Приветствуем, {message.from_user.first_name}!🙋\n\n👱🏻‍♀️Данный бот - <b>удобное и бесплатное средство </b>получения самых актуальным материалов для обработки мамонтов путем голосовых сообщений.\n\n🎙<b>Внутри вас ждет более 600 голосовых сообщения для 8 разных направлений ворка, которые позволяют вам сэкономить ваше время и увеличить профиты.</b> \n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими</a>",
            parse_mode="html",
            disable_web_page_preview=True,
            reply_markup=nav.start_menu,
        )
        await state.update_data(username=message.from_user.first_name)
        await state.set_state(ClientState.START)


@dp.message_handler(content_types=["text"], state=ClientState.all_states)
async def textMessages(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    msg = await bot.send_message(chatid, "Типо кубок", reply_markup=nav.menu_hide)
    await delete_msg(msg, 1)
    await delete_msg(message, 2)
    if message.text == "Гс":
        await bot.send_message(
            message.chat.id,
            "🎤 <b>Выберите необходимую вам категорию</b>",
            parse_mode="html",
            reply_markup=nav.categor_choose,
        )
        await state.set_state(ClientState.START)
    elif message.text == "Кружки":
        await bot.send_message(
            chatid,
            "Выберите девушку",
            reply_markup=nav.get_category_page("circles", 0, 0, "no"),
        )
    elif message.text == "Картинки":
        await bot.send_message(
            chatid,
            "Выберите девушку",
            reply_markup=nav.get_category_page("pictures", 0, 0, "no"),
        )
    elif message.text == "Кружок из видео":
        await bot.send_message(
            chatid,
            "Пришли видео до 20Мб. Видео, длительностью более минуты будут обрезаны до минуты начиная с начала.",
            reply_markup=nav.back_to_menu,
        )
        await state.set_state(ClientState.VIDEO_CONVERT)


@dp.callback_query_handler(state=ClientState.all_states)
async def callback(call: types.CallbackQuery, state: FSMContext):
    chatid = call.message.chat.id
    messageid = call.message.message_id
    await bot.answer_callback_query(callback_query_id=call.id)
    if call.data == "check_member":
        if await checkMember(chatid):
            await bot.delete_message(chatid, call.message.message_id)
            await bot.send_message(
                chatid,
                f"Приветствуем, {call.message.from_user.first_name}!🙋\n\n👱🏻‍♀️Данный бот - <b>удобное и бесплатное средство </b>получения самых актуальным материалов для обработки мамонтов путем голосовых сообщений.\n\n🎙<b>Внутри вас ждет более 600 голосовых сообщения для 8 разных направлений ворка, которые позволяют вам сэкономить ваше время и увеличить профиты.</b> \n\n🏆 <a href='https://t.me/PRADAEMPlRE'>PRADA | EMPIRE - работай с лучшими]</a>",
                parse_mode="html",
                disable_web_page_preview=True,
            )
            await bot.send_message(
                chatid,
                "🎤 <b>Выберите необходимую вам категорию</b>",
                parse_mode="html",
                reply_markup=nav.categor_choose,
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
        state_data = await state.get_data()
        await bot.edit_message_text(
            chat_id=chatid,
            message_id=call.message.message_id,
            parse_mode="html",
            text=f"🎤 <b>Выберите необходимую вам категорию</b>",
            reply_markup=nav.categor_choose,
        )
    elif "hide_photos" in call.data:
        await delete_msg(call.message, int(call.data.split("_")[2]) + 1)
    elif call.data == "back_to_menu":
        await delete_msg(call.message, 2)
        await bot.send_message(chatid, "Меню", reply_markup=nav.start_menu)
        await state.set_state(ClientState.START)
    elif call.data == "back_to_girl_choose":
        await bot.edit_message_text(
            "Выберите девушку",
            chatid,
            messageid,
            reply_markup=nav.get_category_page("pictures", 0, 0, "no"),
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
            if data_split[0] == "circles" or data_split[0] == "pictures":
                dir_path = f"files/{data_split[0]}/{data_split[1]}.{'mp4' if data_split[0] == 'circles' else 'jpg'}"
            else:
                dir_path = f"files/voices/{data_split[0]}/{data_split[1]}.ogg"
            if data_split[0] != "pictures":
                with open(dir_path, "rb") as open_file:
                    if data_split[0] == "circles":
                        await bot.send_message(
                            chatid,
                            find_voice_desc(data_split[1], data_split[0], circles),
                        )
                        await bot.send_video_note(
                            chatid,
                            open_file,
                            reply_markup=nav.msg_desc_hide,
                        )
                    else:
                        await bot.send_message(
                            chatid,
                            find_voice_desc(data_split[1], data_split[0], voices),
                        )
                        await bot.send_audio(
                            chat_id=chatid,
                            audio=open_file,
                            reply_markup=nav.msg_desc_hide,
                        )
            else:
                photos_names = pictures[data_split[1]]
                photos = []
                for name in photos_names:
                    photos.append(
                        types.InputMediaPhoto(
                            types.InputFile(f"files/pictures/{name}.jpg"),
                        )
                    )
                await bot.send_media_group(
                    chatid,
                    photos,
                )
                await bot.send_message(
                    chatid,
                    f"Девушка {data_split[1]}",
                    reply_markup=nav.girl_photos_actions(len(photos_names)),
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


@dp.message_handler(state=ClientState.VIDEO_CONVERT, content_types=["video"])
async def videoToCircle(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    file_info = await bot.get_file(message.video.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    with open("source.mp4", "wb") as new_file:
        new_file.write(downloaded_file.getvalue())
    clip = VideoFileClip("source.mp4")
    clip = clip.subclip(0, min(clip.duration, 60))
    fl_size = min(clip.size + tuple([630]))
    final_clip = CompositeVideoClip(
        [clip.set_position(("center"))],
        size=(fl_size, fl_size),
    )
    final_clip.write_videofile(r"cropped_video.mp4", logger=None)
    with open("cropped_video.mp4", "rb") as circle:
        await bot.send_video_note(chatid, circle, reply_markup=nav.msg_desc_hide)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
