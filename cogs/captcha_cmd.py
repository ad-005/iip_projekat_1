import datetime
from random import randrange
import random
import string

from PIL import Image
from io import BytesIO
from captcha.image import ImageCaptcha

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class ImageVerification:
    def __init__(self) -> None:
        super().__init__()
        self.captcha_text = ''

    async def generate_captcha(self, ctx: Context):
        embed = discord.Embed(
            title='Captcha verifikacija',
            description='Odgovorite tačnim sadržajem slike.',
            color=discord.Color.blurple()
        )

        captcha_source = string.ascii_uppercase + string.digits
        captcha_text = ''.join(random.choice(captcha_source) for _ in range(randrange(5, 9)))
        self.captcha_text = captcha_text

        captcha_obj = ImageCaptcha(
            width=400,
            height=220,
            font_sizes=(20, 25, 45, 50, 70)
        )

        captcha_image: BytesIO = captcha_obj.generate(captcha_text)
        slika: Image = Image.open(captcha_image)
        with BytesIO() as slika_bajt:
            slika.save(slika_bajt, 'PNG')
            slika_bajt.seek(0)
            await ctx.reply(
                embed=embed,
                file=discord.File(fp=slika_bajt, filename='captcha.png')
            )


class CaptchaChoice(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None

    @discord.ui.button(label='Audio', style=discord.ButtonStyle.primary)
    async def audio_captcha(
            self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
            self.value = 'audio'
            self.stop()

    @discord.ui.button(label='Slika', style=discord.ButtonStyle.primary)
    async def image_captcha(
            self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        embed = discord.Embed(title='Image')

        await interaction.message.delete()

        self.value = 'image'
        self.stop()


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
    async def captcha(self, ctx: Context, captcha_text: str=None) -> None:
        """
        :param captcha_text: Tekst sa slike koji se mora podudarati sa slikom.
        :return: None
        """
        verifikacija_slika = ImageVerification()
        buttons = CaptchaChoice()
        embed = discord.Embed(
            title='Odaberite način verifikacije',
            description='Audio za audio verifikaciju, Slika za klasičnu captch-u.',
            color=discord.Color.blurple()
        )
        message = await ctx.reply(embed=embed, view=buttons)
        await buttons.wait()

        if buttons.value == 'image':
            await verifikacija_slika.generate_captcha(ctx)

        elif buttons.value == 'audio':
            await ctx.send("Audio")

        else:
            pass



async def setup(client) -> None:
    await client.add_cog(Captcha(client))
