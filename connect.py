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

@app.route('/loginAuth', methods=['POST'])
def loginAuth():
    login_type = request.form['login_type']
    username = request.form['username']   # customers + agents use email; staff uses username
    password = request.form['password']

    pwd_bytes = password.encode('utf-8')

    cursor = conn.cursor()

    # Corrected SELECT queries
    if login_type == "customer":
        query = "SELECT email AS username, password FROM customer WHERE email=%s"
    elif login_type == "agent":
        query = "SELECT email AS username, password FROM booking_agent WHERE email=%s"
    elif login_type == "staff":
        query = "SELECT username, password FROM airline_staff WHERE username=%s"
    else:
        return render_template("login.html", error="Invalid login type")

    cursor.execute(query, (username,))
    data = cursor.fetchone()
    cursor.close()

    if not data:
        return render_template("login.html", error="Invalid username")

    stored_hash = data["password"]

    # stored_hash MUST be decoded string
    if isinstance(stored_hash, bytes):
        stored_hash = stored_hash.decode('utf-8')

    # Compare bcrypt hashes
    if bcrypt.checkpw(pwd_bytes, stored_hash.encode('utf-8')):
        session['username'] = data["username"]

        if login_type == "customer":
            return redirect(url_for('cust_dashboard'))
        elif login_type == "agent":
            return redirect(url_for('agent_dashboard'))
        elif login_type == "staff":
            return redirect(url_for('staff_dashboard'))
    else:
        return render_template("login.html", error="Wrong password")
  
