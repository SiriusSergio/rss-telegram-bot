FROM python:3.11-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установка рабочей директории
WORKDIR /app
COPY . .

# Переменная окружения для chromium
ENV CHROME_BIN=/usr/bin/chromium

# Запуск бота
CMD ["python", "app.py"]
