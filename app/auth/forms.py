from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import ValidationError,DataRequired,Email,EqualTo
from app.models import User

class LoginForm(FlaskForm):
    useremail = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    rememberme = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(),Email()])
    firstname=StringField('First Name',validators=[DataRequired()])
    lastname=StringField('Last Name',validators=[DataRequired()])
    address1=StringField('Address1',validators=[DataRequired()])
    address2=StringField('Address2')
    city=StringField('City',validators=[DataRequired()])
    state=StringField('State',validators=[DataRequired()])
    zipcode=StringField('Zip Code',validators=[DataRequired()])
    submit=SubmitField('Submit')


class RegistrationForm(FlaskForm):
    useremail=StringField('Email', validators=[DataRequired(),Email()])
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname =StringField('Last Name',validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password1')])
    address1 = StringField('Address', validators=[DataRequired()])
    address2 = StringField('Address2')
    city = StringField('City',validators=[DataRequired()])
    state=StringField('State', validators=[DataRequired()])
    zipcode=StringField('Zip',validators=[DataRequired()])
    submit = SubmitField('Register')


    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email Address has been registered')

class ResetPasswordRequestForm(FlaskForm):
    useremail = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

class ResetEmailForm(FlaskForm):
    oldEmail = StringField('Current Email', validators=[DataRequired(),Email()])
    newEmail = StringField('New Email',validators=[DataRequired(),Email()])
    newEmail2=StringField('Verified Email', validators=[DataRequired(),Email(),EqualTo('newEmail')])
    submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    oldpassword = PasswordField('Current Password',validators=[DataRequired()])
    newpassword = PasswordField('New Password', validators=[DataRequired()])
    newpassword2 = PasswordField('Repeat New Password',validators=[DataRequired(),EqualTo('newpassword')])
    submit = SubmitField('Submit')






