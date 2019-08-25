# Spotify API Module

import requests
from spotify import authenticator as auth
from spotify import util

# Constants
SPOTIFY_BASE_URL = 'https://api.spotify.com/v1'

# Retrieves currently signed-in user's profile
# returns response object
# TODO return json instead of response (error handling for error messages)
def get_current_profile(access_token):
    url = util.build_url([SPOTIFY_BASE_URL, 'me'])
    return requests.get(url, headers = auth.create_header(access_token))

# Uses Spotify's Search Endpoint to search for a resource (finds first resource)
# param: query(string): search query
# param: type(string): comma-separated list of resource types to include
def search(access_token, query, _type, limit = 1):
    url = util.build_url([SPOTIFY_BASE_URL, 'search'])
    params = dict(q = query, type = _type, limit = limit)
    return requests.get(url, headers = auth.create_header(access_token), params = params)

# Gets Audio Analysis information for a Track
# param: _id(string): Spotify ID for the track
def track_audio_analysis(access_token, _id):
    url = util.build_url([SPOTIFY_BASE_URL, 'audio-analysis', _id])
    return requests.get(url, headers = auth.create_header(access_token))

# Gets Audio Features for a track
# param: _id (string): Spotify ID for the track
def track_audio_features(access_token, _id):
    url = util.build_url([SPOTIFY_BASE_URL, 'audio-features', _id])
    return requests.get(url, headers = auth.create_header(access_token))