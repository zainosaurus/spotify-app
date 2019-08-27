from spotify import api
from spotify import util

class Track:

    RESOURCE_TYPE = 'track'

    # List of keys to filter by when getting simple json
    TRACK_KEYS = ['name', 'album:name', 'artists', 'popularity']
    AUDIO_FEATURE_KEYS = ['danceability', 'energy', 'valence', 'tempo', 'loudness', 'acousticness', 'instrumentalness', 'liveness', 'speechiness']

    @staticmethod
    def find(auth_token, search_query):
        track_data = api.search(auth_token, search_query, Track.RESOURCE_TYPE)
        if util.successful_request(track_data):
            return Track(auth_token, track_data['tracks']['items'][0])
        else:
            return None
    
    # Filter data to only include keys of interest
    def filter_track_data(self):
        response = util.filter_dict(self.track_info, Track.TRACK_KEYS)
        # Artists is a list of artist objects, convert to comma separated string of artist names
        response['artists'] = ', '.join(list(map(lambda x: x['name'], response['artists'])))
        # Include audio feature keys if audio features have been populated
        if self.audio_features:
            response.update({'audio_features': util.filter_dict(self.audio_features, Track.AUDIO_FEATURE_KEYS)})
        return response
    
    # Gets Audio Analysis for this track
    def perform_audio_analysis(self):
        response = api.track_audio_features(self._auth_token, self.track_info['id'])
        if util.successful_request(response):
            self.audio_features = response
            return True
        return False
        
    # Formats and returns important fields
    def to_simple_json(self):
        return self.filter_track_data()
    
    # Returns values to plot
    #   danceability, energy, valence
    def data_points(self):
        labels = ['danceability', 'energy', 'valence', 'instrumentalness', 'speechiness', 'acousticness']
        data = []
        for label in labels:
            data.append(self.audio_features[label])
        return {'labels': labels, 'data': data}


    def __init__(self, auth_token, track_json, features_json = None):
        self._auth_token = auth_token
        self.track_info = track_json
        self.audio_features = features_json
