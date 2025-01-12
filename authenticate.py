import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set logging levels for all external libraries to WARNING
logging.getLogger('spotipy').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)

def is_running_in_ci():
    """Check if we're running in a CI environment."""
    return os.getenv('CI') == 'true'

# Define required scopes
SCOPES = [
    'user-library-read',          # Read access to user's liked songs
    'user-library-modify',        # Modify user's liked songs
    'playlist-modify-public',     # Manage public playlists
    'playlist-modify-private',    # Manage private playlists
]

if is_running_in_ci():
    logger.info("Initializing Spotify client for CI environment")
    auth_manager = SpotifyClientCredentials(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET
    )
else:
    logger.info("Initializing Spotify client for local development")
    cache_path = ".spotify_cache"
    if os.path.exists(cache_path):
        os.remove(cache_path)
    
    auth_manager = SpotifyOAuth(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        redirect_uri=config.REDIRECT_URI,
        scope=' '.join(SCOPES),
        open_browser=True,
        cache_path=cache_path
    )
    
    auth_manager.get_access_token(as_dict=False)

sp = spotipy.Spotify(auth_manager=auth_manager)
