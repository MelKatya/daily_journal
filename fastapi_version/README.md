# Daily journal (Flask)

Простое веб-приложение на Flask для отслеживания и управления пользовательских задач.

## Технологии

- Python 3.10+
- FastAPI 0.116.1
- Alembic 1.16.4
- HTML / CSS
- Docker (для базы данных)
- WTForms

## Структура проекта
    daily_journal/
    ├── fastapi_version/                     # Приложение на Flask
    │   ├── alembic/                         # Миграция базы данных
    │   │   └── ... 
    │   ├── api/                             # Роуты приложения
    │   │   ├── __init__.py
    │   │   ├── tasks.py
    │   │   ├── users.py
    │   │   └── utils.py
    │   ├── core/
    │   │   ├── models/                      # Схемы базы данных
    │   │   │   ├── __init__.py
    │   │   │   ├── base.py
    │   │   │   ├── db_helper.py
    │   │   │   ├── task.py
    │   │   │   └── user.py
    │   │   ├── schemas/                     # Схемы валидации
    │   │   │   ├── __init__.py
    │   │   │   ├── tasks.py
    │   │   │   └── users.py
    │   │   ├── __init__.py
    │   │   └── config.py
    │   ├── crud/                            # CRUD-операции (доступ к БД)
    │   │   ├── __init__.py
    │   │   ├── task.py
    │   │   └── user.py
    │   ├── security/                        # Генерация хэшев паролей и JWT-токенов
    │   │   ├── __init__.py
    │   │   └── utils.py
    │   ├── static/
    │   │   └── style.css                    # Стили сайта
    │   ├── templates/                       # Шаблоны страниц сайта
    │   │   ├── _formhelpers.html
    │   │   └── ...
    │   ├── .env.template
    │   ├── README.md
    │   ├── alembic.ini
    │   ├── docker-compose.yml
    │   └── main.py                          # Основной файл запуска приложения 
    ├── images_for_readme/                   # Изображения для readme
    │   ├── all_tasks.png
    │   └── ...
    ├── README.md
    ├── path_write.py
    ├── poetry.lock
    └── pyproject.toml

Process finished with exit code 0



## Установка проекта

1. Клонируйте репозиторий:
    ```
    git clone https://github.com/MelKatya/daily_journal.git
    cd daily_journal/fastapi_version
    ```

2. Установите зависимости с помощью Poetry:
    ```
    pip install poetry
    poetry install --extras fastapi
    ```
3. Скопируйте файл .env.template и переименуйте в .env:
   ```
    cp .env.template .env
    ```
    При необходимости — укажите свои параметры подключения к базе данных.

4. Запустите базу данных (Docker):
    ```
    docker-compose up -d
    ```
5. Запустите приложение:

   ```
   python main.py
   ```

6. Откройте в браузере:
   ```
   http://127.0.0.1:8000/
   ```

