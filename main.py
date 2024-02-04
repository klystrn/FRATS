from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from flask import request, session
import sqlite3
from wtforms.validators import InputRequired
import cv2, face_recognition
import random

app = Flask(__name__)
app.static_folder='static'


app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'ImageTest'

con = sqlite3.connect('FRATS.db', check_same_thread=False)
now = datetime.now()
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    Submit = SubmitField("Upload File")

def find_face_encodings(image_path):
    #reading img
    image = cv2.imread(image_path)
    #get face encoding from the image
    face_enc = face_recognition.face_encodings(image)
    return face_enc[0]

@app.route('/webcam', methods=['GET',"POST"])
def webcam():
    if "UserName" not in session:
        return render_template('index.html')
    form = UploadFileForm()
    form2 = UploadFileForm()
    if form.validate_on_submit():
        # First grab the file
        file = form.file.data
        file2 = form2.file.data
        submit = SubmitField("Upload File")
        img = file.read()
        path = os.path.join(".\\", app.config["UPLOAD_FOLDER"],secure_filename(f"image_{random.randint(1000000000,9999999999)}.png"))
        f = open(path, 'wb')
        f.write(img)
        f.close()
        faceobj = face_recognition.load_image_file(path)
        encode = face_recognition.face_encodings(faceobj)
        #if len(encode) == 0:
        #    error = "No face detected."
        #    return render_template('webcam.html', form = form)

    #insert database
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            #nm = request.form['nm']

            username = session["UserName"]
            # Connect to SQLite3 database and execute the INSERT
            cur = con.cursor()
            #cur.execute("SELECT MAX(ID) FROM Userinfo LIMIT 1")
            #ID = cur.fetchone()[0]
            #if (ID is None):
            #   ID = 0
            
            cur.execute("INSERT INTO Image  (UserName, Image, DateTimeSaved) VALUES (?, ?, ?)",( username, img, now))
            con.commit()
            ImageID = cur.lastrowid
            print(len(str(encode)))
            print(str(encode))
            cur.execute("INSERT INTO OpenCV  (ImageID, Encoding) VALUES (?, ?)",( ImageID, str(encode)))
            con.commit()
            #con.close()
            flash("Successfully upload", "success")
            msg = "Record successfully added to database"
            session["UserName"] = username
            
        except:
            con.rollback()
            msg = "Error in the INSERT"

    return render_template('webcam.html', form=form)

@app.route('/sp', methods=['GET', 'POST'])
def sp():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['npw']
        email = request.form['uemail']
        name = request.form['name']

        # Validate the user's input
        if not username or not password or not email:
            error = "Please enter all required fields."
            return render_template('signup.html', error=error)

        # Create a new user account in the database
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO RegUser (UserName, Password, Email, RealName) VALUES (?, ?, ?, ?)", (username, password, email, name))
            con.commit()
            #con.close()
            success = "Account created successfully."
            flash("Successfully sign up", "success")
            return render_template('signup.html', success=success)
        except:
            error = "An error occurred while creating your account."
            return render_template('signup.html', error=error)

    return render_template('signup.html')

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        username = request.form['una']
        password = request.form['upass']

        cursor = con.cursor()

        cursor.execute('SELECT * FROM RegUser WHERE UserName = ?', (username,))
        user = cursor.fetchone()
        #con.close()

        if user:
            if user[1] == password and user[0] ==username:
                session["UserName"] = username
                return redirect(url_for('webcam'))
            else:
                flash("Wrong username or password!", "warning")
                error = 'Invalid password'
        else:
            flash("Wrong username or password!", "warning")
            error = 'Username not found'

    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/')

@app.route('/index')
def index():
    session.clear()
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

@app.route('/attendance')

def attendance():
    return render_template('attendance.html',p1 = "100", p2 = "100")

@app.route('/card_id')
def card_id():
    return render_template('card_id.html')

@app.route('/view')
def view():
    return render_template('view.html')

if __name__ == '__main__':
    app.run(debug=True)

#session.pop("UserName",default=None) for log out