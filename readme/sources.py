from abc import ABCMeta, abstractmethod, abstractclassmethod


class Source:
    __metaclass__ = ABCMeta

    @abstractclassmethod
    def name(self):
        pass

    @classmethod
    def get_all_sources(cls):
        return [kls.name() for kls in cls.__subclasses__() if kls.name() is not None]

    @classmethod
    def get_source(cls, source_name: str):
        try:
            return next(kls for kls in cls.__subclasses__() if kls.name() == source_name)
        except StopIteration:
            return None

    @abstractmethod
    def fetch(self):
        raise NotImplementedError()


class HackerNews(Source):
    """
    Source: hacker-news (https://news.ycombinator.com/)
    """
    @classmethod
    def name(cls):
        return "hacker-news"

    def fetch(self):
        pass
