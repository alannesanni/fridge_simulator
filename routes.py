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
    if DatabaseMethods().is_ingredients_empty():
        DatabaseMethods().add_ingredients_to_db()
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    try:
        DatabaseMethods().check_login(username, password)
        session["username"] = username
        return redirect("/home")
    except Exception as error:
            flash(str(error))
            return redirect("/")         
    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

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

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/update")
def mainpage():
    options=DatabaseMethods().get_ingredient_options()
    length=len(options)
    return render_template("update.html", options=options, length=length)

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

    return redirect("/home")

@app.route("/home")
def home():
    username=session["username"]
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()[0]
    sql = text("SELECT selected FROM selected_ingredients WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    selected_str = result.fetchone()[0]
    selected= ast.literal_eval(selected_str)
    ing_names_fridge=[]
    ing_names_pantry=[]
    for i in selected:
        sql = text("SELECT name, place FROM ingredients WHERE id=:id_ing")
        result = db.session.execute(sql, {"id_ing":i})
        ing = result.fetchone()
        print(ing)
        if ing[1]=="fridge":
            ing_names_fridge.append(ing[0])
        if ing[1]=="pantry":
            ing_names_pantry.append(ing[0])


    return render_template("home.html", ing_names_fridge=ing_names_fridge, ing_names_pantry=ing_names_pantry)




