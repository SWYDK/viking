# Используем официальный Python-образ как базовый
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY telegram_bot/requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код бота в рабочую директорию
COPY telegram_bot/ .

# Команда для запуска бота
CMD ["python", "bot.py"]