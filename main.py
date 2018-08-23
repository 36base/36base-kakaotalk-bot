from flask import Flask, request, jsonify
from chatterbox import *
import girlsfrontline_core_python as GFLCore
import re
import logging
import json
import pymysql

from logging_db import MySQLHandler
from ranking_poll import EventRankPoll
import static_resp as rp

application = Flask(__name__)

chatter = Chatter(memory='sqlite',
                  frequency=20,
                  fallback=True)

with open("config.json", "r", encoding="utf-8") as f:
    cf = json.load(f)

# MySQL Connection
conn = pymysql.connect(**cf["MySQL"])

# Logging 모듈 설정
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

# 핸들러 설정 및 추가
db_handler = MySQLHandler(conn)
logger.addHandler(db_handler)


# 정규식 컴파일
re_build_time = re.compile(r"^([0-9]{1,2})?[ :]?([0-5][0-9])$")
re_rp_calc = re.compile(r"([0-9]{1,3})[ ,.]([0-9]{1,3})[ ,.]?([0-9]+)?[ ,.]?(서약|ㅅㅇ)?[ ,.]?(요정|ㅇㅈ)?")
re_rank_poll = re.compile(r"([0-9]{0,6})[점]?[ .,]([0-9]{1,3})(퍼|퍼센트|%)?[ .,]?([0-9]{1,3})?[등]?[\n ]?(.+)?$")

# RankingPoll
rank = EventRankPoll(conn)


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
    extra_data = dict(user_status='홈', **data)
    logger.info(rp.msg_search_doll, extra=extra_data)
    return rp.search_doll


@chatter.rule(action='*', src='인형 검색 페이지', dest='홈')
def searched_doll(data):
    re_match = re_build_time.match(data['content'].strip())
    if re_match:
        b_hour, b_min = re_match.groups(default='0')
        build_time = int(b_hour) * 3600 + int(b_min) * 60
        searched = GFLCore.doll_find_all(buildTime=build_time)
        dolls = ["{0}: {1}성 {2}".format(n.get('krName', n['name']), n['rank'], n['type'].upper()) for n in searched]
        if dolls and build_time > 0:
            msg = "찾은 인형 목록:\n{0}".format("\n".join(dolls))
        else:
            msg = "검색 결과가 없습니다."
    else:
        msg = "올바르지 않은 입력입니다."
    extra_data = dict(user_status='인형 검색 페이지', **data)
    logger.info(msg, extra=extra_data)
    return Text(msg) + chatter.home()


@chatter.rule(action='장비 검색', src='홈', dest='장비 검색 페이지')
def search_equip(data):
    extra_data = dict(user_status='홈', **data)
    logger.info(rp.msg_search_equip, extra=extra_data)
    return rp.search_equip


@chatter.rule(action='*', src='장비 검색 페이지', dest='홈')
def searched_equip(data):
    re_match = re_build_time.match(data['content'].strip())
    if re_match:
        b_hour, b_min = re_match.groups('0')
        build_time = int(b_hour) * 3600 + int(b_min) * 60
        if build_time < 3600:
            searched = GFLCore.equip_find_all(buildTime=build_time)
            equips = ["{0}: {1}성 {2}".format(n.get('krName', n['name']), n['rank'], GFLCore.GFLCore.eq_nm[n["type"]])
                      for n in searched]
        else:
            searched = GFLCore.fairy_find_all(buildTime=build_time)
            equips = ["{0}".format(n.get('krName', n['name'])) for n in searched]

        if equips and build_time > 0:
            msg = "찾은 장비/요정 목록:\n{0}".format("\n".join(equips))
        else:
            msg = "검색 결과가 없습니다."
    else:
        msg = "올바르지 않은 입력입니다."
    extra_data = dict(user_status='장비 검색 페이지', **data)
    logger.info(msg, extra=extra_data)
    return Text(msg) + chatter.home()


@chatter.rule(action='작전보고서 계산', src='홈', dest='작전보고서 계산')
def calc_report(data):
    extra_data = dict(user_status='홈', **data)
    logger.info(rp.msg_calc_report, extra=extra_data)
    return rp.calc_report


@chatter.rule(action='*', src='작전보고서 계산', dest='홈')
def calc_report_return(data):
    re_match = re_rp_calc.match(data['content'].strip())
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
    extra_data = dict(user_status='홈', **data)
    logger.info(msg, extra=extra_data)
    return Text(msg) + chatter.home()


@chatter.rule(action='군수지원 계산기', src='홈', dest='홈')
def calc_support(data):
    extra_data = dict(user_status='홈', **data)
    logger.info(rp.msg_calc_support, extra=extra_data)
    return rp.calc_support + chatter.home()


@chatter.rule(action='36베이스 바로가기', src='홈', dest='홈')
def go_to_36db(data):
    extra_data = dict(user_status='홈', **data)
    logger.info(rp.msg_go_to_36db, extra=extra_data)
    return rp.go_to_36db + chatter.home()


@chatter.rule(action='랭킹 집계', src='홈', dest='랭킹 집계')
def rank_poll(data):
    extra_data = dict(user_status='홈', **data)
    logger.info(rp.msg_rank_poll, extra=extra_data)
    last_data = rank.get_today(data["user_key"])
    if last_data:
        msg = (
            "\n\n오늘({0}) 입력한 마지막 기록을 덮어씌웁니다.\n"
            "{1}점, {2}%"
        ).format(*last_data[:3])
    else:
        msg = ""
    return Text(rp.msg_rank_poll + msg) + Keyboard(type="text")


@chatter.rule(action="*", src="랭킹 집계", dest="홈")
def rank_poll_input(data):
    re_match = re_rank_poll.match(data["content"].strip())
    if re_match:
        score, percent, _, ranking, comment = re_match.groups()
        ranking = int(ranking) if ranking else None
        rank.log(data['user_key'], int(score), int(percent), ranking, comment)
        msg = "등록이 완료되었습니다. 감사합니다."
    else:
        msg = (
            "올바른 포맷으로 입력해주세요. "
            "만약 제대로 입력했는데 이 오류가 발생했다면, 관리자에게 알려주세요."
        )
    extra_data = dict(user_status='랭킹 집계', **data)
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
    application.run(debug=True, host='0.0.0.0')
