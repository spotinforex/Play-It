import logging

logging.basicConfig(level=logging.INFO)

def fetch_spotify_playlist(sp, playlist_url):
    """
    Function for fetching Spotify Playlist
    Args:
      sp: Spotify client (Spotipy)
      playlist_url: link to the spotify playlist
    Returns:
      tracks: list of playlist information
    """
    try:
        logging.info("Fetching Spotify Playlist...")
        playlist_id = playlist_url.split("/")[-1].split("?")[0]

        results = sp.playlist_items(
            playlist_id,
            additional_types=["track"],
            limit=10
        )
        logging.info(f"Spotify Playlist Fetched Successfully: {results}")

        tracks = []
        for item in results.get("items", []):  # safe lookup
            track = item.get("track")
            if not track:
                continue
            title = track.get("name", "Unknown Title")
            artist = track.get("artists", [{}])[0].get("name", "Unknown Artist")
            duration = track.get("duration_ms", 0) // 1000
            tracks.append({"title": title, "artist": artist, "duration": duration})
        logging.info(f"Tracks Appended Successfully: {tracks}")

        return tracks
    except Exception as e:
        logging.exception("Error while fetching Spotify playlist")
        return []

