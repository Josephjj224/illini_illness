from flask_restful import Resource, reqparse
from ..services.treatment_service import TreatmentService
from ..common.utils import res
from flask import request
from ..schema.register_sha import create_parser
from flask_jwt_extended import jwt_required


class TreatmentResource(Resource):
    def __init__(self):
        self.treatment_service = TreatmentService()


    def get(self):
        args = {}
        args['treatID'] = request.args.get('treatID', None, type=int)
        args['page'] = request.args.get('page', 1, type=int)
        args['page_size'] = request.args.get('page_size', 10, type=int)
        args['fetch_all'] = request.args.get('fetch_all', False, type=bool)
        args['patID'] = request.args.get('patID', None, type=str)
        if args['treatID']:
            args.pop('patID')
            return self.get_treatment(args['treatID'])
        elif args['patID']:
            args.pop('treatID')
            return self.get_all_treatment_by_patient(**args)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', required=True, choices=('add', 'update', 'delete', 'find', 'findPat'))
        args = parser.parse_args()

        action = args['action']
        if action == 'findPat':
            return self.find_treatment_by_patient()
        else:
            return res(message="Invalid Action", code=400)

    def get_treatment(self, treatID):
        treatment = self.treatment_service.get_treatment_by_id(treatID)
        if treatment:
            return res(data=treatment.to_dict(), success=True, code=200)
        else:
            return res(success=True, code=200)

    def find_treatment_by_patient(self):
        arg_configs = [
            {'name': 'treatDesc', 'type': str, 'required': False, 'default': 'no_param'},
            {'name': 'checkDate', 'type': str, 'required': False, 'default': 'no_param'},
            {'name': 'page', 'type': int, 'required': False, 'default': 1},
            {'name': 'page_size', 'type': int, 'required': False, 'default': 10},
            {'name': 'patID', 'type': str, 'required': True}
        ]
        parser = create_parser(arg_configs)
        args = parser.parse_args()
        if args['treatDesc'] == 'no_param' and args['checkDate'] == 'no_param':
            return res(success=False, code=500, message="Invalid Input: either treatDesc or checkDate is expected")

        if args['treatDesc'] != 'no_param' and args['checkDate'] != 'no_param':
            return res(success=False, code=500, message="Invalid input: either treatDesc or checkDate is expected")

        if args['treatDesc'] == 'no_param':
            args.pop('treatDesc')
        if args['checkDate'] == 'no_param':
            args.pop('checkDate')

        try:
            if 'checkDate' in args:
                treat_list = self.treatment_service.get_treatments_by_check_date_and_pat_id_paginated(**args)
            else:
                treat_list = self.treatment_service.get_treatments_by_description_and_pat_id_paginated(**args)
            treat_json = [t.to_dict() for t in treat_list] if treat_list else None
            return res(data=treat_json)
        except Exception as e:
            error_message = str(e)
            return res(success=False, code=500, message="Error: " + error_message)

    def get_all_treatment_by_patient(self, page, page_size, fetch_all, patID):
        treat_list = self.treatment_service.get_all_treatments_by_pat_id(patID, page, page_size, fetch_all)
        treat_json = [t.to_dict() for t in treat_list]
        return res(data=treat_json)
