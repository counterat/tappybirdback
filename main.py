from bot import  is_user_in_channel, get_chat_id, extract_username
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi import FastAPI, WebSocket, Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import  uvicorn

from validating import validate_init_data as validate_initdata
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from dbmethods import *
from cache import *
from globalstate import global_state, get_global_variable, set_global_variable,get_leaderboard_state, set_leaderboard_state
from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pyrogram import Client, filters
from pyrogram.enums.parse_mode import ParseMode
pyro = Client(api_id= 28840087, api_hash='6a265aad5106ab6bad02c5e5044e73d1', name = 'myacc')
async def has_commented(user_id: int, chat_href: int) -> bool:
    async with pyro:
        username = extract_username(chat_href)
        result = pyro.get_chat_history(f'@{username}')
        
        async for message in result :
            if message.from_user:
                if message.from_user.id == user_id:
                    return True
                    
import jwt
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/admin", response_class=HTMLResponse)
async def get_admin_page(request: Request, login: str = None, password: str = None):
    if auth_by_login_and_password(login, password):
        return templates.TemplateResponse("admin.html", {"request": request, "title": "Admin Panel"})
    return HTTPException(403)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
async def update_all_users_energy():
    try:
        async with r.pipeline(transaction=True) as pipe:
            hk = await r.hkeys('users')
            for user_id in hk:
                print(user_id, 'coach')
                if user_id == '':
                    continue
                user_id = int(user_id)
                try:
                    user_data = await r.hget('users', user_id)
                    if user_data:
                        
                        user_data = json.loads(user_data)
                  
                        if user_data['energy'] < user_data['max_energy']:
                            
                            user = await find_user_by_id(int(user_id))
                            if user_data['energy'] + 6 > user_data['max_energy']:
                                
                                delta_energy = user_data['max_energy'] - user_data['energy']
                                print(delta_energy, 'kros'*100)
                                res = await update_user_energy_and_coin_balance_transaction(int(user_id), delta_energy, 0, True, user.telegram_id)
                                web_app_url = 'https://tappybirdfront.vercel.app/'
                                inline_keyboard_button = {
    "text": "Open WebApp",
    "web_app": {
        "url": web_app_url
    }
}
                                message_text = f'''
Energy recharged! ⚡️Time to collect $BRD and Birds
'''     
                                reply_markup = {
    "inline_keyboard": [[inline_keyboard_button]]
}

                                # Формируем URL для отправки сообщения
                                send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

                                                    # Параметры запроса
                                params = {
                                                        'chat_id': user.telegram_id,
                                                        'text': message_text,
                                                        'reply_markup': reply_markup
                                                    }

                                                    # Отправляем POST-запрос к API Telegram для отправки сообщения
                                response = requests.post(send_message_url, json=params)
                            else:
                                print('pidor'*100)
                                delta_energy = 6
                                res = await update_user_energy_and_coin_balance_transaction(int(user_id), delta_energy, 0, True, user.telegram_id)
                            
                            print(res['energy'], 'ahah'*100)
                            
                            print(res, 'res')
                            res['id'] = int(user_id)
                            await broadcast_message(json.dumps({"eventname": "energy_replenishment", **res}))
                except Exception as ex:
                    print(f"Error processing user {user_id}: {ex}")
    except Exception as e:
        print(f"Error in update_all_users_energy: {e}")


scheduler = AsyncIOScheduler()
scheduler.add_job(click_for_autoclicker_users, 'interval', seconds=60)
scheduler.add_job(update_all_users_energy, 'interval', seconds=4) 
scheduler.add_job(msg_to_autoclickers, 'interval', hours=6)
scheduler.add_job(update_users_leaderboard, 'interval',  minutes=1) 
scheduler.add_job(update_squads_leaderboard, 'interval',  minutes=1)  
scheduler.add_job(update_all_users_income_per_day, CronTrigger(hour=0, minute=0) )
CronTrigger(hour=0, minute=0) 
""" 
 """
