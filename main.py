from flask import Flask, render_template, redirect, url_for, session, request, flash
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
    file = FileField("File", validators=[InputRequired()])
    Submit = SubmitField("Upload File")

@app.route('/webcam', methods=['GET',"POST"])

def webcam():
    form = UploadFileForm()
    form2 = UploadFileForm()
    if form.validate_on_submit():
        # First grab the file
        file = form.file.data
        file2 = form2.file.data
        submit = SubmitField("Upload File")
        img = file.read()
        file2.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config["UPLOAD_FOLDER"],secure_filename(file2.filename)))
        
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
            flash("Successfully upload", "success")
            msg = "Record successfully added to database"
            
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
            conn = sqlite3.connect('FRATS.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO RegUser (UserName, Password, Email, RealName) VALUES (?, ?, ?, ?)", (username, password, email, name))
            conn.commit()
            conn.close()
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

        connection = sqlite3.connect('FRATS.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM RegUser WHERE UserName = ?', (username,))
        user = cursor.fetchone()
        connection.close()

        if user:
            if user[1] == password:
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

if __name__ == '__main__':
    app.run(debug=True)

#session.pop("UserName",default=None) for log out