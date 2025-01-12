import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_track():
    """Mock track data as returned by Spotify API."""
    return {
        "added_at": "2024-01-12T12:00:00Z",
        "track": {
            "id": "track123",
            "name": "Test Song",
            "artists": [
                {
                    "id": "artist123",
                    "name": "Test Artist"
                }
            ],
            "album": {
                "id": "album123",
                "name": "Test Album"
            },
            "duration_ms": 180000
        }
    }

@pytest.fixture
def mock_spotify_client(mock_track):
    """Mock Spotify client with predefined responses."""
    client = Mock()
    
    # Mock current_user_saved_tracks
    client.current_user_saved_tracks.return_value = {
        "items": [mock_track] * 3,  # Return 3 identical tracks for testing
        "total": 3,
        "limit": 100,
        "offset": 0
    }
    
    # Mock current_user_saved_tracks_delete
    client.current_user_saved_tracks_delete.return_value = None
    
    return client 