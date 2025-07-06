from passlib.context import CryptContext

from core.models import db

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def add_new_user(name: str, email: str, password: str):
    """Добавляет нового пользователя"""
    hashed_password = get_password_hash(password)

    with db.connect() as cur:
        cur.execute(
            """
            INSERT INTO users (name, email, hashed_password)
            VALUES (%s, %s, %s)
            """,
            (name, email, hashed_password),
        )


def check_user_exists(name: str, password: str):
    """Проверяет, что пользователь указанным именем и паролем существует"""

    with db.connect() as cur:
        cur.execute(
            """
            SELECT hashed_password, id
            FROM users 
            WHERE name = %s
            """, (name,)
        )
        user_data = cur.fetchone()

        if not user_data:
            return False

        hashed_password, user_id = user_data
        if not verify_password(password, hashed_password):
            return False

        return user_id


