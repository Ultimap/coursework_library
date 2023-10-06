from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
Base = declarative_base()


class Style(Base):
    __tablename__ = 'Style'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)


class Author(Base):
    __tablename__ = 'Authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    birth_data = Column(TIMESTAMP, nullable=False)
    death_data = Column(TIMESTAMP, nullable=False)


class Book(Base):
    __tablename__ = 'Books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    img = Column(String)
    description = Column(String, nullable=False )
    count = Column(Integer, nullable=False, default=0)
    style = Column(ForeignKey(Style.id))
    author = Column(ForeignKey(Author.id))
    age_restriction = Column(Integer, nullable=False)
    release_date = Column(TIMESTAMP)


class Accounting(Base):
    __tablename__ = 'Accounting'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book = Column(ForeignKey(Book.id))
    unique_key = Column(String, unique=True)
    availability = Column(Boolean, default=True)


class Role(Base):
    __tablename__ = 'Roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)


class User(Base):
    __tablename__ = "Users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True)
    role = Column(ForeignKey(Role.id))
    age = Column(Integer, nullable=False)
    password = Column(String, nullable=False)


class UserBook(Base):
    __tablename__ = 'UsersBooks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(ForeignKey(User.id))
    book = Column(Integer, ForeignKey(Accounting.id))
    date_receipt = Column(TIMESTAMP)
    date_return = Column(TIMESTAMP)

