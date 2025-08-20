from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auth.spotify import get_spotify_client
from auth.youtube import get_youtube_client
from services.spotify_service import fetch_spotify_playlist
from services.youtube_service import YoutubeHandler
from utils.matcher import search_and_match
import logging
import spotipy

logging.basicConfig(level = logging.INFO)

app = FastAPI(title = "Spotify to Youtube Migrator")

# Request Model for Migration
class MigrateRequest(BaseModel):
    spotify_playlist_url: str
    youtube_playlist_name: str
    access_token: str

@app.get("/")
def home():
    return{ "message": "Spotify - Youtube Migrator API is Running"}

@app.get("/spotify_auth")
def spotify_auth_url():
        sp = get_spotify_client()
        auth_url = sp.get_authorize_url()
        logging.info(f"Spotify Auth Url {auth_url}")
        return {"auth_url": auth_url}


@app.get("/callback")
def spotify_callback(code: str):
    """
    Spotify redirects here after login.
    Example: /callback?code=ABCD1234
    """
    try:
        sp_auth = get_spotify_client()
        token_info = sp_auth.get_access_token(code)   # ✅ Use the actual code
        logging.info("Spotify authentication successful")
        return {
            "access_token": token_info['access_token'],
            "expires_in": token_info['expires_in'],
            "refresh_token": token_info.get('refresh_token')
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/playlist/migrate")
def migrate_playlist(req: MigrateRequest):
    try:
        sp = spotipy.Spotify(auth=req.access_token)
        yt = get_youtube_client()


        tracks = fetch_spotify_playlist(sp, req.spotify_playlist_url)

        yt_class = YoutubeHandler()
        yt_playlist_id = yt_class.create_youtube_playlist(yt, req.youtube_playlist_name)

        migrated, missing = 0, []
        for track in tracks:
            video_id = search_and_match(yt, track)
            if video_id:
                yt_class.add_track_to_youtube(yt, yt_playlist_id, video_id)

                migrated += 1

            else:
                missing.append(track)


        return {
              "status": "success",
              "youtube_playlist_url": f"https://youtube.com/playlist?list={yt_playlist_id}",
              "migrated": migrated,
              "missing": missing
              }

    except Exception as e:
          raise HTTPException(status_code = 500, detail = str(e))
