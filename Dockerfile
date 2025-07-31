FROM python:3.13.0-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY scripts/wait-for-db.sh /scripts/wait-for-db.sh

RUN chmod +x /scripts/wait-for-db.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]