import os
from dotenv import load_dotenv
import pytest
import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler, SpotifyClientCredentials
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def is_running_in_ci():
    """Check if we're running in a CI environment."""
    return os.getenv('CI') == 'true'

def load_env(env_file='.env.test'):
    """
    Load environment variables from the specified .env file.
    
    Args:
        env_file (str): The environment file to load. Defaults to '.env.test' for test environment.
        
    Raises:
        EnvironmentError: If the required environment variables are not set.
    """
    # For testing, we explicitly want .env.test
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print(f"\nLoaded environment from: {env_file}")
    else:
        print(f"\nWarning: {env_file} not found, checking environment variables...")
    
    # Always required variables
    required_vars = ['SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET']

    # Redirect URI only required for non-CI environments
    if not is_running_in_ci():
        required_vars.append('SPOTIFY_REDIRECT_URI')

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}. "
            f"Please ensure these are set in {env_file} "
            "or in your CI/CD environment variables."
        )

# Load test environment for these tests
load_env('.env.test')

@pytest.mark.skipif(is_running_in_ci(), reason="OAuth flow requires user interaction")
def test_spotify_oauth_flow():
    """Test the OAuth flow for local development."""
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    
    # Print credentials for verification (excluding secret)
    print(f"\nTesting OAuth flow with:")
    print(f"Client ID: {client_id}")
    print(f"Redirect URI: {redirect_uri}")
    
    try:
        # Create a unique cache path for testing
        cache_path = ".spotify_cache_test"
        
        # Remove cache if it exists
        if os.path.exists(cache_path):
            os.remove(cache_path)
            
        # Create cache handler
        cache_handler = CacheFileHandler(cache_path=cache_path)
        
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope='user-library-read playlist-modify-public',
            open_browser=True,
            cache_handler=cache_handler
        )
        
        # Get the auth URL for manual authorization
        auth_url = auth_manager.get_authorize_url()
        print(f"\nPlease visit this URL to authorize the application:")
        print(auth_url)
        
        # Wait for user to authorize and get the code
        print("\nAfter authorizing, please paste the redirect URL here:")
        response = input()
        
        # Extract the code from the response
        code = auth_manager.parse_response_code(response)
        
        # Get the access token
        token = auth_manager.get_access_token(code, as_dict=False)
        
        # Initialize Spotify client with the token
        sp = spotipy.Spotify(auth=token)
        
        # Test API connection by getting current user
        user = sp.current_user()
        assert user is not None
        assert 'id' in user
        print(f"\nSuccessfully authenticated as user: {user['id']}")
        
    except Exception as e:
        pytest.fail(f"Failed to connect to Spotify API: {str(e)}\nType: {type(e)}")
    finally:
        # Clean up the cache file
        if os.path.exists(cache_path):
            os.remove(cache_path)

def test_spotify_client_credentials():
    """Test the Client Credentials flow (used in CI/CD)."""
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    try:
        # Use client credentials flow (no user auth required)
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # Test API connection with a simple search
        # This doesn't require user authentication
        results = sp.search(q='test', limit=1)
        assert results is not None
        assert 'tracks' in results
        print("\nSuccessfully connected to Spotify API using client credentials")
        
    except Exception as e:
        pytest.fail(f"Failed to connect to Spotify API: {str(e)}\nType: {type(e)}")

def test_environment_variables():
    """Test that all required environment variables are set."""
    # Always required variables
    required_vars = [
        'SPOTIFY_CLIENT_ID',
        'SPOTIFY_CLIENT_SECRET'
    ]
    
    # Redirect URI only required for non-CI environments
    if not is_running_in_ci():
        required_vars.append('SPOTIFY_REDIRECT_URI')

    for var in required_vars:
        assert os.getenv(var) is not None, f"Missing environment variable: {var}"
        assert os.getenv(var) != "", f"Empty environment variable: {var}" 