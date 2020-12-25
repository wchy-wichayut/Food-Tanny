from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth

with open("config.json", encoding='utf 8') as json_file:
    data = json.load(json_file)
    config = data["firebase"]
    firebase = pyrebase.initialize_app(config)
    pb = pyrebase.initialize_app(config)
    db = firebase.database()

# db.child('food').set({'key' : 'value'})

cred = credentials.Certificate("loginjson.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)


@app.route('/')
@app.route('/test')
def test():
    return render_template('test.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        firstname = request.form['firstname'] 
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        try:
            user = auth.create_user(email=email, password=password, display_name=username)
            data = {'firstname':firstname, 'lastname':lastname, 'email':user.email, 
                    'username':user.display_name, 'password':password, 'userToken':user.uid}
            db.child('food').push(data)
            return redirect(url_for("login"))
        except:
            return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        pb.auth().sign_in_with_email_and_password(email, password)
        return redirect(url_for("test"))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