scheduler.start()
active_websockets: List[WebSocket] = []
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            # Пример получения сообщения от клиента (можно опустить)
            data = await websocket.receive_text()

                # Отправка сообщения всем подключенным клиентам

            await broadcast_message("Получен OK от стороннего сервера")
    except WebSocketDisconnect:
        active_websockets.remove(websocket)

async def broadcast_message(message: str):
  
    for ws in active_websockets:
        await ws.send_text(message)


@app.post('/get_coins_for_ref')
async def get_coins_for_ref(request: Request):
    data = await request.json()
    user_id = data['userId']
    ref_id = data['refId']
    user = await find_user_by_id(user_id)
    if ref_id in user.invited_users:
        lord = await get_money_for_the_ref(user_id, ref_id)
        return lord
    return HTTPException(403)
@app.post('/get_refs')
async def get_refs_for_ussser(request: Request):
    data = await request.json()

    user_id = data['userId']
    refs = await get_refs_for_user(user_id)
    return refs

@app.get('/tonconnect-manifest.json')
async def tonconnect_manifest_json(request: Request):
    return {
    "url": "https://api.tappybrd.com",                        
    "name": "tappycoin",                     
    "iconUrl": "https://telegra.ph/file/e652eb17c5f402a41e3b2.jpg"}

@app.get('/usersleaderboard')
async def users_leaderboard_handler(request:Request):
    users_leaders = get_leaderboard_state()
    return users_leaders

@app.get('/squadsleaderboard')
async def squads_leaderboard_handler(request:Request):
    squads_leaders = get_leaderboard_squad_state()
    return squads_leaders

@app.post('/buyshopitem')
async def buy_shop_item_handler(request:Request):
    try:
        data = await request.json()
        user_id = data['userId']
        item = data['item']
        print(f'{data}'*30)
        result = await buy_shop_item(int(user_id), item)
        if result == 'no more eggs':
            return 'no more eggs'
        print(f'{type(result)}'*30)
        user = await find_user_by_id(user_id)
        res =   json.loads( result)
        return {**res, **user.to_dict()}
    except Exception as ex:
        print(ex)
        return HTTPException(403)

@app.get('/fetch_all_tasks')
async def fetch_all_tasks_handler():
    tasks = await fetch_all_tasks()
    return tasks

@app.post('/delete_task')
async def delete_task_handler(request:Request):
    print(request)
    data = await request.json()
    login = data['login']
    password = data['password']
    if auth_by_login_and_password(login, password):
        taskId = data['taskId']
        fetched_tasks = await delete_task(taskId)
        return fetched_tasks
    return HTTPException(403)

@app.post('/fetch_tasks_for_geo')
async def fetch_tasks_for_geo(request:Request):
    data = await request.json()
    user_id = data['userId']
    sign  = data['sign']
    user = await find_user_by_id(user_id)
    print(data, user)
    if jwt.decode(sign, "secret_key", algorithms="HS256")['password'] == user.password:
        tasks_in_users_geo = await find_task_in_region_in_cache(user.geo)
        global_tasks = await find_task_in_region_in_cache('GLOBAL')
        tasks_to_send = [*tasks_in_users_geo, *global_tasks]
        return tasks_to_send
    return HTTPException(403)

async def handle_subscribe_on_socnet_task(user_id, task_id):
    task = await find_task_in_cache(task_id)
    action = task['action']
    user = await find_user_by_id(user_id)

    if action['action_title'] == 'subscribe':
        if action['socnet'] == 'telegram':
            href = task['href']
            print(href, 'href'*100)
            channel_id=await find_telegram_id(href)
            result = await is_user_in_channel(user.telegram_id, channel_id)
            print(result, user.telegram_id, channel_id,  'resultisheee'*100)
            if result:
                await append_completed_tasks_to_user(user_id, task_id)
                user = await update_user_energy_and_coin_balance_transaction(user_id, 0, task['reward'])
                
                await update_tappy_balance(user_id, task['reward_in_tappy'])
                user_in_db = await find_user_by_id(user_id)

                return {**user, **user_in_db.to_dict()}
            return HTTPException(403)
        await append_completed_tasks_to_user(user_id, task_id)
        user = await update_user_energy_and_coin_balance_transaction(user_id, 0, task['reward'])
        await update_tappy_balance(user_id, task['reward_in_tappy'])
        user_in_db = await find_user_by_id(user_id)

        return {**user,**user_in_db.to_dict()}
            
