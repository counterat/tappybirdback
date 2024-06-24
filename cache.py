import aioredis
import json
from datetime import datetime, timedelta
from config import *
import requests
import asyncio
from dbmethods import choose_bird_for_user, append_bird_to_user, find_user_by_id
from globalstate import global_state, get_global_variable, set_global_variable, get_leaderboard_state, set_leaderboard_state
loop = asyncio.get_event_loop()

""" {"user_id":{"time_worked" :0, "time_remained_to_work":12*60*60}} """
r = aioredis.from_url("redis://16.170.242.255:6379", password="XGaaNySprD3", decode_responses=True)
async def get_last_task():
    keys = await r.hkeys("all_tasks")
    print(keys)
    # Нахождение последнего ключа по времени
    latest_key = max(keys, key=int)
    print(latest_key)
    latest_value = await r.hget('all_tasks', latest_key)
    print(latest_value, type(latest_value))
    elements = await r.hgetall('all_tasks')
    return json.loads(latest_value)
""" asyncio.run(get_last_task()) """
""" r.set('key', 'value') """

""" r.set('booster', "{}") """
""" r.set('users', json.dumps({1:{}})) """

async def find_telegram_id(link):
    user_data = await r.hget('telegram_ids', link)
    user_data = json.loads(user_data)
    return user_data

async def find_user_in_cache(user_id):
    user_data = await r.hget('users', user_id)
    user_data = json.loads(user_data)
    return user_data

async def find_squad_in_cache(squad_id):
    squad_data = await r.hget('squads', squad_id)
    squad_data = json.loads(squad_data)
    return squad_data

async def find_task_in_cache(task_id):
    task_data = await r.hget('all_tasks', task_id)
    task_data = json.loads(task_data)
    return task_data

async def find_task_in_region_in_cache(geo):
    tasks_data = await r.hget('tasks', geo)
    tasks_data = json.loads(tasks_data)
    return tasks_data

async def new_task(key,value):
    # Сериализация значения в JSON формат
    value_json = json.dumps(value)
    await r.hset('all_tasks',value['id'], value_json )
    # Установка значения в хэш-ключе
    value_json = await r.hget('tasks', key)
    value_json = json.loads(value_json)
    print(value_json, type(value_json))
    value_json.append(value)

    await r.hset('tasks', key, json.dumps(value_json))
    
    
    return (value)

async def new_telegram_id(link, tgid):
    await r.hset('telegram_ids', link, tgid)
    chat_id = await r.hget('telegram_ids', link)
    return chat_id

async def new_user(key, value):
    # Сериализация значения в JSON формат
    value_json = json.dumps(value)
    # Установка значения в хэш-ключе
    await r.hset('users', key, value_json)
    value_json = await r.hget('users', key)
    return (value_json)

async def new_squad_in_cache(key, value):
    # Сериализация значения в JSON формат
    value_json = json.dumps(value)
    # Установка значения в хэш-ключе
    await r.hset('squads', key, value_json)
    value_json = await r.hget('squads', key)
    return json.loads(value_json)

updated_diffs = []

def unix_time(str_date):
    time_obj = datetime.fromisoformat(str_date)
    return time_obj


async def click_for_autoclicker_users():
    users = await r.hkeys('users')
    for user_id in users:
        if user_id !='':
            
            value_json = await r.hget('users', int(user_id))
            value_dict = json.loads(value_json)
            boosters_dict = value_dict.get('boosters')
            if boosters_dict['tap bot'] !={}:
                time_for_expiring_autoclickers = await find_tap_bot_in_cache(int(user_id))
                print(time_for_expiring_autoclickers)
                if time_for_expiring_autoclickers['time_remained_to_work'] <= 0:
                    pass
                else:
                    connected_users = get_global_variable()
                    if int(user_id)not in connected_users:
                        await mine_brd(user_id, True)
                        time_for_expiring_autoclickers['time_remained_to_work'] -= 60
                        time_for_expiring_autoclickers['time_worked'] +=60
                        await update_tap_bot(int(user_id), time_for_expiring_autoclickers)
                    print(f'{connected_users}autoimm{user_id}{int(user_id) in connected_users}'*10)

