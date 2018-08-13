import unittest

from readme.news_formatters import NewsFormatter, ListNewsFormatter, HtmlNewsFormatter
from tests.fixtures import create_news


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

    def test_formatter_for_format(self):
        self.assertEqual(ListNewsFormatter, NewsFormatter.formatter_for_format(format_type='list'))


class TestListNewsFormatter(unittest.TestCase):
    def test_format(self):
        news = create_news()
        formatter = ListNewsFormatter([news])

        formatter.format()

        self.assertEqual(
            ("\n" +
             "\t1. Title: %s\n" +
             "\t    Published At: %s\n") % (
                news.title, news.published_at.strftime('%Y-%m-%dT%H:%M:%SZ')),
            formatter._output)

    def test_format_when_news_has_urls(self):
        url = "http://example.com/thistest"
        news = create_news(url=url)
        formatter = ListNewsFormatter([news])

        formatter.format()

        self.assertEqual(
            ("\n" +
             "\t1. Title: %s\n" +
             "\t    Published At: %s\n" +
             "\t    URL: %s\n"
             ) % (
                news.title,
                news.published_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                url
            ),
            formatter._output)

    def test_format_when_news_has_tags(self):
        tags = ["python", "click"]
        news = create_news(tags=tags)
        formatter = ListNewsFormatter([news])

        formatter.format()

        self.assertEqual(
            ("\n" +
             "\t1. Title: %s\n" +
             "\t    Published At: %s\n" +
             "\t    Tags: %s\n"
             ) % (
                news.title,
                news.published_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                ", ".join(tags)
            ),
            formatter._output)


class TestHtmlNewsFormatter(unittest.TestCase):
    def setUp(self):
        self._news = create_news()
        self._news_list = [self._news]
        self._formatter = HtmlNewsFormatter(self._news_list)

    def test_initialize(self):
        self.assertIsInstance(self._formatter, NewsFormatter)
        self.assertEqual(self._news_list, self._formatter.news_list)
        self.assertEqual(None, self._formatter._output)

    def test_format(self):
        self.assertIsNone(self._formatter.format())