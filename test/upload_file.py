import json

import requests


def upload_song(cover_path):
    url = "http://localhost:8000/song/"
    data = {
        "name": cover_path.split('.')[0],
    }
    try:
        files = {'file': open(cover_path, 'rb')}
        r = requests.post(url, files=files, data=data)
        print(r.text)
    except Exception as e:
        print("here " + str(e))


if __name__ == '__main__':
    upload_song('demo.json')
