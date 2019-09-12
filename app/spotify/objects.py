from spotify import api
from spotify import utils

# Represents a Track Object
class Track:

    RESOURCE_TYPE = 'track'

    # List of keys to filter by when getting simple json
    TRACK_KEYS = ['name', 'album:name', 'artists', 'popularity', 'id']
    AUDIO_FEATURE_KEYS = ['danceability', 'energy', 'valence', 'tempo', 'loudness', 'acousticness', 'instrumentalness', 'liveness', 'speechiness']

    @staticmethod
    def find_by_query(auth_token, search_query):
        track_data = api.search(auth_token, search_query, Track.RESOURCE_TYPE)
        if utils.successful_request(track_data):
            print(track_data.keys())
            return Track(auth_token, track_data['tracks']['items'][0])
        else:
            return None
    
    @staticmethod
    def find_by_id(auth_token, _id):
        track_data = api.get_track(auth_token, _id)
        if utils.successful_request(track_data):
            return Track(auth_token, track_data)
        else:
            return None
    
    # Filter data to only include keys of interest
    def filter_track_data(self):
        response = utils.filter_dict(self.track_info, Track.TRACK_KEYS)
        # Artists is a list of artist objects, convert to comma separated string of artist names
        response['artists'] = ', '.join(list(map(lambda x: x['name'], response['artists'])))
        # Include audio feature keys if audio features have been populated
        if self.audio_features:
            response.update({'audio_features': utils.filter_dict(self.audio_features, Track.AUDIO_FEATURE_KEYS)})
        return response
    
    # Gets Audio Analysis for this track
    def perform_audio_analysis(self):
        response = api.track_audio_features(self._auth_token, self.track_info['id'])
        if utils.successful_request(response):
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


# Represents a Profile Object
class Profile:
    def get_name(self):
        return self.profile_info.get('display_name')
    
    def get_email(self):
        return self.profile_info.get('email')
    
    def get_country(self):
        return self.profile_info.get('country')
    
    def get_follower_count(self):
        try:
            return self.profile_info.get('followers').get('total')
        except:
            return None
    
    def get_image_url(self):
        try:
            return self.profile_info.get('images')[0].get('url')
        except:
            return None
    
    def get_image_height(self):
        try:
            return self.profile_info.get('images')[0].get('height') or 200
        except:
            return 200 # default height
    
    def get_image_width(self):
        try:
            return self.profile_info.get('images')[0].get('width') or 300
        except:
            return 300 # default width

    # Gets user profile associated with auth token
    def load_profile_info(self):
        return api.get_current_profile(self._auth_token)

    def __init__(self, auth_token):
        self._auth_token = auth_token
        self.profile_info = self.load_profile_info()

# Represents a Track saved in a user's library
class SavedTrack(Track):

    @staticmethod
    def get_saved_track_list(auth_token):
        track_list = api.get_saved_tracks(auth_token).get('saved_tracks')
        return list(map(lambda obj: SavedTrack(auth_token, obj), track_list))

    def __init__(self, auth_token, saved_track_json, features_json = None):
        super().__init__(auth_token, saved_track_json.get('track'), features_json)
        self.added_at = saved_track_json.get('added_at')
