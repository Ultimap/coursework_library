from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timedelta
from app.models.database import get_session
from app.models.models import UserBook, User, Book, Accounting
from app.utilits.users import get_current_user
from app.utilits.books import get_book_by_id
from app.scheme.user_books import DateReturn

user_book = APIRouter(prefix='/api/user_book', tags=['UserBook'])


@user_book.post('/{id}/add', status_code=201)
async def add_book_for_user(id: int, data: DateReturn, user: User = Depends(get_current_user),
                            db: AsyncSession = Depends(get_session)):
    try:
        book = await get_book_by_id(id)
        if not book:
            raise HTTPException(status_code=404, detail='book not found')
        accounting_book = await db.execute(
            select(Accounting).where(Accounting.book == book.id and Accounting.availability == True))
        accounting_book = accounting_book.scalars().first()
        if not accounting_book:
            raise HTTPException(status_code=400, detail='no books available')
        if data.date_return:
            date_return = data.date_return
        else:
            date_return = datetime.utcnow() + timedelta(weeks=2)
        new_user_book = UserBook(user=user.id, book=accounting_book.id, date_receipt=datetime.utcnow(),
                                 date_return=date_return)
        db.add(new_user_book)
        await db.execute(update(Accounting).values(availability=False).where(Accounting.id == accounting_book.id))
        await db.commit()
        return {'message': 'Success'}
    except:
        raise HTTPException(status_code=409)


@user_book.delete('/{id}/return', status_code=200)
async def return_book(id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    try:
        order = await db.execute(select(UserBook).where(UserBook.id == id and UserBook.user == user.id))
        order = order.scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=404, detail='book not found')
        accounting_book = await db.execute(select(Accounting).where(Accounting.id == order.book))
        accounting_book = accounting_book.scalar_one_or_none()
        if not accounting_book:
            raise HTTPException(status_code=404, detail='book in accounting not found')
        await db.execute(update(Accounting).values(availability=True).where(Accounting.id == accounting_book.id))
        await db.delete(order)
        await db.commit()
        return {'message': 'Success'}
    except:
        raise HTTPException(status_code=409)


@user_book.get('', status_code=200)
async def get_books(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    books = await db.execute(
        select(Book)
        .distinct()
        .join(Accounting, Accounting.book == Book.id)
        .join(UserBook, UserBook.book == Accounting.id)
        .filter(UserBook.user == user.id)
    )
    return books.scalars().all()
