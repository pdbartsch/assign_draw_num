from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskdraw import db, bcrypt
from flaskdraw.users.forms import (
    LoginForm,
    RegistrationForm,
    UpdateAccountForm,
)
from flaskdraw.models import User
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
@login_required  # login required for this page
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("your account was created! now you can log in", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # if next parameter exists in url redirect to account page after login when trying to access page requiring login
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.index"))
        else:
            flash("Login unsuccessful. Please check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/account", methods=["GET", "POST"])
# @login_required  # login required for this page
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("your account has been updated", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":  # fill form with current users data
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template("account.html", title="Account", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
