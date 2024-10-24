from flask import Flask, render_template
import mysql.connector
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()

app = Flask(__name__)

def db_connection():
    mydb = mysql.connector.connect(
            host="localhost",
            user=os.getenv("USER"),
            password=os.getenv("PW"),
            database="world"
    )
    cursor = mydb.cursor()
    return mydb, cursor

@app.route('/')
def index():
    mydb, cursor = db_connection()
    sql = "INSERT INTO disaster_types (dname, descrip, official_bureau, monitoring_status, protocol) VALUES (%s, %s, %s, %s, %s)"
    val = ("Hurricane", "A tropical system with winds that have reached a constant speed of 74 miles per hour or more. ",
           "RSMC", "Active", "✓ Follow instructions issued by local officials. ✓ Take refuge in a small interior room, closet or hallway on the lowest level during the storm. Put as many walls between you and the outside as you can. ✓ Stay away from windows, skylights and glass doors.")
    cursor.execute(sql, val)
    mydb.commit()
    cursor.execute('SELECT* FROM disaster_types')
    results = cursor.fetchall()
    mydb.close()
    print(results)
    return render_template("index.html", results=results)