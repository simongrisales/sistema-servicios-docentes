from pathlib import Path
from datetime import timedelta

import environ

BASE_DIR = Path(__file__).resolve().parents[3]
BACKEND_DIR = BASE_DIR / "backend"

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "clave-insegura-solo-para-desarrollo"),
    DJANGO_SECRET_KEY=(str, "clave-insegura-solo-para-desarrollo"),
    DATABASE_URL=(str, ""),
    # Permite Hostnames internos de Docker y/o requests directos a servicios.
    # Importante: Django valida request.get_host() contra ALLOWED_HOSTS.
    ALLOWED_HOSTS=(list, [
        "localhost",
        "127.0.0.1",
        "django",
        "daphne",
        "nginx",
        "django:8000",
        "daphne:8001",
        "127.0.0.1:8000",
        "*:8000",
        "*",
    ]),
    POSTGRES_DB=(str, "sistema_servicios_docentes"),
    POSTGRES_USER=(str, "servicios_docentes"),
    POSTGRES_PASSWORD=(str, "servicios_docentes"),
    POSTGRES_HOST=(str, "localhost"),
    POSTGRES_PORT=(int, 5432),
    VALKEY_HOST=(str, "localhost"),
    VALKEY_PORT=(int, 6379),
    VALKEY_URL=(str, ""),
    CHANNEL_LAYERS_URL=(str, ""),
    JWT_SECRET_KEY=(str, "jwt-inseguro-solo-para-desarrollo"),
    JWT_SECRET=(str, "jwt-inseguro-solo-para-desarrollo"),
    JWT_ACCESS_TOKEN_LIFETIME=(int, 60),
    JWT_REFRESH_TOKEN_LIFETIME=(int, 7),
    RECAPTCHA_PUBLIC_KEY=(str, ""),
    RECAPTCHA_PRIVATE_KEY=(str, ""),
    PROMETHEUS_PORT=(int, 9090),
    GRAFANA_PORT=(int, 3000),
    GRAFANA_ADMIN_USER=(str, "admin"),
    GRAFANA_ADMIN_PASSWORD=(str, "admin"),
)


env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env("SECRET_KEY") or env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")
DATABASE_URL = env("DATABASE_URL")

# Normalización: dependiendo de cómo Docker/ENV inyecte variables,
# ALLOWED_HOSTS puede venir como lista, string ("a,b,c") o string con comas.
# Esto evita errores de DisallowedHost en producción.
if isinstance(ALLOWED_HOSTS, str):
    ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS.split(",") if h.strip()]

# En despliegues con Docker, es común que el host llegue como <servicio>:<puerto>
# (ej: "django:8000"). También puede incluir el puerto explícitamente.
extra_hosts = [
    "django:8000",
    "daphne:8001",
    "127.0.0.1:8000",
    "localhost:8000",
    "*:8000",
]
for h in extra_hosts:
    if h not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(h)

# Normalización extra: evitar fallos si ALLOWED_HOSTS incluye valores con espacios.
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS if h and h.strip()]




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
    "notifications.apps.NotificationsConfig",
    "core",
    "apps.usuarios",
    "apps.academico",
    "apps.asignacion",
    "apps.parametros",
    "apps.reservas",
    "apps.reportes",
    "apps.notificaciones.apps.NotificacionesConfig",
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

if DATABASE_URL:
    DATABASES["default"] = env.db("DATABASE_URL")

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
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_IGNORE_RESULT = False
CELERY_TIMEZONE = "America/Bogota"
SIMPLE_JWT = {
    "SIGNING_KEY": env("JWT_SECRET_KEY") or env("JWT_SECRET"),
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env.int("JWT_ACCESS_TOKEN_LIFETIME", default=60)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=env.int("JWT_REFRESH_TOKEN_LIFETIME", default=7)
    ),
}
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")
PROMETHEUS_PORT = env("PROMETHEUS_PORT")
GRAFANA_PORT = env("GRAFANA_PORT")
GRAFANA_ADMIN_USER = env("GRAFANA_ADMIN_USER")
GRAFANA_ADMIN_PASSWORD = env("GRAFANA_ADMIN_PASSWORD")

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
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ("es", "Español"),
    ("en", "English"),
]

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
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/login/"
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
