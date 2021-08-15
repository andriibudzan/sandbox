# author: andrii budzan
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "very_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=3)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = False
        user = request.form.get("nm", "user")
        session["user"] = user
        found_user = users.query.filter_by(name=user).first()
        # if you need to DELETE ONE object from db:
        # found_user = users.query.filter_by(name=user).delete()
        # db.session.commit()
        # if DELETE MULTIPLE:
        # found_users = users.query.filter_by(name=user).all()
        # for user in found_users:
        #   user.delete()
        # db.session.commit()

        if found_user:
            session['email'] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash(f"{user} successfully logged in")
        return redirect(url_for("user", usr=user))
    else:
        if "user" in session:
            flash(f"{session.get('user')} already logged in")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("logged out successfully", "info")
    return redirect(url_for("login"))


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session.get("user")

        if request.method == "POST":
            email = request.form.get("email", "")
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash('your email saved')
        else:
            if "email" in session:
                email = session.get("email", "")
        return render_template("userprofile.html", user=user, email=email)
    else:
        flash(f"you are not logged in")
        return redirect(url_for("login"))


@app.route("/users")
def list_users():
    return render_template("list_users.html", values=users.query.all())


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
