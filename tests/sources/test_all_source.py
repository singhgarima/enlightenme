from unittest import TestCase, mock

from enlightenme.sources import Source
from enlightenme.sources.all_source import AllSource


class TestAllSource(TestCase):
    def setUp(self):
        self._source = AllSource()

    def test_initialize(self):
        self.assertIsInstance(self._source, Source)
        self.assertIsInstance(self._source, AllSource)

        self.assertEqual(0, len(self._source.sources))

    @mock.patch('enlightenme.sources.hacker_news_source.HackerNewsSource.params', return_value=[1, 2])
    @mock.patch('enlightenme.sources.reddit_source.RedditSource.params', return_value=[3, 4])
    def test_params(self, _, __):
        params = AllSource.params()

        self.assertEqual({1, 2, 3, 4}, set(params))

    def test_HELP(self):
        self.assertEqual("Pulls news from all the available sources", AllSource.HELP)

    def test_name(self):
        self.assertEqual("all", AllSource.name())
