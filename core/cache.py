import time
from core.config import CACHE_TTL_SECONDS

_cache = {}

def get_cache(key):
    item = _cache.get(key)
    if not item:
        return None
    expires, value = item
    if time.time() > expires:
        _cache.pop(key, None)
        return None
    return value

def set_cache(key, value, ttl=CACHE_TTL_SECONDS):
    _cache[key] = (time.time() + ttl, value)
