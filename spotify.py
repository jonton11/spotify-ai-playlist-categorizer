from authenticate import sp

def get_liked_songs():
    results = sp.current_user_saved_tracks(limit=50)
    liked_songs = results['items']
    while results['next']:
        results = sp.next(results)
        liked_songs.extend(results['items'])
    return liked_songs

def get_audio_features(track_ids):
    return sp.audio_features(track_ids)

liked_songs = get_liked_songs()
track_ids = [track['track']['id'] for track in liked_songs]
audio_features = get_audio_features(track_ids) # audio features will help with categorizing

