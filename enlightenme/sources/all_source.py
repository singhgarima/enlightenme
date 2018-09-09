from typing import List

import click

from enlightenme.news.news import News
from enlightenme.sources import Source


class AllSource(Source):
    HELP = "Pulls news from all the available sources"

    def __init__(self):
        self.sources = []

    def fetch(self, keywords: List = None) -> List[News]:
        pass

    @classmethod
    def name(cls):
        return "all"

    @classmethod
    def params(cls) -> List[click.Parameter]:
        return sum([source.params() for source in Source.get_all_source_sub_classes() if source is not AllSource], [])
