import json 
import requests
import sys 
import base64
import urllib.parse 
from  urllib.parse import quote
from keys import CLIENT_ID, CLIENT_SECRET, redirect_uri
from settings import *
from flask import request, flash, session, current_app, url_for, redirect
from model import User, Track, Playlist, PlaylistTrack, db, connect_to_db


SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'



auth_query_parameters = {
    'CLIENT_ID' : CLIENT_ID,
    'response_type' : 'code',
    'redirect_uri' : 'http://localhost:6543/callback',
    'scope': 'user-top-read user-follow-read playlist-modify-public streaming user-read-birthdate user-read-email user-read-private'
}

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


## server side 
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = "6543"
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()



def get_user_auth():
    auth_url = "https://accounts.spotify.com/authorize"
    client_id = CLIENT_ID
    redirect_uri = redirect_uri
    scope = "user-read-playback-state user-modify-playback-state playlist-read-private playlist-modify-private playlist-modify-public user-read-recently-played user-library-modify user-library-read"
    auth_params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope,
    }
    auth_url = f"{auth_url}?{urllib.parse.urlencode(auth_params)}"

    return redirect(auth_url)

def get_tokens():
    """ Return authorization tokens from Spotify """


    # Request refresh and access tokens
    auth_token = request.args['code']

    code_payload = {
        'grant_type': 'authorization_code',
        'code': str(auth_token),
        'redirect_uri': redirect_uri
    }

    base64encoded = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('ascii'))
    headers = {'Authorization': 'Basic {}'.format(base64encoded.decode('ascii'))}

    try: 
        post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    except: 

        current_app.logger.error("Spotify client failed")
        raise 

    else: 
         response_data = post_request.json()
         return response_data
    

        