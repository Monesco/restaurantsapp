from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect, send_from_directory, current_app
from flask_login import login_required, current_user
from models import Note, Restaurant
from . import db, generate_text, generate_image, transcribe_audio, generate_speech, generate_chaos, your_friend_snoopy
import json
import time
import os
import random

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
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

    return render_template("home.html", user=current_user, images=images)


@views.route('/chaos', methods=['GET', 'POST'])
@login_required
def chaos():  
    ends = ["Explosion","Pandemic","Invasion","Apocalypse","Cataclysm","Annihilation","Extinction","Obliteration","Destruction","Collapse"] 
    if request.method == 'POST':
        text = request.form.get("text")
        if text:
            response = generate_chaos(text)    

        image = generate_image(f"Realistic, Cinematic, 8k, Real Textures, {response}")  
        final_text = generate_text(f"Generate a short back story of this character: {response} and the end of the story should be about {random.choice(ends)}")
        audio = generate_speech(final_text)
        return render_template("chaos.html", user=current_user, image=image, text=final_text, audio=audio )
    else:
        return render_template("chaos.html", user=current_user, image=None, text=None, audio=None)


@views.route('/texttos', methods=['GET', 'POST'])
def texttos():    
    if request.method == 'POST':
        text = request.form.get("text")
        response = None
        if text:
            file_name = generate_speech(text)  
            response =  f"static/audio_files/{file_name}" 
        return render_template("texttos.html", user=current_user, response=response)
    else:
        return render_template("texttos.html", user=current_user, response=None)


@views.route('/davince', methods=['GET', 'POST'])
@login_required
def index():   
    text = request.form.get("text")
    if text:
        response = generate_text(text)
    else:
        response = None
    return render_template("davince.html", user=current_user, response=response )

@views.route('/future', methods=['GET', 'POST'])
@login_required
def future():   
    text = request.form.get("text")
    if text:
        response = your_friend_snoopy(text)
    else:
        response = None
    return render_template("future.html", user=current_user, response=response )


@views.route('/dalle', methods=['GET', 'POST'])
@login_required
def dalle():
    text = request.form.get("text")
    if text:
        response = generate_image(text)
    else:
        response = None
    return render_template("dalle.html", user=current_user, response=response, text=text)


@views.route("/rev", methods=['GET','POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        transcript = transcribe_audio(f)
    else:
        transcript = None
    return render_template("rev.html", user=current_user, transcript=transcript)
    

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


@views.route('/restaurant/add', methods=['GET', 'POST'])
@login_required
def add_restaurant():
    form = RestaurantForm()
    if form.validate_on_submit():
        restaurant = Restaurant(name=form.name.data, description=form.description.data, rating=form.rating.data)
        db.session.add(restaurant)
        db.session.commit()
        flash('Restaurant added successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_restaurant.html', form=form, user=current_user)

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired

class RestaurantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired()])