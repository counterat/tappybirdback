from datetime import datetime
DB_URL = 'postgresql+asyncpg://myuser:XGaaNySprD3@16.170.242.255/mydatabase'
discord_client_id = 1250527248784687155
discord_public_key = '0fe9a6df57680932784d1d0f809a6e347d445c4967f8c687620840e9decbf32c'
discord_client_secret = 'B6Q80pkS8j1qV4U3EsUZg2jlEhxj526Q'

bot_token = '6986907470:AAFGGwdxSoYAPbOA14qi5kPKwG4uFYltD4k'

official_channel_link = 'https://t.me/tappycoinbot'
admin_credentials = {
    'login':'admin',
    'password':'admin'
}

socnet_actions_for_activity = [
    'subscribe', 'comment'
]

socnets_available = [
    'youtube', 'telegram', 'discord', 'twitter'
]

official_channel_id = -1002161932839
default_config_for_user={
    "coins":0,
    "energy":5000,
    "last_hundred_clicks" : [],
    "boosters" : {
        "multitap":{
            
        },
        "max energy":{

        },
        "tap bot" :{

        }


    },
    "hammers":{
        "stone hammer":{},
        "gold hammer":{},
        "diamond hammer":{}
    },
    "current_level_of_egg":1,
    "total_coins_were_clicked":0,
    "exp":0,
    "completed_tasks":[],
    'max_energy':5000,
    "when_money_was_paid_for_user_last_time":0,
    "income_per_this_day":0,
    "income_for_ref":5000,
    "isBlocked":False
}

"""

	{
				id: 1,
				title: 'Подпишитесь на канал',
				url: '/assets/telegram.png',
				href: 'https://telegram.org/',
				isDone: false,
			},

"""

telegram_ids_for_href = {
    "https://t.me/+1DI436HJtRRmNWQy":  -1002216118815,
    'https://t.me/tappybird': -1002161932839,
    'https://t.me/chatfortesttappybird':-1002216608940
}

task3 = {
        "id":3,
        "title": "Подписаться на канал",
        'url':'/assets/telegram.png',
        "href": 'https://t.me/+1DI436HJtRRmNWQy',
		"isDone": False,
        'reward': 0,
        'reward_in_tappy':0,
       
        'action':{'action_title': 'subscribe', 'socnet':'telegram'},
    }

task4 = {
        "id":4,
        "title": "Подписаться на чат",
        'url':'/assets/telegram.png',
        "href": 'https://t.me/chatfortesttappybird',
		"isDone": False,
        'reward': 0,
        'reward_in_tappy':0,
       
        'action':{'action_title': 'subscribe', 'socnet':'telegram'},
    }
task5 = {
        "id":5,
        "title": "Оставить коммент",
        'url':'/assets/telegram.png',
        "href": 'https://t.me/chatfortesttappybird',
		"isDone": False,
        'reward': 0,
        'reward_in_tappy':0,
       
        'action':{'action_title': 'comment', 'socnet':'telegram'},
    }
""" import json
print(json.dumps(task5)) """

task1 = {
        "id":1,
        "title": "Подписаться на канал на чат и поставить комментарий",
        'url':'/assets/telegram.png',
        "href": 'https://t.me/+1DI436HJtRRmNWQy',
		"isDone": False,
        'reward': 0,
        'reward_in_tappy':0,
        'subtasks':[
            task3, task4, 
        ],
        
    }

task2 = {
        "id":2,
        "title": "Подписаться на канал ютуб",
        'url':'/assets/telegram.png',
        "href": 'https://telegram.org/',
        'reward': 5000,
        'reward_in_tappy':50,
        'subtasks':[],
		"isDone": False,
        'action':{'action_title': 'subscribe', 'socnet':'youtube'},

    }

