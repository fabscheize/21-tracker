FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements/prod.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tracker.wsgi:application"]
