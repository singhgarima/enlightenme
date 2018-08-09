import click

from readme.readme import cli


@cli.command(
    short_help="get latest news from different sources"
)
@click.argument('source_name', required=True)
@click.pass_context
def source(ctx, source_name):
    click.echo("Fetching news from source: %s" % source_name)

# "get latest news from hacker-news (https://news.ycombinator.com/)"