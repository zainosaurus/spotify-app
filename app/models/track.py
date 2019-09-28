import spotify.api
import spotify.utils
import query_builder

class Track:
    """ Represents a Spotify Track Object """
    RESOURCE_TYPE = 'track'

    # List of keys to filter by when getting simple json
    TRACK_KEYS = ['name', 'album:name', 'artists', 'popularity', 'id']
    AUDIO_FEATURE_KEYS = ['danceability', 'energy', 'valence', 'tempo', 'loudness', 'acousticness', 'instrumentalness', 'liveness', 'speechiness']

    @staticmethod
    def find_by_query(auth_token, search_query):
        track_data = spotify.api.search(auth_token, search_query, Track.RESOURCE_TYPE)
        return Track(auth_token, track_data['tracks']['items'][0])
    
    @staticmethod
    def find_by_id(auth_token, _id):
        track_data = spotify.api.get_track(auth_token, _id)
        return Track(auth_token, track_data)
    
    # Filter data to only include keys of interest
    def filter_track_data(self):
        response = spotify.utils.filter_dict(self.track_info, Track.TRACK_KEYS)
        # Artists is a list of artist objects, convert to comma separated string of artist names
        response['artists'] = ', '.join(list(map(lambda x: x['name'], response['artists'])))
        # Include audio feature keys if audio features have been populated
        if self.audio_features:
            response.update({'audio_features': spotify.utils.filter_dict(self.audio_features, Track.AUDIO_FEATURE_KEYS)})
        return response
    
    # Gets Audio Analysis for this track
    def perform_audio_analysis(self):
        response = spotify.api.track_audio_features(self._auth_token, self.track_info['id'])
        self.audio_features = response
        
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

    # Gets a value
    def get_val(self, key):
        if key in list(self.to_simple_json().keys()):
            return self.to_simple_json()[key]
        elif key in self.AUDIO_FEATURE_KEYS:
            return self.to_simple_json()['audio_features'][key]


    def __init__(self, auth_token, track_json, features_json = None):
        self._auth_token = auth_token
        self.track_info = track_json
        self.audio_features = features_json


class SavedTrack(Track):
    """ Represents a Track saved in a user's library """
    def __init__(self, auth_token, saved_track_json, features_json = None):
        super().__init__(auth_token, saved_track_json.get('track'), features_json)
        self.added_at = saved_track_json.get('added_at')


class TrackCollection:
    """ Represents a Collection of Tracks (ex. Library or Playlist) """
    # Hits Spotify endpoint and returns list of SavedTrack objects
    # def get_library(self):
    #     track_list = spotify.api.get_saved_tracks(self._auth_token).get('saved_tracks')
    #     return list(map(lambda obj: SavedTrack(self._auth_token, obj), track_list))

    # Performs audio analysis for the songs in the collection
    def perform_audio_analysis(self):
        for i in range(0, len(self.saved_tracks), 100):
            # Getting batch of 100 tracks (max batch size for spotify's api)
            current_batch = self.saved_tracks[i : i+100]
            # Getting spotify ID's of batch
            spotify_ids = list(map(lambda x: x['spotify_id'], current_batch))
            # Sending request to API
            response_objects = spotify.api.batch_audio_features(self._auth_token, spotify_ids)
            # Updating track objects with info
            for i in range(len(response_objects))

    # Filters the library based on a query (returns list of SavedTracks that match the query)
    def filter_by_query(self, query):
        filtered_tracks = []
        query_func = query_builder.build_query(query)
        for track in self.saved_tracks:
            print('Processing ' + track.to_simple_json()['name'])
            track.perform_audio_analysis()
            arg_strings = query_builder.operands(query)
            arg_vals = []
            for el in arg_strings:
                try:
                    arg_vals.append(float(el))
                except ValueError:
                    arg_vals.append(track.get_val(el))
            if query_func(*arg_vals):
                filtered_tracks.append(track)
        return filtered_tracks

    def __init__(self, auth_token, track_list):
        self._auth_token = auth_token
        self.saved_tracks = track_list