# Spotify API Module

import requests
from spotify import authenticator as auth

# Constants
SPOTIFY_BASE_URL = 'https://api.spotify.com/v1'

# Builds URL
def build_url(path):
    return '/'.join(path)

# Retrieves currently signed-in user's profile
# returns response object
# TODO return json instead of response (error handling for error messages)
def get_current_profile(access_token):
    url = build_url([SPOTIFY_BASE_URL, 'me'])
    return requests.get(url, headers = auth.create_header(access_token))

# Uses Spotify's Search Endpoint to search for a resource (finds first resource)
# param: query(string): search query
# param: type(string): comma-separated list of resource types to include
def search(access_token, query, _type, limit = 1):
    url = build_url([SPOTIFY_BASE_URL, 'search'])
    params = dict(q = query, type = _type, limit = limit)
    return requests.get(url, headers = auth.create_header(access_token), params = params)