
from flask import Flask, render_template, redirect, request
import psycopg2
from dotenv import load_dotenv
import os

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
    cursor.execute('SELECT * FROM "incident" where active=1')
    results = cursor.fetchall()
    print(results)
    db.close()
    final = []
    j = 1
    for i in results:
        final.append('#'+str(j)+': '+i[4])
        j+=1
    return render_template("index.html", results=final)

#add incident
@app.route('/new-incident')
def show_new_incident_form():
    return render_template("add_incident.html")
# post
@app.route('/new-incident', methods=['POST'])
def new_incident():
    type_of_calamity = request.form.get('type_of_calamity')
    date = request.form.get('date')
    place = request.form.get('place')
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
    place = request.form.get('place')
    name = request.form.get('name')
    contact=request.form.get('contact')
    address = request.form.get('address')
    max_capacity=request.form.get('max_capacity')

    print(type(max_capacity))
    print("Veda")
    db, cursor = db_connection()

    # Fetch Locality ID
    cursor.execute("SELECT id FROM locality WHERE name=%s", (place,))
    locality_id = cursor.fetchone()
    
    if not locality_id:
        return "Sorry locality not found"
    else:
        # Insert into shleter table
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
    place = request.form.get('place')
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

@app.route("/donate-fund-indi", methods=["POST"])
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
    return redirect("/successfully-entered-page")


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
    
    db.commit()
    db.close()
    return redirect("/successfully-entered-page")

#get fund alloc page
@app.route('/fund-alloc')
def show_fund_alloc():
    return render_template("fund_alloc.html")



@app.route('/fund-alloc', methods=['POST'])
def fund_alloc():
    incident_name = request.form.get('incident_name')
    fund = request.form.get('fund') 
    
    db, cursor = db_connection()
    
    cursor.execute("SELECT id FROM incident WHERE name LIKE %s", (incident_name,))
    iid = cursor.fetchone()
    
    if not iid:
        return "Incident not found"
    
    cursor.execute("SELECT reqd_funds FROM incident WHERE id=%s", (iid[0],))
    result = cursor.fetchone()
    print(type(result))

    if result[0] == 0 or result[0] < int(fund):
        return "Sorry, cannot allocate the requested fund amount"

    cursor.execute("SELECT fid FROM incident_funding WHERE iid=%s", (iid[0],))
    funding_sources = cursor.fetchall()

    for funding_source in funding_sources:
        fid = funding_source[0]
        cursor.execute("SELECT amt_left FROM incident_funding WHERE fid=%s and iid=%s", (fid,iid[0]))
        amt_left = cursor.fetchone()[0]
        temp = int(fund) - int(amt_left)
        
        if temp >= 0:
            cursor.execute("DELETE FROM incident_funding WHERE fid=%s AND iid=%s", (fid, iid[0]))
        else:
            cursor.execute(
                "UPDATE incident_funding SET amt_left=%s WHERE fid=%s AND iid=%s",
                (int(int(amt_left) - int(fund)), fid, iid[0])
            )
            fund = 0  
            break  
        fund = temp

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
        locality_name = request.form.get("locality_name")
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
    
