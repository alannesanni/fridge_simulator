from flask import redirect, render_template, request, session, flash
from app import app
import db_methods


@app.route("/")
def index():
    if db_methods.is_users_empty():
        db_methods.add_user_to_db("admin", "admin123", "admin")
        
    if db_methods.is_ingredients_empty():
        db_methods.add_ingredients_to_db()

    if db_methods.is_recipes_empty():
        db_methods.add_recipes_to_db()
    session["role"] = "user"
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    try:
        db_methods.check_login(username, password)
        session["username"] = username
        role = db_methods.get_role(username)
        session["role"] = role
        if session["role"]=="admin":
            return redirect("/admin")
        return redirect("/home")
    except Exception as error:
        flash(str(error))
        return redirect("/")
    
@app.route("/admin")
def admin():
    if session["role"]=="admin":
            options = db_methods.get_ingredient_options()
            length = len(options)
            return render_template("admin.html", options=options, length=length)
    return redirect("/")

@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    name = request.form["name"]
    place = request.form["place"]
    db_methods.add_ingredient(name, place)
    return redirect("/admin")

@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    name = request.form["name"]
    ingredients = request.form.getlist('cb')
    instructions = request.form["instructions"]
    db_methods.add_recipe(name, ingredients, instructions)
    return redirect("/admin")

@app.route("/logout")
def logout():
    del session["username"]
    session["role"]="user"
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
            db_methods.add_user_to_db(username, password, "user")
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
    username = session["username"]
    is_liked = db_methods.check_has_user_liked_recipe(username, recipe_name)
    recipe=db_methods.get_recipe(recipe_name)
    length_ing=len(recipe[1])
    return render_template("recipe.html", recipe_name=recipe[0], recipe_ingredients=recipe[1], recipe_instructions=recipe[2], length_ing=length_ing, is_liked=is_liked)

@app.route('/like_recipe', methods=['POST'])
def like_recipe():
    username = session["username"]
    is_liked = 'heart' in request.form and request.form['heart'] == 'true'
    recipe_name = request.form.get('recipe_name', '')
    if is_liked:
        db_methods.add_like(username, recipe_name)
    else:
        db_methods.delete_like(username, recipe_name)
    return ""