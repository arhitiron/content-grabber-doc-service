class CacheClient:
    def __init__(self, addr):
        self.__address = addr

    def get_cache(self, key):
        # mock implementation
        return ResourceCache(0, "")


class ResourceCache:
    def __init__(self, version, resource):
        self.version = version
        self.resource = resource
