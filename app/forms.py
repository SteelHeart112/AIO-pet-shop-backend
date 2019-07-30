from wtforms import StringField, PasswordField, SubmitField, ValidationError, TextField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired
from app.models import User
from flask_wtf import FlaskForm


class RegistrationForm (FlaskForm):
    class Meta:
        csrf = False
    email = StringField("Email", validators=[DataRequired(), Length(min=4, max=100)])
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField("password", validators=[DataRequired(), Length(min=6, max=25), EqualTo("pass_confirm")])
    pass_confirm = PasswordField("Confirm password", validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered!!")


class LoginForm (FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])