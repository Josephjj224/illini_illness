from flask_restful import Resource, reqparse
from ..services.symptom_service import SymptomService
from ..common.utils import res
from flask import request
from ..schema.register_sha import create_parser
from flask_jwt_extended import jwt_required


class SymptomResource(Resource):
    def __init__(self):
        self.symptom_service = SymptomService()

    '''
    FOR GET request:
        response format:
            {
            "success": true,
            "message": "Ok",
            "data": [
                {
                    "sympID": 3,
                    "sympDesc": "Nausea",
                    "rate": 2,
                    "checkDate": "2015-05-27",
                    "patID": "QEVuQwEAO+R1md5HUn8+w1Qpbg7ogw=="
                },
                ...
            ]}
            
        input: 
            1. if sympID is provided, it will just search for that specific symptom (single record)
                eg. 127.0.0.1:5000/api/symptom?sympID=3
            2. if patID is provided, it will just search for symptoms related to that patient
                eg. 127.0.0.1:5000/api/symptom?patID=QEVuQwEAaQwsI4fCpre8q2doTPVc0g%3d%3d
            3. if none of the above is provided, it will search for all symptoms.
                eg. 127.0.0.1:5000/api/symptom
            
            for 2 & 3: 
                all of the following are not required but have default value
                pass page(default: 1) to indicate which page of symptom records
                    eg. 127.0.0.1:5000/api/symptom?patID=QEVuQwEAaQwsI4fCpre8q2doTPVc0g%3d%3d?page=1
                pass page_size(default: 10) to indicate the size of every page
                    eg. 127.0.0.1:5000/api/symptom?patID=QEVuQwEAaQwsI4fCpre8q2doTPVc0g%3d%3d?page_size=100
                pass fetch_all(default: false) to indicate whether you want to get all data at one shot
                    eg. 127.0.0.1:5000/api/symptom?patID=QEVuQwEAaQwsI4fCpre8q2doTPVc0g%3d%3d?fetch_all=true
                    note: fetch_all will make page and page_size meaningless
                    
            one more thing:
                you can also combine different parameters
                127.0.0.1:5000/api/symptom?patID=QEVuQwEAaQwsI4fCpre8q2doTPVc0g%3d%3d?page=1&page_size=100
            
    '''
    def get(self):
        args = {}
        args['sympID'] = request.args.get('sympID', None, type=int)
        args['page'] = request.args.get('page', 1, type=int)
        args['page_size'] = request.args.get('page_size', 10, type=int)
        args['fetch_all'] = request.args.get('fetch_all', False, type=bool)
        args['patID'] = request.args.get('patID', None, type=str)
        if args['sympID']:
            # if sympID is provided, get specific symptom
            args.pop('patID')
            return self.get_symptom(args['sympID'])
        elif args['patID']:
            args.pop('sympID')
            return self.get_all_symptom_by_patient(**args)
        else:
            # otherwise, get all symptoms with page/pagesize...
            args.pop('sympID')
            args.pop('patID')
            return self.get_all_symptoms(**args)

    '''
    FOR POST request:
        response format 1 (find symptoms):
            {
            "success": true,
            "message": "Ok",
            "data": [
                {
                    "sympID": 3,
                    "sympDesc": "Nausea",
                    "rate": 2,
                    "checkDate": "2015-05-27",
                    "patID": "QEVuQwEAO+R1md5HUn8+w1Qpbg7ogw=="
                },
                ...
            ]}
            
        response format 2 (add, delete, update):
            {
                "success": true,
                "message": "Symptom add/delete/update successfully.",
                "data": null
            }
        
        

        input: 
            1. include "action": {update, add, delete, find, findPat} pick one of them to include which operation you want to do
            
            2. specific for every action:
                for update: update the record of sympID=3 with values of other attributes explicitly specified 
                    please fill in all attributes otherwise a null will be written to attributes that are not specified
                    eg.
                        {
                            "action": "update",
                            "sympID": 3,
                            "rate": 4,
                            "sympDesc": "Nausea",
                            "checkDate": "2015-05-27",
                            "patID": "QEVuQwEAO+R1md5HUn8+w1Qpbg7ogw=="
                        }
            
                for delete:
                    specify the sympID
                    eg.
                        {
                            "action": "delete",
                            "sympID": 3
                        }
                        
                for add:
                    no need to specify the sympID
                    eg. 
                    {
                        "action": "add",
                        "rate": 2,
                        "sympDesc": "Nausea",
                        "checkDate": "2015-05-27",
                        "patID": "QEVuQwEAO+R1md5HUn8+w1Qpbg7ogw=="
                    }
                    
                for find:
                    specify the checkDate or sympDesc, must specify exactly one parameter 
                    eg.
                    {
                        "checkDate": "2015-05-27",
                        "action": "find"
                    }
                    
                for findPat:
                    same as find, but this one needs to specify the patID. It will return symptoms only from specified patients with checkDate or sympDesc
                    eg.
                    {
                        "sympDesc": "Acute pain",
                        "patID": "QEVuQwEAaQwsI4fCpre8q2doTPVc0g==",
                        "action": "findPat",
                        "page_size": "100"
                    }
                    
                For last two, page & page_size & fetch_all are optional.
                    

    '''
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', required=True, choices=('add', 'update', 'delete', 'find', 'findPat'))
        args = parser.parse_args()

        action = args['action']
        if action == 'add':
            return self.add_symptom()
        elif action == 'update':
            return self.update_symptom()
        elif action == 'delete':
            return self.delete_symptom()
        elif action == 'find':
            return self.find_symptom()
        elif action == 'findPat':
            return self.find_symptom_by_patient()
        else:
            return res(message="Invalid Action", code=400)

    def get_symptom(self, sympID):
        symptom = self.symptom_service.get_symptom_by_id(sympID)
        if symptom:
            return res(data=symptom.to_dict(), success=True, code=200)
        else:
            return res(success=True, code=200)

    def get_all_symptoms(self, page, page_size=10, fetch_all=False):
        symptom_list = self.symptom_service.get_all_symptoms(page, page_size, fetch_all)
        symptom_json = [s.to_dict() for s in symptom_list]
        return res(data=symptom_json)


    def add_symptom(self):
        arg_configs = [
            {'name': 'sympDesc', 'type': str, 'required': True},
            {'name': 'rate', 'type': int, 'required': True},
            {'name': 'checkDate', 'type': str, 'required': True},
            {'name': 'patID', 'type': str, 'required': True},
        ]
        parser = create_parser(arg_configs)
        args = parser.parse_args()
        try:
            self.symptom_service.add_symptom(**args)
            return res(message='Symptom added successfully.')
        except Exception as e:
            error_message = str(e)
            return res(success=False, code=500, message="Error: " + error_message)

    def update_symptom(self):
        arg_configs = [
            {'name': 'sympDesc', 'type': str, 'required': True},
            {'name': 'rate', 'type': int, 'required': True},
            {'name': 'checkDate', 'type': str, 'required': True},
            {'name': 'patID', 'type': str, 'required': True},
            {'name': 'sympID', 'type': str, 'required': True}
        ]
        parser = create_parser(arg_configs)
        args = parser.parse_args()
        try:
            self.symptom_service.update_symptom(**args)
            return res(success=True, code=200, message="Symptom updated successfully.")
        except Exception as e:
            error_message = str(e)
            return res(success=False, code=500, message="Error: " + error_message)

    def delete_symptom(self):
        arg_configs = [
            {'name': 'sympID', 'type': str, 'required': True}
        ]
        parser = create_parser(arg_configs)
        args = parser.parse_args()
        try:
            self.symptom_service.delete_symptom(args['sympID'])
            return res(message="Symptom deleted successfully.")
        except Exception as e:
            error_message = str(e)
            return res(success=False, code=500, message="Error: " + error_message)

    def find_symptom(self):
        arg_configs = [
            {'name': 'sympDesc', 'type': str, 'required': False, 'default': 'no_param'},
            {'name': 'checkDate', 'type': str, 'required': False, 'default': 'no_param'},
            {'name': 'page', 'type': int, 'required': False, 'default': 1},
            {'name': 'page_size', 'type': int, 'required': False, 'default': 10}
        ]
        parser = create_parser(arg_configs)
        args = parser.parse_args()
        if args['sympDesc'] == 'no_param' and args['checkDate'] == 'no_param':
            return res(success=False, code=500, message="Invalid Input: either sympDesc or checkDate is expected")

        if args['sympDesc'] != 'no_param' and args['checkDate'] != 'no_param':
            return res(success=False, code=500, message="Invalid input: either sympDesc or checkDate is expected")

        if args['sympDesc'] == 'no_param':
            args.pop('sympDesc')
        if args['checkDate'] == 'no_param':
            args.pop('checkDate')

        try:
            if 'checkDate' in args:
                symptom_list = self.symptom_service.get_symptoms_by_check_date_paginated(**args)
            else:
                symptom_list = self.symptom_service.get_symptoms_by_description_paginated(**args)
            symptom_json = [s.to_dict() for s in symptom_list] if symptom_list else None
            return res(data=symptom_json)
        except Exception as e:
            error_message = str(e)
            return res(success=False, code=500, message="Error: " + error_message)

    def find_symptom_by_patient(self):
        arg_configs = [
            {'name': 'sympDesc', 'type': str, 'required': False, 'default': 'no_param'},
            {'name': 'checkDate', 'type': str, 'required': False, 'default': 'no_param'},
            {'name': 'page', 'type': int, 'required': False, 'default': 1},
            {'name': 'page_size', 'type': int, 'required': False, 'default': 10},
            {'name': 'patID', 'type': str, 'required': True}
        ]
        parser = create_parser(arg_configs)
        args = parser.parse_args()
        if args['sympDesc'] == 'no_param' and args['checkDate'] == 'no_param':
            return res(success=False, code=500, message="Invalid Input: either sympDesc or checkDate is expected")

        if args['sympDesc'] != 'no_param' and args['checkDate'] != 'no_param':
            return res(success=False, code=500, message="Invalid input: either sympDesc or checkDate is expected")

        if args['sympDesc'] == 'no_param':
            args.pop('sympDesc')
        if args['checkDate'] == 'no_param':
            args.pop('checkDate')

        try:
            if 'checkDate' in args:
                symptom_list = self.symptom_service.get_symptoms_by_check_date_and_pat_id_paginated(**args)
            else:
                symptom_list = self.symptom_service.get_symptoms_by_description_and_pat_id_paginated(**args)
            symptom_json = [s.to_dict() for s in symptom_list] if symptom_list else None
            return res(data=symptom_json)
        except Exception as e:
            error_message = str(e)
            return res(success=False, code=500, message="Error: " + error_message)


    def get_all_symptom_by_patient(self, page, page_size, fetch_all, patID):
        symptom_list = self.symptom_service.get_all_symptoms_by_pat_id(patID, page, page_size, fetch_all)
        symptom_json = [s.to_dict() for s in symptom_list]
        return res(data=symptom_json)