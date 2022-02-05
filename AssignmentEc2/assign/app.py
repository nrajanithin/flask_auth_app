from flask import Flask, request, render_template, redirect, session, url_for
import os
import sqlite3
import re
from flask_session import Session

currentlocation = os.path.dirname(os.path.abspath(__file__))

myapplication = Flask(__name__)
myapplication.secret_key = '@dkjgfjgfhkj jxbjljv kjxgvljklkj'

@myapplication.route('/',methods=['GET','POST'])
def homepage():
    message=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        UserName = request.form['username'] 
        Password = request.form['password']
        with sqlite3.connect("database.db") as connect:
            connect.row_factory = sqlite3.Row
            c = connect.cursor()
            c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (UserName, Password, ))
            user = c.fetchone()
            if user: 
                session['loggedin'] = True
                session['username'] = UserName
                return redirect(url_for('profile'))
            else:
                # Account doesnt exist
                message = 'Incorrect username/password!'
    return render_template("homepage.html",message=message)
    

@myapplication.route('/logout')
def logout():
   session.pop('username', None)
   return render_template("homepage.html")


@myapplication.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        f_name=request.form['firstname']
        l_name=request.form['lastname']
        UserName = request.form['username']
        Password = request.form['password']
        email = request.form['email']
        with sqlite3.connect("database.db") as connect:
            c = connect.cursor()
            c.execute('SELECT * FROM users WHERE username = ?', (UserName,))
            user = c.fetchone()
            if user:
                message = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                message = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', UserName):
                message = 'Username must contain only characters and numbers!'
            elif not UserName or not Password or not email:
                message = 'Please fill out the form!'
            else:
                c.execute('INSERT INTO users VALUES (?, ?, ?, ?,?)', (f_name,l_name,email,UserName, Password,))
                connect.commit()
                session['loggedin'] = True
                session['username'] = UserName
                return redirect('profile')
    return render_template("register.html",message=message)
            

@myapplication.route('/profile',methods=['GET','POST'])
def profile():
    if 'loggedin' in session:
        with sqlite3.connect("database.db") as connect:
            connect.row_factory = sqlite3.Row
            c = connect.cursor()
            c.execute('SELECT * FROM users WHERE username = ?', (session['username'],))
            user = c.fetchone()
            return render_template('profile.html',user=user)
    return redirect(url_for(login))

    
    

if __name__=="__main__":
    myapplication.run(debug=True,)
