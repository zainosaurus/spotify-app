import spotify.api

class Profile:
    """ Represents a Profile Object """

    # Gets user profile associated with auth token
    def load_profile_info(self):
        return spotify.api.get_current_profile(self._auth_token)

    def __init__(self, auth_token):
        self._auth_token = auth_token
        self.profile_info = self.load_profile_info()