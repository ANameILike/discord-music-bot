# Base music library path: C:\Users\Natha\Music\Downloaded Music
    # Path up to song: C:\Users\Natha\Music\Downloaded Music\Genre\Album\Song
# Type 1 Albums/Playlists have a defined order (have a number before the title)
# Type 2 Albums/Playlists have no defined order (no number before the title)

import os
import random

base_path = r"C:\Users\Natha\Music\Downloaded Music"

# Returns a list of genres in Download Music
def get_all_genres():
    everything_in_music = os.listdir(base_path)
    only_genres = [item for item in everything_in_music if "(Genre) " in item]
    genre_names = [genre[8:] for genre in only_genres]
    return genre_names

# Takes a string for genre, returns a list of albums (folder names) in the specified genre
def get_album_folder_names_from_genre(genre):
    everything_in_genre = os.listdir(base_path + fr"\(Genre) {genre}")
    only_album_folders = [item for item in everything_in_genre if "(Album) " in item]
    album_folder_names = [album[8:] for album in only_album_folders]
    return album_folder_names

# Takes a string for genre, returns a list of album names in the specified genre
def get_album_names_from_genre(genre):
    everything_in_genre = os.listdir(base_path + fr"\(Genre) {genre}")
    only_album_folders = [item for item in everything_in_genre if "(Album) " in item]
    album_names = [album[8:-6] for album in only_album_folders]
    return album_names

# Takes a string for album, returns the genre that the album belongs to
def get_genre_from_album(album):
    for genre in get_all_genres():
        if album in get_album_folder_names_from_genre(genre):
            return genre
    return "Unable to get genre from album."

# Key for sorting song names alphabetically (in numerical order versus 1 -> 10 -> 2)
def song_name_sorter(song_name):
    number = song_name.partition(". ")[0]
    return int(number)

# Takes a string for album, returns a cleaned list of songs in the specified album
def get_song_names_from_album(album):
    genre = get_genre_from_album(album)
    contents = os.listdir(base_path + fr"\(Genre) {genre}" + fr"\(Album) {album}")
    if "1. " in contents[0]:
        album_type = 1
        song_names = [content[content.index(". ") + 2: -4] for content in sorted(contents, key=song_name_sorter)]
    else:
        album_type = 2
        song_names = [content[:-4] for content in contents]
    return song_names

# Takes a string for album, returns a raw list of file names in the specified album
def get_file_names_from_album(album):
    genre = get_genre_from_album(album)
    contents = os.listdir(base_path + fr"\(Genre) {genre}" + fr"\(Album) {album}")
    return contents

# Takes a string for album, returns both a list of song names and a list of file names in the specified
def get_song_and_file_names_from_album(album):
    genre = get_genre_from_album(album)
    contents = os.listdir(base_path + fr"\(Genre) {genre}" + fr"\(Album) {album}")
    if "1. " in contents[0]:
        album_type = 1
        song_names = [content[content.index(". ") + 2: -4] for content in contents]
    else:
        album_type = 2
        song_names = [content[:-4] for content in contents]
    return song_names, contents

# Checks to see if provided album name matches an existing one
def check_album_validity_and_get_tag(album_input):
    all_album_names = []
    all_album_folder_names = []
    for genre in get_all_genres():
        all_album_names += get_album_names_from_genre(genre)
        all_album_folder_names += get_album_folder_names_from_genre(genre)
    if album_input in all_album_names:
        only_the_one = [album for album in all_album_folder_names if album_input in album][0]
        tag = only_the_one[-5:]
        return True, tag
    else:
        return False

# Identifies and returns the song's path by iterating through each album in each genre
def get_song_path(song_name_input):
    for genre in get_all_genres():
        for album in get_album_folder_names_from_genre(genre):
            song_names, file_names = get_song_and_file_names_from_album(album)
            for song_name in song_names:
                if song_name_input == song_name:
                    file_name = file_names[song_names.index(song_name)]
                    return base_path + fr"\(Genre) {genre}" + fr"\(Album) {album}" + fr"\{file_name}"
    return 0

# Returns a list containing the proportion of albums in each genre
def get_genre_densities():
    total_album_count = 0
    album_count_list = []
    for genre in get_all_genres():
        album_count = len([album for album in get_album_folder_names_from_genre(genre) if "[gen]" in album]) 
        total_album_count += album_count
        album_count_list.append(album_count)
    density_list = [count / total_album_count for count in album_count_list]
    return density_list

# Returns a random (acceptable) song name
def get_any_random_song_name():
    random_genre = random.choices(get_all_genres(), weights=get_genre_densities(), k=1)[0]
    random_album = random.choice([album for album in get_album_folder_names_from_genre(random_genre) if "[gen]" in album])
    random_song = random.choice(get_song_names_from_album(random_album))
    return random_song

# Returns a random (acceptable) list of song names from a single album
def get_any_random_album():
    # should have a list of acceptable playlists, split into Type 1s and Type 2s
    # randomly pick Type1 or Type2, then randomly pick a random playlist from those
    # if Type1, return list of names split from numbers (but keep the order)
    # if Type2, return list of names (shuffle the order)
    current_type = 0
    random_genre = random.choices(get_all_genres(), weights=get_genre_densities(), k=1)[0]
    random_album = random.choice([album for album in get_album_folder_names_from_genre(random_genre) if "[gen]" in album])
    return get_song_names_from_album(random_album)