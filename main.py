
from flask import Flask, render_template, redirect, request, make_response
import psycopg2
from dotenv import load_dotenv
import os
import time

load_dotenv()

from urllib.parse import urlparse


app = Flask(__name__)

def db_connection():
    #db = psycopg2.connect(database="permalist",user="postgres",password="B220584cs*",host="localhost",port="5432")
    result = urlparse(os.getenv("POSTGRES_URI"))
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    db = psycopg2.connect(
        database=database, user=username, password=password, host=hostname, port=port
    )
    cursor = db.cursor()
    return db, cursor

@app.route('/')
def index():
    db, cursor = db_connection()
#     cursor.execute("""INSERT INTO emergency_service VALUES(1, 1, 'Ambulance', '12345', 120, 'Very fast'),
#                    (2, 1, 'Police Station', '23323', 120, 'Moderately fast'),
#                    (3, 1, 'Fire Station', '34567', 140, 'Fast'),
# (4, 1, 'Rescue Team', '45678', 160, 'Reliable'),
# (5, 1, 'Poison Control', '56789', 180, 'Prompt'),
# (6, 1, 'Disaster Relief', '67890', 200, 'Dependable'),
# (7, 1, 'Marine Patrol', '78901', 130, 'Efficient'),
# (8, 1, 'Mountain Rescue', '89012', 110, 'Quick response'),
# (9, 1, 'Animal Control', '90123', 150, 'Slow and understaffed'),
# (10, 1, 'Flood Relief', '01234', 170, 'Highly efficient');
                   
#                    """)
#     db.commit()
    cursor.execute('SELECT * FROM "incident"')
    results = cursor.fetchall()
    print(results)
    db.close()
    final = []
    j = 1
    for i in results:
        final.append(i[4])
        j+=1
    return render_template("index.html", results=final)

#add incident
@app.route('/new-incident')
def show_new_incident_form():
    return render_template("add_incident.html")
# post
@app.route('/new-incident', methods=['POST'])
def new_incident():
    type_of_calamity = request.form.get('type_of_calamity').title()
    date = request.form.get('date')
    place = request.form.get('place').title()
    description = request.form.get('description')
    severity = request.form.get('severity')
    status = request.form.get('status')
    active = int(request.form.get('active'))
    reqd_volunteers= int(request.form.get('reqd_volunteers'))
    monitoring_bureau = request.form.get('monitoring_bureau')
    reqd_funds = int(request.form.get('reqd_funds'))
    affected_pop = int(request.form.get('affected_pop'))
    incident_name = request.form.get('incident_name')

    print(incident_name)

    db, cursor = db_connection()
    
    cursor.execute("select max(id) from incident")
    id=cursor.fetchone()
    print(id)

    cursor.execute("SELECT id FROM disaster WHERE name=%s", (type_of_calamity,))
    disaster_id = cursor.fetchone()

    cursor.execute("SELECT id FROM locality WHERE name=%s", (place,))
    locality_id = cursor.fetchone()
    
    print(disaster_id)
    print(locality_id)

    cursor.execute(
        'INSERT INTO "incident" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)',
        (id[0]+1, disaster_id[0], locality_id[0], date, incident_name, description, severity, status, active, monitoring_bureau, reqd_funds, affected_pop, reqd_volunteers)
        )
    db.commit()
    cursor.execute('SELECT * FROM incident')
    print(cursor.fetchall())
    db.close()
    return redirect("/successfully-entered-page")


#add and update shelter
#get add shelter page
@app.route('/add-shelter')
def show_add_shelter():
    return render_template("add_shelter.html")

# post ()
@app.route('/add-shelter', methods=['POST'])
def add_shelter():
    place = request.form.get('place').title()
    name = request.form.get('name')
    contact=request.form.get('contact')
    address = request.form.get('address')
    max_capacity=request.form.get('max_capacity')

    db, cursor = db_connection()
    cursor.execute("SELECT id FROM locality WHERE name=%s", (place,))
    locality_id = cursor.fetchone()
    
    if not locality_id:
        return "Sorry locality not found"
    else:
        cursor.execute("select max(id) from shelter")
        id=cursor.fetchone()
        if id[0]==None:
            cursor.execute('INSERT INTO shelter VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (1,locality_id[0], name, contact, address, max_capacity, str(0),
            ))
        else:
            cursor.execute(
            'INSERT INTO shelter VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (id[0]+1,locality_id[0], name, contact, address, max_capacity, str(0),
            )
            )
        db.commit()
        db.close()
        return redirect("/successfully-entered-page")
        

