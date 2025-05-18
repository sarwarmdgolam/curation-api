# Use local in-memory cache instead of Redis
CACHES = {
    "default": {
        # "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Other test-specific settings (optional)
DEBUG = False
