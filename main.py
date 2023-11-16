from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from flask import request, session
import sqlite3
from wtforms.validators import InputRequired


app = Flask(__name__)
app.static_folder='static'

app.config['SQLAICHEMY_DATABASE_URI'] = 'sqlite:///FRATS.db'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'ImageTest'

con = sqlite3.connect('FRATS.db', check_same_thread=False)
now = datetime.now()
class UploadFileForm(FlaskForm):
    file = FileField("File")
    Submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])

def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        # First grab the file
        file = form.file.data
        
    #insert database
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            img = file.read()
            # Connect to SQLite3 database and execute the INSERT
            cur = con.cursor()
            cur.execute("SELECT MAX(ID) FROM Userinfo LIMIT 1")
            ID = cur.fetchone()[0]
            cur.execute("INSERT INTO Userinfo  (ID, Name, Image, DateTimeSaved) VALUES (?, ?, ?, ?)",(ID+1, nm, img, now))
            con.commit()
            msg = "Record successfully added to database"
            
        except:
            con.rollback()
            msg = "Error in the INSERT"

    return render_template('webcam.html', form=form)
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/reset')
def reset():
    return render_template('reset.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)

