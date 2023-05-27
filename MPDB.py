# To add: loop queue/current song, music folders/playlists, smart folder selection, random playlist, shuffle
# To improve: show queue
# Timeout feature?
# Maybe a "Not these songs" function where you make a temporary new catalog with songs from same album gone
# Display genres, display albums, display songs
# Maybe change playrandom to randomsong? so you can do randomalbum?

# Priority: display catalog, play random playlists
# Add acknowledgement and display thing for playing albums!, fix skip not updating queue

# Import stuff
import discord
import MusicLibraryNavigation
import MusicBotRandomness
import MusicBotSearching
from discord.ext import commands
from discord import FFmpegPCMAudio
from os.path import exists as file_exists
from apikeys import *
import random
import asyncio
import os

# Returns a source for the player for valid names (invalid returns False)
def get_source(song_name):
    song_path = MusicLibraryNavigation.get_song_path(song_name)
    if song_path == 0:
        return False, "Bro you typed it wrong lol"
    elif file_exists(song_path):
        source = FFmpegPCMAudio(song_path)
        if song_path.partition(". ")[2] == "":
            name_with_rating_maybe = song_path.partition("]\\")[2][:-4]
        else:
            name_with_rating_maybe = song_path.partition(". ")[2][:-4]
        if len(name_with_rating_maybe) > 6 and name_with_rating_maybe[-6] == "[":
            proper_name = name_with_rating_maybe[:-7]
        else:
            proper_name = name_with_rating_maybe
        return source, proper_name
    else:
        return False, "Bro you typed it wrong lol"
    
# Still setting up
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = ['!', "！"], help_command=None, intents=intents)

# Queue setup
song_queue = []
queued_song_names = []
song_discard = []
discarded_song_names = []

# Setting up lists of valid album and song names
all_album_names, all_song_names = MusicBotSearching.all_album_names, MusicBotSearching.all_song_names

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
        voice.play(next_up, after=play_next_in_queue)
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
            await ctx.send("You gotta be in my voice channel lol GET IN HERE")
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
    if voice:
        voice.stop()

# Plays song if song queue is empty, appends song to the queue otherwise
def play_song(voice, song_source, song_display_name):
    if song_queue == []:
        song_queue.append(song_source)
        queued_song_names.append(song_display_name)
        voice.play(song_source, after=play_next_in_queue)
        return "Now playing " + song_display_name
    else:
        song_queue.append(song_source)
        queued_song_names.append(song_display_name)
        return "Added " + song_display_name + " to the queue!"

yes_responses = "yes, yeah, ye, ya, sure, yes please, sure please, yes pls, yes thanks, yeah thanks, ye thanks, ya thanks, sure thanks, yes thx, yeah thx, ye thx, ya thx, sure thx"
no_responses = "no, nah, no thank you, no thanks, nah thanks, no thx, nah thx"

# Determines if the user wants the suggested song played and acts accordingly (used in !play and !play-album in conjunction with the song_suggestions and album_suggestions functions)
def suggestion_followup_response(voice, user_response, song_or_album, suggestions):
    if user_response.content in yes_responses and song_or_album == "song":
        new_source, new_name_to_display = get_source(suggestions[0])
        display_message = play_song(voice, new_source, new_name_to_display)
        return display_message
    elif user_response.content in yes_responses and song_or_album == "album":
        album_to_play = suggestions[0]
        valid, tag, proper_album_name = MusicLibraryNavigation.check_album_validity_and_get_tag(album_to_play)
        song_names_in_album = MusicLibraryNavigation.get_song_and_file_names_from_album(proper_album_name + " " + tag)[0]
        for song_name in song_names_in_album:
            play_song(voice, get_source(song_name)[0], song_name)
        return "It's done!"
    elif user_response.content in no_responses:
        return "Ok!"
    else:
        return "Bro that was a yes or no question lol"  

# Commands start below

# Startup indicator
@client.event
async def on_ready():
    print("We're up!")
    print("---------")

# (!help) Displays commands
@client.command()
async def help(ctx):
    await ctx.send("Here are a list of potential commands to be used with the (!) prefix: \nGeneral: \n\thelp, hello \nMusic (must do !join first): \n\tplay [song name], play-album [album name], pause, resume, stop, leave \n\tqueue, shuffle, skip, remove [queue number], clear \n\tplayrandom [number]")

# (!hello) Basic hello
@client.command()
async def hello(ctx):
    await ctx.send("Hello!")

