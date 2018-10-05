from flask import Flask, request, jsonify
from chatterbox import *
import girlsfrontline_core_python as gfl_core
import re
import logging
import json
import pymysql

from logging_db import MySQLHandler
from ranking_poll import EventRankPoll
import static_resp as rp

application = Flask(__name__)

chatter = Chatter(memory='sqlite',
                  frequency=5,
                  fallback=False)

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
re_rp_calc = re.compile(
    r"([0-9]{1,3})[ ,.]([0-9]{1,3})[ ,.]?([0-9]+)?[ ,.]?(서약|ㅅㅇ)?[ ,.]?(요정|ㅇㅈ)?([화ㅎ][력ㄹ]([1]?[0-9])?)?"
)
re_rank_poll = re.compile(r"([0-9]{0,6})[점]? ([0-9]{1,3})(퍼센트|퍼|%|등|)[ ]?(.+)?$")

# RankingPoll
rank = EventRankPoll(conn)

# girlsfrontline_core_python
core = gfl_core.core.Core(cf['gfl_core']['dir'])


# Chatterbox


# 초기 화면 설정
@chatter.base(name='홈')
def home_keyboard():
    home_buttons = ['인형 검색', '장비 검색', '작전보고서 계산', '군수지원 계산기', '36베이스 바로가기', '자유 입력']
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
        # searched(dict): 코어에서 나온 객체들
        searched = [core.l10n("ko-KR", "doll", n) for n in core.doll.build_time.get(build_time, {})]
        dolls = ["{name}: {rank}성 {Type}".format(**n) for n in searched]
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
            searched = [core.l10n("ko-KR", "equip", n) for n in core.equip.build_time.get(build_time, {})]
            equips = ["{name}: {rank}성 {category_name}".format(**n) for n in searched]
        else:
            searched = [core.l10n("ko-KR", "fairy", n) for n in core.fairy.build_time.get(build_time, {})]
            equips = ["{name}".format(**n) for n in searched]

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
        cur_lv, tar_lv, cur_xp, is_oath, is_fairy, hoc, hoc_lv = re_match.groups(default='')
        cur_lv = int(cur_lv)
        tar_lv = int(tar_lv)
        cur_xp = int(cur_xp) if cur_xp else 0
        is_oath = True if is_oath else False
        is_fairy = True if is_fairy else False
        hoc = True if hoc else False
        hoc_lv = int(hoc_lv) if hoc_lv else 10
        if cur_lv >= tar_lv or tar_lv > 120:
            msg = '목표 레벨이 현재 레벨보다 낮거나 120을 넘습니다. 올바른 수치를 입력해주세요.'
        elif tar_lv > 100 and (is_fairy or hoc):
            msg = '요정 및 화력제대는 100레벨 이상의 계산을 지원하지 않습니다.'
        else:
            if hoc:
                hoc_lv = 10 if hoc_lv > 10 or hoc_lv < 0 else hoc_lv
                tar_lv = 100 if tar_lv > 100 else tar_lv
                rp, hr = gfl_core.calc.exp_hoc(cur_lv, tar_lv, cur_xp, hoc_lv)
                msg = '필요 특수 작전 보고서: {0}개\n소모시간: {1}시간\n소모 전지량: {2}개'.format(rp, hr, hr * 5)
            else:
                rp = gfl_core.calc.exp(int(cur_lv), int(tar_lv), int(cur_xp), is_oath, is_fairy)
                msg = '필요 작전 보고서: {0}개'.format(rp)
    else:
        msg = "올바르지 않은 입력입니다."
    extra_data = dict(user_status='작전보고서 계산', **data)
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
    last_data = rank.get_today(data["user_key"])
    if last_data:
        msg = rp.msg_rank_poll + (
            "\n\n오늘({0}) 입력한 마지막 기록을 덮어씌웁니다.\n"
            "{1}점, {2}%"
        ).format(*last_data[:3])
    else:
        msg = rp.msg_rank_poll
    extra_data = dict(user_status='홈', **data)
    logger.info(msg, extra=extra_data)
    return Text(msg) + rp.bt_info + Keyboard(type="text")


