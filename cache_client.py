import json
import logging
import urllib
import urllib2

import sys


class CacheClient:
    def __init__(self, addr):
        self._address = addr

    def get_cache(self, key):
        values = dict(key=key)
        data = urllib.urlencode(values)
        req = urllib2.Request(self._address + "/get-cache", data)
        resp = urllib2.urlopen(req)
        content = resp.read()
        if content == "":
            return RawCache()
        try:
            raw_data = json.loads(content.decode('utf-8'))
            return RawCache(raw_data)
        except:
            logging.info("Catch exception:")
            logging.info(sys.exc_info())
            return RawCache()


class RawCache:
    def __init__(self, data="", version=0):
        self.data = data
        self.version = version
