from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField
)
from wtforms.validators import (
    InputRequired,
    Length
)



class LocationForm(FlaskForm):
    locnum = IntegerField("Location Number", validators=[InputRequired()])
    locdescrip = StringField(
        "Location Name", validators=[InputRequired(), Length(min=8, max=100)]
    )

