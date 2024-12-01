import datetime
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Captcha(commands.Cog, name='captcha'):
    def __init__(self, client):
        self.client = client
        self.welcome_channel = self.client.get_channel(self.client.config["welcome_kanal"])

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        """
        Štampa poruku dobrodošlice u određenom kanalu kada se nova osoba pridruži.
        :param member: Osoba koja se pridružila serveru `discord.Member`.
        :return: None
        """
        embed = discord.Embed(
            title='Dobrodošli!',
            description=f'Dobrodošli na server {member.mention}!'
                        f'\nDa biste započeli verifikaciju, iskoristite komandu `verifikuj`.',
            color=discord.Color.dark_magenta(),
            timestamp=datetime.datetime.now()
        )
        await self.welcome_channel.send(embed=embed)

    @commands.hybrid_command(
        name='captcha',
        description='Verifikuje korisnika i omogućava mu da koristi bota.'
    )
    @app_commands.describe(captcha_text='Tekst sa captcha slike.')
    @commands.has_role("Verifikovan")
    async def captcha(self, ctx: Context, captcha_text: str=None) -> None:
        """
        :param captcha_text: Tekst sa slike koji se mora podudarati sa slikom.
        :return: None
        """
        await ctx.send(captcha_text, tts=True)

async def setup(client) -> None:
    await client.add_cog(Captcha(client))
