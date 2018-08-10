from typing import List


class News:
    def __init__(self, title, body: str = None, url: str = None, tags: List = []):
        self.title = title
        self.body = body
        self.url = url
        self.tags = tags