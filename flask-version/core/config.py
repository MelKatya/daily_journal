import os

from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    database = os.getenv("DATABASE")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    host = os.getenv("HOST")


class Settings:
    db: DatabaseConfig = DatabaseConfig()


settings = Settings()
