from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import config as cfg
import markups as nav


class ClientState(StatesGroup):
    START = State()
    ORDER_DESCRIPTION = State()


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
    await delete_msg(message, 1)
    if message.chat.type == "private":
        await bot.send_message(
            chatid, "Стартовое сообщение", reply_markup=nav.start_menu
        )
        await state.set_state(ClientState.START)


@dp.message_handler(content_types=["text"], state=ClientState.START)
async def textMessage(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    await delete_msg(message, 2)
    try:
        if message.text == "Заказать":
            await bot.send_message(
                chatid, "Какой-то дефолтный текст", reply_markup=nav.service_choose
            )
        elif message.text == "Жалобы":
            # Хз что тут писать
            pass
            # await bot.send_message(
            #     chatid, "Какой-то дефолтный текст", reply_markup=nav.service_choose
            # )
        elif message.text == "Условия":
            # Хз что тут писать
            pass
            # await bot.send_message(
            #     chatid, "Какой-то дефолтный текст", reply_markup=nav.service_choose
            # )
    except Exception as e:
        print(e, message.text)


@dp.callback_query_handler(state=ClientState.all_states)
async def call_handler(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=call.id)
    chatid = call.message.chat.id
    messageid = call.message.message_id
    try:
        if call.data == "back_to_services":
            await bot.edit_message_text(
                "Стартовое сообщение",
                chatid,
                messageid,
                reply_markup=nav.service_choose,
            )
        elif "service" in call.data:
            service = call.data.split("_")[1]
            await bot.edit_message_text(
                nav.get_service_description(service),
                chatid,
                messageid,
                reply_markup=nav.get_service_buttons(service),
            )
        elif "price" in call.data:
            pass
        elif "works" in call.data:
            pass
        elif "order" in call.data:
            await bot.edit_message_text(
                "Кратко опишите ваш заказ и наш менеджер свяжется с вами для уточнения деталей",
                chatid,
                messageid,
            )
            await state.update_data(service=call.data.split("_")[1])
            await state.set_state(ClientState.ORDER_DESCRIPTION)
    except Exception as e:
        print(e, call.data)


@dp.message_handler(content_types=["text"], state=ClientState.ORDER_DESCRIPTION)
async def orderDescription(message: types.Message, state: FSMContext):
    chatid = message.chat.id
    try:
        state_data = await state.get_data()
        await delete_msg(message, 2)
        await bot.send_message(
            cfg.orders_chat_id,
            f'Новый заказ\nКатегория: {state_data["service"]}\nОписание: {message.text}',
        )
        await bot.send_message(
            chatid, "Стартовое сообщение", reply_markup=nav.start_menu
        )
        await state.set_state(ClientState.START)
    except Exception as e:
        print(e, "order description")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
