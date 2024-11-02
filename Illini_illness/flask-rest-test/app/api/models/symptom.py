from datetime import datetime
from typing import List, Dict, Any
from ..common.database_utils import DatabaseUtils


class SymptomModel:
    TABLE_NAME = 'Symptoms'

    def __init__(self, sympDesc, rate, checkDate, patID, sympID=None):
        self.sympID = sympID
        self.sympDesc = sympDesc
        self.rate = rate
        self.checkDate = checkDate
        self.patID = patID

    def to_dict(self):
        return {
            "sympID": self.sympID,
            "sympDesc": self.sympDesc,
            "rate": self.rate,
            "checkDate": self.checkDate.isoformat(),
            "patID": self.patID
        }
    def add_symptom(self):
        query = f"INSERT INTO {self.TABLE_NAME} (sympDesc, rate, checkDate, patID) VALUES (%s, %s, %s, %s)"
        DatabaseUtils.execute_query(query, (self.sympDesc, self.rate, self.checkDate, self.patID))

    @classmethod
    def delete_symptom(cls, sympID):
        query = f"DELETE FROM {cls.TABLE_NAME} WHERE sympID = %s"
        DatabaseUtils.execute_query(query, (sympID,))

    def update_symptom(self):
        query = f"""
        UPDATE {self.TABLE_NAME}
        SET sympDesc = %s, rate = %s, checkDate = %s, patID = %s
        WHERE sympID = %s
        """
        DatabaseUtils.execute_query(query, (self.sympDesc, self.rate, self.checkDate, self.patID, self.sympID))

    @classmethod
    def find_by_id(cls, sympID):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE sympID = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query, (sympID,), single=True)

    @classmethod
    def find_by_description_paginated(cls, sympDesc, page, page_size):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE sympDesc LIKE %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, params=(sympDesc,), page=page, page_size=page_size)

    @classmethod
    def find_by_check_date_paginated(cls, checkDate, page, page_size):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE checkDate = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, params=(checkDate,), page=page, page_size=page_size)

    @classmethod
    def find_symptom_paginated(cls, page, page_size):
        query = f"SELECT * FROM {cls.TABLE_NAME} ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, page=page, page_size=page_size)

    @classmethod
    def find_all_symptom(cls) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {cls.TABLE_NAME} ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query)

    @classmethod
    def find_by_description_and_pat_id_paginated(cls, sympDesc, page, page_size, patID):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE sympDesc LIKE %s AND patID = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, params=(sympDesc, patID), page=page, page_size=page_size)

    @classmethod
    def find_by_check_date_and_pat_id_paginated(cls, checkDate, page, page_size, patID):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE checkDate = %s AND patID = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, params=(checkDate, patID), page=page, page_size=page_size)

    @classmethod
    def find_symptom_paginated_by_pat_id(cls, page, page_size, patID):
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE patID = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, params=(patID,), page=page, page_size=page_size)

    @classmethod
    def find_all_symptom_by_pat_id(cls, patID) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE patID = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query=query, params=(patID,))


