from chatterbox import Text, MessageButton, Keyboard

kb_home = ['인형 검색', '장비 검색', '작전보고서 계산', '군수지원 계산기', '36베이스 바로가기', '랭킹 집계']

msg_search_doll = (
    '인형 검색을 시작합니다.'
    '2자리에서 4자리의 숫자로 입력해주세요\n'
    '예시) 110 또는 0730'
)
msg_search_equip = (
    '장비/요정 검색을 시작합니다.'
    '2자리에서 4자리의 숫자로 입력해주세요\n'
    '예시) 110 또는 0505'
)
msg_calc_report = (
    '작전보고서 계산기입니다\n'
    '(현재 레벨) (목표 레벨) [현재 경험치] [서약] [요정] '
    '순서로 입력하면 됩니다. 띄어쓰기 또는 쉼표로 구분합니다.'
    '서약 여부는 "서약" 또는 "ㅅㅇ" 이라고 쓰면 됩니다.'
)
msg_calc_support = "군수지원 계산기 바로가기"
msg_go_to_36db = "36베이스 바로가기"
msg_rank_poll = (
    "(시험중입니다)\n이벤트 전역 랭킹 입력 기능을 시작합니다.\n"
    "(점수) (퍼센트) "
    "순서로 입력해주세요. 100위 이내는 0퍼센트로 작성해주세요.\n"
    "ex) 123456 78퍼"
)

bt_calc_sp = MessageButton(
    label="여기를 눌러주세요",
    url="https://tempkaridc.github.io/gf/"
)
bt_36db = MessageButton(
    label="여기를 눌러주세요",
    url="https://girlsfrontline.kr/"
)

search_doll = Text(msg_search_doll) + Keyboard(type="text")
search_equip = Text(msg_search_equip) + Keyboard(type="text")
calc_report = Text(msg_calc_report) + Keyboard(type="text")
calc_support = Text(msg_calc_support) + bt_calc_sp + Keyboard(type="text")
go_to_36db = Text(msg_go_to_36db) + bt_36db + Keyboard(type="text")
rank_poll = Text(msg_rank_poll) + Keyboard(type="text")