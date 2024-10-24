from flask import Flask, render_template
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def db_connection():
    db = psycopg2.connect(os.getenv('POSTGRESQL_URI'))
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS disaster_types;")
    db.commit()
    cursor.execute("CREATE TABLE disaster_types (id SERIAL PRIMARY KEY, dname VARCHAR (50) UNIQUE NOT NULL, descrip TEXT NOT NULL, official_bureau TEXT NOT NULL, monitoring_status VARCHAR(10) NOT NULL, protocol TEXT NOT NULL);")
    db.commit()
    return db, cursor

@app.route('/')
def index():
    db, cursor = db_connection()
    sql = "INSERT INTO disaster_types (dname, descrip, official_bureau, monitoring_status, protocol) VALUES (%s, %s, %s, %s, %s)"
    val = ("Hurricane", "A tropical system with winds that have reached a constant speed of 74 miles per hour or more. ",
           "RSMC", "Active", "✓ Follow instructions issued by local officials. ✓ Take refuge in a small interior room, closet or hallway on the lowest level during the storm. Put as many walls between you and the outside as you can. ✓ Stay away from windows, skylights and glass doors.")
    cursor.execute(sql, val)
    db.commit()
    cursor.execute('SELECT* FROM disaster_types')
    results = cursor.fetchall()
    db.close()
    print(results)
    return render_template("index.html", results=results)