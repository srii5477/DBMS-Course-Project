
from flask import Flask, render_template, redirect, request
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def db_connection():
    db = psycopg2.connect(database="permalist",user="postgres",password="B220584cs*",host="localhost",port="5432")
    cursor = db.cursor()
    return db, cursor

@app.route('/')
def index():
    db, cursor = db_connection()
    cursor.execute('SELECT * FROM disaster')
    results = cursor.fetchall()
    db.close()
    print(results)
    return render_template("index.html", results=results)

# Form for adding a new incident
@app.route('/new-incident', methods=['POST'])
def new_incident():
    type_of_calamity = request.form.get('type_of_calamity')
    date = request.form.get('date')
    place = request.form.get('place')
    description = request.form.get('description')
    severity = request.form.get('severity')
    status = request.form.get('status')
    monitoring_bureau = request.form.get('monitoring_bureau')
    reqd_funds = request.form.get('reqd_funds')
    affected_pop = request.form.get('affected_pop')

    db, cursor = db_connection()
    
    # Fetch Disaster ID
    cursor.execute("SELECT id FROM disaster WHERE name=%s", (type_of_calamity,))
    disaster_id = cursor.fetchone()
    
    # Fetch Locality ID
    cursor.execute("SELECT id FROM locality WHERE name=%s", (place,))
    locality_id = cursor.fetchone()
    
    # Insert into Incident table
    cursor.execute(
        'INSERT INTO incident(did, lid, date, time, description, severity, status, monitoring_bureau, reqd_funds, affected_population) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (disaster_id[0], locality_id[0], date, description, severity, status, monitoring_bureau, reqd_funds, affected_pop)
    )
    db.commit()
    db.close()
    return redirect("/successfully_entered_page")


# Update an existing incident
@app.route('/update-incident', methods=['POST'])
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
    return redirect("/successfully-entered-page")

# Volunteer signup
@app.route('/volunteer-signup', methods=['POST'])
def volunteer_signup():
    name = request.form.get('name')
    contact = request.form.get('contact')
    address = request.form.get('address')
    oid = request.form.get('oid')
    print(name,contact,address,oid)
    db, cursor = db_connection()
    cursor.execute("select max(id) from volunteer")
    id=cursor.fetchone()
    #print(id)
    cursor.execute(
        'INSERT INTO volunteer(id,name, contact, address, oid) VALUES (%s, %s, %s, %s, %s)',
        (id[0]+1,name, contact, address,oid)
    )
    db.commit()
    db.close()
    return redirect("/successfully-entered-page")



# Redirect after successful entry
@app.route('/successfully-entered-page')
def successfully_entered_page():
    return render_template("success_page.html")


#view locality incident details
#get
@app.route('/locality-search', methods=['GET', 'POST'])
def locality_search():
    locality_info = None
    not_found_message = None
    
    if request.method == 'POST':
        locality_name = request.form.get('locality_name')
        
        # Database query to check if locality exists
        db, cursor = db_connection()
        cursor.execute("select id from locality where name = %s",(locality_name,))
        id=cursor.fetchone()
        cursor.execute("SELECT * FROM incident WHERE lid = %s", (id[0],))
        
        locality_info = cursor.fetchall()  # Fetch one row of locality info if it exists
        db.close()

        if not locality_info:
            not_found_message = "Sorry, locality not found."
        print(locality_info)
    
    return render_template('locality_search.html', locality_info=locality_info, not_found_message=not_found_message)
    
