import discord, asyncio, ytsearch
from discord.ext import commands

# Change with your TOKEN found in your Discord Application Page
TOKEN = 'NTUyODU4OTY0NTA1Nzg4NDM2.D2FrVg.tfvKUUmpX2NXnptPucDBlFzMlwo'

"""
Any implemented command will need to be typed in chat
with the prefix stated here. (!play, !stop) 
"""
client = commands.Bot(command_prefix = '!')
client.remove_command('help') #removes the default help command; requires implemenentation of custom help command
players = {}
youtube = ytsearch.Search

@asyncio.coroutine
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='!help'))
    print(client.user.name + ' is ready to chooch.')

"""
Assigns a role to a new user on the server
Choose which role you want a new user to have    name='YOUR ROLE'
"""
@client.event
async def on_member_join(member):
    role =  discord.utils.get(member.server.roles, name='Veggie Cutter')
    await client.add_roles(member, role)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

"""
Bot joins the voice channel the user issuing the command is in or joins the
first voice channel on the server if the user isn't in any voice channel.
A player is created and plays the audio the user searched for.
    @args * - supports multiple strings divided my spaces
    @args query - string
    '!play mozart symphony 40 g minor'
"""
@client.command(pass_context=True)
async def play(ctx, *, query):
    options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10" # this fucker took me a while 'cause links expire and music stops :(
    query = youtube.findvid(query)
    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(query, before_options = options)
    players[server.id] = player
    player.start()

# Sends a private message containing the bot commands list to the user who imputted the command
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        color = discord.Color.gold()
    )
    embed.set_author(name = 'Commands list:')
    embed.add_field(name = '!help', value="PM's you the commands list", inline=False)
    embed.add_field(name = '!clear', value='Clears the chat', inline=False)
    embed.add_field(name = '!play', value='Plays a clip from Youtube', inline=False)
    await client.send_message(author, embed=embed)

# Deletes the specified number of messages in chat; '!clear 14' or '!clear' (default = 100)
@client.command(pass_context=True)
async def clear(ctx, amount = 100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages deleted')

client.run(TOKEN)

