import json
from sqlalchemy.sql import text
from db import db
import methods.user_methods as user_methods
import methods.ing_methods as ing_methods 
import methods.recipe_methods as recipe_methods

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
    for ing in data:
        ing_methods.add_ingredient(ing["name"], ing["place"])


def add_recipes_to_db():
    with open("recipes.json") as file:
        data = json.load(file)
    data = data["recipes"]
    for recipe in data:
        try:
            ing_ids = []
            for ing in recipe["ingredients"]:
                sql = text("SELECT id FROM ingredients WHERE name=:name")
                result = db.session.execute(sql, {"name": ing})
                ing_id = result.fetchone()[0]
                ing_ids.append(ing_id)
            recipe_methods.add_recipe(recipe["name"], ing_ids, recipe["instructions"])
        except:
            continue