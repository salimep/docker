from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import data_required,email,length,EqualTo,ValidationError
from blog.model import User,Post
from flask_wtf.file import  FileField,FileAllowed,FileRequired
from wtforms.widgets import TextArea
from wtforms import form

from flask_login import current_user

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[data_required(),length(min=3,max=10)])
    email=StringField('Email',validators=[data_required(),email()])
    password=PasswordField("password",validators=[data_required(),EqualTo('conform')])
    conform=PasswordField("conform",validators=[data_required()])
    submit=SubmitField("sign UP")
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('user already exist ')

    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('mail id already exist ')





class LoginForm(FlaskForm):
    username = StringField('Username', validators=[data_required()])
    password = PasswordField("PassWord", validators=[data_required()])
    remember=BooleanField("rememember me")
    submit=SubmitField("sign in")



class UpdateForm(FlaskForm):
    username=StringField('Username',validators=[data_required(),length(min=3,max=10)])
    email=StringField('Email',validators=[data_required(),email()])
    image=FileField("upload picture",validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField("update")
    def validate_username(self,username):
        if current_user.username != username.data:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('user already exist ')

    def validate_email(self,email):
        if current_user.email != email.data:
            email=User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('mail id already exist ')



class new_post(FlaskForm):

    title=StringField('Title',validators=[data_required()])
    content=StringField('content',widget=TextArea())
    submit = SubmitField("add new post")

    def validate_title(self,username):
        title=Post.query.filter_by(title=username.data).first()
        if title:
            raise ValidationError('Title already exist ')



class update_post(FlaskForm):
    title=StringField('Title',validators=[data_required()])
    content=StringField('content',widget=TextArea())
    submit = SubmitField("update post")
