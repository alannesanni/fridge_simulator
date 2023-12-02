from sqlalchemy.sql import text
import re
from werkzeug.security import check_password_hash, generate_password_hash
import ast
import json
from db import db
from flask import session

def register(username, password):
    validate(username, password)
    add_user_to_db(username, password, "user")

def validate(username, password):
    if not username or not password:
        raise Exception("Username and password are required")
    if not re.match("^[a-z]+$", username):
        raise Exception("Username can only contain letters a-z")

    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    length = len(result.fetchall())
    if length != 0:
        raise Exception(f"User with username {username} already exists")

    if len(username) < 3:
        raise Exception("Username too short")
    if len(password) < 5:
        raise Exception("Password too short")

    if re.match("^[a-z]+$", password):
        raise Exception("Password can't only contain letters")

def add_user_to_db(username, password, role):
    hash_password = generate_password_hash(password)
    sql = text(
        "INSERT INTO users (username, password, role) VALUES (:username, :password, :role)")
    db.session.execute(
        sql, {"username": username, "password": hash_password, "role": role})
    db.session.commit()
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user_id = result.fetchone()[0]
    sql = text(
        "INSERT INTO selected_ingredients (id, selected) VALUES (:user_id, :empty_list)")
    db.session.execute(sql, {"user_id": user_id, "empty_list": []})
    db.session.commit()

def check_login(username, password):
    if not username or not password:
        raise Exception("Username and password are required")
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        raise Exception("Invalid username or password")

    hash_value = user.password
    if check_password_hash(hash_value, password):
        return user.id
    raise Exception("Invalid username or password")

def login(username, password):
    user_id = check_login(username, password)
    session["id"] = user_id
    role = get_role()
    session["role"] = role

def get_role():
    user_id=session["id"]
    sql = text("SELECT role FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    user_role= result.fetchone()[0]
    return user_role