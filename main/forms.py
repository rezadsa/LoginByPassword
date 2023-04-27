from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from main.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):

    username=StringField('Username',validators=[DataRequired(),Length(min=4,max=30)])
    email=EmailField('Email',validators=[DataRequired(),Email(message='Please Enter Valid Email Address')])
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('confirm',message='Passwords must be Match ')])
    confirm=PasswordField('Confirm Password')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This Username Already Exists   ')
        
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This Email Already Exists  ')
        

class UpdateForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=4,max=30)])
    email=EmailField('Email',validators=[DataRequired(),Email(message='Please Enter Valid Email Address')])
    

    def validate_username(self,username):
        if current_user.username!=username.data:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This Username Already Exists  ')

    def validate_email(self,email):
        if current_user.email!=email.data:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This Email Address Already Exists  ')

class LoginForm(FlaskForm):

    email=EmailField('Email',validators=[DataRequired(),Email(message='Please Enter Valid Email Address')])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    


class PostForm(FlaskForm):

    title=StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])

  
