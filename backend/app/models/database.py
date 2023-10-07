
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import create_engine
from app.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
db_session = sessionmaker(engine, class_=Session, expire_on_commit=False)


async def get_session():
    with db_session() as session:
        yield session
