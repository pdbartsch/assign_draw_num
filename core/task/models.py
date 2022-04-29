from .. import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loc = db.Column(db.Integer)
    name = db.Column(db.String(60))

    def __repr__(self):
        return '<Category {}>'.format(self.name)