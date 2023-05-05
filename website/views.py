from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect, send_from_directory, current_app
from flask_login import login_required, current_user
from .models import User, Note, Restaurant, Restaurant_Images, User_Favorites, Restaurant_seed  # import the Restaurant model
from . import db
from sqlalchemy.sql import func
import json
import time
import os
import random
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired
from .forms import RestaurantForm, ReviewForm
from sqlalchemy.orm.exc import NoResultFound

views = Blueprint('views', __name__)

#add note
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    restaurants=Restaurant.query.all()
    restaurant_images = Restaurant_Images.query.all()

    if restaurants == [] or restaurant_images == []:
        Restaurant_seed()
        restaurants=Restaurant.query.all()
        restaurant_images = Restaurant_Images.query.all()


    # Get the current user's favorite restaurants
    favorite_restaurants = User_Favorites.query.filter_by(user_id=current_user.id, favorite=True).all()
    favorite_restaurant_ids = [favorite.restaurant_id for favorite in favorite_restaurants]

    return render_template("home.html", user=current_user, restaurants=restaurants, restaurant_images=restaurant_images, favorite_restaurant_ids=favorite_restaurant_ids)

#remove note
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

#admin page to add restaurant
@views.route('/restaurant/add', methods=['GET', 'POST'])
@login_required
def add_restaurant():
    form = RestaurantForm()
    if form.validate_on_submit():
        # create new restaurant
        restaurant = Restaurant(
            name=form.name.data,
            description=form.description.data,
            rating=form.rating.data,
            address_line_1=form.address_line_1.data,
            address_line_2=form.address_line_2.data,
            number=form.number.data,
            city=form.city.data,
            state=form.state.data,
            country=form.country.data,
            zipcode=form.zipcode.data,
            style=form.style.data,
            totalReviews=form.totalReviews.data
        )
        db.session.add(restaurant)
        db.session.commit()
        restaurant_images=Restaurant_Images(
            restaurant_id=restaurant.id,
            thumbnail_image=form.thumbnail_url.data,
            menu_image=form.menu_url.data
        )
        db.session.add(restaurant_images)
        db.session.commit()
        flash('Restaurant added successfully', 'success')
        return redirect(url_for('views.home'))
    return render_template('add_restaurant.html', form=form, user=current_user)

@views.route('/restaurants')
def restaurants():
    name_filter = request.args.get('name', '')
    city_filter = request.args.get('city', '')
    style_filter = request.args.get('style', '')
    rating_filter = request.args.get('rating','')

    # Query the database for restaurants with optional filters
    restaurants = Restaurant.query \
        .filter(Restaurant.name.ilike(f'%{name_filter}%')) \
        .filter(Restaurant.city.ilike(f'%{city_filter}%')) \
        .filter(Restaurant.style.ilike(f'%{style_filter}%')) \
        .filter(Restaurant.rating.ilike(f'%{rating_filter}%'))\
        .all()

    # Render the restaurants template with the filtered restaurants
    print(restaurants)
    return render_template('restaurants.html', restaurants=restaurants, user=current_user)

#restaurant specifics
@views.route('/restaurant/<int:restaurant_id>')
def restaurant_specifics(restaurant_id):

    # Query the database for restaurants with optional filters
    restaurant = Restaurant.query.get(restaurant_id)
    restaurant_images = Restaurant_Images.query.get(restaurant_id)

    user_id = current_user.id if current_user.is_authenticated else None
    favorite = None
    if user_id:
        # Try to find the user's favorite for the current restaurant
        favorite = User_Favorites.query.filter_by(user_id=user_id, restaurant_id=restaurant.id).first()
    if request.method == 'POST':
        if not favorite:
            # If the user's favorite doesn't exist yet, create it
            favorite = User_Favorites(user_id=user_id, restaurant_id=restaurant.id, favorite=True)
            db.session.add(favorite)
        else:
            # Toggle the favorite value
            favorite.favorite = not favorite.favorite
        db.session.commit()

    users=User.query.all()
    notes = Note.query.all()

    return render_template('restaurant_specifics.html', restaurant=restaurant, restaurant_images = restaurant_images, favorite=favorite, user=current_user, notes=notes,users=users)

@views.route('/toggle_favorite/<int:user_id>/<int:restaurant_id>')
@login_required
def toggle_favorite(user_id, restaurant_id):
    try:
        favorite = User_Favorites.query.filter_by(user_id=user_id, restaurant_id=restaurant_id).one()
        favorite.favorite = not favorite.favorite
        db.session.commit()
        return jsonify({'is_favorite': favorite.favorite})
    except NoResultFound:
        favorite = User_Favorites(user_id=user_id, restaurant_id=restaurant_id, favorite=True)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'is_favorite': True})


@views.route('/user_profile')
@login_required
def user_profile():
    user = current_user
    user_favorites = db.session.query(Restaurant).join(User_Favorites)\
        .filter(User_Favorites.user_id == current_user.id, User_Favorites.favorite == True)\
        .all()
    restaurant_images = Restaurant_Images.query.all()
    return render_template('user_profile.html', user=user, user_favorites=user_favorites, restaurant_images = restaurant_images)

@views.route('/restaurant/<int:restaurant_id>/review', methods=['GET', 'POST'])
def writeReview(restaurant_id):
    form = ReviewForm()
    restaurant=Restaurant.query.get(restaurant_id)
    if form.validate_on_submit():
        review=Note(
            data=form.reviewText.data,
            date=func.now(),
            user_id=current_user.id,
            restaurant_id=restaurant_id,
            rating=form.rating.data
        )
        db.session.query(Restaurant).filter(Restaurant.id==restaurant_id).update({'rating':(((Restaurant.rating)*(Restaurant.totalReviews)+review.rating)/(Restaurant.totalReviews+1))})
        db.session.query(Restaurant).filter(Restaurant.id==restaurant_id).update({'totalReviews':Restaurant.totalReviews+1})
        db.session.add(review)
        db.session.commit()
        flash('Review added successfully', 'success')
        return redirect(url_for('views.home'))
    return render_template('review.html',restaurant=restaurant, user=current_user, form=form)
