from aiohttp import web
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from tools import get_error
from models import User, Ads


async def get_user(session: AsyncSession, user_id: int) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise get_error("User not found", web.HTTPNotFound)
    return user


async def add_user(session: AsyncSession, user: User):
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        raise get_error("user already exist", web.HTTPConflict)

async def get_ads(session: AsyncSession, ads_id: int) -> Ads:
    ads = await session.get(Ads, ads_id)
    if ads is None:
        raise get_error("ads not found", web.HTTPNotFound)
    return ads

async def post_ads(session: AsyncSession, ads: Ads):
    session.add(ads)
    await session.commit()
