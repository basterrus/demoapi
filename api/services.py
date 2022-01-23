import requests
from core.settings import API_KEY  # наверное в идеале импортировать из глобального settings


def get_data_pages(track_name):
    data = {}
    search_url = f'http://ws.audioscrobbler.com/2.0/?method=track.search&track={track_name}&api_key={API_KEY}&format=json'
    response = requests.get(search_url).json()
    total_search_page = int(response["results"]["opensearch:itemsPerPage"])
    # for i in range(1, total_search_page + 1):
    for i in range(1, 2):
        search_url = f'http://ws.audioscrobbler.com/2.0/?method=track.search&track={track_name}&api_key={API_KEY}&format=json&page={i}'
        response = requests.get(search_url).json()
        data[f"{i}"] = response["results"]["trackmatches"]
    return data


def search_track(track_name):
    result = get_data_pages(track_name)
    search_data = []
    count = 0
    for i in range(1, len(result) + 1):
        items = result[f'{i}']
        for item in items["track"]:
            name = item["name"]
            artist = item["artist"]
            url = item["url"]
            # playlist_name = int(pk)
            # search_data.append(
                # {"track_name": name, "track_singer": artist, "track_url": url, "playlist_name": ""})
            search_data.append({"track_name": name, "track_singer": artist, "track_url": url})
            count += 1
    print(search_data)
    return search_data


# if __name__ == '__main__':
#     search_track("Money")
