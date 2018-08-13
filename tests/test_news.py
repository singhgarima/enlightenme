import unittest
from datetime import datetime

from readme.news import News


class TestNews(unittest.TestCase):
    def test_initialize(self):
        title = 'Test Title'
        body = 'Long Description'
        url = "http://example.com"
        tags = ['python', 'click']
        published_at = datetime.now()

        news = News(title=title, published_at=published_at, body=body, url=url, tags=tags)

        self.assertEqual(title, news.title)
        self.assertEqual(published_at, news.published_at)
        self.assertEqual(body, news.body)
        self.assertEqual(url, news.url)
        self.assertEqual(tags, news.tags)
