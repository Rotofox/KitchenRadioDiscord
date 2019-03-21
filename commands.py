import discord
from discord.ext import commands

class Commands:
    def __init__(self, client):
        self.client = client

    async def on_message_delete(self, message):
        await self.client.send_message(message.channel, 'Message Deleted!')

    @commands.command
    async def ping(self):
        await self.client.say('Pong!')

    

def setup(client):
    client.add_cog(Commands(client))