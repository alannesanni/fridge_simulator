from flask import redirect, render_template, request, session, flash
from app import app
import methods.initialize_db as initialize_db
import methods.user_methods as user_methods

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
    return render_template("register.html")
