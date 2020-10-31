from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quote:
    '''
    Quote class to define Quote Objects
    '''
    def __init__(self,quote,author):
        self.quote = quote
        self.author = author

class User(UserMixin,db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index =True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    blogs = db.relationship('Blog', backref= 'user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'This user is {self.username}'
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

class PhotoProfile(db.Model):
    __tablename__='profile_photos'
    id = db.Column(db.Integer,primary_key=True)
    pic_path = db.Column(db.String())
    user_id= db.Column(db.Integer,db.ForeignKey("users.id"))


class Blog(db.Model):
    __tablename__= 'blogs'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(255))
    blog = db.Column(db.String(), index= True)
    comments = db.relationship('Comment', backref='blog', lazy='dynamic')

    def __repr__(self):
        return f'Title: {self.title}'

class Comment(db.Model):
    __tablename__='comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))

    def __repr__(self):
        return f'Comment: {self.comment}'
