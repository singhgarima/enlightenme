from datetime import datetime
from typing import List


class News:
    def __init__(self, title, published_at: datetime, body: str = None, url: str = None, tags: List = []):
        self.title = title
        self.published_at = published_at
        self.body = body
        self.url = url
        self.tags = tags
