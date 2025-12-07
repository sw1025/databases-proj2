#Referenced Flask slides
# referenced GeekforGeeks.
# https://www.geeksforgeeks.org/python/hashing-passwords-in-python-with-bcrypt/

from flask import Flask, render_template, request, session, url_for, redirect 
import bcrypt
import pymysql

app = Flask(__name__)

app.secret_key = 'key that you cant guess'

conn = pymysql.connect(host ='127.0.0.1',
                       user = 'root',
                       password = '',
                       port=3307,
                       db = 'air_reservation',
                       charset = 'utf8mb4',
                       cursorclass = pymysql.cursors.DictCursor)

@app.route('/loginAuth',methods=['POST'])

def loginAuth():
    login_type = request.form['login_type']
    email = request.form['username']
    password = request.form['password']

    pwd_bytes = password.encode('utf-8')
	
    print(request.form)

    #Send query to database by calling execute method of cursor
    cursor = conn.cursor()

    if (login_type == "customer"):
        query = 'SELECT * FROM customer WHERE email = %s'
    elif (login_type == "agent"):
        query = 'SELECT * FROM booking_agent WHERE email = %s'
    elif (login_type == "staff"):
        query = 'SELECT * FROM airline_staff WHERE username = %s'

    cursor.execute(query,(email,))

    data = cursor.fetchone()
    cursor.close()
    error = None
    if(data):
        result = bcrypt.checkpw(pwd_bytes, data['password'].encode('utf-8'))
        if (result):
            session['username'] = email
            if (login_type == "customer"):
                return redirect(url_for('cust_dashboard'))
            elif (login_type == "agent"):
                return redirect(url_for('agent_dashboard'))
            elif (login_type == "staff"):
                return redirect(url_for('staff_dashboard'))
        else:
            error = 'Wrong password'
            return render_template('login.html',error=error)
    else:
        error = 'Invalid username'
        return render_template('login.html',error=error)
    
@app.route('/registerAuth',methods=['POST'])
def registerAuth():
    register_type = request.form['register_type']
    username = request.form['username']
    password = request.form['password']
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes,salt)
    password = hash

    if (register_type == "customer"):
        name = request.form['name']
        building_number = request.form['buildingnum']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        phone_number = request.form['tel']
        passport_number = request.form['passportid']
        passport_expiration = request.form['passportexp']
        passport_country = request.form['country']
        date_of_birth = request.form['dob']
    elif (register_type == "staff"):
        f_name = request.form['first_name']
        l_name = request.form['last_name']
        date_of_birth = request.form['dob']
        airline = request.form['airline_name']
        role = request.form['role']
    
    #Send query to database by calling execute method of cursor
    cursor = conn.cursor()

    if (register_type == "customer"):
        query = 'SELECT * FROM customer WHERE email = %s'
    elif (register_type == "agent"):
        query = 'SELECT * FROM booking_agent WHERE email = %s'
    elif (register_type == "staff"):
        query = 'SELECT * FROM airline_staff WHERE username = %s'

    cursor.execute(query,(username,))

    data = cursor.fetchone()

    if(data):
        error = 'User already exists'
        cursor.close()
        return render_template('register.html',error=error)
    else:
        if (register_type == "customer"):
            ins = 'INSERT INTO customer VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(ins,(username,name,password,building_number,street,city,state,phone_number,passport_number,passport_expiration,passport_country,date_of_birth))
        elif (register_type == "agent"):
            ins = 'INSERT INTO booking_agent VALUES(%s,%s)'
            cursor.execute(ins,(username,password))
        elif (register_type == "staff"):
            ins = 'INSERT INTO airline_staff VALUES(%s,%s)'
            cursor.execute(ins,(username,password,f_name,l_name,date_of_birth,airline,role))
        
        conn.commit()
        cursor.close()
        
        return redirect(url_for('home'))

@app.route('/flightSearch',methods =['POST'])
def flightSearch():
    search_type = request.form['search_type']
    origin = request.form['origin']
    dest = request.form['dest']
    city = request.form['city']
    dep_date = request.form['dep_date']
    arr_date = request.form['arr_date']
    airline_name = request.form['airline_name']
    flight_num = request.form['flight_num']
    
    cursor = conn.cursor()

    if (search_type == "upcoming" or search_type == "purchase"):
        query = 'SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND DATE(departure_time) = %s AND DATE(arrival_time) = %s AND status = "upcoming"'
        cursor.execute(query,(origin,dest,dep_date,arr_date ))
    elif (search_type == "inprogress"):
        query = 'SELECT * FROM flight WHERE airline_name = %s and flight_num = %s AND status = "in-progress"'
        cursor.execute(query,(airline_name, flight_num))

    flights = cursor.fetchall()
    cursor.close()
    error = None

    if (flights):
        result = "Flights found"
    else:
        result = "No flights found"
    return render_template("flight_search.html",error=error,result=result,flights=flights) #add in specifci html file


@app.route('/cust_dashboard')
def cust_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('cust_dashboard.html')

@app.route('/purchased_flights',methods=['GET'])
def purchased_flights():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('purchased_flights.html')

@app.route('/spending',methods=['GET'])
def spending():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('spending.html')

@app.route('/register',methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/login',methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/flight_search',methods=['GET'])
def flight_search():
    return render_template('flight_search.html')

@app.route('/staff_dashboard',methods=['GET'])
def staff_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('staff_dashboard.html')

@app.route('/agent_dashboard',methods=['GET'])
def agent_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('agent_dashboard.html')

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')


#run app on localhost port 5000
#debug = True means no need to restart flask for changes to go through
if __name__ == "__main__":
	app.run('127.0.0.1',5000,debug = True)
