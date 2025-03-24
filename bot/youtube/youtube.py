import time
import random
import logging
from httplib2 import HttpLib2Error
from http.client import (
    NotConnected,
    IncompleteRead,
    ImproperConnectionState,
    CannotSendRequest,
    CannotSendHeader,
    ResponseNotReady,
    BadStatusLine,
)

from apiclient import http, errors, discovery
from googleapiclient.errors import HttpError
from bot.config import Config  # Import Config class

log = logging.getLogger(__name__)

class MaxRetryExceeded(Exception):
    pass

class UploadFailed(Exception):
    pass

class YouTube:

    MAX_RETRIES = 10

    RETRIABLE_EXCEPTIONS = (
        HttpLib2Error,
        IOError,
        NotConnected,
        IncompleteRead,
        ImproperConnectionState,
        CannotSendRequest,
        CannotSendHeader,
        ResponseNotReady,
        BadStatusLine,
    )

    RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

    def __init__(self, auth: discovery.Resource, chunksize: int = -1):
        self.youtube = auth
        self.request = None
        self.chunksize = chunksize
        self.response = None
        self.error = None
        self.retry = 0

    def upload_video(
        self, video: str, properties: dict, progress: callable = None, *args
    ) -> dict:
        """Uploads a video to YouTube and adds it to a playlist (if specified)."""
        self.progress = progress
        self.progress_args = args
        self.video = video
        self.properties = properties

        body = dict(
            snippet=dict(
                title=self.properties.get("title"),
                description=self.properties.get("description"),
                categoryId=self.properties.get("category"),
            ),
            status=dict(privacyStatus=self.properties.get("privacyStatus")),
        )

        media_body = http.MediaFileUpload(
            self.video,
            chunksize=self.chunksize,
            resumable=True,
        )

        self.request = self.youtube.videos().insert(
            part=",".join(body.keys()), body=body, media_body=media_body
        )
        self._resumable_upload()
        return self.response

    def _resumable_upload(self) -> dict:
        """Handles resumable video uploads to YouTube."""
        response = None
        while response is None:
            try:
                status, response = self.request.next_chunk()
                if response is not None:
                    if "id" in response:
                        self.response = response
                        video_id = response["id"]  # Extract uploaded video ID
                        self.add_video_to_playlist(video_id)  # Add to playlist
                    else:
                        self.response = None
                        raise UploadFailed(
                            "The file upload failed with an unexpected response:{}".format(
                                response
                            )
                        )
            except errors.HttpError as e:
                if e.resp.status in self.RETRIABLE_STATUS_CODES:
                    self.error = "A retriable HTTP error {} occurred:\n {}".format(
                        e.resp.status, e.content
                    )
                else:
                    raise
            except self.RETRIABLE_EXCEPTIONS as e:
                self.error = "A retriable error occurred: {}".format(e)

            if self.error is not None:
                log.debug(self.error)
                self.retry += 1

                if self.retry > self.MAX_RETRIES:
                    raise MaxRetryExceeded("No longer attempting to retry.")

                max_sleep = 2 ** self.retry
                sleep_seconds = random.random() * max_sleep

                log.debug(
                    "Sleeping {} seconds and then retrying...".format(sleep_seconds)
                )
                time.sleep(sleep_seconds)

    def add_video_to_playlist(self, video_id: str):
        """
        Adds an uploaded video to a specified YouTube playlist.

        :param video_id: The ID of the uploaded video.
        """
        if not Config.PLAYLIST_ID:
            log.debug("No PLAYLIST_ID specified. Skipping playlist addition.")
            return

        try:
            request = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": Config.PLAYLIST_ID,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            response = request.execute()
            log.debug(f"✅ Video {video_id} added to playlist {Config.PLAYLIST_ID}.")

        except HttpError as e:
            log.error(f"❌ Failed to add video to playlist: {e}")

    def upload_thumbnail(self, video_id: str, thumbnail_path: str) -> dict:
        """Uploads a thumbnail for the given video ID."""
        try:
            youtube_thumbnails = self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=http.MediaFileUpload(thumbnail_path)
            )
            response = youtube_thumbnails.execute()
            log.debug(f"Thumbnail uploaded successfully for video {video_id}")
            return response
        except errors.HttpError as e:
            log.error(f"Failed to upload thumbnail: {e}")
            return {"error": str(e)}

def print_response(response: dict) -> None:
    """Prints the API response."""
    for key, value in response.items():
        print(key, " : ", value, "\n\n")
