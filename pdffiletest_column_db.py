# insert file to pdffiletest column in database
from flask import Flask,render_template
import connect_db

app = Flask(__name__)

# connect database 

def get_pdf_path(tokenid):
    try:
        conn = connect_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT pdf_path FROM pdfcatalog WHERE tokenid = %s", (tokenid,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            print(f"PDF Path for token {tokenid}: {result[0]}")  # เอาไว้debug
            return result[0]
        else:
            print(f"No PDF path found for token {tokenid}")  # เอาไว้debug
    except Exception as e:
        print(f"Error pulling PDF path from db: {e}")  # เอาไว้debug
    return None

@app.route('/')
def index():
    return render_template('viewer.html')

