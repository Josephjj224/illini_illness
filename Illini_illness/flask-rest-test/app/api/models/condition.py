from datetime import datetime
from typing import List, Dict, Any
from ..common.database_utils import DatabaseUtils

class ConditionModel:
    TABLE_NAME = 'Conditions'

    def __init__(self, condDesc, rate, checkDate, patID, condID=None):
        self.condID = condID
        self.condDesc = condDesc
        self.rate = rate
        self.checkDate = checkDate
        self.patID = patID

    def to_dict(self):
        return {
            "condID": self.condID,
            "condDesc": self.condDesc,
            "rate": self.rate,
            "checkDate": self.checkDate.isoformat(),
            "patID": self.patID
        }

    def add_condition(self):
        query = f"INSERT INTO {self.TABLE_NAME} (condDesc, rate, checkDate, patID) VALUES (%s, %s, %s, %s)"
        DatabaseUtils.execute_query(query, (self.condDesc, self.rate, self.checkDate, self.patID))

    @classmethod
    def delete_condition(cls, condID):
        query = f"DELETE FROM {cls.TABLE_NAME} WHERE condID = %s"
        DatabaseUtils.execute_query(query, (condID,))

    def update_condition(self):
        query = f"""
        UPDATE {self.TABLE_NAME}
        SET condDesc = %s, rate = %s, checkDate = %s, patID = %s
        WHERE condID = %s
        """
        DatabaseUtils.execute_query(query, (self.condDesc, self.rate, self.checkDate, self.patID, self.condID))

    @classmethod
    def find_by_id(cls, condID):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE condID = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query, (condID,), single=True)

    @classmethod
    def find_by_description_paginated(cls, condDesc, page, page_size):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE condDesc LIKE %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, params=(condDesc,), page=page, page_size=page_size)

    @classmethod
    def find_by_check_date_paginated(cls, checkDate, page, page_size):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE checkDate = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, params=(checkDate,), page=page, page_size=page_size)

    @classmethod
    def find_condition_paginated(cls, page, page_size):
        query = f"SELECT * FROM {cls.TABLE_NAME} ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, page=page, page_size=page_size)

    @classmethod
    def find_all_condition(cls) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {cls.TABLE_NAME} ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query)

    @classmethod
    def find_by_description_and_pat_id_paginated(cls, condDesc, page, page_size, patID):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE condDesc LIKE %s AND patID = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, params=(condDesc, patID), page=page, page_size=page_size)

    @classmethod
    def find_by_check_date_and_pat_id_paginated(cls, checkDate, page, page_size, patID):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE checkDate = %s AND patID = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, params=(checkDate, patID), page=page, page_size=page_size)

    @classmethod
    def find_condition_paginated_by_pat_id(cls, page, page_size, patID):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE patID = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, params=(patID,), page=page, page_size=page_size)

    @classmethod
    def find_all_condition_by_pat_id(cls, patID) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE patID = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, params=(patID,))