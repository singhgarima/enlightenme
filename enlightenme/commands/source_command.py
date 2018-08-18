import click

from enlightenme.commands.helpers import fetcher
from enlightenme.enlightenme import cli
from enlightenme.news import news_output
from enlightenme.news.news_formatters import NewsFormatter
from enlightenme.sources import Source


@cli.command(
    help="get latest news from different sources"
)
@click.argument('source_name')
@click.option('--format', '-f', default=NewsFormatter.DEFAULT_FORMAT,
              type=click.Choice(NewsFormatter.FORMAT_OPTIONS),
              help="Displays news in a format")
@click.option('--output', '-o', required=False,
              help="Write to FILE instead of stdout")
@click.option('--keywords', '-k', required=False,
              help="Topics or Keywords that interest you (e.g. python,golang)")
@click.pass_context
def source(ctx: click.Context, source_name: str, format: str,
           output: str = None, keywords: str = None):
    if source_name == "list":
        list_sources()
    else:
        keywords = keywords.split(",") if keywords else None
        news_fetchers = fetcher.Fetcher(source_name,
                                        format_type=format,
                                        keywords=keywords)
        if not news_fetchers.valid():
            ctx.fail("Invalid source supplied. See --help")

        click.echo("Fetching news from source: %s" % source_name)
        content = news_fetchers.fetch_and_format()
        news_output.NewsOutput(content).write_to(file_name=output)


def list_sources():
    click.echo("Currently the plugin supports the following sources")
    [click.echo("* %s" % name) for name in Source.get_all_sources()]
