from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.scheme.books import AuthorScheme
from app.models.models import Author, User
from app.models.database import get_session
from app.utilits.books import get_author_by_id
from app.utilits.users import get_current_user

authors = APIRouter(prefix='/api/author', tags=['Author'])


@authors.post('/add', status_code=201)
async def add(data: AuthorScheme, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role == 1:
        try:
            author = Author(name=data.name, birth_data=data.birth_data, death_data=data.death_data)
            db.add(author)
            db.commit()
            return {'message': 'Success'}
        except:
            raise HTTPException(status_code=409)
    raise HTTPException(status_code=403)


@authors.get('', status_code=200)
async def get(db: Session = Depends(get_session)):
    author = db.execute(select(Author))
    return author.scalars().all()


@authors.get('/{id}', status_code=200)
async def get_by_id(id: int):
    author = await get_author_by_id(id)
    if author:
        return author
    raise HTTPException(status_code=404, detail='author not found')


@authors.delete('/{id}/delete', status_code=200)
async def delete(id: int, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role == 1:
        author = await get_author_by_id(id)
        if not author:
            raise HTTPException(status_code=404, detail='author not found')
        try:
            db.delete(author)
            db.commit()
            return {'message': 'Success'}
        except:
            raise HTTPException(status_code=409)
    raise HTTPException(status_code=403)


@authors.put('/{id}/edit', status_code=200)
async def edit(id: int, data: AuthorScheme, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role == 1:
        author = await get_author_by_id(id)
        if not author:
            raise HTTPException(status_code=404, detail='author not found')
        try:
            if data.name:
                db.execute(update(Author).values(name=data.name).where(Author.id == id))
            if data.birth_data:
                db.execute(update(Author).values(birth_data=data.birth_data).where(Author.id == id))
            if data.death_data:
                db.execute(update(Author).values(death_data=data.death_data).where(Author.id == id))
            return {'message': 'Success'}
        except:
            raise HTTPException(status_code=409)
    raise HTTPException(status_code=403)