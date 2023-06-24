from flask import Flask, flash, redirect, render_template, request, session, abort
from jinja2 import StrictUndefined

import spotify as spotify
import mood as mood
from settings import *
from model import User, Track, Playlist, UserTrack, PlaylistTrack, db, connect_to_db

app = Flask(__name__)

app.jinja2_undefined = StrictUndefined


##Authorization

@app.route('/')
def homepage(request):
    """ Render welcome page with login button """
    if request.session.get('access_token'):
        return render_template ('templates/mood.html')
    else:
        return render_template ('templates/index.html')


@app.route('/spotify-auth')
def authorization():
    """ Spotify Authorization Page """
    auth_url = spotify.get_user_authorization()
    return redirect(location=auth_url)


@app.route('/about')
def about(request):
    """ About page with description about app """
    return render_template('templates/about.html')


@app.route('/mood')
def get_user_mood(request):
    """ Get user's current mood. 
    Add User to database and save user's artists to session. """
    response_data = spotify.get_tokens()

    request.session['access_token'] = response_data['access_token']
    auth_header = spotify.get_auth_header(request.session.get('access_token'))

    username = spotify.get_user_id(auth_header)
    request.session['user'] = username

    user = db.session.query(User).filter(User.id == username).all()

    if not user:
        new_user = User(id=username, refresh_token=response_data['refresh_token'])
        db.session.add(new_user)
        db.session.commit()

    # gathering users top artists
    top_artists = mood.get_top_artists(auth_header, 50)
    artists = mood.get_related_artists(auth_header, top_artists)

    request.session['artists'] = artists

    return render_template('templates/mood.html')


@app.route('/playlist')
def playlist_created(request):
    """ Create playlist """
    token = request.session.get('access_token')
    username = request.session.get('user')

    auth_header = spotify.get_auth_header(token)

    name = request.GET.get('name')
    user_mood = request.GET.get('mood')

    request.session['name'] = name

    user = db.session.query(User).filter(User.id == username).one()
    user_tracks = user.tracks

    if not user_tracks:
        user_artists = request.session.get('artists')
        top_tracks = mood.get_top_tracks(auth_header, user_artists)
        cluster = mood.cluster_ids(top_tracks)
        user_tracks = mood.add_and_get_user_tracks(auth_header, cluster)

    audio_feat = mood.standardize_audio_features(user_tracks)
    playlist_tracks = mood.select_tracks(audio_feat, float(user_mood))
    spotify_play = mood.create_playlist(auth_header, username, playlist_tracks, user_mood, name)

    request.session['spotify'] = spotify_play

    return render_template('templates/created.html', spotify_play=spotify_play)


@app.route('/playlist-player')
def playlist_player(request):
  
    name = request.session.get('name')
    token = request.session.get('access_token')
    spotify = request.session.get('spotify')

    return render_template('templates/playlist.html', name=name, token=token)


@app.route('/track-info.json')
def track_info(request):
    """ Return jsonified dictionary containing track name as key and track uri as value """
    track_info = []

    user_playlist = request.session.get('playlist')

    playlist_tracks = db.session.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == user_playlist).all()

   
