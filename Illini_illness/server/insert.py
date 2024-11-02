import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)
cursor = db.cursor(dictionary=True)

# joins items with commas
def join(items):
    return ", ".join(items)

# joins with commas, as single-quoted strings
def joinAsStrings(items):
    return "\'" + "', '".join(map(str, items)) + "\'"

def insert(row):
    cursor.execute(f"insert into Users values ({row.docID}, '********', '{row.firstName + row.lastName + '@example.com'}')")
    cursor.execute(f"insert into Doctors values ({joinAsStrings(row[:])})")

doctors = pd.read_csv("../fakedoctor.csv")
doctors.apply(insert, axis=1)

db.commit()
