from typing import Text
from attr import make_class
import config
import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# инициализируем соединение с БД
db = SQLighter('db.db')


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.username, message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.username,
                               message.from_user.id, True)

    await message.answer("Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.username,
                          message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.username,
                               message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")


# Просто разговор
@dp.message_handler(content_types=['text'])
async def talk(message: types.Message):
    await message.answer(message.from_user.username)


# запускаем лонг поллинг
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
