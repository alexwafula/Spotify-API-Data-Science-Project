# Imports and authetication
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import cred
import datetime
import pandas as pd
from collections import Counter
from itertools import chain
import numpy as np

# Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id= cred.client_id, client_secret= cred.client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Functions

# From a playlist link, this function return its URI
def get_id_playlist(playlist_link):
    return playlist_link.split("/")[-1].split('?')[0]

# From a category and ID, an URI is generated
def generate_uri(category, id):
    return "spotify:" + category + ":" + id

# From a playlist link, get the main information of the playlist
def playlist_info(playlist_link):
    playlist = sp.playlist(get_id_playlist(playlist_link))
    info = {
        'cover': sp.playlist_cover_image(get_id_playlist(playlist_link))[0]['url'],
        'name': playlist["name"],
        'description': playlist["description"],
        'owner': playlist["owner"]["display_name"] # Other information of the owner also available
    }
    return info

# From a playlist link, creates a Pandas DataFrame with the tracks information
def create_playlist_df(playlist_link):
    playlist_id = get_id_playlist(playlist_link)
        
    tracks = sp.playlist_tracks(playlist_id)
    
    tracks_playlist = []
    
    while True:    
        for track in tracks["items"]:
            t_id = track["track"]["id"]
            name = track["track"]["name"]
            album = track["track"]["album"]["name"]
            duration = datetime.timedelta(seconds=int(track["track"]["duration_ms"]/1000))
            popularity = track["track"]["popularity"]

            artist = ""
            for i in range(len(track["track"]["artists"])):
                name_artist = track["track"]["artists"][i]["name"]
                if artist == "":
                    artist = name_artist
                else:
                    artist = artist + ", " + name_artist
            
            artist_album = ""
            for i in range(len(track["track"]["album"]["artists"])):
                name_artist = track["track"]["album"]["artists"][i]["name"]
                if artist_album == "":
                    artist_album = name_artist
                else:
                    artist_album = artist_album + ", " + name_artist

            track_info = {
                'id': t_id,
                'name': name,
                'album': album,
                'duration': duration,
                'popularity': popularity,
                'artist(s)': artist,
                'album_artist(s)': artist_album
            }
            tracks_playlist.append(track_info)
        if tracks["next"]:
            tracks = sp.next(tracks)
        else:
            break
        
    return pd.DataFrame(tracks_playlist)

# Return top 5 artists with most tracks apperances on a playlist
def top_artists_playlist(playlist_df):
    artists = playlist_df['artist(s)']
    series_top = pd.DataFrame.from_dict(Counter(map(str.strip, chain.from_iterable(artists.str.split(',')))),
                             orient='index').squeeze()
    
    series_top = series_top.sort_values(ascending=False)[0:5]
    
    percentage = np.around(100*series_top.values/len(playlist_df), decimals=2)
    
    df_top = pd.DataFrame({'artist':series_top.keys(), 'appearances': series_top.values, '% of all': percentage})

    return df_top

# Return top 5 albums with most tracks apperances on a playlist
def top_albums_playlist(playlist_df):
    return playlist_df.groupby(['album'])['album'].count().sort_values(ascending=False)[0:5]

# Return the track with most popularity (0 to 100)
def most_popular_track(playlist_df):
    return playlist_df.iloc[playlist_df["popularity"].idxmax()]

# Return track with most duration on the playlist
def longest_track(playlist_df):
    return playlist_df.iloc[playlist_df["duration"].idxmax()]

# Return track with most duration on the playlist
def shortest_track(playlist_df):
    return playlist_df.iloc[playlist_df["duration"].idxmin()]