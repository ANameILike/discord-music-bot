# To add: loop queue/current song
# To improve: show queue

# Import stuff
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
from os.path import exists as file_exists
import random
from apikeys import *

# Creates a list of available songs (cleaned_song_list)
def get_clean_list():
    raw_song_list = os.listdir("music")
    remove_m4a = [s.replace(".m4a", "") for s in raw_song_list]
    remove_mp3 = [s.replace(".mp3", "") for s in remove_m4a]
    return remove_mp3

# For valid song names, returns a source for the player
def get_source(song_name):
    if file_exists("music\\" + song_name + ".m4a"):
        source = FFmpegPCMAudio("music\\" + song_name + ".m4a")
        return source
    elif file_exists("music\\" + song_name + ".mp3"):
        source = FFmpegPCMAudio("music\\" + song_name + ".mp3")
        return source
    else:
        return False

# Still setting up
client = commands.Bot(command_prefix = '!', help_command=None)

# Queue setup
cleaned_song_list = get_clean_list()
song_queue = []
queued_song_names = []
song_discard = []
discarded_song_names = []

# Exactly what the title says
def play_next_in_queue(ctx):
    if len(song_queue) > 1:
        voice = ctx.guild.voice_client
        next_up = song_queue[1]
        remove_first_song_in_queue = song_queue.pop(0)
        remove_first_name = queued_song_names.pop(0)
        song_discard.append(remove_first_song_in_queue)
        discarded_song_names.append(remove_first_name)
        player = voice.play(next_up)


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
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        await ctx.send("Hello")
    else:
        await ctx.send("You gotta be in a voice channel lol")

# (!leave) Leave voice channel
@client.command()
async def leave(ctx):
    if ctx.voice_client:
        if ctx.author.voice:
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Kk goodbye")
        else:
            await ctx.send("You gotta be in the voice channel lol")
    else:
        await ctx.send("I'm not in a voice channel lol")

# (!pause) Basic pause
@client.command()
async def pause(ctx):
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel lol")
    elif not ctx.author.voice:
        await ctx.send("You gotta be a voice channel lol")
    else:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Gotta be playing something to pause lol")

# (!resume) Basic resume
@client.command()
async def resume(ctx):   
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel lol")
    elif not ctx.author.voice:
        await ctx.send("You gotta be a voice channel lol")
    else:    
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
           await ctx.send("Gotta be paused to resume something lol")

# (!stop) Basic stop
@client.command()
async def stop(ctx):    
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel lol")
    elif not ctx.author.voice:
        await ctx.send("You gotta be a voice channel lol")
    else:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.stop()

# (!play [songname]) Plays a song if something's not already playing, adds it to the queue otherwise
@client.command()
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    potential_source = get_source(arg)
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel lol")
    elif not ctx.author.voice:
        await ctx.send("You gotta be a voice channel lol")
    elif potential_source == False:
        await ctx.send("not a valid name, possible songs below:")
        await ctx.send("\n".join(cleaned_song_list))
    else:
        if song_queue == []:
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
    if len(song_queue) > 0:
        cleaned_queue_listing = "\n".join(queued_song_names)
        await ctx.send("(NOW PLAYING) " + cleaned_queue_listing)
    else:
        await ctx.send("Queue's empty lol")

# (!skip) Skips the current song
@client.command()
async def skip(ctx):
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel lol")
    elif not ctx.author.voice:
        await ctx.send("You gotta be a voice channel lol")
    else:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            await ctx.send("Nothing's playing lol")
        elif len(song_queue) == 1:
            voice.stop()
            await ctx.send("You've reached the end!")
        else:
            voice.stop()
            play_next_in_queue(ctx)

# (!clear) Clears the queue
@client.command()
async def clear(ctx):
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel lol")
    elif not ctx.author.voice:
        await ctx.send("You gotta be a voice channel lol")
    else:
        song_queue.clear()
        song_discard.clear()
        queued_song_names.clear()
        discarded_song_names.clear()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send("Everything's gone now")

# (!remove [place]) Removes the song at the specified place in the queue (0 for currently playing)
@client.command()
async def remove(ctx, arg):
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel lol")
    elif not ctx.author.voice:
        await ctx.send("You gotta be a voice channel lol")
    else:
        try:
            queue_place = int(arg)
            if queue_place < 0:
                await ctx.send("Negative queue place lol really")
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
    voice = ctx.guild.voice_client
    try:
        arg_as_number = int(arg)
    except ValueError:
        await ctx.send("That's not a valid number lol")
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel lol")
    elif not ctx.author.voice:
        await ctx.send("You gotta be a voice channel lol")
    elif arg_as_number < 1:
        await ctx.send("What's the point lol")
    elif arg_as_number > 10:
        await ctx.send("Let's keep it below 10 at once lol")
    else:
        random_songs = random.choices(cleaned_song_list, k=arg_as_number)
        for random_song in random_songs:
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



