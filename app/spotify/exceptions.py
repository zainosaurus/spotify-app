class SpotifyError(Exception):
    """ Base class for Errors in this module """
    pass

class RequestError(SpotifyError):
    """ Errors pertaining to requests """
    pass

class ExpiredTokenError(RequestError):
    """ Raised when an expired access token is used to make a request to the (official) Spotify API """
    pass