#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    requests_cache.backends.file
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ``file`` cache backend
"""
from .base import BaseCache
from .storage.filedict import FileSystemDict, FileSystemJSONDict


class FileSystemCache(BaseCache):
    """File system cache backend.

    Provides caching to a directory.

    This backend is not designed for caching in production, but rather
    for integration testing, where all interactions with a remote server need to
    be faked/replayed. Using the file system instead of sqlite makes it possible to
    code review the requests/responses.

    The implementation
    """
    def __init__(self, location='cache', **options):
        """
        :param location: directory containing the cache
        """
        super(FileSystemCache, self).__init__(**options)
        self.responses = FileSystemDict(location, 'responses')
        self.keys_map = FileSystemDict(location, 'urls')

