from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SelectField,
)
from wtforms.validators import (
    InputRequired,
    Length,
    NumberRange,
    Optional,
)


class DrawingsForm(FlaskForm):
    oldname = StringField(label="Old Name", validators=[Optional()])
    newname = StringField(label="File Name", validators=[InputRequired()])
    locnum = IntegerField(label="Location Number", validators=[InputRequired()])
    drawnum = IntegerField(label="Drawing Number", validators=[InputRequired()])
    project_title = StringField(
        "Project Title", validators=[InputRequired(), Length(min=10, max=150)]
    )
    project_number = StringField(
        label="Project Number", validators=[Length(max=40), Optional()]
    )
    project_year = IntegerField(
        label="Project Year",
        validators=[NumberRange(min=1900, max=2100, message="Four Integer Year")],
    )
    sheet_title = StringField(
        label="Sheet Title", validators=[InputRequired(), Length(min=10, max=150)]
    )
    sheet_number = StringField(
        label="Sheet Number", validators=[InputRequired(), Length(min=1, max=10)]
    )
    discipline = SelectField(
        label="Drawing Discipline",
        choices=[
            ("", ""),
            ("arch", "Architectural"),
            ("struct", "Structural"),
            ("mech", "Mechanical"),
            ("plumb", "Plumbing"),
            ("elect", "Electrical"),
            ("life_safe", "Life Safety"),
            ("civil", "Civil"),
            ("title", "Title Sheet"),
            ("shop", "Shop Drawings"),
            ("other", "Other"),
        ],
        validators=[InputRequired()],
    )
    drawing_version = SelectField(
        label="Drawing Version",
        choices=[
            ("", ""),
            ("bid", "Bid"),
            ("partial_construct", "Partial Construction"),
            ("full_construct", "100% Construction"),
            ("asbuilt", "As-Built"),
            ("record", "Record"),
        ],
        validators=[InputRequired()],
    )
    notes = StringField(label="Notes", validators=[Optional()])


class DrawingsSearchForm(FlaskForm):
    locnum = IntegerField(label="Location Number", validators=[Optional()])
    drawnum = IntegerField(label="Drawing Number", validators=[Optional()])
    project_title = StringField(
        "Project Title", validators=[Length(max=150), Optional()]
    )
    sheet_title = StringField(
        label="Sheet Title", validators=[Length(max=150), Optional()]
    )
    sheet_number = StringField(
        label="Sheet Number", validators=[Length(max=10), Optional()]
    )
    discipline = SelectField(
        label="Drawing Discipline",
        choices=[
            ("", ""),
            ("arch", "Architectural"),
            ("struct", "Structural"),
            ("mech", "Mechanical"),
            ("plumb", "Plumbing"),
            ("elect", "Electrical"),
            ("life_safe", "Life Safety"),
            ("civil", "Civil"),
            ("title", "Title Sheet"),
            ("shop", "Shop Drawings"),
            ("other", "Other"),
        ],
        validators=[Optional()],
    )
