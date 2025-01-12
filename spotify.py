from authenticate import sp
import time
from typing import List, Dict, Any

def get_liked_songs(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Get user's liked songs with pagination support.
    
    Args:
        limit: Number of tracks to fetch per request
        offset: Starting position of the request
        
    Returns:
        List of liked song objects
    """
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)
    return results['items']

def get_audio_features(track_ids: List[str], batch_size: int = 50) -> List[Dict[str, Any]]:
    """
    Get audio features for tracks in batches to handle rate limits.
    
    Args:
        track_ids: List of Spotify track IDs
        batch_size: Number of tracks to process per batch
        
    Returns:
        List of audio features for the tracks
    """
    features = []
    
    # Process track_ids in batches
    for i in range(0, len(track_ids), batch_size):
        batch = track_ids[i:i + batch_size]
        try:
            batch_features = sp.audio_features(batch)
            if batch_features:
                features.extend(batch_features)
            # Add a small delay to avoid rate limits
            time.sleep(0.1)
        except Exception as e:
            print(f"Error fetching audio features for batch {i//batch_size}: {str(e)}")
            # Add a longer delay if we hit rate limits
            if hasattr(e, 'http_status') and e.http_status == 429:
                retry_after = int(e.headers.get('Retry-After', 3))
                time.sleep(retry_after)
                # Retry this batch
                batch_features = sp.audio_features(batch)
                if batch_features:
                    features.extend(batch_features)
    
    return features

# Remove the actual API calls that were happening on import
if __name__ == '__main__':
    # Only run this if the file is run directly
    liked_songs = get_liked_songs()
    track_ids = [track['track']['id'] for track in liked_songs]
    audio_features = get_audio_features(track_ids)

