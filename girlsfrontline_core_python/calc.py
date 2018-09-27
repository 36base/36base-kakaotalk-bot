import json
import math


_exp_doll, _exp_hoc = json.load(open("./data/exp.json", "r")).values()
_exp_fairy = [n * 3 for n in _exp_doll]
_exp_hoc_hr = [1, 3, 3, 5, 7, 7, 9, 11, 11, 13, 15]


# original source by KOZ39
# https://github.com/KOZ39/gfOperationReportCalculatorQ
def exp(cur_lv, target_lv, cur_exp, is_oath=False, is_fairy=False):
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
    exp_table = _exp_fairy if is_fairy else _exp_doll

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


def exp_hoc(cur_lv, target_lv, cur_exp, fac_lv=10):
    """

    Args:
        cur_lv(int): 중장비 부대의 현재 레벨
        target_lv(int): 중장비 부대의 목표 레벨
        cur_exp(int): 중장비 부대의 현재 경험치
        fac_lv(int) 훈련장의 레벨. 0~10렙. 기본은 10(최대)

    Returns:
        rp(int): 필요한 특수작전보고서 갯수
        hr(int): 훈련에 필요한 시간
    """
    rp = math.ceil((_exp_hoc[target_lv] - _exp_hoc[cur_lv] - cur_exp) / 3000)
    hr = math.ceil(rp / _exp_hoc_hr[fac_lv])
    return rp, hr
