import datetime


ins_sql = (
    "INSERT INTO ranking"
    "(date, user_key, score, per, ranking, comment)"
    "VALUES (%s, %s, %s, %s, %s, %s)"
)


class EventRankPoll():
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def log(self, key, score, per=0, ranking=0, comment=None):
        date = datetime.datetime.now() - datetime.timedelta(hours=6)
        self.cur.execute(ins_sql, (date.strftime("%Y-%m-%d"), key, score, per, ranking, comment))

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
