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


@router.post("/add-review/{book_id}")
async def add_review(book_id: int, review: schemas.AddReview, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    book = db.query(models.Book).filter(models.Book.BookID == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    new_review = models.Review(
        Rating=review.Rating, ReviewText=review.ReviewText, book=book, user=user)

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review
