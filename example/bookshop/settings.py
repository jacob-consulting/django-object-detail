import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Add the project root so django_object_detail can be imported without pip install
sys.path.insert(0, str(BASE_DIR.parent))

SECRET_KEY = "django-insecure-bookshop-example-key-not-for-production"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_bootstrap5",
    "django_object_detail",
    "catalog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bookshop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "bookshop.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "static/"

# django-object-detail template packs
OBJECT_DETAIL_TEMPLATE_PACK_LAYOUT = "split-card"
OBJECT_DETAIL_TEMPLATE_PACK_TYPES = "default"

# django-object-detail icon library
# Options: "bootstrap" (default), "fontawesome"
OBJECT_DETAIL_ICONS_LIBRARY = "bootstrap"
# To use Font Awesome instead, uncomment:
#OBJECT_DETAIL_ICONS_LIBRARY = "fontawesome"
#OBJECT_DETAIL_ICONS_TYPE = "solid"  # or "regular", "light", "thin", "duotone"