@app.route('/registerAuth', methods=['POST'])
def registerAuth():
    register_type = request.form['register_type']
    username = request.form['username']
    password = request.form['password']

    # Hash password correctly
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')  # store as TEXT string

    cursor = conn.cursor()

    # Check if user exists
    if register_type == "customer":
        check_query = "SELECT * FROM customer WHERE email=%s"
    elif register_type == "agent":
        check_query = "SELECT * FROM booking_agent WHERE email=%s"
    elif register_type == "staff":
        check_query = "SELECT * FROM airline_staff WHERE username=%s"
    else:
        return render_template("register.html", error="Invalid registration type")

    cursor.execute(check_query, (username,))
    if cursor.fetchone():
        cursor.close()
        return render_template("register.html", error="User already exists")

    # Insert based on user type
    if register_type == "customer":
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

        ins = """
            INSERT INTO customer
            (email, name, password, building_number, street, city, state,
             phone_number, passport_number, passport_expiration, passport_country, date_of_birth)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(ins, (username, name, hashed, building_number, street, city, state,
                             phone_number, passport_number, passport_expiration, passport_country,
                             date_of_birth))

    elif register_type == "agent":
        ins = """
            INSERT INTO booking_agent (email, password)
            VALUES (%s, %s)
        """
        cursor.execute(ins, (username, hashed))

    elif register_type == "staff":
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
            ins = 'INSERT INTO airline_staff VALUES(%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(ins,(username,password,f_name,l_name,date_of_birth,airline,role))
        
        conn.commit()
        cursor.close()
        
        return redirect(url_for('home'))

@app.route('/flightSearch',methods =['POST'])
def flightSearch():
    search_type = request.form['search_type']
    origin = request.form['origin']
    dest = request.form['dest']
    a_city = request.form['a_city']
    d_city = request.form['d_city']
    dep_date = request.form['dep_date']
    arr_date = request.form['arr_date']
    airline_name = request.form['airline_name']
    flight_num = request.form['flight_num']
    
    cursor = conn.cursor()

    param = []

    if (search_type == "upcoming" or search_type == "purchase"):
        query = "SELECT * FROM flight " \
        "JOIN airport AS dep ON flight.departure_airport = dep.airport_name " \
        "JOIN airport AS arr ON flight.arrival_airport = arr.airport_name " \
        "WHERE status = 'upcoming' "

        if (origin):
            query += " AND departure_airport = %s "
            param.append(origin)
        if (d_city):
            query += " AND dep.city = %s "
            param.append(d_city)
        if (dest):
            query += " AND arrival_airport = %s "
            param.append(dest)
        if (a_city):
            query += " AND arr.city = %s "
            param.append(a_city)
        if (dep_date):
            query += " AND DATE(departure_time) = %s "
            param.append(dep_date)
        if (arr_date):
            query += " AND DATE(arrival_time) = %s "
            param.append(arr_date)

        cursor.execute(query,param)
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

@app.route('/register_success',methods=['GET'])
def register_success():
    return render_template('register_success.html')

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

@app.route('/agent/view_flights', methods=['GET', 'POST'])
def agent_view_flights():
    if 'username' not in session:
        return redirect(url_for('login'))

    agent_email = session['username']
    cursor = conn.cursor()
    flights = []

    if request.method == 'POST':
        origin = request.form['origin']
        dest = request.form['dest']
        start = request.form['start']
        end = request.form['end']

        query = """
        SELECT flight.*
        FROM booking_agent AS ba
        JOIN purchases AS p ON p.booking_agent_email = ba.email
        JOIN ticket AS t ON t.ticket_id = p.ticket_id
        JOIN flight ON flight.flight_num = t.flight_num 
            AND flight.airline_name = t.airline_name
        WHERE ba.email = %s
        AND (%s = '' OR flight.departure_airport = %s)
        AND (%s = '' OR flight.arrival_airport = %s)
        AND (DATE(flight.departure_time) BETWEEN %s AND %s)
        """

        cursor.execute(query, (agent_email, origin, origin, dest, dest, start, end))
        flights = cursor.fetchall()

    cursor.close()
    return render_template('agent_view_flights.html', flights=flights)


@app.route('/agent/search_flights', methods=['GET', 'POST'])
def agent_search_flights():
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = conn.cursor()
    agent_email = session['username']

    # Airlines the agent can sell tickets for
    cursor.execute("SELECT airline_name FROM agent_airline_authorization WHERE agent_email=%s",
                   (agent_email,))
    authorized = [row['airline_name'] for row in cursor.fetchall()]
    flights = []

    if request.method == "POST":
        origin = request.form['origin']
        dest = request.form['dest']

        query = """
        SELECT *
        FROM flight
        WHERE airline_name IN %s
        AND departure_airport=%s
        AND arrival_airport=%s
        """

        cursor.execute(query, (tuple(authorized), origin, dest))
        flights = cursor.fetchall()

    cursor.close()
    return render_template("agent_search_flights.html", flights=flights, authorized=authorized)

@app.route('/agent/purchase_ticket', methods=['GET', 'POST'])
def agent_purchase_ticket():
    if 'username' not in session:
        return redirect(url_for('login'))

    agent_email = session['username']
    cursor = conn.cursor()

    if request.method == 'POST':
        airline = request.form['airline']
        flight_num = request.form['flight_num']
        customer_email = request.form['customer_email']

        # verify authorization
        cursor.execute("""
            SELECT * FROM agent_airline_authorization
            WHERE agent_email=%s AND airline_name=%s
        """, (agent_email, airline))

        if cursor.fetchone() is None:
            return "Not authorized for this airline."

        # check seats sold
        cursor.execute("""
            SELECT COUNT(*) AS sold
            FROM ticket
            WHERE airline_name=%s AND flight_num=%s
        """, (airline, flight_num))
        sold = cursor.fetchone()['sold']

        # get capacity
        cursor.execute("""
            SELECT seat_capacity
            FROM airplane
            WHERE airline_name=%s AND airplane_id=(
                SELECT airplane_id FROM flight
                WHERE airline_name=%s AND flight_num=%s
            )
        """, (airline, airline, flight_num))
        capacity = cursor.fetchone()['seat_capacity']

        if sold >= capacity:
            return "Flight is full."

        # new ticket_id
        cursor.execute("SELECT MAX(ticket_id) AS max FROM ticket")
        next_id = (cursor.fetchone()['max'] or 0) + 1

        cursor.execute("""
            INSERT INTO ticket(ticket_id, airline_name, flight_num)
            VALUES (%s, %s, %s)
        """, (next_id, airline, flight_num))

        cursor.execute("""
            INSERT INTO purchases(ticket_id, customer_email, booking_agent_email, purchase_date)
            VALUES(%s, %s, %s, CURDATE())
        """, (next_id, customer_email, agent_email))

        conn.commit()
        cursor.close()
        return "Ticket purchased."

    return render_template("agent_purchase.html")

#Agent analytics
@app.route('/agent/analytics')
def agent_analytics():
    if 'username' not in session:
        return redirect(url_for('login'))

    agent_email = session['username']
    cursor = conn.cursor()

    # total commission last 30 days
    cursor.execute("""
        SELECT SUM(p.purchase_price * 0.1) AS commission
        FROM purchases p
        WHERE booking_agent_email=%s
        AND p.purchase_date >= CURDATE() - INTERVAL 30 DAY
    """, (agent_email,))
    total_commission = cursor.fetchone()['commission']

    # avg commission
    cursor.execute("""
        SELECT AVG(p.purchase_price * 0.1) AS avg_commission
        FROM purchases p
        WHERE booking_agent_email=%s
        AND p.purchase_date >= CURDATE() - INTERVAL 30 DAY
    """, (agent_email,))
    avg_commission = cursor.fetchone()['avg_commission']

    # tickets sold
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM purchases
        WHERE booking_agent_email=%s
        AND purchase_date >= CURDATE() - INTERVAL 30 DAY
    """, (agent_email,))
    total_tickets = cursor.fetchone()['total']

    # top 5 by tickets
    cursor.execute("""
        SELECT customer_email, COUNT(*) AS tickets
        FROM purchases
        WHERE booking_agent_email=%s
        AND purchase_date >= CURDATE() - INTERVAL 6 MONTH
        GROUP BY customer_email
        ORDER BY tickets DESC
        LIMIT 5
    """, (agent_email,))
    top_tickets = cursor.fetchall()

    # top 5 by commission
    cursor.execute("""
        SELECT customer_email, SUM(purchase_price * 0.1) AS total_commission
        FROM purchases
        WHERE booking_agent_email=%s
        AND purchase_date >= CURDATE() - INTERVAL 1 YEAR
        GROUP BY customer_email
        ORDER BY total_commission DESC
        LIMIT 5
    """, (agent_email,))
    top_commission = cursor.fetchall()

    cursor.close()

    return render_template(
        'agent_analytics.html',
        total_commission=total_commission,
        avg_commission=avg_commission,
        total_tickets=total_tickets,
        top_tickets=top_tickets,
        top_commission=top_commission
    )

