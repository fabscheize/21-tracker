import os
import pathlib

import celery.schedules
import dotenv


__all__ = ()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent


def is_true(value):
    return value in ("", "true", "True", "yes", "YES", "1", "y")


dotenv.load_dotenv()

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "FAKE")

DEBUG = is_true(os.getenv("DJANGO_DEBUG", "False"))

ALLOWED_HOSTS = list(
    filter(None, os.getenv("DJANGO_ALLOWED_HOSTS", "").lower().split(",")),
)

DJANGO_MAIL = os.getenv("DJANGO_MAIL", "basic@gmail.com").lower()

MAX_AUTH_ATTEMPTS = int(os.getenv("MAX_AUTH_ATTEMPTS", 3))

DEFAULT_USER_IS_ACTIVE = is_true(
    os.getenv(
        "DJANGO_DEFAULT_USER_IS_ACTIVE",
        "False",
    ),
)

AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "/"


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    "habits.apps.HabitsConfig",
    "homepage.apps.HomepageConfig",
    "users.apps.UsersConfig",
    "notifications.apps.NotificationsConfig",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "users.middleware.CustomUserMiddleware",
]

INTERNAL_IPS = []

if DEBUG:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INSTALLED_APPS += ["debug_toolbar"]
    INTERNAL_IPS += ["127.0.0.1", "localhost"]


ROOT_URLCONF = "tracker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tracker.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation" ".MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".NumericPasswordValidator"
        ),
    },
]

AUTHENTICATION_BACKENDS = [
    "users.backends.CustomBackend",
    "django.contrib.auth.backends.ModelBackend",
]

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static_dev"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

EMAIL_FILE_PATH = BASE_DIR / "send_mail"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERY_TIMEZONE = "Europe/Moscow"

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER",
    "amqp://guest:guest@localhost:5672//",
)

CELERY_BEAT_SCHEDULE = {
    "periodic-task": {
        "task": "habits.tasks.perodic_task",
        "schedule": celery.schedules.timedelta(hours=1),
    },
}
