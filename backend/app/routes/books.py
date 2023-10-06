from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from datetime import date
from app.models.database import get_session
from app.models.models import Book, Accounting, User
from app.scheme.books import BookEdit
from app.utilits.books import get_style_by_id, get_author_by_id, get_book_by_id
from app.utilits.all import add_img
from app.utilits.users import get_current_user

books = APIRouter(prefix='/api/books', tags=['Book'])


@books.post('/add', status_code=201)
async def add_book(
        name: str = Form(...),
        img: UploadFile = File(...),
        description: str = Form(...),
        count: int = Form(...),
        style: int = Form(...),
        author: int = Form(...),
        age_restriction: int = Form(...),
        release_date: date = Form(...),
        db: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user)
        ):
    if user.role == 1:
        try:
            new_book = Book(name=name, img=img.filename, description=description,
                            count=count, style=style, author=author,
                            age_restriction=age_restriction, release_date=release_date)
            db.add(new_book)
            await db.commit()
            await add_img(img)
        except:
            raise HTTPException(status_code=409)
        for x in range(count):
            try:
                unique_key = f'{new_book.id}+{x + 1}'
                accounting = Accounting(book=new_book.id, unique_key=unique_key)
                db.add(accounting)
            except:
                ...
        await db.commit()
        return {'message': 'Success'}
    raise HTTPException(status_code=403)


@books.get('', status_code=200)
async def get_books(db: AsyncSession = Depends(get_session)):
    book = await db.execute(select(Book))
    return book.scalars().all()


@books.get('/{id}', status_code=200)
async def get_book(id: int):
    try:
        book = await get_book_by_id(id)
        if not book:
            raise HTTPException(status_code=404)
        style = await get_style_by_id(book.style)
        author = await get_author_by_id(book.author)
        return {**book.__dict__, 'style': style, 'author': author}
    except:
        raise HTTPException(status_code=404, detail='book not found')


@books.delete('/{id}/delete', status_code=200)
async def delete(id: int, db: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role == 1:
        try:
            book = await get_book_by_id(id)
            if not book:
                raise HTTPException(status_code=404, detail='book not found')
            await db.delete(book)
            await db.commit()
            return {'message': 'Success'}
        except:
            raise HTTPException(status_code=409)
    raise HTTPException(status_code=403)


@books.put('/{id}/edit', status_code=200)
async def edit(id: int, data: BookEdit, db: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role == 1:
        book = await get_book_by_id(id)
        try:
            if not book:
                raise HTTPException(status_code=404, detail='book not found')
            if data.name:
                await db.execute(update(Book).values(name=data.name).where(Book.id == id))
            if data.style:
                await db.execute(update(Book).values(style=data.style).where(Book.id == id))
            if data.author:
                await db.execute(update(Book).values(author=data.author).where(Book.id == id))
            if data.count:
                accounting_count = await db.execute(select(func.count()).where(Accounting.book == id))
                count = accounting_count.scalar()
                if count > data.count:
                    excess_records = await db.execute(
                        select(Accounting).where(Accounting.book == id).order_by(Accounting.id.desc()).limit(count-data.count))
                    records_to_delete = excess_records.scalars().all()
                    try:
                        for record in records_to_delete:
                            await db.delete(record)
                            await db.commit()
                    except:
                        raise HTTPException(status_code=409, detail='сannot be edit')
                else:
                    for x in range(data.count):
                        try:
                            unique_key = f'{book.id}+{x + 1}'
                            accounting_in_data = await db.execute(
                                select(Accounting).where(Accounting.unique_key == unique_key))
                            if accounting_in_data.scalar_one_or_none() is not None:
                                continue
                            accounting = Accounting(book=book.id, unique_key=unique_key)
                            db.add(accounting)
                        except:
                            ...
                        await db.commit()
                await db.execute(update(Book).values(count=data.count).where(Book.id == id))
            if data.description:
                await db.execute(update(Book).values(description=data.description).where(Book.id == id))
            if data.age_restriction:
                await db.execute(update(Book).values(age_restriction=data.age_restriction).where(Book.id == id))
            if data.release_date:
                await db.execute(update(Book).values(release_date=data.release_date).where(Book.id == id))
            await db.commit()
        except:
            raise HTTPException(status_code=409)
        return {'message': 'Success'}
    raise HTTPException(status_code=403)


@books.put('/{id}/edit/img', status_code=200)
async def edit_img(id: int, img: UploadFile = File(...), db: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role == 1:
        book = await get_book_by_id(id)
        if not book:
            raise HTTPException(status_code=404, detail='book not found')
        try:
            await db.execute(update(Book).values(img=img.filename).where(Book.id == id))
            await db.commit()
            await add_img(img)
            return {'message': 'Success'}
        except:
            raise HTTPException(status_code=409)
    raise HTTPException(status_code=403)
