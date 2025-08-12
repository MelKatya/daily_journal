from datetime import datetime, timedelta

import jwt
from fastapi import Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_jwt_token(user_id: int):
    """
    Создает jwt токен
    """
    expire = datetime.utcnow() + timedelta(settings.jwt.access_token_expire)
    payload = {"user_id": user_id, "exp": expire}
    return jwt.encode(payload, settings.jwt.secret_key, settings.jwt.algorithm)


def get_user_id_from_token(token: str = Depends(oauth2_scheme)):
    """
    Получает ID пользователя из токена
    """
    try:
        payload = jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        pass  # Обработка ошибки истечения срока действия токена
    except jwt.InvalidTokenError:
        pass  # Обработка ошибки недействительного токена
