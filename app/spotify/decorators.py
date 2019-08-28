# Decorators used in this module

import functools
import spotify.exceptions

# Decorator to raise an error if a response indicates that the access token has expired
def verify_token_active(func):
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.get('error'):
            if 'token expired' in response['error']['message']:
                raise spotify.exceptions.ExpiredTokenError
            else:
                raise spotify.exceptions.RequestError(response['error']['message'])
        return response
    return decorated_function