@app.route('/update-shelter', methods=['POST'])
def update_shelter():
    place = request.form.get('place').title()
    name = request.form.get('name')
    contact=request.form.get('contact')
    no_new_ppl = request.form.get('no_new_ppl')
    db, cursor = db_connection()

    cursor.execute("SELECT id FROM locality WHERE name=%s", (place,))
    locality_id = cursor.fetchone()
    if(not locality_id):
        return "Sorry locality not found"
    
    else:
        cursor.execute("select id from shelter where name=%s and contact=%s",(name,contact,))
        id=cursor.fetchone()
        cursor.execute("select max_capacity,current_capacity from shelter where id=%s",(id,))
        result=cursor.fetchone()
        if(result[0]>=result[1]):
            return "Sorry cant add"
        cursor.execute(
        'update shelter set current_capacity=current_capacity+%s where id=%s',
        (no_new_ppl,id[0],)
        )
        db.commit()
        db.close()
        return redirect("/successfully-entered-page")
   
@app.route("/update-shelter-capacity", methods=["GET", "PATCH"])
def update_shelter_capacity():
    shelter_id = int(request.args.get('shelter_id'))
    db, cursor = db_connection()
    cursor.execute('SELECT * FROM shelter WHERE id=%s', (shelter_id,))
    result = cursor.fetchone()
    if result[6]==result[5]:
        return 'Cant allocate you in this shelter. Please select another.'
    else:
        cursor.execute('UPDATE shelter SET current_capacity=current_capacity+1 WHERE id=%s;', (shelter_id,))
    db.commit()
    db.close()
    return redirect("/successfully-entered-page")


@app.route("/await-admin-approval", methods=["GET"])
def await_admin_approval():
    response = make_response(render_template('loading.html'))
    response.headers["Refresh"] = "2; url=/successfully-entered-page"
    return response
    
    
@app.route("/donate-fund-individual", methods=["POST"])
def donate_fund_indi():
    name = request.form.get('name')
    contact = request.form.get('contact')
    std_amt_donated = request.form.get('std_amt_donated')
    incident_name = request.form.get('incident_name')
    
    db, cursor = db_connection()
    cursor.execute("SELECT MAX(id) FROM funding_source")
    max_id = cursor.fetchone()[0]
    new_fund_id = max_id + 1 if max_id is not None else 1
    cursor.execute("SELECT id FROM incident WHERE name LIKE %s", (incident_name,))
    iid = cursor.fetchone()
    if not iid:
        return "Could not add: Incident not found."
    cursor.execute("UPDATE incident SET reqd_funds = reqd_funds-%s WHERE id=%s", (std_amt_donated, iid))
    cursor.execute("SELECT id FROM funding_source WHERE name=%s", (name,))
    funding_id = cursor.fetchone()

    if funding_id is None:
        cursor.execute(
            "INSERT INTO funding_source (id, name, contact, type_of_organization) VALUES (%s, %s, %s,%s)",
            (new_fund_id, name, contact, "Individual")
        )
        funding_id = (new_fund_id,)  

    cursor.execute(
        "INSERT INTO incident_funding (iid, fid, std_amt_donated, amt_left) VALUES (%s, %s, %s, %s)",
        (iid[0], funding_id[0], std_amt_donated, std_amt_donated)
    )

    db.commit()
    db.close()
    return redirect("/await-admin-approval")


@app.route('/donate-fund-org', methods=['POST'])
def donate_fund_org():
    name = request.form.get('name')
    contact = request.form.get('contact')
    std_amt_donated = request.form.get('std_amt_donated')
    incident_name = request.form.get('incident_name')
    contract_terms = request.form.get('contract_terms')
    renewal_period = request.form.get('renewal_period')
    type_of_organisation = request.form.get('type_of_organisation')

    db, cursor = db_connection()

    cursor.execute("SELECT MAX(id) FROM funding_source")
    max_id = cursor.fetchone()[0]
    if(not max_id):
        new_fund_id=1
    new_fund_id = max_id + 1 


    cursor.execute("SELECT id FROM incident WHERE name LIKE %s", (incident_name,))
    iid = cursor.fetchone()
    if not iid:
        return "Incident not found, could not add funding."
    
    cursor.execute("SELECT id FROM funding_source WHERE name=%s", (name,))
    funding_id = cursor.fetchone()

    if funding_id is None:
        cursor.execute(
            "INSERT INTO funding_source (id, name, contract_terms, renewal_period, contact, type_of_organization) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (new_fund_id, name, contract_terms, renewal_period, contact, type_of_organisation)
        )
        funding_id = (new_fund_id,)  
    cursor.execute(
        "INSERT INTO incident_funding (iid, fid, std_amt_donated, amt_left) VALUES (%s, %s, %s, %s)",
        (iid[0], funding_id[0], std_amt_donated, std_amt_donated)
    )
    cursor.execute(
        "UPDATE incident SET reqd_funds = reqd_funds-%s WHERE id=%s", (std_amt_donated, iid[0])
    )
    db.commit()
    db.close()
    return redirect("/await-admin-approval")

