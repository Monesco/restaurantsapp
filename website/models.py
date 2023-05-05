from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from .restaurant_seed import restaurant_seed_list



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id=db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    rating = db.Column(db.Float)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class User_Favorites(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
    favorite = db.Column(db.Boolean, default=False)


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
    totalReviews = db.Column(db.Float)
    reviews=db.relationship('Note')

class Restaurant_Images(db.Model):
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
    thumbnail_image = db.Column(db.String(100))
    menu_image = db.Column(db.String(100))
    restaurant = db.relationship('Restaurant', backref='images')



def Restaurant_seed():
    count = 0
    for restaurant_data in restaurant_seed_list:
        print("restraunt list accessed")
        print(restaurant_data)
        # Add the restaurant to the main table
        restaurant = Restaurant(
            name= restaurant_data[0],
            description= restaurant_data[1],
            rating= int(restaurant_data[2]),
            address_line_1= restaurant_data[3],
            number= restaurant_data[4],
            city= restaurant_data[5],
            state= restaurant_data[6],
            country= restaurant_data[7],
            zipcode= restaurant_data[8],
            style= restaurant_data[9],
            totalReviews=restaurant_data[12]     
        )
        db.session.add(restaurant)
        db.session.commit()

        # Add the images to the images table, if they exist
        images = Restaurant_Images(
            restaurant_id = restaurant.id,
            thumbnail_image = restaurant_data[10],
            menu_image = restaurant_data[11]
        )
        db.session.add(images)
        db.session.commit()