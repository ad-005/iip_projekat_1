import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f"Bot: {self.user} je povezan.")