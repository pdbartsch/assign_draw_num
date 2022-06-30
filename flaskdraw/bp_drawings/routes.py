import os
from flask import Blueprint

from flask import render_template, url_for, redirect, request
from sqlalchemy import text
from flaskdraw import bp_drawings, db
from flaskdraw.bp_drawings.forms import (
    DrawingsForm,
    DrawingsSearchForm,
)

from flaskdraw.models import Drawings
from flask_login import login_required

bp_drawings = Blueprint("bp_drawings", __name__)
base_drawings_url = os.environ.get("base_drawings_url")


@bp_drawings.route("/drawings/")
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
        subheading="Result of drawing search:",
        base_drawings_url=base_drawings_url,
    )


@bp_drawings.route("/drawings/<int:locnum>/")
def location_set(locnum):
    drawings = (
        Drawings.query.order_by(Drawings.locnum.asc(), Drawings.drawnum.asc())
        .filter(Drawings.locnum == locnum)
        .all()
    )
    return render_template(
        "drawings.html",
        drawings=drawings,
        title="Drawing search results",
        subheading="Drawing results for location #" + str(locnum) + ":",
        base_drawings_url=base_drawings_url,
    )


@bp_drawings.route("/drawings/<int:locnum>/<int:drawnum>/")
def drawing_set(locnum, drawnum):
    drawings = (
        Drawings.query.order_by(Drawings.locnum.asc(), Drawings.drawnum.asc())
        .filter(Drawings.locnum == locnum, Drawings.drawnum == drawnum)
        .all()
    )
    return render_template(
        "drawings.html",
        drawings=drawings,
        title="Drawing search results",
        subheading="Drawing Set " + str(locnum) + "-" + str(drawnum) + ":",
        base_drawings_url=base_drawings_url,
    )


@bp_drawings.route("/add_drawing/", methods=("GET", "POST"))
@login_required  # login required for this page
def add_drawing():
    form = DrawingsForm()
    if request.method == "POST":
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

        return redirect(url_for("bp_main.index"))

    return render_template("add_drawing.html", form=form, sidebar="drawingedit")


@bp_drawings.route("/search_drawings/", methods=("GET", "POST"))
def search_drawings():  # https://stackoverflow.com/a/27810889/747748
    form = DrawingsSearchForm()

    q = []

    if request.method == "POST":

        # search across multiple optional fields
        if form.locnum.data:
            q.append("Drawings.locnum == " + str(form.locnum.data))
        if form.drawnum.data:
            q.append("Drawings.drawnum == " + str(form.drawnum.data))
        if form.project_title.data:
            q.append('Drawings.project_title LIKE("%' + form.project_title.data + '%")')
        if form.sheet_title.data:
            q.append('Drawings.sheet_title LIKE("%' + form.sheet_title.data + '%")')
        if form.sheet_number.data:
            q.append('Drawings.sheet_number LIKE("%' + form.sheet_number.data + '%")')
        if form.discipline.data:
            q.append('Drawings.discipline LIKE("%' + form.discipline.data + '%")')
        s = " AND ".join(q)

        if s == "":
            no_search = True
            drawings = None
        else:
            no_search = False
            drawings = (
                Drawings.query.order_by(Drawings.locnum.asc(), Drawings.drawnum.asc())
                .filter(text(s))
                .all()
            )

        return render_template(
            "drawings.html",
            form=form,
            drawings=drawings,
            base_drawings_url=base_drawings_url,
            sidebar="drawingsearch",
            no_search=no_search,
            subheading="Search results:",
        )
    return render_template(
        "drawings.html", form=form, sidebar="drawingsearch", no_search=True
    )


@bp_drawings.route("/<int:drawing_id>/editdraw/", methods=("GET", "POST"))
@login_required  # login required for this page
def edit_draw(drawing_id):
    drawing = Drawings.query.get_or_404(drawing_id)
    if request.method == "POST":
        newname = request.form["newname"]
        locnum = int(request.form["locnum"])
        drawnum = int(request.form["drawnum"])
        project_year = int(request.form["project_year"])
        project_number = request.form["project_number"]
        sheet_number = request.form["sheet_number"]
        project_title = request.form["project_title"]
        sheet_title = request.form["sheet_title"]
        discipline = request.form["discipline"]
        drawing_version = request.form["drawing_version"]
        notes = request.form["notes"]

        drawing.newname = newname
        drawing.locnum = locnum
        drawing.drawnum = drawnum
        drawing.project_year = project_year
        drawing.project_number = project_number
        drawing.sheet_number = sheet_number
        drawing.project_title = project_title
        drawing.sheet_title = sheet_title
        drawing.discipline = discipline
        drawing.drawing_version = drawing_version
        drawing.notes = notes

        db.session.add(drawing)
        db.session.commit()
        return redirect(
            url_for("bp_drawings.drawings") + str(locnum) + "/" + str(drawnum)
        )
    return render_template("edit_draw.html", drawing=drawing, sidebar="drawingedit")
