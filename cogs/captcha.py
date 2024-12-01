from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Captcha(commands.Cog, name='captcha'):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(
        name='captcha',
        description='Verifikuje korisnika i omogućava mu da koristi bota.'
    )
    @app_commands.describe(captcha_text='Tekst sa captcha slike.')
    async def captcha(self, ctx: Context, captcha_text: str) -> None:
        """
        :param captcha_text: Tekst sa slike koji se mora podudarati sa slikom.
        :return: None
        """
