import json
import unittest

import requests_mock
from requests import HTTPError

from tests.fixtures import hacker_news_story
from readme.sources.hacker_news import HackerNews


class TestHackerNews(unittest.TestCase):
    def test_fetch(self):
        stories = [17720786, 17716542, 17714722]
        with requests_mock.mock() as m:
            m.get("https://hacker-news.firebaseio.com/v0/newstories.json", text=json.dumps(stories))
            [m.get("https://hacker-news.firebaseio.com/v0/item/" + str(story_id) + ".json",
                   text=json.dumps(hacker_news_story(story_id=story_id))) for story_id in stories]

            result = HackerNews().fetch()

        self.assertEqual(3, result.__len__())

    def test_fetch_when_hacker_new_api_is_unavailable(self):
        with requests_mock.mock() as m:
            m.get(HackerNews.URL + "v0/newstories.json", text='Not Found', status_code=404)

            with self.assertRaises(HTTPError) as error:
                HackerNews().fetch()

        self.assertEqual('404', str(error.exception.response.status_code))

    def test_fetch_when_hacker_new_item_api_is_unavailable(self):
        stories = [17720786]
        with requests_mock.mock() as m:
            m.get("https://hacker-news.firebaseio.com/v0/newstories.json", text=json.dumps(stories))
            m.get("https://hacker-news.firebaseio.com/v0/item/" + str(stories[0]) + ".json",
                  text='Not Found', status_code=404)

            with self.assertRaises(HTTPError) as error:
                HackerNews().fetch()

        self.assertEqual('404', str(error.exception.response.status_code))