async def handle_comment_on_socnet_task(user_id,task_id):
    task = await find_task_in_cache(task_id)
    action = task['action']
    user = await find_user_by_id(user_id)
    if action['action_title'] == 'comment':
        
        if action['socnet'] == 'telegram':
            href = task['href']
            
           
            result = await has_commented(user.telegram_id,href)
            print(result, 'await has_commented(user.telegram_id,href)'*30)
            if result:
                await append_completed_tasks_to_user(user_id, task_id)
                user = await update_user_energy_and_coin_balance_transaction(user_id, 0, task['reward'])
                await update_tappy_balance(user_id, task['reward_in_tappy'])
                user_in_db = await find_user_by_id(user_id)

                return {**user, **user_in_db.to_dict()}
        else:
            await append_completed_tasks_to_user(user_id, task_id)
            user = await update_user_energy_and_coin_balance_transaction(user_id, 0, task['reward'])
            await update_tappy_balance(user_id, task['reward_in_tappy'])
            user_in_db = await find_user_by_id(user_id)

            return {**user, **user_in_db.to_dict()}

def auth_by_token(sign):
    print(jwt.decode(sign, "secret_key", algorithms="HS256"))
    if jwt.decode(sign, "secret_key", algorithms="HS256")['password'] == admin_credentials['password'] and jwt.decode(sign, "secret_key", algorithms="HS256")['login'] == admin_credentials['login']:
        return True
def auth_by_login_and_password(login, password):
    if login == admin_credentials['login'] and password == admin_credentials['password']:
        return True

async def handler_creating_task_for_only_one_task(data):
                    link_to_banner = None
                    geo = data['geo']
                    type_of_task = data['type']
                    reward = data['reward']
                    reward_in_tappy = data['reward_in_tappy']
                    action = data['action']
                    title = data['title']
                    subtasks = data.get('subtasks')
                    description = data.get('description')
                    banner_title = data.get('banner_title')
                    banner_description = data.get('banner_description')
                    if not subtasks:
                        subtasks = []
                    if action in socnet_actions_for_activity:
                        socnet = data['socnet']
                        href = data['href']

                        if socnet in socnets_available:
                            if socnet == 'telegram':
                                if not subtasks:
                                    chat_id = await get_chat_id(href)
                                    await new_telegram_id(href, chat_id)
                            last_task = await get_last_task()
                            banner_image = data.get('banner_image')
                            if banner_image:
                                image_data = base64.b64decode(banner_image)
                                image_path = f"banner_task{last_task['id']+1}.png"
                                with open(image_path, "wb") as file:
                                    file.write(image_data)
                                    link_to_banner = upload_image_to_imgur(image_path, imgur_CLIENT_ID)
                                os.remove(image_path)
                            print(last_task, type(last_task))

                            task = {
                                        "id":last_task['id']+1,
                                        "title": title,
                                        'url':f'/assets/{socnet}.png',
                                        "href": href,
                                        'reward': reward,
                                        'reward_in_tappy':reward_in_tappy,
                                        'subtasks':subtasks,
                                        "isDone": False,
                                        'action':{'action_title': f'{action}', 'socnet':f'{socnet}'},
                                    }
                            
                            if link_to_banner:
                                print(link_to_banner)
                                task['link_to_banner'] = link_to_banner
                            if banner_title and banner_description and description:
                                task['description'] = description
                                task['bannerTitle'] = banner_title
                                task['bannerDescription'] = banner_description
                            print(task , type(task))
                            task = await new_task(geo, task)
                            return task
                        
