import os 




# Client Keys

CLIENT_ID = "0d8f5422a14a449ead12264e25bee53d"
CLIENT_SECRET = "4f412baacf44480e9f1c521738a863e2"
redirect_uri = 'http://localhost:6543/callback'

SCOPE='user-read-playback-state user-read-currently-playing playlist-manage-public user-top-read'


# Spotify URL
SPOTIFY_AUTH_URL='https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL='https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL='https://api.spotify.com'
API_VERSION='v1'
SPOTIFY_API_URL='{}/{}'.format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL='http://localhost/'

auth_query_parameters = {
    'response_type': 'code',
    'redirect_uri': redirect_uri,
    'scope': SCOPE,
    'client_id': CLIENT_ID
}