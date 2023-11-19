from os import getenv
from app import app
from flask_sqlalchemy import SQLAlchemy


app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