@app.route('/find-emergency-services', methods=['GET'])
def find_emergency_services():
    locality = request.args.get('locality').title()
    print(locality)
    db, cursor = db_connection()
    cursor.execute('select id from locality where name=%s', (locality,))
    result = cursor.fetchone()
    cursor.execute('select * from emergency_service where lid=%s', (result,))
    contacts = cursor.fetchall()
    print(contacts)
    return render_template('contact.html', contacts=contacts)

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

#Contact page route
@app.route('/contact-us')
def contact_us():
    return render_template("contact.html")

#view locality incident details
#get
@app.route('/locality-search', methods=['GET', 'POST'])
def locality_search():
    locality_info = None
    not_found_message = ""
    locality_shelters = None

    if request.method == "POST":
        locality_name = request.form.get("locality_name").title()
        print(locality_name)
        db, cursor = db_connection()
        cursor.execute("select id from locality where name = %s", (locality_name,))
        id = cursor.fetchone()
        print(id)
        cursor.execute("SELECT * FROM incident WHERE lid = %s", (id[0],))

        locality_info = cursor.fetchall() 

        if not locality_info:
            not_found_message = "The locality you have entered is invalid or there are no active incidents there."
        print(locality_info)
        cursor.execute("select * from shelter where lid=%s", (id[0],))
        locality_shelters = cursor.fetchall()
        db.close()
        if not locality_shelters:
            not_found_message += "No shelters were found in this locality."
    
    return render_template('locality_search.html', locality_info=locality_info, not_found_message=not_found_message, locality_shelters=locality_shelters)
    
@app.route('/donate-resource', methods=['GET'])
def donate_resource():
    db, cursor = db_connection()
    # cursor.execute("""
    #                 insert into essential values(1, 'Bread', 5, 0),
    #                 (2, 'Water', 1, 50),
    #                 (3, 'Noodles', 2, 100),
    #                 (4, 'Sanitary Pad', 10, 30),
    #                 (5, 'Rice', 3, 200),
    #                 (6, 'Soap', 2, 75),
    #                 (7, 'Toothpaste', 3, 40),
    #                 (8, 'Milk', 4, 25),
    #                 (9, 'Sugar', 2, 60),
    #                 (10, 'Salt', 1, 80);
    #                """)
    # db.commit()
    cursor.execute('select name from essential;')
    results = cursor.fetchall()
    db.close()
    return render_template('donate_resource.html', results=results)

@app.route('/allocate-resource', methods=['POST'])
def allocate_resource():
    db, cursor = db_connection()
    # cursor.execute("""
    #                drop table if exists incident_resource_allocation;
    #                CREATE TABLE "incident_resource_allocation" (
    #                 "iid" integer,
    #                 "eid" integer,
    #                 "qty_donated" integer
    #                );
    #                ALTER TABLE "incident_resource_allocation" ADD FOREIGN KEY ("iid") REFERENCES "incident" ("id");

    #                ALTER TABLE "incident_resource_allocation" ADD FOREIGN KEY ("eid") REFERENCES "essential" ("id");
    #                """)
    # db.commit()
    incident_name = request.form.get('incident_name').title()
    essential_name = request.form.get('essential_name').title()
    qty_donated = int(request.form.get('quantity'))
    #check if incident exists, if essential exists and if so add the relevant details
    #into the incident_resource_allocation table
    cursor.execute('select id from incident where name=%s', (incident_name,))
    result = cursor.fetchone()
    if result == None:
        return "Such an incident doesn't exist. Try again."
    iid = result
    cursor.execute('select id from essential where name=%s', (essential_name,))
    result = cursor.fetchone()
    if result == None:
        return 'Such an essential does not exist in our catalogue. Try another one.'
    eid = result
    cursor.execute('insert into incident_resource_allocation values(%s, %s, %s);', (iid, eid, qty_donated))
    db.commit()
    db.close()
    
    return redirect("/await-admin-approval")

@app.route('/view-resource-allocations', methods=['GET'])
def view_resource_allocations():
    db, cursor = db_connection()
    #find corresponding essential name from its id, incident name from its id
    incident_name = request.args.get('incident').title()
    cursor.execute('select id from incident where name=%s', (incident_name,))
    result=cursor.fetchone()
    if result == None:
        return 'Select an existing incident.'
    cursor.execute('select eid, qty_donated from incident_resource_allocation where iid=%s', (result,))
    result = cursor.fetchall()
    if result == None:
        return 'No resources allocated for this incident yet. Please consider donating.'
    final = []
    for i in result:
        cursor.execute('select name from essential where id=%s', (i[0],))
        e_name = cursor.fetchone()
        final.append([incident_name, e_name[0], i[1]])
    return render_template('view_resource.html', final=final)