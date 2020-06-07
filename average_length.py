# Shows a user's playlists
import sys
from spotipy import Spotify
import os
import spotipy.util as util
from config import client_id, client_secret
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

def get_total_ms(playlist_uri):
    offset = 0
    total_ms = 0
    has_track = True

    while has_track:
        response = sp.playlist_tracks(
            playlist_uri,
            offset=offset,
            fields='items.track.duration_ms,total'
        )
        for item in response["items"]:
            total_ms += (item["track"]["duration_ms"])
        offset = offset + len(response['items'])

        has_track = len(response['items']) != 0
    return [total_ms, offset]

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
        result = get_total_ms(playlist_uri)
        average_minutes = (result[0] / result[1]) / 60000
        print(f"{average_minutes:.2f}")
