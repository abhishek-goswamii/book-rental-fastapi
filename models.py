from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Boolean, CheckConstraint, func
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=True)
    email = Column(String, nullable=False)
    number = Column(Integer, nullable=True)
    profile = Column(String, nullable=True)
    password = Column(String, nullable=False)
    isAdmin = Column(Boolean, nullable=False, default=False)
    
    book = relationship('Book', back_populates='user')
    reviews = relationship('Review', back_populates='user')

    rentals = relationship('RentalCart', back_populates='user')


class Book(Base):
    __tablename__ = 'books'

    BookID = Column(Integer, primary_key=True)
    Title = Column(String)
    Author = Column(String)
    Genre = Column(String)
    Description = Column(String)
    CoverImage = Column(String)
    Available = Column(Boolean)
    RentingPeriod = Column(Integer)
    PricePerDay = Column(Integer)

    UserID = Column(Integer, ForeignKey('users.id'), nullable=True)

    user = relationship("User", back_populates="book")
    
    genres = relationship('Genre', secondary='book_genres',back_populates='books')

    reviews = relationship('Review', back_populates='book')
    rentals = relationship('RentalCart', uselist=False, back_populates='book')


class Genre(Base):
    __tablename__ = 'genres'

    GenreID = Column(Integer, primary_key=True)
    GenreName = Column(String)

    books = relationship('Book', secondary='book_genres',
                         back_populates='genres')

# many to many relationship of book and genre
class BookGenre(Base):
    __tablename__ = 'book_genres'

    BookID = Column(Integer, ForeignKey('books.BookID'), primary_key=True)
    GenreID = Column(Integer, ForeignKey('genres.GenreID'), primary_key=True)


class Review(Base):
    __tablename__ = 'reviews'

    ReviewID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('users.id'))
    BookID = Column(Integer, ForeignKey('books.BookID'))

    Rating = Column(Integer)

    ReviewText = Column(String)

    ReviewDate = Column(Date, default=func.current_date())

    user = relationship('User', back_populates='reviews')
    book = relationship('Book', back_populates='reviews')


class RentalCart(Base):
    __tablename__ = 'rentals'

    RentalID = Column(Integer, primary_key=True)

    UserID = Column(Integer, ForeignKey('users.id'))
    BookID = Column(Integer, ForeignKey('books.BookID'))

    RentalPeriod = Column(Integer)
    RentalCost = Column(Integer)
    RentalDate = Column(Date, default=func.current_date())
    ReturnDate = Column(Date)
    Active = Column(Boolean)

    user = relationship('User', back_populates='rentals')
    book = relationship('Book', back_populates='rentals')
