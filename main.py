from random import randrange
from fastapi import FastAPI, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import schemas
import utils
import oauth2
from routers import rent, user, book, genre, review
import auth
from fastapi.middleware.cors import CORSMiddleware
from jobs import job1

# models.Base.metadata.create_all(bind=engine)

# If the import statement executes without errors, smtplib is installed

app = FastAPI()
job1.scheduler.start()



origins = [
    "http://www.google.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(genre.router)
app.include_router(review.router)

app.include_router(rent.router)


while True:
    try:
        conn = psycopg2.connect(host='localhost', port=5432, database='fastapi',
                                user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connected')
        break
    except Exception as error:
        print('error: connection failed')
        print(error)
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "homepage"}


@app.get("/admin")
async def admin(user_id: int = Depends(oauth2.get_current_user)):
    return "admin"
