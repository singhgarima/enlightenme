import click

from readme.readme import cli
from readme.sources import Source


@cli.command(
    help="get latest news from different sources"
)
@click.argument('source_name')
@click.pass_context
def source(ctx: click.Context, source_name: str):
    if source_name != "list":
        click.echo("Fetching news from source: %s" % source_name)
        news_list = fetch_updates_from_source(source_name)
        print_news(news_list)
    else:
        list_sources()


def list_sources():
    click.echo("Currently the plugin supports the following sources")
    [click.echo("* %s" % name) for name in Source.get_all_sources()]


def fetch_updates_from_source(source_name: str):
    source_class = Source.get_source(source_name)
    source_object = source_class()
    return source_object.fetch()


def print_news(news_list):
    [click.echo("""
    %d. Title: %s
    """ % (index + 1, news.title)) for index, news in enumerate(news_list)]
