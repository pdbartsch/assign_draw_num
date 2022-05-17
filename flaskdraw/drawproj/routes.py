from flask import Blueprint

from flask import render_template, url_for, redirect, request
from flaskdraw import db
from flaskdraw.drawproj.forms import LocationForm, ProjectForm, DrawingsForm

from flaskdraw.models import Drawfile, Drawloc, User, Drawings
from flask_login import login_user, login_required
from datetime import datetime

drawproj = Blueprint("drawproj", __name__)


@drawproj.route("/drawings/")
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
        heading="Result of drawing search:",
    )


@drawproj.route("/drawings/<int:locnum>/")
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


@drawproj.route("/drawings/<int:locnum>/<int:drawnum>/")
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


@drawproj.route("/create/", methods=("GET", "POST"))
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

        return redirect(url_for("main.index"))

    return render_template("create.html", form=form)


@drawproj.route("/add_drawing/", methods=("GET", "POST"))
@login_required  # login required for this page
def add_drawing():
    form = DrawingsForm()
    if request.method == "POST":
        oldname = form.oldname.data
        newname = form.newname.data
        locnum = int(form.locnum.data)
        drawnum = int(form.drawnum.data)
        project_title = form.project_title.data
        project_number = form.project_number.data
        project_year = form.project_year.data
        sheet_title = form.sheet_title.data
        sheet_number = form.sheet_number.data
        discipline = form.discipline.data
        drawing_version = form.drawing_version.data
        notes = form.notes.data

        drawing = Drawings(
            oldname=oldname,
            newname=newname,
            locnum=locnum,
            drawnum=drawnum,
            project_number=project_number,
            sheet_number=sheet_number,
            project_year=project_year,
            project_title=project_title,
            sheet_title=sheet_title,
            discipline=discipline,
            drawing_version=drawing_version,
            notes=notes,
        )
        db.session.add(drawing)
        db.session.commit()

        return redirect(url_for("main.index"))

    return render_template("add_drawing.html", form=form)


@drawproj.route("/search_drawings/", methods=("GET", "POST"))
def search_drawings():
    form = DrawingsForm()
    if request.method == "POST":
        locnum = int(form.locnum.data)
        drawnum = int(form.drawnum.data)
        project_title = form.project_title.data
        project_number = form.project_number.data
        sheet_title = form.sheet_title.data
        sheet_number = form.sheet_number.data
        discipline = form.discipline.data

        return redirect(url_for("main.index"))

    return render_template("search_drawings.html", form=form)


@drawproj.route("/create/<int:locnum>", methods=("GET", "POST"))
def newproject(locnum):
    form = ProjectForm()
    drawings = (
        Drawfile.query.order_by(Drawfile.locnum.asc(), Drawfile.drawnum.desc())
        .filter(Drawfile.locnum == locnum)
        .limit(5)
        .all()
    )
    return render_template("newproject.html", drawings=drawings)


@drawproj.route("/<int:project_id>/edit/", methods=("GET", "POST"))
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
        return redirect(url_for("main.index"))
    return render_template("edit.html", project=project)


@drawproj.route("/editloc/<int:locnum>", methods=("GET", "POST"))
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
        return redirect(url_for("drawproj.locations"))
    return render_template("edit_loc.html", row=row)


@drawproj.post("/<int:project_id>/delete/")
@login_required  # login required for this page
def delete(project_id):
    project = Drawfile.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("main.index"))


@drawproj.route("/add_loc/", methods=("GET", "POST"))
@login_required  # login required for this page
def add_loc():
    form = LocationForm()
    if request.method == "POST":
        locnum = int(form.locnum.data)
        locdescrip = form.locdescrip.data

        location = Drawloc(locnum=locnum, locdescrip=locdescrip)
        db.session.add(location)
        db.session.commit()

        return redirect(url_for("drawproj.locations"))

    return render_template("addloc.html", form=form)


@drawproj.route("/locs/")
def locations():
    # drawings = Drawfile.query.all()
    location_list = Drawloc.query.order_by(Drawloc.locnum.asc()).all()
    return render_template(
        "locations.html", location_list=location_list, title="Location Categories"
    )
