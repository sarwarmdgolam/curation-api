
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'app.core',
    'app.contents',
    'rest_framework_simplejwt',
]

# Use local in-memory cache instead of Redis
CACHES = {
    "default": {
        # "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Other test-specific settings (optional)
DEBUG = False
