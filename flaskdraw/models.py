from sqlalchemy.sql import func
# from flaskdraw import db
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
    date = db.Column(db.DateTime)

    def __repr__(self):
        return f"<UCSB Drawing #{self.locnum}-{self.drawnum}: {self.title}>"



