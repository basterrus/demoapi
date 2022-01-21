import requests
import json

from core.settings import API_KEY  # наверное в идеале импортировать из глобального settings


def search_track(text):
    search_url = f'http://ws.audioscrobbler.com/2.0/?method=track.search&track={text}&api_key={API_KEY}&format=json'
    response = requests.get(search_url).json()
    return response


def response_handler(response):
    print(response)


if __name__ == '__main__':
    search_track('Money')

