import unittest

from enlightenme.sources import Source
from enlightenme.sources.all_source import AllSource
from enlightenme.sources.hacker_news_source import HackerNewsSource
from enlightenme.sources.reddit_source import RedditSource


class TestSource(unittest.TestCase):
    def test_name(self):
        self.assertEqual(None, Source.name())

    def test_params(self):
        self.assertEqual([], Source.params())

    def test_get_all_sources(self):
        sources = Source.get_all_sources()
        self.assertEqual(3, len(sources))
        self.assertIn('hacker-news', sources)
        self.assertIn('reddit', sources)
        self.assertIn('all', sources)

    def test_get_all_source_sub_classes(self):
        sources = Source.get_all_source_sub_classes()
        self.assertEqual(3, len(sources))
        self.assertIn(AllSource, sources)
        self.assertIn(HackerNewsSource, sources)
        self.assertIn(RedditSource, sources)

    def test_get_source(self):
        self.assertEqual(HackerNewsSource, Source.get_source('hacker-news'))

    def test_get_source_when_invalid_source_name(self):
        self.assertEqual(None, Source.get_source('invalid-name'))

    def test_fetch_is_implemented(self):
        with self.assertRaises(NotImplementedError):
            Source().fetch()

