# Contains code for reading and using song metadata, specifically artist and genre for now

from MusicLibraryNavigation import base_path, get_all_genres, get_album_and_folder_names_from_genre, get_song_file_and_with_tag_names_from_album, get_song_path
from tinytag import TinyTag

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
        all_song_names += get_song_file_and_with_tag_names_from_album(album)[0]
    return all_album_names, all_song_names

all_album_names, all_song_names = generate_album_and_song_list()

# Returns a dict of artist:genre items (used at startup)
def get_all_artists_and_genres():
    artist_genre_dict = {}
    for genre in get_all_genres():
        for album_folder in get_album_and_folder_names_from_genre(genre)[1]:
            for song_file in get_song_file_and_with_tag_names_from_album(album_folder)[1]:
                song_artist = TinyTag.get(base_path + fr"\(Genre) {genre}" + fr"\(Album) {album_folder}" + fr"\{song_file}").artist
                if song_artist not in artist_genre_dict.keys():
                    artist_genre_dict[song_artist] = genre
                # Identifying artists with songs in multiple genres
                # if artist_genre_dict[song_artist] != genre:
                    # print(song_artist)
    # Manually dealing with artists that have songs in multiple genres - I'm never going to have artists in more than 2 though
    artist_genre_dict["Wham!"] = "80s English | Christmas"
    artist_genre_dict["Casiopea"] = "80s Japanese | Jazz Fusion"
    artist_genre_dict["Michael Bublé"] = "Christmas | Modern English"
    artist_genre_dict["Kelly Clarkson"] = "Christmas | Modern English"
    artist_genre_dict["Daft Punk"] = "80s English | Modern English"
    artist_genre_dict["Imagine Dragons"] = "Film, Game, and Show Music | Modern English"
    return artist_genre_dict

all_artists_and_genres = get_all_artists_and_genres()
# Can use all_artists_and_genres.keys() for artist suggestions

# Returns a dict with genres as keys, and songs:artists dicts as their values (used at startup) 
def get_all_genres_songs_and_artists():
    all_songs_and_artists_by_genre = {}
    for genre in get_all_genres():
        song_artist_dict = {}
        for album_folder in get_album_and_folder_names_from_genre(genre)[1]:
            song_files, songs_with_tags = get_song_file_and_with_tag_names_from_album(album_folder)[1:]
            for i in range(len(song_files)):
                song_artist = TinyTag.get(base_path + fr"\(Genre) {genre}" + fr"\(Album) {album_folder}" + fr"\{song_files[i]}").artist
                song_artist_dict[songs_with_tags[i]] = song_artist
        all_songs_and_artists_by_genre[genre] = song_artist_dict
    return all_songs_and_artists_by_genre

all_genres_songs_and_artists = get_all_genres_songs_and_artists()

# get_artist_from_song?

# Takes artist name input, returns list of songs (with tags still on) by that artist (with [icon] or [best] tags coming later)
def get_songs_by_artist(artist_name):
    songs_by_artist = []
    lowercase_artists = [artist_name.lower() for artist_name in all_artists_and_genres.keys()]
    if artist_name.lower() in lowercase_artists:
        artist_index = lowercase_artists.index(artist_name.lower())
        proper_artist_name = list(all_artists_and_genres.keys())[artist_index]
        one_or_two_genres = all_artists_and_genres[proper_artist_name].partition(" | ")
        songs_and_artists_in_first_genre = all_genres_songs_and_artists[one_or_two_genres[0]]
        for song_with_tag in songs_and_artists_in_first_genre.keys():
            if proper_artist_name == songs_and_artists_in_first_genre[song_with_tag]:
                songs_by_artist.append(song_with_tag)
        if one_or_two_genres[1] == " | ":
            # If we have one of the artists with songs in two genres, this gets us the songs in the second genre
            songs_and_artists_in_second_genre = all_genres_songs_and_artists[one_or_two_genres[2]]
            for song_with_tag in songs_and_artists_in_second_genre.keys():
                if proper_artist_name == songs_and_artists_in_second_genre[song_with_tag]:
                    songs_by_artist.append(song_with_tag)
        return songs_by_artist
    return 0
    # !play-artist ____ or !play-best-by ____ can do the tag sorting