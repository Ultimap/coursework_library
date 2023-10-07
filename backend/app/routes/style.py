from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from app.models.models import Style, User
from app.models.database import get_session
from app.scheme.books import StyleScheme
from app.utilits.books import get_style_by_id
from app.utilits.users import get_current_user

styles = APIRouter(prefix='/api/style', tags=['Style'])


@styles.post('/add', status_code=201)
async def add(data: StyleScheme, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role == 1:
        try:
            style = Style(name=data.name)
            db.add(style)
            db.commit()
            return {'message': 'Success'}
        except:
            raise HTTPException(status_code=409)
    raise HTTPException(status_code=403)


@styles.get('', status_code=200)
async def get(db: Session = Depends(get_session)):
    style = db.execute(select(Style))
    return style.scalars().all()


@styles.get('/{id}', status_code=200)
async def get_by_id(id: int):
    style = await get_style_by_id(id)
    if not style:
        raise HTTPException(status_code=404, detail='style not found')
    return style


@styles.delete('/{id}/delete', status_code=200)
async def delete(id: int, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role == 1:
        style = await get_style_by_id(id)
        if not style:
            raise HTTPException(status_code=404, detail='style not found')
        try:
            db.delete(style)
            db.commit()
            return {'message': 'Success'}
        except:
            raise HTTPException(status_code=409)
    raise HTTPException(status_code=403)


@styles.put('{id}/edit', status_code=200)
async def edit(id: int, data: StyleScheme, db: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.role == 1:
        style = await get_style_by_id(id)
        if not style:
            raise HTTPException(status_code=404, detail='style not found')
        try:
            db.execute(update(Style).values(name=data.name).where(Style.id == id))
            return {'message': 'Success'}
        except:
            raise HTTPException(status_code=409)
    raise HTTPException(status_code=403)
