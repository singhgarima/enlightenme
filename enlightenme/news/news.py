from datetime import datetime


class News:
    def __init__(self, title, published_at: datetime = None,
                 body: str = None, url: str = None, tags=None):
        if tags is None:
            tags = []
        self.title = title
        self.published_at = published_at if published_at else datetime.now()
        self.body = body
        self.url = url
        self.tags = tags

    def contains_any_keywords(self, keywords):
        for keyword in keywords:
            if self.has_any_keyword(keyword):
                return True
        return False

    def has_any_keyword(self, keyword: str) -> bool:
        upper_case_keyword = keyword.upper()
        return (self.title and upper_case_keyword in self.title.upper()) or \
               (self.tags and upper_case_keyword in
                [tag.upper() for tag in self.tags]) or \
               (self.body and upper_case_keyword in self.body.upper())
