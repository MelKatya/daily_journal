from datetime import datetime, timedelta

import jwt
from core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет совпадение введенного пароля с захешированным.

    Args:
        plain_password (str): пароль пользователя.
        hashed_password (str): захешированный пароль.

    Returns:
        bool: True, если пароли совпадают, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Хэширует пароль пользователя.

    Args:
        password (str): пароль пользователя.

    Returns:
        str: захешированный пароль.
    """
    return pwd_context.hash(password)


def create_jwt_token(user_id: int) -> str:
    """
    Создает JWT-токен с ID пользователя.

    Args:
        user_id (int): ID пользователя.

    Returns:
        str: сгенерированный JWT-токен.
    """
    expire = datetime.utcnow() + timedelta(settings.jwt.access_token_expire)
    payload = {"user_id": user_id, "exp": expire}
    return jwt.encode(payload, settings.jwt.secret_key, settings.jwt.algorithm)


def get_user_id_from_token(
    token: str = Depends(oauth2_scheme),  # noqa: B008 E501
) -> int | None:
    """
    Получает ID пользователя из JWT-токена.

    Args:
        token (str): JWT-токен.

    Returns:
        int | None: ID пользователя, если токен валиден, иначе None.

    Raises:
        HTTPException: при истечении срока действия токена или его
            некорректности.
    """
    try:
        payload = jwt.decode(
            token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm]
        )
        return payload.get("user_id")
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise HTTPException(status_code=303, headers={"Location": "/login"})
