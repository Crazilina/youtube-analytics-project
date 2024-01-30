import os
import isodate
import datetime
from googleapiclient.discovery import build
from src.video import Video


class PlayList:
    def __init__(self, playlist_id: str) -> None:
        self.playlist_id = playlist_id
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.playlist_data = self.get_playlist_data()
        self.videos = self.get_playlist_videos()

        if self.playlist_data:
            self.title = self.playlist_data['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        else:
            self.title = ''
            self.url = ''

    def get_playlist_data(self) -> dict:
        """Получает данные о плейлисте с YouTube API."""
        request = self.youtube.playlists().list(
            id=self.playlist_id,
            part='snippet'
        )
        return request.execute()

    def get_playlist_videos(self) -> list:
        """Получает список видео в плейлисте."""
        request = self.youtube.playlistItems().list(
            playlistId=self.playlist_id,
            part='snippet',
            maxResults=50
        )
        response = request.execute()
        videos = []
        for item in response.get('items', []):
            video_id = item['snippet']['resourceId']['videoId']
            videos.append(video_id)
        return videos

    def get_video_duration(self, video_id: str) -> datetime.timedelta:
        """Получает длительность видео по его video_id."""
        request = self.youtube.videos().list(
            id=video_id,
            part='contentDetails'
        )
        response = request.execute()
        if response['items']:
            iso_8601_duration = response['items'][0]['contentDetails']['duration']
            return isodate.parse_duration(iso_8601_duration)
        else:
            return datetime.timedelta()

    @property
    def total_duration(self) -> datetime.timedelta:
        """Вычисляет общую длительность видео в плейлисте."""
        total_duration = datetime.timedelta()
        for video_id in self.videos:
            video_duration = self.get_video_duration(video_id)
            total_duration += video_duration
        return total_duration

    def show_best_video(self) -> str:
        """Возвращает короткую ссылку на самое популярное видео в плейлисте (по количеству лайков)."""
        if not self.videos:
            return ''

        best_video = None
        max_likes = -1

        for video_id in self.videos:
            video = Video(video_id)
            if hasattr(video, 'likes') and video.likes is not None and video.likes > max_likes:
                max_likes = video.likes
                best_video = video

        return f"https://youtu.be/{best_video.video_id}" if best_video else ''
