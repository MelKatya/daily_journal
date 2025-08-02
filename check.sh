echo "Проверка кода линтерами"
set -e

black --check ./flask-verson

isort --check-only --profile black ./flask-verson

flake8 ./flask-verson

mypy  ./flask-verson

echo "Все проверки пройдены"