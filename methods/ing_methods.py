import ast
from sqlalchemy.sql import text
from flask import session
from db import db

def add_ingredient(name: str, place: str):
    sql = text("INSERT INTO ingredients (name, place) VALUES (:name, :place)")
    db.session.execute(sql, {"name": name, "place": place})
    db.session.commit()

def get_ingredient_options():
    sql = text("SELECT name, place FROM ingredients")
    result = db.session.execute(sql)
    all = result.fetchall()
    options = ["x"]
    for ing in all:
        options.append(ing[0])
    return options

def update_selected_ingredients(selected):
    user_id = session["id"]
    sql = text(
        "UPDATE selected_ingredients SET selected =:selected WHERE id=:user_id")
    db.session.execute(sql, {"selected": selected, "user_id": user_id})
    db.session.commit()

def get_selected_ingredients(form):
    user_id = session["id"]
    sql = text("SELECT selected FROM selected_ingredients WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    selected_str = result.fetchone()[0]
    selected = ast.literal_eval(selected_str)
    if form == "id":
        return selected
    ing_names_fridge = []
    ing_names_pantry = []
    for ing_id in selected:
        sql = text("SELECT name, place FROM ingredients WHERE id=:id_ing")
        result = db.session.execute(sql, {"id_ing": ing_id})
        ing = result.fetchone()
        if ing[1] == "fridge":
            ing_names_fridge.append(ing[0])
        if ing[1] == "pantry":
            ing_names_pantry.append(ing[0])
    return (ing_names_fridge, ing_names_pantry)