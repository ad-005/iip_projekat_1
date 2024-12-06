import logging

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Internal(commands.Cog, name="internal"):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(
        name='reload',
        with_app_command=True,
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
            embed = discord.Embed(
                description='Cog uspješno reloadovan.', colour=discord.Colour.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                description=str(e), colour=discord.Colour.red()
            )
            await ctx.send(embed=embed, delete_after=5)

    @commands.hybrid_command(
        name='load',
        with_app_command=True,
        description='Učitava odabrani Cog.'
    )
    @app_commands.describe(cog='Ime coga koji treba da se učita.')
    @commands.is_owner()
    async def load(self, ctx: Context, cog: str) -> None:
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
            await ctx.send(embed=embed, delete_after=5)

        embed = discord.Embed(description='Cog uspješno učitan.', colour=discord.Colour.green())
        await ctx.send(embed=embed, delete_after=5)

    @commands.hybrid_command(
        name='unload',
        description='Unloaduje odabrani Cog.'
    )
    @app_commands.describe(cog='Cog koji treba da se unloaduje.')
    @commands.is_owner()
    async def unload(self, ctx: Context, cog: str) -> None:
        """
        Unloaduje odabrani Cog.
        :param cog: Cog koji treba unloadovati.
        :return: None
        """
        try:
            await self.client.unload_extension(f'cogs.{cog}')
        except Exception as e:
            embed = discord.Embed(title='Nije moguće unloadovati Cog.',
                                  description=str(e),
                                  colour=discord.Colour.red()
                                  )
            await ctx.send(embed=embed, delete_after=5)

        embed = discord.Embed(description='Cog uspješno unloadovan.', colour=discord.Colour.green())
        await ctx.send(embed=embed, delete_after=5)


async def setup(client) -> None:
    await client.add_cog(Internal(client))
