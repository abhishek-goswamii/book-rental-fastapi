from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

db_username = os.getenv("DATABASE_USERNAME")
db_password = os.getenv("DATABASE_PASSWORD")
db_port = os.getenv("PORT")
db_name = os.getenv("DATABASE_NAME")
db_host = os.getenv("HOSTNAME")

db_url = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'


# f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
