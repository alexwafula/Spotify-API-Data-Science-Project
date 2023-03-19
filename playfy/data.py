# Imports
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import cred
import datetime
import pandas as pd
from collections import Counter
from itertools import chain
import numpy as np

# Authetication

client_credentials_manager = SpotifyClientCredentials(client_id= cred.client_id, client_secret= cred.client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Functions

def get_id_playlist(playlist_link):
    """Gets Playlist's Id

    Parameters
    ----------
    playlist_link : str
        Playlist's link

    Returns
    -------
    int
        Playlist's Id Number
    """
    
    return playlist_link.split("/")[-1].split('?')[0]

def generate_uri(category, id):
    """Generates URI for playlist

    Parameters
    ----------
    category : str
        Category of what is going to be get
    id : int
        Playlist's Id

    Returns
    -------
    int
        Playlist's Id Number
    """
    return "spotify:" + category + ":" + id

def playlist_info(playlist_link):
    """Gets the main information of a playlist

    Parameters
    ----------
    playlist_link : str
        Playlist's link

    Returns
    -------
    dict
        Info of the playlist: cover, name, description and owner
    """

    playlist = sp.playlist(get_id_playlist(playlist_link))
    info = {
        'cover': sp.playlist_cover_image(get_id_playlist(playlist_link))[0]['url'],
        'name': playlist["name"],
        'description': playlist["description"],
        'owner': playlist["owner"]["display_name"] # Other information of the owner also available
    }
    return info

def create_playlist_df(playlist_link):
    """Create a Pandas DataFrame from the tracks informations

    Parameters
    ----------
    playlist_link : str
        Playlist's link

    Returns
    -------
    DataFrame
        Pandas DataFrame with tracks information
    """

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

def top_artists_playlist(playlist_df):
    """Gets top 5 artists with most tracks apperances on a playlist

    Parameters
    ----------
    playlist_df : DataFrame
        Playlist DataFrame with tracks infos

    Returns
    -------
    DataFrame
        DataFrame with top 5 artists (appearances and their % in the whole playlist)
    """

    artists = playlist_df['artist(s)']
    series_top = pd.DataFrame.from_dict(Counter(map(str.strip, chain.from_iterable(artists.str.split(',')))),
                             orient='index').squeeze()
    
    series_top = series_top.sort_values(ascending=False)[0:5]
    
    percentage = np.around(100*series_top.values/len(playlist_df), decimals=2)

    percentage_2 = []
    for i in percentage:
        percentage_2.append(str(i) + '%')
    
    df_top = pd.DataFrame({'artist':series_top.keys(), 'appearances': series_top.values, '% of all': percentage_2})

    return df_top

def all_top_artists(playlist_df):
    """Gets all artists and their appearances

    Parameters
    ----------
    playlist_df : DataFrame
        Playlist DataFrame with tracks infos

    Returns
    -------
    DataFrame
        DataFrame with artists infos (appearances and their % in the whole playlist)
    """

    artists = playlist_df['artist(s)']
    series_top = pd.DataFrame.from_dict(Counter(map(str.strip, chain.from_iterable(artists.str.split(',')))),
                             orient='index').squeeze()
    
    series_top = series_top.sort_values(ascending=False)
    
    percentage = np.around(100*series_top.values/len(playlist_df), decimals=2)
    
    df_top = pd.DataFrame({'artist':series_top.keys(), 'appearances': series_top.values, '% of all': percentage})

    return df_top

def top_albums_playlist(playlist_df):
    """Gets top 5 albums with most tracks apperances on a playlist

    Parameters
    ----------
    playlist_df : DataFrame
        Playlist DataFrame with tracks infos

    Returns
    -------
    DataFrame
        DataFrame with top 5 albums (appearances and their % in the whole playlist)
    """

    df_top = playlist_df.groupby(['album'])['album'].count().sort_values(ascending=False)[0:5]
    
    percentage = np.around(100*df_top.values/len(playlist_df), decimals=2)
    
    percentage_2 = []
    for i in percentage:
        percentage_2.append(str(i) + '%')
    
    df_top = pd.DataFrame({'album':df_top.keys(), 'appearances': df_top.values, '% of all': percentage_2})
    
    return df_top

def all_albums_playlist(playlist_df):
    """Gets all albums and their appearances

    Parameters
    ----------
    playlist_df : DataFrame
        Playlist DataFrame with tracks infos

    Returns
    -------
    DataFrame
        DataFrame with albums infos (appearances and their % in the whole playlist)
    """

    return playlist_df.groupby(['album'])['album'].count().sort_values(ascending=False)

def most_popular_track(playlist_df):
    """Gets the most popular track in a playlist

    Parameters
    ----------
    playlist_df : DataFrame
        Playlist DataFrame with tracks infos

    Returns
    -------
    DataFrame
        Infos for the most popular track in the playlist
    """

    return playlist_df.iloc[playlist_df["popularity"].idxmax()]

def longest_track(playlist_df):
    """Gets the longest track in a playlist

    Parameters
    ----------
    playlist_df : DataFrame
        Playlist DataFrame with tracks infos

    Returns
    -------
    DataFrame
        Infos for the longest track in the playlist
    """

    return playlist_df.iloc[playlist_df["duration"].idxmax()]

def shortest_track(playlist_df):
    """Gets the shortest track in a playlist

    Parameters
    ----------
    playlist_df : DataFrame
        Playlist DataFrame with tracks infos

    Returns
    -------
    DataFrame
        Infos for the shortest track in the playlist
    """

    return playlist_df.iloc[playlist_df["duration"].idxmin()]