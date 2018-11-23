import os
import json
import glob
import random
import urllib


__all__ = ["Doll", "Equip", "Fairy", "Core"]
G36DB_ROOT = "https://girlsfrontline.kr/"
IMAGE_REPO = "https://raw.githubusercontent.com/krepe-suZette/dccon/master/"
COMPANY_OK = {"BM", "EOT", "AMP", "IOP", "PMC", "AC", "ILM"}
REFERRER = "utm_source=kakao.com&utm_medium=social&utm_campaign={0}search&utm_content=36basebot&utm_term={1}"


def _make_dict(data: list, key: str, mode='', remove_special=False) -> dict:

    ret = {}
    # data(list): 전체 인형 데이터 리스트
    # obj(dict): 인형/장비/요정 객체
    for obj in data:
        if remove_special:
            if mode == "doll" and (1 not in obj['obtain'] and 2 not in obj['obtain']):
                continue
            elif mode == "equip" and (obj['company'] not in COMPANY_OK or obj.get('fitGuns')):
                continue
            elif mode == "fairy" and (obj["id"] > 1000 or obj['qualityExp'][4] < 1000):
                continue

        if obj.get(key, "") in ret:
            ret[obj[key]].append(obj)
        else:
            ret[obj[key]] = [obj]
    return ret


class Doll:
    def __init__(self, data):
        self.data = data
        self.id = {n["id"]: n for n in self.data}
        self.codename = {n["codename"]: n for n in self.data}
        self.build_time = _make_dict(self.data, "buildTime", "doll", True)
        self.rank = _make_dict(self.data, "rank")
        self.type = _make_dict(self.data, "type")

    def get_from_id(self, doll_id: int):
        return self.id[doll_id]


class Equip():
    def __init__(self, data):
        self.data = data
        self.id = {n["id"]: n for n in self.data}
        self.codename = {n["codename"]: n for n in self.data}
        self.build_time = _make_dict(self.data, "buildTime", "equip", True)
        self.rank = _make_dict(self.data, "rank")
        self.type = _make_dict(self.data, "type")
        self.category = _make_dict(self.data, "category")

    def get_from_id(self, equip_id):
        return self.id[equip_id]


class Fairy():
    def __init__(self, data):
        self.data = data
        self.id = {n["id"]: n for n in self.data}
        self.codename = {n["codename"]: n for n in self.data}
        self.build_time = _make_dict(self.data, "buildTime", "fairy", True)
        self.category = _make_dict(self.data, "category")

    def get_from_id(self, fairy_id):
        return self.id[fairy_id]


class Internationalization():
    def __init__(self, core_dir):
        self.data = {}
        for lang in {"ko-KR"}:
            self.data[lang] = {}
            file_list = glob.glob(os.path.join(core_dir, f"i18n/{lang}/*.json"))
            for file_dir in file_list:
                self.data[lang].update(json.load(open(file_dir, "r", encoding="utf-8")))

    def gun(self, lang, gun_id, num, default='', mod=False):
        if gun_id > 20000 and mod:
            return "개조 " + self.data[lang].get(f"gun-{num}{gun_id:0>7}", default)
        else:
            return self.data[lang].get(f"gun-{num}{gun_id:0>7}", default)

    def equip(self, lang, equip_id, num, default=''):
        return self.data[lang].get(f"equip-{num}{equip_id:0>7}", default)

    def fairy(self, lang, fairy_id, num, default=''):
        return self.data[lang].get(f"fairy-{num}{fairy_id:0>7}", default)

    def all(self, lang, o_type, o_id, num=1, default='', mod=False):
        if o_type == 'doll':
            return self.gun(lang, o_id, num, default, mod)
        elif o_type == 'equip':
            return self.equip(lang, o_id, num, default)
        elif o_type == 'fairy':
            return self.fairy(lang, o_id, num, default)
        else:
            return "None"


