from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    DateField,
    SubmitField,
    SelectField
)
from wtforms.validators import (
    InputRequired,
    Length,
    DataRequired,
    NumberRange,
    Optional
)


class DrawingsForm(FlaskForm):
    oldname = StringField(label="Old Name", validators=[Optional()])
    newname = StringField(label="New Name", validators=[InputRequired()])
    locnum = IntegerField(label="Location Number", validators=[InputRequired()])
    drawnum = IntegerField(label="Drawing Number", validators=[InputRequired()])
    project_title = StringField(
        "Project Title", validators=[InputRequired(), Length(min=10, max=150)]
    )
    project_number = StringField(label="Project Number", validators=[Length(max=40), Optional()])
    project_year = IntegerField(label="Project Year", validators=[NumberRange(min=1900, max=2100, message="Four Integer Year")])
    sheet_title = StringField(
        label="Sheet Title", validators=[InputRequired(), Length(min=10, max=150)]
    ) 
    sheet_number = StringField(
        label="Sheet Number", validators=[InputRequired(), Length(min=1, max=10)]
    )
    discipline = SelectField(label=u'Drawing Discipline', 
        choices=[('arch', 'Architectural'), ('struct', 'Structural'), ('mech', 'Mechanical'), ('plumb', 'Plumbing'), 
        ('elect', 'Electrical'), ('life_safe', 'Life Safety'), ('civil', 'Civil'), ('title', 'Title Sheet'), 
        ('shop', 'Shop Drawings'),('other', 'Other')],
        validators=[InputRequired()]
    )
    drawing_version = SelectField(label=u'Drawing Version', 
        choices=[('bid', 'Bid'), ('partial_construct', 'Partial Construction'), ('full_construct', '100% Construction'), 
        ('asbuilt', 'As-Built'), ('record', 'Record')],
        validators=[InputRequired()]
    )
    notes = StringField(label="Notes", validators=[Optional()])


class ProjectForm(FlaskForm):
    locnum = IntegerField("Location Number", validators=[InputRequired()])
    drawnum = IntegerField("Drawing Number", validators=[InputRequired()])
    contractnum = StringField("Contract Number", validators=[Length(max=50)])
    projectnum = StringField("Project Number", validators=[Length(max=10)])
    projectmngr = StringField(
        "Project Manager", validators=[InputRequired(), Length(min=3, max=100)]
    )
    mainconsult = StringField(
        "Consultant", validators=[InputRequired(), Length(min=3, max=100)]
    )
    title = StringField(
        "Project Name", validators=[InputRequired(), Length(min=10, max=100)]
    )
    comments = TextAreaField("Comments", validators=[Length(max=200)])
    daterecorded = DateField(validators=[DataRequired()])


class LocationForm(FlaskForm):
    locnum = IntegerField("Location Number", validators=[InputRequired()])
    locdescrip = StringField(
        "Location Name", validators=[InputRequired(), Length(min=8, max=100)]
    )


class SearchForm(FlaskForm):
    lnum = IntegerField("Location Number", validators=[InputRequired()])
    searched = StringField("Searched", validators=[InputRequired()])
    submit = SubmitField("Submit")
