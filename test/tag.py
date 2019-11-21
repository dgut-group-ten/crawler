import requests

url2 = "https://music-02.niracler.com:8000/playlist/"
data = {
    "lid": 200010148222,
    "name": '你要勇敢去爱',
    "stags": '华语 流行 治愈',
    "description": 'sacasc',
}
print(data)

try:
    r = requests.post(url2, data=data)
    print(r.text)
except Exception as e:
    print(str(e))
