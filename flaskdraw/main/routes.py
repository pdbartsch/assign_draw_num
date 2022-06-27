from flask import Blueprint

from flask import render_template, url_for, flash, redirect, request, abort
from flask import current_app
from sqlalchemy import text
from flaskdraw.drawproj.forms import (
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

@main.route("/projects/")
def projects():
    form = SearchForm()
    # if form.validate_on_submit():
    lnum = request.args.get("lnum")
    searched = request.args.get("searched")

    if lnum:
        filtered_locations = True
        project_list = (
            Drawfile.query.order_by(Drawfile.locnum.asc(), Drawfile.drawnum.asc())
            .filter(Drawfile.locnum == lnum)
            .all()
        )
        subheading = "Projects Associated with Location " + str(lnum) + ":"
    elif searched:
        filtered_locations = True
        project_list = (
            Drawfile.query.order_by(Drawfile.locnum.asc(), Drawfile.drawnum.asc())
            .filter(Drawfile.title.like("%" + searched + "%"))
            .all()
        )
        subheading = "Projects Associated with Title like " + searched + ":"
    else:
        filtered_locations = False
        project_list = Drawfile.query.order_by(
            Drawfile.locnum.asc(), Drawfile.drawnum.asc()
        ).all()
        subheading = "All Projects: "
    return render_template(
        "projects.html",
        project_list=project_list,
        title="Projects Page",
        filtered_locations=filtered_locations,
        subheading=subheading,
        sidebar='projectsearch'
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
    form = SearchForm()
    return dict(form=form)


# search results
@main.route("/projects/search", methods=["POST"])
def search():
    form = SearchForm()
    project_list = Drawfile.query
    # get data from submitted form
    searched = form.searched.data
    if searched:
        if form.validate_on_submit():
            project_list = project_list.filter(Drawfile.title.like("%" + searched + "%"))
            project_list = project_list.order_by(
                Drawfile.locnum.asc(), Drawfile.drawnum.asc()
            ).all()
            return render_template(
                "projects.html", form=form, searched=searched, project_list=project_list, sidebar='projectsearch'
            )
    else:
        project_list = project_list.order_by(
            Drawfile.locnum.asc(), Drawfile.drawnum.asc()
        ).all()
        return render_template("projects.html", form=form, project_list=project_list, sidebar='projectsearch')


# ProjectSearchForm

@main.route("/search_projects/", methods=("GET", "POST"))
def search_drawings(): 
    form = ProjectSearchForm()

    q = []

    if request.method == "POST":

        # search across multiple optional fields
        if form.lnum.data:
            q.append("project_list.locnum == " + str(form.lnum.data))
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
                Drawfile.query.order_by(Drawfile.lnum.asc(), Drawfile.drawnum.asc())
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
