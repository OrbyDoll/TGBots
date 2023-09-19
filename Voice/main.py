from aiogram import Bot, Dispatcher, executor, types

import config as cfg
import markups as nav


bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.chat.type == "private":
        await bot.send_message(
            message.chat.id, "Выберите категорию📋", reply_markup=nav.categor_choose
        )


@dp.callback_query_handler()
async def callback(call: types.CallbackQuery):
    chatid = call.message.chat.id
    if call.data.startswith("cat_"):
        choosed_category = call.data[4:]
        await bot.send_message(
            chatid,
            "Выберите файл📋",
            reply_markup=nav.get_category_page(choosed_category, 1),
        )
    elif call.data.startswith("page_"):
        data_split = call.data.split()
        choosed_category = data_split[2]
        page = int(data_split[1])
        await bot.edit_message_reply_markup(
            chatid,
            call.message.message_id,
            call.message.message_id,
            nav.get_category_page(choosed_category, page),
        )
    else:
        try:
            open_file = open(f"Voice/files/{call.data}.ogg", "rb")
            await bot.send_audio(chatid, open_file)
        except Exception as e:
            print(e)
            await bot.send_message(chatid, "Этот файл недоступен⛔️")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
