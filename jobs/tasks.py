from mail.send_mail import send_email
from datetime import datetime, timedelta
from models import RentalCart, Book
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


def send_book_rental_expiring_email():

    today = datetime.now().date()

    expiration_date = today + timedelta(days=3)

    db_username = settings.DATABASE_USERNAME
    db_password = settings.DATABASE_PASSWORD
    db_hostname = settings.HOSTNAME
    db_port = settings.PORT
    db_name = settings.DATABASE_NAME

    SQLALCHEMY_DATABASE_URL = f'postgresql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}'

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

    db = SessionLocal()

    expiring_rentals = db.query(RentalCart, Book).join(RentalCart.book).filter(
        RentalCart.Active == True,
        RentalCart.ReturnDate <= expiration_date,
        RentalCart.ReturnDate >= today
    ).all()

    for rental, book in expiring_rentals:

        sender_email = settings.SMTPEMAIL
        sender_password = settings.SMTPPASSWORD
        recipient_email = 'abhishek.goswami2100@gmail.com'
        subject = 'Book Rental will expire within 3 days'

        message = f'Your rental period for the book "{book.Title}" will expire within 3 days.Book return date was "{rental.ReturnDate}", You rented the book on "{rental.RentalDate}", Billing amount was "INR={rental.RentalCost}", Please return the book to the library. if you dont return book on time, you will be charged extra amount per day according to the per day renting cost of the book. '

        send_email(sender_email, sender_password,
                   recipient_email, subject, message)


def send_book_rental_due_amount_mail():

    today = datetime.now().date()

    expiration_date = today + timedelta(days=3)
    
    db_username = settings.DATABASE_USERNAME
    db_password = settings.DATABASE_PASSWORD
    db_hostname = settings.HOSTNAME
    db_port = settings.PORT
    db_name = settings.DATABASE_NAME

    SQLALCHEMY_DATABASE_URL = f'postgresql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}'

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

    db = SessionLocal()

    expiring_rentals = db.query(RentalCart, Book).join(RentalCart.book).filter(
        RentalCart.Active == True,
        RentalCart.ReturnDate < today
    ).all()



    for rental, book in expiring_rentals:
        
        book_obj = db.query(Book).filter(Book.BookID == book.BookID).first()
        book_per_day_price = book_obj.PricePerDay

        rent_obj = db.query(RentalCart).filter(RentalCart.RentalID == rental.RentalID).first()
        
        total_due_amount = rent_obj.DueAmount+book_per_day_price
        rent_obj.DueAmount = total_due_amount

        db.commit()

        sender_email = settings.SMTPEMAIL
        sender_password = settings.SMTPPASSWORD
        recipient_email = 'abhishek.goswami2100@gmail.com'
        subject = 'Book Rental period expired'

        message=f'Your rental for book "{book.Title}" has expired on date "{rental.ReturnDate}", you will be charged extra amount per day according to the per day renting cost of the book which is {book_per_day_price}rs per day. Your total due amount is "{total_due_amount}rs". Please return the book to the library as soon as possible to avoid extra charges. '
        send_email(sender_email, sender_password,
                   recipient_email, subject, message)
