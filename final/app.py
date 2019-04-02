from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dyb2aycx'
app.config['MYSQL_DB'] = 'webstore'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def food():

	cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM products where category='Food'")

        product = cur.fetchall()

        if result > 0:
         return render_template('food.html', product=product)
        else:
         msg= 'No Product Found'
         return render_template('food.html', msg=msg)

        cur.close()

@app.route('/clothes')
def clothes():

	cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM products where category='Clothes'")

        product = cur.fetchall()

        if result > 0:
         return render_template('clothes.html', product=product)
        else:
         msg= 'No Product Found'
         return render_template('clothes.html', msg=msg)

        cur.close()



@app.route('/product/<string:id>/')
def product(id):

	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM products WHERE id = %s" ,[id])

	product1 = cur.fetchone()

	result = cur.execute("SELECT name FROM products WHERE id = %s" ,[id])

	pname = cur.fetchone()

	session['pname']=pname

	result = cur.execute("SELECT prices FROM products WHERE id = %s" ,[id])

	pprices = cur.fetchone()

	session['pprices']=pprices

	

        return render_template('product.html', product1=product1, pname=pname, pprices=pprices)
	
	cur.close()




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


@app.route('/productadd/<string:id>/', methods=['GET', 'POST'])
@is_logged_in
def productadd(id):
	
	if request.method == 'POST':

	 	pname = request.form['pname']
		number = request.form['number']
	 	pprices = request.form['pprices']
		n= int(str(number))
		p= int(str(pprices))
		global tp
		tp=n*p

		cur = mysql.connection.cursor()
	 	cur.execute("INSERT INTO cart(pname, quantity, prices, username) VALUES(%s, %s, %s, %s)",(pname, number, tp, session['username']))

		mysql.connection.commit()
		

		return redirect(url_for('food'))

	return render_template('add.html')

@app.route('/shoppingcart', methods=['GET', 'POST'])
@is_logged_in
def shoppingcart():


	if request.method == 'POST':
		username=session['username']
		cur2 = mysql.connection.cursor()
		cur2.execute("SELECT * FROM users where username = %s", [username])
		data = cur2.fetchone()
		reemail=data['email']
		readdress=data['address']
		recontact=data['contact']

		cur1 = mysql.connection.cursor()
		cur1.execute("DELETE FROM cart WHERE username = %s", [username])
		mysql.connection.commit()
		cur1.close()
		
		cur = mysql.connection.cursor()
		stmt = "INSERT INTO orders(pname, quantity, username, reemail, readdress, recontact) VALUES(%s, %s, %s, %s, %s, %s)"
		pname = request.form.getlist('pname')
		number = request.form.getlist('number')

		for i,pname in enumerate(pname):
		 rec = [ (pname, number[i], session['username'], reemail, readdress, recontact) ]
		 

		 cur.executemany(stmt, rec)
		 mysql.connection.commit()
		 
	 	return render_template('shoppingcart.html')


	else:
	  username=session['username']

	  cur = mysql.connection.cursor()

          result = cur.execute("SELECT * FROM cart where username = %s", [username])

          shoppingcart = cur.fetchall()

	  if result > 0:
           return render_template('shoppingcart.html', shoppingcart=shoppingcart)
          else:
           msg= 'No item Found'
           return render_template('shoppingcart.html', msg=msg)
         

@app.route('/delete_item/<string:id>', methods=['POST'])
@is_logged_in
def delete_item(id):

	cur = mysql.connection.cursor()

	cur.execute("DELETE FROM cart WHERE id = %s", [id])

	mysql.connection.commit()

	cur.close()

	flash('Item Deleted', 'success')

	return redirect(url_for('shoppingcart'))

@app.route('/order')
@is_logged_in
def order():

	cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM orders ")

        order = cur.fetchall()

	if result > 0:
         return render_template('order.html', order=order)
        else:
         msg= 'No item Found'
         return render_template('order.html', msg=msg)

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)

