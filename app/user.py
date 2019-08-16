from dbtools.google_cloud import FirestoreRecord

# Class to represent a User - Inherits from FirestoreRecord
class User(FirestoreRecord):
    # Collection Name
    COLLECTION_NAME = 'users'

    # Saves Spotify Authentication Info

    # Constructor
    def __init__(self, params = {}, id = None):
        FirestoreRecord.__init__(self, User.COLLECTION_NAME, params, id)