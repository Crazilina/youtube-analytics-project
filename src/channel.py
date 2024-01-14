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
        self.channel_id = channel_id
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.channel_data = self.get_channel_data()

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
