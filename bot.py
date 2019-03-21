import discord, asyncio, ytsearch
from discord.ext import commands
from discord import message

# Change with your TOKEN found in your Discord Application Page
TOKEN = 'NTUyODU4OTY0NTA1Nzg4NDM2.D2FrVg.tfvKUUmpX2NXnptPucDBlFzMlwo'

"""
Any implemented command will need to be typed in chat
with the prefix stated here. (!play, !stop) 
"""
client = commands.Bot(command_prefix = '!')
client.remove_command('help') #removes the default help command; requires implemenentation of custom help command
extensions = ['commands']
players = {}
queues = {}
youtube = ytsearch.Search

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

@asyncio.coroutine
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='!help'))
    print(client.user.name + ' is ready to chooch.')
# Loads an extension
@client.command()
async def load(extension):
    try:
        client.load_extension(extension)
        print('Loaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be loaded. [{}]'.format(extension, error))

# Unloads an extension
@client.command()
async def unload(extension):
    try:
        client.unload_extension(extension)
        print('Unloaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be unloaded. [{}]'.format(extension, error))

# Automatically loads extensions at runtime
if __name__ == '__main__':
    for extension in extensions: 
        try:
            client.load_extensions(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

"""
Assigns a role to a new user on the server
Choose which role you want a new user to have    name='YOUR ROLE'
"""
@client.event
async def on_member_join(member):
    role =  discord.utils.get(member.server.roles, name='Veggie Cutter')
    await client.add_roles(member, role)

# Disconnects the bot's voice client from the voice channel
@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

"""
Bot joins the voice channel the user issuing the command is in
A player is created and plays the audio the user searched for or
a player is created and put in queue if there's already a player active
    @args * - supports multiple strings divided my spaces
    @args query - string
    '!play mozart symphony 40 g minor'
"""
@client.command(pass_context=True)
async def play(ctx, *, query):
    options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10"
    author = ctx.message.author
    query = youtube.findvid(query)
    server = ctx.message.server
    channelVoice = ctx.message.author.voice.voice_channel
    if not client.is_voice_connected(server):
        await client.join_voice_channel(channelVoice)
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(query, before_options = options, after = lambda: check_queue(server.id))
        player.start()
        embed = discord.Embed(
            color = discord.Color.gold()
        )
        embed.set_author(name = player.title)
        await client.say(embed = embed)
    else:
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(query, before_options = options, after = lambda: check_queue(server.id))
        if player.is_playing == True:
            if server.id in queues:
                queues[server.id].append(player)
            else:
                queues[server.id] = [player]
            players[server.id] = player
            embed = discord.Embed(
                color = discord.Color.gold()
            )
            embed.set_author(name = player.title)
            await client.say(author, embed = embed)
        else:
            player.start()

# Pause command for player
@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

# Resume command for player
@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

# Stop command for player
@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

# Sends a private message containing the bot commands list to the user who imputted the command
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        color = discord.Color.gold()
    )
    embed.set_author(name = 'Commands list:')
    embed.add_field(name = '!help', value='PMs you the commands list.', inline=False)
    embed.add_field(name = '!clear', value='Clears the chat.', inline=False)
    embed.add_field(name = '!play', value='Plays a clip from Youtube. Control with !pause, !resume, !stop', inline=False)
    embed.add_field(name = '!leave', value='Makes the bot leave the voice channel.')
    await client.send_message(author, embed=embed)

# Deletes the specified number of messages in chat; '!clear 14' or '!clear' (default = 10)
@client.command(pass_context=True)
async def clear(ctx, amount = 10):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages deleted')

client.run(TOKEN)