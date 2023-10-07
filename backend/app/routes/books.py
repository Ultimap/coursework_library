from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
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
        db: Session = Depends(get_session),
        user: User = Depends(get_current_user)
        ):
    if user.role == 1:
        try:
            new_book = Book(name=name, img=img.filename, description=description,
                            count=count, style=style, author=author,
                            age_restriction=age_restriction, release_date=release_date)
            db.add(new_book)
            db.commit()
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
        db.commit()
        return {'message': 'Success'}
    raise HTTPException(status_code=403)


@books.get('', status_code=200)
async def get_books(db: Session = Depends(get_session)):
    book = db.execute(select(Book))
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
async def delete(id: int, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role == 1:
        try:
            book = await get_book_by_id(id)
            if not book:
                raise HTTPException(status_code=404, detail='book not found')
            db.delete(book)
            db.commit()
            return {'message': 'Success'}
        except:
            raise HTTPException(status_code=409)
    raise HTTPException(status_code=403)


@books.put('/{id}/edit', status_code=200)
async def edit(id: int, data: BookEdit, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role == 1:
        book = await get_book_by_id(id)
        try:
            if not book:
                raise HTTPException(status_code=404, detail='book not found')
            if data.name:
                db.execute(update(Book).values(name=data.name).where(Book.id == id))
            if data.style:
                db.execute(update(Book).values(style=data.style).where(Book.id == id))
            if data.author:
                db.execute(update(Book).values(author=data.author).where(Book.id == id))
            if data.count:
                accounting_count = db.execute(select(func.count()).where(Accounting.book == id))
                count = accounting_count.scalar()
                if count > data.count:
                    excess_records = db.execute(
                        select(Accounting).where(Accounting.book == id).order_by(Accounting.id.desc()).limit(count-data.count))
                    records_to_delete = excess_records.scalars().all()
                    try:
                        for record in records_to_delete:
                            db.delete(record)
                            db.commit()
                    except:
                        raise HTTPException(status_code=409, detail='сannot be edit')
                else:
                    for x in range(data.count):
                        try:
                            unique_key = f'{book.id}+{x + 1}'
                            accounting_in_data = db.execute(
                                select(Accounting).where(Accounting.unique_key == unique_key))
                            if accounting_in_data.scalar_one_or_none() is not None:
                                continue
                            accounting = Accounting(book=book.id, unique_key=unique_key)
                            db.add(accounting)
                        except:
                            ...
                        db.commit()
                db.execute(update(Book).values(count=data.count).where(Book.id == id))
            if data.description:
                db.execute(update(Book).values(description=data.description).where(Book.id == id))
            if data.age_restriction:
                db.execute(update(Book).values(age_restriction=data.age_restriction).where(Book.id == id))
            if data.release_date:
                db.execute(update(Book).values(release_date=data.release_date).where(Book.id == id))
            db.commit()
        except:
            raise HTTPException(status_code=409)
        return {'message': 'Success'}
    raise HTTPException(status_code=403)


@books.put('/{id}/edit/img', status_code=200)
async def edit_img(id: int, img: UploadFile = File(...), db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role == 1:
        book = await get_book_by_id(id)
        if not book:
            raise HTTPException(status_code=404, detail='book not found')
        try:
            db.execute(update(Book).values(img=img.filename).where(Book.id == id))
            db.commit()
            await add_img(img)
            return {'message': 'Success'}
        except:
            raise HTTPException(status_code=409)
    raise HTTPException(status_code=403)
