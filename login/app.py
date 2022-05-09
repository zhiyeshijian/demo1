from flask import Flask
from flask import request, render_template, redirect, url_for, session, g
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
import pymysql
app=Flask(__name__)
app.config['SECRET_KEY']='sdaw16f54wasd13'

db = pymysql.connect(host="localhost", user="root",password= "rjj020910", db="test")

def qury_data():
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM test.users"
    cursor.execute(sql)
    return cursor.fetchall()

def insert_to_db(username,password):
    sql = f"INSERT INTO test.users (username, password) VALUES ('{username}', '{password}');"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

users=qury_data()

@app.before_request
def before_request():
     g.username=None
     if 'user_id' in session:
          username=[u for u in users if u["id"]==session['user_id']][0]
          g.username=username

@app.route('/signup',methods=['GET','POST'])
def signup():
     if request.method=='POST':
          username=request.form.get('username')
          password=request.form.get('password')
          insert_to_db(username,password)
          return redirect(url_for('profile'))
     return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def signin():
     if request.method=='POST':
          session.pop('username',None)
          username=request.form.get('username',None)
          password=request.form.get('password',None)
          user=[u for u in users if u["username"]==username]
          if len(user)>0:
               user=user[0]
          if user and user["password"]==password:
               session['user_id']=user["id"]
               return redirect(url_for('profile'))
     return render_template('login.html')

@app.route('/profile')
def profile():
     if not g.username:
          return redirect(url_for('signin'))

     return render_template('profile.html')

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for('signin'))

app.debug=True
app.run(debug=True)

# for u in users:
#      print(u["id"])
#      print(u["username"])