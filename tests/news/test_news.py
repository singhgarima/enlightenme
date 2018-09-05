import unittest
from datetime import datetime

from enlightenme.news.news import News, DATE_TIME_STR_FORMAT


class TestNews(unittest.TestCase):
    def setUp(self):
        self._title = 'Test Title'
        self._body = 'Long Description'
        self._url = "http://example.com"
        self._tags = ['python', 'click']
        self._published_at = datetime.now()
        self._news = News(title=self._title, published_at=self._published_at, body=self._body, url=self._url,
                          tags=self._tags)

    def test_initialize(self):
        self.assertEqual(self._title, self._news.title)
        self.assertEqual(self._published_at, self._news.published_at)
        self.assertEqual(self._body, self._news.body)
        self.assertEqual(self._url, self._news.url)
        self.assertEqual(self._tags, self._news.tags)

    def test_has_any_keyword_when_keyword_in_tags(self):
        self.assertTrue(self._news.has_any_keyword('PYTHON'))

    def test_has_any_keyword_when_keyword_in_title(self):
        self.assertTrue(self._news.has_any_keyword('title'))

    def test_has_any_keyword_when_keyword_in_body(self):
        self.assertTrue(self._news.has_any_keyword('LONG'))

    def test_has_any_keyword_when_keyword_not_found(self):
        self.assertFalse(self._news.has_any_keyword('nonexistent'))

    def test_contains_any_keywords_when_one_keyword_in_tags(self):
        self.assertTrue(self._news.contains_any_keywords(['python', 'nonexistent']))

    def test_contains_any_keywords_when_one_keyword_in_title(self):
        self.assertTrue(self._news.contains_any_keywords(['Title', 'nonexistent']))

    def test_contains_any_keywords_when_one_keyword_in_body(self):
        self.assertTrue(self._news.contains_any_keywords(['Long', 'nonexistent']))

    def test_contains_any_keywords_when_one_keyword_not_found(self):
        self.assertFalse(self._news.contains_any_keywords(['nonexistent', 'nonexistent']))

    def test_to_dict(self):
        self.assertDictEqual({'title': self._title,
                           'published_at': datetime.strftime(self._published_at, DATE_TIME_STR_FORMAT),
                           'body': self._body,
                           'url': self._url,
                           'tags': self._tags
                           }, self._news.to_dict())
