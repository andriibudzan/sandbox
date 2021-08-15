# author: andrii budzan
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


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
        user = request.form.get("nm", "user")
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")


@app.route("/user/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == '__main__':
    app.run(debug=True)
