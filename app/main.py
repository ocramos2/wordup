from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2

DATABASE_URL = "postgres://louaeunlzgjquy:c8a7bec02e60dca0d8493dcb1ddfe2b450cd67053fa83727a36829f4c84a7088@ec2-52-54-237-144.compute-1.amazonaws.com:5432/dc0ft4arkacrbg"
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
conn.autocommit = True
cur = conn.cursor()

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def login():
    error = None
    if request.method == 'POST':
        username = str(request.form.get('username')).strip()
        password = str(request.form.get('password')).strip()
        # Retrieving data
        cur.execute("SELECT * from users WHERE username = %s AND password = %s", (username, password))
        results = cur.fetchone()
        db_user = results[1].strip()
        db_pass = results[4].strip()
        if password != db_pass or username != db_user:
            error = 'Invalid username and password, please try again'
        else:
            return redirect(url_for('index', user=db_user))
    return render_template('login.html', error=error)

@app.route('/index')
def index():
    username = request.args['user']
    user_info = {
        'name': username
    }
    return render_template('index.html', user=user_info)

@app.route('/signup', methods=["POST", "GET"])
def signup():
    user_error = None
    password_error = None
    success = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        if len(username) < 5:
            user_error = 'Username must be at least 5 characters long'
        if len(password) < 3:
            password_error = 'Password must be at least 3 characters long'
        if not user_error and not password_error:
            cur.execute("INSERT INTO users VALUES (DEFAULT, %s, %s, %s, %s)", (username, firstname, lastname, password))
            success = 'Account successfully created! Please click the logo to return to the login page'
    return render_template('signup.html', user_error=user_error, password_error=password_error, success=success)

if __name__ == '__main__':
    app.run(debug=True)