from typing import List, Dict

class LikedSongs:
    def __init__(self, spotify_client):
        """
        Initialize LikedSongs handler.
        
        Args:
            spotify_client: An authenticated Spotify client instance
        """
        self.sp = spotify_client
        
    def get_liked_songs(self, limit: int = 100) -> List[Dict]:
        """
        Fetch most recent Liked Songs.
        
        Args:
            limit: Maximum number of songs to fetch (default: 100)
            
        Returns:
            List of tracks with their metadata
        """
        results = self.sp.current_user_saved_tracks(limit=limit)
        return results['items']
    
    def get_audio_features(self, tracks: List[Dict]) -> List[Dict]:
        """
        Get audio features for a list of tracks.
        
        Args:
            tracks: List of track objects from get_liked_songs
            
        Returns:
            List of audio features for each track
        """
        track_ids = [track['track']['id'] for track in tracks]
        return self.sp.audio_features(track_ids)
    
    def get_tracks_with_features(self, limit: int = 100) -> List[Dict]:
        """
        Get Liked Songs with their audio features in a single call.
        
        Args:
            limit: Maximum number of songs to fetch (default: 100)
            
        Returns:
            List of tracks with their metadata and audio features
        """
        tracks = self.get_liked_songs(limit)
        features = self.get_audio_features(tracks)
        
        # Combine track info with audio features
        for track, feature in zip(tracks, features):
            track['audio_features'] = feature
            
        return tracks
    
    def remove_from_liked_songs(self, tracks: List[Dict]) -> bool:
        """
        Remove the specified tracks from Liked Songs.
        
        Args:
            tracks: List of track objects to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            track_ids = [track['track']['id'] for track in tracks]
            self.sp.current_user_saved_tracks_delete(tracks=track_ids)
            return True
        except Exception as e:
            print(f"Error removing tracks from Liked Songs: {str(e)}")
            return False
    
    def process_and_remove(self, limit: int = 100) -> List[Dict]:
        """
        Get tracks with features and remove them from Liked Songs in one operation.
        
        Args:
            limit: Maximum number of songs to process (default: 100)
            
        Returns:
            List of processed tracks with their features
        """
        tracks = self.get_tracks_with_features(limit)
        if tracks:
            success = self.remove_from_liked_songs(tracks)
            if not success:
                raise Exception("Failed to remove tracks from Liked Songs")
        return tracks 