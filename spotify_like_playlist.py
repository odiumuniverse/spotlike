import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'https://example.com/callback'
SCOPE = 'user-library-modify user-library-read playlist-read-private'

if not CLIENT_ID or not CLIENT_SECRET:
    print("⚠️ Spotify credentials not found in environment variables")
    print("📝 Create a .env file and add to it:")
    print("   SPOTIFY_CLIENT_ID=your_client_id")
    print("   SPOTIFY_CLIENT_SECRET=your_client_secret")
    print("\nOr enter them now:")
    CLIENT_ID = input("Client ID: ").strip()
    CLIENT_SECRET = input("Client Secret: ").strip()

def authenticate_spotify():
    """Authentication in Spotify"""
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))
    return sp

def get_playlist_tracks(sp, playlist_id):
    """Get all tracks from playlist"""
    tracks = []
    offset = 0
    
    while True:
        results = sp.playlist_tracks(playlist_id, offset=offset)
        tracks.extend(results['items'])
        
        if results['next'] is None:
            break
        offset += len(results['items'])
    
    return tracks

def like_tracks(sp, tracks):
    """Like tracks"""
    track_ids = []
    track_names = []
    
    for item in tracks:
        track = item['track']
        if track is not None and track['id'] is not None:
            track_ids.append(track['id'])
            track_names.append(f"{track['name']} - {', '.join([artist['name'] for artist in track['artists']])}")
    
    for i in range(0, len(track_ids), 50):
        batch_ids = track_ids[i:i + 50]
        batch_names = track_names[i:i + 50]
        
        try:
            sp.current_user_saved_tracks_add(tracks=batch_ids)
            print(f"✅Added {len(batch_ids)} tracks:")
            for name in batch_names:
                print(f"   - {name}")
        except Exception as e:
            print(f"❌ Error adding tracks: {e}")

def main():
    print("🎵 Spotify Playlist Liker")
    print("-" * 50)
    
    try:
        sp = authenticate_spotify()
        print("✅ Successful authentication in Spotify")
    except Exception as e:
        print(f"❌ Authentication Error: {e}")
        return
    
    user = sp.current_user()
    print(f"👤Login as: {user['display_name']}")
    print("-" * 50)
    
    playlist_url = input("Enter the URL or ID of the Spotify playlist: ").strip()
    
    if 'spotify.com/playlist/' in playlist_url:
        playlist_id = playlist_url.split('playlist/')[1].split('?')[0]
    else:
        playlist_id = playlist_url
    
    try:
        playlist = sp.playlist(playlist_id)
        print(f"\n📋 Playlist: {playlist['name']}")
        print(f"📝 Description: {playlist['description']}")
        print(f"🎵 Number of tracks: {playlist['tracks']['total']}")
        print("-" * 50)
        
        print("\n⏳ Get a list of tracks...")
        tracks = get_playlist_tracks(sp, playlist_id)
        print(f"✅ Found {len(tracks)} tracks")
        
        track_ids = [item['track']['id'] for item in tracks if item['track'] and item['track']['id']]
        
        already_liked = []
        for i in range(0, len(track_ids), 50):
            batch = track_ids[i:i + 50]
            liked = sp.current_user_saved_tracks_contains(tracks=batch)
            already_liked.extend(liked)
        
        tracks_to_like = []
        for i, item in enumerate(tracks):
            if i < len(already_liked) and not already_liked[i]:
                tracks_to_like.append(item)
        
        print(f"\n🆕 New tracks to add: {len(tracks_to_like)}")
        print(f"✅ Already liked: {len(tracks) - len(tracks_to_like)}")
        
        if tracks_to_like:
            confirm = input(f"\nAdd {len(tracks_to_like)} tracks to your library? (y/n): ")
            if confirm.lower() == 'y':
                print("\n⏳ Adding tracks to your library...")
                like_tracks(sp, tracks_to_like)
                print(f"\n✅ Done! All tracks from the playlist are now in your library.")
            else:
                print("❌ Canceled")
        else:
            print("\n✅ All tracks from this playlist are already in your library!")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main() 
