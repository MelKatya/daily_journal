import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    database = os.getenv("DATABASE")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    host = os.getenv("HOST")


@dataclass
class UserAuth:
    user_id: str = "user_id"
    name: str = "name"


@dataclass
class ParamConfig:
    name: str
    default_db: str | tuple
    default_html: str | None = None
    db_map: dict[str, str] | dict[str, tuple[str, ...]] | None = None
    html_map: dict[str, str] | None = None


@dataclass
class AllTaskParams:
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
    db: DatabaseConfig = DatabaseConfig()
    users_data: UserAuth = UserAuth()
    secret_key: str | None = os.getenv("SESSION_KEY")
    tasks: AllTaskParams = AllTaskParams()


settings = Settings()
