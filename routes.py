from app import app
from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        return redirect("/")
        
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/fridge")           
        else:
            return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/fridge")
def fridge():
    #sql = "SELECT ingredient FROM ingredients"
    #result = db.session.execute(sql)
    #ing_list = result.fetchall()

    choices = ["milk", "eggs"]
    return render_template("fridge.html", choices=choices)

@app.route("/send", methods=["POST"])
def send():
    if "send" in request.form:
        send_id = request.form["send"]
        sql = "INSERT INTO selections (send_id) VALUES (:send_id)"
        db.session.execute(sql, {"send_id":send_id})
        db.session.commit()
    return redirect("/choices")

@app.route("/choices")
def choice():
    #sql = "SELECT ingredient FROM selections"
    #result = db.session.execute(sql, {"ingredient":ingredient})
    #choices = result.fetchall()

    return render_template("choices.html")



@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_password=generate_password_hash(password)
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_password})
        db.session.commit()
        return redirect("/")
