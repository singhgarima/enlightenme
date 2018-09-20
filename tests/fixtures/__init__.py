from datetime import datetime
from random import randint
from typing import Dict
from unittest.mock import MagicMock

from enlightenme.news.news import News


def hacker_news_story(story_id: int, title: str = None, author: str = None, text: str = None, url: str = None) -> Dict:
    story_id = randint(1, 100000) if story_id is None else story_id
    author = 'author' + str(randint(1, 10)) if author is None else author
    title = 'Random Title: ' + str(randint(1, 10)) if title is None else title
    url = 'https://www.url.org/' + str(randint(1, 10)) if url is None else url

    story = {'by': author, 'descendants': 42, 'id': story_id, 'kids': [], 'score': 183, 'time': 1533774011,
             'title': title, 'type': 'story',
             'url': url}
    if text:
        story['text'] = text
    return story


def create_news(title: str = None, published_at: datetime = None, body: str = None, url: str = None, tags=None, source=None):
    tags = [] if tags is None else tags
    source = "reddit" if source is None else source
    title = title if title else "I am " + str(randint(1, 100000))
    published_at = datetime.now() if published_at is None else published_at

    return News(title, published_at, body=body, url=url, tags=tags, source=source)


def create_reddit():
    suffix = str(randint(1, 100000))
    return MagicMock(title='Title1' + suffix,
                     url='http://www.reddit/' + suffix,
                     created_utc=1535854049.0,
                     selftext="hello world!" + suffix,
                     subreddit='sr' + suffix)