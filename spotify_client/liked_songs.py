from typing import List, Dict
import time
import logging

logger = logging.getLogger(__name__)

class LikedSongs:
    def __init__(self, sp):
        self.sp = sp
        
    def get_liked_songs(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """
        Get user's liked songs with pagination support.
        
        Args:
            limit: Number of tracks to fetch per request
            offset: Starting position of the request
            
        Returns:
            List of liked song objects
        """
        results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
        return results['items']
    
    def remove_from_liked_songs(self, tracks: List[Dict]) -> bool:
        """
        Remove tracks from user's Liked Songs.
        
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
            logger.error(f"Error removing tracks from Liked Songs: {str(e)}")
            return False 