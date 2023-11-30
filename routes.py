from flask import redirect, render_template, request, session, flash
from app import app
from db_methods import DatabaseMethods

db_methods = DatabaseMethods()


@app.route("/")
def index():
    if db_methods.is_ingredients_empty():
        db_methods.add_ingredients_to_db()
    if db_methods.is_recipes_empty():
        db_methods.add_recipes_to_db()
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    try:
        db_methods.check_login(username, password)
        session["username"] = username
        return redirect("/home")
    except Exception as error:
        flash(str(error))
        return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            db_methods.validate(username, password)
            db_methods.add_user_to_db(username, password)
            return redirect("/")

        except Exception as error:
            flash(str(error))
            return redirect("/register")

@app.route("/update")
def mainpage():
    username = session["username"]
    options = db_methods.get_ingredient_options()
    length = len(options)
    selected = db_methods.get_selected_ingredients(username, "id")
    return render_template("update.html", options=options, length=length, selected=selected)

@app.route("/send", methods=["POST"])
def send():
    username = session["username"]
    selected = request.form.getlist('cb')
    db_methods.update_selected_ingredients(username, selected)
    return redirect("/home")

@app.route("/home")
def home():
    username = session["username"]
    selected_ing = db_methods.get_selected_ingredients(username, "name")
    ing_names_fridge = selected_ing[0]
    ing_names_pantry = selected_ing[1]

    recipes = db_methods.check_which_recipes_can_be_made(username)
    if recipes:
        return render_template("home.html", ing_names_fridge=ing_names_fridge, ing_names_pantry=ing_names_pantry, recipes=recipes)

    return render_template("home.html", ing_names_fridge=ing_names_fridge, ing_names_pantry=ing_names_pantry, recipes=["No recipes"])

@app.route("/recipe/<recipe_name>")
def recipe(recipe_name):
    recipe=db_methods.get_recipe(recipe_name)
    return render_template("recipe.html", recipe_name=recipe[0], recipe_ingredients=recipe[1], recipe_instructions=recipe[2])

