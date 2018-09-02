import unittest
from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock

from enlightenme.sources import Source
from enlightenme.sources.reddit_source import RedditSource
from tests.fixtures import create_reddit


class TestRedditSource(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch('praw.Reddit')
        self.mock_reddit = self.patcher.start()
        self.mock_reddit.return_value = self.mock_reddit

        self._client_id = 'id'
        self._client_secret = 'secret'
        self._source = RedditSource(client_id=self._client_id, client_secret=self._client_secret)

    def tearDown(self):
        self.patcher.stop()

    def test_HELP(self):
        self.assertEqual("Source: Reddit (http://reddit.com/)", RedditSource.HELP)

    def test_HELP(self):
        self.assertEqual(10, RedditSource.NUMBER_OF_REDDITS)

    def test_name(self):
        self.assertEqual("reddit", RedditSource.name())

    def test_params(self):
        params = RedditSource.params()
        self.assertEqual(2, len(params))

        self.assertListEqual(["--client-id", "-c"], params[0].opts)
        self.assertEqual("REDDIT_CLIENT_ID", params[0].envvar)
        self.assertEqual(True, params[0].required)
        self.assertEqual('Client id', params[0].prompt)
        self.assertEqual(True, params[0].hide_input)
        self.assertEqual("See: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps",
                         params[0].help)

        self.assertListEqual(["--client-secret", "-s"], params[1].opts)
        self.assertEqual("REDDIT_CLIENT_SECRET", params[1].envvar)
        self.assertEqual(True, params[1].required)
        self.assertEqual('Client secret', params[1].prompt)
        self.assertEqual(True, params[1].hide_input)
        self.assertEqual("See: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps",
                         params[1].help)

    def test_initialize(self):
        self.assertIsInstance(self._source, Source)
        self.assertIsInstance(self._source, RedditSource)

        self.assertEqual(self._client_id, self._source._client_id)
        self.assertEqual(self._client_secret, self._source._client_secret)

        self.mock_reddit.assert_called_once_with(client_id=self._client_id, client_secret=self._client_secret,
                                                 user_agent='enlightenme')

    def test_fetch_should_get_top_hot_posts_from_reddit(self):
        mock_subreddit = MagicMock()
        self.mock_reddit.subreddit.return_value = mock_subreddit

        self._source.fetch()

        self.mock_reddit.subreddit.assert_called_once_with('all')
        mock_subreddit.hot.assert_called_once_with(limit=10)

    def test_fetch_should_get_top_hot_posts_from_reddit_for_given_keywords(self):
        mock_subreddit = MagicMock()
        self.mock_reddit.subreddit.return_value = mock_subreddit

        self._source.fetch(['python', 'cloud', 'vm'])

        self.mock_reddit.subreddit.assert_called_once_with('python+cloud+vm')
        mock_subreddit.hot.assert_called_once_with(limit=10)

    def test_fetch_should_return_top_10_news(self):
        reddit1 = create_reddit()
        reddit2 = create_reddit()

        mock_subreddit = MagicMock()
        mock_subreddit.hot.return_value = [reddit1, reddit2]
        self.mock_reddit.subreddit.return_value = mock_subreddit

        result = self._source.fetch()

        self.assertEqual(2, len(result))

        self.assertEqual(reddit1.title, result[0].title)
        self.assertEqual(reddit1.url, result[0].url)
        self.assertEqual(datetime.fromtimestamp(reddit1.created_utc), result[0].published_at)
        self.assertEqual(reddit1.selftext, result[0].body)
        self.assertListEqual([reddit1.subreddit], result[0].tags)

        self.assertEqual(reddit2.title, result[1].title)
        self.assertEqual(reddit2.url, result[1].url)
        self.assertEqual(datetime.fromtimestamp(reddit2.created_utc), result[1].published_at)
        self.assertEqual(reddit2.selftext, result[1].body)
        self.assertListEqual([reddit2.subreddit], result[1].tags)
