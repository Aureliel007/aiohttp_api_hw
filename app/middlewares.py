from aiohttp import web

from auth import decode_jwt
from models import Session
from tools import get_error


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response   

@web.middleware
async def jwt_middleware(request: web.Request, handler):
    token = request.headers.get('Authorization', None)
    if token:
        if token.startswith('Bearer '):
            token = token[len('Bearer '):]
        try:
            payload = decode_jwt(token)
            request['payload'] = payload
        except Exception as e:
            raise get_error('Invalid token', web.HTTPUnauthorized)
    
    response = await handler(request)
    return response 
