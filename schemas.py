from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class User(BaseModel):
    id: Optional[int] = None
    firstname: str
    lastname: str
    email: str
    number: Optional[str] = None
    profile: Optional[str] = None
    password: str
    isAdmin: bool


class Login(BaseModel):
    email: str
    password: str


class RegisterResponse(BaseModel):
    id: int
    firstname: str
    email: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class AddBook(BaseModel):
    Title: str
    Author: str
    Genre: str
    Description: str
    CoverImage: str
    Available: bool
    RentingPeriod: int
    PricePerDay: int


class AddGenre(BaseModel):
    GenreName: str


class ConnectGenreBook(BaseModel):
    BookName: str
    GenreName: str


class AddReview(BaseModel):
    Rating: int
    ReviewText: str


class Rent(BaseModel):

    BookName: str
    RentalPeriod: int
    RentalDate: date
    ReturnDate: date

    class Config:
        orm_mode = True
