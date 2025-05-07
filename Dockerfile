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

# Копирование проекта
COPY . /app
WORKDIR /app

# Заменяем chromedriver вручную на подходящий (v136)
RUN curl -SL https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.39/linux64/chromedriver-linux64.zip -o /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -rf /tmp/*

CMD ["python", "app.py"]
