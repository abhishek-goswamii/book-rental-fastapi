from random import randrange
from fastapi import Depends, HTTPException, APIRouter
import time
import models
from database import get_db
from sqlalchemy.orm import Session
import models
import schemas
import utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import oauth2
router = APIRouter()


@router.post("/add-book")
async def register(book: schemas.AddBook, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user.isAdmin:
        return {"error": "Only Admin can add books"}

    existing_book = db.query(models.Book).filter(
        models.Book.Title == book.Title).first()

    if existing_book:
        return "Book already exists"
    
    
    

    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/delete-book/{bookname}")
async def deleteBook(bookname: str, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user.isAdmin:
        return {"error": "Only librarians can delete books"}

    book = db.query(models.Book).filter(models.Book.Title == bookname).first()

    if not book:
        return {"error": "Book not found"}

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}


@router.get("/book-list")
async def get_book_list(user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@router.get('/search-book-by-genre/{genre}')
async def searchBookWithGenres(genre: str, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    genre_id = db.query(models.Genre).filter(
        models.Genre.GenreName == genre).first()

    if not genre_id:
        return "genre with this name not found"

    books_with_genre = db.query(models.Book).join(
        models.Book.genres).filter(models.Genre.GenreName == genre).all()
    return books_with_genre


@router.get('/search-by-author/{author}')
async def searchBookWithAuthor(author: str, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    authors = db.query(models.Book).filter(
        models.Book.Author == author).all()

    if not authors:
        return "no book with this author"

    return authors


@router.get('/search-by-title/{title}')
async def searchBookWithTitle(title: str, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    books = db.query(models.Book).filter(
        models.Book.Title == title).first()

    if not books:
        return f"no book with title : {title}"

    return books


@router.get('/books-detail/{book_name}')
async def bookDetails(book_name: str, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    book = db.query(models.Book).filter(models.Book.Title == book_name).first()

    if not book:
        return {"message": "Book not found"}

    reviews = db.query(models.Review).filter(
        models.Review.BookID == book.BookID).all()

    review_list = []

    for review in reviews:
        review_data = {
            "ReviewID": review.ReviewID,
            "UserID": review.UserID,
            "Rating": review.Rating,
            "ReviewText": review.ReviewText,
            "ReviewDate": review.ReviewDate
        }
        review_list.append(review_data)

    book_data = {
        "BookID": book.BookID,
        "Title": book.Title,
        "Author": book.Author,
        "Description": book.Description,
        "CoverImage": book.CoverImage,
        "Available": book.Available,
        "RentingPeriod": book.RentingPeriod,
        "PricePerDay": book.PricePerDay,
        "Reviews": review_list
    }

    return book_data


@router.get('/available-books')
async def bookDetails(user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    book_details = db.query(models.Book).filter(
        models.Book.Available == True).all()
    return book_details
