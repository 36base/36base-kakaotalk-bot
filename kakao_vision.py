import requests


API_URL = 'https://kapi.kakao.com/v1/vision/adult/detect'
APP_KEY = ''


def detect_adult(image_url):
    headers = {'Authorization': 'KakaoAK {}'.format(APP_KEY)}
    data = {'image_url': image_url}
    resp = requests.post(API_URL, headers=headers, data=data)
    if resp.status_code == 200:
        return resp.json()['result']
    else:
        return {}
