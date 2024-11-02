from ..models.symptom import SymptomModel
from typing import List


class SymptomService:
    def add_symptom(self, sympDesc, rate, checkDate, patID):
        symptom = SymptomModel(sympDesc, rate, checkDate, patID)
        symptom.add_symptom()

    def delete_symptom(self, sympID):
        SymptomModel.delete_symptom(sympID)

    def update_symptom(self, sympID, sympDesc, rate, checkDate, patID):
        symptom = SymptomModel(sympDesc, rate, checkDate, patID, sympID)
        symptom.update_symptom()

    def get_symptom_by_id(self, sympID):
        symp_dict = SymptomModel.find_by_id(sympID)
        return SymptomModel(**symp_dict) if symp_dict else None

    def get_symptoms_by_description_paginated(self, sympDesc, page, page_size):
        symptom_list_dict = SymptomModel.find_by_description_paginated(sympDesc, page, page_size)
        if symptom_list_dict:
            symptom_list = [SymptomModel(**s) for s in symptom_list_dict]
        return symptom_list if symptom_list_dict else None

    def get_symptoms_by_check_date_paginated(self, checkDate, page, page_size):
        symptom_list_dict = SymptomModel.find_by_check_date_paginated(checkDate, page, page_size)
        if symptom_list_dict:
            symptom_list = [SymptomModel(**s) for s in symptom_list_dict]
        return symptom_list if symptom_list_dict else None

    def get_all_symptoms(self, page=1, page_size=10, fetch_all=False) -> List[SymptomModel]:
        if fetch_all:
            symptom_list_dict = SymptomModel.find_all_symptom()
        else:
            symptom_list_dict = SymptomModel.find_symptom_paginated(page, page_size)
        return [SymptomModel(**s) for s in symptom_list_dict]

    def get_symptoms_by_description_and_pat_id_paginated(self, sympDesc, page, page_size, patID):
        symptom_list_dict = SymptomModel.find_by_description_and_pat_id_paginated(sympDesc, page, page_size, patID)
        if symptom_list_dict:
            symptom_list = [SymptomModel(**s) for s in symptom_list_dict]
        return symptom_list if symptom_list_dict else None

    def get_symptoms_by_check_date_and_pat_id_paginated(self, checkDate, page, page_size, patID):
        symptom_list_dict = SymptomModel.find_by_check_date_and_pat_id_paginated(checkDate, page, page_size, patID)
        if symptom_list_dict:
            symptom_list = [SymptomModel(**s) for s in symptom_list_dict]
        return symptom_list if symptom_list_dict else None

    def get_all_symptoms_by_pat_id(self, patID, page=1, page_size=10, fetch_all=False):
        if fetch_all:
            symptom_list_dict = SymptomModel.find_all_symptom_by_pat_id(patID)
        else:
            symptom_list_dict = SymptomModel.find_symptom_paginated_by_pat_id(page, page_size, patID)
        return [SymptomModel(**s) for s in symptom_list_dict]