async def update_all_users_income_per_day():
    user_ids = await r.hkeys('users')
    for user_id in user_ids:
        if user_id != '':
            await update_income_per_day(user_id)

async def get_user_and_his_income_for_ref(user_id):
    user_data = await r.hget('users', user_id)
    user_data = json.loads(user_data)
    data = {
        'coin':user_data['income_for_ref']
    }
    return data

async def update_income_per_day(key):
    async with r.pipeline(transaction=True) as pipe:
        try:
            
            await pipe.watch(f'users:{key}')
            user_data = await pipe.hget('users', key)
            user_data = json.loads(user_data)
            income_for_ref = user_data["income_for_ref"]
            if user_data['income_per_this_day'] > 0:

                income_for_ref += round(user_data['income_per_this_day'] * 0.1)
           
            user_data['income_per_this_day'] = 0
            await pipe.hset(f'users',f'{key}', json.dumps({
                **user_data,
            }))
            await pipe.execute()
            return user_data
        except Exception as e:
            await pipe.reset()
            print(f'{e}'*100)
            raise e

async def get_money_for_the_ref(lord_id, ref_id ):
    lord = await find_user_in_cache(lord_id)
    ref = await find_user_in_cache(ref_id)
    income_for_ref = ref['income_for_ref']
    ref['income_for_ref'] = 0
    lord['coins'] += income_for_ref
    await r.hset('users', f'{lord_id}', json.dumps(
        lord
    ))
    await r.hset('users', f'{ref_id}', json.dumps(
        ref

    ))
    return lord
async def update_tap_bot(key, new_value):
    async with r.pipeline(transaction=True) as pipe:
        try:
            
            await pipe.watch(f'tapbots:{key}')
            await pipe.hset(f'tapbots',f'{key}', json.dumps({
                **new_value,
            }))
            await pipe.execute()
            return (
                {
                **new_value,
            }
            )
        except Exception as e:
            await pipe.reset()
            print(f'{e}'*100)
            raise e

async def update_task_in_geo(key, new_value):
    async with r.pipeline(transaction=True) as pipe:
        try:
            
            await pipe.watch(f'tasks:{key}')
            tasks_data = await pipe.hget('tasks', key)
            tasks_data = json.loads(tasks_data)
            tasks_data.append(new_value)
            await pipe.hset(f'tasks',f'{key}', json.dumps({
                **tasks_data,
            }))
            await pipe.execute()
            return (
                {
                **tasks_data,
            }
            )
        except Exception as e:
            await pipe.reset()
            print(f'{e}'*100)
            raise e


