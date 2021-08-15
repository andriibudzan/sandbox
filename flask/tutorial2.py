# author: andrii budzan
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", content=['andrew', 'choo', 'ptaah'])


@app.route("/base")
def base():
    return render_template("tut2.html")


if __name__ == '__main__':
    app.run(debug=True)
