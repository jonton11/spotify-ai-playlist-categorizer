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