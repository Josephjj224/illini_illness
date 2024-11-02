from flask import Blueprint
from flask_restful import Api
from .resources.auth_resources import Login, Register, GetDoctorList, ExecuteProcedure
from .resources.symptom_resource import SymptomResource
from .resources.condition_resource import ConditionResource
from .resources.treatment_resource import TreatmentResource


api_blueprint = Blueprint('api', __name__, url_prefix="/api")
api = Api(api_blueprint)
api.add_resource(Register, '/register')
api.add_resource(Login, '/login', '/refreshToken')
# api.add_resource(Logout, '/logout',)
# api.add_resource(GetAllUsers, '/getUserList')
# api.add_resource(GetCurrentUser, '/getCurrentUser')
api.add_resource(SymptomResource, '/symptom')
api.add_resource(ConditionResource, '/condition')
api.add_resource(GetDoctorList, '/doctor-list')
api.add_resource(TreatmentResource, '/treatment')
api.add_resource(ExecuteProcedure, '/execute-procedure')