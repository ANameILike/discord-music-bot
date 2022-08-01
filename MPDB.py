# To add: loop queue/current song, music folders/playlists, smart folder selection, random playlist, shuffle
# To improve: show queue
# Timeout feature?
# Maybe a "Not these songs" function where you make a temporary new catalog with songs from same album gone
# Display genres, display albums, display songs

# Priority: display catalog, play random playlists

# Import stuff
import discord
import MusicLibraryNavigation
from discord.ext import commands
from discord import FFmpegPCMAudio
from os.path import exists as file_exists
from apikeys import *
import random
import os


# Returns a source for the player for valid names (invalid returns False)
def get_source(song_name):
    song_path = MusicLibraryNavigation.get_song_path(song_name)
    if song_path == 0:
        return False 
    elif file_exists(song_path):
        source = FFmpegPCMAudio(song_path)
        return source
    else:
        return False

# Still setting up
client = commands.Bot(command_prefix = '!', help_command=None)

# Queue setup
song_queue = []
queued_song_names = []
song_discard = []
discarded_song_names = []

# Exactly what the name suggests
def play_next_in_queue(useless):
    if len(song_queue) > 1:
        voice = discord.utils.get(client.voice_clients)
        next_up = song_queue[1]
        remove_first_song_in_queue = song_queue.pop(0)
        remove_first_name = queued_song_names.pop(0)
        song_discard.append(remove_first_song_in_queue)
        discarded_song_names.append(remove_first_name)
        voice.stop()
        player = voice.play(next_up, after=play_next_in_queue)
    else:
        cease()

# Returns True/False based on who's present in the voice channel
# modes: "bot" checks for bot, "user" checks for user, "both" checks for both
async def check_voice_channel(ctx, mode):
    if mode == "bot":
        if ctx.voice_client:
            return True
        else:
            await ctx.send("I'm not in a voice channel lol")
            return False
    elif mode == "user":
        if ctx.author.voice:
            return True
        else:
            await ctx.send("You gotta be in a voice channel lol")
            return False
    elif mode == "both":
        if not ctx.author.voice and not ctx.voice_client:
            await ctx.send("You're not in a voice channel. I'm not in a voice channel. What are we doing here?")
            return False
        elif ctx.author.voice and not ctx.voice_client:
            await ctx.send("I'm not in a voice channel lol")
            return False
        elif not ctx.author.voice or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send("You gotta be in my voice channel lol")
            return False
        else:
            return True

# Stops playing, clears the queue
def cease():
    song_queue.clear()
    song_discard.clear()
    queued_song_names.clear()
    discarded_song_names.clear()
    voice = discord.utils.get(client.voice_clients)
    voice.stop()

# Commands start below

# Startup indicator
@client.event
async def on_ready():
    print("We're up!")
    print("---------")

# (!help) Displays commands
@client.command()
async def help(ctx):
    await ctx.send("Here are a list of potential commands to be used with the (!) prefix: \nGeneral: \n\thelp, hello \nMusic (must do !join first): \n\tplay [song name], pause, resume, stop, leave \n\tqueue, skip, remove [queue number], clear \n\tplayrandom [number]")

# (!hello) Basic hello
@client.command()
async def hello(ctx):
    await ctx.send("Hello!")

# (!join) Join voice channel
@client.command()
async def join(ctx):
    if await check_voice_channel(ctx, "user"):
        if ctx.voice_client:
            await ctx.send("I'm already in a voice channel")
        else:
            await ctx.message.add_reaction("👍")
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()

# (!leave) Leave voice channel
@client.command()
async def leave(ctx):
    if await check_voice_channel(ctx, "both"):
        await ctx.message.add_reaction("👍")
        await ctx.guild.voice_client.disconnect()

# (!pause) Basic pause
@client.command()
async def pause(ctx):
    if await check_voice_channel(ctx, "both"):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await ctx.message.add_reaction("👍")
            voice.pause()
        else:
            await ctx.send("Gotta be playing something to pause lol")

