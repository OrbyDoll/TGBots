from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import sys
import pathlib
import config as cfg
import markups as nav
from db import Database


class ClientState(StatesGroup):
    GET_MESSAGES = State()
    ANSWER_GET_ID = State()
    ANSWER_SEND_MESSAGE = State()
    CLEAR_MESSAGES = State()


storage = MemoryStorage()
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot, storage=storage)
script_dir = pathlib.Path(sys.argv[0]).parent
db = Database(script_dir / cfg.db_file)


def get_id_from_message(message):
    result = ""
    for letter in message:
        if letter != " ":
            result += letter
        else:
            return result


@dp.message_handler(commands=["start"])
async def sendMessage(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
            db.set_nickname(f"@{message.from_user.username}", message.from_user.id)
            if (
                not message.from_user.id == cfg.admin_id
                and not message.from_user.id == cfg.glav_admin_id
            ):
                await bot.send_message(
                    message.chat.id,
                    "Привет ! Пишите сообщенияя ниже и наш админ ответит вам в ближайшее время.",
                )
            elif (
                message.from_user.id == cfg.admin_id
                or message.from_user.id == cfg.glav_admin_id
            ):
                await bot.send_message(
                    message.chat.id,
                    "Для просмотра сообщений напишите /check.",
                )
        else:
            await bot.send_message(
                message.chat.id,
                "Вы уже зарегестрированы.",
            )


@dp.message_handler(commands=["clearall"])
async def clearall(message: types.Message):
    if message.chat.type == "private":
        if message.from_user.id == cfg.glav_admin_id:
            db.clearall()


@dp.message_handler(commands=["check"])
async def cmd_check(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if (
            message.from_user.id == cfg.admin_id
            or message.from_user.id == cfg.glav_admin_id
        ):
            if len(db.get_active_users()) > 0:
                await bot.send_message(
                    message.chat.id,
                    "Выберите пользователя, сообщения которого вы хотите увидеть",
                    reply_markup=nav.get_users_markup(db),
                )
                await state.set_state(ClientState.GET_MESSAGES)
            else:
                await bot.send_message(
                    message.chat.id, "На данный момент сообщений нет."
                )
        else:
            await bot.send_message(message.chat.id, "Вы не являетесь админом!")
            return


@dp.message_handler(commands=["clear"])
async def cmd_clear(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if (
            message.from_user.id == cfg.admin_id
            or message.from_user.id == cfg.glav_admin_id
        ):
            if len(db.get_active_users()) > 0:
                await bot.send_message(
                    message.chat.id,
                    "Выберите пользователя, сообщения которого вы хотите удалить",
                    reply_markup=nav.get_users_markup(db),
                )
                await state.set_state(ClientState.CLEAR_MESSAGES)
            else:
                await bot.send_message(
                    message.chat.id, "На данный момент сообщений нет."
                )
        else:
            await bot.send_message(message.chat.id, "Вы не являетесь админом!")
            return


@dp.message_handler(commands=["answer"])
async def cmd_answer(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if (
            message.from_user.id == cfg.admin_id
            or message.from_user.id == cfg.glav_admin_id
        ):
            if len(db.get_active_users()) > 0:
                await bot.send_message(
                    message.chat.id,
                    "Выберите пользователя, на сообщение которого вы хотите ответить",
                    reply_markup=nav.get_users_markup(db),
                )
                await state.set_state(ClientState.ANSWER_GET_ID)
            else:
                await bot.send_message(
                    message.chat.id, "На данный момент сообщений нет."
                )
        else:
            await bot.send_message(message.chat.id, "Вы не являетесь админом!")
            return


# Обработка состояний
@dp.message_handler(state=ClientState.GET_MESSAGES)
async def get_messages(message: types.Message, state: FSMContext):
    desired_user = get_id_from_message(message.text)
    try:
        all_messages = db.get_messages(desired_user)[0][0].split("/")
        for msg in all_messages:
            if not msg == "None":
                await bot.send_message(
                    message.chat.id, msg, reply_markup=types.ReplyKeyboardRemove
                )
    except Exception as e:
        print(e)
        await bot.send_message(
            message.chat.id,
            "Что-то пошло не так. Попробуйте еще раз",
            reply_markup=nav.get_users_markup(db),
        )
    await state.finish()


@dp.message_handler(state=ClientState.ANSWER_GET_ID)
async def answer_get_id(message: types.Message, state: FSMContext):
    desired_user = get_id_from_message(message.text)
    await state.update_data(ANSWER_USER=desired_user)
    await bot.send_message(
        message.chat.id,
        "Напишите сообщение, которое вы хотите отправить данному пользователю.",
        reply_markup=types.ReplyKeyboardRemove,
    )
    await state.set_state(ClientState.ANSWER_SEND_MESSAGE)


@dp.message_handler(state=ClientState.ANSWER_SEND_MESSAGE)
async def answer_send_message(message: types.Message, state: FSMContext):
    user_state_data = await state.get_data()
    user_state_id = user_state_data["ANSWER_USER"]
    await bot.send_message(user_state_id, message.text)
    previous_msg = db.get_messages(user_state_id)[0][0]
    new_msg = str(previous_msg) + "/" + "Ответ:" + message.text
    await bot.send_message(message.chat.id, "Сообщение отправлено")
    db.set_messages(new_msg, user_state_id)
    await state.finish()


@dp.message_handler(state=ClientState.CLEAR_MESSAGES)
async def clear(message: types.Message, state: FSMContext):
    desired_user = get_id_from_message(message.text)
    try:
        db.set_messages(None, desired_user)
        db.set_msg_count(0, desired_user)
        await bot.send_message(
            message.chat.id, "Сообщения очищены", reply_markup=types.ReplyKeyboardRemove
        )
    except Exception as e:
        print(e)
        await bot.send_message(
            message.chat.id,
            "Что-то пошло не так. Попробуйте еще раз",
            reply_markup=nav.get_users_markup(db),
        )
    await state.finish()


# Обработка текста от обычных пользователей
@dp.message_handler(content_types=["text"])
async def add_message(message: types.Message):
    if (
        message.chat.type == "private"
        and not message.from_user.id == cfg.admin_id
        and not message.from_user.id == cfg.glav_admin_id
    ):
        user_id = message.from_user.id
        previous_messages = db.get_messages(user_id)[0][0]
        previous_msg_count = db.get_msg_count(user_id)[0][0]
        new_msg_count = previous_msg_count + 1
        if previous_messages == "":
            new_messages = message.text
        else:
            new_messages = str(previous_messages) + "/" + message.text
        db.set_messages(new_messages, user_id)
        db.set_msg_count(new_msg_count, user_id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
