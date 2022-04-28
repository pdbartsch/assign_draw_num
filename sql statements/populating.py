flask shell
from app import db, Student, Drawloc, Drawfile
db.create_all()
# db.drop_all()


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


