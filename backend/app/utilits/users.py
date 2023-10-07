import bcrypt
import jwt
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy import select
from app.models.database import db_session
from app.models.models import User
from app.settings import ALGORITHM, SECRET_KEY, oauth2scheme

EXPIRATION_TIME = timedelta(days=1)


async def hashing_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('UTF-8'), salt)
    return hash_password.decode('UTF-8')


async def verify_password(password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(password.encode('UTF-8'), hash_password.encode('UTF-8'))


async def get_user_by_username(username: str) -> User:
    with db_session() as session:
        user = session.execute(select(User).where(User.username == username))
        return user.scalar_one_or_none()


async def generate_jwt(data: dict):
    expiration = EXPIRATION_TIME+datetime.utcnow()
    data.update({'exp': expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def verify_jwt_token(token: str) -> dict:
    try:
        decode_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decode_data
    except jwt.PyJWTError:
        return None


async def get_current_user(token: str = Depends(oauth2scheme)) -> User:
    decode_data = await verify_jwt_token(token)
    if not decode_data:
        raise HTTPException(status_code=400, detail='invalid token')
    user = await get_user_by_username(decode_data.get('sub'))
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    return user
