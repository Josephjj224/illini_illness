from typing import List, Dict, Any
from ..common.database_utils import DatabaseUtils
from datetime import date


class PatientModel:
    TABLE_NAME = 'Patients'

    def __init__(self, firstName: str, lastName: str, docID: str, age: int, phone: str, gender: str, patID: str):
        self.firstName = firstName
        self.lastName = lastName
        self.docID = docID
        self.age = age
        self.phone = phone
        self.gender = gender
        self.patID = patID

    def to_dict(self) -> Dict[str, Any]:
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "docID": self.docID,
            "age": self.age,
            "phone": self.phone,
            "gender": self.gender,
            "patID": self.patID
        }

    @classmethod
    def find_by_id(cls, patID: int) -> Dict[str, Any]:
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE patID = %s"
        return DatabaseUtils.execute_query(query, (patID,), single=True)

    def add_patient(self):
        query = f"INSERT INTO {self.TABLE_NAME} (firstName, lastName, docID, age, phone, gender, patID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        DatabaseUtils.execute_query(query, (
        self.firstName, self.lastName, self.docID, self.age, self.phone, self.gender, self.patID))

    # @classmethod
    # def delete_patient(cls, patID: int):
    #     query = f"DELETE FROM {cls.TABLE_NAME} WHERE patID = %s"
    #     DatabaseUtils.execute_query(query, (patID,))

    def update_patient(self):
        query = f"""
        UPDATE {cls.TABLE_NAME}
        SET firstName = %s, lastName = %s, docID = %s, age = %s, phone = %s, gender = %s
        WHERE patID = %s
        """
        DatabaseUtils.execute_query(query, (self.firstName, self.lastName, self.docID, self.age, self.phone, self.gender, self.patID))

