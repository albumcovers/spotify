from flask import Flask, render_template, request, redirect
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

username = "t"
scope = "user-read-currently-playing"
redirect_uri='callback' #replace

CLIENT_ID = 'id' #replace
CLIENT_SECRET = 'secret' #replace
app = Flask('currently-playing')


@app.get('/')
def index():
    token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)

    spotify = spotipy.Spotify(auth=token)
    playing = spotify.currently_playing()
    # top_artists = spotify.current_user_top_artists(limit=50, time_range="medium_term")
    open('thing.json', 'w').write(str(playing))
    artist = playing['item']['artists'][0]['name']
    track = playing['item']['name']
    images = playing['item']['album']['images'][0]['url']
    return render_template('index.html', title=track,
    artist=artist,
    final_image_url=images)

@app.get('/api/image')
def api_image():
  token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)

  spotify = spotipy.Spotify(auth=token)
  playing = spotify.currently_playing()
  return playing['item']['album']['images'][0]['url']

@app.get('/api/title')
def api_title():
  token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)

  spotify = spotipy.Spotify(auth=token)
  playing = spotify.currently_playing()
  return playing['item']['name']

@app.get('/api/artist')
def api_artist():
  token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)
  spotify = spotipy.Spotify(auth=token)
  playing = spotify.currently_playing()
  return playing['item']['artists'][0]['name']

@app.errorhandler(500)
def internal_error(error):
  if str(request.url_rule) == '/api/title':
    return 'nothing'
  elif str(request.url_rule) == '/api/artist':
    return 'no one'
  else:
    return render_template('index.html',
    final_image_url='https://i.pinimg.com/564x/46/46/dd/4646dd0ebb3f008253e4deea38d233de--emoji-emoticons-emojis.jpg',
    title='nothing',artist='no one'
  )

@app.errorhandler(404)
def not_found(error):
    return redirect('/'), 404

app.run(host='0.0.0.0', port=8080)
