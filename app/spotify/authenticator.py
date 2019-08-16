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

# Provides User with a login page and returns a url to open up user login dialog
def user_login_url(client_id, redirect_uri, scope, state):
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope,
        'state': state
    }
    return construct_request_string(SPOTIFY_AUTH_URL, params)

# Returns access and refresh tokens given an authorization code
def get_access_credentials(authorization_code, redirect_uri, client_id, client_secret):
    params = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    return requests.post(SPOTIFY_TOKEN_URL, data = params).json()