async def mine_brd(user_id, is_autoclicker=False):
    value_json = await r.hget('users', user_id)
    is_hammer = False
    value_dict = json.loads(value_json)
    brds_for_tap = 1
    boosters_dict = value_dict.get('boosters')
    hammers_dict = value_dict.get('hammers')
    current_level_of_egg = value_dict['current_level_of_egg']
    hammer = None
    if boosters_dict.get('multitap') !={}:
        brds_for_tap += 1*boosters_dict['multitap']['buff_level']
    if hammers_dict.get('diamond hammer'):
        is_hammer = True
        hammer = 'diamond hammer'
        egg = eggs[current_level_of_egg]
        remained_hps_for_egg = egg['hp'] - value_dict['exp']
        damage = shop_items[hammer]['damage']
        if damage*egg['hp'] > remained_hps_for_egg:
            brds_for_tap = remained_hps_for_egg
        else:
            brds_for_tap = damage*egg['hp']
    if hammers_dict.get('gold hammer'):
        is_hammer = True
        hammer = 'gold hammer'
        egg = eggs[current_level_of_egg]
        remained_hps_for_egg = egg['hp'] - value_dict['exp']
        damage = shop_items[hammer]['damage']
        if damage*egg['hp'] > remained_hps_for_egg:
            brds_for_tap = remained_hps_for_egg
        else:
            brds_for_tap = damage*egg['hp']
    if hammers_dict.get('stone hammer'):
        is_hammer = True
        hammer = 'stone hammer'
        egg = eggs[current_level_of_egg]
        remained_hps_for_egg = egg['hp'] - value_dict['exp']
        damage = shop_items[hammer]['damage']
        if damage*egg['hp'] > remained_hps_for_egg:
            brds_for_tap = remained_hps_for_egg
        else:
            brds_for_tap = damage*egg['hp']

    if is_autoclicker:
        if not is_hammer:
            if 60*brds_for_tap > 180:
                brds_for_tap = 3
        result = await update_user_energy_and_coin_balance_transaction(user_id, -60*brds_for_tap,  60*brds_for_tap, )
        current_level_of_egg = result['current_level_of_egg']
        hp_for_egg = eggs[current_level_of_egg]['hp']
        if result['exp'] >= hp_for_egg:
            if current_level_of_egg == 7:
                return 'buy egg'
            bird_id = await choose_bird_for_user(user_id, current_level_of_egg)
            if bird_id == 'all':
                return 'buy egg'
            bird = BIRDLIST[bird_id-1]

            result['current_level_of_egg'] += 1

            await add_user_level_of_egg(user_id)
            exp_result  = await update_exp(user_id, 0)
            result['exp'] = exp_result['exp']
            result['new_bird']  = bird
            await append_bird_to_user(user_id, bird['id'])
    else:
        if not is_hammer:
            result = await update_user_energy_and_coin_balance_transaction(user_id, -1*brds_for_tap, brds_for_tap)
        else:
            await setNoneHammer(user_id, hammer)
            print(brds_for_tap, 'brds_for_tap' )
            result = await update_user_energy_and_coin_balance_transaction(user_id, 0, brds_for_tap)


        print(f'{result}'*2)
        current_level_of_egg = result['current_level_of_egg']

        hp_for_egg = eggs[current_level_of_egg]['hp']
        result['brds_for_tap'] = brds_for_tap
        print(current_level_of_egg, hp_for_egg, result['exp'], "loh")
        if result['exp'] >= hp_for_egg:
            if current_level_of_egg == 7:
                return 'buy egg'
            bird_id = await choose_bird_for_user(user_id, current_level_of_egg)
            if bird_id == 'all':
                return 'buy egg'
            bird = BIRDLIST[bird_id-1]

            result['current_level_of_egg'] += 1

            await add_user_level_of_egg(user_id)
            exp_result  = await update_exp(user_id, 0)
            result['exp'] = exp_result['exp']
            result['new_bird']  = bird
            await append_bird_to_user(user_id, bird['id'])
    return result
import decimal

async def setNoneHammer(user_id, item_name):
    async with r.pipeline(transaction=True) as pipe:
        try:
            shop_item = shop_items[item_name]
            await pipe.watch(f'users:{user_id}')
            user_data = await pipe.hget('users', user_id)
            user_data = json.loads(user_data)
            hammers_dict = user_data['hammers']
            hammers_dict[item_name] = {}
            print(f'{hammers_dict}'*30)
            pipe.multi()
            await pipe.hset(f'users',f'{user_id}', json.dumps({
                **user_data,
            }))
            await pipe.execute()
            return (
                {
                **user_data,
            }
            )
        except Exception as e:
            await pipe.reset()
            print(f'{e}'*100)
            raise e
"""         
async def buy_shop_item_cache(user_id, item_name):
    async with r.pipeline(transaction=True) as pipe:
        try:
            shop_item = shop_items[item_name]
            await pipe.watch(f'users:{user_id}')
            user_data = await pipe.hget('users', user_id)
            user_data = json.loads(user_data)
            hammers_dict = user_data['hammers']
            hammers_dict[item_name] = {'is_ok':True}
            print(f'{hammers_dict}'*30)
            pipe.multi()
            await pipe.hset(f'users',f'{user_id}', json.dumps({
                **user_data,
            }))
            await pipe.execute()
            return (
                {
                **user_data,
            }
            )
        except Exception as e:
            await pipe.reset()
            print(f'{e}'*100)
            raise e """



