import csv
import io
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from typing import List

from enlightenme.news.news import News
from enlightenme.utils import camel_case

DATE_TIME_STR_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class NewsFormatter:
    __metaclass__ = ABCMeta

    DEFAULT_FORMAT = "list"
    FORMAT_OPTIONS = ['list', 'csv']

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
            published_at = news.published_at.strftime(DATE_TIME_STR_FORMAT)
            output += "\t    Published At: %s\n" % published_at

            if news.url:
                output += "\t    URL: %s\n" % news.url
            if news.tags:
                output += "\t    Tags: %s\n" % ", ".join(news.tags)
        return output


class CsvNewsFormatter(NewsFormatter):
    def format(self) -> str:
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        for index, news in enumerate(self.news_list):
            if index == 0:
                writer.writerow(news.__dict__.keys())
            news_dict = deepcopy(news.__dict__)
            news_dict['published_at'] = news_dict['published_at']. \
                strftime(DATE_TIME_STR_FORMAT)
            writer.writerow(news_dict.values())
        return output.getvalue()
