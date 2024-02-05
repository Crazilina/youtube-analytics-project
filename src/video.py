from .youtube_service import YouTubeService


class Video(YouTubeService):
    def __init__(self, video_id: str) -> None:
        super().__init__()  # Инициализация YouTube API через базовый класс
        self.video_id = video_id
        self.title = None  # Инициализация свойств значением None
        self.views = None
        self.like_count = None
        self.link = None

        self.video_data = self.get_video_data()

        if self.video_data:  # Проверяем, не None ли возвращено
            items = self.video_data.get('items', [])
            if items:
                item = items[0]
                self.title = item.get('snippet', {}).get('title')
                self.views = int(item.get('statistics', {}).get('viewCount', 0))
                self.like_count = int(item.get('statistics', {}).get('likeCount', 0))
                self.link = f"https://www.youtube.com/watch?v={self.video_id}"
            # Если self.video_data is None, свойства уже инициализированы как None

    def get_video_data(self) -> dict:
        try:
            request = self.youtube.videos().list(
                id=self.video_id,
                part='snippet,statistics'
            )
            return request.execute()
        except Exception as e:
            print(f"Error fetching video data for ID {self.video_id}: {e}")
            return None  # Оставляем возвращение None в случае исключения

    def __str__(self) -> str:
        return self.title if self.title else "No title available"


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
