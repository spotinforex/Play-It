from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import config
import logging

logging.basicConfig(level = logging.INFO)

def get_youtube_client():
    ''' Function For YouTube Authenication
    Returns:
      Youtube Authenication
    '''
    try:
        logging.info("YouTube Authenication Initialized")
        flow = InstalledAppFlow.from_client_secrets_file(
                config.YOUTUBE_CLIENT_SECRET_FILE,
                config.YOUTUBE_SCOPES)

        creds = flow.run_local_server(port = 8080)
        return build("youtube", "v3", credentials = creds)

    except Exception as e:
        logging.exception(f"An Error Occurred During Youtube Authenication")
