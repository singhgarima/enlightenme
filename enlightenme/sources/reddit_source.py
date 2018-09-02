from typing import List

import click

from enlightenme.news.news import News
from enlightenme.sources import Source


class RedditSource(Source):
    HELP = "Source: Reddit (http://reddit.com/)"

    @classmethod
    def name(cls):
        return 'reddit'

    @classmethod
    def params(cls) -> List[click.Parameter]:
        client_help = "See: https://github.com/reddit-archive/" + \
                      "reddit/wiki/OAuth2-Quick-Start-Example#first-steps"
        return [
            click.Option(('--client_id', '-c'),
                         envvar='REDDIT_CLIENT_ID',
                         required=True,
                         help=client_help),
            click.Option(('--client_secret', '-s'),
                         envvar='REDDIT_CLIENT_SECRET',
                         required=True,
                         prompt=True,
                         hide_input=True,
                         help=client_help)
        ]

    def fetch(self, keywords: List = None) -> List[News]:
        return []
