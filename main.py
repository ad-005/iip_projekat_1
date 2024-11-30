import os
from dotenv import load_dotenv
import discord

load_dotenv()

class Client(discord.Client):
    async def on_ready(self):
        print(f"Bot: {self.user} je povezan.")


intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))
