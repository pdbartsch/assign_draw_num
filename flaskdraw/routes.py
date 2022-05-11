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
    SearchForm,
)
from flaskdraw.models import Drawfile, Drawloc, User, Drawings
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
    form = SearchForm()
    # if form.validate_on_submit():
    lnum = request.args.get("lnum")
    searched = request.args.get("searched")

    if lnum:
        filtered_locations = True
        drawings = (
            Drawfile.query.order_by(Drawfile.locnum.asc(), Drawfile.drawnum.asc())
            .filter(Drawfile.locnum == lnum)
            .all()
        )
        subheading = "Projects Associated with Location " + str(lnum) + ":"
    elif searched:
        filtered_locations = True
        drawings = (
            Drawfile.query.order_by(Drawfile.locnum.asc(), Drawfile.drawnum.asc())
            .filter(Drawfile.title.like("%" + searched + "%"))
            .all()
        )
        subheading = "Projects Associated with Title like " + searched + ":"
    else:
        filtered_locations = False
        drawings = Drawfile.query.order_by(
            Drawfile.locnum.asc(), Drawfile.drawnum.asc()
        ).all()
        subheading = "Showing all Projects: "
    return render_template(
        "index.html",
        drawings=drawings,
        title="Home Page",
        filtered_locations=filtered_locations,
        subheading=subheading,
    )


@app.route("/drawings/")
def drawings():
    locnum = request.args.get("locnum")
    drawnum = request.args.get("drawnum")
    if locnum and drawnum:
        drawings = (
            Drawings.query.order_by(Drawings.locnum.asc(), Drawings.drawnum.asc())
            .filter(Drawings.locnum == locnum, Drawings.drawnum == drawnum)
            .all()
        )
    elif locnum:
        drawings = (
            Drawings.query.order_by(Drawings.locnum.asc(), Drawings.drawnum.asc())
            .filter(Drawings.locnum == locnum)
            .all()
        )
    else:
        drawings = None

    return render_template(
        "drawings.html",
        drawings=drawings,
        title="Drawing results:",
        heading = "Result of drawing search:"
    )


@app.route("/drawings/<int:locnum>/")
def location_set(locnum):
    drawings = (
        Drawings.query.order_by(Drawings.locnum.asc(), Drawings.drawnum.asc())
        .filter(Drawings.locnum == locnum)
        .all()
    )
    return render_template(
        "drawings.html",
        drawings=drawings,
        title="Drawing results for location #" + str(locnum),
    )


@app.route("/drawings/<int:locnum>/<int:drawnum>/")
def drawing_set(locnum, drawnum):
    drawings = (
        Drawings.query.order_by(Drawings.locnum.asc(), Drawings.drawnum.asc())
        .filter(Drawings.locnum == locnum, Drawings.drawnum == drawnum)
        .all()
    )
    return render_template(
        "drawings.html",
        drawings=drawings,
        title="Drawing Set " + str(locnum) + "-" + str(drawnum),
    )

# pass stuff to search div
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# search results
@app.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    drawings = Drawfile.query
    # get data from submitted form
    searched = form.searched.data
    if searched:
        if form.validate_on_submit():
            drawings = drawings.filter(Drawfile.title.like("%" + searched + "%"))
            drawings = drawings.order_by(
                Drawfile.locnum.asc(), Drawfile.drawnum.asc()
            ).all()
            return render_template(
                "search.html", form=form, searched=searched, drawings=drawings
            )
    else:
        drawings = drawings.order_by(
            Drawfile.locnum.asc(), Drawfile.drawnum.asc()
        ).all()
        return render_template("index.html", form=form, drawings=drawings)


@app.route("/<int:locnum>/<int:drawnum>/")
def project(locnum, drawnum):
    # project = Drawfile.query.get_or_404(project_id)
    project = Drawfile.query.filter(
        Drawfile.locnum == locnum, Drawfile.drawnum == drawnum
    ).all()

    return render_template("project.html", project=project)


@app.route("/<int:locnum>/")
def loc_group(locnum):
    # project = Drawfile.query.get_or_404(project_id)
    project = Drawfile.query.filter(Drawfile.locnum == locnum).all()
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


@app.route("/create/<int:locnum>", methods=("GET", "POST"))
def newproject(locnum):
    form = ProjectForm()
    drawings = (
        Drawfile.query.order_by(Drawfile.locnum.asc(), Drawfile.drawnum.desc())
        .filter(Drawfile.locnum == locnum)
        .limit(5)
        .all()
    )
    return render_template("newproject.html", drawings=drawings)


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


@app.route("/editloc/<int:locnum>", methods=("GET", "POST"))
@login_required  # login required for this page
def edit_loc(locnum):
    row = Drawloc.query.filter(Drawloc.locnum == locnum).all()
    if request.method == "POST":
        locnum = int(request.form["locnum"])
        locdescrip = request.form["locdescrip"]

        row.locnum = locnum
        row.locdescrip = locdescrip

        db.session.add(row)
        db.session.commit()
        return redirect(url_for("locations"))
    return render_template("edit_loc.html", row=row)


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
