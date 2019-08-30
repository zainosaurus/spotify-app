from flask import Flask, render_template, request, url_for, redirect, session
import flask_login
from flask_login import current_user, login_required
from functools import wraps
import spotify.authenticator
import spotify.api
from spotify.objects import Track, SavedTrack, Profile, Library
import spotify.exceptions
import requests
import os
from user import User
import json

app = Flask(__name__)
app.secret_key = os.urandom(16)     # for session storage

# Setting up flask-login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# User Loader callback for Flask Login
@login_manager.user_loader
def load_user(user_id):
    return User(id = session['user_id']).find()

def dict_to_string(dic):
    return json.dumps(dic, indent = 4)

# Checks if request was successful
# TODO should be deprecated soon
def successful_request(json_response):
    if json_response.get('error'):
        return False
    else:
        return True

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html', title='Spotify App')

@app.route('/launch_spotify_authentication', methods = ['GET'])
def launch_spotify_authentication():
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    redirect_uri = url_for('spotify_auth_landing', _external = True)
    scope = 'user-read-private user-read-email user-library-read'
    state = 'authenticity_key'
    return redirect(spotify.authenticator.user_login_url(client_id, redirect_uri, scope, state))

@app.route('/spotify_auth_landing/', methods = ['GET'])
def spotify_auth_landing():
    if request.args.get('state') == 'authenticity_key':
        authorization_code = request.args.get('code')

        # Get refresh and access tokens
        redirect_uri = url_for('spotify_auth_landing', _external = True)
        response = spotify.authenticator \
            .get_access_credentials(authorization_code, redirect_uri, os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_CLIENT_SECRET'])
        access_token = response.get('access_token')
        # Get user profile
        profile_info = spotify.api.get_current_profile(access_token)
        if successful_request(profile_info):
            # Find user in database with this profile info
            user_instance = User({
                'display_name': profile_info.get('display_name'),
                'spotify_id': profile_info.get('id'),
                'email': profile_info.get('email')
            })
            user = user_instance.find()
            # if not found, set as a new user
            if not user:
                user = user_instance
                user.save()
            # Update the access credentials
            user.save_access_credentials(response)
            # Login User Session
            flask_login.login_user(user, remember = True)
            return render_template('index.html',
                title = 'Success',
                response_content = dict_to_string(user.params)
            )
        else:
            return render_template('index.html',
                title = 'Fail',
                response_content = dict_to_string(profile_info)
            )
    else:
        return render_template('index.html',
            title = 'Failure :(',
            response_content = str(request.args)
        )

@app.route('/profile', methods = ['GET'])
@login_required
def my_profile():
    profile = Profile(current_user.get_access_token())
    return render_template('profile.html', content = profile.profile_info)

# Searches for a song (based on a query) and redirects to song info page
# required Parameters:
#   search_query: search query to execute (first hit is returned)
@app.route('/search', methods=['GET'])
@login_required
def song_search():
    track = Track.find_by_query(current_user.get_access_token(), request.args.get('search_query'))
    return redirect(url_for('song_info', spotify_id=track.track_info['id']))

# Returns song analysis data
# required parameters:
#   spotify_id: Spotify ID of the track to display
@app.route('/track/<string:spotify_id>', methods=['GET'])
@login_required
def song_info(spotify_id):
    track = Track.find_by_id(current_user.get_access_token(), spotify_id)
    track.perform_audio_analysis()
    return render_template('song_analysis.html', 
        title = track.track_info['name'],
        track_info = track.to_simple_json(), 
        labels = [],
        data_labels = track.data_points().get('labels'),
        data_values = track.data_points().get('data')
    )

# Get user's library
@app.route('/library')
@login_required
def my_library():
    library = Library(current_user.get_access_token())
    return render_template('library.html', saved_tracks = library.saved_tracks)

# Launch App
if __name__ == "__main__":
	try:
		app.run(host='0.0.0.0', port=8080, debug=True)
	except:
		print("Server Crashed :(")