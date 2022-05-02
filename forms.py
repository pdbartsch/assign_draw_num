from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField, DateField)
from wtforms.validators import InputRequired, Length, DataRequired
from datetime import datetime


class ProjectForm(FlaskForm):
    locnum = IntegerField('Location Number', validators=[InputRequired()])
    drawnum = IntegerField('Drawing Number', validators=[InputRequired()])
    contractnum = StringField('Contract Number', validators=[Length(max=50)])
    projectnum = StringField('Project Number', validators=[Length(max=10)])
    projectmngr = StringField('Project Manager', validators=[InputRequired(), Length(min=3, max=100)])
    mainconsult = StringField('Consultant', validators=[InputRequired(), Length(min=3, max=100)])
    title = StringField('Project Name', validators=[InputRequired(), Length(min=10, max=100)])
    comments = TextAreaField('Comments', validators=[Length(max=200)])
    daterecorded = DateField('Date of Record', format='%d.%m.%Y', default=datetime.today(), validators=[DataRequired()])

class LocationForm(FlaskForm):
    locnum = IntegerField('Location Number', validators=[InputRequired()])
    locdescrip = StringField('Location Name', validators=[InputRequired(), Length(min=8, max=100)])


# # in form field specific custom validator:
# class FourtyTwoForm(Form):
#     num = IntegerField('Number')

#     def validate_num(form, field):
#         if field.data != 42:
#             raise ValidationError('Must be 42')