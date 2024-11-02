from datetime import datetime
from ..common.database_utils import DatabaseUtils

class UserModel:
    TABLE_NAME = 'Users'

    def __init__(self, email, password, salt, created_at=None, updated_at=None, userID=None):
        self.email = email
        self.password = password
        self.salt = salt
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.userID = userID

    def add_user(self):
        query = f"INSERT INTO {self.TABLE_NAME} (email, password, salt, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
        DatabaseUtils.execute_query(query, (self.email, self.password, self.salt, self.created_at, self.updated_at))

    def to_dict(self):
        return {
            "userID": self.userID,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def find_by_email(cls, email) -> dict:
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE email = %s"
        return DatabaseUtils.execute_query(query, (email,), single=True)

    @classmethod
    def get_all_users(cls) -> list:
        query = f"SELECT * FROM {cls.TABLE_NAME}"
        return DatabaseUtils.execute_query(query)

    @classmethod
    def get_users_paginated(cls, page, page_size) -> list:
        query = f"SELECT * FROM {cls.TABLE_NAME}"
        return DatabaseUtils.execute_query(query, page=page, page_size=page_size)