all_tasks = [task1, task2]
imgur_api_secret = 'ab87a03bf0307ae2421ea9addad444f1752b1ddf'
imgur_CLIENT_ID = '24a97f47e7ecf1d'
default_tasks_for_all = {
    "global":[
        task1, task2



    ]


}
import requests
regions = {
    "EUROPE": ["AL", "AD", "AT", "BE", "BA", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IS", "IE", "IT", "XK", "LV", "LI", "LT", "LU", "MT", "MC", "ME", "NL", "MK", "NO", "PL", "PT", "RO", "SM", "RS", "SK", "SI", "ES", "SE", "CH", "GB", "VA"],
    "ORIENTAL": ["BH", "EG", "IR", "IQ", "IL", "JO", "KW", "LB", "OM", "PS", "QA", "SA", "SY", "TR", "AE", "YE"],
    "RUSSIA": [],
    "CIS": ["AM", "AZ", "BY", "KZ", "KG", "MD", "RU", "TJ", "TM", "UZ", "UA"],
    "ASIA": ["AF", "BD", "BT", "BN", "KH", "CN", "TL", "IN", "ID", "JP", "LA", "MY", "MV", "MN", "MM", "NP", "KP", "PK", "PH", "SG", "KR", "LK", "TW", "TH", "VN"],
    "MIDDLE ASIA": [],
    "AUSTRALIA": ["AU", "FJ", "KI", "MH", "FM", "NR", "NZ", "PW", "PG", "WS", "SB", "TO", "TV", "VU"],
    "LATIN AMERICA": ["AR", "BZ", "BO", "BR", "CL", "CO", "CR", "CU", "DM", "DO", "EC", "SV", "GD", "GT", "GY", "HT", "HN", "JM", "MX", "NI", "PA", "PY", "PE", "KN", "LC", "VC", "SR", "TT", "UY", "VE"],
    "AMERICA": ["CA", "US"],
    "АFRICA": ["DZ", "AO", "BJ", "BW", "BF", "BI", "CV", "CM", "CF", "TD", "KM", "CG", "CD", "DJ", "EG", "GQ", "ER", "SZ", "ET", "GA", "GM", "GH", "GN", "GW", "CI", "KE", "LS", "LR", "LY", "MG", "MW", "ML", "MR", "MU", "MA", "MZ", "NA", "NE", "NG", "RW", "ST", "SN", "SC", "SL", "SO", "ZA", "SS", "SD", "TZ", "TG", "TN", "UG", "ZM", "ZW"],
    "GLOBAL": []
}


BIRDLIST = [
    {
        "id": 1,
        "src": "/assets/inventory/Exclusive_1.jpg",
        "title": "Bird #1",
        "tier": "Exclusive",
    },
    {
        "id": 2,
        "src": "/assets/inventory/Exclusive_2.jpg",
        "title": "Bird #2",
        "tier": "Exclusive",
    },
    {
        "id": 3,
        "src": "/assets/inventory/Exclusive_3.jpg",
        "title": "Bird #3",
        "tier": "Exclusive",
    },
    {
        "id": 4,
        "src": "/assets/inventory/Exclusive_4.jpg",
        "title": "Bird #4",
        "tier": "Exclusive",
    },
    {
        "id": 5,
        "src": "/assets/inventory/Exclusive_5.jpg",
        "title": "Bird #5",
        "tier": "Exclusive",
    },
    {
        "id": 6,
        "src": "/assets/inventory/Exclusive_6.jpg",
        "title": "Bird #6",
        "tier": "Exclusive",
    },
    {
        "id": 7,
        "src": "/assets/inventory/Exclusive_7.jpg",
        "title": "Bird #7",
        "tier": "Exclusive",
    },
    {
        "id": 8,
        "src": "/assets/inventory/Exclusive_8.jpg",
        "title": "Bird #8",
        "tier": "Exclusive",
    },
    {
        "id": 9,
        "src": "/assets/inventory/Exclusive_9.jpg",
        "title": "Bird #9",
        "tier": "Exclusive",
    },
    {
        "id": 10,
        "src": "/assets/inventory/Exclusive_10.jpg",
        "title": "Bird #10",
        "tier": "Exclusive",
    },
    {
        "id": 11,
        "src": "/assets/inventory/Tier 1_1.jpg",
        "title": "Bird #11",
        "tier": "Tier 1",
    },
    {
        "id": 12,
        "src": "/assets/inventory/Tier 1_2.jpg",
        "title": "Bird #12",
        "tier": "Tier 1",
    },
    {
        "id": 13,
        "src": "/assets/inventory/Tier 1_3.jpg",
        "title": "Bird #13",
        "tier": "Tier 1",
    },
    {
        "id": 14,
        "src": "/assets/inventory/Tier 1_4.jpg",
        "title": "Bird #14",
        "tier": "Tier 1",
    },
    {
        "id": 15,
        "src": "/assets/inventory/Tier 1_5.jpg",
        "title": "Bird #15",
        "tier": "Tier 1",
    },
    {
        "id": 16,
        "src": "/assets/inventory/Tier 1_6.jpg",
        "title": "Bird #16",
        "tier": "Tier 1",
    },
    {
        "id": 17,
        "src": "/assets/inventory/Tier 1_7.jpg",
        "title": "Bird #17",
        "tier": "Tier 1",
    },
    {
        "id": 18,
        "src": "/assets/inventory/Tier 1_8.jpg",
        "title": "Bird #18",
        "tier": "Tier 1",
    },
    {
        "id": 19,
        "src": "/assets/inventory/Tier 1_9.jpg",
        "title": "Bird #19",
        "tier": "Tier 1",
    },
    {
        "id": 20,
        "src": "/assets/inventory/Tier 1_10.jpg",
        "title": "Bird #20",
        "tier": "Tier 1",
    },
    {
        "id": 21,
        "src": "/assets/inventory/Tier 2_1.jpg",
        "title": "Bird #21",
        "tier": "Tier 2",
    },
    {
        "id": 22,
        "src": "/assets/inventory/Tier 2_2.jpg",
        "title": "Bird #22",
        "tier": "Tier 2",
    },
    {
        "id": 23,
        "src": "/assets/inventory/Tier 2_3.jpg",
        "title": "Bird #23",
        "tier": "Tier 2",
    },
    {
        "id": 24,
        "src": "/assets/inventory/Tier 2_4.jpg",
        "title": "Bird #24",
        "tier": "Tier 2",
    },
    {
        "id": 25,
        "src": "/assets/inventory/Tier 2_5.jpg",
        "title": "Bird #25",
        "tier": "Tier 2",
    },
    {
        "id": 26,
        "src": "/assets/inventory/Tier 2_6.jpg",
        "title": "Bird #26",
        "tier": "Tier 2",
    },
    {
        "id": 27,
        "src": "/assets/inventory/Tier 2_7.jpg",
        "title": "Bird #27",
        "tier": "Tier 2",
    },
    {
        "id": 28,
        "src": "/assets/inventory/Tier 2_8.jpg",
        "title": "Bird #28",
        "tier": "Tier 2",
    },
    {
        "id": 29,
        "src": "/assets/inventory/Tier 2_9.jpg",
        "title": "Bird #29",
        "tier": "Tier 2",
    },
    {
        "id": 30,
        "src": "/assets/inventory/Tier 2_10.jpg",
        "title": "Bird #30",
        "tier": "Tier 2",
    },
    {
        "id": 31,
        "src": "/assets/inventory/Tier 3_1.jpg",
        "title": "Bird #31",
        "tier": "Tier 3",
    },
    {
        "id": 32,
        "src": "/assets/inventory/Tier 3_2.jpg",
        "title": "Bird #32",
        "tier": "Tier 3",
    },
    {
        "id": 33,
        "src": "/assets/inventory/Tier 3_3.jpg",
        "title": "Bird #33",
        "tier": "Tier 3",
    },
    {
        "id": 34,
        "src": "/assets/inventory/Tier 3_4.jpg",
        "title": "Bird #34",
        "tier": "Tier 3",
    },
    {
        "id": 35,
        "src": "/assets/inventory/Tier 3_5.jpg",
        "title": "Bird #35",
        "tier": "Tier 3",
    },
    {
        "id": 36,
        "src": "/assets/inventory/Tier 3_6.jpg",
        "title": "Bird #36",
        "tier": "Tier 3",
    },
    {
        "id": 37,
        "src": "/assets/inventory/Tier 3_7.jpg",
        "title": "Bird #37",
        "tier": "Tier 3",
    },
    {
        "id": 38,
        "src": "/assets/inventory/Tier 3_8.jpg",
        "title": "Bird #38",
        "tier": "Tier 3",
    },
    {
        "id": 39,
        "src": "/assets/inventory/Tier 3_9.jpg",
        "title": "Bird #39",
        "tier": "Tier 3",
    },
    {
        "id": 40,
        "src": "/assets/inventory/Tier 3_10.jpg",
        "title": "Bird #40",
        "tier": "Tier 3",
    },
    {
        "id": 41,
        "src": "/assets/inventory/Tier 4_1.jpg",
        "title": "Bird #41",
        "tier": "Tier 4",
    },
    {
        "id": 42,
        "src": "/assets/inventory/Tier 4_2.jpg",
        "title": "Bird #42",
        "tier": "Tier 4",
    },
    {
        "id": 43,
        "src": "/assets/inventory/Tier 4_3.jpg",
        "title": "Bird #43",
        "tier": "Tier 4",
    },
    {
        "id": 44,
        "src": "/assets/inventory/Tier 4_4.jpg",
        "title": "Bird #44",
        "tier": "Tier 4",
    },
    {
        "id": 45,
        "src": "/assets/inventory/Tier 4_5.jpg",
        "title": "Bird #45",
        "tier": "Tier 4",
    },
    {
        "id": 46,
        "src": "/assets/inventory/Tier 4_6.jpg",
        "title": "Bird #46",
        "tier": "Tier 4",
    },
    {
        "id": 47,
        "src": "/assets/inventory/Tier 4_7.jpg",
        "title": "Bird #47",
        "tier": "Tier 4",
    },
    {
        "id": 48,
        "src": "/assets/inventory/Tier 4_8.jpg",
        "title": "Bird #48",
        "tier": "Tier 4",
    },
    {
        "id": 49,
        "src": "/assets/inventory/Tier 4_9.jpg",
        "title": "Bird #49",
        "tier": "Tier 4",
    },
    {
        "id": 50,
        "src": "/assets/inventory/Tier 4_10.jpg",
        "title": "Bird #50",
        "tier": "Tier 4",
    },
    {
        "id": 51,
        "src": "/assets/inventory/Tier 5_1.jpg",
        "title": "Bird #51",
        "tier": "Tier 5",
    },
    {
        "id": 52,
        "src": "/assets/inventory/Tier 5_2.jpg",
        "title": "Bird #52",
        "tier": "Tier 5",
    },
    {
        "id": 53,
        "src": "/assets/inventory/Tier 5_3.jpg",
        "title": "Bird #53",
        "tier": "Tier 5",
    },
    {
        "id": 54,
        "src": "/assets/inventory/Tier 5_4.jpg",
        "title": "Bird #54",
        "tier": "Tier 5",
    },
    {
        "id": 55,
        "src": "/assets/inventory/Tier 5_5.jpg",
        "title": "Bird #55",
        "tier": "Tier 5",
    },
    {
        "id": 56,
        "src": "/assets/inventory/Tier 5_6.jpg",
        "title": "Bird #56",
        "tier": "Tier 5",
    },
    {
        "id": 57,
        "src": "/assets/inventory/Tier 5_7.jpg",
        "title": "Bird #57",
        "tier": "Tier 5",
    },
    {
        "id": 58,
        "src": "/assets/inventory/Tier 5_8.jpg",
        "title": "Bird #58",
        "tier": "Tier 5",
    },
    {
        "id": 59,
        "src": "/assets/inventory/Tier 5_9.jpg",
        "title": "Bird #59",
        "tier": "Tier 5",
    },
    {
        "id": 60,
        "src": "/assets/inventory/Tier 5_10.jpg",
        "title": "Bird #60",
        "tier": "Tier 5",
    },
    
]
exclusive_birds  = BIRDLIST[:10]
first_tier_birds = [BIRDLIST[10]]
second_tier_birds  = BIRDLIST[11:20]

third_tier_birds  = BIRDLIST[20:30]

fourth_tier_birds  = BIRDLIST[30:40]

fifth_tier_birds = BIRDLIST[40:50]

sixth_tier_birds  = BIRDLIST[50:60]

exclusive_tier = [exclusive_birds]


tiers = [
    first_tier_birds, second_tier_birds, third_tier_birds, fourth_tier_birds, fifth_tier_birds, sixth_tier_birds
]
print(fourth_tier_birds, '\n', fifth_tier_birds, '\n', sixth_tier_birds)
def get_country_by_ip(ip_address):
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        data = response.json()
        country = data.get('country')
        if country:
            return country
        else:
            print(f"Не удалось получить страну для IP: {ip_address}")
            return None
    except Exception as e:
        print(f"Ошибка при определении страны: {e}")
        return None
def get_regions_by_country(country_code):
    found_regions = []
    for region, countries in regions.items():
        if country_code in countries:
            found_regions.append(region)
    return found_regions if found_regions else ["Неизвестный регион"]

eggs = {
    0:{'hp':2500000},
    1:{'hp':5000},
    2:{'hp': 250000},
    3:{'hp':1000000},
    4:{'hp':2500000},
    5:{'hp':5000000},
    6:{'hp':10000000},
}

boosters = {
    "multitap":{"init_price":5000},
    "max energy":{"init_price":5000},
    "tap bot":{"init_price":100000, "duration":12}
}

ton_to_tappy_currency = 100
shop_items = {

"exclusive egg":{'price':1*ton_to_tappy_currency},
'random egg':{'price':0.9*ton_to_tappy_currency},
'stone hammer':{"price":0.25*ton_to_tappy_currency, "damage":0.25},
'gold hammer':{"price":0.5*ton_to_tappy_currency, "damage":0.75},
'diamond hammer':{"price":0.7*ton_to_tappy_currency, "damage":1}
}

toncenter_api_key= '1c93c6a032f12b836fce61dcba836f8fa1eedd3eb87bfca427c68ee179d9f1c2'