async def squads_leaderboard_cache():
    async with r.pipeline(transaction=True) as pipe:
        squads_and_their_coins = {}
        squads_ids = await r.hkeys('squads')
        for squad_id in squads_ids:
            if squad_id != '':
                
                squads_and_their_coins[int(squad_id)] = 0
                squad_data = await pipe.hget('squads', int(squad_id))
                squad_data_list = await pipe.execute()
                for squad_data in squad_data_list:                        
                    squad_data = json.loads(squad_data)
                    users_in_this_squad = squad_data['users']
                    for user_id in users_in_this_squad:
                        user = await find_user_in_cache(user_id)
                        squads_and_their_coins[int(squad_id)] += user['coins']
        print(squads_and_their_coins, 'squads_and_their_coins')
        sorted_squads = sorted(squads_and_their_coins.items(), key=lambda item: item[1], reverse=True)

    # Преобразование обратно в словарь (если необходимо)
        sorted_squads_dict = dict(sorted_squads)
        return sorted_squads_dict
    
async def users_leaderboard_cache():
    async with r.pipeline(transaction=True) as pipe:

            user_ids = await r.hkeys('users')
            users_and_their_coins = []
            for user_id in user_ids:
                if user_id != '':
                    user_data = await pipe.hget('users', (user_id))
                    user_data_list = await pipe.execute()
                    for user_data in user_data_list:
                        
                        user_data = json.loads(user_data)
                        users_and_their_coins.append({  int(user_id) :user_data['coins']})
            sorted_users = sorted(users_and_their_coins, key=lambda x: list(x.values())[0], reverse=True)
            print(sorted_users)
            return sorted_users

async def append_completed_tasks_to_user(user_id, task_id):
    async with r.pipeline(transaction=True) as pipe:
        try:
            # Начинаем транзакцию
            await pipe.watch(f'users:{user_id}')
            user_data = await pipe.hget('users', user_id)
            user_data = json.loads(user_data)
            completed_tasks = user_data['completed_tasks']  
            completed_tasks.append(task_id)
            user_data['completed_tasks']  = completed_tasks
            if not user_data:
                raise ValueError("User not found")
            await pipe.hset(f'users',f'{user_id}', json.dumps({
                **user_data,
                
                
            }))

    
            results =await pipe.execute()
      
            return {**user_data}

        except Exception as e:
            await pipe.reset()
            raise e


async def choose_random_level(user_id):
    user = await find_user_by_id(user_id)
    birds = user.birds 
    allowed_tiers = []
    for i in range(1,6):
        print(i)
        tier = tiers[i]
        result = all(elem in birds for elem in tier)
        if not result:
            allowed_tiers.append(i)
    print(allowed_tiers)
    if allowed_tiers:
        import random
        choice  =random.choice(allowed_tiers)
        print(choice, 'choice')
        return choice+1
    else:
        return 'no more eggs'
        
async def lol():
    result = await choose_random_level(9324290)
    print(result)
asyncio.run(lol())
async def buy_shop_item_cache(user_id, item_name):
    async with r.pipeline(transaction=True) as pipe:
        try:
            shop_item = shop_items[item_name]
            await pipe.watch(f'users:{user_id}')
            user_data = await pipe.hget('users', user_id)
            user_data = json.loads(user_data)
            if 'hammer' in item_name:
                hammers_dict = user_data['hammers']
                hammers_dict[item_name] = {'is_ok':True}
                print(f'{hammers_dict}'*30)
            elif 'random' in item_name:
                random_level = await choose_random_level(user_id)
                if random_level == 'no more eggs':
                    return random_level
                user_data['current_level_of_egg'] = random_level
                user_data['exp'] = 0
            pipe.multi()
            await pipe.hset(f'users',f'{user_id}', json.dumps({
                **user_data,
            }))
            await pipe.execute()
            return (
                json.dumps({
                **user_data,
            })
            )
        except Exception as e:
            await pipe.reset()
            print(f'{e}'*100)
            raise e

""" 
async def new_user(key, value):
    # Сериализация значения в JSON формат
    value_json = json.dumps(value)
    # Установка значения в хэш-ключе
    await r.hset('users', key, value_json)
    value_json = await r.hget('users', key)
    return (value_json)
 """
""" async def find_user_in_cache(user_id):
    user_data = await r.hget('users', user_id)
    user_data = json.loads(user_data)
    return user_data
 """
async def add_tap_bot(key,value):
    value_json = json.dumps(value)
    # Установка значения в хэш-ключе
    await r.hset('tapbots', key, value_json)
    value_json = await r.hget('tapbots', key)
    return (value_json)
