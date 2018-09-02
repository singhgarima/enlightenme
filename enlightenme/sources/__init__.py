from abc import ABCMeta, abstractclassmethod, abstractmethod
from typing import List, Optional

import click

from enlightenme.news.news import News
from enlightenme.utils import import_submodules


class Source:
    __metaclass__ = ABCMeta
    HELP = None

    @abstractclassmethod
    def name(self):
        pass

    @classmethod
    def get_all_sources(cls) -> List[str]:
        return [kls.name() for kls in cls._sub_classes()
                if kls.name() is not None]

    @classmethod
    def get_source(cls, source_name: str) -> Optional[type]:
        try:
            return next(kls for kls in cls._sub_classes()
                        if kls.name() == source_name)
        except StopIteration:
            return None

    @classmethod
    def params(cls) -> List[click.Parameter]:
        return []

    @abstractmethod
    def fetch(self, keywords: List = None) -> List[News]:
        raise NotImplementedError()

    @classmethod
    def _sub_classes(cls) -> List:
        import_submodules('enlightenme.sources')
        return cls.__subclasses__()
