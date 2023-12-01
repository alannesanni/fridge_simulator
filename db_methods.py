from sqlalchemy.sql import text
import re
from werkzeug.security import check_password_hash, generate_password_hash
import ast
import json
from db import db


class DatabaseMethods:
    def __init__(self):
        pass

    def add_ingredients_to_db(self):
        with open("ingredients.json") as file:
            data = json.load(file)
        data = data["ingredients"]
        for i in data:
            sql = text(
                "INSERT INTO ingredients (name, place) VALUES (:name, :place)")
            db.session.execute(sql, {"name": i["name"], "place": i["place"]})
            db.session.commit()

    def add_recipes_to_db(self):
        with open("recipes.json") as file:
            data = json.load(file)
        data = data["recipes"]
        for i in data:
            try:
                ingredient_ids = []
                for j in i["ingredients"]:
                    print(j)
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

    def add_ingredient(self, name:str, place:str):
        sql = text(
                "INSERT INTO ingredients (name, place) VALUES (:name, :place)")
        db.session.execute(sql, {"name": name, "place": place})
        db.session.commit()

    def add_recipe(self, name:str, ingredients:list, instructions:str):
        sql = text(
            "INSERT INTO recipes (name, ingredient_ids, instructions) VALUES (:name, :ingredient_ids, :instructions)")
        db.session.execute(sql, {
                            "name": name, "ingredient_ids": ingredients, "instructions": instructions})
        db.session.commit()



    def validate(self, username, password):
        if not username or not password:
            raise Exception("Username and password are required")
        if not re.match("^[a-z]+$", username):
            raise Exception("Username can only contain letters a-z")

        sql = text("SELECT * FROM users WHERE username=:username")
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

    def check_login(self, username, password):
        if not username or not password:
            raise Exception("Username and password are required")
        sql = text("SELECT id, password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        user = result.fetchone()
        if not user:
            raise Exception("Invalid username or password")

        hash_value = user.password
        if check_password_hash(hash_value, password):
            return
        raise Exception("Invalid username or password")

    def get_ingredient_options(self):
        sql = text("SELECT name, place FROM ingredients")
        result = db.session.execute(sql)
        all = result.fetchall()
        options = ["x"]
        for i in all:
            options.append(i[0])
        return options

    def is_ingredients_empty(self):
        sql = text("SELECT name FROM ingredients")
        result = db.session.execute(sql)
        all = result.fetchall()
        if all:
            return False
        return True

    def is_recipes_empty(self):
        sql = text("SELECT name FROM recipes")
        result = db.session.execute(sql)
        all = result.fetchall()
        if all:
            return False
        return True

    def is_users_empty(self):
        sql = text("SELECT username FROM users")
        result = db.session.execute(sql)
        all = result.fetchall()
        if all:
            return False
        return True
    
    def check_which_recipes_can_be_made(self, username):
        sql = text(
            "SELECT selected FROM selected_ingredients WHERE id=(SELECT id FROM users WHERE username=:username)")
        result = db.session.execute(sql, {"username": username})
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

    def add_user_to_db(self, username, password, role):
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

    def update_selected_ingredients(self, username, selected):
        sql = text("SELECT id FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        user_id = result.fetchone()[0]
        sql = text(
            "UPDATE selected_ingredients SET selected =:selected WHERE id =:user_id")
        db.session.execute(sql, {"selected": selected, "user_id": user_id})
        db.session.commit()

    def get_selected_ingredients(self, username, form):
        sql = text("SELECT id FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        user_id = result.fetchone()[0]
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
            print(ing)
            if ing[1] == "fridge":
                ing_names_fridge.append(ing[0])
            if ing[1] == "pantry":
                ing_names_pantry.append(ing[0])
        return (ing_names_fridge, ing_names_pantry)
    
    def get_recipe(self, recipe_name):
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
    

    def get_role(self, username):
        sql = text("SELECT role FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        user_role= result.fetchone()[0]
        return user_role




