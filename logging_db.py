# Original source by giumas
# https://gist.github.com/giumas/994e48d3c1cff45fbe93
import logging
import time


insertion_sql = (
    "INSERT INTO log (timestamp, log_level, user_status, user_key, type, content, response, func_name)"
    "VALUES (%(dbtime)s, %(levelno)s, %(user_status)s, %(user_key)s, %(type)s, %(content)s, %(msg)s, %(funcName)s)"
)


class MySQLHandler(logging.Handler):
    """
    Thread-safe logging handler for SQLite.
    """

    def __init__(self, conn):
        logging.Handler.__init__(self)
        self.conn = conn
        self.cur = self.conn.cursor()

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
        self.cur.execute(insertion_sql, record.__dict__)
        self.conn.commit()


if __name__ == '__main__':
    # main()
    pass
