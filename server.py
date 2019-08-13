from flask import Flask, render_template, request, url_for, redirect
import requests
import os

app = Flask(__name__)
authorization_code = None

@app.route('/')
def index():
    return render_template('index.html', title='yeetosaurus')

@app.route('/launch_spotify_authentication')
def launch_spotify_authentication():
    request_string = 'https://accounts.spotify.com/authorize?' +\
        'client_id=' + os.environ['SPOTIFY_CLIENT_ID'] + \
        '&response_type=code' + \
        '&redirect_uri=http://localhost:8080/spotify_auth_landing/' +\
        '&scope=user-read-private%20user-read-email' +\
        '&state=dumm'
    return redirect(request_string)

@app.route('/spotify_auth_landing/')
def spotify_auth_landing():
    if request.args.get('state') == 'dumm':
        authorization_code = request.args.get('code')

        # Get refresh and access tokens
        response = requests.post('https://accounts.spotify.com/api/token', data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': 'http://localhost:8080/spotify_auth_landing/',
            'client_id': os.environ['SPOTIFY_CLIENT_ID'],
            'client_secret': os.environ['SPOTIFY_CLIENT_SECRET']
        })
        print("Request completed ----------> response: \n" + str(response))
        return render_template('index.html', title='Success', response_content=str(response.json()))
    else:
        print('Wrong state!! error; state= ' + request.args.get('state') )
        return render_template('index.html', title='Failure :(', response_content=str(request.args))


# Launch App
if __name__ == "__main__":
	try:
		app.run(host='0.0.0.0', port=8080, debug=True)
	except:
		print("Server Crashed :(")