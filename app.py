from flask import Flask, send_file, abort, render_template, send_from_directory,request, session, redirect, url_for, flash
import connect_db
import os
import psycopg2
import psycopg2.extras
import re
from werkzeug.security import generate_password_hash, check_password_hash
from tkinter import *

app = Flask(__name__)

def get_pdf_path(tokenid):
    try:
        conn = connect_db.connect_db()
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

@app.route('/')
def login_index():
    return render_template('login.html')

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