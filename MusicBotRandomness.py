# Contains code for random selection of songs, albums, and whatnot

import random
from MusicLibraryNavigation import *

# Returns a list containing the proportion of albums in each genre
def get_genre_densities():
    total_album_count = 0
    album_count_list = []
    for genre in get_all_genres():
        album_count = len([album for album in get_album_and_folder_names_from_genre(genre)[1] if "[gen]" in album]) 
        total_album_count += album_count
        album_count_list.append(album_count)
    density_list = [count / total_album_count for count in album_count_list]
    return density_list

# Returns a random (acceptable) song name
def get_any_random_song_name():
    random_genre = random.choices(get_all_genres(), weights=get_genre_densities(), k=1)[0]
    random_album = random.choice([album for album in get_album_and_folder_names_from_genre(random_genre)[1] if "[gen]" in album])
    random_song = random.choice(get_song_and_file_names_from_album(random_album)[0])
    return random_song

# Returns a random (acceptable) list of song names from a single album
def get_any_random_album():
    # should have a list of acceptable playlists, split into Type 1s and Type 2s
    # randomly pick Type1 or Type2, then randomly pick a random playlist from those
    # if Type1, return list of names split from numbers (but keep the order)
    # if Type2, return list of names (shuffle the order)
    current_type = 0
    random_genre = random.choices(get_all_genres(), weights=get_genre_densities(), k=1)[0]
    random_album = random.choice([album for album in get_album_and_folder_names_from_genre(random_genre)[1] if "[gen]" in album])
    return get_song_and_file_names_from_album(random_album)[0]