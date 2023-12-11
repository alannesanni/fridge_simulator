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
    if form == "id":
        sql = text("SELECT selected FROM selected_ingredients WHERE id=:user_id")
        result = db.session.execute(sql, {"user_id": user_id})
        selected_str = result.fetchone()[0]
        selected = ast.literal_eval(selected_str)
        return selected
    sql = text("""SELECT ingredients.name, ingredients.place 
              FROM selected_ingredients sel
              JOIN ingredients ON ingredients.id=ANY((CAST(sel.selected AS INTEGER[])))
              WHERE sel.id = :user_id""")
    result = db.session.execute(sql, {"user_id": user_id})
    ing = result.fetchall()
    ing_names_fridge = [name for name, place in ing if place == "fridge"]
    ing_names_pantry = [name for name, place in ing if place == "pantry"]
    return (ing_names_fridge, ing_names_pantry)