from dbtools.google_cloud import FirestoreRecord
import time
import spotify.authenticator    # to refresh token when required
import os   # [temp] used to access env variables when refreshing token    TODO pass env vars as params
from models import TrackCollection, Profile, SavedTrack 

# Class to represent a User - Inherits from FirestoreRecord
class User(FirestoreRecord):
    # Collection Name
    COLLECTION_NAME = 'users'

    # Saves Spotify Authentication Info
    def save_access_credentials(self, credentials):
        self.params.update({
            'access_token': credentials.get('access_token'),
            'refresh_token': credentials.get('refresh_token'),
            'permissions': credentials.get('scope'),
            'token_valid_for': credentials.get('expires_in'),
            'last_refresh_at': time.time()
        })
        self.save()

    # Updates access credentials (when token is refreshed)
    def update_access_credentials(self, credentials):
        self.params.update({
            'access_token': credentials.get('access_token'),
            'token_valid_for': credentials.get('expires_in'),
            'last_refresh_at': time.time()
        })
        self.save()

    # Accessor for refresh token
    def get_refresh_token(self):
        return self.params.get('refresh_token')
    
    # Sends request to refresh access token when expired
    def refresh_access_token(self):
        response = spotify.authenticator.refresh_access_credentials(
            self.get_refresh_token(),
            os.environ['SPOTIFY_CLIENT_ID'],
            os.environ['SPOTIFY_CLIENT_SECRET']
        )
        self.update_access_credentials(response)

    # Checks if access token has expired
    def token_expired(self):
        current_time = time.time()  # time in seconds
        time_issued = self.params.get('last_refresh_at')
        time_valid = self.params.get('token_valid_for')
        return (current_time - time_issued) > time_valid

    # Gets a valid access token to use
    def get_access_token(self):
        if self.token_expired():
            self.refresh_access_token()
        return self.params.get('access_token')

    # Accessor for ID
    #   Required by flask-login
    def get_id(self):
        return self.id
    
    # Retrieves user's profile
    #   Returns a Profile Object
    def get_profile(self):
        return Profile(self.get_access_token())
    
    # Gets User's Library
    #   Hits Spotify endpoint and returns list of SavedTrack objects
    def get_library(self):
        track_list = spotify.api.get_saved_tracks(self.get_access_token()).get('saved_tracks')
        track_objects = list(map(lambda obj: SavedTrack(self.get_access_token(), obj).perform_audio_analysis(), track_list))
        return TrackCollection(self.get_access_token(), track_objects)

    # Constructor
    def __init__(self, params = {}, id = None):
        FirestoreRecord.__init__(self, User.COLLECTION_NAME, params, id)
        
        # Following fields are required by flask-login
        self.is_active = True
        self.is_anonymous = False
        if self.exists():
            self.is_authenticated = True
        else:
            self.is_authenticated = False