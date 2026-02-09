from pathlib import Path

import django
from django.conf import settings

TESTS_DIR = Path(__file__).resolve().parent


def pytest_configure():
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django_object_detail",
            "tests",
        ],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [TESTS_DIR / "templates"],
                "APP_DIRS": True,
            }
        ],
        ROOT_URLCONF="tests.urls",
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        USE_TZ=True,
    )
    django.setup()
