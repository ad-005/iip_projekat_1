import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context


class Client(commands.Bot):
    async def on_ready(self) -> None:
        """
        Stampa da je bot upaljen kada se uspjesno poveze sa Discordom.
        :return: None
        """
        print(f"Bot: {self.user} je povezan.")
        await self.load_cogs()

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
                    print(f"Ucitan Cog: {extension}")

                except Exception as e:
                    print(f"Cog {extension} nije ucitan.\nError: {e}")


client = Client(command_prefix="!", intents=discord.Intents.all())

@client.hybrid_command(name='sync', description='Sinhronizuje slash commande.')
async def sync(ctx: Context) -> None:
    await client.tree.sync(guild=ctx.guild)
    embed = discord.Embed(
        description='Sinhronizovane slash komande za ovaj server.'
    )

    await ctx.send(embed=embed)


load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))
