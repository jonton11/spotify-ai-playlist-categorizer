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
def mock_audio_features():
    """Mock audio features as returned by Spotify API."""
    return {
        "danceability": 0.8,
        "energy": 0.9,
        "key": 5,
        "loudness": -4.329,
        "mode": 1,
        "speechiness": 0.0461,
        "acousticness": 0.0346,
        "instrumentalness": 0.0,
        "liveness": 0.0897,
        "valence": 0.813,
        "tempo": 118.211,
        "id": "track123",
        "duration_ms": 180000
    }

@pytest.fixture
def mock_spotify_client(mock_track, mock_audio_features):
    """Mock Spotify client with predefined responses."""
    client = Mock()
    
    # Mock current_user_saved_tracks
    client.current_user_saved_tracks.return_value = {
        "items": [mock_track] * 3,  # Return 3 identical tracks for testing
        "total": 3,
        "limit": 100,
        "offset": 0
    }
    
    # Mock audio_features
    client.audio_features.return_value = [mock_audio_features] * 3
    
    # Mock current_user_saved_tracks_delete
    client.current_user_saved_tracks_delete.return_value = None
    
    return client 