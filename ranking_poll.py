import os
import time
import sqlite3


init_sql = (
    "CREATE TABLE IF NOT EXISTS rank("
    "time INT,"
    "user_key TEXT,"
    "score INT,"
    "percent INT)"
)

ins_sql = (
    "INSERT INTO rank"
    "(time, user_key, score, percent)"
    "VALUES ({0}, '{1}', {2}, {3})"
)


class EventRankPoll():
    def __init__(self, db_name, end_date):
        # ./db 폴더 없으면 생성
        os.makedirs("db", exist_ok=True)
        # SQLite 파일 생성 및 테이블도 생성
        self.db = "db/{0}.db".format(db_name)
        conn = sqlite3.connect(self.db)
        conn.execute(init_sql)
        conn.commit()

    def log(self, key, score, per):
        times = int(time.time())
        conn = sqlite3.connect(self.db)
        conn.execute(ins_sql.format(times, key, score, per))
        conn.commit()


if __name__ == "__main__":
    rank = EventRankPoll("rank")
    rank.log("testuser", 12456, 12)
    pass
