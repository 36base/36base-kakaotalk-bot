import os
import json
import glob


__all__ = ["Doll", "Equip", "Fairy", "Core"]
G36DB_ROOT = "https://girlsfrontline.kr/"


def _make_dict(data: list, key: str, mode='', remove_special=False) -> dict:
    company_ok = {"BM", "EOT", "AMP", "IOP", "PMC", "AC", "ILM"}
    ret = {}
    # data(list): 전체 인형 데이터 리스트
    # obj(dict): 인형/장비/요정 객체
    for obj in data:
        if remove_special:
            if mode == "doll" and (1 not in obj['obtain'] and 2 not in obj['obtain']):
                continue
            elif mode == "equip" and (obj['company'] not in company_ok or obj.get('fitGuns')):
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

    def gun(self, lang, gun_id, num, default=''):
        return self.data[lang].get(f"gun-{num}{gun_id:0>7}", default)

    def equip(self, lang, equip_id, num, default=''):
        return self.data[lang].get(f"equip-{num}{equip_id:0>7}", default)

    def fairy(self, lang, fairy_id, num, default=''):
        return self.data[lang].get(f"fairy-{num}{fairy_id:0>7}", default)

    def all(self, lang, o_type, o_id, num=1, default=''):
        if o_type == 'doll':
            return self.gun(lang, o_id, num, default)
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

    def _build_alias(self):
        self._alias = {}
        json_alias = json.load(open("./data/alias.json", "r", encoding="utf-8"))
        # 인형 이름으로 별명 만들기
        for doll_id in self.doll.id.keys():
            if f"gun-1{doll_id:0>7}" in self.i18n.data['ko-KR']:
                self._alias[self.i18n.data["ko-KR"][f"gun-1{doll_id:0>7}"]] = [('doll', doll_id)]
            else:
                # 이름이 없는경우 codename 으로 대체
                self._alias[self.doll.id[doll_id]["codename"]] = [('doll', doll_id)]
        # 장비 이름으로 별명 목록 추가
        for equip_id in self.equip.id.keys():
            if f"equip-1{equip_id:0>7}" in self.i18n.data['ko-KR']:
                self._alias[self.i18n.data["ko-KR"][f"equip-1{equip_id:0>7}"]] = [('equip', equip_id)]
            else:
                # 이름이 없는경우 codename 으로 대체
                self._alias[self.equip.id[equip_id]["codename"]] = [('equip', equip_id)]
        # 장비 이름으로 별명 목록 추가
        for fairy_id in self.equip.id.keys():
            if f"fairy-1{fairy_id:0>7}" in self.i18n.data['ko-KR']:
                self._alias[self.i18n.data["ko-KR"][f"fairy-1{fairy_id:0>7}"]] = [('fairy', fairy_id)]
            else:
                # 이름이 없는경우 codename 으로 대체
                self._alias[self.equip.id[fairy_id]["codename"]] = [('fairy', fairy_id)]
        # alias_type(str): 해당 별명의 종류. doll, equip, fairy
        # item_in_types(dict): 종류별 id: [*alias] 로 구성된 딕셔너리
        for alias_type, item_in_types in json_alias.items():
            # key: 인형/장비/요정 id
            # values: 별명 list
            for key, values in item_in_types.items():
                # alias: 리스트 안에 있던 별명 목록들
                # values: id 별로 대응되는 별명 들어있는 리스트
                for alias in values:
                    if alias in self._alias:
                        self._alias[alias].append((alias_type, int(key)))
                    else:
                        self._alias[alias] = [(alias_type, int(key))]
        return

    def get_names(self, items: list):
        return [self.i18n.all("ko-KR", item[0], self.get_value(item)["id"]) for item in items]

    def get_value(self, item: tuple) -> dict:
        info_type, info_id = item
        return getattr(self, info_type).get_from_id(info_id)

    def l10n(self, lang, data_type: str, data: dict):
        """언어랑, 데이터 종류랑, 데이터 받아서 쓰기 편한 몇몇개 데이터들 추가.
        """
        if data_type == 'doll':
            extra = dict(
                Type=data['type'].upper(),
                name=self.i18n.gun(lang, data['id'], 1, data['codename']),
                build_time=f"{data['buildTime'] // 3600:0>2}:{data['buildTime'] // 60 % 60:0>2}",
                link=f"{G36DB_ROOT}doll/{data['id']}"
            )
        elif data_type == 'equip':
            extra = dict(
                name=self.i18n.equip(lang, data['id'], 1, data['codename']),
                build_time=f"{data['buildTime'] // 3600:0>2}:{data['buildTime'] // 60 % 60:0>2}",
                category_name=f"{self.eq_nm[data['type']]}",
                link=f"{G36DB_ROOT}equip#{data['id']}"
            )
        elif data_type == 'fairy':
            extra = dict(
                name=self.i18n.fairy(lang, data['id'], 1, data['codename']),
                build_time=f"{data['buildTime'] // 3600:0>2}:{data['buildTime'] // 60 % 60:0>2}",
                link=f"{G36DB_ROOT}fairy/{data['id']}"
            )
        return dict(**data, **extra)

    def find_nickname(self, alias, lang="ko-KR"):
        alias = self._alias.get(alias, [])
        if len(alias) is 0:
            return
        elif len(alias) is 1:
            data = self.get_value(alias[0])
            ret = self.l10n(lang, alias[0][0], data)
            return alias[0][0], ret
        else:
            data = self.get_names(alias)
            return data


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
