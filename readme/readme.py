import click


class Readme(click.Group):
    """
    collect news from your favorite channels
    """

    NAME = "readme"
    help = "collect news from your favorite channels"

    def list_commands(self, ctx):
        return ['source']

    def get_command(self, ctx, cmd_name):
        try:
            mod = __import__('readme.commands', fromlist=[cmd_name])
            return getattr(mod, cmd_name)
        except AttributeError:
            ctx.fail('No such sub-command supported for readme: %s' % cmd_name)


@click.group(cls=Readme, help=Readme.help)
@click.pass_context
def cli(ctx):
    pass
