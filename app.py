import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- CONFIGURATION ---
load_dotenv()

# Expect DB config via environment variables. Create a `.env` from
# `.env.example` during development and DO NOT commit `.env` to Git.
# Preferred env var: `SQLALCHEMY_DATABASE_URI` (or `DATABASE_URL`).
db_uri = os.getenv('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URL')
if not db_uri:
    # Fallback to a local sqlite DB for development if no env var set
    db_uri = 'sqlite:///student_db.sqlite'

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ('1', 'true', 'yes')

db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    major = db.Column(db.String(50))

# --- ROUTES ---
@app.route('/')
def index():
    # Fetch all students from MySQL
    all_students = Student.query.all()
    return render_template('index.html', students=all_students)

@app.route('/add', methods=['POST'])
def add_student():
    # Get data from the form
    new_student = Student(
        name=request.form['name'],
        email=request.form['email'],
        major=request.form['major']
    )
    # Save to MySQL
    db.session.add(new_student)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    # This creates the tables in MySQL automatically if they don't exist
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=80, debug=True)