import unittest

from readme.sources import Source
from readme.sources.hacker_news import HackerNews


class TestSource(unittest.TestCase):
    def test_get_all_sources(self):
        self.assertEqual(['hacker-news'], Source.get_all_sources())

    def test_get_source(self):
        self.assertEqual(HackerNews, Source.get_source('hacker-news'))

    def test_get_source_when_invalid_source_name(self):
        self.assertEqual(None, Source.get_source('invalid-name'))

    def test_fetch_is_implemented(self):
        with self.assertRaises(NotImplementedError):
            class SubSource(Source):
                pass

            SubSource().fetch()