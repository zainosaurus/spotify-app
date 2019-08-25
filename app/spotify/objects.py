from spotify import api
from spotify import util

class Track:

    RESOURCE_TYPE = 'track'
    MAIN_KEYS = ['album', 'artists', 'duration_ms', 'id', 'name', 'popularity']

    @staticmethod
    def find(auth_token, search_query):
        track_data = api.search(auth_token, search_query, Track.RESOURCE_TYPE).json()
        if util.successful_request(track_data):
            return Track(auth_token, track_data['tracks']['items'][0])
        else:
            return None
    
    # Gets Audio Analysis for this track
    def get_audio_analysis(self):
        

    # Formats and returns important fields
    def get_simple_json(self):
        response = {key: self.data[key] for key in Track.MAIN_KEYS}
        response['artists'] = ', '.join(list(map(lambda x: x['name'], response['artists'])))
        response['album'] = response['album']['name']


    def __init__(self, auth_token, json_data):
        self._auth_token = auth_token
        self.data = json_data