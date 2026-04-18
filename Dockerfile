FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libpango-1.0-0 libglib2.0-0 \
    libharfbuzz0b libpangoft2-1.0-0 libpangocairo-1.0-0 libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn psycopg2-binary

COPY . .

# Это лечит проблемы прав доступа Windows
RUN chmod -R 755 /app

# Используем максимально простую команду без скобок
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 app:app