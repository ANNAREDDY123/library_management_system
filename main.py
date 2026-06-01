from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from database import Base, engine, get_db
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")


@app.get("/")
def home():
    return {"message": "Library Management System API Running"}


# ---------------- BOOK MANAGEMENT ----------------

@app.post("/books")
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {
        "message": "Book added successfully",
        "book_id": new_book.book_id
    }


@app.get("/books")
def view_books(
    search: str = "",
    category: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    query = db.query(models.Book)

    if search:
        query = query.filter(models.Book.title.like(f"%{search}%"))

    if category:
        query = query.filter(models.Book.category == category)

    total = query.count()

    books = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "books": books
    }


@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(
        models.Book.book_id == book_id
    ).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.put("/books/{book_id}")
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(
        models.Book.book_id == book_id
    ).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)

    db.commit()

    return {"message": "Book updated successfully"}


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(
        models.Book.book_id == book_id
    ).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()

    return {"message": "Book deleted successfully"}


# ---------------- MEMBER MANAGEMENT ----------------

@app.post("/members")
def add_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):

    existing_member = db.query(models.Member).filter(
        models.Member.email == member.email
    ).first()

    if existing_member:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_member = models.Member(**member.dict())

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return {
        "message": "Member added successfully",
        "member_id": new_member.member_id
    }


@app.get("/members")
def view_members(db: Session = Depends(get_db)):
    return db.query(models.Member).all()


@app.put("/members/{member_id}")
def update_member(member_id: int, member: schemas.MemberUpdate, db: Session = Depends(get_db)):
    db_member = db.query(models.Member).filter(
        models.Member.member_id == member_id
    ).first()

    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")

    for key, value in member.dict(exclude_unset=True).items():
        setattr(db_member, key, value)

    db.commit()

    return {"message": "Member updated successfully"}


@app.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(models.Member).filter(
        models.Member.member_id == member_id
    ).first()

    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(db_member)
    db.commit()

    return {"message": "Member deleted successfully"}


# ---------------- BORROW & RETURN ----------------

@app.post("/borrow")
def borrow_book(record: schemas.BorrowCreate, db: Session = Depends(get_db)):

    book = db.query(models.Book).filter(
        models.Book.book_id == record.book_id
    ).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    member = db.query(models.Member).filter(
        models.Member.member_id == record.member_id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No copies available")

    borrow = models.BorrowRecord(
        book_id=record.book_id,
        member_id=record.member_id
    )

    book.available_copies -= 1

    db.add(borrow)
    db.commit()

    return {"message": "Book borrowed successfully"}


@app.put("/return/{borrow_id}")
def return_book(borrow_id: int, db: Session = Depends(get_db)):

    borrow = db.query(models.BorrowRecord).filter(
        models.BorrowRecord.borrow_id == borrow_id
    ).first()

    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    if borrow.status == "Returned":
        raise HTTPException(status_code=400, detail="Book already returned")

    borrow.status = "Returned"
    borrow.return_date = date.today()

    book = db.query(models.Book).filter(
        models.Book.book_id == borrow.book_id
    ).first()

    book.available_copies += 1

    db.commit()

    return {"message": "Book returned successfully"}


@app.get("/borrowed-books")
def view_borrowed_books(db: Session = Depends(get_db)):
    return db.query(models.BorrowRecord).filter(
        models.BorrowRecord.status == "Borrowed"
    ).all()
