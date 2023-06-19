from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from datetime import datetime
from sqlalchemy import select
import plotly.express as px
import pandas as pd
app = Flask(__name__) 
app.config["SECRET_KEY"] = "ieatass69"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(69))
    admin = db.Column(db.Boolean)

    def __init__(self, name, admin):
        self.name = name
        self.admin = admin

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
    # Get the data from the database.
    results = Score.query.all()
    data = [{'Math': d.Math, 'Chemistry': d.Chemistry, 'Physics': d.Physics, 'id': d.student_id} for d in results]
    df = {'Math': [d['Math'] for d in data], 'Chemistry': [d['Chemistry'] for d in data], 'Physics': [d['Physics'] for d in data], 'id': [d['id'] for d in data]} 
    fig = px.bar(df, x='id', y='Math', color='Math', barmode='group')
    # Render the report template with the data and charts.
    return render_template('index.html', plot=fig.to_html(full_html=False))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":   
        user_name = request.form["name"]
        session.permanent = True
        if user_name:
            session["user"] = user_name
            user = User(user_name)
            db.session.add(user)
            db.session.commit()
            print(user_name)
            flash("Logged in successfully, welcome!", "success")
            return redirect(url_for("user"))
    return render_template("login.html")


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
        return redirect('/student')
    return render_template('student/add.html')

@app.route("/student/delete/<id>")
def delete(id):
    data = Student.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/student')

@app.route('/scoreboard')
def scoreboard():
    data = Score.query.order_by(Score.student_id).all()
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
