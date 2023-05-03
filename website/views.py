from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect, send_from_directory, current_app
from flask_login import login_required, current_user
from .models import Note, Restaurant  # import the Restaurant model
from . import db
import json
import time
import os
import random
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired
from .forms import RestaurantForm

views = Blueprint('views', __name__)

#add note
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    restaurants=Restaurant.query.all()
    return render_template("home.html", user=current_user, restaurants=restaurants)

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
        flash('Restaurant added successfully', 'success')
        return redirect(url_for('views.home'))
    return render_template('add_restaurant.html', form=form, user=current_user)

@views.route('/restaurants')
def restaurants():
    name_filter = request.args.get('Name', '')
    city_filter = request.args.get('City', '')
    style_filter = request.args.get('Style', '')
    rating_filter = request.args.get('Rating','')

    # Query the database for restaurants with optional filters
    restaurants = Restaurant.query \
        .filter(Restaurant.name.ilike(f'%{name_filter}%')) \
        .filter(Restaurant.city.ilike(f'%{city_filter}%')) \
        .filter(Restaurant.style.ilike(f'%{style_filter}%')) \
        .filter(Restaurant.rating.ilike(f'%{rating_filter}'))\
        .all()

    # Render the restaurants template with the filtered restaurants
    print(restaurants)
    return render_template('restaurants.html', restaurants=restaurants, user=current_user)



