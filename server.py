from flask import Flask, render_template, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from werkzeug.utils import secure_filename
import os
import speech_recognition as sr
from pydub import AudioSegment
from collections import defaultdict

from model import db, connect_to_db, User

import nlp

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/emplify'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['wav','m4a'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route('/upload')
def process_speech():
    #get request audio file
    #request.body.get
    #wav_file = request.args.get(‘content’, 0, type=str) 
    wav_file = "test.wav"
    watson_json= transcibe_watson(wav_file)
    df = makeDFfromJson(watson_json)
    speaker_dict = retreiveSpeakerInfoAsDict(df)
    for speaker in speaker_dict:
        
        speaker["name"]=get_name_from_first_sentence(sentences)
        if speaker["name"]==None:
               speaker["name"]==speaker
                
        speaker["top_cats"] = get_semantic_categories(sentences)
    
    #save speaker_dict to file
    return jsonify(speaker_dict=speaker_dict)

    
@app.route('/names')
def get_names(string):
    count = 0
    speaker_dict = defaultdict(str)
    while get_name_from_first_sentence(string):
        speaker_dict[count] = get_name_from_first_sentence(string)
        count += 1
    return speaker_dict

@app.route('/results')
def get_results():

# Set "homepage" to index.html
@app.route('/')
def index():
    print (nlp.to_spacy_doc())
    print (nlp.to_textacy_doc())
    return render_template('index.html')

# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        r = sr.Recognizer()
        if filename.rsplit('.', 1)[1].lower() == 'm4a':
            m4_audio = AudioSegment.from_file(app.config['UPLOAD_FOLDER']+filename, format="m4a")
            m4_audio.export("sound_file.wav", format="wav")
            filename = "sound_file.wav"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with sr.WavFile(filename) as source:
                    audio = r.record(source)
        else:
            with sr.WavFile(app.config['UPLOAD_FOLDER']+filename) as source:
                    audio = r.record(source)

        try:
            flash("Transcription: " + r.recognize_google(audio))
        except LookupError:
            flash("Could not understand audio")
    return render_template('index.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.debug = True
    app.run()
