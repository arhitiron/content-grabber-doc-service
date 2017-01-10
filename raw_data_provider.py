import urllib2

from cache_client import CacheClient


class ResourceProvider:
    def __init__(self, cache_addr):
        self._cache_service = CacheClient(cache_addr)

    def get_resource(self, url):
        cache = self._cache_service.get_cache(url)
        if cache.resource == "":
            res = urllib2.urlopen(url).read()
            decoded_res = res.decode('utf-8')
            return decoded_res
        return cache.resource
