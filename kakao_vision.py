import os
import requests


API_URL = 'https://kapi.kakao.com/v1/vision/adult/detect'
APP_KEY = ''


def _save_image(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(f"image/{os.path.split(url)[1]}", "wb") as f:
            f.write(resp.content)
    return


def detect_adult(image_url):
    _save_image(image_url)
    headers = {'Authorization': f'KakaoAK {APP_KEY}'}
    data = {'image_url': image_url}
    resp = requests.post(API_URL, headers=headers, data=data)
    return resp.json()
