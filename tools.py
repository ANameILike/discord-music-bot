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

print(get_artist_stats(all_genres_songs_and_artists).head(50))

