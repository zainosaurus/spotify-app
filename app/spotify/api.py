# Spotify API Module

import requests

# Constants
SPOTIFY_BASE_URL = 'https://api.spotify.com/v1'

# Retrieves currently signed-in user's profile
def get_current_profile(access_token):
    url = "{}/me".format(SPOTIFY_BASE_URL)
    return requests.get(url, headers={'Authorization': 'Bearer {}'.format(access_token)})
