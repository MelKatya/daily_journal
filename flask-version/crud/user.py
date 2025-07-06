from passlib.context import CryptContext

from core.models import db

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def add_new_user(name: str, email: str, password: str):
    hashed_password = get_password_hash(password)

    with db.connect() as cur:
        cur.execute(
            """
            INSERT INTO users (name, email, hashed_password)
            VALUES (%s, %s, %s)
            """,
            (name, email, hashed_password),
        )
