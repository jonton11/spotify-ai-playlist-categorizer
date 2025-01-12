import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import config

def is_running_in_ci():
    """Check if we're running in a CI environment."""
    return os.getenv('CI') == 'true'

if is_running_in_ci():
    # Use Client Credentials flow in CI
    auth_manager = SpotifyClientCredentials(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET
    )
else:
    # Use OAuth flow in local development
    auth_manager = SpotifyOAuth(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        redirect_uri=config.REDIRECT_URI,
        scope="user-library-read playlist-modify-public playlist-modify-private"
    )

sp = spotipy.Spotify(auth_manager=auth_manager)
