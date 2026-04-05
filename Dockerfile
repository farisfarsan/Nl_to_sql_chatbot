FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY supervisord/app.conf /etc/supervisor/conf.d/app.conf

EXPOSE 8000 8501

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
