from ..models.patient import PatientModel

class PatientService:
    def get_patient_by_id(self, patID):
        pat_dict = PatientModel.find_by_id(patID)
        return PatientModel(**pat_dict) if pat_dict else None
    def add_patient(self, patID, firstName, lastName, docID, age, phone, gender):
        patient = PatientModel(patID=patID, firstName=firstName, lastName=lastName, docID=docID, age=age, phone=phone, gender=gender)
        patient.add_patient()
    def update_patient(self, patID, firstName, lastName, docID, age, phone, gender):
        patient = PatientModel(patID=patID, firstName=firstName, lastName=lastName, docID=docID, age=age, phone=phone, gender=gender)
        patient.update_patient()