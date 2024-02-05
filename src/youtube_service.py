import os
from googleapiclient.discovery import build


class YouTubeService:
    def __init__(self):
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
