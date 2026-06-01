from sqlalchemy import Column, Integer, String, ForeignKey, Date
from datetime import date
from database import Base

class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    available_copies = Column(Integer, default=1)

class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), nullable=False)

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    borrow_id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.book_id"))
    member_id = Column(Integer, ForeignKey("members.member_id"))
    borrow_date = Column(Date, default=date.today)
    return_date = Column(Date, nullable=True)
    status = Column(String(20), default="Borrowed")
