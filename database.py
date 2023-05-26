from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from config import settings

db_username = settings.DATABASE_USERNAME
db_password = settings.DATABASE_PASSWORD
db_port = settings.PORT
db_name = settings.DATABASE_NAME
db_host = settings.HOSTNAME

db_url = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
print(db_url)

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
