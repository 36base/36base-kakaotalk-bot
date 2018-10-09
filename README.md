# 36base-kakaotalk-bot

## Introduce
36베이스의 카카오톡 플러스친구용 봇입니다. PR 언제나 환영합니다.

구동에 Flask + uWSGI + nginx, 채팅 기록 로깅 및 데이터 저장용으로 MySQL과 PyMySQL을 사용합니다.

## Features
- [x] 인형 제조 시간으로 검색
- [x] 장비 제조 시간으로 검색
- [x] 요정 제조 시간으로 검색
- [x] 작전보고서 계산기
- [x] 히든 전역 랭킹 정보 수집
- [x] 히든 전역 랭킹 정보 가공 및 배포
- [x] 인형/장비 상세정보 페이지 및 별명으로 인형 검색하기 추가
- [x] 히든 랭킹전 만료시 데이터 수집 날짜 변경하기?
- [x] 코어 2.0.x 대응을 위한 구조 변경
- [x] 유용한 링크 목록 더 써넣기
- [ ] 기타 등등

## Requirements
```
Flask
chatterbox.py
PyMySQL
requests
emoji
```

`python 3.6` 버전에서의 정상작동만을 보장합니다.
