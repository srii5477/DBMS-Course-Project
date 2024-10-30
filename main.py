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

# Form for adding a new incident
@app.route('/new_incident', methods=['POST'])
def new_incident():
    type_of_calamity = request.form.get('type_of_calamity')
    date = request.form.get('date')
    time = request.form.get('time')
    place = request.form.get('place')
    description = request.form.get('description')
    severity = request.form.get('severity')
    status = request.form.get('status')
    monitoring_bureau = request.form.get('monitoring_bureau')
    reqd_funds = request.form.get('reqd_funds')
    affected_pop = request.form.get('affected_pop')

    db, cursor = db_connection()
    
    # Fetch Disaster ID
    cursor.execute("SELECT id FROM Disaster WHERE name=%s", (type_of_calamity,))
    disaster_id = cursor.fetchone()
    
    if not disaster_id:
        db.close()
        return redirect("/add_disaster_info")
    
    # Fetch Locality ID
    cursor.execute("SELECT id FROM Locality WHERE name=%s", (place,))
    locality_id = cursor.fetchone()
    
    if not locality_id:
        db.close()
        return redirect("/add_location_info")
    
    # Insert into Incident table
    cursor.execute(
        'INSERT INTO Incident(did, lid, date, time, description, severity, status, monitoring_bureau, reqd_funds, affected_population) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (disaster_id[0], locality_id[0], date, time, description, severity, status, monitoring_bureau, reqd_funds, affected_pop)
    )
    db.commit()
    db.close()
    return redirect("/successfully_entered_page")

# Add locality information
@app.route('/add_location_info', methods=['POST'])
def add_location_info():
    name = request.form.get('name')
    geographical_size = request.form.get('geographical_size')
    development_level = request.form.get('development_level')
    db, cursor = db_connection()
    cursor.execute(
        'INSERT INTO Locality(name, geographical_size, development_level) VALUES (%s, %s, %s)',
        (name, geographical_size, development_level)
    )
    db.commit()
    db.close()
    return redirect("/new_incident")

# Add disaster information
@app.route('/add_disaster_info', methods=['POST'])
def add_disaster_info():
    name = request.form.get('name')
    description = request.form.get('description')
    protocol = request.form.get('protocol')
    db, cursor = db_connection()
    cursor.execute(
        'INSERT INTO Disaster(name, description, protocol) VALUES (%s, %s, %s)',
        (name, description, protocol)
    )
    db.commit()
    db.close()
    return redirect("/new_incident")

# Update an existing incident
@app.route('/update_incident', methods=['POST'])
def update_incident():
    id = request.form.get('id')
    severity = request.form.get('severity')
    status = request.form.get('status')
    monitoring_bureau = request.form.get('monitoring_bureau')
    reqd_funds = request.form.get('reqd_funds')
    affected_pop = request.form.get('affected_pop')

    db, cursor = db_connection()
    cursor.execute(
        "UPDATE Incident SET severity=%s, status=%s, monitoring_bureau=%s, reqd_funds=%s, affected_population=%s WHERE id=%s",
        (severity, status, monitoring_bureau, reqd_funds, affected_pop, id)
    )
    db.commit()
    db.close()
    return redirect("/successfully_entered_page")

# Volunteer signup
@app.route('/volunteer_signup', methods=['POST'])
def volunteer_signup():
    name = request.form.get('name')
    contact = request.form.get('contact')
    address = request.form.get('address')
    age = request.form.get('age')

    db, cursor = db_connection()
    cursor.execute(
        'INSERT INTO Volunteer(name, contact, address, age) VALUES (%s, %s, %s, %s)',
        (name, contact, address, age)
    )
    db.commit()
    db.close()
    return redirect("/successfully_entered_page")

# Redirect after successful entry
@app.route('/successfully_entered_page')
def successfully_entered_page():
    return redirect("/")

