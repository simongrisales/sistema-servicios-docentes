import sys  # noqa: E402

from .base import *  # noqa: F403
from .base import env

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    }
}

use_sqlite = env.bool("USE_SQLITE", default=False)
is_test_run = "test" in sys.argv or "pytest" in sys.modules

if use_sqlite or is_test_run:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:" if is_test_run else str(BASE_DIR / "db.sqlite3"),
        }
    }

if is_test_run:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }

RECAPTCHA_TESTING_MODE = True
RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

# Permite usar claves de test de Google sin fallar `manage.py check` en dev.
SILENCED_SYSTEM_CHECKS = [
    "django_recaptcha.recaptcha_test_key_error",
    "captcha.recaptcha_test_key_error",
]

