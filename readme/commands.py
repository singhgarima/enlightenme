from typing import List

import click

from readme import news
from readme.readme import cli
from readme.sources import Source


@cli.command(
    help="get latest news from different sources"
)
@click.argument('source_name')
@click.pass_context
def source(ctx: click.Context, source_name: str):
    if source_name == "list":
        list_sources()
    else:
        if source_name not in Source.get_all_sources():
            ctx.fail("Invalid source supplied. See --help")
        click.echo("Fetching news from source: %s" % source_name)
        news_list = fetch_updates_from_source(source_name)
        format_news_list(news_list)


def list_sources():
    click.echo("Currently the plugin supports the following sources")
    [click.echo("* %s" % name) for name in Source.get_all_sources()]


def fetch_updates_from_source(source_name: str) -> List:
    source_class = Source.get_source(source_name)
    __import__(source_class.__module__, fromlist=[source_class.__name__])
    source_object = source_class()
    return source_object.fetch()


def format_news_list(news_list):
    formatter = news.ConsoleNewsFormatter(news_list)
    formatter.format()
    formatter.send()
