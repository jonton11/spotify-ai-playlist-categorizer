import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    redirect_uri=config.REDIRECT_URI,
    scope="user-library-read playlist-modify-public playlist-modify-private"
))
