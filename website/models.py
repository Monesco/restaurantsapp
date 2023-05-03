from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    rating = db.Column(db.Float)
    address_line_1 = db.Column(db.String(100))
    address_line_2 = db.Column(db.String(100))
    number = db.Column(db.String(20))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    zipcode = db.Column(db.String(20))
    style = db.Column(db.String(100))
    
class Restaurant_Images(db.Model):
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
    thumbnail_image = db.Column(db.String(100))
    menu_image = db.Column(db.String(100))
    restaurant = db.relationship('Restaurant', backref='images')