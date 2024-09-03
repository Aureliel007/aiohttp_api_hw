import json

from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession

from models import Session, User, Ads, engine
from schema import AdsCreate, UpdateAds, UserCreate
from auth import create_jwt, check_password, hash_password
from crud import get_user, add_user, post_ads, get_ads
from tools import get_error, validate


async def login(request):
    json_data = await request.json()
    session = request.session
    user = await get_user(session, json_data["id"])
    if check_password(json_data["password"], user.password):
        token = create_jwt(user_id=user.id)
        return web.json_response({'token': token})
    raise get_error('Incorrect user id or password', web.HTTPUnauthorized)

class UserView(web.View):

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    @property
    def session(self) -> AsyncSession:
        return self.request.session

    async def get(self):
        user = await get_user(self.session, self.user_id)
        return web.json_response(user.json)

    async def post(self):
        json_data = await self.request.json()
        json_data = validate(json_data, UserCreate)
        json_data["password"] = hash_password(json_data["password"])
        user = User(**json_data)
        await add_user(self.session, user)
        return web.json_response({"id": user.id})

class AdsView(web.View):

    @property
    def ads_id(self):
        return int(self.request.match_info["ads_id"])

    @property
    def session(self) -> AsyncSession:
        return self.request.session

    async def get(self):
        ads = await get_ads(self.session, self.ads_id)
        return web.json_response(ads.json)

    async def post(self):
        if "payload" not in self.request:
            raise get_error("Not authorized", web.HTTPUnauthorized)
        json_data = await self.request.json()
        json_data = validate(json_data, AdsCreate)
        author_id = self.request["payload"]["user_id"]
        json_data["author_id"] = author_id
        ads = Ads(**json_data)
        await post_ads(self.session, ads)
        return web.json_response(ads.json)

    async def patch(self):
        if "payload" not in self.request:
            raise get_error("Not authorized", web.HTTPUnauthorized)
        json_data = await self.request.json()
        json_data = validate(json_data, UpdateAds)
        author_id = self.request["payload"]["user_id"]
        ads = await get_ads(self.session, self.ads_id)
        if ads.author_id != author_id:
            raise get_error("Permission denied", web.HTTPForbidden)
        for field, value in json_data.items():
            setattr(ads, field, value)
        await post_ads(self.session, ads)
        return web.json_response(ads.json)

    async def delete(self):
        if "payload" not in self.request:
            raise get_error("Not authorized", web.HTTPUnauthorized)
        author_id = self.request["payload"]["user_id"]
        ads = await get_ads(self.session, self.ads_id)
        if ads.author_id != author_id:
            raise get_error("Permission denied", web.HTTPForbidden)
        await self.session.delete(ads)
        await self.session.commit()
        return web.json_response({"status": "deleted"})
