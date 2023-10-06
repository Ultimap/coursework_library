from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.models import User, UserBook
from app.models.database import get_session
from app.utilits.users import hashing_password, get_user_by_username, verify_password, generate_jwt, get_current_user
from app.scheme.users import UserScheme
auth = APIRouter(prefix='/api/user', tags=['User'])


@auth.post('/register', status_code=201)
async def register(data: UserScheme, db: AsyncSession = Depends(get_session)):
    try:
        password = await hashing_password(data.password)
        user = User(username=data.username, age=data.age, password=password)
        db.add(user)
        await db.commit()
        return {'message': 'Success'}
    except:
        raise HTTPException(409)


@auth.post('/login', status_code=200)
async def login(username: str = Form(...), password: str = Form(...)):
    user = await get_user_by_username(username)
    if not user or not await verify_password(password, user.password):
        raise HTTPException(status_code=400, detail='invalid username or password')
    token = await generate_jwt({'sub': user.username})
    return {'token': token}


@auth.get('/profile', status_code=200)
async def get_profile(user: User = Depends(get_current_user)):
    return user


@auth.put('/profile/edit', status_code=200)
async def edit(data: UserScheme, db: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    try:
        if data.username:
            await db.execute(update(User).values(username=data.username).where(User.id == user.id))
        if data.age:
            await db.execute(update(User).values(age=data.age).where(User.id == user.id))
        if data.password:
            password = await hashing_password(data.password)
            await db.execute(update(User).values(password=password).where(User.id == user.id))
        return {'message': "Success"}
    except:
        raise HTTPException(status_code=409)


@auth.delete('/profile/delete', status_code=200)
async def delete(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    try:
        user_book = await db.execute(select(UserBook).where(UserBook.user == user.id))
        user_book = user_book.scalars().all()
        for data in user_book:
            await db.delete(data)
            await db.commit()
        await db.delete(user)
        await db.commit()
        return {'message': 'Success'}
    except:
        raise HTTPException(status_code=409)


@auth.get('/profile/books', status_code=200)
async def books_user(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    books = await db.execute(select(UserBook).where(UserBook.user == user.id))
    books = books.scalars().all()
    return books
