import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from forms import LocationForm, ProjectForm

SECRET_KEY = os.urandom(32)


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f"<Student {self.firstname}>"


class Drawloc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    locnum = db.Column(db.Integer, nullable=False)
    locdescrip = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Drawing Location {self.locnum} - {self.locdescrip}>"


class Drawfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    locnum = db.Column(db.Integer, db.ForeignKey("drawloc.locnum"), nullable=False)
    drawnum = db.Column(db.Integer, nullable=False)
    contractnum = db.Column(db.String(50), nullable=True)
    projectnum = db.Column(db.String(10), nullable=True)
    projectmngr = db.Column(db.String(100), nullable=True)
    mainconsult = db.Column(db.String(100), nullable=True)
    title = db.Column(db.Text, nullable=False)
    comments = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return f"<UCSB Drawing #{self.locnum}-{self.drawnum}: {self.title}>"


@app.route("/")
def index():
    lnum = request.args.get('lnum')

    if lnum:
        drawings = Drawfile.query.order_by(Drawfile.locnum.asc(), Drawfile.drawnum.asc()).filter(Drawfile.locnum == lnum).all()
    else:
        drawings = Drawfile.query.order_by(Drawfile.locnum.asc(), Drawfile.drawnum.asc()).all()
    return render_template("index.html", drawings=drawings, title="Home Page")


@app.route("/<int:project_id>/")
def project(project_id):
    project = Drawfile.query.get_or_404(project_id)
    return render_template("project.html", project=project)


@app.route("/create/", methods=("GET", "POST"))
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

        project = Drawfile(
            locnum=locnum, drawnum=drawnum, contractnum=contractnum, projectnum=projectnum, projectmngr=projectmngr, mainconsult=mainconsult, title=title, comments=comments
        )
        db.session.add(project)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("create.html", form=form)


@app.route("/<int:project_id>/edit/", methods=("GET", "POST"))
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

        project.locnum = locnum
        project.drawnum = drawnum
        project.contractnum = contractnum
        project.projectnum = projectnum
        project.projectmngr = projectmngr
        project.mainconsult = mainconsult
        project.title = title
        project.comments = comments

        db.session.add(project)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("edit.html", project=project)


@app.post("/<int:project_id>/delete/")
def delete(project_id):
    project = Drawfile.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("index"))



@app.route("/add_loc/", methods=("GET", "POST"))
def add_loc():
    form = LocationForm()
    if request.method == "POST":
        locnum = int(form.locnum.data)
        locdescrip = (form.locdescrip.data)

        location = Drawloc(locnum=locnum, locdescrip=locdescrip)
        db.session.add(location)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("addloc.html", form=form)


@app.route("/locs/")
def locations():
    # drawings = Drawfile.query.all()
    location_list = Drawloc.query.order_by(Drawloc.locnum.asc()).all()
    return render_template("locations.html", location_list=location_list, title="Location Categories")

