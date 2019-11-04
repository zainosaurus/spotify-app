import spotify.api

class Profile:
    """ Represents a Profile Object """

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
        return spotify.api.get_current_profile(self._auth_token)

    def __init__(self, auth_token):
        self._auth_token = auth_token
        self.profile_info = self.load_profile_info()