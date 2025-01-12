#!/usr/bin/env python3
import argparse
from spotify_client.liked_songs import LikedSongs
from authenticate import sp
from typing import List, Dict
import sys

def summarize_tracks(tracks: List[Dict]) -> None:
    """Print a summary of the fetched tracks."""
    print(f"\nFetched {len(tracks)} tracks:")
    
    # Show first few tracks as examples
    print("\nExample tracks:")
    for i, track in enumerate(tracks[:5], 1):
        track_info = track['track']
        artists = ", ".join(artist['name'] for artist in track_info['artists'])
        print(f"{i}. {track_info['name']} by {artists}")
    
    if len(tracks) > 5:
        print(f"... and {len(tracks) - 5} more")

def confirm_action(prompt: str) -> bool:
    """Ask user for confirmation."""
    while True:
        response = input(f"\n{prompt} (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        if response in ['no', 'n']:
            return False
        print("Please answer 'yes' or 'no'")

def main():
    parser = argparse.ArgumentParser(description='Fetch and manage Spotify liked songs')
    parser.add_argument('--limit', type=int, default=100, help='Number of songs to fetch')
    args = parser.parse_args()

    try:
        # Initialize LikedSongs handler
        liked_songs = LikedSongs(sp)
        
        print(f"\n🎵 Fetching your {args.limit} most recent liked songs...")
        tracks = liked_songs.get_liked_songs(args.limit)
        
        if not tracks:
            print("❌ No liked songs found")
            return
            
        print(f"\n✅ Successfully fetched {len(tracks)} songs")
        
        # Show summary
        summarize_tracks(tracks)
        
        # Ask about removal
        if confirm_action("Would you like to remove these songs from your Liked Songs?"):
            if confirm_action("⚠️  WARNING: This action cannot be undone. Are you sure?"):
                print("\n🗑️  Removing songs from Liked Songs...")
                if liked_songs.remove_from_liked_songs(tracks):
                    print("\n✅ Successfully removed tracks from Liked Songs")
                else:
                    print("\n❌ Failed to remove some tracks from Liked Songs")
            else:
                print("\n⏭️  Skipping removal.")
        else:
            print("\n⏭️  Keeping songs in Liked Songs.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 