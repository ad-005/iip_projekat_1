import os
from dotenv import load_dotenv
import json
import logging
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Context

with open("config.json") as file:
    config = json.load(file)

# Setup za logovanje i formatiranje loga (izgled)
logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)

discord_logging = logging.FileHandler(filename="activities.log", encoding="utf-8", mode="w")
discord_logging_formatter = logging.Formatter(
    "[{asctime}] [{levelname}] {name}: {message}",
    "%Y-%m-%d %H:%M:%S",
    style="{"
)

discord_logging.setFormatter(discord_logging_formatter)
logger.addHandler(discord_logging)


class Client(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all()
        )
        self.config = config
        self.logger = logger

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

    async def on_command_completion(self, ctx: Context) -> None:
        """
        Loguje svaku uspješno iskorišćenu komandu.
        :return: None
        """
        command_name = ctx.command.name
        self.logger.info(f"Komanda [{command_name}] je iskorišćena od strane {ctx.author}. (ID: {ctx.author.id})")

    async def on_command_error(self, ctx: Context, error: Exception) -> None:
        """
        Loguje neuspješno iskoričćene komande i error zbog kojeg nije radila.
        :param error: Error do kojeg je došlo.
        :return: None
        """
        error_embed = discord.Embed(
            title='Došlo je do greške',
            description='Došlo je do greške u izvršenju komande.\nMolim Vas pokušajte ponovo.',
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        command_name = ctx.command.name
        self.logger.error(f"Komanda [{command_name}] error: {error}")

        if isinstance(error, commands.MissingRole) and discord.utils.get(ctx.guild.roles, name='Verifikovan') not in ctx.author.roles:
            role_embed = discord.Embed(
                title='Niste verifikovani',
                description='Ne posjedujete role potreban za izvršenje ove komande.'
                            '\nMolim Vas verifikujte se komandom `captcha`.',
                color=discord.Color.red(),
                timestamp=datetime.datetime.now()
            )
            await ctx.send(embed=role_embed, delete_after=5.0)

        else:
            await ctx.send(embed=error_embed, delete_after=5.0)

client = Client()

@client.hybrid_command(name='sync', description='Sinhronizuje slash commande.')
@commands.is_owner()
async def sync(ctx: Context) -> None:
    """
    Sinhronizuje sve slash komande samo za server u kojem je upotrijebljena ova komanda.
    :return: None
    """
    try:
        await client.tree.sync(guild=discord.Object(id=ctx.guild.id))
    except Exception as e:
        print(e)

    embed = discord.Embed(
        description='Sinhronizovane slash komande za ovaj server.',
        color=discord.Colour.green()
    )
    await ctx.send(embed=embed)


load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))