async def handle_creating_task(data):
            geo = data['geo']
            type_of_task = data['type']
            if geo in list(regions.keys()):
                if type_of_task == 'simple':
                    result = await handler_creating_task_for_only_one_task(data)
                    return result
                elif type_of_task == 'complex':
                    subtasks = data['subtasks']
                    subtasks_for_new_task = []
                    for subtask in subtasks:
                        new_subtask =  await handler_creating_task_for_only_one_task(subtask)
                        subtasks_for_new_task.append(new_subtask['id'])

                        if not new_subtask:
                            return False
                    data['subtasks'] = subtasks_for_new_task
                    print(data['subtasks'], 'lol')
                    result = await handler_creating_task_for_only_one_task(data)
                    print(result)
                    return True
import base64
import os
def upload_image_to_imgur(image_path, client_id):
    headers = {
        'Authorization': f'Client-ID {client_id}'
    }

    with open(image_path, 'rb') as image_file:
        data = {
            'image': image_file,
            'type': 'file'
        }
        response = requests.post('https://api.imgur.com/3/image', headers=headers, files=data)

    if response.status_code == 200:
        result = response.json()
       
        return result['data']['link']
    else:
        raise Exception(f"Failed to upload image: {response.status_code} - {response.text}")

@app.post('/distribute_message')
async def distribute_message(request: Request):
    data = await request.json()
    sign = data.get('sign')
    message = data.get('message')
    if sign:
        result = auth_by_token(sign)
        print(result)
        if result:
            await ditribute_message_work(message)
            return {'is_ok':True}
    return HTTPException(403)

@app.post('/create_task')
async def create_task(request: Request):
    data = await request.json()
    sign = data.get('sign')
    headers =  request.headers
 
    """ sign = headers.get('sign') """
    login = data.get('login')
    
    

    password = data.get('password')
    if sign:
        result = auth_by_token(sign)
        print(result)
        if result:
            print(result)
            result = await handle_creating_task(data)
            return {'is_ok':True}
    if login and password:
        result  = auth_by_login_and_password(login,password)
        if result:
            result = await handle_creating_task(data)
            return {'is_ok':True}

    return HTTPException(403)



@app.post('/check_is_task_completed')
async def check_is_task_completed(request: Request):
    data = await request.json()
    user_id = data['userId']
    user = await find_user_in_cache(user_id)
    task_id = data['taskId']
    task = await find_task_in_cache(task_id)
    action  = task.get('action')
    subtasks = task.get('subtasks')
    print(data)
    print(task)
    if task_id not in user['completed_tasks']:
        if subtasks:
            print('huyatina', task)
            completed_subtasks = []
            for subtask_id in subtasks:
                subtask = await find_task_in_cache(subtask_id)
                if task_id not in user['completed_tasks']:
                    if subtask['id'] not in user['completed_tasks']:
                        if subtask['action']['action_title'] == 'subscribe':
                            print(subtask['id'], task_id, 'AHAHAHAHHAH'*100)
                            if subtask['id'] != task_id:
                                print('completed_subtasks'*100)
                                result = await handle_subscribe_on_socnet_task(user_id, subtask['id'])
                                
                                print(result, 'zholtov'*100)
                                if result:
                                
                                    print("completed_subtasks.append(subtask['id'])")
                                    completed_subtasks.append(subtask['id'])
                                    result = await append_completed_tasks_to_user(user_id, subtask['id'])
                                
                        elif subtask['action']['action_title'] == 'comment':
                            result = await handle_comment_on_socnet_task(user_id, subtask['id'])
                            
                            print(result, 'zholtov'*100)
                            if result:
                                print("completed_subtasks.append(subtask['id'])")
                                completed_subtasks.append(subtask['id'])
                                result = await append_completed_tasks_to_user(user_id, subtask['id'])
                    else:
                        completed_subtasks.append(subtask['id'])
            print(completed_subtasks, subtasks, 'mudak'*100)
            print(task)
            if len(completed_subtasks) == len(subtasks):
                    user = await update_user_energy_and_coin_balance_transaction(user_id, 0, task['reward'])
                    user_in_db = await update_tappy_balance(user_id, task['reward_in_tappy'])
                    result = await append_completed_tasks_to_user(user_id, task_id)
                
                    return {**result, **user_in_db.to_dict()  }            
                                
        elif action:
            print(task['id'] not in user['completed_tasks'])
            if task['id'] not in user['completed_tasks']:
                if task['action']['action_title'] == 'subscribe':
                        result = await handle_subscribe_on_socnet_task(user_id, task['id'])
                        print(result)
                        return result
                elif task['action']['action_title'] == 'comment':
                    result = await handle_comment_on_socnet_task(user_id, task['id'])
                    print(result)
                    return result

