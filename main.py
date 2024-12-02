import os
from dotenv import load_dotenv
import json

import discord
from discord.ext import commands
from discord.ext.commands import Context

with open("config.json") as file:
    config = json.load(file)

class Client(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all()
        )
        self.config = config

    async def on_ready(self) -> None:
        """
        Stampa da je bot upaljen kada se uspjesno poveze sa Discordom.
        :return: None
        """
        print(f"Bot: {self.user} je povezan.")
        await self.load_cogs()
        await self.set_status()

    async def load_cogs(self) -> None:
        """
        Ucitava sve komande, odnosno cogove. Stampa da li je uspjesno ucitan ili ne
        :return: None
        """
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                extension = cog[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    print(f"Učitan Cog: {extension}")

                except Exception as e:
                    print(f"Cog {extension} nije učitan.\nRazlog: {e}")

    async def set_status(self) -> None:
        """
        Postavlja status bota svaki put kada se uključi.
        :return: None
        """
        await self.change_presence(activity=discord.Game('😎'))


client = Client()

@client.hybrid_command(name='sync', description='Sinhronizuje slash commande.')
@commands.is_owner()
async def sync(ctx: Context) -> None:
    """
    Sinhronizuje sve slash komande samo za server u kojem je upotrijebljena ova komanda.
    :return: None
    """
    try:
        await client.tree.sync(guild=ctx.guild)
    except Exception as e:
        print(e)

    embed = discord.Embed(
        description='Sinhronizovane slash komande za ovaj server.',
        color=discord.Colour.green()
    )
    await ctx.send(embed=embed)


load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))
