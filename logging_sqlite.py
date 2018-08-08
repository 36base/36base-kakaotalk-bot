# Original source by giumas
# https://gist.github.com/giumas/994e48d3c1cff45fbe93
import sqlite3
import logging
import time


initial_sql = (
    "CREATE TABLE IF NOT EXISTS log("
    "timestamp TEXT,"
    "source TEXT,"
    "log_level INT,"
    "log_level_name TEXT,"
    "user_status TXT,"
    "user_key TEXT,"
    "content TEXT,"
    "message TEXT,"
    "module TEXT,"
    "func_name TEXT,"
    "process INT,"
    "thread TEXT,"
    "thread_name TEXT)"
)

insertion_sql = (
    "INSERT INTO log("
    "timestamp,"
    "source,"
    "log_level,"
    "log_level_name,"
    "user_status,"
    "user_key,"
    "content,"
    "message,"
    "module,"
    "func_name,"
    "process,"
    "thread,"
    "thread_name)"
    "VALUES ("
    "'%(dbtime)s',"
    "'%(name)s',"
    "%(levelno)d,"
    "'%(levelname)s',"
    "'%(user_status)s',"
    "'%(user_key)s',"
    "'%(content)s',"
    "'%(msg)s',"
    "'%(module)s',"
    "'%(funcName)s',"
    "%(process)d,"
    "'%(thread)s',"
    "'%(threadName)s'"
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
        sql = insertion_sql % record.__dict__
        conn = sqlite3.connect(self.db)
        conn.execute(sql)
        conn.commit()  # not efficient, but hopefully thread-safe


if __name__ == '__main__':
    # main()
    pass
