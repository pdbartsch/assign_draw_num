from flask import Blueprint

from flask import render_template, url_for, flash, redirect, request, abort
from flask import current_app
from sqlalchemy import text
from flaskdraw.bp_drawings.forms import (
    SearchForm,
    ProjectSearchForm
)

from flaskdraw.models import Drawfile
from flask_login import login_user, login_required

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template(
        "index.html",
        title="Home Page",
        sidebar="homepage"
    )

@main.route("/projects/<int:locnum>/<int:drawnum>/")
def project(locnum, drawnum):
    # project = Drawfile.query.get_or_404(project_id)
    project = Drawfile.query.filter(
        Drawfile.locnum == locnum, Drawfile.drawnum == drawnum
    ).all()

    return render_template("project.html", project=project, sidebar='projectsearch')


@main.route("/projects/<int:locnum>/")
def loc_group(locnum):
    # project = Drawfile.query.get_or_404(project_id)
    project = Drawfile.query.filter(Drawfile.locnum == locnum).all()
    return render_template("project.html", project=project, sidebar='projectsearch')


# pass stuff to search div
@main.context_processor
def base():
    form = ProjectSearchForm()
    return dict(form=form)


@main.route("/projects/", methods=("GET", "POST"))
def projects(): 
    form = ProjectSearchForm()

    q = []

    if request.method == "POST":

        # search across multiple optional fields
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
            sidebar='projectsearch',
            no_search=no_search,
        )
    return render_template("projects.html", form=form, sidebar='projectsearch', no_search=True)