from app import app
from flask import Flask
from flask import redirect, render_template, request, session, flash
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import ast
from db_methods import DatabaseMethods

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    try:
        DatabaseMethods().check_login(username, password)
        session["username"] = username
        return redirect("/mainpage")
    except Exception as error:
            flash(str(error))
            return redirect("/")         
    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/mainpage")
def mainpage():
    #sql = "SELECT ingredient FROM ingredients"
    #result = db.session.execute(sql)
    #ing_list = result.fetchall()

    choices = ["milk", "eggs"]
    return render_template("mainpage.html", choices=choices)

@app.route("/send", methods=["POST"])
def send():
    username=session["username"]
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()[0]
    selected=request.form.getlist('cb')
    sql = text("UPDATE selected_ingredients SET selected =:selected WHERE id =:user_id")
    db.session.execute(sql, {"selected":selected, "user_id":user_id})
    db.session.commit()

    return redirect("/selections")

@app.route("/selections")
def choices():
    username=session["username"]
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()[0]
    sql = text("SELECT selected FROM selected_ingredients WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    selected_str = result.fetchone()[0]
    selected= ast.literal_eval(selected_str)
    print(selected)
    ing_names=[]
    for i in selected:
        sql = text("SELECT name FROM ingredients WHERE id=:id_ing")
        result = db.session.execute(sql, {"id_ing":i})
        ing_name = result.fetchone()[0]
        ing_names.append(ing_name)
    print(ing_names)

    return render_template("choices.html", ing_names=ing_names)



@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            DatabaseMethods().validate(username, password)
            hash_password=generate_password_hash(password)
            sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(sql, {"username":username, "password":hash_password})
            db.session.commit()
            sql = text("SELECT id FROM users WHERE username=:username")
            result = db.session.execute(sql, {"username":username})
            user_id = result.fetchone()[0]
            sql = text("INSERT INTO selected_ingredients (id, selected) VALUES (:user_id, :empty_list)")
            db.session.execute(sql, {"user_id":user_id, "empty_list":[]})
            db.session.commit()
            return redirect("/")
        except Exception as error:
            flash(str(error))
            return redirect("/register")
