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


@bp_locations.route("/<int:loc_id>/editloc/", methods=("GET", "POST"))
@login_required  # login required for this page
def edit_loc(loc_id):
    location = Drawloc.query.get_or_404(loc_id)
    if request.method == "POST":
        locnum = int(request.form["locnum"])
        locdescrip = request.form["locdescrip"]

        location.locnum = locnum
        location.locdescrip = locdescrip

        db.session.add(location)
        db.session.commit()
        return redirect(url_for("bp_locations.locations"))
    return render_template("edit_loc.html", location=location)


@bp_locations.post("/<int:loc_id>/delete/")
@login_required  # login required for this page
def delete(loc_id):
    location = Drawloc.query.get_or_404(loc_id)
    db.session.delete(location)
    db.session.commit()
    return redirect(url_for("bp_main.index"))
