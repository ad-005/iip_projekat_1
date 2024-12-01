import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Internal(commands.Cog, name="internal"):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(
        name='reload',
        description='Ponovo učitava Cog.'
    )
    @app_commands.describe(cog='Ime coga koji treba da se reloaduje.')
    @commands.is_owner()
    async def reload(self, ctx: Context, cog: str) -> None:
        """
        Ponovo ucitava odabrani cog.
        :param cog: Cog koji treba da se reloaduje.
        :return:
        """
        try:
            await self.client.reload_extension(f'cogs.{cog}')
        except Exception as e:
            embed = discord.Embed(
                description=str(e), colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)

        embed = discord.Embed(
            description='Cog uspješno reloadovan.', colour=discord.Colour.green()
        )
        await ctx.send(embed=embed)

        @commands.hybrid_command(
            name='load', description='Učitava odabrani Cog.'
        )
        @app_commands.describe(cog='Ime coga koji treba da se učita.')
        @commands.is_owner()
        async def load(ctx: Context, cog: str) -> None:
            """
            Učitava odabrani cog.
            :param cog: Cog koji treba da se učita
            :return: None
            """
            try:
                await self.client.load_extension(f'cogs.{cog}')
            except Exception as e:
                embed = discord.Embed(
                    title='Nije moguće učitati Cog.',
                    description=str(e),
                    colour=discord.Colour.red()
                )
                await ctx.send(embed=embed)

            embed = discord.Embed(description='Cog uspješno učitan.', colour=discord.Colour.green())
            await ctx.send(embed=embed)

async def setup(client) -> None:
    await client.add_cog(Internal(client))
