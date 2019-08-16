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

    # Gets a valid access token to use
    def get_access_token(self):
        return self.params.get('access_token')

    # Constructor
    def __init__(self, params = {}, id = None):
        FirestoreRecord.__init__(self, User.COLLECTION_NAME, params, id)