set FLASK_APP=run.py
set FLASK_ENV=development
flask run
flask shell

# populate the database with some dummy data

# haven't figured out date format yet

from flaskdraw import create_app, db
app = create_app()
from flaskdraw.models import User, Drawloc, Drawfile, Drawings
db.drop_all()
db.create_all()

library = Drawloc(locnum = 525, locdescrip='Library')
bren = Drawloc(locnum = 521, locdescrip='Bren Hall')
ilp = Drawloc(locnum = 506, locdescrip='Interactive Learning Pavillion')
origlibrary = Drawfile(locnum = 525, drawnum = 101, projectmngr = 'Ray Aronson', mainconsult = 'Fugro', title = 'Library original construction set')
origbren = Drawfile(locnum = 521, drawnum = 101, projectmngr = 'Gary Banks', mainconsult = 'zgf', title = 'The construction of the BREN building')
origilp = Drawfile(locnum = 506, drawnum = 101, projectmngr = 'Liana Khammash', mainconsult = 'TBD', title = 'Classroom Building')
remlibrary = Drawfile(locnum = 525, drawnum = 601, projectmngr = 'Karl Burrelsman', mainconsult = 'McCarthy', title = 'Library addition and remodel')
libcastle = Drawfile(locnum = 525, drawnum = 701, projectmngr = 'Paul David Bartsch', mainconsult = 'Landon Bartsch', title = "Parker's New Castle")
db.session.add(library)
db.session.add(bren)
db.session.add(ilp)
db.session.add(origlibrary)
db.session.add(remlibrary)
db.session.add(origbren)
db.session.add(origilp)
db.session.add(libcastle)
db.session.commit()

# Drawloc.query.all()

- [generate requirements.txt file]
  `pip freeze > requirements.txt`

- [install dependencies from requirements.txt file]
  `pip install -r requirements.txt`

- [main tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)
- [flask package structure](https://medium.com/thedevproject/flask-project-structure-the-right-choice-to-start-4553740fad98)
- [Flask application setup](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/)

- [Flask WTF webforms](https://www.digitalocean.com/community/tutorials/how-to-use-and-validate-web-forms-with-flask-wtf)

- [How To Build Web Applications with Flask SERIES](https://www.digitalocean.com/community/tutorial_series/how-to-create-web-sites-with-flask)

https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

# table sorting

- [My favorite method as of 2022](https://stackoverflow.com/a/49041392/747748)
- [With this tweak](https://stackoverflow.com/a/53880407/747748)

# git branching

- [git checkout -b dev](https://stackoverflow.com/a/4470822/747748)
- branch from a branch
- `git checkout -b feature dev`

try: http://localhost:5000/drawings/525/601/

# testing

pytest --cov -v
or
pytest -v
or
python pytest -v
https://testdriven.io/blog/flask-pytest/
https://realpython.com/python-testing/
