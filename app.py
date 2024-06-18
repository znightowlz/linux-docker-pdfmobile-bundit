from flask import Flask, send_file, abort, render_template, send_from_directory,request, session, redirect, url_for, flash
import connect_db
import os
import psycopg2
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
from tkinter import *

app = Flask(__name__)
app.secret_key = 'x]kp/yo_1234'
conn = connect_db.connect_db()

def get_pdf_path(tokenid):
    try:
        # conn = connect_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT pdf_path FROM pdfcatalog WHERE tokenid = %s", (tokenid,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            print(f"PDF Path for token {tokenid}: {result[0]}")  # Debug
            return result[0]
        else:
            print(f"No PDF path found for token {tokenid}")  # Debug
    except Exception as e:
        print(f"Error pulling PDF path from db: {e}")  # Debug
    return None

@app.route('/',methods=['GET','POST'])
def login_index():
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'userid' in request.form and 'password_reg' in request.form and 'email' in request.form:
        # Create variables for easy access
        userid = request.form['userid']
        realname = request.form['realname']
        surname = request.form['surname'] 
        email = request.form['email']
        name_occu_ref = request.form['name_occu_ref']
        password_reg = request.form['password_reg']
        _hashed_password = generate_password_hash(password_reg) 
 
        #Check if account exists using Postgresql
        cursor.execute('SELECT * FROM register_record WHERE userid = %s', (userid,)) #Debug
        # print(f"*--Userid is : {userid}")
        account = cursor.fetchone()
        # print(f"*--account is : {account}")
        # If account exists show error and validation checks
        if account:
            flash('This user account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+[A-Za-z]', email):
            flash('Invalid email address!')
        elif not re.match(r'[0-9]+', userid):
            flash('Username must consist of letters and numbers only!')
        elif not userid or not password_reg or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into register_record table
            cursor.execute("INSERT INTO register_record (userid,realname,surname,email, password_reg,name_occu_ref ) VALUES (%s,%s,%s,%s,%s,%s)", (userid,realname,surname,email, _hashed_password,name_occu_ref))
            conn.commit()
            flash('Successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    # return render_template('register.html')
    cursor.execute("SELECT name_occu_ref FROM occu_ref;")  # แก้ไข: ดึงข้อมูลอาชีพ
    occu_ref_pull = cursor.fetchall()  # แก้ไข: ดึงข้อมูลทั้งหมดจากการ query
    cursor.close()
    return render_template('register.html', occu_ref=occu_ref_pull)  # แก้ไข: ส่งข้อมูล occu_refs ไปยัง template

@app.route('/default')
def default_viewer():
    return render_template('viewer.html')

@app.route('/pdf/<tokenid>')
def serve_pdf(tokenid):
    pdf_path = get_pdf_path(tokenid)
    if pdf_path:
        absolute_path = os.path.abspath(pdf_path.replace('/', '\\'))
        print(f"Serving PDF from absolute path: {absolute_path}")  # Debug
        if os.path.exists(absolute_path):
            return send_file(absolute_path)
        else:
            print(f"File does not exist: {absolute_path}")  # Debug
            abort(404)
    else:
        print(f"No PDF path found for token {tokenid}")  # Debug
        abort(404)

@app.route('/view/<tokenid>')
def view_pdf(tokenid):
    return render_template('view_pdf.html', tokenid=tokenid)

@app.route('/web/<path:filename>')
def serve_static(filename):
    return send_from_directory('web', filename)

if __name__ == '__main__':
    app.run(debug=True)