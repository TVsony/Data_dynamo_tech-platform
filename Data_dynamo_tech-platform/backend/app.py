from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

# Setup Flask app and database path
app = Flask(__name__, template_folder='templates')
app.secret_key = "your_secret_key"

# Base directory for absolute path to instance folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'courses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# --------------------------- MODELS ---------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)

# --------------------------- ROUTES ---------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    courses = Course.query.all()
    return render_template('dashboard.html', courses=courses)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# --------------------------- INIT DB ---------------------------

with app.app_context():
    db.create_all()
    if Course.query.count() == 0:
        course1 = Course(name="Python for Data Science", description="Basics of Python", video_url="https://example.com/video1", price=999)
        course2 = Course(name="Machine Learning", description="Supervised/Unsupervised ML", video_url="https://example.com/video2", price=1499)
        db.session.add_all([course1, course2])
        db.session.commit()

# --------------------------- RUN APP ---------------------------

if __name__ == "__main__":
    app.run(debug=True)

