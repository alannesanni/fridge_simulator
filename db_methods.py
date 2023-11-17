from db import db
from sqlalchemy.sql import text
import re
from werkzeug.security import check_password_hash, generate_password_hash

class DatabaseMethods:
    def __init__(self):
        pass
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
        sql = text("SELECT name FROM ingredients")
        result = db.session.execute(sql)
        all = result.fetchall()
        options=["x"]
        for i in all:
             options.append(i[0])
        return options