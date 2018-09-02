import unittest
from unittest import mock
from unittest.mock import call

from enlightenme.news.news_manager import NewsManager


class TestNewsManager(unittest.TestCase):
    def setUp(self):
        self._keywords = ['a', 'b']
        self._manager = NewsManager('hacker-news', keywords=self._keywords, format_type='list',
                                    source_params={})

    def test_initialize_when_typical(self):
        self._manager = NewsManager('reddit', keywords=self._keywords, format_type='list',
                                    source_params={'key': 'value'})

        self.assertEqual('reddit', self._manager._source_name)
        self.assertEqual({'key': 'value'}, self._manager._source_params)
        self.assertEqual('list', self._manager._format_type)
        self.assertEqual(['a', 'b'], self._manager._keywords)

    def test_initialize_when_no_optional_parameter_is_provided(self):
        self._manager = NewsManager('hacker-news')

        self.assertEqual('hacker-news', self._manager._source_name)
        self.assertEqual('list', self._manager._format_type)
        self.assertEqual(None, self._manager._keywords)
        self.assertEqual({}, self._manager._source_params)

    @mock.patch('enlightenme.news.news_formatters.ListNewsFormatter')
    @mock.patch('enlightenme.sources.hacker_news_source.HackerNewsSource.fetch')
    def test_fetch_and_format_when_typical_then_should_fetch_from_hacker_news_source(self, mock_fetch, _):
        news_list = ['news1', 'news2']
        mock_fetch.return_value = news_list

        self._manager.fetch_and_format()

        self.assertEqual(news_list, self._manager._news_list)
        mock_fetch.assert_called_once_with(keywords=self._keywords)

    @mock.patch('enlightenme.news.news_formatters.ListNewsFormatter')
    @mock.patch('enlightenme.sources.hacker_news_source.HackerNewsSource.fetch')
    def test_fetch_and_format_when_typical_then_should_use_list_formatter_to_format_news(self, mock_fetch,
                                                                                         mock_formatter):
        news_list = ['news1', 'news2']
        mock_fetch.return_value = news_list

        self._manager.fetch_and_format()

        mock_formatter.assert_has_calls([call(news_list), call().format()])

    @mock.patch('enlightenme.news.news_formatters.CsvNewsFormatter')
    @mock.patch('enlightenme.sources.hacker_news_source.HackerNewsSource.fetch')
    def test_fetch_and_format_when_format_is_html_then_should_use_html_formatter_to_format_news(self, mock_fetch,
                                                                                                mock_formatter):
        news_list = ['news1', 'news2']
        mock_fetch.return_value = news_list

        self._manager._format_type = "csv"
        self._manager.fetch_and_format()

        mock_formatter.assert_has_calls([call(news_list), call().format()])

    @mock.patch('enlightenme.news.news_formatters.ListNewsFormatter')
    @mock.patch('enlightenme.sources.hacker_news_source.HackerNewsSource.fetch')
    def test_fetch_and_format_when_no_keywords_are_passed_then_should_pass_keywords_to_source(self, mock_fetch,
                                                                                              mock_formatter):
        news_list = ['news1', 'news2']
        mock_fetch.return_value = news_list

        self._manager = NewsManager('hacker-news')
        self._manager.fetch_and_format()

        mock_formatter.assert_has_calls([call(news_list), call().format()])
