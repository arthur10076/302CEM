from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dyb2aycx'
app.config['MYSQL_DB'] = 'webstore'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def food():
	return render_template('food.html')

@app.route('/clothes')
def clothes():
	return render_template('clothes.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':

	 # Get Form Fields
	 username = request.form['username']
	 password_candidate = request.form['password']

	 # Create cursor
	 cur = mysql.connection.cursor()

	 # Get user by username
	 result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

	 if result > 0:

	  #Get stored hash 
	  data = cur.fetchone()
	  password = data['password']

	  # Compare Passwords
	  if (password_candidate == password):
 
	   # Passed
	   session['logged_in'] = True
	   session['username'] = username

	   flash('You are now logged in', 'success')
	   return redirect(url_for('food'))

	  else:
	   error = 'Invalid login'
	   return render_template('login.html', error=error)

	  cur.close()

	 else:
	  error = 'User not found'
	  return render_template('login.html', error=error)

	return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
	 if 'logged_in' in session:
	  return f(*args, **kwargs)
	 else:
	  flash('Unauthorized, Please login', 'danger')
	  return redirect(url_for('login'))
	return wrap

# Logout
@app.route('/logout')
def logout():
	 session.clear()
	 flash('You are now logged out', 'success')
	 return redirect(url_for('login'))

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)

