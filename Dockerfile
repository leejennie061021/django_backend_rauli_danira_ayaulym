# Используем легкий образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Запрещаем Python писать файлы кэша .pyc на диск
ENV PYTHONDONTWRITEBYTECODE 1
# Запрещаем буферизацию вывода (чтобы логи были видны сразу)
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости системы (нужны для некоторых библиотек Python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]