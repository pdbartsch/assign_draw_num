set FLASK_APP=run.py
set FLASK_ENV=development
flask run

- [generate requirements.txt file]
  `pip freeze > requirements.txt`

- [main tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)
- [flask package structure](https://medium.com/thedevproject/flask-project-structure-the-right-choice-to-start-4553740fad98)
- [Flask application setup](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/)

- [Flask WTF webforms](https://www.digitalocean.com/community/tutorials/how-to-use-and-validate-web-forms-with-flask-wtf)

- [How To Build Web Applications with Flask SERIES](https://www.digitalocean.com/community/tutorial_series/how-to-create-web-sites-with-flask)

https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

flask shell
from app import db, Student, Drawloc, Drawfile
db.create_all()

## db.drop_all()

student_john = Student(firstname='john', lastname='doe',
email='jd@example.com', age=23,
bio='Biology student')

library = Drawloc(locnum = 525, locdescrip='Library')
bren = Drawloc(locnum = 521, locdescrip='Bren Hall')
ilp = Drawloc(locnum = 506, locdescrip='Interactive Learning Pavillion')

origlibrary = Drawfile(locnum = 525, drawnum = 101, projectmngr = 'Ray Aronson', mainconsult = 'Fugro', title = 'Library original construction set')
origbren = Drawfile(locnum = 521, drawnum = 101, projectmngr = 'Gary Banks', mainconsult = 'zgf', title = 'The construction of the BREN building')
origilp = Drawfile(locnum = 506, drawnum = 101, projectmngr = 'Liana Khammash', mainconsult = 'TBD', title = 'Classroom Building')

db.session.add(student_john)

db.session.add(library)
db.session.add(bren)
db.session.add(ilp)

db.session.add(origlibrary)
db.session.add(origbren)
db.session.add(origilp)

db.session.commit()

# Drawloc.query.all()

# table sorting

- [My favorite method as of 2022](https://stackoverflow.com/a/70024272/747748)