class Core:
    def __init__(self, core_dir: str):
        """girlsfrontline-core 의 데이터들을 로딩

        Args:
            core_dir(str): girlsfrontline-core 레포 경로.
        """
        json_doll = json.load(open(os.path.join(core_dir, "data/doll.json"), "r", encoding="utf-8"))
        json_equip = json.load(open(os.path.join(core_dir, "data/equip.json"), "r", encoding="utf-8"))
        json_fairy = json.load(open(os.path.join(core_dir, "data/fairy.json"), "r", encoding="utf-8"))
        json_eq_nm = json.load(open("./data/equip_name.json", "r", encoding="utf-8"))

        self.doll = Doll(json_doll)
        self.equip = Equip(json_equip)
        self.fairy = Fairy(json_fairy)
        self.i18n = Internationalization(core_dir)

        self.eq_nm = json_eq_nm

        self._build_alias()
        self._special = json.load(open("./data/special.json", "r", encoding="utf-8"))

    def _build_alias(self):
        self._alias = {}
        json_alias = json.load(open("./data/alias.json", "r", encoding="utf-8"))
        # 인형 이름으로 별명 만들기
        for doll_id in self.doll.id.keys():
            if f"gun-1{doll_id:0>7}" in self.i18n.data['ko-KR']:
                if doll_id < 20000:
                    # 개조가 아닌 인형들
                    self._alias[self.i18n.data["ko-KR"][f"gun-1{doll_id:0>7}"].lower()] = [('doll', doll_id)]
                else:
                    # 개조 인형들. Mod 를 뒤에 붙여 구분 가능하게 변경.
                    self._alias[f"{self.i18n.data['ko-KR'][f'gun-1{doll_id:0>7}']}Mod".lower()] = [('doll', doll_id)]
                    self._alias[f"개조 {self.i18n.data['ko-KR'][f'gun-1{doll_id:0>7}']}".lower()] = [('doll', doll_id)]
            else:
                # 이름이 없는경우 codename 으로 대체
                self._alias[self.doll.id[doll_id]["codename"].lower()] = [('doll', doll_id)]
        # 장비 이름으로 별명 목록 추가
        for equip_id in self.equip.id.keys():
            if f"equip-1{equip_id:0>7}" in self.i18n.data['ko-KR']:
                self._alias[self.i18n.data["ko-KR"][f"equip-1{equip_id:0>7}"].lower()] = [('equip', equip_id)]
            else:
                # 이름이 없는경우 codename 으로 대체
                self._alias[self.equip.id[equip_id]["codename"].lower()] = [('equip', equip_id)]
        # 요정 이름으로 별명 목록 추가
        for fairy_id in self.fairy.id.keys():
            if f"fairy-1{fairy_id:0>7}" in self.i18n.data['ko-KR']:
                self._alias[self.i18n.data["ko-KR"][f"fairy-1{fairy_id:0>7}"].lower()] = [('fairy', fairy_id)]
            else:
                # 이름이 없는경우 codename 으로 대체
                self._alias[self.fairy.id[fairy_id]["codename"].lower()] = [('fairy', fairy_id)]
        # alias_type(str): 해당 별명의 종류. doll, equip, fairy
        # item_in_types(dict): 종류별 id: [*alias] 로 구성된 딕셔너리
        for alias_type, item_in_types in json_alias.items():
            # key: 인형/장비/요정 id
            # values: 별명 list
            for key, values in item_in_types.items():
                # alias: 리스트 안에 있던 별명 목록들
                # values: id 별로 대응되는 별명 들어있는 리스트
                for alias in values:
                    # 해당 별명 key 가 이미 목록에 존재하면 append, 아니면 설정
                    if alias.lower() in self._alias:
                        self._alias[alias.lower()].append((alias_type, int(key)))
                    else:
                        self._alias[alias.lower()] = [(alias_type, int(key))]
                    # 개조가 있는 인형일 경우
                    if alias_type == "doll" and (int(key) + 20000) in self.doll.id.keys():
                        if "개조 " + alias.lower() in self._alias:
                            self._alias["개조 " + alias.lower()].append((alias_type, int(key) + 20000))
                        else:
                            self._alias["개조 " + alias.lower()] = [(alias_type, int(key) + 20000)]
        return

    def get_names(self, items: list):
        return [self.i18n.all("ko-KR", item[0], item[1], 1, '', True) for item in items]

    def get_value(self, item: tuple) -> dict:
        info_type, info_id = item
        return getattr(self, info_type).get_from_id(info_id)

    def l10n(self, lang, data_type: str, data: dict):
        """언어랑, 데이터 종류랑, 데이터 받아서 쓰기 편한 몇몇개 데이터들 추가.
        """
        if data_type == 'doll':
            if 1 in data['obtain'] or 2 in data['obtain']:
                build_time = f"{data['buildTime'] // 3600:0>2}:{data['buildTime'] // 60 % 60:0>2}"
            else:
                build_time = "제조 불가능"
            if data['rank'] == 7:
                data['rank'] = 5
            photo = {
                "url": f"{IMAGE_REPO}_doll/{urllib.parse.quote(data['codename'])}.jpg",
                "width": 512,
                "height": 360
            }
            extra = dict(
                Type=data['type'].upper(),
                name=self.i18n.gun(lang, data['id'], 1, data['codename']),
                build_time=build_time,
                link=f"{G36DB_ROOT}doll/{data['id']}?{REFERRER.format(data_type, data['id'])}",
                photo=photo
            )
        elif data_type == 'equip':
            if data['company'] in COMPANY_OK and not data.get('fitGuns'):
                build_time = f"{data['buildTime'] // 3600:0>2}:{data['buildTime'] // 60 % 60:0>2}"
            else:
                build_time = "제조 불가능"
            extra = dict(
                name=self.i18n.equip(lang, data['id'], 1, data['codename']),
                build_time=build_time,
                category_name=f"{self.eq_nm[data['type']]}",
                info=f"{self.i18n.equip(lang, data['id'], 3)}",
                link=f"{G36DB_ROOT}equip/{data['id']}?{REFERRER.format(data_type, data['id'])}"
            )
        elif data_type == 'fairy':
            if data["id"] < 1000 and data['qualityExp'][4] > 1000:
                build_time = f"{data['buildTime'] // 3600:0>2}:{data['buildTime'] // 60 % 60:0>2}"
            else:
                build_time = "제조 불가능"
            extra = dict(
                name=self.i18n.fairy(lang, data['id'], 1, data['codename']),
                build_time=build_time,
                desc=f"{self.i18n.fairy(lang, data['id'], 2)}",
                info=f"{self.i18n.fairy(lang, data['id'], 3)}",
                link=f"{G36DB_ROOT}fairy/{data['id']}?{REFERRER.format(data_type, data['id'])}"
            )
        return dict(**data, **extra)

    def find_nickname(self, alias, nick_type="", lang="ko-KR"):
        if nick_type:
            alias_list = [n for n in self._alias.get(alias.lower(), []) if n[0] == nick_type]
        else:
            alias_list = self._alias.get(alias.lower(), [])

        if len(alias_list) is 0:
            return
        elif len(alias_list) is 1:
            data = self.get_value(alias_list[0])
            ret = self.l10n(lang, alias_list[0][0], data)
            return alias_list[0][0], ret
        else:
            data = self.get_names(alias_list)
            return data

    def special(self, msg):
        resp = self._special.get(msg)
        if resp:
            return random.choice(resp)
        else:
            return


def main():
    core = Core("D:/GitHub/girlsfrontline-core")

    # print(core.find_nickname("용사요정"))
    # print(core.find_nickname("흥국이"))
    # print(core.find_nickname("갓속탄"))
    print([core.l10n("ko-KR", "doll", n) for n in core.doll.build_time[14100]])
    return


if __name__ == "__main__":
    main()
    print("")
