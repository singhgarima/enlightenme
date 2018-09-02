import unittest

from enlightenme.sources import Source
from enlightenme.sources.hacker_news_source import HackerNewsSource


class TestSource(unittest.TestCase):
    def test_name(self):
        self.assertEqual(None, Source.name())

    def test_params(self):
        self.assertEqual([], Source.params())

    def test_get_all_sources(self):
        sources = Source.get_all_sources()
        self.assertEqual(2, len(sources))
        self.assertIn('hacker-news', sources)
        self.assertIn('reddit', sources)

    def test_get_source(self):
        self.assertEqual(HackerNewsSource, Source.get_source('hacker-news'))

    def test_get_source_when_invalid_source_name(self):
        self.assertEqual(None, Source.get_source('invalid-name'))

    def test_fetch_is_implemented(self):
        with self.assertRaises(NotImplementedError):
            class SubSource(Source):
                pass

            SubSource().fetch()
