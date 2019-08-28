from dbtools.google_cloud import FirestoreRecord
import time

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
            'last_refresh_at': time.time()
        })
        self.save()

    # Updates access credentials (when token is refreshed)
    def update_access_credentials(self, credentials):
        self.params.update({
            'access_token': credentials.get('access_token'),
            'last_refresh_at': time.time()
        })
        self.save()

    # Gets a valid access token to use
    def get_access_token(self):
        return self.params.get('access_token')

    # Accessor for refresh token
    def get_refresh_token(self):
        return self.params.get('refresh_token')

    # Accessor for ID
    #   Required by flask-login
    def get_id(self):
        return self.id

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