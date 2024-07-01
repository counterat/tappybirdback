import asyncio
import aiohttp
import time

async def fetch_coins(session, user_id):
    url = f'https://api.tappybird.top/minecoin'
    data = {"userId": user_id}
    async with session.post(url, json=data) as response:
        result = await response.json()
        return result['coins']

async def main():
    user_ids = [9324295, 9324296, 9324289, 9324288, 9324290, 9324297]

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [fetch_coins(session, user_id) for user_id in user_ids]
            coins = await asyncio.gather(*tasks)

            print(coins)
            
            # Добавляем небольшую задержку перед следующей итерацией
            await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