async def find_tap_bot_in_cache(user_id):
    try:
        user_data = await r.hget('tapbots', user_id)
        user_data = json.loads(user_data)
        return user_data
    except Exception as ex:
        print(ex)
async def buy_booster_cache(user_id, price, times_booster_was_bought_by_user, booster_name):
    async with r.pipeline(transaction=True) as pipe:
        try:
            await pipe.watch(f'users:{user_id}')
            user_data = await pipe.hget('users', user_id)
            user_data = json.loads(user_data)
            if booster_name == 'tap bot':
                if user_data['boosters']['tap bot'] != {}:
                    return 
            
       
            if price <= user_data['coins']:
                new_coins = float(decimal.Decimal(str(user_data['coins'])) - decimal.Decimal(str(price)))
                pipe.multi()
                user_data['boosters'][booster_name] ={
"buff_level":times_booster_was_bought_by_user+1,
"bought_at" : datetime.isoformat(datetime.now()),
            }    
                user_data['coins'] = new_coins
                if booster_name == 'max energy':
                    
                    user_data['max_energy'] += 500
                    
                if booster_name =='tap bot':
                    await add_tap_bot(user_id,{"time_worked" :0, "time_remained_to_work":60} )
                   

                await pipe.hset(f'users',f'{user_id}', json.dumps({
                **user_data,
                "coins":new_coins
            }))
                results =await pipe.execute()
                return ({ 
                **user_data,
                "coins":new_coins
            })
            else:
                return 'not enough money'
        except Exception as e:
            await pipe.reset()
            raise e

async def update_exp(user_id, value):
    async with r.pipeline(transaction=True) as pipe:
        try:
            # Начинаем транзакцию
            await pipe.watch(f'users:{user_id}')
            user_data = await pipe.hget('users', user_id)
            user_data = json.loads(user_data)
            if not user_data:
                raise ValueError("User not found")
            await pipe.hset(f'users',f'{user_id}', json.dumps({
                **user_data,
                "exp": value
                
            }))

    
            results =await pipe.execute()
      
            return {**user_data,
                "exp": value}

        except Exception as e:
            await pipe.reset()
            raise e

async def update_squad_users(squad_id, users):
    async with r.pipeline(transaction=True) as pipe:
        try:
            # Начинаем транзакцию
            await pipe.watch(f'squads:{squad_id}')
            squad_data = await pipe.hget('squads', squad_id)
            squad_data = json.loads(squad_data)
            if not squad_data:
                raise ValueError("User not found")
            await pipe.hset(f'squads',f'{squad_id}', json.dumps({
                **squad_data,
                "users": users
                
            }))

    
            results =await pipe.execute()
      
            return {
                **squad_data,
                "users": users
                
            }

        except Exception as e:
            await pipe.reset()
            raise e

async def add_user_level_of_egg(user_id):
    async with r.pipeline(transaction=True) as pipe:
        try:
            # Начинаем транзакцию
            await pipe.watch(f'users:{user_id}')
            user_data = await pipe.hget('users', user_id)
            user_data = json.loads(user_data)
            if not user_data:
                raise ValueError("User not found")
            await pipe.hset(f'users',f'{user_id}', json.dumps({
                **user_data,
                "current_level_of_egg": user_data['current_level_of_egg']+1
                
            }))

    
            results =await pipe.execute()
      
            return {**user_data,
                "current_level_of_egg": user_data['current_level_of_egg']+1}

        except Exception as e:
            await pipe.reset()
            raise e
import random

async def get_random_egg(user_id):
    numbers = [2, 3, 4, 5, 6]
    weights = [0.1, 0.225, 0.225, 0.225, 0.225] 
    async with r.pipeline(transaction=True) as pipe:
        try:
            # Начинаем транзакцию
            await pipe.watch(f'users:{user_id}')

            # Получаем текущие данные пользователя
            user_data = await pipe.hget('users', user_id)
            user_data = json.loads(user_data)

            if not user_data:
                raise ValueError("User not found")
            pipe.multi()
            random_level = random.choices(numbers, weights)
            user_data['current_level_of_egg'] = random_level
            await pipe.hset(f'users',f'{user_id}', json.dumps({
                **user_data,
             
            }))

    
            results =await pipe.execute()
         
            return {**user_data,
                }

        except Exception as e:
            await pipe.reset()
            raise e


