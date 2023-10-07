from sqlalchemy import select
from app.models.database import db_session
from app.models.models import Book, Style, Author


async def get_book_by_id(id: int) -> Book:
    with db_session() as session:
        book = session.execute(select(Book).where(Book.id == id))
        return book.scalar_one_or_none()


async def get_style_by_id(id: int) -> Style:
    with db_session() as session:
        style = session.execute(select(Style).where(Style.id == id))
        return style.scalar_one_or_none()


async def get_author_by_id(id: int) -> Author:
    with db_session() as session:
        style = session.execute(select(Author).where(Author.id == id))
        return style.scalar_one_or_none()
