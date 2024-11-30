import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands

load_dotenv()

class Client(commands.Bot):
    async def on_ready(self):
        print(f"Bot: {self.user} je povezan.")

    async def on_message(self, message):
        if message.author == self.user:
            return


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

client.run(os.getenv('DISCORD_TOKEN'))
