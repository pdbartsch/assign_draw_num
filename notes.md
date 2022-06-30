## To Do:
* More SQL Injection Testing
* SQL Alchemy working on a SQL DB
* Sidebars for the:
  * add_drawing page
  * Edit project page
* Edit Location page needs to be completed - currently not functional
* Edit project page could be improved visually
* drawing results page could use an edit row if logged in button
* subheadings and page titles should be visually consistent across pages


## Scratch  Notes:


`set FLASK_APP=run.py`

`set FLASK_ENV=development`

`flask run`

`flask shell`

## populate the database with some dummy data:

`from flaskdraw import create_app, db`

`app = create_app()`

`from flaskdraw.models import User, Drawloc, Drawfile, Drawings`

`db.drop_all()`

`db.create_all()`

`library = Drawloc(locnum = 525, locdescrip='Library')`

`bren = Drawloc(locnum = 521, locdescrip='Bren Hall')`

`ilp = Drawloc(locnum = 506, locdescrip='Interactive Learning Pavillion')`

`origlibrary = Drawfile(locnum = 525, drawnum = 101, projectmngr = 'Ray Aronson', mainconsult = 'Fugro', title = 'Library original construction set')`

`origbren = Drawfile(locnum = 521, drawnum = 101, projectmngr = 'Gary Banks', mainconsult = 'zgf', title = 'The construction of the BREN building')`

`origilp = Drawfile(locnum = 506, drawnum = 101, projectmngr = 'Liana Khammash', mainconsult = 'TBD', title = 'Classroom Building')`

`remlibrary = Drawfile(locnum = 525, drawnum = 601, projectmngr = 'Karl Burrelsman', mainconsult = 'McCarthy', title = 'Library addition and remodel')`

`libcastle = Drawfile(locnum = 525, drawnum = 701, projectmngr = 'Paul David Bartsch', mainconsult = 'Landon Bartsch', title = "Parker's New Castle")`

`db.session.add(library)`

`db.session.add(bren)`

`db.session.add(ilp)`

`db.session.add(origlibrary)`

`db.session.add(remlibrary)`

`db.session.add(origbren)`

`db.session.add(origilp)`

`db.session.add(libcastle)`

`db.session.commit()`

`Drawloc.query.all()`

- _generate requirements.txt file:_
  `pip freeze > requirements.txt`

- _install dependencies from requirements.txt file:_
  `pip install -r requirements.txt`

- [main tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)
- [flask package structure](https://medium.com/thedevproject/flask-project-structure-the-right-choice-to-start-4553740fad98)
- [Flask application setup](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/)

- [Flask WTF webforms](https://www.digitalocean.com/community/tutorials/how-to-use-and-validate-web-forms-with-flask-wtf)

- [How To Build Web Applications with Flask SERIES](https://www.digitalocean.com/community/tutorial_series/how-to-create-web-sites-with-flask)

- [Flask models](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/)

### table sorting

- [data tables](https://datatables.net/)

### git branching

- [git checkout -b dev](https://stackoverflow.com/a/4470822/747748)
- branch from a branch
- `git checkout -b feature dev`

## testing

`pytest --cov -v`

- try: http://localhost:5000/drawings/525/601/
- https://testdriven.io/blog/flask-pytest/
- https://realpython.com/python-testing/

- [check out the test configuration section](https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/)

## coverage report

- `coverage report -m`
- `coverage html`

## generate a secret key

`>python> import os`

`>python> os.urandom(32)`

- sort_args = request.args.getlist("\_sort")
- http://localhost:5000/?searched=lib&lnum=11
- https://programtalk.com/python-examples/flask.request.args.getlist/

## deploy

- [link 1](http://exploreflask.com/en/latest/deployment.html)
- []()
- []()
- []()
- []()

## todo

- remember me login page
- user groups with certain permissions ... after this I'll show the registration page again
- implement drawing search
- [possibly add text search across multiple fields](https://pythonhosted.org/Flask-WhooshAlchemy/)
