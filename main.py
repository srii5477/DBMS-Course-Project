from flask import Flask, render_template
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def db_connection():
    db = psycopg2.connect(os.getenv('POSTGRESQL_URI'))
    cursor = db.cursor()
    return db, cursor

@app.route('/')
def index():
    db, cursor = db_connection()
    cursor.execute('SELECT* FROM Disaster')
    results = cursor.fetchall()
    db.close()
    print(results)
    return render_template("index.html", results=results)