# (!resume) Basic resume
@client.command()
async def resume(ctx):   
    if await check_voice_channel(ctx, "both"):   
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            await ctx.message.add_reaction("👍")
            voice.resume()
        else:
           await ctx.send("Gotta be paused to resume something lol")

# (!stop) Basic stop, clears the queue (pretty much synonymous with !clear)
@client.command()
async def stop(ctx):    
    if await check_voice_channel(ctx, "both"):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing() or voice.is_paused():
            await ctx.message.add_reaction("👍")
            cease()
        else:
            await ctx.send("What are you stopping lol")

# (!play [songname]) Plays a song if something's not already playing, adds it to the queue otherwise
@client.command()
async def play(ctx, arg):
    if await check_voice_channel(ctx, "both"):
        voice = ctx.guild.voice_client
        potential_source = get_source(arg)
        if potential_source == False:
            await ctx.send("Either I don't have that song or you typed something wrong. Song names are case sensitive and multi-word names should be in quotes.")
        elif song_queue == []:
            song_queue.append(potential_source)
            queued_song_names.append(arg)
            player = voice.play(potential_source, after=play_next_in_queue)
            await ctx.send("Now playing " + arg)
        else:
            song_queue.append(potential_source)
            queued_song_names.append(arg)
            await ctx.send("Added " + arg + " to the queue!")

# (!queue) Displays the queue
@client.command()
async def queue(ctx):
    if await check_voice_channel(ctx, "bot"):
        if len(song_queue) > 0:
            cleaned_queue_listing = "\n".join(queued_song_names)
            await ctx.send("(NOW PLAYING) " + cleaned_queue_listing)
        else:
            await ctx.send("Queue's empty lol")

# (!skip) Skips the current song
@client.command()
async def skip(ctx):
    if await check_voice_channel(ctx, "both"):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            await ctx.send("Nothing's playing lol")
        elif len(song_queue) == 1:
            cease()
            await ctx.send("You've reached the end!")
        else:
            await ctx.message.add_reaction("👍")
            voice.stop()

# (!clear) Clears the queue
@client.command()
async def clear(ctx):
    if await check_voice_channel(ctx, "both"):
        cease()
        await ctx.send("Everything's gone now")

# (!remove [place]) Removes the song at the specified place in the queue (0 for currently playing)
@client.command()
async def remove(ctx, arg):
    if await check_voice_channel(ctx, "both"):
        try:
            queue_place = int(arg)
            if queue_place < 0:
                await ctx.send("Negative queue place lol really")
            elif queue_place == 0:
                await ctx.send("Use !skip instead please (tbh idk how to implement this)")
            else:
                song_queue.pop(queue_place)
                removed_name = queued_song_names.pop(queue_place)
                if song_queue == []:
                    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
                    voice.stop()
                await ctx.send("Removed " + removed_name)
        except ValueError:
            await ctx.send("That's not a valid number lol")
        except IndexError:
            await ctx.send("That's not in the queue lol")

# (!playrandom [number]) Plays a number of random songs
@client.command()
async def playrandom(ctx, arg):
    if await check_voice_channel(ctx, "both"):
        voice = ctx.guild.voice_client
        try:
            arg_as_number = int(arg)
        except ValueError:
            await ctx.send("That's not a valid number lol")
        if arg_as_number < 1:
            await ctx.send("What's the point lol")
        elif arg_as_number > 10:
            await ctx.send("Let's keep it below 10 at once lol")
        else:
            for i in range(arg_as_number):
                random_song = MusicLibraryNavigation.get_any_random_song_name()
                source_of_random_song = get_source(random_song)
                if song_queue == []:
                    song_queue.append(source_of_random_song)
                    queued_song_names.append(random_song)
                    player = voice.play(source_of_random_song, after=play_next_in_queue)
                    await ctx.send("Now playing " + random_song)
                else:
                    song_queue.append(source_of_random_song)
                    queued_song_names.append(random_song)
                    await ctx.send("Added " + random_song + " to the queue!")    

# Starts the magic
client.run(BOTTOKEN)