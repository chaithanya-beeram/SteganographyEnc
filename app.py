import os
from flask import Flask, flash, request, redirect, url_for, render_template, make_response, session
from functools import wraps, update_wrapper
from werkzeug.utils import secure_filename
from werkzeug.http import http_date
from datetime import datetime
import pymongo
import bcrypt
import urllib

import stega
import algo

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
#set app as a Flask instance 
app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#encryption relies on secret keys so they could be run
app.secret_key = "testing"
#connoct to your Mongo DB database
mongo_uri = "mongodb+srv://SteganoSatya:" + urllib.parse.quote("Bput@035") + "@cluster0.ommm3.mongodb.net/test?authSource=admin&replicaSet=atlas-e6c8s7-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
client = pymongo.MongoClient(mongo_uri)

#get the database name
db = client.get_database('users')
#get the particular collection that contains the data
records = db.register

#assign URLs to have a particular route 
@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed}
            #insert it in the record collection
            records.insert_one(user_input)
            
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            return render_template('startEncoding.html', email=new_email)
    return render_template('index.html')



@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("startEncoding"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('startEncoding'))
            else:
                if "email" in session:
                    return redirect(url_for("startEncoding"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('startEncoding.html', email=email)
    else:
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')


@app.route("/decode")
def decode():
    return render_template("decode.html")

@app.route("/encode")
def encode():
    return render_template("encode.html")

@app.route("/updateEncode", methods = ['POST'])
def updateEncode():
    UPLOAD_FOLDER = "static/images"

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        file = request.files['input']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename("Cristi2.png")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("success.html")
    else:
        return render_template("error.html")

@app.route("/updateDecode", methods = ['POST'])
def updateDecode():
    UPLOAD_FOLDER = "static/images"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        file = request.files['input']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename("Cristi2.png")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_address = UPLOAD_FOLDER + "/" + "Cristi2.png"
            text = stega.decode(image_address)
            opt = text.split(" -")
            if opt[0] == "-c":
                delay = opt[1]
                text = opt[2]
                text = algo.caesarDecode(text, int(delay))
                return render_template("finalDecode.html", text = text)
            if opt[0] == "-v":
                delay = opt[1]
                text = opt[2]
                text = algo.vigenereDecode(text, delay)
                return render_template("finalDecode.html", text = text)
            else:
                return render_template("finalDecode.html", text = text)
    else:
        return render_template("error.html")

@app.route("/final", methods = ['POST'])
def finalEncode():
    address = "static/images/Cristi2.png"
    UPLOAD_FOLDER = "static/images"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        text = request.form['text']
        cipher = request.form['crypto']

        if(cipher == 'vigenere'):
            delay = request.form['delay']
            text = "-v " + "-" + delay + " -" + text
            text = algo.vigenereEncode(text,delay)
        if(cipher == 'caesar'):
            delay = request.form['delay']
            text = "-c " + "-" + delay + " -" + text
            text = algo.caesarEncode(text,int(delay))
        newimg = stega.encode(address, text)
        new_img_name = "encoded.png"
        newimg.save(os.path.join(app.config['UPLOAD_FOLDER'], new_img_name))
        os.remove(address)
        return render_template("finalEncode.html")
    else:
        return render_template("error.html")

@app.route("/walkThrough")
def walkThrough():
    return render_template("walkThrough.html")




if __name__ == "__main__":
  app.run(debug=True)
