# Используем стабильный bullseye
FROM python:3.10-slim-bullseye

# Установка системных зависимостей (добавлены cairo и pkg-config)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wkhtmltopdf \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    libjpeg62-turbo \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    xfonts-75dpi \
    xfonts-base \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# Сначала обновляем pip, потом ставим зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Явно доставим библиотеку для базы, если она вдруг выпала
RUN pip install --no-cache-dir gunicorn psycopg2-binary

COPY . .

RUN chmod -R 755 /app

CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app