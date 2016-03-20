#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    requests_cache.backends
    ~~~~~~~~~~~~~~~~~~~~~~~

    Classes and functions for cache persistence
"""

from .base import BaseCache
from .file import FileSystemCache

BACKEND_SQLITE = 'sqlite'
BACKEND_MEMORY = 'memory'
BACKEND_MONGO = 'mongo'
BACKEND_REDIS = 'redis'
BACKEND_FILE = 'file'

registry = {
    'memory': BaseCache,
    'file': FileSystemCache
}

_backend_dependencies = {
    BACKEND_SQLITE: 'sqlite3',
    BACKEND_MONGO: 'pymongo',
    BACKEND_REDIS: 'redis'
}

try:
    # Heroku doesn't allow the SQLite3 module to be installed
    from .sqlite import DbCache
    registry[BACKEND_SQLITE] = DbCache
except ImportError:
    DbCache = None

try:
    from .mongo import MongoCache
    registry[BACKEND_MONGO] = registry['mongodb'] = MongoCache
except ImportError:
    MongoCache = None

try:
    from .redis import RedisCache
    registry[BACKEND_REDIS] = RedisCache
except ImportError:
    RedisCache = None


def create_backend(backend_name, cache_name, options):
    if isinstance(backend_name, BaseCache):
        return backend_name

    if backend_name is None:
        backend_name = _get_default_backend_name()
    try:
        return registry[backend_name](cache_name, **options)
    except KeyError:
        if backend_name in _backend_dependencies:
            raise ImportError('You must install the python package: %s' %
                              _backend_dependencies[backend_name])
        else:
            raise ValueError('Unsupported backend "%s" try one of: %s' %
                             (backend_name, ', '.join(registry.keys())))


def _get_default_backend_name():
    if BACKEND_SQLITE in registry:
        return BACKEND_SQLITE
    return BACKEND_MEMORY

