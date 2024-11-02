from ..models.treatment import TreatmentModel
from typing import List


class TreatmentService:
    def get_treatment_by_id(self, treatID):
        treat_dict = TreatmentModel.find_by_id(treatID)
        return TreatmentModel(**treat_dict) if treat_dict else None

    def get_treatments_by_description_and_pat_id_paginated(self, treatDesc, page, page_size, patID):
        treat_list_dict = TreatmentModel.find_by_description_and_pat_id_paginated(treatDesc, page, page_size, patID)
        if treat_list_dict:
            treat_list = [TreatmentModel(**t) for t in treat_list_dict]
        return treat_list if treat_list_dict else None

    def get_treatments_by_check_date_and_pat_id_paginated(self, checkDate, page, page_size, patID):
        treat_list_dict = TreatmentModel.find_by_check_date_and_pat_id_paginated(checkDate, page, page_size, patID)
        if treat_list_dict:
            treat_list = [TreatmentModel(**t) for t in treat_list_dict]
        return treat_list if treat_list_dict else None

    def get_all_treatments_by_pat_id(self, patID, page=1, page_size=10, fetch_all=False):
        if fetch_all:
            treat_list_dict = TreatmentModel.find_all_treatment_by_pat_id(patID)
        else:
            treat_list_dict = TreatmentModel.find_treatment_paginated_by_pat_id(page, page_size, patID)
        return [TreatmentModel(**t) for t in treat_list_dict]