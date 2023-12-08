from flask import redirect, render_template, request, session, flash
from app import app
import methods.initialize_db as initialize_db
import methods.user_methods as user_methods
import methods.like_methods as like_methods
import methods.ing_methods as ing_methods
import methods.recipe_methods as recipe_methods

@app.route("/")
def index():
    initialize_db.initialize_db()
    session["role"] = "user"
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    try:
        user_methods.login(username, password)
        if "login_data" in session:
            del session["login_data"]
        if session["role"] == "admin":
            return redirect("/admin")
        return redirect("/home")
    except ValueError as error:
        flash(str(error))
        session["login_data"] = {"username": username, "password": password}
        return redirect("/")


@app.route("/logout")
def logout():
    del session["id"]
    if "login_data" in session:
        del session["login_data"]
    if "register_data" in session:
        del session["register_data"]
    session["role"] = "user"
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            user_methods.register(username, password)
            user_methods.login(username, password)
            if "register_data" in session:
                del session["register_data"]
            return redirect("/home")

        except ValueError as error:
            session["register_data"] = {
                "username": username, "password": password}
            flash(str(error))
            return redirect("/register")


@app.route("/admin")
def admin():
    if session["role"] == "admin":
        options = ing_methods.get_ingredient_options()
        length = len(options)
        return render_template("admin.html", options=options, length=length)
    return render_template("error.html", error_message="You don't have access to this page.")



@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html")
    name = request.form["name"]
    place = request.form["place"]
    ing_methods.add_ingredient(name, place)
    return redirect("/admin")


@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html")
    name = request.form["name"]
    ingredients = request.form.getlist('cb')
    instructions = request.form["instructions"]
    recipe_methods.add_recipe(name, ingredients, instructions)
    return redirect("/admin")


@app.route("/home")
def home():
    if "id" not in session:
        return render_template("error.html", error_message="You need to be logged in to access this page.")
    selected_ing = ing_methods.get_selected_ingredients("name")
    ing_names_fridge = selected_ing[0]
    ing_names_pantry = selected_ing[1]
    recipes = recipe_methods.check_which_recipes_can_be_made()
    liked_rec=like_methods.get_liked_recipes()
    if recipes:
        return render_template("home.html", ing_names_fridge=ing_names_fridge, ing_names_pantry=ing_names_pantry, recipes=recipes, liked_rec=liked_rec)
    return render_template("home.html", ing_names_fridge=ing_names_fridge, ing_names_pantry=ing_names_pantry, recipes=None, liked_rec=liked_rec)


@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "GET":
        if "id" not in session:
            return render_template("error.html", error_message="You need to be logged in to access this page.")
        options = ing_methods.get_ingredient_options()
        length = len(options)
        selected = ing_methods.get_selected_ingredients("id")
        return render_template("update.html", options=options, length=length, selected=selected)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            return render_template("error.html")
        selected = request.form.getlist('cb')
        ing_methods.update_selected_ingredients(selected)
        return redirect("/home")


@app.route("/recipe/<recipe_name>")
def recipe(recipe_name):
    if "id" not in session:
        return render_template("error.html", error_message="You need to be logged in to access this page.")
    recipe_tuple = recipe_methods.get_recipe(recipe_name)
    if not recipe_tuple: 
        return render_template("error.html", error_message="We don't have this recipe.")
    is_liked = like_methods.check_has_user_liked_recipe(recipe_name)
    length_ing = len(recipe_tuple[1])
    return render_template("recipe.html", recipe_name=recipe_tuple[0],
                           recipe_ingredients=recipe_tuple[1], recipe_instructions=recipe_tuple[2], length_ing=length_ing, is_liked=is_liked)


@app.route("/like_recipe", methods=["POST"])
def like_recipe():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html")
    is_liked = "heart" in request.form and request.form["heart"] == "true"
    recipe_name = request.form.get("recipe_name", "")
    if is_liked:
        like_methods.add_like(recipe_name)
    else:
        like_methods.delete_like(recipe_name)
    return ""
