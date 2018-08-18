from abc import ABCMeta, abstractmethod
from typing import List

from readme.news.news import News
from readme.utils import camel_case


class NewsFormatter:
    __metaclass__ = ABCMeta

    DEFAULT_FORMAT = "list"
    FORMAT_OPTIONS = ['list', 'html']

    def __init__(self, news_list: List[News]):
        self._news_list = news_list

    @property
    def news_list(self):
        return self._news_list

    @news_list.setter
    def news_list(self, value: List[News]):
        self._news_list = value

    @abstractmethod
    def format(self) -> str:
        raise NotImplementedError

    @classmethod
    def formatter_for_format(cls, format_type: str):
        return eval("%sNewsFormatter" % camel_case(format_type))


class ListNewsFormatter(NewsFormatter):
    def format(self) -> str:
        output = "\n"
        for index, news in enumerate(self.news_list):
            output += "\t%d. Title: %s\n" % (index + 1, news.title)
            output += "\t    Published At: %s\n" % news.published_at.strftime('%Y-%m-%dT%H:%M:%SZ')

            if news.url: output += "\t    URL: %s\n" % news.url
            if news.tags: output += "\t    Tags: %s\n" % ", ".join(news.tags)
        return output


class HtmlNewsFormatter(NewsFormatter):
    def format(self) -> str:
        pass