async def update_user_energy_and_coin_balance_transaction(user_id, delta_energy, delta_coins, is_energy_replenishment = False, telegram_id=''):
    new_updated = datetime.isoformat(datetime.now())
    async with r.pipeline(transaction=True) as pipe:
        try:
            # Начинаем транзакцию
            await pipe.watch(f'users:{user_id}')

            # Получаем текущие данные пользователя
            user_data = await pipe.hget('users', user_id)
            user_data = json.loads(user_data)

            if not user_data:
                raise ValueError("User not found")
            current_currency = int(user_data.get("coins", 0))
            current_total_coins_were_clicked = int(user_data.get('total_coins_were_clicked',0))
            current_energy = int(user_data.get("energy", 0))
            current_exp = int(user_data.get("exp", 0))
            current_last_time_updated = user_data.get('last_updated')
            last_hundred_clicks = user_data.get('last_hundred_clicks')
            income_per_this_day = user_data['income_per_this_day']
            if not last_hundred_clicks:
                new_hundred_clicks = []
            if delta_coins ==0:
                new_updated = current_last_time_updated
            if current_last_time_updated:
                diff = unix_time(new_updated)-unix_time(current_last_time_updated)
                updated_diffs.append(diff.total_seconds()*1000)

                if last_hundred_clicks or last_hundred_clicks==[]:
                    new_hundred_clicks = last_hundred_clicks

                    if len(last_hundred_clicks) >=100:
                        last_hundred_clicks.pop()
                        last_hundred_clicks.append(diff.total_seconds()*1000)
                        new_hundred_clicks = last_hundred_clicks
                        if ((sum(new_hundred_clicks)/len(new_hundred_clicks) -min(new_hundred_clicks))) / 50 < 6:
                            return 'autoclicker!!!'
                        
                        
                    else:
                        last_hundred_clicks.append(diff.total_seconds()*1000)
                        new_hundred_clicks = last_hundred_clicks
            # Обновляем данные пользователя
            new_income_per_this_day = income_per_this_day + delta_coins
            new_currency = current_currency + delta_coins
            new_current_total_coins_were_clicked = current_total_coins_were_clicked+delta_coins
            new_energy = current_energy + delta_energy
            new_exp = current_exp+ delta_coins
            if new_energy > user_data['max_energy']:
                new_energy = user_data['max_energy']
            
            if new_energy == user_data['max_energy']:
                if is_energy_replenishment:
                    message_text = f'Ваша энергия переполнена! Возвращайтесь в бота!'

                                # Формируем URL для отправки сообщения
                    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

                                        # Параметры запроса
                    params = {
                                            'chat_id': telegram_id,
                                            'text': message_text
                                        }

                                        # Отправляем POST-запрос к API Telegram для отправки сообщения
                    response = requests.post(send_message_url, json=params)

            if delta_energy>0 and  new_energy < 0:
                raise ValueError("Not enough energy")

            # Обновляем Redis
         
            pipe.multi()


            await pipe.hset(f'users',f'{user_id}', json.dumps({
                **user_data,
                "income_per_this_day":new_income_per_this_day,
                "coins": new_currency,
                "energy": new_energy,
                "last_updated": new_updated,
                'last_hundred_clicks':new_hundred_clicks,
                'total_coins_were_clicked':new_current_total_coins_were_clicked,
                "exp":new_exp
            }))

    
            results =await pipe.execute()
         
            return {**user_data,
                    "income_per_this_day":new_income_per_this_day,
                "coins": new_currency,
                "energy": new_energy,
                "last_updated": new_updated,
                'last_hundred_clicks':new_hundred_clicks,
                'total_coins_were_clicked':new_current_total_coins_were_clicked,
                "exp":new_exp
                }

        except Exception as e:
            await pipe.reset()
            raise e



  



# Запуск event loop


""" 
loop.run_until_complete(set_value("888",{'energy':0})) """
""" 
loop.run_until_complete(update_user_energy_and_coin_balance_transaction(888, 5000, 0)) """