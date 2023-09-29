# Displays duplicate items in a list and returns a new list with duplicates removed, preserving the first instance.
def remove_dupes(list_with_dupes):
    duped_values = []
    temporarily_alphabetized = sorted(list_with_dupes)
    for i in range(len(temporarily_alphabetized) - 1):
        if temporarily_alphabetized[i] == temporarily_alphabetized[i+1]:
            duped_values.append(temporarily_alphabetized[i])
    reversed_original = list_with_dupes[::-1]
    for duped_value in duped_values:
        reversed_original.remove(duped_value)
    list_of_uniques = reversed_original[::-1]
    print(f"Duplicates: {duped_values}")
    return list_of_uniques

# Just to check if I have any overlapping song names
from MusicBotMetadata import all_song_names
remove_dupes(all_song_names)


# Displays a list of artists with their song counts, sorted in descending order
import pandas as pd
from MusicBotMetadata import all_genres_songs_and_artists
def get_artist_stats(song_artist_dict_within_genre_dict):
    master_redundant_artists_list = []
    songs_and_artists_dicts = song_artist_dict_within_genre_dict.values()
    for songs_and_artists_dict in songs_and_artists_dicts:
        redundant_list_of_artists_in_this_genre = list(songs_and_artists_dict.values())
        master_redundant_artists_list += redundant_list_of_artists_in_this_genre
    pandas_dataframe = pd.DataFrame({"Artist": pd.Categorical(master_redundant_artists_list), "Count": 1})
    grouped_by_artist = pandas_dataframe.groupby("Artist").count()
    sorted_by_count = grouped_by_artist.sort_values(by=["Count"], ascending=False)
    return sorted_by_count

pd.set_option("display.max_rows", None)
print(get_artist_stats(all_genres_songs_and_artists))




# Display a list of every song name containing a specified string
def search_within_songs(song_list, search_term):
    search_results = [song for song in song_list if search_term in song]
    for result in search_results:
        print(result)
    return "done"

search_within_songs(all_song_names, "Feat.")



# This one's going to check song names against album names and print out the dupes
def get_song_album_name_overlaps(song_list, album_list):
    intersection = set(song_list).intersection(album_list)
    print(intersection)

from MusicBotMetadata import all_album_names
get_song_album_name_overlaps(all_song_names, all_album_names)