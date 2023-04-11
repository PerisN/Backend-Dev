from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from email_validator import validate_email, EmailNotValidError
from urlshortener.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators= [DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', 
                        validators= [DataRequired(), Email(message="Invalid email address.")])
    password = PasswordField('Password',validators= [DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password',validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please login or choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username',
                            validators= [DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password',validators= [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')