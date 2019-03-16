import discord
from discord.ext import commands
import asyncio

# Change with your TOKEN found in your Discord Application Page
TOKEN = 'NTUyODU4OTY0NTA1Nzg4NDM2.D2FrVg.tfvKUUmpX2NXnptPucDBlFzMlwo'

# Any implemented command will need to be typed in chat
# with the prefix stated here. (!play, !stop) 
client = commands.Bot(command_prefix = '!')

@asyncio.coroutine

@client.event
# Prints to console that it's ready, has full functionality.
# Function will run reagardless of what the bot is doing at the time.
async def on_ready():
    await client.change_presence(game=discord.Game(name='!commands'))
    print(client.user.name + ' is ready to chooch.')

@client.event
# Assigns a role to a new user on the server;
# Choose which role you want a new user to have    name='YOUR ROLE'
async def on_member_join(member):
    role =  discord.utils.get(member.server.roles, name='Veggie Cutter')
    await client.add_roles(member, role)

@client.command()
async def commands():
    await client.say('!commands - Displays this list\n'
                   + '!ping - Pong!\n'
                   + '!clear - Clears the chat\n'
                   + '!play - Plays a clip from Youtube')

@client.command()
async def ping():
    await client.say('Pong!')

@client.command(pass_context=True)
async def clear(ctx, amount = 100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages deleted')




@client.command()
async def play():
    await client.say('!play NOT YET IMPLEMENTED')


client.run(TOKEN)

