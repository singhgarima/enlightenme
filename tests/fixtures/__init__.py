from datetime import datetime
from random import randint
from typing import Dict

from readme.news.news import News


def hacker_news_story(story_id: int, author: str = None, text: str = None) -> Dict:
    story_id = randint(1, 100000) if story_id is None else story_id
    author = 'author' + str(randint(1, 10)) if author is None else author

    story = {'by': author, 'descendants': 42, 'id': story_id, 'kids': [], 'score': 183, 'time': 1533774011,
             'title': 'Show HN: NES Party – Online Multiplayer NES Emulator Using WebRTC', 'type': 'story',
             'url': 'https://nes.party'}
    if text:
        story['text'] = text
    return story


def create_news(title: str = None, published_at: datetime = None, body: str = None, url: str = None, tags=None):
    tags = [] if tags is None else tags
    title = title if title else "I am " + str(randint(1, 100000))
    published_at = datetime.now() if published_at is None else published_at

    return News(title, published_at, body=body, url=url, tags=tags)
