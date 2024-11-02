from ..services.patient_service import PatientService
from flask_restful import Resource, reqparse


class PatientResource(Resource):
    def __init__(self):
        self.patient_service = PatientService()

    def get(self):
        args = {}
        args['patID'] = request.args.get('patID', None, type=str)
        if args['patID']:
            return self.patient_service.get_patient_by_id(args['patID'])


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', required=True, choices=('add', 'update'))
        args = parser.parse_args()

        action = args['action']
        if action == 'add':
            return self.add_patient()
        elif action == 'update':
            return self.update_patient()
        else:
            return res(message="Invalid Action", code=400)


    def add_patient(self):
        arg_configs = [
            {'name': 'Pat', 'type': str, 'required': True},
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