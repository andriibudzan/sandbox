# author: andrii budzan
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "very_secret_key"
app.permanent_session_lifetime = timedelta(minutes=3)


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/")
def f_red():
    return redirect(url_for("home"))


@app.route("/items")
def items():
    return render_template("items.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = False
        user = request.form.get("nm", "user")
        session["user"] = user
        flash(f"{user} successfully logged in")
        return redirect(url_for("user", usr=user))
    else:
        if "user" in session:
            flash(f"{session.get('user')} already logged in")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        user = session.get("user")
        return render_template("userprofile.html", user=user)
    else:
        flash(f"you are not logged in")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("logged out successfully", "info")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
