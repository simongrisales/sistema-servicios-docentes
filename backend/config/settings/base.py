from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parents[3]
BACKEND_DIR = BASE_DIR / "backend"

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "clave-insegura-solo-para-desarrollo"),
    DJANGO_SECRET_KEY=(str, "clave-insegura-solo-para-desarrollo"),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    POSTGRES_DB=(str, "sistema_servicios_docentes"),
    POSTGRES_USER=(str, "servicios_docentes"),
    POSTGRES_PASSWORD=(str, "servicios_docentes"),
    POSTGRES_HOST=(str, "localhost"),
    POSTGRES_PORT=(int, 5432),
    VALKEY_HOST=(str, "localhost"),
    VALKEY_PORT=(int, 6379),
    VALKEY_URL=(str, ""),
    CHANNEL_LAYERS_URL=(str, ""),
    JWT_SECRET=(str, "jwt-inseguro-solo-para-desarrollo"),
    RECAPTCHA_PUBLIC_KEY=(str, ""),
    RECAPTCHA_PRIVATE_KEY=(str, ""),
)

env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env("SECRET_KEY") or env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

INSTALLED_APPS = [
    "django_prometheus",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "rest_framework",
    "drf_spectacular",
    "django_ratelimit",
    "django_recaptcha",
    "core",
    "apps.usuarios",
    "apps.academico",
    "apps.asignacion",
    "apps.parametros",
    "apps.reservas",
    "apps.reportes",
    "apps.notificaciones",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]


ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "frontend" / "templates"],
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

DATABASES = {
    "default": {
        "ENGINE": "django_prometheus.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
        "CONN_MAX_AGE": 0,
    }
}

VALKEY_URL = env("VALKEY_URL") or f"redis://{env('VALKEY_HOST')}:{env('VALKEY_PORT')}/0"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": VALKEY_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                env("CHANNEL_LAYERS_URL") or (env("VALKEY_HOST"), env("VALKEY_PORT"))
            ]
        },
    }
}

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default=VALKEY_URL)
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default=VALKEY_URL)
CELERY_TASK_IGNORE_RESULT = False
CELERY_TIMEZONE = "America/Bogota"
SIMPLE_JWT = {"SIGNING_KEY": env("JWT_SECRET")}
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Sistema de Servicios Docentes API",
    "DESCRIPTION": "API para la asignacion academica de aulas de la UCO.",
    "VERSION": "0.1.0",
}

LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# I18N: rutas para mensajes de Django en formatos nativos.
LOCALE_PATHS = [BASE_DIR / "locale"]


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "frontend" / "static"]
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "usuarios.UsuarioModel"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        )
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
