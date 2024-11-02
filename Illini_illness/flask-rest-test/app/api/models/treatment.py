from datetime import datetime
from typing import List, Dict, Any
from ..common.database_utils import DatabaseUtils


class TreatmentModel:
    TABLE_NAME = 'Treatments'
    MEDICINE_REF_TABLE = 'Medicine_Ref'
    MEDICINE_TABLE = 'Medicines'

    def __init__(self, treatDesc, patID, checkDate, medName, treatID=None):
        self.treatID = treatID
        self.treatDesc = treatDesc
        self.checkDate = checkDate
        self.medName = medName
        self.patID = patID

    def to_dict(self):
        return {
            "treatID": self.treatID,
            "treatDesc": self.treatDesc,
            "checkDate": self.checkDate.isoformat(),
            "medName": self.medName,
            "patID": self.patID
        }
    @classmethod
    def find_by_id(cls, treatID):
        query = f"SELECT treatID, treatDesc, checkDate, medName, patID FROM {cls.TABLE_NAME} NATURAL JOIN {cls.MEDICINE_REF_TABLE} NATURAL JOIN {cls.MEDICINE_TABLE} WHERE treatID = %s ORDER BY checkDate DESC"
        return DatabaseUtils.execute_query(query, (treatID,), single=True)

    @classmethod
    def find_treatment_paginated_by_pat_id(cls, page, page_size, patID):
        query = f"""
        SELECT treatID, treatDesc, checkDate, medName, patID
        FROM {cls.TABLE_NAME} NATURAL JOIN {cls.MEDICINE_REF_TABLE} NATURAL JOIN {cls.MEDICINE_TABLE}
        WHERE patID = %s
        ORDER BY checkDate DESC
        """
        return DatabaseUtils.execute_query(query=query, params=(patID,), page=page, page_size=page_size)

    @classmethod
    def find_all_treatment_by_pat_id(cls, patID) -> List[Dict[str, Any]]:
        query = f"""
        SELECT treatID, treatDesc, checkDate, medName, patID
        FROM {cls.TABLE_NAME} NATURAL JOIN {cls.MEDICINE_REF_TABLE} NATURAL JOIN {cls.MEDICINE_TABLE}
        WHERE patID = %s
        ORDER BY checkDate DESC
        """
        return DatabaseUtils.execute_query(query=query, params=(patID,))

    @classmethod
    def find_by_check_date_and_pat_id_paginated(cls, checkDate, page, page_size, patID):
        query = f"""
        SELECT treatID, treatDesc, checkDate, medName, patID
        FROM {cls.TABLE_NAME} NATURAL JOIN {cls.MEDICINE_REF_TABLE} NATURAL JOIN {cls.MEDICINE_TABLE}
        WHERE patID = %s AND checkDate = %s
        ORDER BY checkDate DESC
        """
        return DatabaseUtils.execute_query(query=query, params=(patID, checkDate), page=page, page_size=page_size)

    @classmethod
    def find_by_description_and_pat_id_paginated(cls, treatDesc, page, page_size, patID):
        query = f"""
        SELECT treatID, treatDesc, checkDate, medName, patID
        FROM {cls.TABLE_NAME} NATURAL JOIN {cls.MEDICINE_REF_TABLE} NATURAL JOIN {cls.MEDICINE_TABLE}
        WHERE patID = %s AND treatDesc LIKE %s
        ORDER BY checkDate DESC
        """
        return DatabaseUtils.execute_query(query=query, params=(patID, treatDesc), page=page, page_size=page_size)