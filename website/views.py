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

views = Blueprint('views', __name__)

#add note
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    restaurants=Restaurant.query.all()
    images = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png']
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user, images=images, restaurants=restaurants)

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
            style=form.style.data
        )
        db.session.add(restaurant)
        db.session.commit()
        flash('Restaurant added successfully', 'success')
        return redirect(url_for('views.home'))
    return render_template('add_restaurant.html', form=form, user=current_user)

@views.route('/restaurants')
def restaurants():
    name_filter = request.args.get('name', '')
    address_filter = request.args.get('address', '')
    style_filter = request.args.get('style', '')

    # Query the database for restaurants with optional filters
    restaurants = Restaurant.query \
        .filter(Restaurant.name.ilike(f'%{name_filter}%')) \
        .filter(Restaurant.address_line_1.ilike(f'%{address_filter}%')) \
        .filter(Restaurant.style.ilike(f'%{style_filter}%')) \
        .all()

    # Render the restaurants template with the filtered restaurants
    print(restaurants)
    return render_template('restaurants.html', restaurants=restaurants, user=current_user)


class RestaurantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired()])
    address_line_1 = StringField('Address Line 1', validators=[DataRequired()])
    address_line_2 = StringField('Address Line 2')
    number = StringField('Number', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    zipcode = StringField('Zipcode', validators=[DataRequired()])
    style = StringField('Style', validators=[DataRequired()])
