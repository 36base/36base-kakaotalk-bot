from flask import Flask, request, jsonify
from chatterbox import Chatter, Text, Keyboard, MessageButton
import girlsfrontline_core_python as GFLCore
import re
import logging
from logging_sqlite import SQLiteHandler
from ranking_poll import EventRankPoll

application = Flask(__name__)

chatter = Chatter(memory='sqlite',
                  frequency=20,
                  fallback=True)

# Logging 모듈 설정
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

# 핸들러 설정 및 추가
db_handler = SQLiteHandler('log.db')
logger.addHandler(db_handler)


# 정규식 컴파일
re_build_time = re.compile(r"^([0-9]{1,2})?[ :]?([0-5][0-9])$")
re_rp_calc = re.compile(r"([0-9]{1,3})[ ,.]([0-9]{1,3})[ ,.]?([0-9]+)?[ ,.]?(서약|ㅅㅇ)?[ ,.]?(요정|ㅇㅈ)?")
re_rank_poll = re.compile(r"([0-9]{0,6})(점)?[ .,\n]([0-9]{1,3})(퍼|퍼센트|%)?[ .,\n]?$")

# RankingPoll
rank = EventRankPoll("rank_beta", "20180810")


# Chatterbox


# 초기 화면 설정
@chatter.base(name='홈')
def home_keyboard():
    home_buttons = ['인형 검색', '장비 검색', '작전보고서 계산', '군수지원 계산기', '36베이스 바로가기', '랭킹 집계']
    return Keyboard(home_buttons)


# 유저의 현재 state가 src이고 input으로 받은 데이터에서 content가 action일 때,
# func 함수를 실행하고 유저의 state를 dest로 변경합니다.
# state를 활용하여 1 depth 이상의 자동응답 시나리오를 구성할 수 있습니다.
# src = 현재 상태(status)
# action = 유저가 입력한 것
# dest = 다음 상태(status)


@chatter.rule(action='인형 검색', src='홈', dest='인형 검색 페이지')
def search_doll(data):
    msg = (
        '인형 검색을 시작합니다.'
        '2자리에서 4자리의 숫자로 입력해주세요\n'
        '예시) 110 또는 0730'
    )
    extra_data = dict(user_status='홈', user_key=data['user_key'], content=data['content'])
    logger.info(msg, extra=extra_data)
    return Text(msg) + Keyboard(type='text')


@chatter.rule(action='*', src='인형 검색 페이지', dest='홈')
def serched_doll(data):
    re_match = re_build_time.match(data['content'])
    if re_match:
        b_hour, b_min = re_match.groups(default='0')
        build_time = int(b_hour) * 3600 + int(b_min) * 60
        searched = GFLCore.doll_find_all(buildTime=build_time)
        dolls = ["{0}: {1}성 {2}".format(n.get('krName', n['name']), n['rank'], n['type'].upper()) for n in searched]
        if dolls:
            msg = "찾은 인형 목록:\n{0}".format("\n".join(dolls))
        else:
            msg = "검색 결과가 없습니다."
    else:
        msg = "잘못된 입력입니다."
    extra_data = dict(user_status='인형 검색 페이지', user_key=data['user_key'], content=data['content'])
    logger.info(msg, extra=extra_data)
    return Text(msg) + chatter.home()


@chatter.rule(action='장비 검색', src='홈', dest='장비 검색 페이지')
def search_equip(data):
    msg = (
        '장비/요정 검색을 시작합니다.'
        '2자리에서 4자리의 숫자로 입력해주세요\n'
        '예시) 110 또는 0111'
    )
    extra_data = dict(user_status='홈', user_key=data['user_key'], content=data['content'])
    logger.info(msg, extra=extra_data)
    return Text(msg) + Keyboard(type='text')


@chatter.rule(action='*', src='장비 검색 페이지', dest='홈')
def serched_equip(data):
    re_match = re_build_time.match(data['content'])
    msg = "기본 메시지"
    if re_match and len(data['content']) < 5:
        b_hour, b_min = re_match.groups('0')
        build_time = int(b_hour) * 3600 + int(b_min) * 60
        if build_time < 3600:
            searched = GFLCore.equip_find_all(buildTime=build_time)
            equips = ["{0}: {1}성".format(n.get('krName', n['name']), n['rank']) for n in searched]
        else:
            searched = GFLCore.fairy_find_all(buildTime=build_time)
            equips = ["{0}".format(n.get('krName', n['name'])) for n in searched]

        if equips:
            msg = "찾은 장비/요정 목록:\n{0}".format("\n".join(equips))
        else:
            msg = "검색 결과가 없습니다."
    extra_data = dict(user_status='장비 검색 페이지', user_key=data['user_key'], content=data['content'])
    logger.info(msg, extra=extra_data)
    return Text(msg) + chatter.home()


