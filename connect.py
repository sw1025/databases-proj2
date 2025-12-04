#Referenced Flask slides

from flask import Flask, render_template, request, session, url_for, redirect 

import pymysql

app = Flask(__name__)

app.secret_key = 'key that you cant guess'

conn = pymysql.connect(host ='127.0.0.1',
                       user = 'root',
                       password = '',
                       port=3306,
                       db = 'air_reservation',
                       charset = 'utf8mb4',
                       cursorclass = pymysql.cursors.DictCursor)

@app.route('/loginAuth',methods=['POST'])

def loginAuth():

    email = request.form['username']
    password = request.form['password']
	
    print(request.form)
    print(email, password)
    
    #Send query to database by calling execute method of cursor
    cursor = conn.cursor()

    query = 'SELECT * FROM customer WHERE email = %s and password = %s'
    cursor.execute(query,(email,password))

    data = cursor.fetchone()
    cursor.close()
    error = None
    if(data):
        session['username'] = email

        return redirect(url_for('cust_dashboard'))
    else:
        error = 'Invalid username or password'
        return render_template('login.html',error=error)
    
@app.route('/registerAuth',methods=['POST'])
def registerAuth():
    email = request.form['username']
    name = request.form['name']
    password = request.form['password']
    building_number = request.form['buildingnum']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['tel']
    passport_number = request.form['passportid']
    passport_expiration = request.form['passportexp']
    passport_country = request.form['country']
    date_of_birth = request.form['dob']
    
    #Send query to database by calling execute method of cursor
    cursor = conn.cursor()

    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query,(email,))

    data = cursor.fetchone()

    if(data):
        error = 'User already exists'
        cursor.close()
        return render_template('register.html',error=error)
    else:
        ins = 'INSERT INTO customer VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(ins,(email,name,password,building_number,street,city,state,phone_number,passport_number,passport_expiration,passport_country,date_of_birth))
        
        conn.commit()
        cursor.close()
        
        return render_template('index.html')

@app.route('/cust_dashboard')
def cust_dashboard():
    return render_template('cust_dashboard.html')
     

@app.route('/register',methods=['GET'])

def register():
    return render_template('register.html')

@app.route('/login',methods=['GET'])

def login():
    return render_template('login.html')

#run app on localhost port 5000
#debug = True means no need to restart flask for changes to go through
if __name__ == "__main__":
	app.run('127.0.0.1',5000,debug = True)
