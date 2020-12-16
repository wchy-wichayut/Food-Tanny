from json import encoder
from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import pyrebase
from firebase_admin import auth

with open("config.json", encoding='utf 8') as json_file:
    data = json.load(json_file)
    config = data["firebase"]
    firebase = pyrebase.initialize_app(config)
    pb = pyrebase.initialize_app(config)
    db = firebase.database()

# db.child('food').set({'key' : 'value'})

app = Flask(__name__)


@app.route('/')
@app.route('/test')
def test():
    return render_template('test.html')
# @app.route('/index')
# def index():
#     return render_template('index.html')


@app.route('/loginsignup', methods=["GET", "POST"])
def login_signup():
    if request.method == "GET":
        return render_template("loginSignup.html")
    elif request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        username = request.form['username']
        password = request.form['password']
        user = auth.create_user(email=email, password=password, display_name=username)
        data = {'firstname':firstname, 'lastname':lastname, 'email':user.email,
                'password':password, 'userToken':user.uid, 'username':user.display_name}
        db.child('food').push(data)
        return render_template('login.html')
        


if __name__ == '__main__':
    app.run(debug=True, port=8080)
