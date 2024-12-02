from discord.ext import commands
from discord.ext.commands import Context


class Ping(commands.Cog, name='ping'):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(
        name='ping',
        with_app_command=True,
        description="Pong...?"
    )
    async def ping(self, ctx: Context) -> None:
        """
        Odgovara sa 'Pong' i vraca latency bota.
        :return: None
        """
        await ctx.send(f'Pong! Za {round(self.client.latency * 1000)}ms.')


async def setup(client) -> None:
    await client.add_cog(Ping(client))
