from random import randrange
from fastapi import Depends, HTTPException, APIRouter
import time
import models
from database import get_db
from sqlalchemy.orm import Session
import models
import schemas
import utils
import oauth2
router = APIRouter()


@router.post("/register", response_model=schemas.RegisterResponse | str)
async def register(user: schemas.User, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email).first()

    if existing_user:
        return "User already exists"

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(
        **user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/profile")
async def profile(user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    rental_history = db.query(models.RentalCart).filter(
        models.RentalCart.UserID == user.id, models.RentalCart.Active == False).all()

    active_rentals = db.query(models.RentalCart).filter(
        models.RentalCart.UserID == user.id, models.RentalCart.Active == True).all()

    return {
        "Name": user.firstname + " " + user.lastname,
        "Rental history": rental_history,
        "Active rentals": active_rentals,
        "Other Info": {
            "Email": user.email,
            "Phone": user.number,
            "Profile picture": user.profile
        }
    }
