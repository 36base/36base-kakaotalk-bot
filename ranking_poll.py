import os
import datetime
import sqlite3


init_sql = (
    "CREATE TABLE IF NOT EXISTS rank{0.year}{0.month:02}{0.day:02}("
    "user_key TEXT,"
    "score INT,"
    "percent INT)"
)

ins_sql = (
    "INSERT INTO rank{0.year}{0.month:02}{0.day:02}"
    "(user_key, score, percent)"
    "VALUES ('{1}', {2}, {3})"
)


class EventRankPoll():
    def __init__(self, db_name):
        # ./db 폴더 없으면 생성
        os.makedirs("db", exist_ok=True)
        # SQLite 파일 생성 및 테이블도 생성
        self.db = "db/{0}.db".format(db_name)
        self.td = datetime.timedelta(hours=6)
        self.daily_table()

    def daily_table(self):
        res = datetime.datetime.now() - self.td
        conn = sqlite3.connect(self.db)
        conn.execute(init_sql.format(res))
        conn.commit()

    def log(self, key, score, per):
        self.daily_table()
        res = datetime.datetime.now() - self.td
        conn = sqlite3.connect(self.db)
        conn.execute(ins_sql.format(res, key, score, per))
        conn.commit()


if __name__ == "__main__":
    rank = EventRankPoll("rank")
    rank.log("testuser", 12456, 12)
    pass