#staff routes
@app.route('/staff/view_flights')
def staff_view_flights():
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = conn.cursor()

    cursor.execute("SELECT airline_name FROM airline_staff WHERE username=%s",
                   (session['username'],))
    airline = cursor.fetchone()['airline_name']

    cursor.execute("""
        SELECT *
        FROM flight
        WHERE airline_name=%s
        AND departure_time BETWEEN NOW() AND NOW() + INTERVAL 30 DAY
    """, (airline,))

    flights = cursor.fetchall()
    cursor.close()

    return render_template('staff_view_flights.html', flights=flights)

@app.route('/staff/passengers', methods=['GET', 'POST'])
def staff_passengers():
    if 'username' not in session:
        return redirect(url_for('login'))

    passengers = []
    if request.method == 'POST':
        airline = request.form['airline']
        flight_num = request.form['flight_num']

        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.name, c.email
            FROM ticket t
            JOIN purchases p ON p.ticket_id=t.ticket_id
            JOIN customer c ON c.email=p.customer_email
            WHERE t.airline_name=%s AND t.flight_num=%s
        """, (airline, flight_num))

        passengers = cursor.fetchall()
        cursor.close()

    return render_template('staff_passengers.html', passengers=passengers)

@app.route('/staff/customer_flights', methods=['GET', 'POST'])
def staff_customer_flights():
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM airline_staff WHERE username=%s",
                   (session['username'],))
    airline = cursor.fetchone()['airline_name']
    flights = []

    if request.method == 'POST':
        email = request.form['email']

        cursor.execute("""
            SELECT f.*
            FROM flight f
            JOIN ticket t ON f.flight_num = t.flight_num AND f.airline_name = t.airline_name
            JOIN purchases p ON p.ticket_id = t.ticket_id
            WHERE p.customer_email=%s AND f.airline_name=%s
        """, (email, airline))

        flights = cursor.fetchall()

    cursor.close()
    return render_template('staff_customer_flights.html', flights=flights)

@app.route('/staff/update_status', methods=['POST'])
def staff_update_status():
    if 'username' not in session:
        return redirect(url_for('login'))

    airline = request.form['airline']
    flight_num = request.form['flight_num']
    new_status = request.form['status']

    cursor = conn.cursor()

    # verify staff belongs to airline
    cursor.execute("SELECT airline_name FROM airline_staff WHERE username=%s",
                   (session['username'],))
    staff_airline = cursor.fetchone()['airline_name']

    if staff_airline != airline:
        return "Not authorized."

    cursor.execute("""
        UPDATE flight
        SET status=%s
        WHERE airline_name=%s AND flight_num=%s
    """, (new_status, airline, flight_num))

    conn.commit()
    cursor.close()
    return "Status updated."

#admin routes
def is_admin(username):
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM airline_staff WHERE username=%s", (username,))
    role = cursor.fetchone()
    cursor.close()
    return role and role['role'] in ('admin', 'both')

@app.route('/admin/add_airport', methods=['GET', 'POST'])
def admin_add_airport():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not is_admin(session['username']):
        return "Access denied."

    if request.method == 'POST':
        name = request.form['airport_name']
        city = request.form['airport_city']

        cursor = conn.cursor()
        cursor.execute("INSERT INTO airport VALUES (%s, %s)", (name, city))
        conn.commit()
        cursor.close()
        return "Airport added!"

    return render_template('admin_add_airport.html')

@app.route('/admin/add_airplane', methods=['GET', 'POST'])
def admin_add_airplane():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not is_admin(session['username']):
        return "Access denied."

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM airline_staff WHERE username=%s",
                   (session['username'],))
    airline = cursor.fetchone()['airline_name']

    if request.method == 'POST':
        airplane_id = request.form['airplane_id']
        capacity = request.form['seat_capacity']

        cursor.execute("""
            INSERT INTO airplane (airline_name, airplane_id, seat_capacity)
            VALUES (%s, %s, %s)
        """, (airline, airplane_id, capacity))

        conn.commit()
        cursor.close()
        return "Airplane added!"

    return render_template('admin_add_airplane.html', airline=airline)

@app.route('/admin/create_flight', methods=['GET', 'POST'])
def admin_create_flight():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not is_admin(session['username']):
        return "Access denied."

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM airline_staff WHERE username=%s",
                   (session['username'],))
    airline = cursor.fetchone()['airline_name']

    if request.method == 'POST':
        flight_num = request.form['flight_num']
        dep_airport = request.form['departure_airport']
        dep_time = request.form['departure_time']
        arr_airport = request.form['arrival_airport']
        arr_time = request.form['arrival_time']
        price = request.form['price']
        airplane_id = request.form['airplane_id']

        cursor.execute("""
            INSERT INTO flight
            (airline_name, flight_num, departure_airport, departure_time,
             arrival_airport, arrival_time, base_price, status, airplane_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,'upcoming',%s)
        """, (airline, flight_num, dep_airport, dep_time,
              arr_airport, arr_time, price, airplane_id))

        conn.commit()
        cursor.close()
        return "Flight created!"

    return render_template('admin_create_flight.html', airline=airline)

@app.route('/admin/add_agent_authorization', methods=['GET', 'POST'])
def admin_add_agent_authorization():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not is_admin(session['username']):
        return "Access denied."

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM airline_staff WHERE username=%s",
                   (session['username'],))
    airline = cursor.fetchone()['airline_name']

    if request.method == 'POST':
        agent_email = request.form['agent_email']

        cursor.execute("""
            INSERT INTO agent_airline_authorization (agent_email, airline_name)
            VALUES (%s, %s)
        """, (agent_email, airline))

        conn.commit()
        cursor.close()
        return "Agent authorized!"

    return render_template('admin_add_agent.html', airline=airline)

#anti-automation - seat class
@app.route('/purchase_with_seat_class', methods=['GET', 'POST'])
def purchase_with_seat_class():
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor = conn.cursor()
    buyer = session['username']

    # is agent?
    cursor.execute("SELECT * FROM booking_agent WHERE email=%s", (buyer,))
    is_agent = cursor.fetchone() is not None

    if request.method == 'POST':
        airline = request.form['airline']
        flight_num = request.form['flight_num']
        customer_email = request.form['customer_email']
        seat_class_id = request.form['seat_class_id']

        # get airplane + base price
        cursor.execute("""
            SELECT airplane_id, base_price
            FROM flight
            WHERE airline_name=%s AND flight_num=%s
        """, (airline, flight_num))
        flight = cursor.fetchone()
        airplane_id = flight['airplane_id']
        base_price = flight['base_price']

        # class capacity
        cursor.execute("""
            SELECT seat_capacity
            FROM seat_class
            WHERE airline_name=%s AND airplane_id=%s AND seat_class_id=%s
        """, (airline, airplane_id, seat_class_id))
        seat_data = cursor.fetchone()

        capacity = seat_data['seat_capacity']

        cursor.execute("""
            SELECT COUNT(*) AS sold
            FROM ticket
            WHERE airline_name=%s AND flight_num=%s
              AND airplane_id=%s AND seat_class_id=%s
        """, (airline, flight_num, airplane_id, seat_class_id))
        sold = cursor.fetchone()['sold']

        if sold >= capacity:
            return f"Seat class {seat_class_id} full."

        # new ticket id
        cursor.execute("SELECT MAX(ticket_id) AS max FROM ticket")
        next_id = (cursor.fetchone()['max'] or 0) + 1

        cursor.execute("""
            INSERT INTO ticket(ticket_id, airline_name, flight_num, airplane_id, seat_class_id)
            VALUES(%s,%s,%s,%s,%s)
        """, (next_id, airline, flight_num, airplane_id, seat_class_id))

        # price multiplier
        class_multiplier = {
            "1": 1.0,
            "2": 1.5,
            "3": 2.0,
            "4": 3.0
        }
        final_price = int(base_price * class_multiplier.get(seat_class_id, 1.0))

        cursor.execute("""
            INSERT INTO purchases(ticket_id, customer_email, booking_agent_email, purchase_date, purchase_price)
            VALUES (%s, %s, %s, CURDATE(), %s)
        """, (next_id, customer_email, buyer if is_agent else None, final_price))

        conn.commit()
        cursor.close()
        return f"Purchased seat class {seat_class_id}."

    cursor.execute("SELECT DISTINCT seat_class_id FROM seat_class")
    classes = [c['seat_class_id'] for c in cursor.fetchall()]
    cursor.close()

    return render_template('purchase_with_seat_class.html', classes=classes)



#run app on localhost port 5000
#debug = True means no need to restart flask for changes to go through
if __name__ == "__main__":
	app.run('127.0.0.1',5000,debug = True)

