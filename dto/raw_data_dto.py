import time


class RawDataDto:
    def __init__(self, data, url, version=1):
        self.data = data
        self.url = url
        self.version = version
        self.created = time.time()