@chatter.rule(action="*", src="랭킹 집계", dest="홈")
def rank_poll_input(data):
    re_match = re_rank_poll.match(data["content"].strip())
    if re_match:
        score, num, mode, comment = re_match.groups()
        if 0 < int(num) <= 100:
            if mode in {"등"}:
                percent, ranking = 0, int(num)
                msg = "{0}점 {1}등으로 등록 완료했습니다. 감사합니다.".format(score, ranking)
            else:
                percent, ranking = int(num), 0
                msg = "{0}점 {1}%으로 등록 완료했습니다. 감사합니다.".format(score, percent)
            rank.log(data['user_key'], int(score), percent, ranking, comment)
        else:
            msg = rp.msg_rank_poll_err
    else:
        msg = (
            "올바른 양식으로 입력해주세요. "
            "만약 제대로 입력했는데 이 오류가 발생했다면, 관리자에게 알려주세요."
        )
    extra_data = dict(user_status='랭킹 집계', **data)
    logger.info(msg, extra=extra_data)
    return Text(msg) + rp.bt_ranking_result + chatter.home()


@chatter.rule(action="자유 입력", src="홈", dest="자유 입력")
def start_free_input(data):
    extra_data = dict(user_status='홈', **data)
    logger.info(rp.msg_start_free_input, extra=extra_data)
    return rp.start_free_input + Keyboard(type="text")


@chatter.rule(action="*", src="자유 입력")
def free_input_check(data):
    if data['content'] in {'돌아가기', '취소', '종료', '잘가', 'ㅂㅂ'}:
        return cancel(data)
    elif data['content'][:2] in {'ㅇㅎ', '인형', '제조'}:
        data['content'] = data['content'][2:]
        return searched_doll(data)
    elif data['content'][:2] in {'ㅈㅂ', '장비'}:
        data['content'] = data['content'][2:]
        return searched_equip(data)
    elif data['type'] == 'photo':
        return photo_input(data)
    else:
        return free_input(data)


@chatter.rule(dest="자유 입력")
def free_input(data):
    res = core.find_nickname(data["content"].strip(), "ko-KR")
    res_special = core.special(data["content"].strip())
    if res:
        if isinstance(res, tuple):
            msg = Text(rp.f_msg_free_input_info[res[0]].format(**res[1])) + MessageButton("상세 정보", res[1]['link'])
            if "photo" in res[1]:
                msg += Photo(**res[1]["photo"])
            adv = Keyboard(type="text")
        else:
            msg = Text("무엇을 찾으셨나요?")
            adv = Keyboard(buttons=res)
    elif res_special:
        msg = Message(**res_special)
        adv = Keyboard(type="text")
    else:
        msg = Text("잘 모르겠습니다. 다시 입력해주세요.")
        adv = Keyboard(type="text")
    extra_data = dict(user_status='자유 입력', **data)
    logger.info(msg['message'].get('text', msg['message'].get('photo', {"url": ""})['url']), extra=extra_data)
    return msg + adv


@chatter.rule(dest="홈")
def photo_input(data):
    msg = "사진은 아직 지원하지 않습니다."
    extra_data = dict(user_status='자유 입력', **data)
    logger.info(msg, extra=extra_data)
    return Text(msg) + chatter.home()


@chatter.rule(dest='홈')
def cancel(data):
    msg = '기본 화면으로 돌아갑니다.'
    extra_data = dict(user_status='자유 입력', **data)
    logger.info(msg, extra=extra_data)
    return Text(msg) + chatter.home()


@chatter.rule(action="*", src="홈", dest="홈")
def fallback(data):
    extra_data = dict(user_status='홈', **data)
    logger.info(rp.msg_fallback, extra=extra_data)
    return rp.fallback + chatter.home()


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
