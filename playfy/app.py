# Set-ExecutionPolicy Unrestricted -Scope Process

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import data
import plotly.express as px

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Lato:wght@700&display=swap",
        "rel": "stylesheet",
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title= "PlayFy: Stats of your Playlists!"

app.layout = html.Div([
    html.Div(
        children=[
            html.H1(
                children="PlayFy",
                style={'font-family': 'Lato'},
                className="header-title",
            ),
            html.P(
                children="See interesting stats of your public playlists",
                style={'font-family': 'Lato'},
                className="header-description",
            ),
            html.Div([
                html.P(
                    "Playlist link: ",
                    style={'color': 'white'}
                ),
                dcc.Input(
                    id='playlist_link',
                    type='text',
                    value='https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=ae129e2bc3ee4f01',
                    className="link", 
                ),
            ],
            className="header-link",),
            html.Div(
                children=[
                    html.Img(
                        id='playlist_cover',
                        className="cover"
                    ),
                    html.Span(
                        id='playlist_name',
                        className="playlist-name",
                    ),
                    html.Span(
                        id='playlist_owner',
                        className="playlist-owner",
                    ),
            ],
            className="playlist-info",),
    ],
    className="header",),

    html.Div(
        children=[
            dcc.Graph(id='top_artists'),
            dcc.Graph(id='top_albums'),
        ],
    className="body",),
    
], style={"overflow-x:": 'hidden'},)

@app.callback(
    Output('playlist_cover', 'src'),
    Output('playlist_name', 'children'),
    Output('playlist_owner', 'children'),
    Output('top_artists', 'figure'),
    Output('top_albums', 'figure'),
    Input(component_id='playlist_link', component_property='value')
)
def playlist_df(link):
    # Datasets being created according to the playlist link
    playlist = data.create_playlist_df(link)
    top_artists = data.top_artists_playlist(playlist)
    top_albums = data.top_albums_playlist(playlist)
    playlist_cover = data.playlist_info(link)['cover']
    playlist_name = data.playlist_info(link)['name']
    playlist_owner = data.playlist_info(link)['owner']

    # Figure Top Artists
    fig_art = px.bar(top_artists, x='artist', y='appearances')

    # Figure Top Albums
    fig_alb = px.bar(x=top_albums.keys(), y=top_albums.values)

    return playlist_cover, playlist_name, playlist_owner, fig_art, fig_alb

if __name__ == "__main__":
    app.run_server(debug=True)