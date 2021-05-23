# type: ignore # FIXME: lazy

import os
import types

import requests_cache.backends  # noqa: E402
import requests_cache.backends.base  # noqa: E402


try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping

import pickle


# By default tests use persistent (commited to Git) cache.
# Setting this env-var allows the cache to be populated.
# This is necessary if, say, adding new test case or TVDB response changes.
# It is recommended to clear the cache directory before re-populating the cache.
ALLOW_CACHE_WRITE_ENV_VAR = "TVNAMER_TESTS_ALLOW_CACHE_WRITE"
ALLOW_CACHE_WRITE = os.getenv(ALLOW_CACHE_WRITE_ENV_VAR, "0") == "1"


class FileCacheDict(MutableMapping):
    def __init__(self, base_dir):
        self._base_dir = base_dir

    def __getitem__(self, key):
        path = os.path.join(self._base_dir, key)
        try:
            with open(path, "rb") as f:
                data = pickle.load(f)
                return data
        except FileNotFoundError:
            if not ALLOW_CACHE_WRITE:
                raise RuntimeError("No cache file found %s (and %s is not active)" % (path, ALLOW_CACHE_WRITE_ENV_VAR))
            raise KeyError

    def __setitem__(self, key, item):
        if ALLOW_CACHE_WRITE:
            path = os.path.join(self._base_dir, key)
            with open(path, "wb") as f:
                # Dump with protocol 2 to allow Python 2.7 support
                f.write(pickle.dumps(item, protocol=2))
        else:
            raise RuntimeError(
                "Requested uncached URL and $%s not set to 1" % (ALLOW_CACHE_WRITE_ENV_VAR)
            )

    def __delitem__(self, key):
        raise RuntimeError("Removing items from test-cache not supported")

    def __len__(self):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def __str__(self):
        return str(dict(self.items()))


class FileCache(requests_cache.backends.base.BaseCache):
    def __init__(self, _name, fc_base_dir, **options):
        super(FileCache, self).__init__(**options)
        self.responses = FileCacheDict(base_dir=fc_base_dir)
        self.keys_map = FileCacheDict(base_dir=fc_base_dir)


requests_cache.backends.registry['tvnamer_file_cache'] = FileCache


def get_test_cache_session():
    here = os.path.dirname(os.path.abspath(__file__))
    sess = requests_cache.CachedSession(
        backend="tvnamer_file_cache",
        fc_base_dir=os.path.join(here, "..", "tests", "httpcache"),
        include_get_headers=True,
        allowable_codes=(200, 404),
    )
    import tvdb_api
    sess.cache.create_key = types.MethodType(tvdb_api.create_key, sess.cache)
    return sess
