from db import *

from globalstate import set_leaderboard_state, get_leaderboard_state, set_leaderboard_squad_state, get_leaderboard_squad_state
from config import boosters, shop_items
from bot import get_chat_title
from config import *
import jwt
async def find_user_by_telegram_id(telegram_id):
    try:
        async with async_session() as session:
            async with session.begin():
                query = select(User).where(User.telegram_id == telegram_id)
                result = await session.execute(query)
                users = result.scalars().all()
                print(users[0].to_dict())
                return users[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
async def find_squad_by_link(link):
    try:
        async with async_session() as session:
            async with session.begin():
                query = select(Squad).where(Squad.link_to_squad == link)
                result = await session.execute(query)
                squad = result.scalar()
                return squad
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
async def find_squad_by_id(id):
    try:
        async with async_session() as session:
            async with session.begin():
                query = select(Squad).where(Squad.id == id)
                result = await session.execute(query)
                squad = result.scalar()
                return squad
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    

async def update_users_leaderboard():
    from cache import users_leaderboard_cache
    sorted_users = await users_leaderboard_cache()
    leaders = []
    for users_with_coins in sorted_users:
        user_id = list(users_with_coins.keys())[0]
        user = await find_user_by_id(user_id)
        print(user.to_dict(), 'stroy')
        leaders.append({
            user_id:{
                'coins':users_with_coins[user_id],
                'name':user.name
            }

        })
    set_leaderboard_state(leaders)

async def update_squads_leaderboard():
    from cache import squads_leaderboard_cache
    result = await squads_leaderboard_cache()
    print(result, 'result')
    results_to_send = []
    for squad_id in result:
        print(squad_id, 'squad_id')
        
        print(squad_id, 'squad_id')
        if squad_id != '':
            squad = await find_squad_by_id(int(squad_id))
            coins = result[squad_id]
            results_to_send.append({
                    "id":squad_id,
                    "nickname":squad.title,
                    "coins":  coins,
                    "telegram_link":squad.link_to_squad
                })
    set_leaderboard_squad_state(results_to_send)
    return results_to_send
async def find_user_by_id(id):
    try:
        async with async_session() as session:
            async with session.begin():
                query = select(User).where(User.id == id)
                result = await session.execute(query)
                users = result.scalar()
                return users
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

async def find_all_purchases(user_id, booster_name):
    try:
        async with async_session() as session:
            query = select(Booster).where(Booster.was_bought_by_user == int(user_id), Booster.booster_name==booster_name)
            result = await session.execute(query)
            return result.scalars().all()
    except Exception as ex:
        print(ex)

async def update_tappy_balance(user_id, delta_value):
    async with async_session() as session:
        user = await find_user_by_id(user_id)
        
        new_balance = user.balance_in_tappycoin + decimal.Decimal(str(delta_value))
        print(decimal.Decimal(str(delta_value)),new_balance, 'zarabotal'*100)
        update_query = update(User).where(User.id == user_id).values(balance_in_tappycoin = new_balance)
        async with session.begin():
            await session.execute(update_query)
        user = await find_user_by_id(user_id)
        print(user.to_dict(), 'silicon'*100)
        return user
async def buy_booster(user_id, booster_name):
    from cache import buy_booster_cache
    try:
        async with async_session() as session:
            async with session.begin():
                user = await find_user_by_id(user_id)
                times_booster_was_bought_by_user = len(await find_all_purchases(user_id, booster_name))
                price_booster = boosters[booster_name]['init_price'] * 2**(times_booster_was_bought_by_user)
      
                if user:
                    result = await buy_booster_cache(user.id,price_booster,  times_booster_was_bought_by_user , booster_name)
                    if not result:
                        return 'you already have this item'
                    if result == 'not enough money':
                        return 'not enough money'
                    booster_in_db = Booster(price = price_booster, booster_name=booster_name,was_bought_by_user=user_id )
                    session.add(booster_in_db)
                    return result
    except Exception as ex:
        print(ex)

async def ditribute_message_work(message):
    async with async_session() as session:
        all_users_query = select(User)
        result = await session.execute(all_users_query)
        all_users = result.scalars().all()
        for user in all_users:
            send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

                                # Параметры запроса
            params = {
                                    'chat_id': user.telegram_id,
                                    'text': message
                                }

                                # Отправляем POST-запрос к API Telegram для отправки сообщения
            response = requests.post(send_message_url, json=params)
            
async def buy_shop_item(user_id, item_name):
        from cache import buy_shop_item_cache
        async with async_session() as session:
            async with session.begin():
                user = await find_user_by_id(user_id)
                shop_item = shop_items[item_name]
                if shop_item.get('price'):
                    price = decimal.Decimal(str(shop_item['price']))
                    if user.balance_in_tappycoin >= price:
                        print(user.to_dict())
                        update_query = update(User).where(User.id == user_id).values(balance_in_tappycoin = user.balance_in_tappycoin - price )
                        shop_item_in_db = ShopItem(price = price, item_name=item_name, was_bought_by_user=user_id)
                        session.add(shop_item_in_db)
                        await session.execute(update_query)
                        result = await buy_shop_item_cache(user_id, item_name)
                        if result == 'no more eggs':
                            return 'no more eggs'
                        return result 
                else:
                    price = shop_item.get('price_in_coins')
                    shop_item_in_db = ShopItem(price = price, item_name=item_name, was_bought_by_user=user_id)
                    session.add(shop_item_in_db)
                    result = await buy_shop_item_cache(user_id, item_name)
                    return result
                
async def update_in_squad(user_id,new_value):
    async with async_session() as session:
            async with session.begin():

                    update_query = update(User).where(User.id == user_id).values(in_squad = new_value)
                    
                    await session.execute(update_query)
                    
            result = await find_user_by_id(user_id)
            return result 


async def get_refs_for_user(user_id):
    from cache import get_user_and_his_income_for_ref
    async with async_session() as session:
        user = await find_user_by_id(user_id)
        refs_to_send = []
        invited_by_user = user.invited_users
        for invited_user in invited_by_user:
            invited_user = await find_user_by_id(invited_user)
            invited_user_and_his_money = await get_user_and_his_income_for_ref(invited_user.id)
            invited_user_and_his_money['title'] = invited_user.name
            invited_user_and_his_money['id'] = invited_user.id
            invited_user_and_his_money['url'] = ''
            refs_to_send.append(invited_user_and_his_money)
        return refs_to_send
                
async  def find_user_by_invit_code(invit_code):
    try:
        async with async_session() as session:
            query = select(User).where(User.invitation_code == int(invit_code))
            result = await session.execute(query)
            return result.scalar()
    except Exception as ex:
        print(ex)

async def choose_bird_for_user(user_id, tier):
    async with async_session() as session:
        user = await find_user_by_id(user_id)
        birds = user.birds
        if tier > 0:
            birds_in_this_tier = tiers[tier-1]
        else:
            birds_in_this_tier = exclusive_tier[0]
        print('birds_in_this_tier', birds_in_this_tier)
        ids_of_this_tier_birds = [] 
        for bird in birds_in_this_tier:
            ids_of_this_tier_birds.append(bird['id'])
        for bird_that_user_already_have in birds:
            if bird_that_user_already_have in ids_of_this_tier_birds:
                ids_of_this_tier_birds.remove(bird_that_user_already_have)
        if ids_of_this_tier_birds:
            bird_id = random.choice(ids_of_this_tier_birds)
            return bird_id
        else:
            return 'all'
        
async def append_bird_to_user(user_id, bird_id ):
    async with async_session() as session:
        user = await find_user_by_id(user_id)
        birds = user.birds
        if user:
            birds.append(bird_id)
            update_query =  update(User).where(User.id == user_id).values(birds=birds)
            async with session.begin():
                await session.execute(update_query)
        user.birds = birds
        return birds

async def join_squad(user_id, squad_id):
    from cache import update_squad_users
    async with async_session() as session:
        user = await find_user_by_id(user_id)
        update_old_squad_query = None
        update_query = update(User).where(User.id == user_id).values(in_squad = squad_id)
        if user.in_squad:
            old_squad = await find_squad_by_id(user.in_squad)
            old_squad_users = old_squad.users
            old_squad_users.remove(user_id)
            update_old_squad_query = update(Squad).where(Squad.id == old_squad.id).values(users=old_squad_users)
            await update_squad_users(old_squad.id, old_squad_users)
        
        squad = await find_squad_by_id(squad_id)
        users_in_squad = squad.users
        users_in_squad.append(user_id)
        update_squad_query = update(Squad).where(Squad.id == squad_id).values(users=users_in_squad)
        async with session.begin():
            if update_old_squad_query is not None:
                await session.execute(update_old_squad_query)
            await session.execute(update_query)
            
            await session.execute(update_squad_query)
        squad = await find_squad_by_id(squad_id)
        print(squad.to_dict(), 'durov'*20)
        result = await update_squad_users(squad_id, users_in_squad)
        return result



async def create_squad(user_id, telegram_link):
    from cache import new_squad_in_cache
    async with async_session() as session:
        title = await get_chat_title(telegram_link)
        print(title, 'kkk'*30)
        maybe_squad = await find_squad_by_link(telegram_link)
        
        if not maybe_squad:
            if title:
                new_squad = Squad(users=[user_id], founder = user_id, title =title, link_to_squad = telegram_link)
                
            else:
                return None
            async with session.begin():
                session.add(new_squad)
            new_squad = await find_squad_by_link(telegram_link)
            print(new_squad.to_dict())
            user = await find_user_by_id(user_id)
            print(user.to_dict(),'dre'*10)
            if user.in_squad:
                from cache import update_squad_users
                        
                old_squad = await find_squad_by_id(user.in_squad)
                old_squad_users =  old_squad.users
                old_squad_users.remove(user_id)
                update_old_squad_query = update(Squad).where(Squad.id == old_squad.id).values(users=old_squad_users)
                await update_squad_users(old_squad.id,old_squad_users)
                async with session.begin():
                
                    await session.execute(update_old_squad_query)
            update_query = update(User).where(User.id == user_id).values(in_squad = new_squad.id)
            async with session.begin():
                
                await session.execute(update_query)
          
            result = await new_squad_in_cache(new_squad.id, new_squad.to_dict())
            print(f'{result}'*20)
            return result
        else:
            result = await join_squad(user_id, maybe_squad.id)
            print(result)
            async with session.begin():
            
                update_query = update(User).where(User.id == user_id).values(in_squad = result.id)
                await session.execute(update_query)
            return result

async def top_up_balance(user_id, amount):
    user = await find_user_by_id(user_id)
    if user:
        amount =  decimal.Decimal(str(amount))
        update_user_query = update(User).where(User.id == user_id).values(balance_in_tappycoin = user.balance_in_tappycoin + (amount*ton_to_tappy_currency))
        new_top_up_object = TopUps(user_id = user_id, amount = (amount*ton_to_tappy_currency) )
        async with async_session() as session:
            async with session.begin():
                await session.execute(update_user_query)
                session.add(new_top_up_object)
            user.balance_in_tappycoin += (amount*ton_to_tappy_currency)
            return user
    
async def add_user(telegram_id, name, username, created_at, invit_code, geo):

        password = str(uuid.uuid4())
        user = await find_user_by_invit_code(invit_code)
        from bot import get_photo_url_of_user
        photo_url = await get_photo_url_of_user(telegram_id)
        if not user:
            new_user = User(
                telegram_id=telegram_id,
                name=name,
                username=username,
                created_at=created_at,
                password=password,
                sign=jwt.encode({'id': telegram_id, "password": password}, 'secret_key'),
                invitation_code=random.randint(100, 2147483647),
                geo = geo,
                photo_url = photo_url

            )
        else:
            new_user = User(
            telegram_id=telegram_id,
            name=name,
            username=username,
            created_at=created_at,
            password=password,
            sign=jwt.encode({'id':telegram_id, "password":password}, 'secret_key'),
            invitation_code = random.randint(100, 2147483647),
            invited_by = user.id,
                geo = geo,
                photo_url = photo_url
        )
            send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            if not username:
                username = 'your friend'
            else:
                username = f'@{username}'
            message = f'''
Congratulations !
you have received 50k $BRD + 10% of {username}'s income for participating in the referral program !
 '''
                                # Параметры запроса
            params = {
                                    'chat_id': user.telegram_id,
                                    'text': message
                                }

                                # Отправляем POST-запрос к API Telegram для отправки сообщения
            response = requests.post(send_message_url, json=params)
        # Создание асинхронной сессии и добавление пользователя в базу данных
        async with async_session() as session:
            async with session.begin():
                print('\n'*5, new_user, '\n'*5)
                session.add(new_user)
            if user:
                from cache import update_user_energy_and_coin_balance_transaction
                await update_user_energy_and_coin_balance_transaction(user.id, 0, 50000, isref=True)
                await add_to_invited_users(session, user.id, new_user.id)
                if not user.username:
                    username = 'your friend'
                else:
                    username = f'@{user.username}'
                message = f'''
congratulations !
you have received 50k $BRD for participation in the referral program !
you have been invited by {username}
    '''
                                    # Параметры запроса
                params = {
                                        'chat_id': new_user.telegram_id,
                                        'text': message
                                    }

                                    # Отправляем POST-запрос к API Telegram для отправки сообщения
                response = requests.post(send_message_url, json=params)
        print(new_user.to_dict(), 'sosi')

        return new_user


async def add_to_invited_users(session, user_id, new_value):
    async with async_session() as session:
        async with session.begin():
            user = await find_user_by_id(user_id)
           
            array = user.invited_users
            array.append(new_value)
            await session.execute(
                update(User)
                .where(User.id == user_id)
                .values(invited_users=array)
            )   
