import os
import json
from googleapiclient.discovery import build
from accessify import private, protected

class Channel:
    api_key: str = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id):
        self.__channel_id = channel_id  #инициализирует id канала

        self.title = self.get_title()  #инициализирует название канала
        self.description = self.get_description()  #инициализирует описание канала
        self.url = self.get_url()  #инициализирует ссылку на канал
        self.subscriber_count = self.get_subscriber_count()  #инициализирует количество подписчиков
        self.video_count = self.get_video_count()  #инициализирует количество видео
        self.viewCount = self.get_viewCount  #инициализирует общее количество просмотров

    # @private
    @property
    def channel_id(self):
        return self.__channel_id

    # @private
    @channel_id.setter
    def channel_id(self, channel_id):
        self.__channel_id = channel_id

    def print_info(self):
        channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def get_info(self):
        """Получение информации о канале"""
        channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel

    def get_title(self):
        """Получение названия канала"""
        return self.get_info().get('items')[0].get('snippet').get('title')

    def get_video_count(self):
        """Получение количества видеороликов канала"""
        return self.get_info().get('items')[0].get('statistics').get('viewCount')

    def get_description(self):
        """Получение описания канала"""
        return self.get_info().get('items')[0].get('snippet').get('description')

    def get_subscriber_count(self):
        """Получение количества подписчиков канала"""
        return self.get_info().get('items')[0].get('statistics').get('subscriberCount')

    def get_viewCount(self):
        """Получение количества просмотров канала"""
        return self.get_info().get('items')[0].get('statistics').get('viewCount')

    def get_url(self):
        """Записывает html адрес  канала"""
        return f"https://www.youtube.com/channel/{self.get_info().get('items')[0].get('id')}"

    def to_json(self, title):
        """Запись полученной инфы с сайта в файл json"""
        with open(title, 'w') as f:
            json.dump(self.get_info(), f, indent=3)

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __repr__(self):
        """Получаем название канала в формате Youtube-канал: <название_канала>"""
        return f"Youtube-канал: {self.get_title()}"

    def __len__(self):
        return len(self.get_subscriber_count())

    def __add__(self, other):
        return self.get_subscriber_count() + other.get_subscriber_count()

    def __gt__(self, other):
        return self.get_subscriber_count() > other.get_subscriber_count()

vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
# print(vdud.print_info())
# print(vdud.get_info())
# print(vdud.get_title())

# # получаем значения атрибутов
# print(vdud.title)
# вДудь
# print(vdud.video_count)
# print(vdud.subscriber_count)
# 163
# print(vdud.url)
# https://www.youtube.com/channel/UCMCgOm8GZkHp8zJ6l7_hIuA
#
# # менять не можем
# vdud.channel_id= 'Новое название'
# print(vdud.channel_id)
# AttributeError: property 'channel_id' of 'Channel' object has no setter
#
# # можем получить объект для работы с API вне класса
# print(Channel.get_service())
# <googleapiclient.discovery.Resource object at 0x000002B1E54F9750>

# создать файл 'vdud.json' в данными по каналу
# vdud.to_json('vdud.json')

ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
# print(ch1)
# print(ch2)
print(ch1 < ch2)
print(ch1 > ch2)
print(ch1 + ch2)