@app.post('/check_is_user_in_channel')
async def check_is_user_in_channel(request: Request):
    data = await request.json()
    user_id = data['userId']
    task_id = data['taskId']
    task = await find_task_in_cache(task_id)
    href = task['href']
    channel_id=await find_telegram_id(href)
    result = await is_user_in_channel(user_id, channel_id)

    if result:
        await append_completed_tasks_to_user(user_id, task_id)
        user = await update_user_energy_and_coin_balance_transaction(user_id, 0, task['reward'])
        return user
    return HTTPException(403)

@app.post('/check_is_user_subscribed_on_socnet')
async def check_is_user_subscribed_on_socnet(request: Request):
    data = await request.json()
    data = await request.json()
    user_id = data['userId']
    task_id = data['taskId']
    socnet = data['socnet']
    task = await find_task_in_cache(task_id)
    href = task['href']
    channel_id=await find_telegram_id(href)
    result = True
    if result:
        await append_completed_tasks_to_user(user_id, task_id)
        user = await update_user_energy_and_coin_balance_transaction(user_id, 0, task['reward'])
        return user
    return HTTPException(403)

@app.post('/create_squad')
async def create_squad_handler(request:Request):

        data = await request.json()
        user_id = data['userId']
        sign = data['sign']
        link = data['link']
        user = await find_user_by_id(user_id)
        if user:
            if jwt.decode(sign, "secret_key", algorithms="HS256")['password'] == user.password:
             
                    result = await create_squad(user_id, link)
                    if result:
                        return result
        return HTTPException(403)

@app.post('/join_squad')
async def join_squad_handler(request:Request):

        data = await request.json()
        user_id = data['userId']
        squad_id = data['squadId']
        sign = data['sign']
        user = await find_user_by_id(user_id)
        if user:
            if jwt.decode(sign, "secret_key", algorithms="HS256")['password'] == user.password:
                result = await join_squad(user_id, squad_id)
                
                if result:
                    return {'is_ok':True}
    
        return HTTPException(403)

@app.post('/disconnect_ws')
async def disconnect_ws_handler(request:Request):
    
    try:
        data = await request.json()
        connected_users = get_global_variable()
        print(f'{connected_users}HUY'*90)
        sign = data.get('sign')
        user_id = int(data.get('user_id'))
        print(connected_users, 'before','\n'*5)
        user = await find_user_by_id(user_id)
        if user:
            if jwt.decode(sign, "secret_key", algorithms="HS256")['password'] == user.password:
                
                if not connected_users:
                    connected_users = set()
                else:
                    connected_users.remove(user_id)
                set_global_variable(connected_users)
                print(connected_users, 'after','\n'*5)
    except:
        return HTTPException(403)
@app.post('/minecoin')
async def mine_coin_handler(request: Request):
    data = await request.json()
    user_id = data['userId']
    
    # Запускаем выполнение mine_brd в фоновом режиме
    task = asyncio.create_task(mine_brd(user_id))
    
    # Дожидаемся завершения выполнения mine_brd и получаем результат
    res = await task
    
    # Возвращаем результат в зависимости от условий
    if res == 'buy egg':
        return 'buy egg'
    elif res == 'autoclicker!!!':
        return 'autoclicker!!!'
    else:
        return res
