import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flaskdraw import app, db, bcrypt
from flaskdraw.forms import (
    LocationForm,
    ProjectForm,
    LoginForm,
    RegistrationForm,
    UpdateAccountForm,
)
from flaskdraw.models import Drawfile, Drawloc, User
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

# Custom Filters
@app.template_filter("my_multiplier")
def datetime_format(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)


# Routes
@app.route("/register", methods=["GET", "POST"])
# @login_required  # login required for this page
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
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
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # if next parameter exists in url redirect to account page after login when trying to access page requiring login
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Login unsuccessful. Please check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/account", methods=["GET", "POST"])
# @login_required  # login required for this page
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("your account has been updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":  # fill form with current users data
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template("account.html", title="Account", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/")
def index():
    lnum = request.args.get("lnum")

    if lnum:
        drawings = (
            Drawfile.query.order_by(Drawfile.locnum.asc(), Drawfile.drawnum.asc())
            .filter(Drawfile.locnum == lnum)
            .all()
        )
    else:
        drawings = Drawfile.query.order_by(
            Drawfile.locnum.asc(), Drawfile.drawnum.asc()
        ).all()
    return render_template("index.html", drawings=drawings, title="Home Page")


@app.route("/<int:project_id>/")
def project(project_id):
    project = Drawfile.query.get_or_404(project_id)
    return render_template("project.html", project=project)


@app.route("/create/", methods=("GET", "POST"))
@login_required  # login required for this page
def create():
    form = ProjectForm()
    if request.method == "POST":
        locnum = int(form.locnum.data)
        drawnum = int(form.drawnum.data)
        contractnum = form.contractnum.data
        projectnum = form.projectnum.data
        projectmngr = form.projectmngr.data
        mainconsult = form.mainconsult.data
        title = form.title.data
        comments = form.comments.data
        datenow = datetime.now()

        project = Drawfile(
            locnum=locnum,
            drawnum=drawnum,
            contractnum=contractnum,
            projectnum=projectnum,
            projectmngr=projectmngr,
            mainconsult=mainconsult,
            title=title,
            comments=comments,
            date=datenow,
        )
        db.session.add(project)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("create.html", form=form)


@app.route("/<int:project_id>/edit/", methods=("GET", "POST"))
@login_required  # login required for this page
def edit(project_id):
    project = Drawfile.query.get_or_404(project_id)
    if request.method == "POST":
        locnum = int(request.form["locnum"])
        drawnum = int(request.form["drawnum"])
        contractnum = request.form["contractnum"]
        projectnum = request.form["projectnum"]
        projectmngr = request.form["projectmngr"]
        mainconsult = request.form["mainconsult"]
        title = request.form["title"]
        comments = request.form["comments"]
        daterecorded = request.form["daterecorded"]

        project.locnum = locnum
        project.drawnum = drawnum
        project.contractnum = contractnum
        project.projectnum = projectnum
        project.projectmngr = projectmngr
        project.mainconsult = mainconsult
        project.title = title
        project.comments = comments
        project.date = datetime.strptime(daterecorded, "%Y-%m-%d")

        db.session.add(project)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", project=project)


@app.post("/<int:project_id>/delete/")
@login_required  # login required for this page
def delete(project_id):
    project = Drawfile.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/add_loc/", methods=("GET", "POST"))
@login_required  # login required for this page
def add_loc():
    form = LocationForm()
    if request.method == "POST":
        locnum = int(form.locnum.data)
        locdescrip = form.locdescrip.data

        location = Drawloc(locnum=locnum, locdescrip=locdescrip)
        db.session.add(location)
        db.session.commit()

        return redirect(url_for("locations"))

    return render_template("addloc.html", form=form)


@app.route("/locs/")
def locations():
    # drawings = Drawfile.query.all()
    location_list = Drawloc.query.order_by(Drawloc.locnum.asc()).all()
    return render_template(
        "locations.html", location_list=location_list, title="Location Categories"
    )
