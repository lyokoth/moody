import os
from dotenv import load_dotenv
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = os.getenv("redirect_uri")
scope = "user-library-read user-top-read playlist-modify-public user-follow-read"

def authenticate_spotify(token):
    return spotipy.Spotify(auth=token)

# Rest of your code goes here
