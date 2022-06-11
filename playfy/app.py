import dash
from dash import dcc, html, Input, Output
import pandas as pd
import data
import plotly.express as px

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            children="PlayFy",
        ),
        html.P(
            children="See interesting stats of your playlist",
        ),
        html.Div([
            "Playlist link: ",
            dcc.Input(id='playlist_link', type='text')
        ]),
        dcc.Graph(id='top_artists'),
        dcc.Graph(id='top_albums'),
    ]
)

@app.callback(
    Output('top_artists', 'figure'),
    Output('top_albums', 'figure'),
    Output('popular', '')
    Input(component_id='playlist_link', component_property='value')
)
def playlist_df(link):
    # Datasets being created according to the playlist link
    playlist = data.create_playlist_df(link)
    top_artists = data.top_artists_playlist(playlist)
    top_albums = data.top_albums_playlist(playlist)

    # Figure Top Artists
    fig_art = px.bar(top_artists, x='artist', y='appearances')

    # Figure Top Albums
    fig_alb = px.bar(x=top_albums.keys(), y=top_albums.values)

    return fig_art, fig_alb

if __name__ == "__main__":
    app.run_server(debug=True)