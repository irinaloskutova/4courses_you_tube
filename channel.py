import os
import json
import isodate
from datetime import datetime
from datetime import timedelta

from googleapiclient.discovery import build


class Channel:
    api_key: str = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id):
        self.__channel_id = channel_id  #инициализирует id канала

        self.title = self.get_info().get('items')[0].get('snippet').get('title')  #инициализирует название канала
        self.description = self.get_info().get('items')[0].get('snippet').get('description')  #инициализирует описание канала
        self.subscriber_count = self.get_info().get('items')[0].get('statistics').get('subscriberCount') #инициализирует количество подписчиков
        self.video_count = self.get_info().get('items')[0].get('statistics').get('videoCount')  #инициализирует количество видео
        self.viewCount = self.get_info().get('items')[0].get('statistics').get('viewCount')  #инициализирует общее количество просмотров

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        if self.__channel_id == channel_id:
            self.__channel_id = channel_id
        else:
            raise ValueError('Нельзя менять название канала')

    def print_info(self):
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def get_info(self):
        """Получение информации о канале"""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel

    @property
    def url(self):
        """Записывает html адрес канала"""
        return f"https://www.youtube.com/channel/{self.get_info().get('items')[0].get('id')}"

    def to_json(self, title):
        """Запись полученной информации с сайта в файл json"""
        with open(title, 'w') as f:
            json.dump(self.get_info(), f, indent=3)

    @classmethod
    def get_service(cls):
        """Получение сервиса для работы с каналами"""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __repr__(self):
        """Получаем название канала в формате Youtube-канал: <название_канала>"""
        return f"Youtube-канал: {self.title}"

    def __len__(self):
        """Получаем количество видео"""
        return len(self.subscriber_count)

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count


class Video:

    def __init__(self, video):
        """Инициализируем класс по id видео, также инициализируем
        название, количество просмотров и лайков"""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)

        try:
            self.video = youtube.videos().list(id=video, part='snippet,contentDetails,statistics').execute()
            self.video_id = self.video["items"][0]["id"]
            self.video_title = self.video["items"][0]["snippet"]["title"]
            self.video_views = self.video["items"][0]["statistics"]["viewCount"]
            self.video_likes = self.video["items"][0]["statistics"]["likeCount"]
        except IndexError:
            self.video = video
            self.video_id = None
            self.video_title = None
            self.video_views = None
            self.video_likes = None

    def __repr__(self):
        """Получаем название канала в формате Youtube-канал: <название_канала>"""
        return f"Youtube-канал: {self.video_title}"


class PLVideo(Video):
    def __init__(self, video, playlist):
        """Инициализируем дочерний класс по id видео, и id плейлиста"""
        super().__init__(video)
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist = playlist
        self.playlist_name = self.get_playlist_name()

    def get_playlist_name(self):
        """Получаем название плейлиста"""
        self.playlist = self.youtube.playlists().list(id=self.playlist, part='snippet').execute()
        self.playlist_name = self.playlist['items'][0]['snippet']['title']
        return self.playlist_name

    def __repr__(self):
        """Переопределили метод репр в дочернем классе"""
        return f"{self.video_title} ({self.playlist_name})"


class PlayList:
    def __init__(self, playlist_id):
        """Инициализируем класс по id видео, также инициализируем
        название, количество просмотров и лайков"""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist_id = playlist_id
        self.playlist = youtube.playlists().list(id=playlist_id, part='snippet').execute()
        self.playlist_video = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails,snippet',
                                                           maxResults=50,).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_video['items']]
        self.videos = youtube.videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def to_json(self, title):
        """Запись полученной информации с сайта в файл json"""
        with open(title, 'w') as f:
            json.dump(self.videos, f, indent=3)

    @property
    def total_duration(self):
        duration_ = timedelta()
        total_duration_ = timedelta()
        for i in range(len(self.videos)+1):
            iso_8601_duration = self.videos['items'][i]['contentDetails']['duration']
            duration_ = isodate.parse_duration(iso_8601_duration)
            total_duration_ += duration_
        return total_duration_

    def total_seconds(self):
        return self.total_duration.seconds

    def show_best_video(self):
        videos = {}
        id_ = None
        likes = 0
        for i in range(len(self.playlist_video)+1):
            videos[self.videos['items'][i]['statistics']['likeCount']] = self.playlist_video['items'][i]
            if likes < int(self.videos['items'][i]['statistics']['likeCount']):
                likes = int(self.videos['items'][i]['statistics']['likeCount'])
                id_ = self.videos['items'][i]['id']
        return f"https://www.youtube.com/watch?v={id_}"


if __name__ == '__main__':
    broken_video = Video('broken_video_id')
    print(broken_video.video_title)

    print(broken_video.video_likes)



