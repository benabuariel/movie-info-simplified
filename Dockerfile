# ---- Base (shared) ----
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# ---- Dev image ----
FROM base AS dev
ENV DJANGO_SETTINGS_MODULE=movie_info_demo.settings.local \
    DEBUG=1

COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ---- Prod image ----
FROM base AS prod
ENV DJANGO_SETTINGS_MODULE=movie_info_demo.settings.production \
    DEBUG=0

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "movie_info_demo.wsgi:application"]
