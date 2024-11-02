from flask import Flask,request, redirect, render_template, url_for, session, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
import base64
from flask_cors import CORS


load_dotenv()
app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)
cursor = db.cursor(dictionary=True)


# Joseph Jaeyun Jeong: NOV 20 2023
#  this function basically generates the userID using* base64 encoding
# by doing it we can create unique userID (Primary Key)
#

def generator_id():
    random_bytes = os.urandom(16)
    encoded_id = base64.b64encode(random_bytes).decode('utf-8')
    return encoded_id


app.secret_key = generator_id()  # secret_key need it to use session


# Joseph Jaeyun Jeong: NOV 27 2023
#  endpoint for register page
# user can create their credential and save that credential in database
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
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
            return jsonify({"message": "Email already registered"}), 400

        while True:
            user_id = generator_id()
            cursor.execute("select * from Users where userID = %s", (user_id,))
            if not cursor.fetchone():
                break

        user_data = {
            "userID": user_id,
            "password": password,
            "email": email
        }
        insert("Users", user_data)


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
            return jsonify({"role":role ,"ID":user_id}), 200
        elif role == 'doctor':
            doctor_data = {
                "docID": user_id,
                "firstName": first_name,
                "lastName": last_name,
                "phone": phone,
            }
            insert("Doctors", doctor_data)
            # You may want to add similar handling for doctors
            return jsonify({"role":role ,"ID":user_id}), 200



@app.get('/doctor-list')
def doctor_list():
    if request.method == 'GET':
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

        return jsonify(doctors=doctors_list), 200






@app.post("/login")
def login():
    data = request.json  # Get data from JSON request
    email = data['email']
    password = data['password']
    print(email,password,data)

    cursor.execute("select * from Users where email = %s", (email,))
    user = cursor.fetchone()

    if user and user['password'] == password:
        cursor.execute("select * from Doctors where docID = %s", (user['userID'],))
        if cursor.fetchone():
            # User is a doctor
            return jsonify({"role": "doctor" ,"ID": user['userID'] }), 200

        cursor.execute("select * from Patients where patID = %s", (user['userID'],))
        if cursor.fetchone():
            # User is a patient
            return jsonify({"role": "patient", "ID": user['userID']}), 200

        # User exists but is neither a doctor nor a patient
        return jsonify({"message": "User role not defined", "ID": user['userID']}), 200
    else:
        # Login failed
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401





@app.route('/')
def foo():
    return selectAll("Users")
    # data = {"userID": "user1", "email": "user1@gmail.com", "password": "iAmUser1"}
    # return insert("Users", data)

def insert(table, row):
    cursor.execute(f"insert into {table}({join(row.keys())}) values ({joinAsStrings(row.values())})")
    db.commit()
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



if __name__ == '__main__':
    app.run(debug=True)
