from ..models.condition import ConditionModel
from typing import List

class ConditionService:
    def add_condition(self, condDesc, rate, checkDate, patID):
        condition = ConditionModel(condDesc, rate, checkDate, patID)
        condition.add_condition()

    def delete_condition(self, condID):
        ConditionModel.delete_condition(condID)

    def update_condition(self, condID, condDesc, rate, checkDate, patID):
        condition = ConditionModel(condDesc, rate, checkDate, patID, condID)
        condition.update_condition()

    def get_condition_by_id(self, condID):
        cond_dict = ConditionModel.find_by_id(condID)
        return ConditionModel(**cond_dict) if cond_dict else None

    def get_conditions_by_description_paginated(self, condDesc, page, page_size):
        condition_list_dict = ConditionModel.find_by_description_paginated(condDesc, page, page_size)
        if condition_list_dict:
            condition_list = [ConditionModel(**c) for c in condition_list_dict]
        return condition_list if condition_list_dict else None

    def get_conditions_by_check_date_paginated(self, checkDate, page, page_size):
        condition_list_dict = ConditionModel.find_by_check_date_paginated(checkDate, page, page_size)
        if condition_list_dict:
            condition_list = [ConditionModel(**c) for c in condition_list_dict]
        return condition_list if condition_list_dict else None

    def get_all_conditions(self, page=1, page_size=10, fetch_all=False) -> List[ConditionModel]:
        if fetch_all:
            condition_list_dict = ConditionModel.find_all_condition()
        else:
            condition_list_dict = ConditionModel.find_condition_paginated(page, page_size)
        return [ConditionModel(**c) for c in condition_list_dict]

    def get_conditions_by_description_and_pat_id_paginated(self, condDesc, page, page_size, patID):
        condition_list_dict = ConditionModel.find_by_description_and_pat_id_paginated(condDesc, page, page_size, patID)
        if condition_list_dict:
            condition_list = [ConditionModel(**c) for c in condition_list_dict]
        return condition_list if condition_list_dict else None

    def get_conditions_by_check_date_and_pat_id_paginated(self, checkDate, page, page_size, patID):
        condition_list_dict = ConditionModel.find_by_check_date_and_pat_id_paginated(checkDate, page, page_size, patID)
        if condition_list_dict:
            condition_list = [ConditionModel(**c) for c in condition_list_dict]
        return condition_list if condition_list_dict else None

    def get_all_conditions_by_pat_id(self, patID, page=1, page_size=10, fetch_all=False) -> List[ConditionModel]:
        if fetch_all:
            condition_list_dict = ConditionModel.find_all_condition_by_pat_id(patID)
        else:
            condition_list_dict = ConditionModel.find_condition_paginated_by_pat_id(page, page_size, patID)
        return [ConditionModel(**c) for c in condition_list_dict]

