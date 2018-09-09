from unittest import TestCase, mock

from enlightenme.sources import Source
from enlightenme.sources.all_source import AllSource
from tests.fixtures import create_news


class TestAllSource(TestCase):
    def setUp(self):
        self._source = AllSource(reddit_client_id=123, reddit_client_secret=234)

    def test_initialize(self):
        self.assertIsInstance(self._source, Source)
        self.assertIsInstance(self._source, AllSource)

        self.assertEqual(2, len(self._source.sources))
        self.assertIsInstance(self._source.sources[0], Source)
        self.assertIsInstance(self._source.sources[1], Source)

    def test_params(self):
        params = AllSource.params()

        self.assertEqual(2, len(params))
        self.assertEqual('reddit_client_id', params[0].name)
        self.assertEqual(['--reddit-client-id'], params[0].opts)
        self.assertEqual('reddit_client_secret', params[1].name)
        self.assertEqual(['--reddit-client-secret'], params[1].opts)

    def test_HELP(self):
        self.assertEqual("Pulls news from all the available sources", AllSource.HELP)

    def test_name(self):
        self.assertEqual("all", AllSource.name())

    @mock.patch('enlightenme.sources.hacker_news_source.HackerNewsSource.fetch')
    @mock.patch('enlightenme.sources.reddit_source.RedditSource.fetch')
    def test_fetch_should_call_fetch_method_for_all_sources(self, mock_hn_fetch, mock_reddit_fetch):
        news1 = create_news()
        news2 = create_news()
        mock_hn_fetch.return_value = [news1]
        mock_reddit_fetch.return_value = [news2]

        news_list = self._source.fetch()

        self.assertEqual(2, len(news_list))
        self.assertIn(news1, news_list)
        self.assertIn(news2, news_list)
        mock_hn_fetch.assert_called_once_with()
        mock_reddit_fetch.assert_called_once_with()
