from typing import List

import readme.news.news_formatters
from readme.news.news_formatters import NewsFormatter
from readme.sources import Source


class Fetcher:
    def __init__(self, source_name: str, format_type: str = NewsFormatter.DEFAULT_FORMAT, keywords: List = None):
        self._source_name = source_name
        self._format_type = format_type
        self._keywords = keywords
        self._news_list = []

    def valid(self):
        return self._source_name in Source.get_all_sources()

    def fetch_and_format(self) -> str:
        self._fetch()
        return self._format()

    def _fetch(self):
        source_class = Source.get_source(self._source_name)
        __import__(source_class.__module__, fromlist=[source_class.__name__])
        source_object = source_class()
        self._news_list = source_object.fetch(keywords=self._keywords)

    def _format(self) -> str:
        klass = readme.news.news_formatters.NewsFormatter.formatter_for_format(self._format_type)
        formatter = klass(self._news_list)
        return formatter.format()