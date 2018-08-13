from typing import List

import click

import readme.news_formatters
from readme import news_output
from readme.news_formatters import NewsFormatter
from readme.readme import cli
from readme.sources import Source


@cli.command(
    help="get latest news from different sources"
)
@click.argument('source_name')
@click.option('--format', default=NewsFormatter.DEFAULT_FORMAT,
              type=click.Choice(NewsFormatter.FORMAT_OPTIONS),
              help="Displays news in a format")
@click.option('--output', required=False, help="Write to FILE instead of stdout")
@click.pass_context
def source(ctx: click.Context, source_name: str, format: str, output: str = None):
    if source_name == "list":
        list_sources()
    else:
        fetcher = Fetcher(source_name, format)
        if not fetcher.valid():
            ctx.fail("Invalid source supplied. See --help")

        click.echo("Fetching news from source: %s" % source_name)
        content = fetcher.fetch_and_format()
        news_output.NewsOutput(content).write_to(file_name=output)


def list_sources():
    click.echo("Currently the plugin supports the following sources")
    [click.echo("* %s" % name) for name in Source.get_all_sources()]


class Fetcher:
    def __init__(self, source_name: str, format_type: str = NewsFormatter.DEFAULT_FORMAT):
        self._source_name = source_name
        self._format_type = format_type
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
        self._news_list = source_object.fetch()

    def _format(self) -> str:
        klass = readme.news_formatters.NewsFormatter.formatter_for_format(self._format_type)
        formatter = klass(self._news_list)
        return formatter.format()
