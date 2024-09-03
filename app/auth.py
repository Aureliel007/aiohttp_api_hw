import bcrypt
import jwt
from aiohttp import web
from jwt import ExpiredSignatureError, InvalidTokenError

from tools import get_error


SECRET_KEY = 'qw9hen7392hxnd723xndeyxesfs87er7s7f6a6sfa97fd9s7f89sfs7d6f6ds76f'


def hash_password(password: str) -> str:
    password = password.encode()
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    password = password.decode()
    return password

def check_password(password: str, hashed_password: str) -> bool:
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(password, hashed_password)


def create_jwt(user_id):
    payload = {
        'user_id': user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except ExpiredSignatureError:
        raise get_error('Token has expired', web.HTTPUnauthorized)
    except InvalidTokenError:
        raise get_error('Invalid token', web.HTTPUnauthorized)
