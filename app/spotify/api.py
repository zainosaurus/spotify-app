# Spotify API Module

import requests
from spotify import authenticator as auth
from spotify import utils
from spotify.decorators import verify_token_active

# Constants
SPOTIFY_BASE_URL = 'https://api.spotify.com/v1'

# Retrieves currently signed-in user's profile
# returns response object
# TODO return json instead of response (error handling for error messages)
@verify_token_active
def get_current_profile(access_token):
    url = utils.build_url([SPOTIFY_BASE_URL, 'me'])
    return requests.get(url, headers = auth.create_header(access_token)).json()

# Uses Spotify's Search Endpoint to search for a resource (finds first resource)
# param: query(string): search query
# param: type(string): comma-separated list of resource types to include
@verify_token_active
def search(access_token, query, _type, limit = 1):
    url = utils.build_url([SPOTIFY_BASE_URL, 'search'])
    params = dict(q = query, type = _type, limit = limit)
    return requests.get(url, headers = auth.create_header(access_token), params = params).json()

# Gets Audio Analysis information for a Track
# param: _id(string): Spotify ID for the track
@verify_token_active
def track_audio_analysis(access_token, _id):
    url = utils.build_url([SPOTIFY_BASE_URL, 'audio-analysis', _id])
    return requests.get(url, headers = auth.create_header(access_token)).json()

# Gets Audio Features for a track
# param: _id (string): Spotify ID for the track
@verify_token_active
def track_audio_features(access_token, _id):
    url = utils.build_url([SPOTIFY_BASE_URL, 'audio-features', _id])
    return requests.get(url, headers = auth.create_header(access_token)).json()