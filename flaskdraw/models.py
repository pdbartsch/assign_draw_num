from flaskdraw import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # defines how printed out
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


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
    date = db.Column(db.Date)

    def __repr__(self):
        return f"<UCSB Drawing #{self.locnum}-{self.drawnum}: {self.title}>"


class Drawings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oldname = db.Column(db.String(255), nullable=True)
    newname = db.Column(db.String(255), nullable=True)
    locnum = db.Column(db.Integer, nullable=True)
    drawnum = db.Column(db.Integer, nullable=True)
    project_title = db.Column(db.String(255), nullable=True)
    project_number = db.Column(db.String(50), nullable=True)
    project_year = db.Column(db.Integer, nullable=True)
    sheet_title = db.Column(db.String(255), nullable=True)
    sheet_number = db.Column(db.String(255), nullable=True)
    discipline = db.Column(db.String(255), nullable=True)
    drawing_version = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.String(255), nullable=True)
    physical_location = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<UCSB Drawing #{self.locnum}-{self.drawnum}: {self.title}: c.{self.project_year}>"
