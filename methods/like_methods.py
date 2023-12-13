from sqlalchemy.sql import text
from flask import session
from db import db

def add_like(recipe_name):
    user_id = session["id"]
    sql = text("SELECT id FROM recipes WHERE name=:name")
    result = db.session.execute(sql, {"name": recipe_name})
    recipe_id = result.fetchone()[0]
    sql = text(
        "INSERT INTO liked_recipes (user_id, recipe_id) VALUES (:user_id, :recipe_id)")
    db.session.execute(
        sql, {"user_id": user_id, "recipe_id": recipe_id})
    db.session.commit()


def delete_like(recipe_name):
    user_id = session["id"]
    sql = text("SELECT id FROM recipes WHERE name=:name")
    result = db.session.execute(sql, {"name": recipe_name})
    recipe_id = result.fetchone()[0]
    sql = text(
        "DELETE FROM liked_recipes WHERE user_id=:user_id AND recipe_id=:recipe_id")
    db.session.execute(
        sql, {"user_id": user_id, "recipe_id": recipe_id})
    db.session.commit()


def check_has_user_liked_recipe(recipe_name):
    user_id = session["id"]
    sql = text("SELECT id FROM recipes WHERE name=:name")
    result = db.session.execute(sql, {"name": recipe_name})
    recipe_id = result.fetchone()[0]
    sql = text(
        "SELECT id FROM liked_recipes WHERE user_id=:user_id AND recipe_id=:recipe_id")
    result = db.session.execute(
        sql, {"user_id": user_id, "recipe_id": recipe_id})
    res = result.fetchone()
    if res:
        return True
    return False

def get_liked_recipes():
    user_id = session["id"]
    sql = text("""SELECT name FROM recipes WHERE id IN
                (SELECT recipe_id FROM liked_recipes WHERE user_id=:user_id)""")
    result = db.session.execute(sql, {"user_id": user_id})
    recipe_tuples = result.fetchall()
    if not recipe_tuples:
        return None
    recipe_names=[]
    for recipe in recipe_tuples:
        recipe_names.append(recipe[0])
    return recipe_names

def user_liked_recipes_count():
    user_id = session["id"]
    sql = text("""SELECT COUNT(name) FROM recipes WHERE id IN
               (SELECT recipe_id FROM liked_recipes WHERE user_id=:user_id)""")
    result = db.session.execute(sql, {"user_id": user_id})
    liked_count = result.fetchone()[0]
    return liked_count

def recipe_likes(recipe_name):
    sql = text("""SELECT COUNT(user_id) FROM liked_recipes WHERE recipe_id IN
               (SELECT id FROM recipes WHERE name=:recipe_name)""")
    result = db.session.execute(sql, {"recipe_name": recipe_name})
    recipe_likes_count = result.fetchone()[0]
    return recipe_likes_count
