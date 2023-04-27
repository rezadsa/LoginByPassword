from main import db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    email=db.Column(db.String(60),nullable=True,unique=True)
    password=db.Column(db.String(60),nullable=True)

    post=db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id},{self.username},{self.email})'
    

class Post(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255),nullable=False)
    date=db.Column(db.Date,nullable=False,default=datetime.now)
    content=db.Column(db.Text,nullable=False)

    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.title[:30]},{self.date})'