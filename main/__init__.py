from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///../test.db'
app.config['SECRET_KEY']='598a6265c3977c69873bcc44e737bf414891ac24a7a8aba7'

db=SQLAlchemy(app)

bcrypt=Bcrypt(app)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message='You have to login to access this page'
login_manager.login_message_category=['info',' ']




from main.models import db as data_base
with app.app_context():
    data_base.create_all()




from main import routes