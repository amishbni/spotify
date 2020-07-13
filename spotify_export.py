import sys
import os
import spotipy.util as util
import pandas as pd
from spotipy import Spotify
from config import client_id, client_secret
from spotipy.oauth2 import SpotifyClientCredentials

def export(playlist_uri):
    offset = 0
    has_track = True

    columns = ["track_id", "name", "track_number", "album", "artists",
            "release_date", "release_date_precision",
            "duration_ms", "episode", "explicit", "popularity",
            "external_urls.spotify"]
    play_list = []
    while has_track:
        response = sp.playlist_tracks(
            playlist_uri,
            offset=offset
        )
        if response["items"]:
            for item in response["items"]:
                if item["track"]:
                    track_id = item["track"]["id"]
                    name = item["track"]["name"]
                    track_number = item["track"]["track_number"]
                    album = item["track"]["album"]["name"]
                    artists_list = []
                    for artist in item["track"]["artists"]:
                        artists_list.append(artist["name"])
                    artists = '; '.join(artists_list)
                    release_date = item["track"]["album"]["release_date"]
                    release_date_precision = item["track"]["album"]["release_date_precision"]
                    duration_ms = item["track"]["duration_ms"]
                    episode = item["track"]["episode"]
                    explicit = item["track"]["explicit"]
                    popularity = item["track"]["popularity"]
                    external_urls_spotify = item["track"]["external_urls"]["spotify"]
                    play_list.append([
                        track_id, name, track_number, album, artists,
                        release_date, release_date_precision,
                        duration_ms, episode, explicit, popularity,
                        external_urls_spotify
                    ])

        offset = offset + len(response['items'])
        has_track = len(response['items']) != 0

    print(len(play_list))
    playlist = pd.DataFrame(play_list, columns=columns)
    playlist.to_csv("playlist.csv")

if __name__ == "__main__":
    os.environ["SPOTIPY_CLIENT_ID"] = client_id
    os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
    os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8888/callback"

    sp = Spotify(client_credentials_manager=SpotifyClientCredentials())
    args = sys.argv
    if len(args) < 2:
        print("No playlist uri was specified.")
        exit(1)
    else:
        playlist_uri = args[1]
        export(playlist_uri)
