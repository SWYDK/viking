# Используйте официальный образ Python в качестве базового
FROM python:3.11-slim

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файл зависимостей и установите их
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте все файлы в рабочую директорию
COPY . .

# Выполните миграции при запуске контейнера
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
