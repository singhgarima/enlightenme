from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List

import click

from readme.utils import camel_case


class News:
    def __init__(self, title, published_at: datetime, body: str = None, url: str = None, tags: List = []):
        self.title = title
        self.published_at = published_at
        self.body = body
        self.url = url
        self.tags = tags


class NewsFormatter:
    __metaclass__ = ABCMeta

    DEFAULT_FORMAT = "console"
    FORMAT_OPTIONS = ['console', 'html']

    def __init__(self, news_list: List[News]):
        self._news_list = news_list
        self._output = None

    @property
    def news_list(self):
        return self._news_list

    @news_list.setter
    def news_list(self, value: List[News]):
        self._news_list = value

    @abstractmethod
    def format(self):
        raise NotImplementedError

    @classmethod
    def formatter_for_format(cls, format_type: str):
        return eval("%sNewsFormatter" % camel_case(format_type))


class ConsoleNewsFormatter(NewsFormatter):
    def format(self):
        self._output = "\n"
        for index, news in enumerate(self.news_list):
            self._output += "\t%d. Title: %s\n" % (index + 1, news.title)
            self._output += "\t   Published At: %s\n" % news.published_at.strftime('%Y-%m-%dT%H:%M:%SZ')

            if news.url: self._output += "\t   URL: %s\n" % news.url
            if news.tags: self._output += "\t   Tags: %s\n" % ", ".join(news.tags)

    def send(self):
        click.echo(self._output)


class HtmlNewsFormatter(NewsFormatter):
    def format(self):
        pass
