from typing import Any

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import desc
from starlette.templating import Jinja2Templates


class RunConfig(BaseModel):
    """
    Конфигурация подключения к приложению.

    Attributes:
        host (str): хост подключения.
        port (int): порт подключения.
    """

    host: str = "0.0.0.0"
    port: int = 8000


class DatabaseConfig(BaseSettings):
    """
    Конфигурация подключения к базе данных.

    Attributes:
        url (str): строка подключения к БД.
        echo (bool): логирование SQL-запросов.
        echo_pool (bool): логирование работы пула соединений.
        pool_size (int): размер пула соединений.
        max_overflow (int): максимальное число дополнительных соединений.
    """

    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class JwtConfig(BaseModel):
    """
    Конфигурация JWT.

    Attributes:
        secret_key (str): пароль для подписания JWT.
        algorithm (str): алгоритм.
        access_token_expire (int): время истечения токена.
    """

    secret_key: str
    algorithm: str
    access_token_expire: int = 60


class ParamConfig(BaseModel):
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
    default_db: str | list[bool]
    default_html: str | None = None
    db_map: dict[str, str | list[bool] | Any] | None = None
    html_map: dict[str, str] | None = None


class AllTaskParams(BaseModel):
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
            "down": desc("created_at"),
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
        default_db=[True, False],
        default_html="all",
        db_map={
            "all": [True, False],
            "completed": [
                True,
            ],
            "uncompleted": [
                False,
            ],
        },
        html_map={
            "all": "Все",
            "completed": "Только завершенные",
            "uncompleted": "Только незавершенные",
        },
    )

    SEARCH: ParamConfig = ParamConfig(name="search", default_db="")


class Settings(BaseSettings):
    """
    Хранит настройки для работы приложения.

    Attributes:
        model_config
        run (RunConfig): запуска приложения.
        templates (Any): папка для хранения html форм.
        jwt (JwtConfig): конфигурация JWT.
        tasks (AllTaskParams): параметры сортировки, фильтрации и поиска задач.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.template"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    templates: Any = Jinja2Templates(directory="templates")
    db: DatabaseConfig
    jwt: JwtConfig
    tasks: AllTaskParams = AllTaskParams()


settings = Settings()
