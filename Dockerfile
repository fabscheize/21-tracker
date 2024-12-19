FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements/ requirements/

ARG DJANGO_DEBUG
ENV DJANGO_DEBUG=${DJANGO_DEBUG}
RUN if [ "$DJANGO_DEBUG" = "true" ]; then \
        pip install --no-cache-dir -r requirements/dev.txt; \
    else \
        pip install --no-cache-dir -r requirements/prod.txt; \
    fi

COPY . .

EXPOSE 8000

CMD ["bash", "-c", "if [ \"$DJANGO_DEBUG\" = \"true\" ]; then python manage.py runserver 0.0.0.0:8000; else gunicorn --bind 0.0.0.0:8000 tracker.wsgi:application; fi"]
