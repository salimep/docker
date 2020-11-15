from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app=Flask(__name__)

app.config['SECRET_KEY']='e5254aaa360ce60d2c6ad5bf515f7ec7'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

mysql_host=os.environ.get('mysql_host')
mysql_user=os.environ.get('mysql_user')

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://'+mysql_user+':salim123@'+mysql_host+'/blog'


db=SQLAlchemy(app)

bcrypt=Bcrypt(app)
LoginManager=LoginManager(app)
LoginManager.login_view ='login'
LoginManager.login_message_category='info'

#from blog import route



