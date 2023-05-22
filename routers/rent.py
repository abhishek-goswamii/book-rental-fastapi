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


@router.post('/rentbook')
async def rentABook(rent: schemas.Rent, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    book = db.query(models.Book).filter(
        models.Book.Title == rent.BookName).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book.Available:
        raise HTTPException(
            status_code=400, detail="Book is not available for rental")

    rental = models.RentalCart(

        user=user,
        book=book,
        RentalPeriod=rent.RentalPeriod,
        RentalCost=book.PricePerDay * rent.RentalPeriod,
        RentalDate=rent.RentalDate,
        ReturnDate=rent.ReturnDate,
        Active=True
    )

    print(rental)
    db.add(rental)
    book.Available = False

    book.user = user

    db.commit()
    db.refresh(rental)

    return {"message": "Book rented successfully"}


@router.post('/return/{book_name}')
async def returnABook(book_name: str, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    book = db.query(models.Book).filter(models.Book.Title == book_name).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    rental = db.query(models.RentalCart).filter(
        models.RentalCart.UserID == user.id,
        models.RentalCart.BookID == book.BookID,
        models.RentalCart.Active == True
    ).first()

    if not rental:
        raise HTTPException(
            status_code=400, detail="Book is not rented by the user")

    rental.Active = False
    book.Available = True

    db.commit()

    return {"message": "Book returned successfully"}
