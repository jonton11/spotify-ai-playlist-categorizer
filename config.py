from dotenv import load_dotenv
import os
import sys

def is_running_in_ci():
    """Check if we're running in a CI environment."""
    return os.getenv('CI') == 'true'

def is_running_tests():
    """Check if we're running tests."""
    return 'pytest' in sys.modules

# Load appropriate .env file
if is_running_tests():
    # Use .env.test for tests
    load_dotenv('.env.test')
elif not is_running_in_ci():
    # Use .env for development
    load_dotenv('.env')

# Required in all environments
required_vars = ['SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET']

# Required only in local development
if not is_running_in_ci():
    required_vars.append('SPOTIFY_REDIRECT_URI')

# Check for required variables
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing_vars)}. "
        "Please ensure these are set in your .env file or CI environment."
    )

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')  # May be None in CI
