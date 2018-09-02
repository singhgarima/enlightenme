from datetime import datetime
from typing import List

import click
import praw

from enlightenme.news.news import News
from enlightenme.sources import Source


class RedditSource(Source):
    NUMBER_OF_REDDITS = 10
    HELP = "Source: Reddit (http://reddit.com/)"

    def __init__(self, client_id: str = None,
                 client_secret: str = None) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self.reddit = praw.Reddit(client_id=client_id,
                                  user_agent='enlightenme',
                                  client_secret=self._client_secret)

    @classmethod
    def name(cls):
        return 'reddit'

    @classmethod
    def params(cls) -> List[click.Parameter]:
        client_help = "See: https://github.com/reddit-archive/" + \
                      "reddit/wiki/OAuth2-Quick-Start-Example#first-steps"
        return [
            click.Option(('--client-id', '-c'),
                         envvar='REDDIT_CLIENT_ID',
                         required=True,
                         prompt=True,
                         hide_input=True,
                         help=client_help),
            click.Option(('--client-secret', '-s'),
                         envvar='REDDIT_CLIENT_SECRET',
                         required=True,
                         prompt=True,
                         hide_input=True,
                         help=client_help)
        ]

    def fetch(self, keywords: List = None) -> List[News]:
        subreddits = '+'.join(keywords) if keywords else 'all'
        hot_reddits = self.reddit.subreddit(subreddits). \
            hot(limit=RedditSource.NUMBER_OF_REDDITS)
        return [
            News(title=submission.title,
                 published_at=datetime.fromtimestamp(submission.created_utc),
                 url=submission.url,
                 body=submission.selftext,
                 tags=[str(submission.subreddit)]
                 )
            for submission in hot_reddits]
