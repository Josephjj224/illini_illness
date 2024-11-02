from flask_restful import Resource, reqparse
from ..services.condition_service import ConditionService
from ..common.utils import res
from flask import request
from ..schema.register_sha import create_parser
from flask_jwt_extended import jwt_required


class ConditionResource(Resource):
    def __init__(self):
        self.condition_service = ConditionService()


    def get(self):
        args = {}
        args['condID'] = request.args.get('condID', None, type=int)
        args['page'] = request.args.get('page', 1, type=int)
        args['page_size'] = request.args.get('page_size', 10, type=int)
        args['fetch_all'] = request.args.get('fetch_all', False, type=bool)
        args['patID'] = request.args.get('patID', None, type=str)
        if args['condID']:
            # if condID is provided, get specific condition
            args.pop('patID')
            return self.get_condition(args['condID'])
        elif args['patID']:
            args.pop('condID')
            return self.get_all_condition_by_patient(**args)
        else:
            # otherwise, get all conditions with page/pagesize...
            args.pop('patID')
            args.pop('condID')
            return self.get_all_conditions(**args)


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', required=True, choices=('add', 'update', 'delete', 'find', 'findPat'))
        args = parser.parse_args()

        action = args['action']
        if action == 'add':
            return self.add_condition()
        elif action == 'update':
            return self.update_condition()
        elif action == 'delete':
            return self.delete_condition()
        elif action == 'find':
            return self.find_condition()
        elif action == 'findPat':
            return self.find_condition_by_patient()
        else:
            return res(message="Invalid Action", code=400)

    def get_condition(self, condID):
        condition = self.condition_service.get_condition_by_id(condID)
        if condition:
            return res(data=condition.to_dict(), success=True, code=200)
        else:
            return res(success=True, code=200)

    def get_all_conditions(self, page, page_size=10, fetch_all=False):
        condition_list = self.condition_service.get_all_conditions(page, page_size, fetch_all)
        condition_json = [c.to_dict() for c in condition_list]
        return res(data=condition_json)

    def add_condition(self):
        arg_configs = [
            {'name': 'condDesc', 'type': str, 'required': True},
            {'name': 'rate', 'type': int, 'required': True},
            {'name': 'checkDate', 'type': str, 'required': True},
            {'name': 'patID', 'type': str, 'required': True},
        ]
        parser = create_parser(arg_configs)
        args = parser.parse_args()
        try:
            self.condition_service.add_condition(**args)
            return res(message='Condition added successfully.')
        except Exception as e:
            error_message = str(e)
            return res(success=False, code=500, message="Error: " + error_message)

    def update_condition(self):
        arg_configs = [
            {'name': 'condDesc', 'type': str, 'required': True},
            {'name': 'rate', 'type': int, 'required': True},
            {'name': 'checkDate', 'type': str, 'required': True},
            {'name': 'patID', 'type': str, 'required': True},
            {'name': 'condID', 'type': str, 'required': True}
        ]
        parser = create_parser(arg_configs)
        args = parser.parse_args()
        try:
            self.condition_service.update_condition(**args)
            return res(success=True, code=200, message="Condition updated successfully.")
        except Exception as e:
            error_message = str(e)
            return res(success=False, code=500, message="Error: " + error_message)

    def delete_condition(self):
        arg_configs = [
            {'name': 'condID', 'type': str, 'required': True}
        ]
        parser = create_parser(arg_configs)
        args = parser.parse_args()
        try:
            self.condition_service.delete_condition(args['condID'])
            return res(message="Condition deleted successfully.")
        except Exception as e:
            error_message = str(e)
            return res(success=False, code=500, message="Error: " + error_message)

    def find_condition(self):
        arg_configs = [
            {'name': 'condDesc', 'type': str, 'required': False, 'default': 'no_param'},
            {'name': 'checkDate', 'type': str, 'required': False, 'default': 'no_param'},
            {'name': 'page', 'type': int, 'required': False, 'default': 1},
            {'name': 'page_size', 'type': int, 'required': False, 'default': 10}
        ]
        parser = create_parser(arg_configs)
        args = parser.parse_args()
        if args['condDesc'] == 'no_param' and args['checkDate'] == 'no_param':
            return res(success=False, code=500, message="Invalid Input: either condDesc or checkDate is expected")

        if args['condDesc'] != 'no_param' and args['checkDate'] != 'no_param':
            return res(success=False, code=500, message="Invalid input: either condDesc or checkDate is expected")

        if args['condDesc'] == 'no_param':
            args.pop('condDesc')
        if args['checkDate'] == 'no_param':
            args.pop('checkDate')

        try:
            if 'checkDate' in args:
                condition_list = self.condition_service.get_conditions_by_check_date_paginated(**args)
            else:
                condition_list = self.condition_service.get_conditions_by_description_paginated(**args)
            condition_json = [c.to_dict() for c in condition_list] if condition_list else None
            return res(data=condition_json)
        except Exception as e:
            error_message = str(e)
            return res(success=False, code=500, message="Error: " + error_message)

    def find_condition_by_patient(self):
        arg_configs = [
            {'name': 'condDesc', 'type': str, 'required': False, 'default': 'no_param'},
            {'name': 'checkDate', 'type': str, 'required': False, 'default': 'no_param'},
            {'name': 'page', 'type': int, 'required': False, 'default': 1},
            {'name': 'page_size', 'type': int, 'required': False, 'default': 10},
            {'name': 'patID', 'type': str, 'required': True}
        ]
        parser = create_parser(arg_configs)
        args = parser.parse_args()
        if args['condDesc'] == 'no_param' and args['checkDate'] == 'no_param':
            return res(success=False, code=500, message="Invalid Input: either condDesc or checkDate is expected")

        if args['condDesc'] != 'no_param' and args['checkDate'] != 'no_param':
            return res(success=False, code=500, message="Invalid input: either condDesc or checkDate is expected")

        if args['condDesc'] == 'no_param':
            args.pop('condDesc')
        if args['checkDate'] == 'no_param':
            args.pop('checkDate')

        try:
            if 'checkDate' in args:
                condition_list = self.condition_service.get_conditions_by_check_date_and_pat_id_paginated(**args)
            else:
                condition_list = self.condition_service.get_conditions_by_description_and_pat_id_paginated(**args)
            condition_json = [c.to_dict() for c in condition_list] if condition_list else None
            return res(data=condition_json)
        except Exception as e:
            error_message = str(e)
            return res(success=False, code=500, message="Error: " + error_message)

    def get_all_condition_by_patient(self, page, page_size, fetch_all, patID):
        condition_list = self.condition_service.get_all_conditions_by_pat_id(patID, page, page_size, fetch_all)
        condition_json = [c.to_dict() for c in condition_list]
        return res(data=condition_json)