@app.post('/successful_transaction')
async def succesful_transaction(request:Request):
    data = await request.json()
    print(data)
    user_id = data['userId']
    sign = data.get('sign')
    amount = data['amount']
    if auth_by_token(sign):
        user = await top_up_balance(user_id, amount)
        print(user)
        if user:
            return user.to_dict()
    return HTTPException(403)

def auth_by_login_and_password(login, password):
    if login == admin_credentials['login'] and password == admin_credentials['password']:
        return True

@app.post('/buybooster')
async def buy_booster_handler(request:Request):
    data = await request.json()

    
    user_id = data.get('userId')
    sign = data.get('sign')
    user = await find_user_by_id(user_id)
    if user:
        if jwt.decode(sign, "secret_key", algorithms="HS256")['password'] == user.password:
            booster_name = data.get('booster_name')

            result = await buy_booster(user_id, booster_name)
            return result
    return HTTPException(403)

isTest = False
@app.get('/tonconnect-manifest.json')
async def return_tonconnect_manifest(request:Request):
    return  {
    "url": "https://api.tappybrd.com",                        
    "name": "tappybird",                     
      "iconUrl": "https://ton-connect.github.io/demo-dapp-with-react-ui/apple-touch-icon.png",
  "termsOfUseUrl": "https://ton-connect.github.io/demo-dapp-with-react-ui/terms-of-use.txt",
  "privacyPolicyUrl": "https://ton-connect.github.io/demo-dapp-with-react-ui/privacy-policy.txt"
  }
@app.post('/authorize')
async def authorize_user(request: Request):
    client_host = request.client.host
    print(client_host)
    
    if client_host != '127.0.0.1':
        country_code = get_country_by_ip(client_host)
        region = get_regions_by_country(country_code)[0]
    else:
        region = 'EUROPE'
    
    if isTest:
        tg_id = 881704893
        first_name = 'leps'
        username = 'leps'
        invit_code = 150004449
    else:
        data = await request.json()
        initdata = data['initdata']
        invit_code = data.get('invitCode')
        
        result, vals = validate_initdata(initdata, bot_token)
        if not result:
            raise HTTPException(status_code=403, detail="Unauthorized")
        vals = json.loads(vals['user'])
        print(vals, initdata, '\n*5')
        tg_id = vals['id']
        first_name = vals['first_name']
        username = vals.get('username')
    
    user = await find_user_by_telegram_id(tg_id)
    
    if user:
        connected_users = get_global_variable() or set()
        connected_users.add(user.id)
        set_global_variable(connected_users)
        
        res = await find_user_in_cache(user.id)
        response = {
            **user.to_dict(),
            **res
        }
        time_for_expiring_autoclickers = await find_tap_bot_in_cache(int(user.id))
        if time_for_expiring_autoclickers:
            if not time_for_expiring_autoclickers['time_remained_to_work']:
                time_for_expiring_autoclickers['time_remained_to_work'] = 12*60*60
                time_for_expiring_autoclickers['time_worked'] = 0
                await update_tap_bot(user.id, time_for_expiring_autoclickers)
        users_birds = [BIRDLIST[bird_id - 1] for bird_id in user.birds]
        response['birds'] = users_birds
        response['invite_link'] = official_channel_link + f'?start={user.invitation_code}'
        
        return response
    else:
        connected_users = get_global_variable() or set()
        userr = await add_user(tg_id, first_name, username, datetime.now(), invit_code, geo=region)
        conf = default_config_for_user
        if userr.invited_by:
            conf['coins'] = 50000
            conf['income_for_ref'] = 50000

        res = await new_user(userr.id, conf)
        res = json.loads(res)
        
        connected_users.add(userr.id)
        set_global_variable(connected_users)
        
        response = {
            **userr.to_dict(),
            **res
        }
        
        users_birds = [BIRDLIST[bird_id - 1] for bird_id in userr.birds]
        response['birds'] = users_birds
        response['invite_link'] = official_channel_link + f'?start={userr.invitation_code}'
        
        return response
async def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())