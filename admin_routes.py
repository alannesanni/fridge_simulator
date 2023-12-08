from flask import redirect, render_template, request, session
from app import app
import methods.ing_methods as ing_methods
import methods.recipe_methods as recipe_methods

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