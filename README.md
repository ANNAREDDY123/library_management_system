# Library Management System

## Objective

Backend application to manage Books, Members, and Book Borrowing using FastAPI and SQL.

## Tech Stack

- Python 3
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite / MySQL

## Features

### Book Management
- Add Book
- View All Books
- Get Book by ID
- Update Book
- Delete Book
- Search by Title
- Search by Category
- Pagination

### Member Management
- Add Member
- View Members
- Update Member
- Delete Member
- Unique Email Validation
- Phone Validation

### Borrow & Return System
- Borrow Book
- Return Book
- View Borrowed Books
- Automatic Copy Management

### SQL Reports
- Most Borrowed Books
- Members Borrowing More Than 3 Books
- Books by Category
- Currently Borrowed Books
- Total Available Books

## Project Structure

library_management_system/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── README.md
├── sql/
│ ├── schema.sql
│ └── report_queries.sql
└── postman_collection.json

## Run Project

pip install -r requirements.txt
uvicorn main:app 
Swagger:

http://127.0.0.1:8000/docs

Explanation

I created three tables: Books, Members, and Borrow Records.

Books store book information and available copies.

Members store library member details with email uniqueness validation.

Borrow Records track book borrowing and returning.

When a member borrows a book, available copies decrease by one. When returned, copies increase by one.

Error handling prevents borrowing unavailable books and returning already returned books.

FastAPI automatically provides Swagger documentation.

Submission Files
Source Code
SQL Script
SQL Report Queries
Postman Collection
README






