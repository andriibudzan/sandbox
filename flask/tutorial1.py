# author: andrii budzan
from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>home page</h1>"


@app.route("/<name>")
def user(name):
    return f"<h1>user page</h1>user: {name}"

# basic redirect
# @app.route("/admin")
# def admin():
#     return redirect(url_for("home"))  # in url_for we need to pass function, which renders our redirect target


# parametrized redirect
@app.route("/admin")
def admin():
    # we need to define parameter,
    # which will be passed to our target function:
    return redirect(url_for("user", name='Admin'))


if __name__ == '__main__':
    app.run()
