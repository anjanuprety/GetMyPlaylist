from flask import Flask, redirect, request, url_for, session
import spotipy #spotipy is a lightweight Python library for the Spotify Web API
from spotipy.oauth2 import SpotifyOAuth
import time #time module provides various time-related functions
import pandas as pd 

# Initialize the Flask web application
app = Flask(__name__)

# Set a secret key to sign session cookies and configure the session cookie name
app.secret_key = "ADutebgfe2445ief"
app.config['SESSION_COOKIE_NAME'] = 'music cookie'

# This constant will store the key used to save the token info in the session
TOKEN_INFO = "token_info"

# Define the route for the home page
@app.route('/')
def login():
    # Create an instance of the Spotify OAuth object
    sp_oauth = create_spotify_oauth()
    # Get the Spotify authorization URL
    auth_url = sp_oauth.get_authorize_url()
    # Redirect the user to the Spotify login page to grant access
    return redirect(auth_url)

# Define the route where Spotify will redirect after the user grants access
@app.route('/authorize')
def authorize():
    # Create an instance of the Spotify OAuth object
    sp_oauth = create_spotify_oauth()
    # Clear any previous session data
    session.clear()
    # Get the authorization code from the URL
    code = request.args.get('code')
    # Exchange the code for an access token
    token_info = sp_oauth.get_access_token(code)
    # Save the token info in the session
    session[TOKEN_INFO] = token_info
    # Redirect the user to the page where their library will be displayed
    return redirect("/getLibrary")

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

# Define the route for retrieving all the user's saved songs
@app.route('/getLibrary')
def get_all_tracks():
    # Get token info and check if it's authorized
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    
    # Create Spotify object with the access token
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    
    results = []
    iter = 0
    while True:
        offset = iter * 50
        iter += 1
        # Get 50 tracks from the user's library at a time
        curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
        for idx, item in enumerate(curGroup):
            track = item['track']
            # Format track name and artist, and add to results list
            val = track['name'] + " - " + track['artists'][0]['name']
            results.append(val)
        
        if len(curGroup) < 50:
            break
    
    # Create a DataFrame and save the results as a CSV file
    df = pd.DataFrame(results, columns=["song names"])
    df.to_csv('songs.csv', index=False)
    
    return "done"

# Checks if token is valid and refreshes it if expired
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not session.get('token_info', False):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if is_token_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

# Function to create the Spotify OAuth object for handling authentication
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="id",   
        client_secret="secret",  
        redirect_uri=url_for('authorize', _external=True),  
        scope="user-library-read"  # The scope (permission) to access the user's saved tracks
    )