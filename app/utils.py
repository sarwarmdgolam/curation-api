import logging

from django.core.cache import cache

logger = logging.getLogger('django')


def remove_cache(keyname: str):
    """Remove cache by keyname."""
    try:
        keys = cache.keys(f'{keyname}')  # Only works with django-redis
        cache.delete_many(keys)
        logger.info("Cache removed %s", keyname)
    except AttributeError:
        # Fallback: Just clear the whole cache in non-Redis environments (like testing)
        cache.clear()
        logger.warning("Cache backend does not support keys(). Cache cleared instead.")