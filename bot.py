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
admin_ids = [415275008, 284539277, 616305943, 881704893]

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
        members_statuses = ['creator', 'administrator', 'member', 'restricted']
        if chat_member.status in members_statuses:
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

async def get_photo_url_of_user(user_id):
    try:
        photos = await bot.get_user_profile_photos(user_id)
    
        file_info = await bot.get_file(photos.photos[0][-1].file_id)
            
            # Получаем URL файла
        file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_info.file_path}"
        return file_url
    except:
        return 'https://telegra.ph/file/99e7fb4ff14703f8d0d7f.png'
    
@dp.message_handler(commands=['ref_link'])
async def get_users_ref_link_handler(message: types.Message):
    from dbmethods import find_user_by_telegram_id
    user = await find_user_by_telegram_id(message.from_user.id)
    if user:
        message_text = f'''
    Invite friends and get 50k $BRD + 10% from income of each friend
    {official_channel_link + f'?start={user.invitation_code}'}
    '''
        
        await message.answer(message_text)

@dp.message_handler(commands=['social'])
async def social_networks_handler(message: types.Message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Discord', url='discord.com'))
    kb.add(types.InlineKeyboardButton('Twitter', url='https://x.com/tappybirdd?s=21'))
    kb.add(types.InlineKeyboardButton('Telegram', url='https://t.me/tappy_bird'))
    await message.answer('Join our community!', reply_markup=kb)

@dp.message_handler()
async def handler(message:types.Message):
    from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
    referal_code = message.get_args()
    
    if  not referal_code:
        referal_code = ''
    keyboard = InlineKeyboardMarkup()
    if message.from_user.id in admin_ids:
        keyboard.add(InlineKeyboardButton(text='Админка', web_app=WebAppInfo(url='https://tappyback.ton-runes.top/admin?login=admin&password=admin')))
    keyboard.add(  InlineKeyboardButton(text='Играть', web_app= WebAppInfo(url='https://tappybirdfront.vercel.app/'+str(referal_code))))
    await message.answer('''
Welcome to Tappy Bird!
we are a new project on ton blockchain .
Hurry up and go to the app to break all the eggs and get unique birds and $BRD tokens!🐣
Complete tasks and invite friends to get extra rewards ✅
''', reply_markup=keyboard)
   

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
