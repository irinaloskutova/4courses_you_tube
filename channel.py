import os
import json
from googleapiclient.discovery import build

class Channel:
    api_key: str = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id):
        self.id = id

    def print_info(self):
        channel = Channel.youtube.channels().list(id=self.id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
vdud.print_info()