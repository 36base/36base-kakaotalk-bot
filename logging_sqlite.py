# Original source by giumas
# https://gist.github.com/giumas/994e48d3c1cff45fbe93
import sqlite3
import logging
import time


initial_sql = (
    "CREATE TABLE IF NOT EXISTS log2("
    "timestamp INT,"
    "source TEXT,"
    "log_level INT,"
    "user_status TXT,"
    "user_key TEXT,"
    "content TEXT,"
    "message TEXT,"
    "module TEXT,"
    "func_name TEXT)"
)

insertion_sql = (
    "INSERT INTO log2("
    "timestamp,"
    "source,"
    "log_level,"
    "user_status,"
    "user_key,"
    "content,"
    "message,"
    "module,"
    "func_name)"
    "VALUES ("
    " :dbtime,"
    " :name,"
    " :levelno,"
    " :user_status,"
    " :user_key,"
    " :content,"
    " :msg,"
    " :module,"
    " :funcName"
    ")"
)


class SQLiteHandler(logging.Handler):
    """
    Thread-safe logging handler for SQLite.
    """

    def __init__(self, db='app.db'):
        logging.Handler.__init__(self)
        self.db = db
        conn = sqlite3.connect(self.db)
        conn.execute(initial_sql)
        conn.commit()

    def format_time(self, record):
        """
        Create a time stamp
        """
        record.dbtime = int(time.time())

    def emit(self, record):
        self.format(record)
        self.format_time(record)
        if record.exc_info:  # for exceptions
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
        else:
            record.exc_text = ""

        # Insert the log record
        conn = sqlite3.connect(self.db)
        conn.execute(insertion_sql, record.__dict__)
        conn.commit()  # not efficient, but hopefully thread-safe


# def main():
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)
#
#     # sqlite handler
#     sh = SQLiteHandler(db="test.db")
#     sh.setLevel(logging.INFO)
#     logging.getLogger().addHandler(sh)
#
#     # user_status, user_key, content
#     extra_data = dict(user_status="홈", user_key="asdfuserkey", content="후냐앙")
#     # test
#     logging.info('Start', extra=extra_data)
#     logging.info('End', extra=extra_data)


if __name__ == '__main__':
    # main()
    pass
