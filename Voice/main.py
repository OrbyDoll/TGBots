from aiogram import Bot, Dispatcher, executor, types

import config as cfg
import markups as nav
from filesMass import files_name

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)


def find_voice_desc(name, category):
    for voices in files_name[category]:
        if voices[1] == name:
            return voices[0]


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.chat.type == "private":
        await bot.send_message(
            message.chat.id, f"Приветствую, {message.from_user.username} ✅\n\nPRADA MATERIALS - универсальный, полностью бесплатный бот, позволяющий вам брать материалы для комфортной работы по любым направлениям💎\n\n🏆PRADA EMPIRE - работай с лучшим🏆", reply_markup=nav.categor_choose)


@dp.callback_query_handler()
async def callback(call: types.CallbackQuery):
    chatid = call.message.chat.id
    await bot.answer_callback_query(callback_query_id=call.id)
    if call.data.startswith("cat_"):
        choosed_category = call.data[4:]
        await bot.send_message(
            chatid,
            "Выберите файл📋",
            reply_markup=nav.get_category_page(choosed_category, 0),
        )
    elif call.data.startswith("page_"):
        data_split = call.data.split()
        choosed_category = data_split[2]
        page = int(data_split[1])
        if nav.get_category_page(choosed_category, page) == "huy":
            return
        await bot.edit_message_reply_markup(
            chatid,
            call.message.message_id,
            call.message.message_id,
            nav.get_category_page(choosed_category, page),
        )
    elif call.data == "back":
        await bot.delete_message(chatid, call.message.message_id)
    elif not call.data == "aboba":
        try:
            data_split = call.data.split('/')
            open_file = open(
                f"files/{data_split[0]}/{data_split[1]}.ogg",
                "rb",
            )
            await bot.send_message(chatid, find_voice_desc(data_split[1], data_split[0]))
            await bot.send_audio(chatid, open_file)
        except Exception as e:
            print(e)
            await bot.send_message(chatid, "Этот файл недоступен⛔️")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
