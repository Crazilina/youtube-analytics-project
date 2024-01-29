import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.video_data = self.get_video_data()
        if self.video_data and 'items' in self.video_data and len(self.video_data['items']) > 0:
            item = self.video_data['items'][0]
            self.title = item['snippet']['title']
            self.views = int(item['statistics'].get('viewCount', 0))
            self.likes = int(item['statistics'].get('likeCount', 0))
            self.link = f"https://www.youtube.com/watch?v={self.video_id}"
        else:
            self.title = ''
            self.views = 0
            self.likes = 0
            self.link = ''

    def get_video_data(self) -> dict:
        """Получает данные о видео с YouTube API."""
        request = self.youtube.videos().list(
            id=self.video_id,
            part='snippet,statistics'
        )
        return request.execute()

    def __str__(self) -> str:
        return self.title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
