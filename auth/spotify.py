import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config
import logging

logging.basicConfig(level = logging.INFO)

def get_spotify_client():
    '''
    Function to Access Spotify API
    Returns:
      Authenication
    '''
    try:
        logging.info('Spotify Authenication Initialized ')
        sp = SpotifyOAuth(
              client_id = config.SPOTIFY_CLIENT_ID,
              client_secret = config.SPOTIFY_CLIENT_SECRET,
              redirect_uri = config.SPOTIFY_REDIRECT_URL,
              scope = "playlist-read-private playlist-read-collaborative")
        return sp
    except Exception as e:
        logging.exception(f"An Error Occurred During Spotify Authenication")

