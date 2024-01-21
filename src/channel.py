import os
import json
from googleapiclient.discovery import build


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._channel_id = channel_id
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.channel_data = self.get_channel_data()

        item = self.channel_data['items'][0]
        self.title = item['snippet']['title']
        self.description = item['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(item['statistics'].get('subscriberCount', 0))
        self.video_count = int(item['statistics'].get('videoCount', 0))
        self.view_count = int(item['statistics'].get('viewCount', 0))

    @property
    def channel_id(self):
        return self._channel_id

    def get_channel_data(self):
        """Получает полные данные о канале с YouTube API, включая общую структуру ответа."""
        request = self.youtube.channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        )
        return request.execute()

    def print_info(self) -> None:
        """Выводит в консоль полную информацию о канале."""
        if self.channel_data:
            printj(self.channel_data)
        else:
            print("Channel information not found.")

    @classmethod
    def get_service(cls):
        """ Класс-метод для получения объекта работы с YouTube API """
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename: str) -> None:
        """ Сохраняет данные канала в файл формата JSON """
        channel_info = {
            'id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(channel_info, file, ensure_ascii=False, indent=2)
