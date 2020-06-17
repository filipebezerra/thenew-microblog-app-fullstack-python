from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Filipe"}
    posts = [
        {
            "author": {"username": "Marilyn"},
            "body": "I'm having good times at the beach",
        },
        {
            "author": {"username": "Susan"},
            "body": "I want to give you a tip about travelling to Paris",
        },
        {
            "author": {"username": "Jake"},
            "body": "What's going on right now at Democratic Republic of Congo",
        },
        {"author": {"username": "Frank"}, "body": "We need your donation right now"},
        {"author": {"username": "Natalie"}, "body": "Give love to everyone"},
        {
            "author": {"username": "Joanna"},
            "body": "We need to talk about Impostor Syndrome",
        },
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}"
        )
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)
