from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from datetime import datetime
app = Flask(__name__) 
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "ieatass69"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(69))
    birthdate = db.Column(db.Date)
    gender = db.Column(db.String(10))
    pnumber = db.Column(db.Integer)
    classnum = db.Column(db.String(50))

    def __init__(self, name, birthdate, gender, pnumber, classnum):
        self.name = name
        self.birthdate = birthdate
        self.gender = gender
        self.pnumber = pnumber
        self.classnum = classnum


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Math = db.Column(db.Integer)
    Physics = db.Column(db.Integer)
    Chemistry = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __init__(self, Math, Physics, Chemistry, student_id):
        self.Math = Math
        self.Physics = Physics
        self.Chemistry = Chemistry
        self.student_id = student_id

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/student')
def student():
    data = Student.query.all()
    return render_template('/student/student_list.html', students=data)

@app.route('/student/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        birthdatestr = request.form['birthdate']
        birthdate = datetime.strptime(birthdatestr, '%Y-%m-%d').date()
        gender = request.form['gender']
        pnumber = request.form['pnumber']
        classnum = request.form['classnum']
        student = Student(name, birthdate, gender, pnumber, classnum)
        db.session.add(student)
        db.session.commit()
    return render_template('/student/add.html')

@app.route('/scoreboard')
def scoreboard():
    data = Score.query.all()
    return render_template('scoreboard.html', scores=data)

@app.route('/scoreboard/add', methods=['POST', 'GET'])
def add_score():
    if request.method == 'POST':
        Math = request.form['Math']
        Physics = request.form['Physics']
        Chemistry = request.form['Chemistry']
        student_id = request.form['student_id']
        score = Score(Math, Physics, Chemistry, student_id)
        db.session.add(score)
        db.session.commit()
    return render_template('add_score.html')

if __name__ == '__main__':
    if not path.exists("user.db"):
        db.create_all(app = app)
        print("Database created.")
    app.run(debug=True)
