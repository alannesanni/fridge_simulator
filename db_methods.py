from sqlalchemy.sql import text
import re
from werkzeug.security import check_password_hash, generate_password_hash
import ast
import json
from db import db
import user_methods
from flask import session

def initialize_db():
    if is_users_empty():
        user_methods.add_user_to_db("admin", "admin123", "admin")
        
    if is_ingredients_empty():
        add_ingredients_to_db()

    if is_recipes_empty():
        add_recipes_to_db()

def is_ingredients_empty():
    sql = text("SELECT name FROM ingredients")
    result = db.session.execute(sql)
    all = result.fetchall()
    if all:
        return False
    return True

def is_recipes_empty():
    sql = text("SELECT name FROM recipes")
    result = db.session.execute(sql)
    all = result.fetchall()
    if all:
        return False
    return True

def is_users_empty():
    sql = text("SELECT username FROM users")
    result = db.session.execute(sql)
    all = result.fetchall()
    if all:
        return False
    return True

def add_ingredients_to_db():
    with open("ingredients.json") as file:
        data = json.load(file)
    data = data["ingredients"]
    for i in data:
        sql = text(
            "INSERT INTO ingredients (name, place) VALUES (:name, :place)")
        db.session.execute(sql, {"name": i["name"], "place": i["place"]})
        db.session.commit()

def add_recipes_to_db():
    with open("recipes.json") as file:
        data = json.load(file)
    data = data["recipes"]
    for i in data:
        try:
            ingredient_ids = []
            for j in i["ingredients"]:
                sql = text("SELECT id FROM ingredients WHERE name=:name")
                result = db.session.execute(sql, {"name": j})
                ing_id = result.fetchone()[0]
                ingredient_ids.append(ing_id)
            sql = text(
                "INSERT INTO recipes (name, ingredient_ids, instructions) VALUES (:name, :ingredient_ids, :instructions)")
            db.session.execute(sql, {
                                "name": i["name"], "ingredient_ids": ingredient_ids, "instructions": i["instructions"]})
            db.session.commit()
        except:
            continue

def add_ingredient(name:str, place:str):
    sql = text(
            "INSERT INTO ingredients (name, place) VALUES (:name, :place)")
    db.session.execute(sql, {"name": name, "place": place})
    db.session.commit()

def add_recipe(name:str, ingredients:list, instructions:str):
    sql = text(
        "INSERT INTO recipes (name, ingredient_ids, instructions) VALUES (:name, :ingredient_ids, :instructions)")
    db.session.execute(sql, {
                        "name": name, "ingredient_ids": ingredients, "instructions": instructions})
    db.session.commit()

def get_ingredient_options():
    sql = text("SELECT name, place FROM ingredients")
    result = db.session.execute(sql)
    all = result.fetchall()
    options = ["x"]
    for i in all:
        options.append(i[0])
    return options

def check_which_recipes_can_be_made():
    user_id=session["id"]
    sql = text(
        "SELECT selected FROM selected_ingredients WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    ing_ids_str = result.fetchone()[0]
    users_ing_ids = list(ast.literal_eval(ing_ids_str))
    sql = text("SELECT name, ingredient_ids FROM recipes")
    result = db.session.execute(sql)
    recipes = result.fetchall()
    recipes_that_can_be_made = []
    for i in recipes:
        recipe_ing_ids = list(ast.literal_eval(i[1]))
        if all(ing_id in users_ing_ids for ing_id in recipe_ing_ids):
            recipes_that_can_be_made.append(i[0])
    return recipes_that_can_be_made

def update_selected_ingredients(selected):
    user_id=session["id"]
    sql = text(
        "UPDATE selected_ingredients SET selected =:selected WHERE id=:user_id")
    db.session.execute(sql, {"selected": selected, "user_id": user_id})
    db.session.commit()

def get_selected_ingredients(form):
    user_id=session["id"]
    sql = text("SELECT selected FROM selected_ingredients WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    selected_str = result.fetchone()[0]
    selected = ast.literal_eval(selected_str)
    if form == "id":
        return selected
    ing_names_fridge = []
    ing_names_pantry = []
    for i in selected:
        sql = text("SELECT name, place FROM ingredients WHERE id=:id_ing")
        result = db.session.execute(sql, {"id_ing": i})
        ing = result.fetchone()
        if ing[1] == "fridge":
            ing_names_fridge.append(ing[0])
        if ing[1] == "pantry":
            ing_names_pantry.append(ing[0])
    return (ing_names_fridge, ing_names_pantry)

def get_recipe(recipe_name):
    sql = text("SELECT name, ingredient_ids, instructions FROM recipes WHERE name =:recipe_name")
    result = db.session.execute(sql, {"recipe_name": recipe_name})
    recipe = result.fetchone()
    ingredients_id = list(ast.literal_eval(recipe[1]))
    ing_names=[]
    for i in  ingredients_id:
        sql = text("SELECT name FROM ingredients WHERE id=:ing_id")
        result = db.session.execute(sql, {"ing_id": i})
        ing = result.fetchone()[0]
        ing_names.append(ing)
    return (recipe[0], ing_names, recipe[2])


def add_like(recipe_name):
    user_id=session["id"]
    sql = text("SELECT id FROM recipes WHERE name=:name")
    result = db.session.execute(sql, {"name": recipe_name})
    recipe_id = result.fetchone()[0]
    sql = text(
        "INSERT INTO liked_recipes (user_id, recipe_id) VALUES (:user_id, :recipe_id)")
    db.session.execute(
        sql, {"user_id": user_id, "recipe_id": recipe_id})
    db.session.commit()

def delete_like(recipe_name):
    user_id=session["id"]
    sql = text("SELECT id FROM recipes WHERE name=:name")
    result = db.session.execute(sql, {"name": recipe_name})
    recipe_id = result.fetchone()[0]
    sql = text(
        "DELETE FROM liked_recipes WHERE user_id=:user_id AND recipe_id=:recipe_id")
    db.session.execute(
        sql, {"user_id": user_id, "recipe_id": recipe_id})
    db.session.commit()

def check_has_user_liked_recipe(recipe_name):
    user_id=session["id"]
    sql = text("SELECT id FROM recipes WHERE name=:name")
    result = db.session.execute(sql, {"name": recipe_name})
    recipe_id = result.fetchone()[0]
    sql = text("SELECT id FROM liked_recipes WHERE user_id=:user_id AND recipe_id=:recipe_id")
    result = db.session.execute(sql, {"user_id": user_id, "recipe_id": recipe_id})
    res = result.fetchone()
    if res:
        return True
    else:
        return False

