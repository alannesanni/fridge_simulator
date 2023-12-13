import ast
from sqlalchemy.sql import text
from flask import session
from db import db

def add_recipe(name: str, ingredients: list, instructions: str):
    sql = text(
        """INSERT INTO recipes (name, ingredient_ids, instructions)
        VALUES (:name, :ingredient_ids, :instructions)""")
    db.session.execute(sql, {
        "name": name, "ingredient_ids": ingredients, "instructions": instructions})
    db.session.commit()

def check_which_recipes_can_be_made():
    user_id = session["id"]
    sql = text(
        "SELECT selected FROM selected_ingredients WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    ing_ids_str = result.fetchone()[0]
    users_ing_ids = list(ast.literal_eval(ing_ids_str))
    sql = text("SELECT name, ingredient_ids FROM recipes")
    result = db.session.execute(sql)
    recipes = result.fetchall()
    recipes_that_can_be_made = []
    for recipe in recipes:
        recipe_ing_ids = list(ast.literal_eval(recipe[1]))
        if all(ing_id in users_ing_ids for ing_id in recipe_ing_ids):
            recipes_that_can_be_made.append(recipe[0])
    return recipes_that_can_be_made

def get_recipe(recipe_name):
    sql = text("""SELECT ingredients.name, recipes.instructions
              FROM recipes
              JOIN ingredients ON ingredients.id=ANY((CAST(recipes.ingredient_ids AS INTEGER[])))
              WHERE recipes.name = :recipe_name""")
    result = db.session.execute(sql, {"recipe_name": recipe_name})
    recipe = result.fetchall()
    if not recipe:
        return None
    ing_names = [ing[0] for ing in recipe]
    instructions = recipe[0][1]
    return (recipe_name, ing_names, instructions)
