from settings.base import *  # noqa: F403

ENVIRONMENT = "test"

DEBUG = False

# ruff: noqa: F405
DATABASES["default"]["TEST"] = {"SERIALIZE": False}
DATABASES["default"]["TEST"]["NAME"] = "test_" + str(os.getpid())

DEFAULT_FILE_STORAGE = "django.core.files.storage.InMemoryStorage"
