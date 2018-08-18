import click


class Readme(click.Group):
    """
    collect news from your favorite channels
    """

    NAME = "enlightenme"
    help = "collect news from your favorite channels"

    def list_commands(self, ctx: click.Context):
        return ['source']

    def get_command(self, ctx: click.Context, cmd_name: str):
        try:
            mod = __import__('enlightenme.commands.' + cmd_name + '_command',
                             fromlist=[cmd_name])
            return getattr(mod, cmd_name)
        except (ImportError, AttributeError):
            ctx.fail('No such sub-command supported for enlightenme: %s' %
                     cmd_name)


@click.group(cls=Readme, help=Readme.help)
@click.pass_context
def cli(ctx: click.Context):
    pass
