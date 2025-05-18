import logging

from django.core.cache import cache

logger = logging.getLogger('django')


def remove_cache(keyname: str):
    """Remove cache by keyname."""
    cache.delete_many(keys=cache.keys('*{0}*'.format(keyname)))
    logger.info('Cache removed {0}'.format(keyname))
