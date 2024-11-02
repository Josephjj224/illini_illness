from contextlib import contextmanager
import mysql.connector
from ...config import Config


class DatabaseUtils:
    @staticmethod
    @contextmanager
    def get_connection():
        connection = mysql.connector.connect(**Config.MYSQL_CONFIG)
        try:
            yield connection
        finally:
            connection.close()

    @staticmethod
    def execute_query(query, params=None, single=False, page=None, page_size=None):
        with DatabaseUtils.get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            if page is not None and page_size is not None:
                offset = (page - 1) * page_size
                query += " LIMIT %s OFFSET %s"
                params = params + (page_size, offset) if params else (page_size, offset)
            cursor.execute(query, params or ())
            # if it's a select query
            if query.strip().upper().startswith("SELECT"):
                if single:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()
            else:
                # for other queries
                connection.commit()