@chatter.rule(action='작전보고서 계산', src='홈', dest='작전보고서 계산')
def calc_report(data):
    msg = (
        '작전보고서 계산기입니다\n'
        '(현재 레벨) (목표 레벨) [현재 경험치] [서약] [요정] '
        '순서로 입력하면 됩니다. 띄어쓰기 또는 쉼표로 구분합니다.'
        '서약 여부는 "서약"이라고 쓰면 됩니다.'
    )
    extra_data = dict(user_status='홈', user_key=data['user_key'], content=data['content'])
    logger.info(msg, extra=extra_data)
    return Text(msg) + Keyboard(type='text')


@chatter.rule(action='*', src='작전보고서 계산', dest='홈')
def calc_report_return(data):
    re_match = re_rp_calc.match(data['content'])
    if re_match:
        cur_lv, tar_lv, cur_xp, is_oath, is_fairy = re_match.groups(default='')
        cur_lv = int(cur_lv)
        tar_lv = int(tar_lv)
        cur_xp = int(cur_xp) if cur_xp else 0
        is_oath = True if is_oath else False
        is_fairy = True if is_fairy else False
        if cur_lv >= tar_lv or tar_lv > 120 or (tar_lv > 100 and is_fairy):
            msg = '올바르지 않은 입력값입니다.'
        else:
            rp = GFLCore.calc_exp(int(cur_lv), int(tar_lv), int(cur_xp), is_oath, is_fairy)
            msg = '필요 작전 보고서: {0}개'.format(rp)
    else:
        msg = "올바르지 않은 입력입니다."
    extra_data = dict(user_status='홈', user_key=data['user_key'], content=data['content'])
    logger.info(msg, extra=extra_data)
    return Text(msg) + chatter.home()


@chatter.rule(action='군수지원 계산기', src='홈', dest='홈')
def calc_support(data):
    msg = (
        "군수지원 계산기 바로가기"
    )
    msg_bt = MessageButton(
        label="여기를 눌러주세요",
        url="https://tempkaridc.github.io/gf/"
    )
    extra_data = dict(user_status='홈', user_key=data['user_key'], content=data['content'])
    logger.info(msg, extra=extra_data)
    return Text(msg) + msg_bt + chatter.home()


@chatter.rule(action='36베이스 바로가기', src='홈', dest='홈')
def go_to_36db(data):
    msg = (
        "36베이스 바로가기"
    )
    msg_bt = MessageButton(
        label="여기를 눌러주세요",
        url="https://girlsfrontline.kr/"
    )
    extra_data = dict(user_status='홈', user_key=data['user_key'], content=data['content'])
    logger.info(msg, extra=extra_data)
    return Text(msg) + msg_bt + chatter.home()


@chatter.rule(action='랭킹 집계', src='홈', dest='랭킹 집계')
def rank_poll(data):
    msg = (
        "(시험중입니다)\n이벤트 전역 랭킹 입력 기능을 시작합니다.\n"
        "(점수) (퍼센트) "
        "순서로 입력해주세요. 100위 이내는 0퍼센트로 작성해주세요.\n"
        "ex) 123456 78퍼"
    )
    extra_data = dict(user_status='홈', user_key=data['user_key'], content=data['content'])
    logger.info(msg, extra=extra_data)
    return Text(msg) + Keyboard(type='text')


@chatter.rule(action="*", src="랭킹 집계", dest="홈")
def rank_poll_input(data):
    re_match = re_rank_poll.match(data["content"])
    if re_match:
        score, _, percent, _ = re_match.groups()
        rank.log(data['user_key'], int(score), int(percent))
        msg = "등록이 완료되었습니다. 감사합니다."
    else:
        msg = (
            "올바른 포맷으로 입력해주세요."
            " 만약 제대로 입력했는데 이 오류가 발생했다면, 관리자에게 알려주세요."
        )
    extra_data = dict(user_status='랭킹 집계', user_key=data['user_key'], content=data['content'])
    logger.info(msg, extra=extra_data)
    return Text(msg) + chatter.home()


# ##################
# Flask Func


@application.route('/keyboard', methods=['GET'])
def keyboard():
    return jsonify(chatter.home())


@application.route('/message', methods=['POST'])
def message():
    return jsonify(chatter.route(request.json))


@application.route('/friend', methods=['POST'])
def add_friend():
    return jsonify({'message': 'SUCCESS'})


@application.route('/friend/<key>', methods=['DELETE'])
def block_friend(key):
    return jsonify({'message': 'SUCCESS'})


@application.route('/chat_room/<key>', methods=['DELETE'])
def exit_friend(key):
    return jsonify({'message': 'SUCCESS'})


if __name__ == '__main__':
    application.run(debug=True)
