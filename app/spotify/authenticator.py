# Spotify Authentication Module
import requests

# Constants
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Constructs a get request string given a dict of params and a base url
def construct_request_string(base_url, params):
    string = "{}?".format(base_url)
    params_arr = []
    for key, value in params.items():
        params_arr.append("{}={}".format(key, value.replace(' ', '%20')))
    string += '&'.join(params_arr)
    return string

# Provides User with a login page and returns an access code
def user_login_url(client_id, redirect_uri, scope, state):
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope,
        'state': state
    }
    return construct_request_string(SPOTIFY_AUTH_URL, params)