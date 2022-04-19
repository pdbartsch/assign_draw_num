# flask run

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "{} is the title and {} is the description".format(
            self.title, self.description
        )


@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == "POST":  # IF is a post request then ...
        title = request.form["title"]
        description = request.form["description"]
        todo = Todo(title=title, description=description)
        db.session.add(todo)  # for adding values in the database
        db.session.commit()  # save the above additions to the database
    alltodos = Todo.query.all()  # if the request is not a post then ...
    return render_template("index.html", todos=alltodos)


@app.route("/delete/<int:sno>")
def delete(sno):
    deletetodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(deletetodo)
    db.session.commit()
    return redirect("/")


@app.route("/updatetodo/<int:sno>", methods=["GET", "POST"])
def updatetodo(sno):

    if request.method == "POST":
        updatetodo = Todo.query.filter_by(sno=sno).first()
        title = request.form["title"]
        description = request.form["description"]
        todo = Todo(title=title, description=description)
        updatetodo.title = title
        updatetodo.description = description
        db.session.commit()
        return redirect("/")
    updatetodo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", updatetodo=updatetodo)


# not for production:
if __name__ == "__main__":
    app.run(debug=True)
