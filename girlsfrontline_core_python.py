import json
import math


class GFLCore:
    with open("data/doll.json", 'r', encoding='utf-8') as f:
        doll = json.load(f)

    with open("data/equip.json", 'r', encoding='utf-8') as f:
        equip = json.load(f)

    with open("data/fairy.json", 'r', encoding='utf-8') as f:
        fairy = json.load(f)

    with open("data/exp.json", "r", encoding='utf-8') as f:
        exp_doll = json.load(f)
        exp_fairy = [n * 3 for n in exp_doll]


def doll_find(**kwargs):
    """고유한 조건으로 인형 정보를 찾을때 사용(id, name 등등)

    Args:
        kwargs(Any): id, name 등의 값만 받음

    Return:
        doll_info(dict): 해당 인형의 정보
    """
    # if not {"id", "name", "krName"}.issuperset(set(kwargs.keys())):
    #     return {}
    for doll in GFLCore.doll:
        if doll.items() >= kwargs.items():
            return doll
    else:
        return {}


def doll_find_all(**kwargs):
    """조건에 맞는 인형 데이터를 전부 list 로 반환. 해당 조건에 중복되는 인형이 있을때만 사용

    Args:
        **kwargs(Any): doll.json 내 인형 정보

    Return:
        ret(list): 검색된 인형들의 정보를 list 에 담아 반환
    """
    ret = []
    for doll in GFLCore.doll:
        if doll.items() >= kwargs.items():
            ret.append(doll)
        else:
            continue
    return ret


def equip_find(**kwargs):
    for equip in GFLCore.equip:
        if equip.items() >= kwargs.items():
            return equip
    else:
        return {}


def equip_find_all(**kwargs):
    """조건에 맞는 장비 데이터를 전부 list 로 반환. 해당 조건에 중복되는 장비가 있을때만 사용 권장

    Args:
        **kwargs(Any): equip.json 내 장비 정보

    Return:
        ret(list): 검색된 장비들의 정보(dict)를 list 에 담아 반환
    """
    ret = []
    for equip in GFLCore.equip:
        if equip.items() >= kwargs.items():
            ret.append(equip)
        else:
            continue
    return ret


def fairy_find(**kwargs):
    for fairy in GFLCore.fairy:
        if fairy.items() >= kwargs.items():
            return fairy
    else:
        return {}


def fairy_find_all(**kwargs):
    """조건에 맞는 요정 데이터를 전부 list 로 반환. 해당 조건에 중복되는 장비가 있을때만 사용 권장

    Args:
        **kwargs(Any): equip.json 내 장비 정보

    Return:
        ret(list): 검색된 장비들의 정보(dict)를 list 에 담아 반환
    """
    ret = []
    for fairy in GFLCore.fairy:
        if fairy.items() >= kwargs.items():
            ret.append(fairy)
        else:
            continue
    return ret


# original source by KOZ39
# https://github.com/KOZ39/gfOperationReportCalculatorQ
def calc_exp(cur_lv, target_lv, cur_exp, is_oath=False, is_fairy=False):
    """작전보고서 계산기

    Args:
        cur_lv(int): 현재 인형의 레벨
        target_lv(int): 목표 인형 레벨
        cur_exp(int): 현재 인형의 경험치(누적 아님)
        is_oath(bool): 서약 여부(참/거짓)
        is_fairy(bool): 요정 필요양 계산여부

    Return:
        report(int): 필요한 작전보고서의 갯수
    """
    rp = 0
    oath = 2 if is_oath else 1
    fairy = 3 if is_fairy else 1
    exp_table = GFLCore.exp_fairy if is_fairy else GFLCore.exp_doll

    # 레벨 검증 (시작레벨보다 목표레벨이 높은지 등)
    if cur_lv > target_lv:
        return

    # 구간별 분류
    if target_lv > 115:
        rp += math.ceil((exp_table[target_lv] - exp_table[max(cur_lv, 115)] - cur_exp) / (3000 * oath))
        target_lv = 115
        cur_exp = 0

    if target_lv > 110 and cur_lv < 115:
        rp += math.ceil((exp_table[target_lv] - exp_table[max(cur_lv, 110)] - cur_exp) / (3000 * oath))
        target_lv = 110
        cur_exp = 0

    if target_lv > 100 and cur_lv < 110:
        rp += math.ceil((exp_table[target_lv] - exp_table[max(cur_lv, 100)] - cur_exp) / (3000 * oath))
        target_lv = 100
        cur_exp = 0

    if target_lv <= 100 and cur_lv < 100:
        rp += math.ceil((exp_table[target_lv] - exp_table[cur_lv] - cur_exp) / 3000)
    return rp


if __name__ == '__main__':
    # print([n.get("krName", n['name']) for n in doll_find_all(rank=5, type='hg')])
    # print([n.get('name') for n in equip_find_all(type="scope", rank=5)])
    pass
