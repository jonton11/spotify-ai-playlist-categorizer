from authenticate import sp
from spotify import get_liked_songs

def main():
    liked_songs = get_liked_songs()

    print("Liked Songs:")
    for song in liked_songs:
        print(song['track']['name'])

if __name__ == "__main__":
    main()
