import time


class DocDto:
    def __init__(self, title="", description="", location="", date="", author="", author_location="", url=""):
        self.title = title
        self.description = description
        self.location = location
        self.date = date
        self.author = author
        self.author_location = author_location
        self.created = time.time()
        self.url = url
