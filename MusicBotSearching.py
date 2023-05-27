# We are generating a list of valid song and album names, 
# if our input doesn't match one exactly, 
# we make the thing display the 3 closest matches for reference and copy pasting

from MusicLibraryNavigation import *
import difflib

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

# Takes a lowercase name as well as "album or song name" specification, returns the name with all capital letters originally present restored.
def lowercase_to_proper_name(lowercase_name, album_or_song):
    if album_or_song == "album":
        lowercase_pool = [album_name.lower() for album_name in all_album_names]
        name_location = lowercase_pool.index(lowercase_name)
        proper_name = all_album_names[name_location]
    else:
        lowercase_pool = [song_name.lower() for song_name in all_song_names]
        name_location = lowercase_pool.index(lowercase_name)
        proper_name = all_song_names[name_location]
    return proper_name

# Takes an invalid name and returns a list of the three most similar song names available.
def song_suggestions(bad_song_name):
    no_case = [song_name.lower() for song_name in all_song_names]
    song_names_with_bad_name_as_substring = [song_name for song_name in no_case if bad_song_name.lower() in song_name]
    if len(song_names_with_bad_name_as_substring) > 0:
        three_ish_closest_songs_lowercase = difflib.get_close_matches(bad_song_name.lower(), song_names_with_bad_name_as_substring, n=3, cutoff=0)
        how_many_more_do_we_need = 3 - len(three_ish_closest_songs_lowercase)
        if how_many_more_do_we_need > 0:
            avoid_repeats = [song_name for song_name in no_case if song_name not in song_names_with_bad_name_as_substring]
            necessary_addition = difflib.get_close_matches(bad_song_name.lower(), avoid_repeats, n=how_many_more_do_we_need, cutoff=0)
            final_three_lowercase = three_ish_closest_songs_lowercase + necessary_addition
            three_correct_song_names = [lowercase_to_proper_name(lowercase_name, "song") for lowercase_name in final_three_lowercase]
        else:
            three_correct_song_names = [lowercase_to_proper_name(lowercase_name, "song") for lowercase_name in three_ish_closest_songs_lowercase]
    else:
        three_lowercase_names = difflib.get_close_matches(bad_song_name.lower(), no_case, n=3, cutoff=0)
        three_correct_song_names = [lowercase_to_proper_name(lowercase_name, "song") for lowercase_name in three_lowercase_names]
    return three_correct_song_names

# Takes an invalid name and returns a list of the three most similar album names available.
def album_suggestions(bad_album_name):
    no_case = [album_name.lower() for album_name in all_album_names]
    album_names_with_bad_name_as_substring = [album_name for album_name in no_case if bad_album_name.lower() in album_name]
    if len(album_names_with_bad_name_as_substring) > 0:
        three_ish_closest_albums_lowercase = difflib.get_close_matches(bad_album_name.lower(), album_names_with_bad_name_as_substring, n=3, cutoff=0)
        how_many_more_do_we_need = 3 - len(three_ish_closest_albums_lowercase)
        if how_many_more_do_we_need > 0:
            avoid_repeats = [album_name for album_name in no_case if album_name not in album_names_with_bad_name_as_substring]
            necessary_addition = difflib.get_close_matches(bad_album_name.lower(), avoid_repeats, n=how_many_more_do_we_need, cutoff=0)
            final_three_lowercase = three_ish_closest_albums_lowercase + necessary_addition
            three_correct_album_names = [lowercase_to_proper_name(lowercase_name, "album") for lowercase_name in final_three_lowercase]
        else:
            three_correct_album_names = [lowercase_to_proper_name(lowercase_name, "album") for lowercase_name in three_ish_closest_albums_lowercase]
    else:
        three_lowercase_names = difflib.get_close_matches(bad_album_name.lower(), no_case, n=3, cutoff=0)
        three_correct_album_names = [lowercase_to_proper_name(lowercase_name, "album") for lowercase_name in three_lowercase_names]
    return three_correct_album_names