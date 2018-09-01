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
    '작전보고서 계산기 입력을 시작합니다.\n'
    '입력 양식:\n'
    '(현재 레벨) (목표 레벨) [현재 경험치] [서약] [요정] [화력[대규모 훈련장 레벨]]\n\n'
    '자세한 사용법은 아래 링크를 참조해주세요.'
)
msg_calc_support = "군수지원 계산기 바로가기"
msg_go_to_36db = "36베이스 바로가기"
msg_rank_poll = (
    "한국서버 <난류연속> 히든전역 <돌풍구출> 랭킹 정보 입력을 시작합니다.\n"
    "입력 양식:\n"
    "(점수) (퍼센트) [등수] [코멘트]\n\n"
    "예시:\n"
    "123456 78퍼\n"
    "777777 0% 10등 4제대\n\n"
    "100위 이내일 경우 퍼센트는 0을 입력해주세요.\n"
    "자세한 사용법은 아래 링크를 참조해주세요."
)

bt_info = MessageButton(
    label="사용설명 바로가기",
    url="http://pf.kakao.com/_MaxmXC/27228298"
)
bt_calc_sp = MessageButton(
    label="여기를 눌러주세요",
    url="https://tempkaridc.github.io/gf/"
)
bt_36db = MessageButton(
    label="여기를 눌러주세요",
    url="https://girlsfrontline.kr/"
)

search_doll = Text(msg_search_doll) + bt_info + Keyboard(type="text")
search_equip = Text(msg_search_equip) + bt_info + Keyboard(type="text")
calc_report = Text(msg_calc_report) + bt_info + Keyboard(type="text")
calc_support = Text(msg_calc_support) + bt_calc_sp
go_to_36db = Text(msg_go_to_36db) + bt_36db
# rank_poll = Text(msg_rank_poll) + Keyboard(type="text")
