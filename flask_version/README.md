# Daily journal (Flask)

Простое веб-приложение на Flask для отслеживания и управления пользовательских задач.

## Технологии

- Python 3.10+
- Flask ~3.1.1
- HTML / CSS
- Docker (для базы данных)
- WTForms

## Структура проекта
    daily_journal/      
    ├── flask_version                  # Приложение на Flask
    │   ├── api/                       # Роуты приложения
    │   │   ├── __init__.py
    │   │   ├── task.py
    │   │   ├── user.py
    │   │   └── utils.py
    │   ├── core/
    │   │   ├── models/                # Схемы базы данных
    │   │   │   ├── __init__.py
    │   │   │   ├── base.py
    │   │   │   ├── task.py
    │   │   │   └── user.py
    │   │   ├── schemas/               # Схемы валидации wtforms
    │   │   │   ├── __init__.py
    │   │   │   ├── task.py
    │   │   │   └── user.py
    │   │   ├── __init__.py
    │   │   └── config.py
    │   ├── crud/                      # CRUD-операции (доступ к БД)
    │   │   ├── __init__.py
    │   │   ├── task.py
    │   │   └── user.py
    │   ├── static/                    # Стили сайта
    │   │   └── style.css
    │   ├── templates/                 # Шаблоны страниц сайта
    │   │   ├── _formhelpers.html
    │   │   ├── create_task.html
    │   │   ├── delete_id.html
    │   │   ├── login.html
    │   │   ├── mistakes.html
    │   │   ├── register.html
    │   │   ├── task_id.html
    │   │   ├── tasks.html
    │   │   └── user_page.html
    │   ├── .env.template             
    │   ├── docker-compose.yml          
    │   ├── main.py                    # Основной файл запуска приложения 
    │   └── README.md
    ├── .gitignore
    ├── poetry.lock
    ├── poetry.toml
    └── README.md


## Установка проекта

1. Клонируйте репозиторий:
    ```
    git clone https://github.com/MelKatya/daily_journal.git
    cd daily_journal/flask_version
    ```

2. Установите зависимости с помощью Poetry:
    ```
    pip install poetry
    poetry install --extras flask
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
   http://127.0.0.1:5000/
   ```

