from random import randint
from typing import Dict, List

from readme.news import News


def hacker_news_story(story_id: int, author: str = None, text: str = None) -> Dict:
    story_id = randint(1, 100000) if story_id is None else story_id
    author = 'author' + str(randint(1, 10)) if author is None else author

    story = {'by': author, 'descendants': 42, 'id': story_id, 'kids': [], 'score': 183, 'time': 1533774011,
             'title': 'Show HN: NES Party – Online Multiplayer NES Emulator Using WebRTC', 'type': 'story',
             'url': 'https://nes.party'}
    if text:
        story['text'] = text
    return story


def create_news(title: str = None, body: str = None, url: str = None, tags: List = []):
    title = title if title else "I am " + str(randint(1, 100000))

    return News(title, body=body, url=url, tags=tags)
