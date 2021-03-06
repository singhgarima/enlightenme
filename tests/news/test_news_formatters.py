import json
import unittest
from datetime import datetime

from enlightenme.news.news import DATE_TIME_STR_FORMAT
from enlightenme.news.news_formatters import NewsFormatter, ListNewsFormatter, CsvNewsFormatter, JsonNewsFormatter
from tests.fixtures import create_news


class TestNewsFormatter(unittest.TestCase):
    def setUp(self):
        self._news_list = [create_news()]
        self._formatter = NewsFormatter(self._news_list)

    def test_initialize(self):
        self.assertEqual(self._news_list, self._formatter.news_list)

    def test_set_news_list(self):
        new_news_list = [create_news(), create_news()]
        self._formatter.news_list = new_news_list

        self.assertEqual(new_news_list, self._formatter.news_list)

    def test_format_is_an_abstract_method(self):
        class SubFormatter(NewsFormatter):
            pass

        with self.assertRaises(NotImplementedError):
            NewsFormatter(self._news_list).format()

    def test_formatter_for_format(self):
        self.assertEqual(ListNewsFormatter, NewsFormatter.formatter_for_format(format_type='list'))


class TestListNewsFormatter(unittest.TestCase):
    def test_format(self):
        news = create_news(source=None)
        formatter = ListNewsFormatter([news])

        output = formatter.format()

        self.assertEqual(
            ("\n" +
             "\t1. Title: %s\n" +
             "\t    Published At: %s\n" +
             "\t    Source: %s\n") % (
                news.title, news.published_at.strftime('%Y-%m-%dT%H:%M:%SZ'), news.source), output)

    def test_format_when_news_has_urls(self):
        url = "http://example.com/thistest"
        news = create_news(url=url)
        formatter = ListNewsFormatter([news])

        output = formatter.format()

        self.assertEqual(
            ("\n" +
             "\t1. Title: %s\n" +
             "\t    Published At: %s\n" +
             "\t    URL: %s\n" +
             "\t    Source: %s\n"
             ) % (
                news.title,
                news.published_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                url,
                news.source
            ), output)

    def test_format_when_news_has_tags(self):
        tags = ["python", "click"]
        news = create_news(tags=tags)
        formatter = ListNewsFormatter([news])

        output = formatter.format()

        self.assertEqual(
            ("\n" +
             "\t1. Title: %s\n" +
             "\t    Published At: %s\n" +
             "\t    Tags: %s\n"
             "\t    Source: %s\n"
             ) % (
                news.title,
                news.published_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                ", ".join(tags),
                news.source
            ), output)


class TestCsvNewsFormatter(unittest.TestCase):
    def setUp(self):
        self._news = create_news()
        self._news_list = [self._news]
        self._formatter = CsvNewsFormatter(self._news_list)

    def test_initialize(self):
        self.assertIsInstance(self._formatter, NewsFormatter)
        self.assertEqual(self._news_list, self._formatter.news_list)

    def test_format(self):
        result = self._formatter.format().split("\n")

        self.assertIn('"title","published_at","body","url","tags"', result[0])
        self.assertIn('"' + self._news.title +
                      '","' +
                      self._news.published_at.strftime('%Y-%m-%dT%H:%M:%SZ') +
                      '","' +
                      str(self._news.body or '') +
                      '","' +
                      str(self._news.url or '') +
                      '","[]"', result[1])


class TestJsonNewsFormatter(unittest.TestCase):
    def setUp(self):
        self._news = create_news()
        self._news_list = [self._news]
        self._formatter = JsonNewsFormatter(self._news_list)

    def test_initialize(self):
        self.assertIsInstance(self._formatter, NewsFormatter)
        self.assertEqual(self._news_list, self._formatter.news_list)

    def test_format(self):
        result = self._formatter.format()

        self.assertListEqual([{'title': self._news.title,
                               'published_at': datetime.strftime(self._news.published_at, DATE_TIME_STR_FORMAT),
                               'source': self._news.source,
                               'body': self._news.body,
                               'url': self._news.url,
                               'tags': []
                               }], json.loads(result))
