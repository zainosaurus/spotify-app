from flask import Flask, render_template, request, url_for, redirect, session
from functools import wraps
import spotify.authenticator
import spotify.api
import requests
import os
from user import User
import json

app = Flask(__name__)
app.secret_key = os.urandom(16)     # for session storage

def dict_to_string(dic):
    return json.dumps(dic, indent = 4)

# Checks if request was successful
def successful_request(json_response):
    if json_response.get('error'):
        return False
    else:
        return True

# Finds current user based on browser session
# Returns current User (User), or None if the session hash is empty
def current_user():
    try:
        return User(id = session['user_id']).find()
    except KeyError:
        return None

# Decorator to ensure user has been verified before continuing
def verify_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user() is None:
            return render_template('index.html', title='Invalid User', response_content='User Session does not exist')
        return f(*args, **kwargs)
    return decorated_function

# Helper method - filters response json to only include keys of interest
# In keys_of_interest, keys multiple levels deep can be specified using : (example: key1:key2:...)
def filter_dict(full_dict, keys_of_interest):
    filtered_dict = {}
    for key in keys_of_interest:
        # Handle keys multiple levels deep
        nested_keys = key.split(':')
        key_name = '_'.join(nested_keys)
        val = full_dict
        for k in nested_keys:
            val = val[k]
        filtered_dict[key_name] = val
    return filtered_dict

def filter_search_response(track, features):
    response = {}
    response.update(filter_dict(track, ['name', 'album:name', 'artists', 'popularity']))
    response['artists'] = ', '.join(list(map(lambda x: x['name'], response['artists'])))
    response.update(filter_dict(features, ['danceability', 'energy', 'valence', 'tempo', 'loudness', 'acousticness', 'instrumentalness', 'liveness', 'speechiness']))
    return response

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html', title='Spotify App')

@app.route('/launch_spotify_authentication', methods = ['GET'])
def launch_spotify_authentication():
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    redirect_uri = url_for('spotify_auth_landing', _external = True)
    scope = 'user-read-private user-read-email'
    state = 'dumm'
    return redirect(spotify.authenticator.user_login_url(client_id, redirect_uri, scope, state))

@app.route('/spotify_auth_landing/', methods = ['GET'])
def spotify_auth_landing():
    if request.args.get('state') == 'dumm':
        authorization_code = request.args.get('code')

        # Get refresh and access tokens
        redirect_uri = url_for('spotify_auth_landing', _external = True)
        response = spotify.authenticator \
            .get_access_credentials(authorization_code, redirect_uri, os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_CLIENT_SECRET'])
        access_token = response.get('access_token')
        # Get user profile
        profile_info = spotify.api.get_current_profile(access_token).json()
        if successful_request(profile_info):
            # Find user in database with this profile info
            user_instance = User({'display_name': profile_info.get('display_name'), 'spotify_id': profile_info.get('id'), 'email': profile_info.get('email')})
            user = user_instance.find()
            # if not found, set as a new user
            if not user:
                user = user_instance
                user.save()
            # Update the access credentials
            user.save_access_credentials(response)
            # store user id in session
            session['user_id'] = user.id
            return render_template('index.html', title='Success', response_content=dict_to_string(user.params))
        else:
            return render_template('index.html', title='Fail', response_content=dict_to_string(profile_info))
    else:
        print('Wrong state!! error; state= ' + request.args.get('state') )
        return render_template('index.html', title='Failure :(', response_content=str(request.args))

@app.route('/my_profile', methods = ['GET'])
@verify_user
def my_profile():
    # send request to spotify to get current profile information
    response = spotify.api.get_current_profile(current_user().get_access_token()).json()

    return render_template('index.html', title='My Profile', response_content=dict_to_string(response))

# Returns song analysis data
# required parameters:
#   search_query(string): string to search for
@app.route('/song_info', methods = ['GET'])
@verify_user
def song_info():
    track_info = spotify.api.search(current_user().get_access_token(), request.args.get('search_query'), 'track').json()
    song_id = track_info['tracks']['items'][0]['id']
    audio_features = spotify.api.track_audio_features(current_user().get_access_token(), song_id).json()
    response_filtered = filter_search_response(track_info['tracks']['items'][0], audio_features)
    return render_template('index.html', title = request.args.get('search_query'), response_content = dict_to_string(response_filtered))

# Launch App
if __name__ == "__main__":
	try:
		app.run(host='0.0.0.0', port=8080, debug=True)
	except:
		print("Server Crashed :(")