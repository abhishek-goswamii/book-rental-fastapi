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


@router.post("/add-genre")
async def addGenre(genre: schemas.AddGenre, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    existing_genre = db.query(models.Genre).filter(
        models.Genre.GenreName == genre.GenreName).first()

    if existing_genre:
        return "Genre already exists"

    new_genre = models.Genre(**genre.dict())
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return new_genre


@router.get('/genre-list')
async def getGenres(user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    genre_list = db.query(models.Genre).all()
    return genre_list


@router.post('/connect-genre-book')
async def connectGenreBook(genreBook: schemas.ConnectGenreBook, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    genre_id = db.query(models.Genre).filter(
        models.Genre.GenreName == genreBook.GenreName).first()

    if not genre_id:
        return "genre with this name not found"

    book_id = db.query(models.Book).filter(
        models.Book.Title == genreBook.BookName).first()

    if not book_id:
        return "book with this name not found"

    genre = book_id.genres
    genre.append(genre_id)
    db.commit()

    return "added"