import os
import datetime
import requests


API_URL = 'https://kapi.kakao.com/v1/vision/adult/detect'
APP_KEY = ''
API_STATUS = 1
API_STATUS_UPDATE = datetime.date.today()
ERROR_MSG = {
    -10: "오늘 최대 이용횟수를 초과했습니다. 내일 다시 시도해주세요.",
    -603: "이미지 로딩 시간초과. 더 작은 크기의 이미지를 사용해주세요.",
    -911: "지원하지 않는 이미지 포맷입니다. jpg와 png만 보내주세요."
}


def _save_image(url):
    today = datetime.date.today()
    resp = requests.get(url)
    if resp.status_code == 200:
        os.makedirs(f"image/{today}", exist_ok=True)
        with open(f"image/{today}/{os.path.split(url)[1]}", "wb") as f:
            f.write(resp.content)
    return


def detect_adult(image_url):
    _save_image(image_url)

    global API_STATUS
    global API_STATUS_UPDATE
    if datetime.date.today() != API_STATUS_UPDATE:
        API_STATUS = 1
        API_STATUS_UPDATE = datetime.date.today()
    elif API_STATUS:
        pass
    elif os.path.splitext(image_url)[1] not in ['png', 'jpg', 'jpeg']:
        return {'msg': '지원하지 않는 이미지 포맷입니다. jpg와 png만 보내주세요.'}
    else:
        return {'msg': '오늘 최대 이용횟수를 초과했습니다. 내일 다시 시도해주세요.'}
    headers = {'Authorization': f'KakaoAK {APP_KEY}'}
    data = {'image_url': image_url}
    resp = requests.post(API_URL, headers=headers, data=data)
    result = resp.json()
    if resp.status_code == 400:
        result['msg'] = ERROR_MSG.get(result['code'], result['msg'])
        if result['code'] == -10:
            API_STATUS = 0
    return result
