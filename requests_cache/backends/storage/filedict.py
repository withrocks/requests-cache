#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    requests_cache.backends.filedict
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Dictionary-like objects for saving data sets to `file` database
"""
from collections import MutableMapping
import sqlite3 as sqlite
from contextlib import contextmanager
try:
    import threading
except ImportError:
    import dummy_threading as threading
try:
    import cPickle as pickle
except ImportError:
    import pickle

import logging
import os
logger = logging.getLogger(__name__)

class FileSystemDict(MutableMapping):
    def __init__(self, root_directory, sub_directory, **options):
        """
        :param root_directory: The root directory containing the cache files
        """
        self.path = os.path.join(root_directory, sub_directory)
        self._lock = threading.RLock()

    def _file_path(self, key, postfix=""):
        return os.path.join(self.path, key, postfix)

    def __getitem__(self, key):
        # TODO: Wont the long path names be a problem?
        # consider using another key scheme in this case?
        file_path = self._file_path(key)
        exists = os.path.exists(file_path)
        logger.debug("__getitem__: {}=>{}, exists={}".format(key, file_path, exists))

        if exists:
            with open(file_path) as f:
                return f.read()
        else:
            raise KeyError

    def __setitem__(self, key, item):
        logger.debug("__setitem__: {} ({}) {}".format(key, len(item), type(item)))
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # Write the file in a human-readable JSON format (for code reviews)
        # as well as in the pickled format.
        # HACK: Optimal to "unpickle" the JSON object itself
        with open(self._file_path(key), 'w') as f:
            f.write(pickle.dumps(item))

        import json
        serialized = json.dumps(item, default=serialize_to_json, sort_keys=True, indent=True)
        with open(self._file_path(key, extension=".json"), 'w') as f:
            f.write(serialized)

    def __delitem__(self, key):
        logger.debug("__delitem__")

    def __iter__(self):
        for file_name in os.listdir(self.path):
            yield file_name

    def __len__(self):
        return len(os.listdir(self.path))

    def clear(self):
        logger.debug("__delitem__")

    def __str__(self):
        return str(dict(self.items()))


def serialize_to_json(obj):
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    else:
        return "{} can't be serialized".format(type(obj))


