# We are generating a list of valid song and album names,
# if our input doesn't match one exactly,
# we make the thing display the 3 closest matches for reference and copy pasting

import MusicBotMetadata
import difflib

all_album_names, all_song_names = MusicBotMetadata.all_album_names, MusicBotMetadata.all_song_names
all_artists_and_genres = MusicBotMetadata.all_artists_and_genres
all_genres_songs_and_artists = MusicBotMetadata.all_genres_songs_and_artists

# Takes a lowercase name as well as "album, song, artist, or genre name" specification, returns the name with all capital letters originally present restored.
def lowercase_to_proper_name(lowercase_name, album_song_artist_or_genre):
    if album_song_artist_or_genre == "album":
        lowercase_pool = [album_name.lower() for album_name in all_album_names]
        name_location = lowercase_pool.index(lowercase_name)
        proper_name = all_album_names[name_location]
    elif album_song_artist_or_genre == "song":
        lowercase_pool = [song_name.lower() for song_name in all_song_names]
        name_location = lowercase_pool.index(lowercase_name)
        proper_name = all_song_names[name_location]
    elif album_song_artist_or_genre == "artist":
        lowercase_pool = [artist_name.lower() for artist_name in list(all_artists_and_genres.keys())]
        name_location = lowercase_pool.index(lowercase_name)
        proper_name = list(all_artists_and_genres.keys())[name_location]
    elif album_song_artist_or_genre == "genre":
        lowercase_pool = [genre_name.lower() for genre_name in list(all_genres_songs_and_artists.keys())]
        name_location = lowercase_pool.index(lowercase_name)
        proper_name = list(all_genres_songs_and_artists.keys())[name_location]
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

# Takes an invalid artist name and returns the closest artist name available (as a list for discord UI appearance).
def artist_suggestion(bad_artist_name):
    no_case = [artist_name.lower() for artist_name in all_artists_and_genres.keys()]
    artist_names_with_bad_name_as_substring = [artist_name for artist_name in no_case if bad_artist_name.lower() in artist_name]
    if len(artist_names_with_bad_name_as_substring) > 0:
        lowercase_closest_artist = difflib.get_close_matches(bad_artist_name.lower(), artist_names_with_bad_name_as_substring, n=1, cutoff=0)
        correct_artist_name = lowercase_to_proper_name(lowercase_closest_artist[0], "artist")
    else:
        lowercase_closest_artist = difflib.get_close_matches(bad_artist_name.lower(), no_case, n=1, cutoff=0)
        correct_artist_name = lowercase_to_proper_name(lowercase_closest_artist[0], "artist")   
    return [correct_artist_name]

# Takes an invalid genre name and returns the closest genre name available (as a list for discord UI appearance).
def genre_suggestion(bad_genre_name):
    no_case = [genre_name.lower() for genre_name in all_genres_songs_and_artists.keys()]
    genre_names_with_bad_name_as_substring = [genre_name for genre_name in no_case if bad_genre_name.lower() in genre_name]
    if len(genre_names_with_bad_name_as_substring) > 0:
        lowercase_closest_genre = difflib.get_close_matches(bad_genre_name.lower(), genre_names_with_bad_name_as_substring, n=1, cutoff=0)
        correct_genre_name = lowercase_to_proper_name(lowercase_closest_genre[0], "genre")
    else:
        lowercase_closest_genre = difflib.get_close_matches(bad_genre_name.lower(), no_case, n=1, cutoff=0)
        correct_genre_name = lowercase_to_proper_name(lowercase_closest_genre[0], "genre")   
    return [correct_genre_name]