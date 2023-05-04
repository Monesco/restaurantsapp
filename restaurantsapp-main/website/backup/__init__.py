from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import openai
from rev_ai import apiclient
from gtts import gTTS
import hashlib
import os
import time
import random



Google_cloud_api_key = "AIzaSyB6gUFl7KOsbG47htNd3u7ctcFBoIPJXiE"
db = SQLAlchemy()
DB_NAME = "database.db"


openai.api_key = "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"

rev_token = "02fLKDyaWF972paFVZDzbcAJ4hZiAj6_RbJ5Ih_9-FyJTjaizosz5xn5j2pcFX7JNFljlS9asiTEb9nhRy1y53QpVmxe8"
rev_client = apiclient.RevAiAPIClient(rev_token)





#future teller function
def your_friend_snoopy(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"The AI is inpersonating Snoop Dogg and answer the questions rapping and adding weed everywhere. The AI answers the following question from the human:{prompt}",
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.8,
    )
                     

    message = completions.choices[0].text
    return message


#speech generator
def generate_speech(prompt):
    text = prompt
    voices = ["co.za", "ie", "co.in", "com.au"]   
    tts = gTTS(text=text, lang='en', tld=random.choice(voices))
    file_name = f"{random.randint(100,999)}.mp3"
    directory = f"{current_app.root_path}/static/audio_files/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = directory + file_name
    print("Saving audio file to: " + file_path)
    try:
        tts.save(file_path)        
    except Exception as e:
        print(f"An error occurred while saving the audio file: {e}")

    return file_name


#chaotic character generator
def generate_chaos(texto):
    chaotic_words = ["turmoil", "disorder", "anarchy", "bedlam", "chaos", "confusion", "mayhem", "havoc", "upheaval", "unrest"]
    completions = openai.Completion.create(
        engine="text-davinci-003",        
        prompt= f"Generate a short and descriptive physical description of a chaotic: {texto}, the prompt must contain the word: {random.choice(chaotic_words)} ",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.3,
    )

    message = completions.choices[0].text
    return message
    

#text generator
def generate_text(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message


#img generator
def generate_image(prompt):
    completions = openai.Image.create(        
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    image_url = completions['data'][0]['url']
    return image_url


#audio transcription
def transcribe_audio(audio_file):
    job = rev_client.submit_job_local_file(audio_file)
    transcript = rev_client.get_transcript_text(job.id)
    return transcript


#creating app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
 
    from models import User, Note

    with app.app_context():
       create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))   

    return app


#creating database
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')

