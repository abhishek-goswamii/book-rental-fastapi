from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from config import settings
# db_username = os.getenv("DATABASE_USERNAME")
# db_password = os.getenv("DATABASE_PASSWORD")
# db_port = os.getenv("PORT")
# db_name = os.getenv("DATABASE_NAME")
# db_host = os.getenv("HOSTNAME")
# testt = os.getenv("ENVV")

db_username = settings.DATABASE_USERNAME
db_password = settings.DATABASE_PASSWORD
db_port = settings.PORT
db_name = settings.DATABASE_NAME
db_host = settings.HOSTNAME

print(db_username)
print(db_password)
print(db_port)
print(db_name)
print(db_host)
print(settings.TEST)

db_url = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
