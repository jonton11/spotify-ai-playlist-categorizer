import pytest
from spotify_client.liked_songs import LikedSongs

def test_get_liked_songs_with_limit(mock_spotify_client, mock_track):
    """Test fetching liked songs with a limit."""
    liked_songs = LikedSongs(mock_spotify_client)
    tracks = liked_songs.get_liked_songs(limit=5)
    
    assert len(tracks) == 3  # Our mock returns 3 tracks
    assert all('track' in track for track in tracks)
    assert all('added_at' in track for track in tracks)
    assert tracks[0] == mock_track  # Verify the track data matches our mock

def test_get_audio_features(mock_spotify_client, mock_audio_features):
    """Test fetching audio features for tracks."""
    liked_songs = LikedSongs(mock_spotify_client)
    
    # Get tracks and their features
    tracks = liked_songs.get_liked_songs(limit=3)
    features = liked_songs.get_audio_features(tracks)
    
    assert len(features) == 3
    assert features[0] == mock_audio_features
    
    # Verify all expected features are present
    expected_features = {'danceability', 'energy', 'key', 'loudness', 'tempo'}
    assert all(all(feature in audio_feature for feature in expected_features) 
              for audio_feature in features)

def test_get_tracks_with_features(mock_spotify_client, mock_track, mock_audio_features):
    """Test fetching tracks with their audio features."""
    liked_songs = LikedSongs(mock_spotify_client)
    
    tracks = liked_songs.get_tracks_with_features(limit=3)
    
    assert len(tracks) == 3
    # Verify track data
    assert tracks[0]['track'] == mock_track['track']
    # Verify audio features
    assert tracks[0]['audio_features'] == mock_audio_features

def test_remove_from_liked_songs(mock_spotify_client, mock_track):
    """Test removing tracks from Liked Songs."""
    liked_songs = LikedSongs(mock_spotify_client)
    tracks = [mock_track]
    
    # Test successful removal
    assert liked_songs.remove_from_liked_songs(tracks) == True
    mock_spotify_client.current_user_saved_tracks_delete.assert_called_once()
    
    # Test error handling
    mock_spotify_client.current_user_saved_tracks_delete.side_effect = Exception("API Error")
    assert liked_songs.remove_from_liked_songs(tracks) == False

def test_process_and_remove(mock_spotify_client, mock_track, mock_audio_features):
    """Test the full process of fetching and removing tracks."""
    liked_songs = LikedSongs(mock_spotify_client)
    
    tracks = liked_songs.process_and_remove(limit=2)
    
    assert len(tracks) == 3  # Our mock returns 3 tracks
    assert all('audio_features' in track for track in tracks)
    assert tracks[0]['audio_features'] == mock_audio_features
    
    # Verify removal was called
    mock_spotify_client.current_user_saved_tracks_delete.assert_called_once() 