# from pandas import isnull
from flaskdraw.models import User, Drawfile, Drawloc, Drawings
from flask_bcrypt import generate_password_hash


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email and hashed_password are correctly defined
    """
    user = User(
        username="pdbar", email="pdbartsch@gmail.com", password="FlaskIsAwesome"
    )
    hashed_password = generate_password_hash(user.password).decode("utf-8")
    assert user.username == "pdbar"
    assert user.email == "pdbartsch@gmail.com"
    assert hashed_password != user.password


def test_new_location():
    """
    GIVEN Drawloc model
    WHEN a new location is created
    THEN check the fields are correctly defined
    """
    ilp = Drawloc(locnum=506, locdescrip="Interactive Learning Pavillion")
    # assert ilp.id > 0
    assert ilp.locnum == 506
    assert ilp.locdescrip == "Interactive Learning Pavillion"


def test_new_project():
    """
    GIVEN Drafile model
    WHEN a new project is created
    THEN check the fields are correctly defined
    """
    origilp = Drawfile(
        locnum=506,
        drawnum=101,
        projectmngr="Liana Khammash",
        mainconsult="TBD",
        title="Classroom Building",
    )
    assert origilp.locnum == 506
    assert origilp.title == "Classroom Building"
    assert origilp.drawnum == 101
    assert origilp.projectmngr == "Liana Khammash"
    assert origilp.mainconsult == "TBD"
    assert origilp.projectnum == None


def test_new_drawing():
    """
    GIVEN Drawings model
    WHEN a new project is created
    THEN check the fields are correctly defined
    """

    newDrawing = Drawings(
        oldname="34_348_0.pdf",
        newname="34_348_CIV_0_26726.pdf",
        locnum=34,
        drawnum=348,
        project_title="PARKING LOT 38",
        project_number="FM805/18-7",
        project_year=2004,
        sheet_title="Sheet Title Example",
        sheet_number="A1_0_7",
        discipline="CIVIL",
        drawing_version="As-Built",
        notes="Original file name was: R_G8_0034_0348_NO_0000.TIF Original drawer was: 31",
        physical_location="Original Ucsb Drawer 31",
    )

    assert newDrawing.project_number == "FM805/18-7"
    assert newDrawing.oldname == "34_348_0.pdf"
    assert newDrawing.newname == "34_348_CIV_0_26726.pdf"
    assert newDrawing.locnum == 34
    assert newDrawing.drawnum == 348
    assert newDrawing.project_title == "PARKING LOT 38"
    assert newDrawing.project_number == "FM805/18-7"
    assert newDrawing.project_year == 2004
    assert newDrawing.sheet_title == "Sheet Title Example"
    assert newDrawing.sheet_number == "A1_0_7"
    assert newDrawing.discipline == "CIVIL"
    assert newDrawing.drawing_version == "As-Built"
    assert (
        newDrawing.notes
        == "Original file name was: R_G8_0034_0348_NO_0000.TIF Original drawer was: 31"
    )
    assert newDrawing.physical_location == "Original Ucsb Drawer 31"
