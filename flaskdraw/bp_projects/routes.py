import os
from flask import Blueprint

from flask import render_template, url_for, redirect, request
from sqlalchemy import text
from flaskdraw import bp_projects, db
from flaskdraw.bp_drawings.forms import (
    LocationForm,
    ProjectForm,
    DrawingsForm,
    DrawingsSearchForm,
)

from flaskdraw.models import Drawfile, Drawloc, Drawings
from flask_login import login_user, login_required
from datetime import datetime

bp_projects = Blueprint("bp_projects", __name__)
base_drawings_url = os.environ.get("base_drawings_url")



@bp_projects.route("/create/<int:locnum>", methods=("GET", "POST"))
def newproject(locnum):
    form = ProjectForm()
    drawings = (
        Drawfile.query.order_by(Drawfile.locnum.asc(), Drawfile.drawnum.desc())
        .filter(Drawfile.locnum == locnum)
        .limit(5)
        .all()
    )
    return render_template("newproject.html", drawings=drawings)


@bp_projects.route("/<int:project_id>/editproj/", methods=("GET", "POST"))
@login_required  # login required for this page
def edit_proj(project_id):
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
    return render_template("edit_proj.html", project=project)


@bp_projects.route("/editloc/<int:locnum>", methods=("GET", "POST"))
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


@bp_projects.post("/<int:project_id>/delete/")
@login_required  # login required for this page
def delete(project_id):
    project = Drawfile.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("main.index"))

