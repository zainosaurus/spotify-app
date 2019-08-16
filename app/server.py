from flask import Flask, render_template, request, url_for, redirect
import spotify.authenticator
import spotify.api
import requests
import os

app = Flask(__name__)
authorization_code = None
access_token = None
refresh_token = None

def dict_to_string(dic):
    string = ''
    for key, val in dic.items():
        string += "{}: {}\n".format(key, val)
    return string

@app.route('/')
def index():
    return render_template('index.html', title='yeetosaurus')

@app.route('/launch_spotify_authentication')
def launch_spotify_authentication():
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    redirect_uri = url_for('spotify_auth_landing', _external = True)
    scope = 'user-read-private user-read-email'
    state = 'dumm'
    return redirect(spotify.authenticator.user_login_url(client_id, redirect_uri, scope, state))

@app.route('/spotify_auth_landing/')
def spotify_auth_landing():
    global authorization_code
    global access_token
    global refresh_token

    if request.args.get('state') == 'dumm':
        authorization_code = request.args.get('code')

        # Get refresh and access tokens
        redirect_uri = url_for('spotify_auth_landing', _external = True)
        response = spotify.authenticator \
            .get_access_credentials(authorization_code, redirect_uri, os.environ['SPOTIFY_CLIENT_ID'], os.environ['SPOTIFY_CLIENT_SECRET'])
        access_token = response.get('access_token')
        refresh_token = response.get('refresh_token')
        return render_template('index.html', title='Success', response_content=dict_to_string(response))
    else:
        print('Wrong state!! error; state= ' + request.args.get('state') )
        return render_template('index.html', title='Failure :(', response_content=str(request.args))

@app.route('/my_profile')
def my_profile():
    global access_token

    # send request to spotify to get current profile information
    response = spotify.api.get_current_profile(access_token).json()

    return render_template('index.html', title='My Profile', response_content=dict_to_string(response))

# Launch App
if __name__ == "__main__":
	try:
		app.run(host='0.0.0.0', port=8080, debug=True)
	except:
		print("Server Crashed :(")