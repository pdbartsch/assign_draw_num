import os
from flask import Blueprint

from flask import render_template, url_for, redirect, request
from sqlalchemy import text
from flaskdraw import bp_projects, db
from flaskdraw.bp_projects.forms import ProjectForm, ProjectSearchForm

from flaskdraw.models import Drawfile, Drawloc, Drawings
from flask_login import login_user, login_required
from datetime import datetime

bp_projects = Blueprint("bp_projects", __name__)
base_drawings_url = os.environ.get("base_drawings_url")


@bp_projects.route("/projects/<int:locnum>/")
def loc_group(locnum):
    form = ProjectSearchForm()
    # project = Drawfile.query.get_or_404(project_id)
    project = Drawfile.query.filter(Drawfile.locnum == locnum).all()
    return render_template(
        "project_cards.html",
        project=project,
    )


@bp_projects.route("/projects/<int:locnum>/<int:drawnum>/")
def project(locnum, drawnum):
    form = ProjectSearchForm()
    project = Drawfile.query.filter(
        Drawfile.locnum == locnum, Drawfile.drawnum == drawnum
    ).all()

    return render_template(
        "project_cards.html", project=project, sidebar="projectsearch", form=form
    )


@bp_projects.route("/projects/", methods=("GET", "POST"))
def projects():

    form = ProjectSearchForm()
    q = []

    if request.method == "POST":
        locnum = request.args.get("locnum")
        if locnum:
            no_search = False
            project_list = Drawfile.query.filter(Drawfile.locnum == locnum).all()
        else:
            if form.lnum.data:
                q.append("Drawfile.locnum == " + str(form.lnum.data))
            if form.drawnum.data:
                q.append("Drawfile.drawnum == " + str(form.drawnum.data))
            if form.projectmngr.data:
                q.append('Drawfile.projectmngr LIKE("%' + form.projectmngr.data + '%")')
            if form.mainconsult.data:
                q.append('Drawfile.mainconsult LIKE("%' + form.mainconsult.data + '%")')
            if form.title.data:
                q.append('Drawfile.title LIKE("%' + form.title.data + '%")')
            s = " AND ".join(q)
        if s == "":
            no_search = True
            project_list = None
        else:
            no_search = False
            project_list = (
                Drawfile.query.order_by(Drawfile.locnum.asc(), Drawfile.drawnum.asc())
                .filter(text(s))
                .all()
            )
        return render_template(
            "projects.html",
            form=form,
            project_list=project_list,
            sidebar="projectsearch",
            no_search=no_search,
        )
    return render_template(
        "projects.html", form=form, sidebar="projectsearch", no_search=True
    )


@bp_projects.route("/create/", methods=("GET", "POST"))
@bp_projects.route("/create/<int:locnum>", methods=("GET", "POST"))
@login_required  # login required for this page
def newproject(locnum):
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

        return redirect(url_for("bp_projects.projects") + str(locnum))

    project_count = Drawfile.query.filter(Drawfile.locnum == locnum).count()
    if project_count == 0:
        last_drawnum = None
        next_drawnum = None
    else:
        last_drawnum = (
            Drawfile.query.order_by(Drawfile.drawnum.desc())
            .filter(Drawfile.locnum == locnum)
            .options(db.load_only("drawnum"))
            .limit(1)
            .one()
        )
        next_drawnum = last_drawnum.drawnum + 1

    # sidebar last 5 projects under this location number
    drawings = (
        Drawfile.query.order_by(Drawfile.locnum.asc(), Drawfile.drawnum.desc())
        .filter(Drawfile.locnum == locnum)
        .limit(5)
        .all()
    )
    return render_template(
        "newproject.html",
        drawings=drawings,
        form=form,
        sidebar="addproject",
        locnum=locnum,
        next_drawnum=next_drawnum,
    )


@bp_projects.route("/<int:project_id>/editproj/", methods=("GET", "POST"))
@login_required  # login required for this page
def edit_proj(project_id):
    form = ProjectSearchForm()
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
        return redirect(
            url_for("bp_projects.projects") + str(locnum) + "/" + str(drawnum)
        )
    return render_template(
        "edit_proj.html", project=project, form=form, sidebar="projectsearch"
    )


@bp_projects.post("/<int:project_id>/delete/")
@login_required  # login required for this page
def delete(project_id):
    project = Drawfile.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("bp_main.index"))
