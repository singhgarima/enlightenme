import unittest
from unittest import mock
from unittest.mock import call

from readme.commands.helpers.fetcher import Fetcher


class TestFetcher(unittest.TestCase):
    def setUp(self):
        self._keywords = ['a', 'b']
        self._fetcher = Fetcher('hacker-news', 'list', self._keywords)

    def test_initialize_when_typical(self):
        self.assertEqual('hacker-news', self._fetcher._source_name)
        self.assertEqual('list', self._fetcher._format_type)
        self.assertEqual(['a', 'b'], self._fetcher._keywords)

    def test_initialize_when_no_optional_parameter_is_provided(self):
        self._fetcher = Fetcher('hacker-news')

        self.assertEqual('hacker-news', self._fetcher._source_name)
        self.assertEqual('list', self._fetcher._format_type)
        self.assertEqual(None, self._fetcher._keywords)

    def test_valid(self):
        self.assertTrue(self._fetcher.valid())

    def test_valid_when_invalid_source_then_is_false(self):
        invalid_fetcher = Fetcher('invalid', 'list')
        self.assertFalse(invalid_fetcher.valid())

    @mock.patch('readme.news.news_formatters.ListNewsFormatter')
    @mock.patch('readme.sources.hacker_news.HackerNews.fetch')
    def test_fetch_and_format_when_typical_then_should_fetch_from_hacker_news_source(self, mock_fetch, _):
        news_list = ['news1', 'news2']
        mock_fetch.return_value = news_list

        self._fetcher.fetch_and_format()

        self.assertEqual(news_list, self._fetcher._news_list)
        mock_fetch.assert_called_once_with(keywords=self._keywords)

    @mock.patch('readme.news.news_formatters.ListNewsFormatter')
    @mock.patch('readme.sources.hacker_news.HackerNews.fetch')
    def test_fetch_and_format_when_typical_then_should_use_list_formatter_to_format_news(self, mock_fetch,
                                                                                         mock_formatter):
        news_list = ['news1', 'news2']
        mock_fetch.return_value = news_list

        self._fetcher.fetch_and_format()

        mock_formatter.assert_has_calls([call(news_list), call().format()])

    @mock.patch('readme.news.news_formatters.HtmlNewsFormatter')
    @mock.patch('readme.sources.hacker_news.HackerNews.fetch')
    def test_fetch_and_format_when_format_is_html_then_should_use_html_formatter_to_format_news(self, mock_fetch,
                                                                                                mock_formatter):
        news_list = ['news1', 'news2']
        mock_fetch.return_value = news_list

        self._fetcher._format_type = "html"
        self._fetcher.fetch_and_format()

        mock_formatter.assert_has_calls([call(news_list), call().format()])

    @mock.patch('readme.news.news_formatters.ListNewsFormatter')
    @mock.patch('readme.sources.hacker_news.HackerNews.fetch')
    def test_fetch_and_format_when_no_keywords_are_passed_then_should_pass_keywords_to_source(self, mock_fetch,
                                                                                           mock_formatter):
        news_list = ['news1', 'news2']
        mock_fetch.return_value = news_list

        self._fetcher = Fetcher('hacker-news')
        self._fetcher.fetch_and_format()

        mock_formatter.assert_has_calls([call(news_list), call().format()])