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
async def get_admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request, "title": "Admin Panel"})

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

""" scheduler.add_job(update_all_users_energy, 'interval', seconds=2) 
scheduler.add_job(click_for_autoclicker_users, 'interval', seconds=60)
scheduler.add_job(update_users_leaderboard, 'interval',  minutes=1) 
scheduler.add_job(update_squads_leaderboard, 'interval',  minutes=1) 
scheduler.add_job(update_all_users_income_per_day, CronTrigger(hour=0, minute=0)) 
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
    "url": "http://127.0.0.1:8000",                        
    "name": "tappybird",                     
    "iconUrl": "data:image/jpeg;base64,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",             
}

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
                subtask = await find_task_in_cache(task_id)
                if task_id not in user['completed_tasks']:
                    if subtask['id'] not in user['completed_tasks']:
                        if subtask['action']['action_title'] == 'subscribe':
                            result = await handle_subscribe_on_socnet_task(user_id, subtask['id'])
                            if result:
                                print("completed_subtasks.append(subtask['id'])")
                                completed_subtasks.append(subtask['id'])
                            
                        elif subtask['action']['action_title'] == 'comment':
                            result = await handle_comment_on_socnet_task(user_id, subtask['id'])
                            if result:
                                print("completed_subtasks.append(subtask['id'])")
                                completed_subtasks.append(subtask['id'])
                                
            print(completed_subtasks, subtasks, 'mudak'*100)
            print(task)
            if len(completed_subtasks) == len(subtasks):
                user = await update_user_energy_and_coin_balance_transaction(user_id, 0, task['reward'])
                await update_tappy_balance(user_id, task['reward_in_tappy'])
                result = await append_completed_tasks_to_user(user_id, task_id)
                return result
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

isTest = True
@app.get('/tonconnect-manifest.json')
async def return_tonconnect_manifest(request:Request):
    return  {
    "url": "https://tappyback.ton-runes.top",                        
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
        tg_id = 6874159282
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