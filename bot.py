import discord
from discord.ext import commands
import asyncio

TOKEN = 'NTUyODU4OTY0NTA1Nzg4NDM2.D2FrVg.tfvKUUmpX2NXnptPucDBlFzMlwo'

client = commands.Bot(command_prefix = '!')

@asyncio.coroutine
@client.event
async def on_ready():
    print(client.user.name + ' is ready to chooch.')

client.run(TOKEN)

