import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


client_id = "fd3d8b8ab8ec4f6481c73e02c51adbf3"
client_secret = "d362908c17c142058b35c61e348949d8"

# Authenticate your request to the Spotify API using your client ID and client secret
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

tracks = pd.read_csv('/Users/tariqgeorges/Documents/Riq Coding/result.csv')
# Filter out tracks with a popularity score below 70
tracks = tracks[tracks.popularity > 70]


# Get input from the user in the form of comma-separated track IDs
ids = input('Enter comma-separated IDs of your favorite songs:\nSample input: 7ytR5pFWmSjzHJIeQkgog4,079Ey5uxL04AKPQgVQwx5h\n\n\n')
# song_names = input('Enter a song titile and artist name in the format (Fair Trade - Drake)')

# ids = '40iJIUlhi6renaREYGeIDS,5N9oDpshl2kfazjIwjNpCQ,6GNG0YQixWuLE0M5FtrRxY,1wNdaSWQHqXTlwFYiORqdg,40mjsnRjCpycdUw3xhS20g'
# Convert the input IDs into a list
ids_list = ids.strip().split(',')
# song_names_list = song_names.strip().split('-')

# Use the Spotify API to retrieve information about the user's favorite tracks
favorites = []
for track_id in ids_list:
    track_info = sp.track(track_id)
    favorites.append(track_info)

# Create a DataFrame to hold information about the user's favorite tracks
# favorites_df = pd.DataFrame(favorites, columns=['id', 'name', 'artists'])

favorites_df = pd.DataFrame(favorites)

# Extract the artist IDs from the DataFrame
artist_ids = favorites_df.artists.apply(lambda x: x[0]['id']).tolist()

# Use the Spotify API to retrieve information about the user's favorite artists
favorite_artists = []
for artist_id in artist_ids:
    artist_info = sp.artist(artist_id)
    favorite_artists.append(artist_info)


# Create a DataFrame to hold information about the user's favorite artists
favorite_artists_df = pd.DataFrame(favorite_artists, columns=['id', 'name', 'genres'])

# Extract the top genre for each artist and add it to the DataFrame
favorite_artists_df['top_genre'] = favorite_artists_df.genres.apply(lambda x: x[0] if x else '')

# print(f'Top Genres are: \n\n {favorite_artists_df["top_genre"]}')

# Merge the track and artist information into a single DataFrame
# print(f'Favorites_df is: \n{favorites_df}')
# print('\n\n')
# print(f'Favorite_artists_df is: \n{favorite_artists_df}')
favorites_df = pd.concat([favorites_df, favorite_artists_df], axis=1)



# Determine the user's favorite cluster based on the top genre of their favorite artists 
clusters = favorites_df.top_genre.value_counts()
if not clusters.empty:
    user_favorite_cluster = clusters.index[0]
    print('\nFavorite cluster:', user_favorite_cluster, '\n')

    # Get suggestions for tracks in the user's favorite cluster using the Spotify API
    suggestions = []
    results = sp.search(q=user_favorite_cluster, type='track', limit=50)
    for track in results['tracks']['items']:
        track_info = {
            'id': track['id'],
            'name': track['name'],
            'artists': ', '.join([artist['name'] for artist in track['artists']])
        }
        suggestions.append(track_info)

    # Create a DataFrame to hold the suggestions
    suggestions_df = pd.DataFrame(suggestions, columns=['artists', 'name', 'id'])

    print(suggestions_df.head())
else:
    print('No clusters found')




#_______________________________________________________
# clusters = favorites_df.top_genre.value_counts()
# user_favorite_cluster = clusters.index[0]

# print('\nFavorite cluster:', user_favorite_cluster, '\n')

# # Get suggestions for tracks in the user's favorite cluster using the Spotify API
# suggestions = []
# results = sp.search(q=user_favorite_cluster, type='track', limit=50)
# for track in results['tracks']['items']:
#     track_info = {
#         'id': track['id'],
#         'name': track['name'],
#         'artists': ', '.join([artist['name'] for artist in track['artists']])
#     }
#     suggestions.append(track_info)

# # Create a DataFrame to hold the suggestions
# suggestions_df = pd.DataFrame(suggestions, columns=['id', 'name', 'artists'])

# print(suggestions_df.head())