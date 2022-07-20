from enum import unique
from flask_login import UserMixin
from stockchart import db,login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(20),unique=False,nullable=False)
    lastname = db.Column(db.String(20),unique=False,nullable=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable = False)
    # stocks = db.relationship('Stock',backref='buy',lazy=True)  
    
    def __repr__(self):
        return f"User('{self.image_file}','{self.firstname}','{self.lastname}','{self.username}','{self.email}')"

class Stock(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    symbol = db.Column(db.String(10),nullable=False,unique=True)
    price = db.Column(db.String(100),nullable=False)
    percent_change = db.Column(db.Text,nullable = False)
    
    def __repr__(self):
        return f"Post('{self.price}','{self.symbol}','{self.percent_change}')"