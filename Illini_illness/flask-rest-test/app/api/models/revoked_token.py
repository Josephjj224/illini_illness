import mysql.connector
from ...config import Config

class RevokedTokenModel():
    """
    Table for revoked tokens
    """

    def __init__(self, jti):
        self.jti = jti


    # Add a token to the blacklist
    def add(self):
        connection = mysql.connector.connect(**Config.MYSQL_CONFIG)
        cursor = connection.cursor(dictionary=True)
        query = "INSERT INTO revoked_tokens (jti) VALUES (%s)"
        values = (self.jti,)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        connection = mysql.connector.connect(**Config.MYSQL_CONFIG)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM revoked_tokens WHERE jti = %s"
        values = (jti,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        return bool(result)