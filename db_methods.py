from db import db
from sqlalchemy.sql import text
import re
from werkzeug.security import check_password_hash, generate_password_hash
import ast
import json



class DatabaseMethods:
    def __init__(self):
        pass

    def add_ingredients_to_db(self):
        with open("ingredients.json") as f:
            data=json.load(f)
        data=data["ingredients"]
        for i in data:
            sql = text("INSERT INTO ingredients (name, place) VALUES (:name, :place)")
            db.session.execute(sql, {"name":i["name"], "place":i["place"]})
            db.session.commit()

    def add_recipes_to_db(self):
        with open("recipes.json") as a:
            data=json.load(a)
        data=data["recipes"]
        for i in data:
            try:
                ingredient_ids=[]
                for j in i["ingredients"]:
                    print(j)
                    sql = text("SELECT id FROM ingredients WHERE name=:name")
                    result = db.session.execute(sql, {"name":j})
                    ing_id = result.fetchone()[0]
                    ingredient_ids.append(ing_id)
                sql = text("INSERT INTO recipes (name, ingredient_ids, instructions) VALUES (:name, :ingredient_ids, :instructions)")
                db.session.execute(sql, {"name":i["name"], "ingredient_ids":ingredient_ids, "instructions":i["instructions"]})
                db.session.commit()
            except:
                continue
        

    def validate(self, username, password):
        if not username or not password:
            raise Exception("Username and password are required")
        if not re.match("^[a-z]+$", username):
                raise Exception("Username can only contain letters a-z")

        sql = text("SELECT * FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        length = len(result.fetchall())
        if length!=0:
            raise Exception(f"User with username {username} already exists")
        
        if len(username)<3:
            raise Exception("Username too short")
        if len(password)<5:
                raise Exception("Password too short")

        if re.match("^[a-z]+$", password):
             raise Exception("Password can't only contain letters")

    def check_login(self, username, password):
        if not username or not password:
            raise Exception("Username and password are required")
        sql = text("SELECT id, password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()    
        if not user:
            raise Exception("Invalid username or password")
            
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                return         
            else:
                raise Exception("Invalid username or password")
            
    def get_ingredient_options(self):
        sql = text("SELECT name, place FROM ingredients")
        result = db.session.execute(sql)
        all = result.fetchall()
        options=["x"]
        for i in all:
            options.append(i[0])
        return options


        #options_fridge=["x"]
        #options_pantry=["x"]
        #for i in all:
        #    if i[1]=="fridge":
        #        options_fridge.append(i[0])
        #    if i[1]=="pantry":
        #        options_pantry.append(i[0])
        #return (options_fridge, options_pantry)
    
    def is_ingredients_empty(self):
        sql = text("SELECT * FROM ingredients")
        result = db.session.execute(sql)
        all = result.fetchall()
        if all:
            return False
        return True

    def is_recipes_empty(self):
        sql = text("SELECT * FROM recipes")
        result = db.session.execute(sql)
        all = result.fetchall()
        if all:
            return False
        return True
    
    def check_which_recipes_can_be_made(self, username):
        sql = text("SELECT selected FROM selected_ingredients WHERE id=(SELECT id FROM users WHERE username=:username)")
        result = db.session.execute(sql, {"username":username})
        ing_ids_str = result.fetchone()[0]
        users_ing_ids=list(ast.literal_eval(ing_ids_str))    

        sql = text("SELECT name, ingredient_ids FROM recipes")
        result = db.session.execute(sql)
        recipes = result.fetchall()
        recipes_that_can_be_made=[]
        for i in recipes:
            recipe_ing_ids=list(ast.literal_eval(i[1]))
            if all(id in users_ing_ids for id in recipe_ing_ids):
                recipes_that_can_be_made.append(i[0])

        return recipes_that_can_be_made
        


        
        


        



        
    
