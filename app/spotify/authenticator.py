# Spotify Authentication Module

import requests
from spotify import utils

# Constants
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Creates a header hash to send with requests to Spotify API, given an access token
def create_header(access_token):
    return {'Authorization': 'Bearer {}'.format(access_token)}

# Provides User with a login page and returns a url to open up user login dialog
def user_login_url(client_id, redirect_uri, scope, state):
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope,
        'state': state
    }
    return utils.construct_request_string(SPOTIFY_AUTH_URL, params)

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

# Uses refresh token to get new access codes
def refresh_access_credentials(refresh_token, client_id, client_secret):
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token, 
        'client_id': client_id, 
        'client_secret': client_secret
    }
    return requests.post(SPOTIFY_TOKEN_URL, data = params).json()