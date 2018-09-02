import unittest

from enlightenme.sources import Source
from enlightenme.sources.reddit_source import RedditSource


class TestReddit(unittest.TestCase):
    def setUp(self):
        self._source = RedditSource()

    def test_HELP(self):
        self.assertEqual("Source: Reddit (http://reddit.com/)", RedditSource.HELP)

    def test_name(self):
        self.assertEqual("reddit", RedditSource.name())

    def test_params(self):
        params = RedditSource.params()
        self.assertEqual(2, len(params))

        self.assertListEqual(["--client_id", "-c"], params[0].opts)
        self.assertEqual("REDDIT_CLIENT_ID", params[0].envvar)
        self.assertEqual(True, params[0].required)
        self.assertEqual("See: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps",
                         params[0].help)

        self.assertListEqual(["--client_secret", "-s"], params[1].opts)
        self.assertEqual("REDDIT_CLIENT_SECRET", params[1].envvar)
        self.assertEqual(True, params[1].required)
        self.assertEqual('Client secret', params[1].prompt)
        self.assertEqual(True, params[1].hide_input)
        self.assertEqual("See: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps",
                         params[1].help)

    def test_initialize(self):
        self.assertIsInstance(self._source, Source)
        self.assertIsInstance(self._source, RedditSource)

    def test_fetch_should_get_top_hot_posts_from_reddit(self):
        self.assertEqual([], self._source.fetch())
