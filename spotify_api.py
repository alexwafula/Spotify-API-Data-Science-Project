import json
import urllib3
import requests

client_id = "b968ead753e94682a284992589175fc6"
my_id = "bwa07z52cw66zd3zad7qmmt8f"
token = "BQBnGq9QB1YwclJEVEfFp0zZnY0NJduDkUyy0DZMER6zj6ONWoA36RjM_W_-Xk7xwzd4LWLQ81DiXK5nBeKvJ5xE2NpyXWQxlbFfsv8NzFGG5FltQ319XytgiOz292BwUqscmQzmjPwQwXKPFTtsFwJqr066CqvXuRmIYJmVqqPCklDzozEwp7M6Ca1_m9PVj1M"

# From a category and the ID, a uri is generated
def generate_uri(category, id):
    return "spotify:" + category + ":" + id

def list_playlists_user(user_id):
    query = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)

    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )

    response_json = response.json()
    print("Total of playlists: " + str(response_json["total"]))
    print("-----------------------------")
    for x in response_json["items"]:
        print(x.keys())
    for i in range(response_json["total"]):
        print(i, response_json["items"][i]["name"], response_json["items"][i]["tracks"])

def list_tracks_playlist(playlist_id):
    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
    )
    response_json = response.json()

    total = response_json["total"]
    for i in response_json["items"][0]["track"]:
        print(i)
    
list_playlists_user(my_id)
list_tracks_playlist('17VqfYlGuKc8kmL8cAumGo')