import datetime
import json
import random
import unittest

import requests_mock
from requests import HTTPError

from enlightenme.news.news import News
from enlightenme.sources.hacker_news import HackerNews, HackerNewsStory
from tests.fixtures import hacker_news_story


class TestHackerNews(unittest.TestCase):
    def setUp(self):
        self._source = HackerNews()

    def test_initialize(self):
        self.assertEqual([], self._source._story_ids)

    def test_fetch_should_fetch_latest_20_stories(self):
        stories = list(range(20))
        with requests_mock.mock() as m:
            m.get("https://hacker-news.firebaseio.com/v0/newstories.json", text=json.dumps(stories))
            [m.get("https://hacker-news.firebaseio.com/v0/item/" + str(story_id) + ".json",
                   text=json.dumps(hacker_news_story(story_id=story_id))) for story_id in stories[0:10]]

            result = self._source.fetch()

        self.assertEqual(10, result.__len__())

    def test_fetch_should_fetch_latest_containing_the_keywords(self):
        keywords = ["python", "golang", "chaos"]
        stories = list(range(20))
        with requests_mock.mock() as m:
            m.get("https://hacker-news.firebaseio.com/v0/newstories.json", text=json.dumps(stories))
            self._mock_10_stories_to_have_keywords(m, stories, keywords=keywords)

            result = self._source.fetch(keywords=keywords)

        self.assertEqual(10, result.__len__())

    def test_fetch_when_hacker_news_api_is_available_but_result_returned_in_response_is_none(self):
        stories = [121232]
        with requests_mock.mock() as m:
            m.get("https://hacker-news.firebaseio.com/v0/newstories.json", text=json.dumps(stories))
            m.get("https://hacker-news.firebaseio.com/v0/item/" + str(stories[0]) + ".json",
                  text=json.dumps(None))

            result = self._source.fetch()

        self.assertEqual(0, result.__len__())
        self.assertEqual([], result)

    def test_fetch_when_hacker_news_api_is_unavailable(self):
        with requests_mock.mock() as m:
            m.get(HackerNews.URL + "v0/newstories.json", text='Not Found', status_code=404)

            with self.assertRaises(HTTPError) as error:
                self._source.fetch()

        self.assertEqual('404', str(error.exception.response.status_code))

    def test_fetch_when_hacker_news_item_api_is_unavailable(self):
        stories = [17720786]
        with requests_mock.mock() as m:
            m.get("https://hacker-news.firebaseio.com/v0/newstories.json", text=json.dumps(stories))
            m.get(self._get_item_url_for_story(stories[0]), text='Not Found', status_code=404)

            with self.assertRaises(HTTPError) as error:
                self._source.fetch()

        self.assertEqual('404', str(error.exception.response.status_code))

    @staticmethod
    def _mock_10_stories_to_have_keywords(m, stories, keywords=None):
        keywords = [] if keywords is None else keywords
        for index, story_id in enumerate(stories):
            text = "Test Test"
            if index % 2 == 0:
                text = text + " " + keywords[random.randint(0, len(keywords) - 1)]
            item_url = TestHackerNews._get_item_url_for_story(story_id)
            m.get(item_url, text=json.dumps(hacker_news_story(story_id=story_id, text=text)))

    @staticmethod
    def _get_item_url_for_story(story_id):
        return "https://hacker-news.firebaseio.com/v0/item/" + str(story_id) + ".json"


class HackerNewsStoryTest(unittest.TestCase):
    def test_initialize(self):
        story = HackerNewsStory(123)

        self.assertEqual(123, story._story_id)
        self.assertEqual(None, story._story_details)

    def test_initialize_with_story_details_specified(self):
        story_id = 123
        details = {'title': 'test'}

        story = HackerNewsStory(story_id, details)

        self.assertEqual(story_id, story._story_id)
        self.assertEqual(details, story._story_details)

    def test_fetch(self):
        story_id = 12
        title = 'Show HN: NES Party – Online Multiplayer NES Emulator Using WebRTC'
        url = 'https://nes.party'
        with requests_mock.mock() as m:
            m.get("https://hacker-news.firebaseio.com/v0/item/" + str(story_id) + ".json",
                  text=json.dumps(hacker_news_story(story_id=story_id, author='dsr12', title=title, url=url)))

            story = HackerNewsStory(story_id)
            result = story.fetch()

        self.assertIsInstance(result, News)
        self.assertEqual(title, result.title)
        self.assertEqual([], result.tags)
        self.assertEqual(datetime.datetime(2018, 8, 9, 8, 20, 11), result.published_at)
        self.assertEqual(url, result.url)
        self.assertEqual(None, result.body)
