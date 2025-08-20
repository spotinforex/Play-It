import logging

logging.basicConfig(level=logging.INFO)

class YoutubeHandler:
    ''' Class For Handling Youtube Processes '''

    def create_youtube_playlist(self, yt, title, description="Migrated From Spotify"):
        '''
        Function For Creating Youtube Playlist
        Args:
            yt: User Youtube Authentication
            title: Preferred Playlist Name
            description: Playlist description
        Returns:
            playlist_id
        '''
        try:
            logging.info('Creating Youtube Playlist')
            request = yt.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {"title": title, "description": description},
                    "status": {"privacyStatus": "private"}
                }
            )
            response = request.execute()
            logging.info("Playlist Created Successfully")
            return response["id"]

        except Exception as e:
            logging.exception(f"An Error Occurred During Playlist Creation")
            raise

    def add_track_to_youtube(self, yt, playlist_id, video_id):
        '''
        Function For Adding Tracks To The Youtube Playlist
        Args:
            yt: User Youtube Authentication
            playlist_id: ID of the newly created playlist
            video_id: ID of a video of the track
        '''
        try:
            logging.info("Adding Songs To Playlist")
            yt.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()
            logging.info("Songs Added Successfully")
        except Exception as e:
            logging.exception(f"An Error Occurred While Adding Songs to Playlist")

