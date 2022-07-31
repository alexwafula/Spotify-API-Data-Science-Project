# Set-ExecutionPolicy Unrestricted -Scope Process

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import data
import plotly.express as px
import plotly.graph_objects as go

from io import BytesIO

from wordcloud import WordCloud
import base64

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
            ],
            className="playlist-info",),
    ],
    className="header",),

    html.Div(
        children=[
            dcc.Graph(id='top_artists'),
            html.Img(id='wc_artists', className='align-self-center'),
            dcc.Graph(id='top_albums'),
            html.Img(id='wc_albums', className = 'align-self-center'),
        ],
    className="body",),
    
], style={"overflow-x:": 'hidden'},)

def plot_wordcloud(data, op):
    if(op == 'artists'):
        d = dict(zip(data['artist'].tolist(), data['appearances'].tolist()))
    else:
        d = dict(zip(data.keys().tolist(), data.values.tolist()))

    wc = WordCloud(background_color='white', width=480, height=360)
    wc.fit_words(d)
    return wc.to_image()

@app.callback(
    Output('playlist_cover', 'src'),
    Output('top_artists', 'figure'),
    Output('wc_artists', 'src'),
    Output('top_albums', 'figure'),
    Output('wc_albums', 'src'),
    Input(component_id='playlist_link', component_property='value'),
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
    fig_art = go.Figure(data=[go.Bar(
        x=top_artists['artist'], y=top_artists['appearances'],
        text=top_artists['% of all'],
        textposition='inside'
    )])

    # WordCloud Top Artists
    img_art = BytesIO()
    plot_wordcloud(data=data.all_top_artists(playlist), op='artists').save(img_art, format='PNG')
    artists_wc = 'data:img_art/png;base64,{}'.format(base64.b64encode(img_art.getvalue()).decode())

    # Figure Top Albums
    fig_alb = go.Figure(data=[go.Bar(
        x=top_albums['album'], y=top_albums['appearances'],
        text=top_albums['% of all'],
        textposition='inside'
    )])

    # WordCloud Top Artists
    img_alb = BytesIO()
    plot_wordcloud(data=data.all_albums_playlist(playlist), op='albums').save(img_alb, format='PNG')
    albums_wc = 'data:img_alb/png;base64,{}'.format(base64.b64encode(img_alb.getvalue()).decode())

    return playlist_cover, fig_art, artists_wc, fig_alb, albums_wc

if __name__ == "__main__":
    app.run_server(debug=True)