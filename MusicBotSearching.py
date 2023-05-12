# We are generating a list of valid song and album names, 
# if our input doesn't match one exactly, 
# we make the thing display the 3 closest matches for reference and copy pasting

from MusicLibraryNavigation import *

# Returns a two-item tuple containing a list of all album names and a list of all song names in the music library (do this once on bot startup)
def generate_album_and_song_list():
    all_album_names = []
    all_album_folders = []
    all_song_names = []
    for genre in get_all_genres():
        names_to_add, folder_names_to_add = get_album_and_folder_names_from_genre(genre)
        all_album_names += names_to_add
        all_album_folders += folder_names_to_add
    for album in all_album_folders:
        all_song_names += get_song_and_file_names_from_album(album)[0]
    return all_album_names, all_song_names

all_album_names, all_song_names = generate_album_and_song_list()

def song_suggestions(bad_song_name):
    # I want to make it so it prioritizes titles with the input already in them
        # if len([song_name for song_name in all_song_names if bad_song_name in song_name]) > 2:
            # we just work with this list now (the song names that have the input in them)
        # else: see below
    # comparison_values = [comparison_function(bad_song_name, song_name) for song_name in all_song_names] 
    # zip the comparison values with all_song_names, then sort to get the top 3 results for comparison_values then return the corresponding song names
    closest_songs = 3
    return closest_songs

def album_suggestions(bad_album_name):
    # See song_suggestions
    closest_albums = 3
    return closest_albums