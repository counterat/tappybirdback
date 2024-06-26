
import decimal
import random
from datetime import datetime, timedelta
from random import randint
from sqlalchemy import  Column, Integer, String, Float, JSON, DateTime, Boolean, ForeignKey,ARRAY, DECIMAL, BigInteger, Sequence
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import array
from config import DB_URL
import json

import uuid
import decimal
Base = declarative_base()
class TappyBird(Base):
    __abstract__ = True

    def to_dict(self):
        return {
            c.name: (
                getattr(self, c.name).__str__() if isinstance(getattr(self, c.name), datetime)
                else str(getattr(self, c.name)) if isinstance(getattr(self, c.name), decimal.Decimal)
                else getattr(self, c.name)
            )
            for c in self.__table__.columns if c.name != 'password'
        }

class Squad(TappyBird):
    __tablename__ = 'squads'
    id = Column(BigInteger,Sequence('squads_id_seq', start=323), primary_key=True )
    users = Column(ARRAY(BigInteger), default=[])
    total_coins = Column(DECIMAL, default=0)
    founder = Column(BigInteger, ForeignKey('users.id'))
    title = Column(String)
    link_to_squad = Column(String)
    invite_link = Column(String)
    created_at = Column(DateTime, default=datetime.now)

class User(TappyBird):
    __tablename__ = 'users'
    id = Column(BigInteger,Sequence('user_id_seq', start=9324234), primary_key=True)
    telegram_id = Column(BigInteger, index=True)
    name = Column(String)
    password = Column(String)
    username = Column(String)
    in_squad = Column(BigInteger, ForeignKey('squads.id'))
    invitation_code = Column(BigInteger, index=True)
    invited_users = Column(ARRAY(BigInteger), default=[])
    birds = Column(ARRAY(Integer), default = [])
    times_multitap_was_used = Column(Integer, default=0)
    times_max_energy_was_used = Column(Integer, default=0)
    photo_url = Column(String, default = 'https://telegra.ph/file/99e7fb4ff14703f8d0d7f.png')
    sign = Column(String)
    invited_by = Column(BigInteger)
    balance_in_ton = Column(DECIMAL, default=0)
    balance_in_tappycoin = Column(DECIMAL, default=0)
    geo = Column(String)
    inventory = Column(JSON, default=json.dumps( {}))
    created_at = Column(DateTime, default=datetime.now)
    boosters = Column(JSON, default=json.dumps( {}))

class Booster(TappyBird):
    __tablename__ = 'boosters'
    id = Column(BigInteger,Sequence('booster_id_seq', start=1), primary_key=True)
    price = Column(DECIMAL)
    booster_name = Column(String)
    was_bought_by_user = Column(BigInteger, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)

class TopUps(TappyBird):
    __tablename__ = 'topups'
    id = Column(Integer, primary_key= True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    amount = Column(DECIMAL)
    created_at =  Column(DateTime, default=datetime.now)
    

class ShopItem(TappyBird):
    __tablename__ = 'shopitems'
    id = Column(BigInteger, primary_key=True)
    item_name = Column(String)
    price = Column(DECIMAL)
    was_bought_by_user = Column(BigInteger, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)


engine = create_async_engine(DB_URL, echo=True)

# Создание асинхронной фабрики сессий
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
""" 
import asyncio
asyncio.run(create_tables())   """ 