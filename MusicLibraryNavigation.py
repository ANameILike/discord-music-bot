# Base music library path: C:\Users\Natha\Music\Downloaded Music
    # Path up to song: C:\Users\Natha\Music\Downloaded Music\Genre\Album\Song
# Type 1 Albums/Playlists have a defined order (have a number before the title)
# Type 2 Albums/Playlists have no defined order (no number before the title)

import os
import random

base_path = r"C:\Users\Natha\Music\Downloaded Music"

# Returns a list of genres in Downloaded Music
def get_all_genres():
    everything_in_music = os.listdir(base_path)
    only_genres = [item for item in everything_in_music if "(Genre) " in item]
    genre_names = [genre[8:] for genre in only_genres]
    return genre_names

# Takes a string for genre, returns (as a two-item tuple) both a list of album names and album folder names in the specified genre
def get_album_and_folder_names_from_genre(genre):
    everything_in_genre = os.listdir(base_path + fr"\(Genre) {genre}")
    only_album_folders = [item for item in everything_in_genre if "(Album) " in item]
    album_names = [album[8:-6] for album in only_album_folders]
    album_folder_names = [album[8:] for album in only_album_folders]
    return album_names, album_folder_names

# Takes a string for album, returns the genre that the album belongs to
def get_genre_from_album(album):
    for genre in get_all_genres():
        if album in get_album_and_folder_names_from_genre(genre)[1]:
            return genre
    return "Unable to get genre from album."

# Key for sorting song names alphabetically (in numerical order versus 1 -> 10 -> 2)
def song_name_sorter(song_name):
    number = song_name.partition(". ")[0]
    return int(number)

# Takes a string for album, returns (as a two-item tuple) both a list of song names and a list of file names in the specified album
def get_song_and_file_names_from_album(album):
    genre = get_genre_from_album(album)
    contents = os.listdir(base_path + fr"\(Genre) {genre}" + fr"\(Album) {album}")
    if "AlbumArtSmall.jpg" in contents:
        contents.remove("AlbumArtSmall.jpg")
    if "Folder.jpg" in contents:
        contents.remove("Folder.jpg")
    if "1. " in contents[0]:
        # album_type = 1
        contents = sorted(contents, key=song_name_sorter)
        song_names_with_rating_maybe = [content[content.index(". ") + 2: -4] for content in contents]
    else:
        # album_type = 2
        song_names_with_rating_maybe = [content[:-4] for content in contents]
    final_song_names = []
    for song_name in song_names_with_rating_maybe:
        if len(song_name) > 6 and song_name[-6] == "[":
            final_song_names.append(song_name[:-7])
        else:
            final_song_names.append(song_name)
    return final_song_names, contents


# Checks to see if provided album name matches an existing one
def check_album_validity_and_get_tag(album_input):
    all_album_names = []
    all_album_folder_names = []
    for genre in get_all_genres():
        all_album_names += get_album_and_folder_names_from_genre(genre)[0]
        all_album_folder_names += get_album_and_folder_names_from_genre(genre)[1]
    lowercase_album_names = [album_name.lower() for album_name in all_album_names]
    if album_input.lower() in lowercase_album_names:
        album_index = lowercase_album_names.index(album_input.lower())
        proper_album_name = all_album_names[album_index]
        the_folder_name_we_need = all_album_folder_names[album_index]
        #only_the_one = [album_folder_name for album_folder_name in all_album_folder_names if album_input.lower() in album_folder_name.lower()][0]
        tag = the_folder_name_we_need[-5:]
        return True, tag, proper_album_name
    else:
        return False, "Ain't getting a tag for this one", "It's not even case sensitive anymore how are you getting this wrong?"

# Identifies and returns the song's path by iterating through each album in each genre
def get_song_path(song_name_input):
    for genre in get_all_genres():
        for album in get_album_and_folder_names_from_genre(genre)[1]:
            song_names, file_names = get_song_and_file_names_from_album(album)
            for song_name in song_names:
                if song_name_input.lower() == song_name.lower():
                    file_name = file_names[song_names.index(song_name)]
                    return base_path + fr"\(Genre) {genre}" + fr"\(Album) {album}" + fr"\{file_name}"
    return 0