from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.models.database import get_session
from app.models.models import UserBook, User, Book, Accounting
from app.utilits.users import get_current_user
from app.utilits.books import get_book_by_id

accounting = APIRouter(prefix='/api/accounting', tags=['Accounting'])


@accounting.get('/status_book', status_code=200)
async def get_status_book(user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    if user.role == 1:
        books = db.execute(select(Accounting))
        return books.scalars().all()
    raise HTTPException(status_code=403)


@accounting.get('/users', status_code=200)
async def get_users(user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    if user.role == 1:
        user_book = db.execute(select(UserBook))
        return user_book.scalars().all()
    raise HTTPException(status_code=403)

