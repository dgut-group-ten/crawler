import requests

lid = """3042446516
3042446517
3042446518
3042446519
3042446521
3042446522
3042446523
3042446524
3042446527
3042446528
3042446529
3042446530
3042446531
3042446532
3042446533
3042446534
3042446535
3042446536
3042446537
3042446538
3042446539
3042446540"""

headers = {
    "Token": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjM3LCJ3ZWIiOiJncm91cHRlbiIsImV4cCI6MTU3NTY4Mzg2MywiaWF0IjoxNTc1MDc5MDYzfQ.JmNbqCtvqIJltLUjVoB92bpwibBei3yjikFLKS4MlcQ'
}

for id in lid.split('\n'):
    url = "https://music-02.niracler.com:8000/playlist/" + id + '/'
    try:
        files = {'cimg': open('../tmp/default.jpg', 'rb')}
        r = requests.patch(url, files=files, headers=headers)
        print(r.text)
    except Exception as e:
        print(str(e))
    print(id)