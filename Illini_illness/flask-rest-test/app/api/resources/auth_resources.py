from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

from ..schema.register_sha import reg_args_valid
from ..common.utils import res2
from ...config import Config
from ..services.auth_service import AuthService
from flask_jwt_extended import jwt_required
from flask import Flask, request, redirect, render_template, url_for, session, jsonify
import mysql.connector
import base64


connection = mysql.connector.connect(**Config.MYSQL_CONFIG)
cursor = connection.cursor(dictionary=True)


class Login(Resource):
    def __init__(self):
        self.auth_service = AuthService()

    def post(self):
        data = request.json  # Get data from JSON request
        email = data['email']
        password = data['password']
        print(email, password, data)

        cursor.execute("select * from Users where email = %s", (email,))
        user = cursor.fetchone()

        if user and user['password'] == password:
            cursor.execute("select * from Doctors where docID = %s", (user['userID'],))
            if cursor.fetchone():
                # User is a doctor
                # return jsonify({"role": "doctor", "ID": user['userID']}), 200
                return res2(data={"role": "doctor", "ID": user['userID']})

            cursor.execute("select * from Patients where patID = %s", (user['userID'],))
            patient = cursor.fetchone()
            if patient:
                # User is a patient
                first_name = patient['firstName']
                last_name = patient['lastName']
                return res2(data={"role": "patient", "ID": user['userID'], "firstName": first_name, "lastName": last_name})

            # User exists but is neither a doctor nor a patient
            return res2(message="User role not defined", code=500, success=False)
        else:
            # Login failed
            return res2(message="Login Failed", code=500, success=False)

    # @jwt_required(refresh=True)
    # def get(self):
    #     # After the access token expires, use the refresh token to obtain a new token
    #     # Retrieve the current email from the refresh token
    #     current_email = get_jwt_identity()
    #
    #     # Generate a new access token
    #     access_token = create_access_token(identity=current_email)
    #
    #     # Return the new access token in the response
    #     return res(data={'accessToken': 'Bearer ' + access_token})


class Register(Resource):
    def __init__(self):
        self.auth_service = AuthService()

    def post(self):
        data = request.json
        email = data['email']
        password = data['password']
        role = data['role']
        first_name = data['firstName']
        last_name = data['lastName']
        phone = data['phone']

        age = data.get('age') if role == 'patient' else None
        gender = data.get('gender') if role == 'patient' else None

        cursor.execute("select * from Users where email = %s", (email,))
        if cursor.fetchone():
            return res2(message="Email Already Registered", code=400, success=False)

        user_data = {
            "password": password,
            "email": email
        }
        insert("Users", user_data)

        cursor.execute("select * from Users where email= %s", (email,))
        user_dict = cursor.fetchone()
        user_id = user_dict['userID']

        # Additional handling for patients
        if role == 'patient':
            patient_data = {
                "patID": user_id,
                "firstName": first_name,
                "lastName": last_name,
                "phone": phone,
                "age": age,
                "gender": gender
            }
            insert("Patients", patient_data)
            return res2(data={"role": role, "ID": user_id, "firstName": first_name, "lastName":last})
        elif role == 'doctor':
            doctor_data = {
                "docID": user_id,
                "firstName": first_name,
                "lastName": last_name,
                "phone": phone,
            }
            insert("Doctors", doctor_data)
            # You may want to add similar handling for doctors
            return res2(data={"role": role, "ID": user_id})


# def generator_id():
#     random_bytes = os.urandom(16)
#     encoded_id = base64.b64encode(random_bytes).decode('utf-8')
#     return encoded_id
class GetDoctorList(Resource):
    def get(self):
        cursor.execute("select * from Doctors")
        doctors = cursor.fetchall()

        doctors_list = []
        for doc in doctors:
            doc_dict = {
                'docID': doc['docID'],
                'firstName': doc['firstName'],
                'lastName': doc['lastName'],
                'phone': doc['phone']
            }
            doctors_list.append(doc_dict)

        # return jsonify(doctors=doctors_list), 200
        return res2(data={"doctors": doctors_list})

def insert(table, row):
    cursor.execute(f"insert into {table}({join(row.keys())}) values ({joinAsStrings(row.values())})")
    connection.commit()
    return selectAll(table)


def selectAll(table):
    cursor.execute(f"select * from {table}")
    res = cursor.fetchall()
    return res


# joins items with commas
def join(items):
    return ", ".join(items)


# joins with commas, as single-quoted strings
def joinAsStrings(items):
    return "\'" + "', '".join(items) + "\'"

class ExecuteProcedure(Resource):
    def post(self):
        self.execute_procedure()
    def execute_procedure(self):
        data = request.json
        patID = data['patID']
        try:
            conn = connection
            cursor = conn.cursor()

            # 调用存储过程
            call_statement = f"CALL CheckPatientAlerts('{patID}')"
            cursor.execute(call_statement)

            connection.commit()
            # 获取存储过程返回的数据
            result = []
            for result_set in cursor.stored_results():
                result.append(result_set.fetchall())

            # cursor.close()
            # conn.close()
            return "succeed in calling procedure"

        except Exception as e:
            return "error happens"
