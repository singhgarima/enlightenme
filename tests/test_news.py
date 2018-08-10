import unittest
from datetime import datetime

from readme.news import News, NewsFormatter, ConsoleNewsFormatter
from tests.fixtures import create_news


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


class TestNewsFormatter(unittest.TestCase):
    def setUp(self):
        self._news_list = [create_news()]
        self._formatter = NewsFormatter(self._news_list)

    def test_initialize(self):
        self.assertEqual(self._news_list, self._formatter.news_list)
        self.assertEqual(None, self._formatter._output)

    def test_set_news_list(self):
        new_news_list = [create_news(), create_news()]
        self._formatter.news_list = new_news_list

        self.assertEqual(new_news_list, self._formatter.news_list)

    def test_format_is_an_abstract_method(self):
        class SubFormatter(NewsFormatter):
            pass

        with self.assertRaises(NotImplementedError):
            NewsFormatter(self._news_list).format()


class TestConsoleNewsFormatter(unittest.TestCase):
    def test_format(self):
        news = create_news()
        formatter = ConsoleNewsFormatter([news])

        formatter.format()

        self.assertEqual(
            ("\n" +
             "\t1. Title: %s\n" +
             "\t   Published At: %s\n") % (
                news.title, news.published_at.strftime('%Y-%m-%dT%H:%M:%SZ')),
            formatter._output)

    def test_format_when_news_has_urls(self):
        url = "http://example.com/thistest"
        news = create_news(url=url)
        formatter = ConsoleNewsFormatter([news])

        formatter.format()

        self.assertEqual(
            ("\n" +
             "\t1. Title: %s\n" +
             "\t   Published At: %s\n" +
             "\t   URL: %s\n"
             ) % (
                news.title,
                news.published_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                url
            ),
            formatter._output)

    def test_format_when_news_has_tags(self):
        tags = ["python", "click"]
        news = create_news(tags=tags)
        formatter = ConsoleNewsFormatter([news])

        formatter.format()

        self.assertEqual(
            ("\n" +
             "\t1. Title: %s\n" +
             "\t   Published At: %s\n" +
             "\t   Tags: %s\n"
             ) % (
                news.title,
                news.published_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                ", ".join(tags)
            ),
            formatter._output)
