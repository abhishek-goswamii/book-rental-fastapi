from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_USERNAME:str
    DATABASE_PASSWORD:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    SMTPPASSWORD:str
    HOSTNAME:str
    PORT:int
    DATABASE_NAME:str
    TESTING_DB_NAME:str
    TESTING_DB_HOST:str
    TESTING_DB_PORT:int
    SMTPEMAIL:str
    SMTPPASSWORD:str
    
    class Config:
        env_file=".env"

settings=Settings()