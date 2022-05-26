from flask import Blueprint

from flask import render_template, url_for, flash, redirect, request, abort
from flask import current_app

from flaskdraw.drawproj.forms import (
    SearchForm,
)

from flaskdraw.models import Drawfile
from flask_login import login_user, login_required

main = Blueprint("main", __name__)


@main.route("/")
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
        subheading = "All Projects: "
    return render_template(
        "index.html",
        drawings=drawings,
        title="Home Page",
        filtered_locations=filtered_locations,
        subheading=subheading,
    )


@main.route("/<int:locnum>/<int:drawnum>/")
def project(locnum, drawnum):
    # project = Drawfile.query.get_or_404(project_id)
    project = Drawfile.query.filter(
        Drawfile.locnum == locnum, Drawfile.drawnum == drawnum
    ).all()

    return render_template("project.html", project=project)


@main.route("/<int:locnum>/")
def loc_group(locnum):
    # project = Drawfile.query.get_or_404(project_id)
    project = Drawfile.query.filter(Drawfile.locnum == locnum).all()
    return render_template("project.html", project=project)


# pass stuff to search div
@main.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# search results
@main.route("/search", methods=["POST"])
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
