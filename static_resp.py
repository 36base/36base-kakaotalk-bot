from chatterbox import Text, MessageButton, Keyboard, Message


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
msg_useful_info = "소녀전선 이용자들을 위한 유용한 정보들입니다. 버튼을 눌러주세요."
msg_go_to_36db = "36베이스 바로가기"
msg_rank_poll = (
    "한국서버 <난류연속> 히든전역 <돌풍구출> 랭킹 정보 입력을 시작합니다.\n"
    "입력 양식:\n"
    "(점수) (퍼센트 또는 등수) [코멘트]\n\n"
    "예시:\n"
    "88888점 40\n"
    "123456 78퍼\n"
    "777777 10등 4제대\n\n"
    "퍼센트 또는 등수는 별도 식별문자(~등, ~퍼센트)를 입력하지 않으면 퍼센트로 인식합니다.\n"
    "자세한 사용법은 아래의 글을 참조해주세요."
)
msg_rank_poll_err = (
    "잘못된 입력값입니다. 퍼센트 또는 등수는 1~100사이 숫자로 입력해주세요."
)
msg_start_free_input = (
    "자유롭게 입력해주세요. 현재 별명으로 인형/장비/요정 검색이 구현되어 있습니다.\n"
    "자세한 내용은 아래의 글을 참조해주세요. 메인으로 돌아가려면 '돌아가기'를 입력해주세요."
)
msg_fallback = "오류가 발생하였습니다. 홈으로 돌아갑니다."
f_msg_free_input_info = {
    "doll": "< 인형 정보 >\n{name}: {rank}성 {Type}\n제조시간: {build_time}",
    "equip": "< 장비 정보 >\n{name}: {rank}성 {category_name}\n제조시간: {build_time}\n\n{info}",
    "fairy": "< 요정 정보 >\n{name}\n제조시간: {build_time}\n\n{desc}\n{info}"
}

bt_info = MessageButton(
    label="사용설명 바로가기",
    url="http://pf.kakao.com/_MaxmXC/27228298"
)
bt_36db = MessageButton(
    label="여기를 눌러주세요",
    url="https://girlsfrontline.kr/"
)
bt_ranking_result = MessageButton(
    label="랭킹 그래프 보기",
    url="https://github.com/krepe-suZette/gfl-event-ranking/blob/master/docs/Home.md"
)
bt_start_free_input = MessageButton(
    label="여기를 눌러주세요",
    url="http://pf.kakao.com/_MaxmXC/29180221"
)

kb_home = Keyboard(['인형 검색', '장비 검색', '작전보고서 계산', '36베이스 바로가기', '유용한 정보 모음', '대화하기'])
kb_useful_info = Keyboard(["36베이스", "군수지원 계산기", "소녀전선 구글시트", "소전DB", "편성 시뮬레이터", "철혈시트", "DPS 시뮬레이터", "소전사전", "돌아가기"])

d_useful_info = {
    "36베이스": Message(
        text=Text("소녀전선 데이터베이스 36베이스입니다. 인형, 장비, 요정의 상세 정보, 제조시간표, 작전보고서 계산기, OST 플레이어 등이 있습니다."),
        message_button=MessageButton("바로가기", "https://girlsfrontline.kr/")
    ),
    "군수지원 계산기": Message(
        text=Text("자신에게 필요한 군수지원을 추천해주는 홈페이지입니다."),
        message_button=MessageButton("바로가기", "https://tempkaridc.github.io/gf/")
    ),
    "소녀전선 구글시트": Message(
        text=Text("소녀전선과 관련된 자료들을 많이 모아놓은 구글 시트입니다."),
        message_button=MessageButton("바로가기", "https://docs.google.com/spreadsheets/d/1IxJxfpBHboVRJe92_GPC6iUZCq1M2NJkbtKo6SP-3SM/pubhtml#")
    ),
    "소전DB": Message(
        text=Text("소녀전선의 인형, 장비, 요정, 스토리 다시보기 등이 있는 홈페이지입니다."),
        message_button=MessageButton("바로가기", "http://gfl.zzzzz.kr/")
    ),
    "편성 시뮬레이터": Message(
        text=Text("소녀전선 제대 편성을 해볼 수 있는 안드로이드 앱입니다."),
        message_button=MessageButton("바로가기", "https://play.google.com/store/apps/details?id=com.Cosmos.GfTileSim")
    ),
    "철혈시트": Message(
        text=Text("소녀전선 전역별 적 데이터를 상세히 볼 수 있는 홈페이지입니다."),
        message_button=MessageButton("바로가기", "https://gf.underseaworld.net/")
    ),
    "DPS 시뮬레이터": Message(
        text=Text("제대의 DPS를 확인할 수 있는 사이트입니다. 하지만 너무 신뢰는 하지 말아주세요.\n\n(36베이스에서 운영하는게 아니기 때문에 업데이트가 불가능한 점 양해 부탁드립니다.)"),
        message_button=MessageButton("바로가기", "https://gf.dck.moe/ynntk4815/gf/main2.html")
    ),
    "소전사전": Message(
        text=Text("소녀전선의 여러 데이터들을 모아둔 안드로이드 앱입니다."),
        message_button=MessageButton("바로가기", "https://play.google.com/store/apps/details?id=com.gfl.dic")
    ),
}

search_doll = Text(msg_search_doll) + bt_info + Keyboard(type="text")
search_equip = Text(msg_search_equip) + bt_info + Keyboard(type="text")
calc_report = Text(msg_calc_report) + bt_info + Keyboard(type="text")
useful_info = Text(msg_useful_info) + kb_useful_info
go_to_36db = Text(msg_go_to_36db) + bt_36db
start_free_input = Text(msg_start_free_input) + bt_start_free_input
fallback = Text(msg_fallback)
# rank_poll = Text(msg_rank_poll) + Keyboard(type="text")
