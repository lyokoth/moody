import spotipy
import spotify
import mood
from dotenv import load_dotenv
from spotify import get_user_auth, auth_query_parameters, SPOTIFY_AUTH_URL, SPOTIFY_TOKEN_URL
from urllib.parse import quote
import os 
import json
import requests
import base64
from keys import CLIENT_ID, CLIENT_SECRET, redirect_uri
from flask import Flask, flash, redirect, render_template, request, session, abort
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from functions import authenticate_spotify, aggregate_top_artists, aggregate_top_tracks, select_tracks, create_playlist
from model import User, Track, Playlist, PlaylistTrack, db, connect_to_db
from jinja2 import StrictUndefined


# Client Keys


app = Flask(__name__)

CLIENT_ID = CLIENT_ID
CLIENT_SECRET = CLIENT_SECRET
redirect_uri = redirect_uri



scope = 'user-top-read user-follow-read playlist-modify-public streaming user-read-birthdate user-read-email user-read-private'
oauth = SpotifyOAuth(CLIENT_ID,CLIENT_SECRET,redirect_uri, scope=scope)


pp = Flask(__name__)

app.jinja_env.undefinded = StrictUndefined

@app.route('/')
def homepage():
    """ Render welcome page with login button """

    if session.get('access_token'):
        return render_template('index.html')

    else:
        return render_template('homepage.html')


@app.route('/spotify-auth')
def authorization():
    """ Spotify Authorization Page """

    auth_url = spotify.get_user_authorization()
    return redirect(auth_url)


@app.route('/about')
def about():
    """ About page with description about app """

    return render_template('about.html')


@app.route('/mood')
def get_user_mood():
    """ Get user's current mood. 

    Add User to database and save user's artists to session. """

    response_data = spotify.get_tokens()

    session['access_token'] = response_data['access_token']
    auth_header = spotify.get_auth_header(session.get('access_token'))

    username = spotify.get_user_id(auth_header)
    session['user'] = username 

    user = db.session.query(User).filter(User.id == username).all()

    if not user:
        new_user = User(id = username, refresh_token = response_data['refresh_token'])
        db.session.add(new_user)
        db.session.commit()

    # gathering users top artists
    top_artists = mood.get_top_artists(auth_header, 50)
    artists = mood.get_related_artists(auth_header, top_artists)
    
    session['artists'] = artists

    return render_template('mood.html')


@app.route('/playlist')
def playlist_created():
    """ Create playlist """

    token = session.get('access_token')
    username = session.get('user')

    auth_header = spotify.get_auth_header(token)

    name = request.args.get('name')
    user_mood = request.args.get('mood')

    session['name'] = name

    user = db.session.query(User).filter(User.id == username).one()
    user_tracks = user.tracks

    if not user_tracks:
        user_artists = session.get('artists')
        top_tracks = mood.get_top_tracks(auth_header, user_artists)
        cluster = mood.cluster_ids(top_tracks)
        user_tracks = mood.add_and_get_user_tracks(auth_header, cluster)
    
    audio_feat = mood.standardize_audio_features(user_tracks)
    playlist_tracks = mood.select_tracks(audio_feat, float(user_mood))
    spotify_play = mood.create_playlist(auth_header, username, playlist_tracks, user_mood, name)

    session['spotify'] = spotify_play

    return render_template('created.html', spotify_play = spotify_play)

@app.route('/playlist-player')
def playlist_player():
    """ Take user to moodify web player with created playlist """

    name = session.get('name')
    token = session.get('access_token')
    spotify = session.get('spotify')

    return render_template('playlist.html', name = name, token = token)

@app.route('/track-info.json')
def track_info():
    """ Return jsonified dictionary containing track name as key and track uri as value """

    track_info = []

    user_playlist = session.get('playlist')

    playlist_tracks = db.session.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == user_playlist).all()

    for track in playlist_tracks:
        track_uri = track.track_uri

        track = db.session.query(Track).filter(Track.uri == track_uri).one()

        track_name = track.name

        track_data = {'name' : track_name,
                      'uri' : track_uri}

        track_info.append(track_data)

    return json({'tracks' : track_info})


@app.route('/logout')
def logout():
    """ Logged out and session cleared """

    session.clear()
    flash("Logged out!")
    return redirect('/')

