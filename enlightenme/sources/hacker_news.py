from datetime import datetime
from typing import List

import requests

from enlightenme.news.news import News
from enlightenme.sources import Source


class HackerNews(Source):
    """
    Source: hacker-news (https://news.ycombinator.com/)
    """
    URL = "https://hacker-news.firebaseio.com/"

    LATEST_NUMBER_OF_STORIES_TO_FETCH = 10
    MAX_STORIES_TO_LOOP = 100

    @classmethod
    def name(cls):
        return "hacker-news"

    def fetch(self, keywords: List = None) -> List[News]:
        stories = self._fetch_new_stories()[0:self.MAX_STORIES_TO_LOOP]
        if keywords:
            return self._fetch_latest_stories_with_keywords(stories, keywords)
        else:
            return self._fetch_latest_stories(stories, number=self.LATEST_NUMBER_OF_STORIES_TO_FETCH)

    def _fetch_new_stories(self):
        response = requests.get(self.URL + "v0/newstories.json")
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()

    def _fetch_latest_stories(self, stories, number=20):
        return [self._fetch_story(story_id) for story_id in stories[0:number]]

    def _fetch_latest_stories_with_keywords(self, stories, keywords):
        interesting_news = []
        for index, story_id in enumerate(stories):
            news = self._fetch_story(story_id)
            if news.contains_any_keywords(keywords):
                interesting_news.append(news)
            if len(interesting_news) == self.LATEST_NUMBER_OF_STORIES_TO_FETCH:
                break
        return interesting_news

    def _fetch_story(self, story_id):
        response = requests.get(self.URL + "v0/item/%s.json" % str(story_id))
        if response.status_code == 200:
            story_details = response.json()
            published_at = datetime.fromtimestamp(story_details.get("time"))
            return News(story_details.get("title"), published_at, story_details.get("text"), story_details.get("url"))
        response.raise_for_status()
