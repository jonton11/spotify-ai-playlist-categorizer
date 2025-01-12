import pytest
from unittest.mock import patch, MagicMock
from spotify import get_liked_songs, get_audio_features

@pytest.fixture
def mock_spotify_client():
    with patch('spotify.sp') as mock_sp:
        # Mock the current_user_saved_tracks response
        mock_sp.current_user_saved_tracks.return_value = {
            'items': [
                {
                    'track': {
                        'id': 'track1',
                        'name': 'Test Track 1'
                    }
                },
                {
                    'track': {
                        'id': 'track2',
                        'name': 'Test Track 2'
                    }
                }
            ]
        }
        
        # Mock the audio_features response
        mock_sp.audio_features.return_value = [
            {
                'id': 'track1',
                'danceability': 0.8,
                'energy': 0.6
            },
            {
                'id': 'track2',
                'danceability': 0.7,
                'energy': 0.5
            }
        ]
        yield mock_sp

def test_get_liked_songs(mock_spotify_client):
    """Test fetching liked songs."""
    songs = get_liked_songs(limit=2)
    
    # Verify the function called the API correctly
    mock_spotify_client.current_user_saved_tracks.assert_called_once_with(limit=2, offset=0)
    
    # Verify we got the expected number of songs
    assert len(songs) == 2
    assert songs[0]['track']['name'] == 'Test Track 1'
    assert songs[1]['track']['name'] == 'Test Track 2'

def test_get_audio_features(mock_spotify_client):
    """Test fetching audio features with batching."""
    track_ids = ['track1', 'track2']
    features = get_audio_features(track_ids, batch_size=2)
    
    # Verify the function called the API correctly
    mock_spotify_client.audio_features.assert_called_once_with(['track1', 'track2'])
    
    # Verify we got the expected features
    assert len(features) == 2
    assert features[0]['id'] == 'track1'
    assert features[1]['id'] == 'track2'

def test_get_audio_features_with_rate_limit(mock_spotify_client):
    """Test handling of rate limit errors."""
    # Mock a rate limit error on first call
    rate_limit_error = type('SpotifyException', (Exception,), {
        'http_status': 429,
        'headers': {'Retry-After': '1'}
    })
    mock_spotify_client.audio_features.side_effect = [
        rate_limit_error(),  # First call fails
        [{'id': 'track1', 'danceability': 0.8}]  # Retry succeeds
    ]
    
    features = get_audio_features(['track1'], batch_size=1)
    
    # Verify we got features after retry
    assert len(features) == 1
    assert features[0]['id'] == 'track1'
    # Verify the function was called twice (initial + retry)
    assert mock_spotify_client.audio_features.call_count == 2
