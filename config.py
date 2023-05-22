from pydantic import BaseSettings


class Settings(BaseSettings):
    database_username = str
    database_password = str
    secret_key = str

    class Config:
        env_file = ".env"


settings = Settings()
