from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email

# This form used for signing up
class UserLoginForm(FlaskForm):
    first_name = StringField('First Name', validators= [DataRequired()])    
    last_name = StringField('Last Name', validators=[DataRequired()])       
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()

# This form used for signing in
class UserSigninForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()