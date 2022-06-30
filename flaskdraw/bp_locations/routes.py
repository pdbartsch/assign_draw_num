import os
from flask import Blueprint

from flask import render_template, url_for, redirect, request
from sqlalchemy import text
from flaskdraw import bp_projects, db
from flaskdraw.bp_locations.forms import LocationForm

from flaskdraw.models import Drawfile, Drawloc, Drawings
from flask_login import login_user, login_required
from datetime import datetime

bp_locations = Blueprint("bp_locations", __name__)
base_drawings_url = os.environ.get("base_drawings_url")


@bp_locations.route("/locations/")
def locations():
    location_list = Drawloc.query.order_by(Drawloc.locnum.asc()).all()
    return render_template(
        "locations.html",
        location_list=location_list,
        title="Location Categories",
        sidebar="locationpage",
        subheading="Location Categories:",
    )


@bp_locations.route("/add_loc/", methods=("GET", "POST"))
@login_required  # login required for this page
def add_loc():
    form = LocationForm()
    if request.method == "POST":
        locnum = int(form.locnum.data)
        locdescrip = form.locdescrip.data

        location = Drawloc(locnum=locnum, locdescrip=locdescrip)
        db.session.add(location)
        db.session.commit()

        return redirect(url_for("bp_locations.locations"))

    return render_template("addloc.html", form=form)


# @bp_locations.route("/<int:project_id>/editproj/", methods=("GET", "POST"))
# @login_required  # login required for this page
# def edit_proj(project_id):
#     project = Drawfile.query.get_or_404(project_id)
#     if request.method == "POST":
#         locnum = int(request.form["locnum"])
#         drawnum = int(request.form["drawnum"])
#         contractnum = request.form["contractnum"]
#         projectnum = request.form["projectnum"]
#         projectmngr = request.form["projectmngr"]
#         mainconsult = request.form["mainconsult"]
#         title = request.form["title"]
#         comments = request.form["comments"]
#         daterecorded = request.form["daterecorded"]

#         project.locnum = locnum
#         project.drawnum = drawnum
#         project.contractnum = contractnum
#         project.projectnum = projectnum
#         project.projectmngr = projectmngr
#         project.mainconsult = mainconsult
#         project.title = title
#         project.comments = comments
#         project.date = datetime.strptime(daterecorded, "%Y-%m-%d")

#         db.session.add(project)
#         db.session.commit()
#         return redirect(url_for("bp_main.index"))
#     return render_template("edit_proj.html", project=project)


@bp_locations.route("/editloc/<int:locnum>", methods=("GET", "POST"))
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
        return redirect(url_for("bp_locations.locations"))
    return render_template("edit_loc.html", row=row)


@bp_locations.post("/<int:project_id>/delete/")
@login_required  # login required for this page
def delete(project_id):
    project = Drawfile.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("bp_main.index"))
