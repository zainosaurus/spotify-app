# Spotify API Module

import requests
from spotify import authenticator as auth
from spotify import utils
from spotify.decorators import validate_token

# Constants
SPOTIFY_BASE_URL = 'https://api.spotify.com/v1'

# Retrieves currently signed-in user's profile
# returns response object
# TODO return json instead of response (error handling for error messages)
@validate_token
def get_current_profile(access_token):
    url = utils.build_url(SPOTIFY_BASE_URL, 'me')
    return requests.get(url, headers = auth.create_header(access_token)).json()

# Uses Spotify's Search Endpoint to search for a resource (finds first resource)
# param: query(string): search query
# param: type(string): comma-separated list of resource types to include
@validate_token
def search(access_token, query, _type, limit = 1):
    url = utils.build_url(SPOTIFY_BASE_URL, 'search')
    params = dict(q = query, type = _type, limit = limit)
    return requests.get(url, headers = auth.create_header(access_token), params = params).json()

# Retrieves a track by it's Spotify ID
# param: id(string): Spotify ID of the track
@validate_token
def get_track(access_token, _id):
    url = utils.build_url(SPOTIFY_BASE_URL, 'tracks', _id)
    return requests.get(url, headers = auth.create_header(access_token)).json()

# Gets Audio Analysis information for a Track
# param: _id(string): Spotify ID for the track
@validate_token
def track_audio_analysis(access_token, _id):
    url = utils.build_url(SPOTIFY_BASE_URL, 'audio-analysis', _id)
    return requests.get(url, headers = auth.create_header(access_token)).json()

# Gets Audio Features for a track
# param: _id (string): Spotify ID for the track
@validate_token
def track_audio_features(access_token, _id):
    url = utils.build_url(SPOTIFY_BASE_URL, 'audio-features', _id)
    return requests.get(url, headers = auth.create_header(access_token)).json()

# Gets Audio Features for a multiple tracks
# param: ids (string): Spotify IDs for the track (note that max. 100 at a time is allowed by spotify)
@validate_token
def batch_audio_features(access_token, ids):
    url = utils.build_url(SPOTIFY_BASE_URL, 'audio-features')
    params = {'ids': ','.join(ids)}
    return requests.get(url, headers = auth.create_header(access_token), params = params).json()

# Gets all songs in the user's library
@validate_token
def get_saved_tracks(access_token):
    saved_tracks = []
    url = utils.build_url(SPOTIFY_BASE_URL, 'me', 'tracks')
    while url is not None:
        track_page = requests.get(url, headers = auth.create_header(access_token), params = dict(limit=50)).json()
        saved_tracks += track_page['items']
        url = track_page['next']
    return {'saved_tracks': saved_tracks}