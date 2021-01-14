from flask import Flask, render_template, jsonify, request, redirect, url_for, make_response
import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
import requests

with open("config.json", encoding='utf 8') as json_file:
    data = json.load(json_file)
    config = data["firebase"]
    firebase = pyrebase.initialize_app(config) # database
    pb = pyrebase.initialize_app(config) # ใช้ต่างกัน authen
    db = firebase.database()

# db.child('food').set({'key' : 'value'})


cred = credentials.Certificate("loginjson.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)


@app.route('/')
@app.route('/homepage')
def test():
    return render_template('/main/welcome.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        firstname = request.form['firstname'] 
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['pword']

        try:
            user = auth.create_user(email=email, password=password, display_name=username)
            data = {'firstname':firstname, 'lastname':lastname, 'email':user.email, 
                    'username':user.display_name, 'password':password, 'userToken':user.uid}
            db.child('food').push(data)
            return redirect(url_for("signup"))
        except:
            return render_template("signup.html")


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        pb.auth().sign_in_with_email_and_password(email, password)
        return redirect(url_for("test"))

#---------------------Food-Tanny------------------------#


@app.route('/getapi', methods=['GET',"POST"])
def getapi():
    if request.method == 'POST':
        event = request.get_json()
        print("CheckData :",event)
        
        
        keyword = event['keyword']
        revision = event['revision']
        imex_type = event['imex_type']
        order_by = event['order_by']

        url = f"https://dataapi.moc.go.th/products?keyword={keyword}"
        response = requests.get(url, verify=False)
        texts = response.json()
        lst = []
        for i in texts:
            group = {'revision':i['revision'], 'hs_code':i['hs_code'], 'com_code': i['com_code'], 
                    'imex_type':i['type'], 'com_description_en':i['com_description_en'], 'com_description_th':i['com_description_th'], 
                    'unit_code':i['unit_code'], 'unit':i['unit'], 'unit2en':i['unit2en'], 'unit2th':i['unit2th']}
            lst.append(group)
        
        data = {
            'ref':lst
        }
        print(data)
        return jsonify(data)
    else:
        return render_template('/trainRPA/table.html')
    

@app.route('/tbproduct')
def tbproduct():
    return render_template('/trainRPA/test.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)

