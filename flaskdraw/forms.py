from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    PasswordField,
    DateField,
    BooleanField,
    SubmitField,
    FileField,
)
from wtforms.validators import (
    InputRequired,
    Length,
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
)
from datetime import datetime

from flask_login import current_user
from flaskdraw.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )

    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )

    submit = SubmitField("Sign Up")

    # create custom validation to ensure unique user name and email
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        # if user exists
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # if user exists
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

    # create custom validation to ensure unique user name and email
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            # if user exists
            if user:
                raise ValidationError(
                    "That username is taken. Please choose a different one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            # if user exists
            if user:
                raise ValidationError(
                    "That email is taken. Please choose a different one."
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
    daterecorded = DateField(
        "Date of Record",
        format="%d.%m.%Y",
        default=datetime.today(),
        validators=[DataRequired()],
    )


class LocationForm(FlaskForm):
    locnum = IntegerField("Location Number", validators=[InputRequired()])
    locdescrip = StringField(
        "Location Name", validators=[InputRequired(), Length(min=8, max=100)]
    )


# # in form field specific custom validator:
# class FourtyTwoForm(Form):
#     num = IntegerField('Number')

#     def validate_num(form, field):
#         if field.data != 42:
#             raise ValidationError('Must be 42')
