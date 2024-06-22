from aiogram import Bot, Dispatcher, types 
from aiogram.utils import executor

import logging
from config import *
BOT_TOKEN = '6986907470:AAFGGwdxSoYAPbOA14qi5kPKwG4uFYltD4k'
import re
# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем объект бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def extract_username(link):
    # Регулярное выражение для извлечения имени пользователя из ссылки
    match = re.search(r'https://t\.me/([a-zA-Z0-9_]+)', link)
    if match:
        return match.group(1)
    else:
        return None
async def get_chat_title(link):
    username = extract_username(link)
    print(username, 'cut'*90)
    chat = await bot.get_chat(f'@{username}')
    return chat.title

async def is_user_in_channel(user_id, channel):
    try:
        chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return chat_member
    except Exception as ex:
        print(ex)

async def get_chat_id(link):
    username = extract_username(link)
    chat = await bot.get_chat(f'@{username}')
    return chat.id
""" @dp.message_handler()
async def handler(message:types.Message):
    chat = await bot.get_chat(official_channel_id)
    await message.answer(f'{chat}')

    chat_member = await bot.get_chat_member(chat_id=official_channel_id, user_id=871704893)
    await message.answer(f'{chat_member}') """



@dp.message_handler()
async def handler(message:types.Message):
    result = await is_user_in_channel(881704893 ,-1002216118815)
    await message.answer(f'{result}')



if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    # Запустите асинхронную функцию в событийном цикле

   