# (!join) Join voice channel
@client.command()
async def join(ctx):
    if await check_voice_channel(ctx, "user"):
        if client.voice_clients:
            await ctx.send("I'm already in a voice channel")
        else:
            await ctx.message.add_reaction("👍")
            channel = ctx.message.author.voice.channel
            await channel.connect()
            cease()

# (!leave) Leave voice channel
@client.command(aliases=["die", "depart", "goodbye"])
async def leave(ctx):
    if await check_voice_channel(ctx, "both"):
        await ctx.message.add_reaction("👍")
        cease()
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
@client.command(aliases=["放"])
async def play(ctx, *, arg):
    if await check_voice_channel(ctx, "both"):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        potential_source, name_to_display = get_source(arg)
        if potential_source == False:
            specific_song_suggestions = MusicBotSearching.song_suggestions(arg)
            await ctx.send("Either I don't have that song or you typed something wrong D: \nNo quotes or case sensitivity needed. \nHere are the 3 closest things I have to what you typed: \n" + f"{specific_song_suggestions}")
            await ctx.send("Want me to play the first one?")
            intended_respondent = ctx.author
            intended_channel = ctx.channel
            def check_intended(message):
                return message.author == intended_respondent and message.channel == intended_channel
            try:
                user_response = await client.wait_for("message", check=check_intended, timeout=15)
                bot_response = suggestion_followup_response(voice, user_response, "song", specific_song_suggestions)
                await ctx.send(bot_response)
            except asyncio.TimeoutError:
                await ctx.send("Bro you really left me hanging like that...")
        else:
            display_message = play_song(voice, potential_source, name_to_display)
            await ctx.send(display_message)

# (!play-album [albumname]) Plays all songs of an album
@client.command(name="play-album")
async def playalbum(ctx, *, arg):
    if await check_voice_channel(ctx, "both"):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        valid, tag, proper_album_name = MusicLibraryNavigation.check_album_validity_and_get_tag(arg)
        if not valid:
            specific_album_suggestions = MusicBotSearching.album_suggestions(arg)
            await ctx.send("Either I don't have that album or you typed something wrong D: \nDon't use quotes here and don't worry about case sensitivity. \nHere are the 3 closest things I have to what you typed: \n" + f"{specific_album_suggestions}")
            await ctx.send("Want me to play the first one?")
            intended_respondent = ctx.author
            intended_channel = ctx.channel
            def check_intended(message):
                return message.author == intended_respondent and message.channel == intended_channel
            try:
                user_response = await client.wait_for("message", check=check_intended, timeout=15)
                bot_response = suggestion_followup_response(voice, user_response, "album", specific_album_suggestions)
                await ctx.send(bot_response)
            except asyncio.TimeoutError:
                await ctx.send("Bro you really left me hanging like that...")
        else:
            await ctx.message.add_reaction("👍")
            songs_in_album = MusicLibraryNavigation.get_song_and_file_names_from_album(proper_album_name + " " + tag)[0]
            for song_name in songs_in_album:
                play_song(voice, get_source(song_name)[0], song_name)

# (!queue) Displays the queue
@client.command()
async def queue(ctx):
    if await check_voice_channel(ctx, "bot"):
        if len(song_queue) > 0:
            cleaned_queue_listing = "\n".join(queued_song_names)
            await ctx.send("(NOW PLAYING) " + cleaned_queue_listing)
        else:
            await ctx.send("Queue's empty lol")

# (!shuffle) Randomly reorders the queue (this is irreversible)
@client.command()
async def shuffle(ctx):
    if await check_voice_channel(ctx, "both"):
        global song_queue, queued_song_names
        if len(song_queue) > 2:
            await ctx.message.add_reaction("👍")
            names_and_associated_sources = list(zip(queued_song_names, song_queue))
            preserve_the_first = names_and_associated_sources.pop(0)
            random.shuffle(names_and_associated_sources)
            names_and_associated_sources.insert(0, preserve_the_first)
            queued_song_names, song_queue = zip(*names_and_associated_sources)
            queued_song_names = list(queued_song_names)
            song_queue = list(song_queue)
        elif len(song_queue) == 1 or len(song_queue) == 2:
            await ctx.send("Ahaha you gotta be kidding me right?")
        else:
            await ctx.send("Bro what are you trying to shuffle??")

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
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
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
                random_song = MusicBotRandomness.get_any_random_song_name()
                source_of_random_song = get_source(random_song)[0]
                await ctx.send(play_song(voice, source_of_random_song, random_song))

# Starts the magic
client.run(BOTTOKEN)