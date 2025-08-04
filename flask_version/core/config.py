import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConfig:
    """
    Конфигурация подключения к базе данных.

    Attributes:
        database (str | None): имя базы данных.
        user (str | None): имя пользователя.
        password (str | None): пароль пользователя.
        host (str | None): адрес хоста базы данных.
    """

    database: str | None = os.getenv("DATABASE")
    user: str | None = os.getenv("USER")
    password: str | None = os.getenv("PASSWORD")
    host: str | None = os.getenv("HOST")


@dataclass
class UserAuth:
    """
    Константы ключей для хранения данных пользователя в сессии.

    Attributes:
        user_id (str): ключ для хранения ID пользователя.
        name (str): ключ для хранения имени пользователя.
    """

    user_id: str = "user_id"
    name: str = "name"


@dataclass
class ParamConfig:
    """
    Класс-шаблон для хранения параметров сортировки/фильтрации/поиска

    Attributes:
        name (str): название параметра.
        default_db (str | tuple): значение по умолчанию для работы с бд.
        default_html (str | None): значение по умолчанию для отображения
            на HTML-страница.
        db_map (dict[str, str | tuple[str, ...]] | None):
            сопоставление значений из HTML-страницы с выражениями для SQL.
        html_map (dict[str, str] | None):
            сопоставление ключей с читаемыми подписями на HTML-странице.
    """

    name: str
    default_db: str | tuple
    default_html: str | None = None
    db_map: dict[str, str] | dict[str, tuple[str, ...]] | None = None
    html_map: dict[str, str] | None = None


@dataclass
class AllTaskParams:
    """
    Хранит преднастроенные параметры для сортировки, фильтрации и поиска задач.

    Attributes:
        SORTED (ParamConfig): параметры сортировки задач.
        FILTER (ParamConfig): параметры фильтрации задач по статусу выполнения.
        SEARCH (ParamConfig): параметры поиска задач по имени.
    """

    SORTED: ParamConfig = ParamConfig(
        name="sorted",
        default_db="created_at",
        default_html="up",
        db_map={
            "up": "created_at",
            "down": "created_at DESC",
            "completed": "completed_at",
            "name": "name",
        },
        html_map={
            "up": "Сначала старые",
            "down": "Сначала новые",
            "completed": "По дате завершения",
            "name": "По названию",
        },
    )

    FILTER: ParamConfig = ParamConfig(
        name="filter",
        default_db=("true", "false"),
        default_html="all",
        db_map={
            "all": ("true", "false"),
            "completed": ("true",),
            "uncompleted": ("false",),
        },
        html_map={
            "all": "Все",
            "completed": "Только завершенные",
            "uncompleted": "Только незавершенные",
        },
    )

    SEARCH: ParamConfig = ParamConfig(name="search", default_db="")


@dataclass
class Settings:
    """
    Хранит настройки для работы приложения.

    Attributes:
        db (DatabaseConfig): конфигурация бд.
        users_data (UserAuth): ключи для хранения данных пользователя в сессии.
        secret_key (str | None): секретный ключ для подписи сессий Flask.
        tasks (AllTaskParams): параметры сортировки, фильтрации и поиска задач.
    """

    db: DatabaseConfig = DatabaseConfig()
    users_data: UserAuth = UserAuth()
    secret_key: str | None = os.getenv("SESSION_KEY")
    tasks: AllTaskParams = AllTaskParams()


settings = Settings()
