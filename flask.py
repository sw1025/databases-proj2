#Referenced Flask slides

from flask import Flask, render_template
import pymsql.cursor

app = Flask(__name__)

conn = pymysql.connect(host ='localhost',
			     user = 'root',
			     password = 'root',
			     db = 'meetup',
			     charset = 'rutf8mb4',
			     cursorclass = pymysql.cursors.DictCursor)

@app.route('/loginAuth',methods=['GET','POST']) 

def loginAuth():
	username = request.form['username']
	username = request.form['password']
	
    #Send query to database by calling execute method of cursor
    cursor = conn.cursor

    query = 'SELECT * FROM user WHERE username = %s and password = %s'
    cursor.execute(query,(username,password))

    data = cursor.fetchone()
    cursor.close()
    error = None
    if(data):
        session['username'] = username

        return redirect(url_for('home'))
    else:
        error = 'Invalid username or password'
        return render_template('login.html',error=error)



@app.route('/register')

def register():
    return render_template('register.html')

@app.route('/login')

def login():
	return render_template('login.html')



app.secret_key = 'key that you cant guess'

#run app on localhost port 5000
#debug = True means no need to restart flask for changes to go through
if __name__ == "__main__":
	app.run('127.0.0.1',5000,debug = True)
