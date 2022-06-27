from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    DateField,
)
from wtforms.validators import (
    InputRequired,
    Length,
    DataRequired,
    Optional,
)



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


class ProjectSearchForm(FlaskForm):
    lnum = IntegerField("Location Number", validators=[Optional()])
    drawnum = IntegerField("Drawing Number", validators=[Optional()])
    projectmngr = StringField(
        "Project Manager", validators=[Optional(), Length(max=100)]
    )
    mainconsult = StringField(
        "Consultant", validators=[Optional(), Length(max=100)]
    )
    title = StringField(
        "Project Name", validators=[Optional(), Length(max=100)]
    )
