import datetime


ins_sql = (
    "INSERT INTO ranking"
    "(date, user_key, score, per, ranking, comment)"
    "VALUES (%s, %s, %s, %s, %s, %s);"
)

get_sql = (
    "SELECT date, score, per, ranking FROM ranking "
    "WHERE user_key=%s "
    "ORDER BY date DESC;"
)

upd_sql = (
    "UPDATE ranking "
    "SET score=%s, per=%s, ranking=%s, comment=%s "
    "WHERE date=%s AND user_key=%s;"
)


def date_today(date):
    cur_date = datetime.datetime.now() - datetime.timedelta(hours=6)
    if date == cur_date.date():
        return True
    else:
        return False


class EventRankPoll():
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def log(self, key, score, per=0, ranking=0, comment=None):
        date = datetime.datetime.now() - datetime.timedelta(hours=6)
        if isinstance(comment, str):
            comment = comment.strip()

        if self.get_today(key):
            self.cur.execute(upd_sql, (score, per, ranking, comment, date.date(), key))
        else:
            self.cur.execute(ins_sql, (date.date(), key, score, per, ranking, comment))

    def get(self, user_key):
        self.cur.execute(get_sql, user_key)
        # 마지막 입력 데이터 불러오기
        row = self.cur.fetchone()
        # date, score, per. ranking
        return row

    def get_today(self, user_key):
        row = self.get(user_key)
        if row:
            if date_today(row[0]):
                return row
        return None

    def __del__(self):
        self.conn.commit()


if __name__ == "__main__":
    config = {
        "host": "192.168.99.100",
        "user": "root",
        "password": "password",
        "db": "36base",
        "charset": "utf8"
    }
    import pymysql
    conn = pymysql.connect(**config)
    rank = EventRankPoll(conn)
    rank.log("testusertest", 12456, 12)
    pass
