from typing import List

import requests

from readme.news import News
from readme.sources import Source


class HackerNews(Source):
    """
    Source: hacker-news (https://news.ycombinator.com/)
    """
    URL = "https://hacker-news.firebaseio.com/"

    @classmethod
    def name(cls):
        return "hacker-news"

    def fetch(self) -> List[News]:
        stories = self._fetch_latest_stories()
        return [self._fetch_story(story_id) for story_id in stories[0:20]]

    def _fetch_latest_stories(self):
        response = requests.get(self.URL + "v0/newstories.json")
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()

    def _fetch_story(self, story_id):
        response = requests.get(self.URL + "v0/item/%s.json" % str(story_id))
        if response.status_code == 200:
            story_details = response.json()
            return News(story_details.get("title"), story_details.get("text"), story_details.get("url"))
        response.raise_for_status()