import datetime
from random import randrange
import random
import string

from PIL import Image
from io import BytesIO
from captcha.image import ImageCaptcha
from captcha.audio import AudioCaptcha

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class ImageVerification:
    def __init__(self) -> None:
        super().__init__()
        self.captcha_text = ''
        self.img_message = None

    async def generate_captcha(self, ctx: Context) -> None:
        """
        Generiše i šalje captcha sliku u kanal u kojem je pokrenuta komanda 'captcha'.
        Nema parametre 'osim' context-a, sama generiše tekst za captch-u.
        :return: None
        """
        embed = discord.Embed(
            title='Captcha verifikacija',
            description='Odgovorite tačnim sadržajem iz slike.',
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.now()
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
            embed.set_image(url='attachment://captcha.png')
            self.img_message = await ctx.reply(
                embed=embed,
                file=discord.File(fp=slika_bajt, filename='captcha.png')
            )


class AudioVerification:
    def __init__(self) -> None:
        super().__init__()
        self.audio_value = ''
        self.audio_message = None

    async def generate_audio_captcha(self, ctx: Context) -> None:
        """
        Generiše i šalje .wav audio CAPTCH-u.
        :return: None
        """
        allowed_chars = string.digits
        self.audio_value = ''.join(random.choice(allowed_chars) for _ in range(randrange(4, 8)))

        audio_captcha = AudioCaptcha()
        audio_data = audio_captcha.generate(self.audio_value)

        embed = discord.Embed(
            title='Captcha verifikacija',
            description='Odgovorite tačnim sadržajem iz audio snimka.',
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.now()
        )

        self.audio_message = await ctx.reply(embed=embed, file=discord.File(BytesIO(audio_data), filename='audio_captcha.wav'))


# UI elementi za captcha komandu (biranje audio ili image captche)
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

    async def on_member_join(self, member) -> None:
        """
        Štampa poruku dobrodošlice u određenom kanalu kada se nova osoba pridruži.
        :param member: Osoba koja se pridružila serveru `discord.Member`.
        :return: None
        """
        embed = discord.Embed(
            title='Dobrodošli!',
            description=f'Dobrodošli na server {member.mention}!'
                        f'\nDa biste započeli verifikaciju, iskoristite komandu `captcha`.',
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.now()
        )
        await self.welcome_channel.send(embed=embed)

    @commands.hybrid_command(
        name='captcha',
        with_app_command=True,
        description='Verifikuje korisnika i omogućava mu da koristi bota.'
    )
    async def captcha(self, ctx: Context) -> None:
        """
        Komanda pomoću koje se novi korisnik verifikuje. Bira između slike i audio captche,
        tekst se mora podudarati.
        :return: None
        """
        verified_role = discord.utils.get(ctx.guild.roles, name='Verifikovan')
        if verified_role in ctx.author.roles:
            embed = discord.Embed(
                title='Već ste verifikovani',
                description='Ne možete se ponovo verifikovati.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        embed_success = discord.Embed(
            title='Verifikacija uspješna',
            description='Sada možete koristiti sve komande.',
            color=discord.Color.teal(),
            timestamp=datetime.datetime.now()
        )

        embed_failed = discord.Embed(
            title='Verifikacija neuspješna',
            description='Odgovor se ne podudara.'
                        '\nPokušajte ponovo upotrebom komande `captcha`.',
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )

        verifikacija_audio = AudioVerification()
        verifikacija_slika = ImageVerification()
        buttons = CaptchaChoice()
        embed = discord.Embed(
            title='Odaberite način verifikacije',
            description='Audio za audio verifikaciju, Slika za klasičnu captch-u.',
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.now()
        )
        embed.set_image(url='attachment://captcha.jpg')
        await ctx.reply(embed=embed, view=buttons)
        await buttons.wait()

        if buttons.value == 'image':
            await verifikacija_slika.generate_captcha(ctx)
            user_response = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)

            if user_response.content == verifikacija_slika.captcha_text:
                await ctx.reply(embed=embed_success)
                await ctx.author.add_roles(
                    verified_role,
                    reason='Korisnik prošao captcha verifikaciju.'
                )
            else:
                await ctx.reply(embed=embed_failed)

            await verifikacija_slika.img_message.delete()

        elif buttons.value == 'audio':
            await verifikacija_audio.generate_audio_captcha(ctx)
            user_response = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)

            if user_response.content == verifikacija_audio.audio_value:
                await ctx.reply(embed=embed_success)
                await ctx.author.add_roles(
                    verified_role,
                    reason='Korisnik prošao captcha verifikaciju.'
                )
            else:
                await ctx.reply(embed=embed_failed)

            await verifikacija_audio.audio_message.delete()

        else:
            pass


async def setup(client) -> None:
    await client.add_cog(Captcha(client))
